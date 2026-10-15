"""AI operator: Bayesian optimization of the French press recipe, plus honest baselines.

Setpoints x = (grind d in um, water temperature in C, steep time in s, water-to-coffee ratio in g/g).
Each batch is "measured" with a noisy TDS meter, like a real lab. The AI fits a Gaussian process
(scikit-learn) to the batches so far and picks the next recipe with the largest expected improvement.
"""
import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from plant import physics as ph

# Setpoint names, units and allowed ranges (lower, upper)
BOUNDS = {
    "grind_um": (300.0, 1200.0),
    "T_water_C": (85.0, 96.0),
    "steep_s": (60.0, 600.0),
    "ratio": (12.0, 20.0),
}
NAMES = list(BOUNDS)
LO = np.array([b[0] for b in BOUNDS.values()])
HI = np.array([b[1] for b in BOUNDS.values()])
STANDARD_RECIPE = {"grind_um": 800.0, "T_water_C": 93.0, "steep_s": 240.0, "ratio": 16.7}
TDS_METER_SD = 0.0003     # standard deviation of the TDS meter reading, - (0.03 % TDS, ASSUMED)
TDS_TARGET, EY_TARGET = 0.0125, 0.20   # centre of the SCA ideal box


def run_batch(x, rng=None, m_coffee=0.015, check_bounds=True, **brew_options):
    """Brew one virtual batch at setpoints x (dict). Returns measured TDS, EY and the full simulation.
    If rng is given, the TDS reading gets meter noise; EY is computed from the measured TDS,
    exactly as you would in a real lab: EY = TDS * beverage mass / coffee mass.
    check_bounds=False lets a human operator go outside the AI's search box (physics still rejects
    impossible inputs). brew_options are passed on to physics.brew (e.g. preheated=True)."""
    for k, (lo, hi) in BOUNDS.items():
        if check_bounds and not lo <= x[k] <= hi:
            raise ValueError(f"{k} = {x[k]} is outside the allowed range {lo}-{hi}.")
    sim = ph.brew(x["grind_um"] * 1e-6, x["T_water_C"] + 273.15, x["steep_s"],
                  m_coffee=m_coffee, m_water=m_coffee * x["ratio"], **brew_options)
    tds = sim["TDS"] + (rng.normal(0, TDS_METER_SD) if rng is not None else 0.0)
    ey = tds * sim["m_beverage"] / m_coffee
    return {"TDS": tds, "EY": ey, "sim": sim}


def score(tds, ey):
    """Distance from the centre of the SCA box, scaled by the box half-widths (-). 0 is perfect;
    any cup inside the box scores at most sqrt(2)."""
    return float(np.hypot((tds - TDS_TARGET) / 0.001, (ey - EY_TARGET) / 0.02))


def to_unit(x):
    return (np.array([x[k] for k in NAMES]) - LO) / (HI - LO)


STEP = np.array([10.0, 0.5, 10.0, 0.1])   # setpoint resolution an operator can actually dial in


def from_unit(u):
    """Unit-cube point to setpoints, rounded to the dial resolution STEP."""
    x = np.clip(np.round((LO + np.asarray(u) * (HI - LO)) / STEP) * STEP, LO, HI)
    return {k: float(v) for k, v in zip(NAMES, x)}


def fit_gp(X, y):
    """Gaussian process (Matern 5/2 kernel + noise) fitted to inputs X (unit cube) and outputs y."""
    kernel = ConstantKernel(1.0) * Matern(length_scale=np.full(X.shape[1], 0.3), nu=2.5) + WhiteKernel(1e-4)
    return GaussianProcessRegressor(kernel, normalize_y=True, n_restarts_optimizer=2, random_state=0).fit(X, y)


