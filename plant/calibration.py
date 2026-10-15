"""Calibrate the extraction model against measured data from Moroney et al. (2016), Figure 5.

The experiment: 60 g of coffee in 0.5 L of hot water, well mixed (the same situation as our press), with
the dissolved concentration measured over time. The figure gives concentration on an unknown dimensionless
scale, so the fit uses the curve's shape plus a free amplitude A:

    data(t) = A * m_l(t) / M_E        (m_l / M_E from physics.extraction_isothermal)

Fitted parameters: ln tau_s, ln tau_d (logs keep them positive), fast fraction phi, amplitude A.
Uncertainty: linearised least squares, cov = s^2 (J^T J)^-1 with s^2 the residual variance.
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from plant import physics

DATA = json.loads((Path(__file__).resolve().parents[1] / "data" / "moroney2016_fig5.json").read_text())
M_COFFEE, M_WATER, T_EXPERIMENT = 0.060, 0.500, 363.15   # 60 g in 0.5 L; 90 C assumed (paper's quoted temperature)
NAMES = ["tau_s", "tau_d", "phi", "A"]


def measured(grind):
    """Measured points for 'fine' or 'coarse': physical time (s) and dimensionless concentration (-)."""
    g = DATA[grind]
    return np.array(g["t"]) * g["t_s"], np.array(g["c_h"])


def curve(p, t):
    """Model curve A * m_l/M_E at times t (s) for parameters p = [ln tau_s, ln tau_d, phi, A]."""
    return p[3] * physics.extraction_isothermal(t, np.exp(p[0]), np.exp(p[1]), p[2], M_COFFEE, M_WATER, T_EXPERIMENT)


def fit(t, y, p0):
    """Least-squares fit of curve() to (t, y). Returns best parameters, covariance and residuals.
    p0: starting guess [tau_s, tau_d, phi, A] in natural units."""
    x0 = [np.log(p0[0]), np.log(p0[1]), p0[2], p0[3]]
    r = least_squares(lambda p: curve(p, t) - y, x0, bounds=([-5, 0, 0.01, 0.1], [8, 10, 0.99, 10]))
    s2 = np.sum(r.fun**2) / (len(y) - len(x0))
    cov = s2 * np.linalg.inv(r.jac.T @ r.jac)
    return {"p": r.x, "cov": cov, "residuals": r.fun, "rms": np.sqrt(s2)}


def summary(result):
    """Best values with 1-sigma ranges in natural units. Time scales were fitted as logs, so their range is
    multiplicative: [best / k, best * k] with k = exp(sigma)."""
    p, sd = result["p"], np.sqrt(np.diag(result["cov"]))
    return {"tau_s": (np.exp(p[0]), np.exp(p[0] - sd[0]), np.exp(p[0] + sd[0])),
            "tau_d": (np.exp(p[1]), np.exp(p[1] - sd[1]), np.exp(p[1] + sd[1])),
            "phi": (p[2], p[2] - sd[2], p[2] + sd[2]), "A": (p[3], p[3] - sd[3], p[3] + sd[3])}


def band(result, t, n=300, seed=0):
    """95 % band of the model curve: sample parameters from the fitted normal distribution (seeded)."""
    rng = np.random.default_rng(seed)
    samples = rng.multivariate_normal(result["p"], result["cov"], size=n)
    samples[:, 2] = np.clip(samples[:, 2], 0.01, 0.99)
    curves = np.array([curve(s, t) for s in samples])
    return np.percentile(curves, 2.5, axis=0), np.percentile(curves, 97.5, axis=0)


def calibrate(grind):
    """Fit the model to one grind of the published data, starting from Moroney's own time scales."""
    t, y = measured(grind)
    return fit(t, y, [DATA[grind]["t_s"], DATA[grind]["t_d"], 0.5, y.max()])
