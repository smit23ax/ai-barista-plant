"""Numbers and figures for the submission website. Everything is computed from plant.physics / plant.packed_bed
(the tested model), so the website never retypes a number by hand.

Symbols (SI units):
  d       nominal grind size (m);  d32  Sauter mean diameter (m);  d_s = Phi_s * d32  Ergun diameter (m)
  eps     bed porosity (-);  K  permeability (m^2);  u  superficial velocity (m/s);  T  temperature (K)
  dP      pressure drop (Pa);  F  plunge force (N);  Re_b  bed Reynolds number (-);  f_p  friction factor (-)
  rho_b   bulk density of the grounds cake (kg/m^3);  mu  water viscosity (Pa s)
"""
import numpy as np
import plotly.graph_objects as go

from plant import packed_bed as pb, physics as ph, style
from site_src import explorer

# ---------------------------------------------------------------- Wadsworth et al. (2021), Am. J. Phys. 89, 769
# Values copied from the open-access published version (Edinburgh Research Explorer PDF), read 2026-11-05:
# 1 L press, internal radius 4.75 cm; 54 g coffee; cake bulk density 230 kg/m^3, porosity 0.53;
# Sauter radius ~80 um (they take it from Corrochano); lab-fitted permeability (1.34 +/- 0.10) x 10^-12 m^2;
# lab force ~12.5 N for 54 g at <u> ~ 1e-4 m/s (caption gives 2.8e-4 m/s); viscosity used 8.9e-4 Pa s.
W21 = {"R_press": 0.0475, "m": 0.054, "rho_bulk": 230.0, "eps": 0.53, "d32": 160e-6,
       "k_measured": 1.34e-12, "k_sd": 0.10e-12, "F_lab": 12.5, "u_lab": 1e-4, "mu": 8.9e-4}


def wadsworth_check():
    """Ergun's viscous-limit permeability with the project's conventions (d_s = 0.75 d32) at Wadsworth's bed,
    against their measured permeability, and the Darcy force each permeability gives at their lab speed."""
    d_s = ph.SPHERICITY * W21["d32"]
    k_ergun = ph.permeability(d_s, W21["eps"])
    A = np.pi * W21["R_press"] ** 2
    L = W21["m"] / (W21["rho_bulk"] * A)
    F_from_k = lambda k: W21["mu"] * W21["u_lab"] * L * A / k          # Darcy: F = dP A = mu u L A / k
    return {"k_ergun": k_ergun, "ratio_ergun": k_ergun / W21["k_measured"],
            "A": A, "L": L,
            "F_ergun": F_from_k(k_ergun), "F_measured_k": F_from_k(W21["k_measured"])}


def corrochano_rows():
    return pb.corrochano_check()


def implied_porosity():
    """Porosity implied by the model's own bulk density and particle (envelope) density: eps = 1 - rho_b / rho_env,
    rho_env = rho_solid (1 - eps_particle)."""
    rho_env = ph.RHO_SOLID * (1 - ph.EPS_PARTICLE)
    return {"rho_env": rho_env, "eps": 1 - 400.0 / rho_env}


def sensitivity(d=800e-6, T=explorer.T_PLUNGE):
    """Plunge force (N) at one grind when one assumed input changes and the rest stay at the model defaults."""
    base = ph.plunge(d, T)["force"]
    cases = [("porosity ε", "eps_bed", [0.30, 0.36, 0.40, 0.50]),
             ("mesh R_m (1/m)", "R_mesh", [1e8, 2e8, 4e8]),
             ("fines w_f", "fines_fraction", [0.0, 0.05, 0.10, 0.15, 0.25])]
    rows = []
    for label, key, values in cases:
        for v in values:
            rows.append({"input": label, "value": v, "force": ph.plunge(d, T, **{key: v})["force"]})
    return {"base": base, "rows": rows}


def crossover_Re():
    """Bed Reynolds number where Ergun's viscous and inertial terms are equal: 150/Re_b = 1.75."""
    return ph.ERGUN_VISCOUS / ph.ERGUN_INERTIAL


def numbers():
    """Every number the pages quote, rounded only at display time."""
    s = explorer.sweep()
    g = list(explorer.GRID_UM)
    pick = lambda key, um: s[key][g.index(um)]
    rows = corrochano_rows()
    ratios = [r["ratio"] for r in rows]
    w = wadsworth_check()
    brew = ph.brew(800e-6, 93 + 273.15, 240, m_coffee=0.015, m_water=0.015 * 16.7)
    return {
        "K300": pick("k", 300), "K1200": pick("k", 1200), "K800": pick("k", 800),
        "dP800": pick("dP", 800), "dPcake800": pick("dP_cake", 800), "dPmesh800": pick("dP_mesh", 800),
        "F800": pick("force", 800), "F300": pick("force", 300), "F1200": pick("force", 1200),
        "Re800": pick("Re_b", 800), "inert800": pick("inertial_share", 800),
        "mesh_share800": pick("dP_mesh", 800) / pick("dP", 800),
        "c15_min": min(ratios), "c15_max": max(ratios), "c15_Ceff_min": 150 * min(ratios), "c15_Ceff_max": 150 * max(ratios),
        "w21": w, "eps_implied": implied_porosity(), "Re_cross": crossover_Re(),
        "T_end": float(brew["T"][-1]), "TDS": brew["TDS"], "EY": brew["EY"],
    }


