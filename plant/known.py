"""Known (specified) variables for each unit's degree-of-freedom analysis, with values and SI units.

Every value is read from the model's own constants and function defaults (plant/physics.py, plant/ai.py,
plant/packed_bed.py), or computed from them, for the standard recipe: 800 um grind, 93 C kettle, 4 min steep,
15 g coffee in 250 g water, 20 s plunge. Nothing here is retyped by hand, so the DOF tables cannot drift from the
code. Each row is (symbol, meaning, value, SI unit, source).
Sources: [C15] Corrochano 2015, [M16] Moroney 2016, [IAPWS] water properties via CoolProp, "assumed" = our choice.
"""
import inspect

import numpy as np

from plant import ai, physics as ph

D = 800e-6                  # standard grind, m
T_W = 93 + 273.15           # standard kettle temperature, K
T_S = 240.0                 # standard steep time, s


def _defaults(fn):
    return {k: v.default for k, v in inspect.signature(fn).parameters.items() if v.default is not inspect._empty}


def _standard():
    b = _defaults(ph.brew)
    p = _defaults(ph.plunge)
    out = ph.brew(D, T_W, T_S, m_coffee=b["m_coffee"], m_water=b["m_water"])
    T_end = float(out["T"][-1])
    rho_w, mu_w, cp_w = ph.water(T_W)
    rho_e, mu_e, _ = ph.water(T_end)
    return b, p, T_end, (rho_w, mu_w, cp_w), (rho_e, mu_e)


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _f(x, digits=3):
    """Number with `digits` significant figures; very small or large values as m × 10ⁿ."""
    if x != 0 and not 1e-2 <= abs(x) < 1e5:
        m, e = f"{x:.{digits - 1}e}".split("e")
        return f"{float(m):g} × 10{str(int(e)).translate(SUP)}"
    return f"{x:.{digits}g}"


