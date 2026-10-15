"""AI Barista Plant: a French press drawn and operated like a chemical plant.
Thin Streamlit UI. All physics lives in plant/physics.py and the AI in plant/ai.py."""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from plant import physics as ph
from plant import ai
from plant.diagram import plant_svg
from plant import steps as presenter_steps
from plant import calibration as cal
from plant import standards
from plant import packed_bed as pb
from plotly.subplots import make_subplots
from plant.style import CHART_CONFIG, COLORS, CSS, card, header, label

st.set_page_config(page_title="AI Barista Plant", page_icon="☕", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
C2K = 273.15


# ---------------------------------------------------------------- cached calculations
@st.cache_data(max_entries=256, ttl=3600)
def simulate(grind_um, T_water_C, steep_s, ratio, m_coffee_g, preheated):
    sim = ph.brew(grind_um * 1e-6, T_water_C + C2K, steep_s, m_coffee=m_coffee_g / 1000,
                  m_water=m_coffee_g / 1000 * ratio, preheated=preheated)
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in sim.items()}


@st.cache_data(max_entries=4, ttl=86400)
def calibration_result(grind):
    r = cal.calibrate(grind)
    t, y = cal.measured(grind)
    tt = np.linspace(0, 1.1 * t.max(), 150)
    lo, hi = cal.band(r, tt)
    s = cal.summary(r)
    return {"t": t.tolist(), "y": y.tolist(), "tt": tt.tolist(), "fit": cal.curve(r["p"], tt).tolist(),
            "lo": lo.tolist(), "hi": hi.tolist(), "res": r["residuals"].tolist(), "rms": float(r["rms"]),
            "summary": {k: [float(x) for x in v] for k, v in s.items()}}


@st.cache_data(max_entries=64, ttl=3600)
def grind_sweep(T_water_C, steep_s, ratio, m_coffee_g, preheated, plunge_s, fines):
    return pb.grind_sweep(list(range(300, 1201, 50)), T_water_C + C2K, steep_s, m_coffee_g / 1000,
                          m_coffee_g / 1000 * ratio, preheated, plunge_s, fines)


@st.cache_data(max_entries=1, ttl=86400)
def standards_checks():
    return [(name, bool(ok), detail) for name, ok, detail in standards.run_checks()]


def load_benchmark():
    path = Path(__file__).parent / "plant" / "benchmark.json"
    return json.loads(path.read_text()) if path.exists() else None


# ---------------------------------------------------------------- session state
for key, default in {"lab": [], "human": [], "ai": [], "last": None, "seed": 0}.items():
    st.session_state.setdefault(key, default)

# ---------------------------------------------------------------- sidebar: setpoints
with st.sidebar:
    st.markdown(label("Area 100 · setpoints") + "<h3 style='margin-top:0'>Control panel</h3>", unsafe_allow_html=True)
    with st.form("setpoints"):
        st.caption("Batch setpoints (R-101)")
        grind = st.slider("Grind size d (µm)", 300, 1200, 800, 10)
        T_water = st.slider("Kettle temperature T_w (°C)", 85.0, 99.0, 93.0, 0.5)
        steep = st.slider("Steep time t (s)", 60, 600, 240, 10)
        ratio = st.slider("Water-to-coffee ratio R (g/g)", 12.0, 20.0, 16.7, 0.1)
        m_coffee = st.slider("Coffee dose m_c (g)", 10.0, 30.0, 15.0, 0.5)
        preheated = st.checkbox("Preheat press with hot water", value=False)
        st.caption("Fluid unit settings")
        plunge_s = st.slider("Plunge time t_p (s)", 3, 60, 20, 1)
        fines = st.slider("Fines mass fraction w_f (-)", 0.0, 0.40, 0.15, 0.01)
        run = st.form_submit_button("▶ RUN BATCH", type="primary", width="stretch")

setpoints = {"grind_um": float(grind), "T_water_C": float(T_water), "steep_s": float(steep), "ratio": float(ratio)}

if run:
    rng = np.random.default_rng(st.session_state.seed)
    st.session_state.seed += 1
    meas = ai.run_batch(setpoints, rng, m_coffee=m_coffee / 1000, check_bounds=False, preheated=preheated)
    bar = st.progress(0.0, text="Batch running: pouring, steeping, plunging…")
    for i in range(20):                       # short visual run so the operator sees the batch progress
        time.sleep(0.05)
        bar.progress((i + 1) / 20, text=f"Batch running: t = {steep * (i + 1) / 20:.0f} s of {steep} s")
    bar.empty()
    row = {**setpoints, "m_coffee_g": m_coffee, "preheated": preheated,
           "TDS_measured_pct": 100 * meas["TDS"], "EY_measured_pct": 100 * meas["EY"],
           "TDS_model_pct": 100 * meas["sim"]["TDS"], "in_box": ph.in_target(meas["TDS"], meas["EY"])}
    st.session_state.lab.append(row)
    st.session_state.human.append(row)
    st.session_state.last = row

