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
from plant.style import COLORS

st.set_page_config(page_title="AI Barista Plant", page_icon="☕", layout="wide")
C2K = 273.15


# ---------------------------------------------------------------- cached calculations
@st.cache_data(max_entries=256, ttl=3600)
def simulate(grind_um, T_water_C, steep_s, ratio, m_coffee_g, preheated):
    sim = ph.brew(grind_um * 1e-6, T_water_C + C2K, steep_s, m_coffee=m_coffee_g / 1000,
                  m_water=m_coffee_g / 1000 * ratio, preheated=preheated)
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in sim.items()}


@st.cache_data(max_entries=64, ttl=3600)
def pump_curves(T_water_C, D_mm, L_m, K_total):
    T = T_water_C + C2K
    Q = np.linspace(2e-6, 1.95e-4, 120)
    sys_H = []
    for q in Q:
        try:
            sys_H.append(ph.transfer_line(q, T, D=D_mm / 1000, L=L_m, K_total=K_total)["H"])
        except ValueError:          # transition region: no reliable friction factor, leave a gap
            sys_H.append(None)
    return Q.tolist(), ph.pump_head(Q).tolist(), sys_H


def load_benchmark():
    path = Path(__file__).parent / "plant" / "benchmark.json"
    return json.loads(path.read_text()) if path.exists() else None


# ---------------------------------------------------------------- session state
for key, default in {"lab": [], "human": [], "ai": [], "last": None, "seed": 0}.items():
    st.session_state.setdefault(key, default)

# ---------------------------------------------------------------- sidebar: setpoints
with st.sidebar:
    st.markdown("### CONTROL PANEL · AREA 100")
    with st.form("setpoints"):
        st.caption("Batch setpoints (R-101)")
        grind = st.slider("Grind size d (µm)", 300, 1200, 800, 10)
        T_water = st.slider("Kettle temperature T_w (°C)", 85.0, 99.0, 93.0, 0.5)
        steep = st.slider("Steep time t (s)", 60, 600, 240, 10)
        ratio = st.slider("Water-to-coffee ratio R (g/g)", 12.0, 20.0, 16.7, 0.1)
        m_coffee = st.slider("Coffee dose m_c (g)", 10.0, 30.0, 15.0, 0.5)
        preheated = st.checkbox("Preheat press with hot water", value=False)
        st.caption("Fluid unit settings")
        stir_rpm = st.slider("Stirrer speed N (rpm)", 10, 600, 180, 10)
        plunge_s = st.slider("Plunge time t_p (s)", 3, 60, 20, 1)
        fines = st.slider("Fines mass fraction w_f (-)", 0.0, 0.40, 0.15, 0.01)
        run = st.form_submit_button("▶ RUN BATCH", type="primary", width="stretch")

setpoints = {"grind_um": float(grind), "T_water_C": float(T_water), "steep_s": float(steep), "ratio": float(ratio)}

if run:
    rng = np.random.default_rng(st.session_state.seed)
    st.session_state.seed += 1
    meas = ai.run_batch(setpoints, rng, m_coffee=m_coffee / 1000, check_bounds=False, preheated=preheated)
    bar = st.progress(0.0, text="Batch running: heating, pumping, steeping…")
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
Q_op = ph.operating_point(T_K)
line = ph.transfer_line(Q_op, T_K)
npsh_a, npsh_r = ph.npsh_available(T_K, Q_op), ph.npsh_required(Q_op)
stir = ph.stirring(stir_rpm / 60, sim["T0"])
plg = ph.plunge(grind * 1e-6, T_brew_end, m_coffee=m_coffee / 1000, plunge_time=plunge_s, fines_fraction=fines)
settle = ph.settling(ph.CELL_SIZE, T_brew_end)
h_carafe = (m_coffee / 1000 * ratio / 1000) / (np.pi * 0.085**2 / 4)
drain = ph.drain_time(h_carafe)
PLUG_LIMIT_N = 30.0
alarms = []
if npsh_a < npsh_r:
    alarms.append(("P-101 CAVITATION", f"NPSH available {npsh_a:.2f} m < required {npsh_r:.2f} m. Water is too close to boiling."))
if plg["force"] > PLUG_LIMIT_N:
    alarms.append(("F-101 FILTER PLUGGED", f"Plunge force {plg['force']:.0f} N > {PLUG_LIMIT_N:.0f} N. Grind is too fine or has too many fines."))
if not ph.in_target(sim["TDS"], sim["EY"]):
    alarms.append(("R-101 OFF-SPEC", "Predicted cup is outside the SCA ideal box (strength 1.15–1.35 %, extraction 18–22 %)."))

