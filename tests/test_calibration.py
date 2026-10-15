import numpy as np
from plant import calibration as cal


def test_fit_recovers_known_parameters_from_synthetic_data():
    # Synthetic data from known parameters, sampled like the coarse experiment, plus seeded noise.
    t, _ = cal.measured("coarse")
    true = np.array([np.log(20.0), np.log(300.0), 0.5, 1.6])
    rng = np.random.default_rng(1)
    y = cal.curve(true, t) + rng.normal(0, 0.01, t.size)
    s = cal.summary(cal.fit(t, y, [10.0, 100.0, 0.3, 1.0]))
    for name, value in zip(["tau_s", "tau_d", "phi", "A"], [20.0, 300.0, 0.5, 1.6]):
        best, lo, hi = s[name]
        width = hi - lo
        assert lo - 1.5 * width <= value <= hi + 1.5 * width, (name, s[name])   # within about 2 sigma


def test_fine_grind_diffusion_time_matches_the_paper():
    s = cal.summary(cal.calibrate("fine"))
    best, lo, hi = s["tau_d"]
    assert lo <= 42.2 <= hi                      # Moroney's fitted diffusion time lies in our 1-sigma range
    assert abs(s["phi"][0] - 0.46) < 0.1         # geometric fast fraction at 322 um is 0.46


def test_calibration_residuals_are_small():
    for grind in ["fine", "coarse"]:
        r = cal.calibrate(grind)
        assert r["rms"] < 0.03, grind