# ---------------------------------------------------------------- live calculations for the current setpoints
T_K = T_water + C2K
sim = simulate(float(grind), float(T_water), float(steep), float(ratio), float(m_coffee), preheated)
T_brew_end = sim["T"][-1]
plg = ph.plunge(grind * 1e-6, T_brew_end, m_coffee=m_coffee / 1000, plunge_time=plunge_s, fines_fraction=fines)
settle = ph.settling(ph.CELL_SIZE, T_brew_end)
PLUG_LIMIT_N = 30.0
alarms = []
if plg["force"] > PLUG_LIMIT_N:
    alarms.append(("F-101 FILTER PLUGGED", f"Plunge force {plg['force']:.0f} N > {PLUG_LIMIT_N:.0f} N. Grind is too fine or has too many fines."))
if not ph.in_target(sim["TDS"], sim["EY"]):
    alarms.append(("R-101 OFF-SPEC", "Predicted cup is outside the SCA ideal box (strength 1.15–1.35 %, extraction 18–22 %)."))

values = {
    "T_kettle": f"{T_water:.1f} °C", "grind": f"{grind} µm",
    "T_brew": f"{T_brew_end - C2K:.1f} °C", "TDS": f"{100 * sim['TDS']:.2f} %", "EY": f"{100 * sim['EY']:.1f} %",
    "plunge_F": f"{plg['force']:.1f} N", "plug_alarm": plg["force"] > PLUG_LIMIT_N,
    "settle_t": f"{settle['t_settle']:.0f} s", "in_box": ph.in_target(sim["TDS"], sim["EY"]),
}

# ---------------------------------------------------------------- layout
st.markdown(header("Fluid mechanics · Flow through a packed bed", "AI Barista Plant",
                   "A French press is a packed bed. Dimensional analysis and the Ergun equation show how grind size "
                   "sets the flow, a material balance links it to the cup, and an AI operator picks the recipe."),
            unsafe_allow_html=True)

VIEWS = ["Plant", "Trends", "Packed bed", "Lab notebook", "AI operator", "Presenter", "Engineering notes"]
view = st.segmented_control("View", VIEWS, default="Plant", key="view", label_visibility="collapsed") or "Plant"

# ---- Plant
if view == "Plant":
    st.markdown(label("Live process · model predictions"), unsafe_allow_html=True)
    st.image(plant_svg(values, running=bool(run)), width="stretch")
    cols = st.columns(4)
    cols[0].metric("Strength (TDS)", f"{100 * sim['TDS']:.2f} %", help="Dissolved coffee mass / beverage mass")
    cols[1].metric("Extraction yield (EY)", f"{100 * sim['EY']:.1f} %", help="Dissolved coffee mass / dry coffee mass")
    cols[2].metric("Brew temperature after mixing", f"{sim['T0'] - C2K:.1f} °C")
    cols[3].metric("Mass balance closure error", f"{sim['balance_error']:.1e}")
    st.markdown("#### Alarm summary")
    if alarms:
        for name, msg in alarms:
            st.error(f"**{name}** · {msg}")
    else:
        st.success("All units normal. The predicted cup is inside the SCA ideal box.")
    st.caption("Values on the diagram are model predictions for the current setpoints. Batches you run in the "
               "control panel add measurement noise and go to the lab notebook.")

# ---- Trends
if view == "Trends":
    t = np.array(sim["t"])
    c1, c2 = st.columns(2)
    fig = go.Figure(go.Scatter(x=t, y=np.array(sim["T"]) - C2K, name="T (TI-102)", line=dict(color=COLORS["alarm"])))
    fig.update_layout(xaxis_title="t (s)", yaxis_title="T (°C)", showlegend=True)
    c1.markdown("##### Energy balance: brew temperature")
    c1.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    M_E = ph.X_EXTRACTABLE * m_coffee / 1000
    fig = go.Figure()
    fig.add_scatter(x=t, y=np.array(sim["m_l"]) / M_E, name="dissolved (m_l)", line=dict(color=COLORS["coffee"]))
    fig.add_scatter(x=t, y=np.array(sim["F"]) / M_E, name="surface (F)", line=dict(color=COLORS["warn"], dash="dot"))
    fig.add_scatter(x=t, y=np.array(sim["S"]) / M_E, name="inside grains (S)", line=dict(color=COLORS["grey"], dash="dash"))
    fig.update_layout(xaxis_title="t (s)", yaxis_title="fraction of extractables (-)", showlegend=True)
    c2.markdown("##### Material balance: where the solubles are")
    c2.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    st.caption(f"Time scales at the start of the batch: surface dissolution τ_s = {sim['tau_s']:.1f} s, "
               f"diffusion out of the grains τ_d = {sim['tau_d']:.0f} s. Both grow with grind size, "
               "and τ_d grows as d².")