values = {
    "T_kettle": f"{T_water:.1f} °C", "Q_pump": f"{Q_op * 6e4:.1f} L/min", "H_pump": f"{line['H']:.2f} m",
    "npsh": f"{npsh_a - npsh_r:+.2f} m", "cav_alarm": npsh_a < npsh_r, "grind": f"{grind} µm",
    "T_brew": f"{T_brew_end - C2K:.1f} °C", "TDS": f"{100 * sim['TDS']:.2f} %", "EY": f"{100 * sim['EY']:.1f} %",
    "stir_Re": f"{stir['Re']:.1e}", "plunge_F": f"{plg['force']:.1f} N", "plug_alarm": plg["force"] > PLUG_LIMIT_N,
    "settle_t": f"{settle['t_settle']:.0f} s", "drain_t": f"{drain:.1f} s", "in_box": ph.in_target(sim["TDS"], sim["EY"]),
}

# ---------------------------------------------------------------- layout
st.markdown("## ☕ AI BARISTA PLANT")
st.caption("A French press, modelled and operated like a chemical plant: fluid mechanics, material and energy balances, and an AI operator.")

VIEWS = ["Plant", "Trends", "Fluid units", "Lab notebook", "AI operator", "Engineering notes"]
view = st.segmented_control("View", VIEWS, default="Plant", key="view", label_visibility="collapsed") or "Plant"

# ---- Plant
if view == "Plant":
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
    fig.update_layout(title="Energy balance: brew temperature", xaxis_title="t (s)", yaxis_title="T (°C)", showlegend=True)
    c1.plotly_chart(fig, width="stretch")
    M_E = ph.X_EXTRACTABLE * m_coffee / 1000
    fig = go.Figure()
    fig.add_scatter(x=t, y=np.array(sim["m_l"]) / M_E, name="dissolved (m_l)", line=dict(color=COLORS["coffee"]))
    fig.add_scatter(x=t, y=np.array(sim["F"]) / M_E, name="surface (F)", line=dict(color=COLORS["warn"], dash="dot"))
    fig.add_scatter(x=t, y=np.array(sim["S"]) / M_E, name="inside grains (S)", line=dict(color=COLORS["grey"], dash="dash"))
    fig.update_layout(title="Material balance: where the solubles are", xaxis_title="t (s)",
                      yaxis_title="fraction of extractables (-)", showlegend=True)
    c2.plotly_chart(fig, width="stretch")
    st.caption(f"Time scales at the start of the batch: surface dissolution τ_s = {sim['tau_s']:.1f} s, "
               f"diffusion out of the grains τ_d = {sim['tau_d']:.0f} s. Both grow with grind size, "
               "and τ_d grows as d².")