# ---------------------------------------------------------------- figures
def parity_figure():
    """Permeability predicted by Ergun (project conventions) vs measured, for Corrochano's 12 espresso-style beds
    and Wadsworth's French-press bed. Points above the 1:1 line mean Ergun over-predicts K."""
    rows = corrochano_rows()
    w = wadsworth_check()
    fig = go.Figure()
    lo, hi = 1e-14, 1e-10
    fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="1:1 (perfect)", line=dict(color=style.COLORS["grey"])))
    fig.add_trace(go.Scatter(x=[lo, hi], y=[10 * lo, 10 * hi], mode="lines", name="10× over-prediction",
                             line=dict(color=style.COLORS["grey"], dash="dot")))
    fig.add_trace(go.Scatter(
        x=[r["k_measured"] for r in rows], y=[r["k_ergun"] for r in rows], mode="markers",
        name="Corrochano 2015 (espresso-style beds)", marker=dict(size=9, color=style.COLORS["coffee"]),
        error_x=dict(type="data", array=[r["k_sd"] for r in rows], thickness=1),
        text=[f"grind {r['grind']}, ρ_b {r['rho_bulk']} kg/m³" for r in rows], hovertemplate="%{text}<extra></extra>"))
    fig.add_trace(go.Scatter(x=[W21["k_measured"]], y=[w["k_ergun"]], mode="markers", name="Wadsworth 2021 (French press)",
                             marker=dict(size=13, symbol="diamond", color=style.COLORS["alarm"]),
                             error_x=dict(type="data", array=[W21["k_sd"]], thickness=1)))
    fig.update_layout(height=460, margin=dict(l=80, r=20, t=30, b=110),
                      legend=dict(orientation="h", x=0, y=-0.22, yanchor="top"))
    fig.update_xaxes(type="log", range=[np.log10(lo), np.log10(hi)], title_text="measured K (m²)", exponentformat="power")
    fig.update_yaxes(type="log", range=[np.log10(lo), np.log10(hi)], title_text="Ergun-predicted K (m²)", exponentformat="power")
    return fig


def ceff_figure():
    """C_eff (the viscous constant that would have matched each measurement) against the Sauter diameter, Corrochano 2015."""
    rows = corrochano_rows()
    fig = go.Figure()
    for rho in sorted({r["rho_bulk"] for r in rows}):
        sub = [r for r in rows if r["rho_bulk"] == rho]
        fig.add_trace(go.Scatter(x=[r["d32_um"] for r in sub], y=[r["C_eff"] for r in sub], mode="lines+markers",
                                 name=f"ρ_b = {rho} kg/m³", error_y=dict(type="data", array=[r["C_eff_sd"] for r in sub], thickness=1)))
    fig.add_hline(y=150, line=dict(color=style.COLORS["grey"], dash="dot"), annotation_text="Ergun: 150", annotation_position="bottom right")
    fig.update_layout(height=400, margin=dict(l=80, r=20, t=30, b=100), legend=dict(orientation="h", x=0, y=-0.25, yanchor="top"))
    fig.update_xaxes(title_text="Sauter diameter d₃₂ (µm)")
    fig.update_yaxes(type="log", title_text="C_eff (-)", range=[1.9, 3.6])
    return fig


def sensitivity_figure():
    s = sensitivity()
    fig = go.Figure()
    for label in dict.fromkeys(r["input"] for r in s["rows"]):
        sub = [r for r in s["rows"] if r["input"] == label]
        fig.add_trace(go.Bar(y=[f"{label.split()[-1].replace('(1/m)', 'R_m')} = {r['value']:g}" for r in sub], x=[r["force"] for r in sub], orientation="h", name=label))
    fig.add_vline(x=s["base"], line=dict(color=style.COLORS["grey"], dash="dot"))
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=20, b=100), barmode="group",
                      legend=dict(orientation="h", x=0, y=-0.15, yanchor="top"))
    fig.update_xaxes(title_text="plunge force F at 800 µm (N), fluid resistance only")
    fig.update_yaxes(autorange="reversed", automargin=True)
    return fig