# ---- Packed bed (Ergun)
if view == "Packed bed":
    st.markdown(label("Start here · F-101"), unsafe_allow_html=True)
    st.markdown("#### The grounds cake is a packed bed")
    m = st.columns(5)
    m[0].metric("d₃₂ (Sauter)", f"{1e6 * plg['d32']:.0f} µm", help="Surface-weighted mean size, including fines.")
    m[1].metric("d_s (effective)", f"{1e6 * plg['d_s']:.0f} µm", help="Sphericity 0.75 × d₃₂ (Corrochano 2015).")
    m[2].metric("Re_b", f"{plg['Re_b']:.2f}")
    m[3].metric("Inertial share", f"{100 * plg['inertial_share']:.1f} %", help="Burke–Plummer term / total Ergun loss.")
    m[4].metric("Plunge force", f"{plg['force']:.1f} N", help=f"Cake {plg['dP_cake']:.0f} Pa + mesh {plg['dP_mesh']:.0f} Pa, times the press area.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Ergun chart: friction factor vs bed Reynolds number")
        Re = np.logspace(-2, 4, 200)
        fig = go.Figure()
        fig.add_scatter(x=Re, y=pb.ergun_curve(Re), name="Ergun: 150/Re_b + 1.75", line=dict(color=COLORS["coffee"], width=3))
        fig.add_scatter(x=Re, y=150 / Re, name="viscous limit (Kozeny–Carman)", line=dict(color=COLORS["water"], dash="dash"))
        fig.add_scatter(x=Re, y=np.full_like(Re, 1.75), name="inertial limit (Burke–Plummer)", line=dict(color=COLORS["warn"], dash="dash"))
        for b, sym in zip(pb.brewer_points(plg, T_brew_end), ["diamond", "square", "circle"]):
            live = b["name"].endswith("(live)")
            fig.add_scatter(x=[b["Re_b"]], y=[b["f_p"]], mode="markers", name=b["name"],
                            marker=dict(symbol=sym, size=16 if live else 12, color=COLORS["ok"] if live else COLORS["grey"],
                                        line=dict(color="#0d1117", width=1)))
        fig.add_vrect(x0=pb.C15_RE_RANGE[0], x1=pb.C15_RE_RANGE[1], fillcolor=COLORS["coffee"], opacity=0.12, line_width=0)
        fig.add_scatter(x=[None], y=[None], mode="markers", name="Re_b measured in real coffee beds (Corrochano 2015)",
                        marker=dict(symbol="square", size=12, color=COLORS["coffee"], opacity=0.35))
        fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_range=[-2, 4], yaxis_range=[0, 4],
                          xaxis_title="bed Reynolds number Re_b (-)", yaxis_title="bed friction factor f_p (-)",
                          legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                          margin=dict(l=60, r=20, t=20, b=150), height=470)
        st.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
        st.caption("Every brewer sits far left, where the viscous term dominates, so pressure drop ∝ μu/d². "
                   "Even espresso at 9 bar has Re_b ≈ 0.16: 9 bar, still laminar. "
                   "Espresso and pour-over use typical recipes (assumed values, listed in plant/packed_bed.py); "
                   "the dots are Ergun evaluated, not measured.")
    with c2:
        st.markdown("##### Check against measured coffee beds (Corrochano 2015)")
        rows = pd.DataFrame(pb.corrochano_check())
        fig = go.Figure()
        for rho_b, sym in zip([360, 400, 480], ["circle", "square", "triangle-down"]):
            r = rows[rows.rho_bulk == rho_b]
            fig.add_scatter(x=r.d32_um, y=r.C_eff, mode="markers", name=f"measured, packed to {rho_b} kg/m³",
                            marker=dict(symbol=sym, size=11, color=COLORS["coffee"]),
                            error_y=dict(type="data", array=r.C_eff_sd, color=COLORS["grey"]))
        fig.add_scatter(x=[70, 140], y=[150, 150], mode="lines", name="Ergun's constant, 150", line=dict(color=COLORS["water"], dash="dash"))
        fig.add_scatter(x=[70, 140], y=[180, 180], mode="lines", name="Carman's constant, 180", line=dict(color=COLORS["grey"], dash="dot"))
        fig.update_layout(yaxis_type="log", yaxis_range=[2, np.log10(5000)], xaxis_range=[70, 140],
                          xaxis_title="Sauter diameter d₃₂ (µm)", yaxis_title="constant that fits the data, C_eff (-)",
                          legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                          margin=dict(l=60, r=20, t=20, b=150), height=470)
        st.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
        st.caption(f"Each measured permeability, turned round into the viscous constant it implies: C_eff = d_s²ε³/(k(1−ε)²). "
                   f"Ergun says 150. Espresso beds need {rows.C_eff.min():.0f}–{rows.C_eff.max():.0f}, so Ergun over-predicts "
                   f"permeability {rows.ratio.min():.1f}–{rows.ratio.max():.0f}× and the gap grows with grind size. These beds are "
                   "compressed far below random packing (ε 0.12–0.33). Error bars cover the permeability scatter only; "
                   "porosity was read off the paper's Fig. 13.")

    st.markdown("##### Why dimensional analysis pays off: three beds, one curve")
    beds = pb.collapse_data(T_brew_end, np.logspace(-4, 0, 25))
    c1, c2 = st.columns(2)
    figs = [go.Figure(), go.Figure()]
    for b, col, sym, size in zip(beds, [COLORS["water"], COLORS["coffee"], COLORS["warn"]],
                                 ["circle-open", "diamond-open", "circle"], [13, 9, 5]):
        figs[0].add_scatter(x=b["u"], y=b["dPdL"], name=b["label"], line=dict(color=col, width=3))
        figs[1].add_scatter(x=b["Re_b"], y=b["f_p"], name=b["label"], mode="markers",
                            marker=dict(symbol=sym, size=size, color=col, line=dict(width=2, color=col)))
    figs[0].update_layout(xaxis_type="log", yaxis_type="log", xaxis_range=[-4, 0], yaxis_range=[1, 10],
                          xaxis_title="superficial velocity u (m/s)", yaxis_title="pressure gradient ΔP/L (Pa/m)")
    figs[1].update_layout(xaxis_type="log", yaxis_type="log", xaxis_range=[-2, 3.5], yaxis_range=[0, 4],
                          xaxis_title="bed Reynolds number Re_b (-)", yaxis_title="bed friction factor f_p (-)")
    for f in figs:
        f.update_layout(legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                        margin=dict(l=60, r=20, t=20, b=130), height=400)
    c1.plotly_chart(card(figs[0]), width="stretch", theme=None, config=CHART_CONFIG)
    c2.plotly_chart(card(figs[1]), width="stretch", theme=None, config=CHART_CONFIG)
    st.caption("Left: in dimensional form, three beds that differ in grain size and porosity give three separate curves. "
               "Right: the same points as f_p vs Re_b fall on one curve. Here the collapse is built in (the points are Ergun "
               "evaluated); Ergun's 1952 discovery was that measured beds collapse like this.")

    st.markdown("##### Grind-size explorer: what grind size does to the plunge and to the cup")
    sw = grind_sweep(float(T_water), float(steep), float(ratio), float(m_coffee), preheated, float(plunge_s), float(fines))
    c1, c2 = st.columns(2)
    fig = go.Figure()
    fig.add_scatter(x=sw["grind_um"], y=sw["force"], name=f"with {100 * fines:.0f} % fines", line=dict(color=COLORS["coffee"], width=3))
    fig.add_scatter(x=sw["grind_um"], y=sw["force_no_fines"], name="no fines", line=dict(color=COLORS["water"], dash="dash"))
    fig.add_vline(x=grind, line=dict(color=COLORS["grey"], dash="dot"))
    fig.update_layout(xaxis_title="grind size d (µm)", yaxis_title="plunge force F_p (N)", yaxis_rangemode="tozero",
                      legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                      margin=dict(l=60, r=20, t=20, b=120), height=380)
    c1.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    fig = go.Figure()
    fig.add_hrect(y0=100 * ph.EY_RANGE[0], y1=100 * ph.EY_RANGE[1], fillcolor=COLORS["ok"], opacity=0.12, line_width=0)
    fig.add_scatter(x=sw["grind_um"], y=[100 * e for e in sw["EY"]], name="extraction yield EY", line=dict(color=COLORS["coffee"], width=3))
    fig.add_vline(x=grind, line=dict(color=COLORS["grey"], dash="dot"))
    fig.update_layout(xaxis_title="grind size d (µm)", yaxis_title="extraction yield EY (%)",
                      yaxis_range=[5, 32],
                      legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                      margin=dict(l=60, r=20, t=20, b=120), height=380)
    c2.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    i_lo, i_hi = 0, len(sw["grind_um"]) - 1
    st.caption(f"Going from {sw['grind_um'][i_hi]:.0f} to {sw['grind_um'][i_lo]:.0f} µm changes extraction from "
               f"{100 * sw['EY'][i_hi]:.0f} % to {100 * sw['EY'][i_lo]:.0f} % but the plunge force only from "
               f"{sw['force'][i_hi]:.1f} to {sw['force'][i_lo]:.1f} N, because the fines set d₃₂ and so the flow. "
               "About 1 N of every force is the mesh, which doesn't depend on grind. "
               "The green band is the SCA extraction target (18–22 %). Same recipe as the control panel.")

    st.markdown("##### Real grinds: what the fines look like, and where finer stops helping")
    c1, c2 = st.columns(2)
    fig = go.Figure()
    summ = {g: pb.psd_summary(g) for g in ["2.5", "2.0", "1.5", "1.0"]}
    for g, col in zip(summ, [COLORS["water"], COLORS["ok"], COLORS["warn"], COLORS["coffee"]]):
        c = pb.C20["psd"][g]
        fig.add_scatter(x=c["d_um"], y=c["vol_pct"], mode="lines", line=dict(color=col, width=2),
                        name=f"setting {g}: d₃₂ {1e6 * summ[g]['d32']:.0f} µm, {100 * summ[g]['fines_volume']:.0f} % fines")
    fig.add_vline(x=100, line=dict(color=COLORS["grey"], dash="dot"))
    fig.update_layout(xaxis_type="log", xaxis_range=[0, np.log10(2000)], yaxis_range=[0, 22],
                      xaxis_title="particle diameter (µm)", yaxis_title="volume percent (%)",
                      legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                      margin=dict(l=60, r=20, t=20, b=150), height=430)
    c1.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    c1.caption(f"Measured espresso grinds (Cameron et al. 2020, Fig. 2B; finer setting = smaller number). Two families: "
               f"fines below 100 µm and boulders. Grinding finer adds fines of the same size. Fines are "
               f"{100 * min(v['fines_volume'] for v in summ.values()):.0f}–{100 * max(v['fines_volume'] for v in summ.values()):.0f} % "
               f"of the volume but {100 * min(v['fines_surface'] for v in summ.values()):.0f}–{100 * max(v['fines_surface'] for v in summ.values()):.0f} % "
               f"of the surface, so d₃₂ = {1e6 * min(v['d32'] for v in summ.values()):.0f}–{1e6 * max(v['d32'] for v in summ.values()):.0f} µm, "
               "close to Corrochano's 80–131 µm from a different lab. Uman et al. (2016) found the fines' surface peak at 27 µm, "
               f"close to the 30 µm fines in this model, whose assumed {100 * fines:.0f} % fines carry "
               f"{100 * pb.model_fines_surface_share(grind * 1e-6, fines):.0f} % of the surface.")
    c20 = pb.C20
    fig = go.Figure()
    fig.add_vrect(x0=1.0, x1=1.7, fillcolor=COLORS["alarm"], opacity=0.10, line_width=0)
    fig.add_scatter(x=c20["grind_setting"], y=c20["EY_pct"], mode="lines+markers", name="measured EY (±1 sd)",
                    line=dict(color=COLORS["coffee"], dash="dash"), marker=dict(size=11),
                    error_y=dict(type="data", array=c20["EY_sd_pct"], color=COLORS["grey"]))
    fig.add_scatter(x=[None], y=[None], mode="markers", name="finer than 1.7: partly clogged, uneven flow",
                    marker=dict(symbol="square", size=12, color=COLORS["alarm"], opacity=0.3))
    fig.update_layout(xaxis_range=[1.0, 2.4], yaxis_range=[20, 23.6], xaxis_title="grinder setting (smaller = finer)",
                      yaxis_title="extraction yield EY (%)",
                      legend=dict(orientation="h", x=0, y=-0.25, xanchor="left", yanchor="top"),
                      margin=dict(l=60, r=20, t=20, b=150), height=430)
    c2.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    c2.caption("Measured espresso extraction (Cameron et al. 2020, Fig. 4B, 6 bar). A uniform-bed model, like the grind "
               "explorer above, says finer always extracts more. The data agree down to setting 1.7, then extraction falls: "
               "with too many fines the bed clogs unevenly and water channels through cracks. That's the limit of the "
               "uniform packed-bed assumption, and where Ergun stops describing the real bed.")

    with st.expander("T-101 · fines settling in the cup (Stokes' law)"):
        st.markdown(f"30 µm fines: v_t = **{1000 * settle['v']:.2f} mm/s**, Re_p = **{settle['Re_p']:.3f}**, "
                    f"settle 8 cm in **{settle['t_settle']:.0f} s**")
        d_f = np.linspace(10e-6, 300e-6, 100)
        res = [ph.settling(x, T_brew_end) for x in d_f]
        fig = go.Figure()
        ok = [r["valid"] for r in res]
        fig.add_scatter(x=d_f[ok] * 1e6, y=[r["t_settle"] for r, o in zip(res, ok) if o], name="Stokes valid (Re_p<0.1)",
                        line=dict(color=COLORS["ok"]))
        fig.add_scatter(x=d_f[~np.array(ok)] * 1e6, y=[r["t_settle"] for r, o in zip(res, ok) if not o],
                        name="Stokes invalid", line=dict(color=COLORS["alarm"], dash="dot"))
        fig.update_layout(xaxis_title="particle diameter (µm)", yaxis_title="time to settle 8 cm (s)", yaxis_type="log",
                          yaxis_range=[np.log10(0.5), np.log10(3e4)], showlegend=True)
        st.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)