# ---- Fluid units
if view == "Fluid units":
    st.markdown("#### P-101 · pump and transfer line")
    c1, c2 = st.columns([2, 1])
    D_mm = c2.slider("Pipe inner diameter D (mm)", 5.0, 15.0, 8.0, 0.5)
    L_m = c2.slider("Pipe length L (m)", 0.5, 5.0, 1.5, 0.1)
    K_tot = c2.slider("Sum of fitting loss coefficients ΣK (-)", 0.0, 10.0, 2.6, 0.1)
    Qs, pumpH, sysH = pump_curves(T_water, D_mm, L_m, K_tot)
    fig = go.Figure()
    fig.add_scatter(x=np.array(Qs) * 6e4, y=pumpH, name="pump curve", line=dict(color=COLORS["water"]))
    fig.add_scatter(x=np.array(Qs) * 6e4, y=sysH, name="system curve", line=dict(color=COLORS["warn"]))
    try:
        q_op = ph.operating_point(T_K, D=D_mm / 1000, L=L_m, K_total=K_tot)
        lop = ph.transfer_line(q_op, T_K, D=D_mm / 1000, L=L_m, K_total=K_tot)
        fig.add_scatter(x=[q_op * 6e4], y=[lop["H"]], mode="markers", name="operating point",
                        marker=dict(size=12, color=COLORS["ok"]))
        c2.markdown(f"Q = **{q_op * 6e4:.2f} L/min**, V = **{lop['V']:.2f} m/s**  \nRe = **{lop['Re']:.3g}**, "
                    f"f = **{lop['f']:.4f}**  \nfriction head h_f = **{lop['h_f']:.2f} m**, fittings h_m = **{lop['h_m']:.2f} m**")
    except ValueError as e:
        c2.warning(f"No reliable operating point: {e}")
    fig.update_layout(xaxis_title="Q (L/min)", yaxis_title="head H (m)", yaxis_range=[0, 4.5], showlegend=True)
    c1.plotly_chart(fig, width="stretch")

    st.markdown("#### P-101 · cavitation check (NPSH)")
    Ts = np.arange(85.0, 99.6, 0.5)
    na = [ph.npsh_available(x + C2K, ph.operating_point(x + C2K)) for x in Ts]
    nr = [ph.npsh_required(ph.operating_point(x + C2K)) for x in Ts]
    fig = go.Figure()
    fig.add_scatter(x=Ts, y=na, name="NPSH available", line=dict(color=COLORS["water"]))
    fig.add_scatter(x=Ts, y=nr, name="NPSH required", line=dict(color=COLORS["alarm"], dash="dash"))
    fig.add_vline(x=T_water, line=dict(color=COLORS["grey"], dash="dot"))
    fig.update_layout(xaxis_title="kettle temperature T_w (°C)", yaxis_title="NPSH (m)", showlegend=True)
    st.plotly_chart(fig, width="stretch")
    st.caption("As water nears 100 °C its vapour pressure approaches atmospheric pressure, so the suction margin "
               "collapses. Where the curves cross, the pump would cavitate. The pump curve and NPSH-required curve are for a hypothetical small pump.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### A-101 · stirring")
        st.markdown(f"Impeller Reynolds number Re = ρND²/μ = **{stir['Re']:.3g}** ({stir['regime']})  \n"
                    f"Power number Np = **{stir['Np']:.2f}**, stirring power P = Np ρ N³ D⁵ = **{1000 * stir['P']:.2f} mW**")
        if stir["regime"] != "turbulent":
            st.warning("Not fully turbulent: the 'well-mixed' assumption in the extraction model is weaker here.")
    with c2:
        st.markdown("#### F-101 · plunge filtration")
        st.markdown(f"Sauter diameter with fines d₃₂ = **{1e6 * plg['d32']:.0f} µm**, permeability k = **{plg['k']:.2e} m²**  \n"
                    f"Pressure drop: cake **{plg['dP_cake']:.0f} Pa** + mesh **{plg['dP_mesh']:.0f} Pa**, force **{plg['force']:.1f} N**")
        st.caption("Kozeny–Carman is known to over-predict coffee-bed permeability (Corrochano et al. 2015), "
                   "and the mesh resistance and cake porosity are assumed. Calibrate by plunging a real press on a kitchen scale.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### T-101 · fines settling (Stokes' law)")
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
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.markdown("#### D-101 · carafe draining (Torricelli)")
        sp = np.linspace(4e-3, 20e-3, 60)
        fig = go.Figure(go.Scatter(x=sp * 1000, y=[ph.drain_time(h_carafe, d_spout=x) for x in sp], name="drain time",
                                   line=dict(color=COLORS["coffee"])))
        fig.update_layout(xaxis_title="spout diameter (mm)", yaxis_title="drain time (s)", showlegend=True)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Liquid height in the carafe h₀ = {100 * h_carafe:.1f} cm, discharge coefficient C_d = 0.6 (assumed).")

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
    fig.add_shape(type="rect", x0=18, x1=22, y0=1.15, y1=1.35, line=dict(color=COLORS["ok"]), fillcolor="rgba(126,231,135,0.12)")
    for who, rows, color in [("you", st.session_state.human, COLORS["human"]), ("AI", st.session_state.ai, COLORS["ai"])]:
        if rows:
            fig.add_scatter(x=[r["EY_measured_pct"] for r in rows], y=[r["TDS_measured_pct"] for r in rows],
                            mode="markers+lines+text", text=[str(i + 1) for i in range(len(rows))], textposition="top center",
                            name=who, marker=dict(size=10, color=color), line=dict(color=color, width=1, dash="dot"))
    fig.update_layout(title="Brewing control chart", xaxis_title="extraction yield EY (%)", yaxis_title="strength TDS (%)",
                      xaxis_range=[8, 30], yaxis_range=[0.5, 2.2], showlegend=True)
    st.plotly_chart(fig, width="stretch")
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

# ---- Engineering notes
if view == "Engineering notes":
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
| Q, V | volumetric flow rate, mean velocity | m³/s, m/s |
| H, h_f, h_m | head: system, friction loss, fitting loss | m |
| Re, f | Reynolds number, Darcy friction factor | – |
| ΣK | sum of fitting loss coefficients | – |
| NPSH | net positive suction head | m |
| N, D | stirrer speed, impeller diameter | 1/s, m |
| Np, P | power number, stirring power | –, W |
| k | permeability of the grounds cake | m² |
| C_d | discharge coefficient | – |

#### Sources
- Moroney et al. (2016), *Coffee extraction kinetics in a well mixed system*, J. Math. Industry 7: extraction time scales, extractable fraction, solubility, cell size.
- Corrochano et al. (2015), *A new methodology to estimate the steady-state permeability of roast and ground coffee in packed beds*, J. Food Eng. 150: coffee solid density, particle porosity, bulk density, and Kozeny–Carman accuracy.
- SCAA Golden Cup brewing control chart: ideal strength 1.15–1.35 %, extraction 18–22 %.
- Water properties: CoolProp (IAPWS-95 formulation).

#### What is assumed (not measured)
The pump and NPSH-required curves describe a hypothetical small pump. The press heat-loss conductance UA = 1 W/K,
grounds specific heat 1700 J/(kg K), mesh resistance, cake porosity, fines fraction, TDS meter noise and
carafe discharge coefficient are assumed values, marked in the code. Real-brew validation would replace them with measurements.

The full derivations, with every step, are in `docs/derivations.html`.
""")
