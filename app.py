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
from plant.style import COLORS

st.set_page_config(page_title="AI Barista Plant", page_icon="☕", layout="wide")
C2K = 273.15


# ---------------------------------------------------------------- cached calculations
@st.cache_data(max_entries=256, ttl=3600)
def simulate(grind_um, T_water_C, steep_s, ratio, m_coffee_g, preheated):
    sim = ph.brew(grind_um * 1e-6, T_water_C + C2K, steep_s, m_coffee=m_coffee_g / 1000,
                  m_water=m_coffee_g / 1000 * ratio, preheated=preheated)
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in sim.items()}


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
st.markdown("## ☕ AI BARISTA PLANT")
st.caption("A French press, modelled and operated like a chemical plant: fluid mechanics, material and energy balances, and an AI operator.")

VIEWS = ["Plant", "Trends", "Fluid units", "Lab notebook", "AI operator", "Presenter", "Engineering notes"]
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
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### F-101 · plunge filtration (Darcy's law)")
        st.markdown(f"Sauter diameter with fines d₃₂ = **{1e6 * plg['d32']:.0f} µm**, permeability k = **{plg['k']:.2e} m²**  \n"
                    f"Pressure drop: cake **{plg['dP_cake']:.0f} Pa** + mesh **{plg['dP_mesh']:.0f} Pa**, force **{plg['force']:.1f} N**")
        g = np.linspace(300, 1200, 60)
        fig = go.Figure(go.Scatter(x=g, y=[ph.plunge(x * 1e-6, T_brew_end, m_coffee=m_coffee / 1000, plunge_time=plunge_s,
                                                      fines_fraction=fines)["force"] for x in g],
                                   name="plunge force", line=dict(color=COLORS["coffee"])))
        fig.add_vline(x=grind, line=dict(color=COLORS["grey"], dash="dot"))
        fig.update_layout(xaxis_title="grind size d (µm)", yaxis_title="plunge force (N)", showlegend=True)
        st.plotly_chart(fig, width="stretch")
        st.caption("Kozeny–Carman is known to over-predict coffee-bed permeability (Corrochano et al. 2015), "
                   "and the mesh resistance and cake porosity are assumed values.")
    with c2:
        st.markdown("#### T-101 · fines settling (Stokes' law)")
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
        st.plotly_chart(fig, width="stretch")

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