# ---- Lab notebook
if view == "Lab notebook":
    st.markdown("#### Lab notebook: every batch you ran")
    if st.session_state.lab:
        df = pd.DataFrame(st.session_state.lab)
        st.dataframe(df.round(3), width="stretch")
        st.download_button("Download CSV", df.to_csv(index=False), "lab_notebook.csv", "text/csv")
        st.caption(f"Measured TDS includes meter noise (standard deviation {100 * ai.TDS_METER_SD:.2f} % TDS). "
                   "Measured EY is computed from measured TDS, as in a real lab.")
    else:
        st.info("No batches yet. Set the setpoints in the control panel and press RUN BATCH.")

# ---- AI operator
if view == "AI operator":
    st.markdown("#### Human vs AI: who reaches the ideal cup first?")
    st.caption("Both players control the same four setpoints: grind, temperature, steep time and ratio "
               "(15 g dose, press not preheated). Your batches come from the control panel. "
               "The AI uses Gaussian process models of strength and extraction, and picks the recipe with the highest chance of landing in the SCA box.")
    c1, c2 = st.columns(2)
    if c2.button("🤖 AI: brew next batch", type="primary", width="stretch"):
        rng = np.random.default_rng(1000 + len(st.session_state.ai))
        hist = [({k: r[k] for k in ai.NAMES}, r["TDS_measured_pct"] / 100, r["EY_measured_pct"] / 100) for r in st.session_state.ai]
        with st.spinner("AI fitting its models and choosing the next recipe…"):
            x, info = ai.suggest(hist, rng)
            meas = ai.run_batch(x, rng)
        st.session_state.ai.append({**x, "TDS_measured_pct": 100 * meas["TDS"], "EY_measured_pct": 100 * meas["EY"],
                                    "in_box": ph.in_target(meas["TDS"], meas["EY"]), "why": info["reason"]})
    if c1.button("Reset game", width="stretch"):
        st.session_state.human, st.session_state.ai = [], []

    def first_hit(rows):
        return next((i + 1 for i, r in enumerate(rows) if r["in_box"]), None)

    hh, ah = first_hit(st.session_state.human), first_hit(st.session_state.ai)
    s1, s2 = st.columns(2)
    s1.metric("You: batches run", len(st.session_state.human))
    s1.caption(f"✅ ideal cup at batch {hh}" if hh else "no ideal cup yet")
    s2.metric("AI: batches run", len(st.session_state.ai))
    s2.caption(f"✅ ideal cup at batch {ah}" if ah else "no ideal cup yet")

    fig = go.Figure()
    fig.add_shape(type="rect", x0=18, x1=22, y0=1.15, y1=1.35, line=dict(color=COLORS["ok"]), fillcolor="rgba(31,157,85,0.10)")
    for who, rows, color in [("you", st.session_state.human, COLORS["human"]), ("AI", st.session_state.ai, COLORS["ai"])]:
        if rows:
            fig.add_scatter(x=[r["EY_measured_pct"] for r in rows], y=[r["TDS_measured_pct"] for r in rows],
                            mode="markers+lines+text", text=[str(i + 1) for i in range(len(rows))], textposition="top center",
                            name=who, marker=dict(size=10, color=color), line=dict(color=color, width=1, dash="dot"))
    st.markdown("##### Brewing control chart")
    fig.update_layout(xaxis_title="extraction yield EY (%)", yaxis_title="strength TDS (%)",
                      xaxis_range=[8, 30], yaxis_range=[0.5, 2.2], showlegend=True)
    st.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
    if st.session_state.ai:
        st.markdown("**Why the AI chose each batch**")
        st.dataframe(pd.DataFrame(st.session_state.ai).round(2), width="stretch")

    bench = load_benchmark()
    if bench:
        st.markdown("#### Benchmark over many virtual operators")
        st.caption(f"{bench['seeds']} independent runs, at most {bench['budget']} batches each, with the same noisy TDS meter. "
                   "These are best-found results for the strategies tried, not a proof that the AI is optimal.")
        rows = []
        for name, label in [("ai", "AI (Gaussian process)"), ("ofat", "One factor at a time"), ("random", "Random recipes")]:
            hits = [h for h in bench["results"][name] if h]
            rows.append({"strategy": label, "reached ideal cup": f"{len(hits)} / {bench['seeds']}",
                         "median batches (when reached)": float(np.median(hits)) if hits else None})
        st.table(pd.DataFrame(rows))