def known_variables():
    """{unit name in plant.steps.UNITS: [rows]}."""
    b, p, T_end, (rho_w, mu_w, cp_w), (rho_e, mu_e) = _standard()
    m_c, m_w = b["m_coffee"], b["m_water"]
    recipe = [
        ("d", "nominal grind diameter", _f(D), "m", "setpoint"),
        ("T_w", "kettle water temperature", _f(T_W, 5), "K", "setpoint (93 °C)"),
        ("t_s", "steep time", _f(T_S), "s", "setpoint"),
        ("R_w", "brew ratio m_w / m_c", _f(m_w / m_c), "1", "setpoint"),
        ("m_c", "dry coffee dose", _f(m_c), "kg", "fixed"),
    ]
    liquid_end = [("rho", "water density at the end-of-steep temperature", _f(rho_e, 4), "kg/m³", "[IAPWS]"),
                  ("mu", "water viscosity at the end-of-steep temperature", _f(mu_e), "Pa s", "[IAPWS]")]
    bed = [
        ("w_f", "fines mass fraction", _f(p["fines_fraction"]), "1", "assumed"),
        ("d_f", "fines diameter (one coffee cell)", _f(ph.CELL_SIZE), "m", "[M16]"),
        ("phi_s", "sphericity", _f(p["sphericity"]), "1", "[C15]"),
        ("epsilon", "bed porosity", _f(p["eps_bed"]), "1", "assumed"),
    ]
    plunge = [
        ("T", "bed temperature during the plunge (end of steep)", _f(T_end, 4), "K", "model"),
        ("t_p", "plunge time", _f(p["plunge_time"]), "s", "assumed"),
        ("V_l", "liquid volume pushed through the cake", _f(p["V_liquid"]), "m³", "assumed"),
        ("D_p", "press inner diameter", _f(p["D_press"]), "m", "assumed"),
        ("rho_b", "cake bulk density", _f(p["rho_bulk"]), "kg/m³", "[C15: 360–480]"),
        ("R_m", "mesh resistance", _f(p["R_mesh"]), "1/m", "assumed"),
        ("m_c", "dry coffee dose", _f(p["m_coffee"]), "kg", "fixed"),
    ]
    A = np.pi * p["D_press"] ** 2 / 4
    u = p["V_liquid"] / (A * p["plunge_time"])
    d_s = p["sphericity"] * ph.sauter_diameter(D, p["fines_fraction"])
    flow = [("u", "superficial velocity (from V_l, D_p and t_p)", _f(u), "m/s", "computed"),
            ("d_s", "Ergun diameter phi_s d32 (from d, w_f, d_f)", _f(d_s), "m", "computed")]
    extraction = recipe + [
        ("m_w", "water mass", _f(m_w), "kg", "fixed"),
        ("x_E", "extractable mass fraction", _f(ph.X_EXTRACTABLE), "1", "[M16]"),
        ("c_sat", "solubility of coffee solubles", _f(ph.C_SAT, 4), "kg/m³", "[M16]"),
        ("tau_s,ref", "surface dissolution time at d_ref, 90 °C", _f(ph.TAU_S_REF), "s", "[M16]"),
        ("tau_d,ref", "diffusion time at d_ref, 90 °C", _f(ph.TAU_D_REF), "s", "[M16]"),
        ("d_ref", "reference grind (Sauter)", _f(ph.D_REF), "m", "[M16]"),
        ("T_ref", "reference temperature", _f(ph.T_REF, 5), "K", "[M16]"),
        ("rho_s", "coffee solid density", _f(ph.RHO_SOLID, 4), "kg/m³", "[C15]"),
        ("epsilon_p", "porosity inside a grain", _f(ph.EPS_PARTICLE), "1", "[C15]"),
    ]
    cooling = [
        ("m_w", "water mass", _f(m_w), "kg", "fixed"),
        ("c_p,w", "water specific heat at T_w", _f(cp_w, 4), "J/(kg K)", "[IAPWS]"),
        ("m_c", "dry coffee dose", _f(m_c), "kg", "fixed"),
        ("c_p,c", "coffee specific heat", _f(ph.CP_COFFEE, 4), "J/(kg K)", "assumed"),
        ("m_v", "press (vessel) mass", _f(b["m_vessel"]), "kg", "assumed"),
        ("c_p,v", "press specific heat (glass)", _f(b["cp_vessel"]), "J/(kg K)", "assumed"),
        ("T_w", "kettle water temperature", _f(T_W, 5), "K", "setpoint"),
        ("T_inf", "room temperature", _f(b["T_amb"], 5), "K", "assumed"),
        ("UA", "heat-loss conductance of the press", _f(b["UA"]), "W/K", "assumed"),
    ]
    rho_p = ph.settling(ph.CELL_SIZE, T_end)["rho_p"]
    stokes = [
        ("d_p", "fine particle diameter", _f(ph.CELL_SIZE), "m", "[M16]"),
        ("rho_p", "wet particle density", _f(rho_p, 4), "kg/m³", "from [C15]"),
        *liquid_end,
        ("g", "gravitational acceleration", _f(ph.G), "m/s²", "standard"),
        ("H", "cup depth", _f(_defaults(ph.settling)["depth"]), "m", "assumed"),
    ]
    lo, hi = ai.LO, ai.HI
    ai_rows = [
        ("d range", "grind bounds", f"{_f(lo[0] * 1e-6)} to {_f(hi[0] * 1e-6)}", "m", "operator limits"),
        ("T_w range", "kettle bounds", f"{lo[1] + 273.15:g} to {hi[1] + 273.15:g}", "K", "operator limits"),
        ("t_s range", "steep bounds", f"{lo[2]:g} to {hi[2]:g}", "s", "operator limits"),
        ("R_w range", "ratio bounds", f"{lo[3]:g} to {hi[3]:g}", "1", "operator limits"),
        ("TDS box", "target strength", f"{ph.TDS_RANGE[0]:g} to {ph.TDS_RANGE[1]:g}", "1", "SCA"),
        ("EY box", "target extraction yield", f"{ph.EY_RANGE[0]:g} to {ph.EY_RANGE[1]:g}", "1", "SCA"),
        ("sigma_n", "TDS meter noise (standard deviation)", _f(ai.TDS_METER_SD), "1", "assumed"),
        ("N_cand", "random candidates per suggestion", _f(_defaults(ai.suggest)["n_candidates"]), "1", "choice"),
    ]
    return {
        "Plant overview & DOF": recipe + [("m_w", "water mass", _f(m_w), "kg", "fixed")],
        "Dimensional analysis (packed bed)": flow + [("epsilon", "bed porosity", _f(p["eps_bed"]), "1", "assumed")] + liquid_end,
        "Ergun equation (F-101)": flow + bed + liquid_end,
        "Extraction balance (R-101)": extraction,
        "Energy balance (R-101)": cooling,
        "Plunge filtration (F-101)": [("d", "nominal grind diameter", _f(D), "m", "setpoint")] + bed + plunge + liquid_end,
        "Channeling (F-101)": [("epsilon", "bed porosity", "0.4", "1", "assumed"),
                               ("epsilon_c", "channel porosity (example)", "0.5", "1", "example"),
                               ("a_c", "channel area fraction (example)", "0.1", "1", "example")] + flow + liquid_end,
        "Stokes settling (T-101)": stokes,
        "AI operator": ai_rows,
    }