def suggest(history, rng, n_candidates=3000, n_start=3):
    """Next recipe. history: list of (x dict, measured TDS, measured EY).
    The AI fits one Gaussian process to TDS and one to EY, then picks the candidate recipe with the
    highest probability of landing inside the SCA box:
        P(in box) = P(TDS_lo < TDS < TDS_hi) * P(EY_lo < EY < EY_hi)
    using each GP's predicted mean and standard deviation (normal distributions)."""
    if len(history) < n_start:
        return from_unit(rng.uniform(size=len(NAMES))), {"reason": "random start (too little data for a model)"}
    X = np.array([to_unit(x) for x, _, _ in history])
    gp_tds = fit_gp(X, np.array([t for _, t, _ in history]))
    gp_ey = fit_gp(X, np.array([e for _, _, e in history]))
    cand = rng.uniform(size=(n_candidates, len(NAMES)))
    m_t, s_t = gp_tds.predict(cand, return_std=True)
    m_e, s_e = gp_ey.predict(cand, return_std=True)
    s_t, s_e = np.maximum(s_t, 1e-9), np.maximum(s_e, 1e-9)
    p_t = norm.cdf((ph.TDS_RANGE[1] - m_t) / s_t) - norm.cdf((ph.TDS_RANGE[0] - m_t) / s_t)
    p_e = norm.cdf((ph.EY_RANGE[1] - m_e) / s_e) - norm.cdf((ph.EY_RANGE[0] - m_e) / s_e)
    p = p_t * p_e
    i = int(np.argmax(p))
    return from_unit(cand[i]), {
        "reason": f"highest predicted chance of an ideal cup ({100 * p[i]:.0f} %)",
        "pred_TDS": float(m_t[i]), "pred_TDS_sd": float(s_t[i]),
        "pred_EY": float(m_e[i]), "pred_EY_sd": float(s_e[i]), "p_in_box": float(p[i])}


def random_strategy(history, rng):
    return from_unit(rng.uniform(size=len(NAMES))), {"reason": "random"}


def ofat_plan():
    """One-factor-at-a-time, the classic lab approach: start at the standard recipe and vary one setpoint
    at a time over 3 levels, keeping the best value before moving to the next setpoint."""
    return [("grind_um", [500.0, 800.0, 1100.0]), ("steep_s", [120.0, 240.0, 480.0]),
            ("T_water_C", [88.0, 93.0, 96.0]), ("ratio", [14.0, 16.7, 19.0])]


def run_campaign(strategy, budget, seed):
    """Run up to `budget` batches with strategy 'ai', 'random' or 'ofat'.
    Returns the list of (x, measured TDS, measured EY, score) and the batch number of the first
    in-box cup (None if never)."""
    rng = np.random.default_rng(seed)
    history, log, first_hit = [], [], None
    plan = [(k, v) for k, levels in ofat_plan() for v in levels]
    current = dict(STANDARD_RECIPE)
    best_val = {}
    for n in range(budget):
        if strategy == "ai":
            x, _ = suggest(history, rng)
        elif strategy == "random":
            x, _ = random_strategy(history, rng)
        else:
            if n >= len(plan):
                break
            k, v = plan[n]
            # once all levels of the previous setpoint are tried, lock in its best level
            for kk, (val, _) in best_val.items():
                if kk != k:
                    current[kk] = val
            x = dict(current, **{k: v})
        r = run_batch(x, rng)
        s = score(r["TDS"], r["EY"])
        history.append((x, r["TDS"], r["EY"]))
        log.append((x, r["TDS"], r["EY"], s))
        if strategy == "ofat":
            k = plan[n][0]
            if k not in best_val or s < best_val[k][1]:
                best_val[k] = (x[k], s)
        if first_hit is None and ph.in_target(r["TDS"], r["EY"]):
            first_hit = n + 1
    return log, first_hit


def benchmark(budget=12, seeds=20):
    """Batches needed to reach the SCA box for each strategy over many seeds.
    Returns {strategy: list of first-hit batch numbers (None = missed)}."""
    return {s: [run_campaign(s, budget, seed)[1] for seed in range(seeds)] for s in ["ai", "random", "ofat"]}