# ---- Presenter: Write / Say teleprompter with a Grill-me quiz
if view == "Presenter":
    names = list(presenter_steps.UNITS)
    top = st.columns([3, 1, 1])
    unit_name = top[0].selectbox("Unit", names, key="p_unit")
    grill = top[1].toggle("Grill me", key="p_grill")
    if top[2].button("⏱ Start timer", key="p_timer"):
        st.session_state.p_t0 = time.time()
    unit = presenter_steps.UNITS[unit_name]
    if st.session_state.get("p_last_unit") != unit_name:
        st.session_state.p_i, st.session_state.p_last_unit = 0, unit_name
    n = len(unit["steps"])
    if grill:
        st.markdown(f"#### Grill me: {unit['title']}")
        st.caption("Answer out loud first, then open the question to check yourself.")
        for k, (q, a) in enumerate(unit["questions"], 1):
            with st.expander(f"Q{k}. {q}"):
                st.write(a)
    else:
        def move(delta):   # callback runs before the rerun, so the buttons' disabled state is current
            st.session_state.p_i = min(max(st.session_state.p_i + delta, 0), n - 1)
        i = st.session_state.p_i
        nav = st.columns([1, 1, 4])
        nav[0].button("◀ Back", key="p_prev", disabled=i == 0, on_click=move, args=(-1,))
        nav[1].button("Next ▶", key="p_next", disabled=i == n - 1, on_click=move, args=(1,))
        t0 = st.session_state.get("p_t0")
        clock = f" · ⏱ {int((time.time() - t0) // 60)}:{int((time.time() - t0) % 60):02d}" if t0 else ""
        nav[2].markdown(f"**Step {i + 1} of {n}**{clock}  \nSign convention: {unit['sign']}")
        step = unit["steps"][i]
        left, right = st.columns([1, 1])
        with left:
            st.markdown(f"##### {i + 1}. {step['title']}")
            st.markdown("**Write:**")
            st.latex(step["write"])
        with right:
            st.markdown("**Say:**")
            st.info(step["say"])
        st.image(plant_svg(values, highlight=unit["tag"]), width="stretch")
        with st.expander("Degrees of freedom"):
            d = unit["dof"]
            st.markdown("**Unknowns:** " + "; ".join(d["unknowns"]) + "  \n**Equations:** " + "; ".join(d["equations"])
                        + "  \n**Specified:** " + ", ".join(d["specified"]) + f"  \n**Result:** {d['result']}")
        with st.expander("Physical checks"):
            for c in unit["checks"]:
                st.markdown(f"- {c}")

