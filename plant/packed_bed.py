"""Packed-bed analysis for the app: the Ergun chart, the grind-size sweep, and the check against measured
coffee-bed permeability from Corrochano et al. (2015) [C15]. Physics lives in plant.physics; this module only
arranges it for plots and tests.
"""
import json
from pathlib import Path

import numpy as np

from plant import physics

C15 = json.loads((Path(__file__).resolve().parents[1] / "data" / "corrochano2015.json").read_text())


def ergun_curve(Re_b):
    """Ergun's dimensionless form f_p = 150/Re_b + 1.75 (-), for bed Reynolds numbers Re_b (-)."""
    return physics.ERGUN_VISCOUS / np.asarray(Re_b) + physics.ERGUN_INERTIAL


def brewer_points(plunge_result, T_press):
    """Where three brewers sit on the Ergun chart. Every point is on the curve by construction (Ergun is
    evaluated, not measured), so the chart shows each brewer's regime, not a test of the equation.
    plunge_result: physics.plunge() output for the live French press batch; T_press: its temperature (K).
    Espresso and pour-over use TYPICAL recipes (ASSUMED values, listed here so they can be checked):
      espresso: 36 g out in 27 s through a 58 mm basket, d32 = 101.6 um and eps = 0.20 (both [C15]), 93 C
      pour-over: 300 g in 180 s through a 60 mm bed, 600 um grind with 15 % fines, eps = 0.40, 93 C"""
    out = []
    for name, u, d_s, eps, T in [
        ("Espresso", 36e-3 / 965 / 27 / (np.pi * 0.029**2), physics.SPHERICITY * 101.6e-6, 0.20, 366.15),
        ("Pour-over", 0.300 / 965 / 180 / (np.pi * 0.030**2),
         physics.SPHERICITY * physics.sauter_diameter(600e-6, 0.15), 0.40, 366.15),
    ]:
        e = physics.ergun(u, d_s, eps, T)
        out.append({"name": name, "u": u, "Re_b": e["Re_b"], "f_p": e["f_p"], "inertial_share": e["inertial_share"]})
    out.append({"name": "French press (live)", "u": plunge_result["u"], "Re_b": plunge_result["Re_b"],
                "f_p": plunge_result["f_p"], "inertial_share": plunge_result["inertial_share"]})
    return out


def corrochano_check():
    """Compare Ergun's viscous limit with measured coffee-bed permeability [C15].
    Ergun predicts k = d_s^2 eps^3 / (150 (1 - eps)^2) with d_s = sphericity * d32. Turning it round, each
    measurement gives the constant that would have matched it: C_eff = d_s^2 eps^3 / (k (1 - eps)^2) (-).
    Ergun says C_eff = 150. Inputs are the paper's measured d32, k, sphericity and (digitized) porosity.
    Returns one row per grind and bulk density."""
    rows = []
    for i, name in enumerate(C15["names"]):
        d_s = C15["sphericity"] * C15["d32_m"][i]
        for j, rho_bulk in enumerate(C15["bulk_density_kg_m3"]):
            eps, k, k_sd = C15["eps_bed"][i][j], C15["k_m2"][i][j], C15["k_sd_m2"][i][j]
            k_pred = physics.permeability(d_s, eps)
            C_eff = d_s**2 * eps**3 / (k * (1 - eps) ** 2)
            rows.append({"grind": name, "d32_um": 1e6 * C15["d32_m"][i], "rho_bulk": rho_bulk, "eps": eps,
                         "k_measured": k, "k_sd": k_sd, "k_ergun": k_pred, "ratio": k_pred / k,
                         "C_eff": C_eff, "C_eff_sd": C_eff * k_sd / k})
    return rows


def grind_sweep(grinds_um, T_water, t_steep, m_coffee, m_water, preheated, plunge_time, fines_fraction):
    """Trade-off across grind sizes (um) for one recipe: plunge force with the chosen fines and with no fines,
    Re_b, permeability, and the cup (strength TDS and extraction yield EY). The plunge is evaluated at the
    brew's end temperature. Other inputs as in physics.brew and physics.plunge (SI units)."""
    out = {k: [] for k in ["grind_um", "force", "force_no_fines", "k", "Re_b", "d32_um", "TDS", "EY"]}
    for g in grinds_um:
        b = physics.brew(g * 1e-6, T_water, t_steep, m_coffee=m_coffee, m_water=m_water, preheated=preheated)
        T_end = float(b["T"][-1])
        p = physics.plunge(g * 1e-6, T_end, m_coffee=m_coffee, plunge_time=plunge_time, fines_fraction=fines_fraction)
        p0 = physics.plunge(g * 1e-6, T_end, m_coffee=m_coffee, plunge_time=plunge_time, fines_fraction=0.0)
        for k, v in [("grind_um", g), ("force", p["force"]), ("force_no_fines", p0["force"]), ("k", p["k"]),
                     ("Re_b", p["Re_b"]), ("d32_um", 1e6 * p["d32"]), ("TDS", b["TDS"]), ("EY", b["EY"])]:
            out[k].append(float(v))
    return out


# Three made-up beds that differ in grain size and packing, for the collapse plot: (label, d_s in m, eps).
COLLAPSE_BEDS = [("fine, tight (espresso-like)", 75e-6, 0.25), ("medium (French press)", 125e-6, 0.40),
                 ("coarse, loose", 600e-6, 0.45)]
C15_RE_RANGE = (0.04, 4.0)   # particle Reynolds numbers measured in Corrochano's coffee beds [C15, Section 4.2]


def collapse_data(T, u=np.logspace(-4, 0, 60)):
    """Ergun evaluated for COLLAPSE_BEDS over superficial velocities u (m/s) at temperature T (K).
    In dimensional form (dP/L vs u) the beds give three separate curves; as f_p vs Re_b they fall on one.
    The collapse here is by construction (it's Ergun); Ergun's 1952 point was that measured beds collapse."""
    return [{"label": lab, "u": u, **physics.ergun(u, d_s, eps, T)} for lab, d_s, eps in COLLAPSE_BEDS]