# ---- Engineering notes
if view == "Engineering notes":
    checks = standards_checks()
    passed = sum(ok for _, ok, _ in checks)
    badge = st.success if passed == len(checks) else st.error
    badge(f"**PROFESSOR-STANDARD CHECKS: {passed}/{len(checks)} LIVE CHECKS PASSED**  \n"
          + "  \n".join(f"{'✅' if ok else '❌'} {name} ({detail})" for name, ok, detail in checks)
          + "  \n✅ Every equation passes a strict KaTeX parse (run in the test suite, which needs node)")

    st.markdown("#### Model check against measured data (Moroney et al. 2016, Figure 5)")
    st.caption("Measured: 60 g of coffee in 0.5 L of hot water, well mixed, concentration sampled over time. Points read "
               "from the paper's vector figure and overlay-checked. The paper's concentration axis is dimensionless, so the "
               "fit uses the curve's shape plus a free amplitude A. Band: 95 % range from the fitted parameter uncertainty.")
    rows = []
    cols = st.columns(2)
    for col, grind, title in [(cols[0], "fine", "Fine grind (JK drip filter)"), (cols[1], "coarse", "Coarse grind (Cimbali #20)")]:
        r = calibration_result(grind)
        col.markdown(f"##### {title}")
        fig = make_subplots(rows=2, cols=1, row_heights=[0.72, 0.28], vertical_spacing=0.08, shared_xaxes=True)
        fig.add_scatter(x=r["tt"] + r["tt"][::-1], y=r["hi"] + r["lo"][::-1], fill="toself", line=dict(width=0),
                        fillcolor="rgba(31,157,85,0.25)", name="95 % band", row=1, col=1)
        fig.add_scatter(x=r["tt"], y=r["fit"], name="model fit", line=dict(color=COLORS["ok"]), row=1, col=1)
        fig.add_scatter(x=r["t"], y=r["y"], mode="markers", name="measured", marker=dict(color=COLORS["coffee"], size=9),
                        row=1, col=1)
        fig.add_bar(x=r["t"], y=r["res"], name="residual", marker_color=COLORS["warn"], row=2, col=1)
        fig.update_xaxes(title_text="time t (s)", row=2, col=1)
        fig.update_yaxes(title_text="c_h (paper's scale)", row=1, col=1)
        fig.update_yaxes(title_text="residual", row=2, col=1)
        fig.update_layout(height=470, showlegend=True, margin=dict(l=60, r=20, t=50, b=50),
                          legend=dict(orientation="h", x=0, y=1.02, xanchor="left", yanchor="bottom"))
        col.plotly_chart(card(fig), width="stretch", theme=None, config=CHART_CONFIG)
        s = r["summary"]
        lit = cal.DATA[grind]
        rows.append({"grind": grind, "τ_s fit (s)": f"{s['tau_s'][0]:.2g} ({s['tau_s'][1]:.2g}–{s['tau_s'][2]:.2g})",
                     "τ_s Moroney (s)": f"{lit['t_s']:.3g}",
                     "τ_d fit (s)": f"{s['tau_d'][0]:.0f} ({s['tau_d'][1]:.0f}–{s['tau_d'][2]:.0f})",
                     "τ_d Moroney (s)": f"{lit['t_d']:.3g}",
                     "fast fraction φ": f"{s['phi'][0]:.2f} ± {s['phi'][0] - s['phi'][1]:.2f}",
                     "rms residual": f"{r['rms']:.3f}"})
    st.table(pd.DataFrame(rows).set_index("grind"))
    st.markdown("""
- **Fine grind:** the fitted diffusion time τ_d (best found, with its 1-sigma range) contains Moroney's 42.2 s, which is the value
  this app is anchored to. The fitted fast fraction φ matches the broken-cell geometry, 0.46 at 322 µm. The surface time τ_s
  can't be pinned down, because the first sample is at 35 s, long after a 1 s process has finished. The wide range says so honestly.
- **Coarse grind:** τ_s agrees with Moroney's value to about 15 %, but the data favour a slower diffusion time than the paper's fit.
  The paper's own curve sits above the later points in its Figure 5d. Coarse-grind predictions in this app are therefore
  less certain than fine-grind ones.
""")
    st.markdown("""
#### Symbols used on this page (SI units in the model)
| Symbol | Meaning | Unit |
|---|---|---|
| d | grind (particle) diameter | m (shown in µm) |
| d₃₂ | Sauter mean diameter including fines | m |
| w_f | mass fraction of fines | – |
| T_w, T | kettle temperature, brew temperature | K (shown in °C) |
| t, t_p | steep time, plunge time | s |
| R | water-to-coffee mass ratio | – |
| m_c | dry coffee mass | kg (shown in g) |
| TDS | strength: dissolved mass / beverage mass | – (shown in %) |
| EY | extraction yield: dissolved mass / dry coffee mass | – (shown in %) |
| τ_s, τ_d | surface dissolution and diffusion time scales | s |
| F, S, m_l | solubles on grain surfaces, inside grains, dissolved in liquid | kg |
| k | permeability of the grounds cake | m² |

#### Sources
- Moroney et al. (2016), *Coffee extraction kinetics in a well mixed system*, J. Math. Industry 7: extraction time scales, extractable fraction, solubility, cell size.
- Corrochano et al. (2015), *A new methodology to estimate the steady-state permeability of roast and ground coffee in packed beds*, J. Food Eng. 150: coffee solid density, particle porosity, bulk density, and Kozeny–Carman accuracy.
- SCAA Golden Cup brewing control chart: ideal strength 1.15–1.35 %, extraction 18–22 %.
- Water properties: CoolProp (IAPWS-95 formulation).

#### What is assumed (not measured)
The press heat-loss conductance UA = 1 W/K, grounds specific heat 1700 J/(kg K), mesh resistance, cake porosity,
fines fraction and TDS meter noise are assumed values, marked in the code. Real-brew validation would replace them with measurements.

The full derivations, with every step, are in `docs/derivations.html`.
""")
