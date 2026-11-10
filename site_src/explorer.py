"""Static grind-size explorer for the GitHub Pages site.

Every number is computed here, in Python, by plant.physics.plunge (the same function the app and the tests use).
The browser only shows the precomputed values: the slider selects one grind from the grid, it does not
interpolate and runs no physics in JavaScript.

Symbols (SI units):
  d      nominal grind size (m; shown in micrometres)
  T      bed temperature during the plunge (K); 341 K is the end-of-steep temperature of the default recipe
  K      Darcy permeability of the grounds cake (m^2)
  dP     pressure drop across cake + mesh (Pa); dP_cake, dP_mesh its two parts (Pa)
  F      plunge force = dP * press area (N); fluid resistance only (no seal friction, buoyancy or acceleration)
  Re_b   bed Reynolds number (-);  f_p  packed-bed friction factor (-)
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from plant import physics, style  # noqa: F401  (style registers the shared "plant" plotly template)

GRID_UM = np.arange(300, 1201, 10)          # same range and step as the app's grind slider, micrometres
T_PLUNGE = 341.0                             # K, end-of-steep bed temperature for the default recipe
DEFAULT_UM = 800
OUTPUTS = ["k", "dP", "dP_cake", "dP_mesh", "force", "Re_b", "f_p", "inertial_share"]


def sweep(grid_um=GRID_UM, T=T_PLUNGE):
    """plunge() at every grind of the grid, defaults for everything else. Returns {output: np.array}."""
    rows = [physics.plunge(g * 1e-6, T) for g in grid_um]
    return {key: np.array([r[key] for r in rows]) for key in OUTPUTS}


def figure(data=None, grid_um=GRID_UM, narrow=False):
    """Four linked panels and one slider. Traces 0-6 are fixed curves; traces 7-10 are the selected-grind markers
    that the slider moves (restyle), and the title line shows the selected values (relayout)."""
    data = sweep(grid_um) if data is None else data
    x = grid_um.astype(float)
    pos = [(1, 1), (2, 1), (3, 1), (4, 1)] if narrow else [(1, 1), (1, 2), (2, 1), (2, 2)]
    fig = make_subplots(rows=4 if narrow else 2, cols=1 if narrow else 2, horizontal_spacing=0.12,
                        vertical_spacing=0.095 if narrow else 0.2, subplot_titles=(
        "Permeability K (m²)", "Pressure drop Δp (Pa)", "Plunge force F (N)", "Ergun chart: f_p vs Re_b"))
    c = style.COLORS
    fig.add_trace(go.Scatter(x=x, y=data["k"], name="K", line=dict(color=c["water"])), *pos[0])
    fig.add_trace(go.Scatter(x=x, y=data["dP"], name="Δp total", line=dict(color=c["alarm"])), *pos[1])
    fig.add_trace(go.Scatter(x=x, y=data["dP_cake"], name="Δp cake (Ergun)", line=dict(color=c["coffee"])), *pos[1])
    fig.add_trace(go.Scatter(x=x, y=data["dP_mesh"], name="Δp mesh", line=dict(color=c["grey"], dash="dot")), *pos[1])
    fig.add_trace(go.Scatter(x=x, y=data["force"], name="F", line=dict(color=c["ok"])), *pos[2])
    re_line = np.logspace(-2, 3, 200)
    fig.add_trace(go.Scatter(x=re_line, y=physics.ERGUN_VISCOUS / re_line + physics.ERGUN_INERTIAL,
                             name="Ergun 150/Re_b + 1.75", line=dict(color=c["grey"])), *pos[3])
    fig.add_trace(go.Scatter(x=data["Re_b"], y=data["f_p"], name="press, 300–1200 µm",
                             line=dict(color=c["coffee"], width=5), opacity=0.5), *pos[3])
    i0 = int(np.flatnonzero(grid_um == DEFAULT_UM)[0])
    marker = dict(size=11, color=c["alarm"], line=dict(color="white", width=1.5))
    for (row, col), ykey, xs in zip(pos, ["k", "dP", "force", "f_p"], [x, x, x, data["Re_b"]]):
        fig.add_trace(go.Scatter(x=[xs[i0]], y=[data[ykey][i0]], mode="markers", marker=marker,
                                 showlegend=False, hoverinfo="skip"), row, col)

    steps = []
    for i, g in enumerate(grid_um):
        steps.append(dict(label=f"{g}", method="update", args=[
            {"x": [[x[i]], [x[i]], [x[i]], [data["Re_b"][i]]],
             "y": [[data["k"][i]], [data["dP"][i]], [data["force"][i]], [data["f_p"][i]]]},
            {"title.text": readout(data, i, g, narrow)}, [7, 8, 9, 10]]))
    fig.update_layout(
        title=dict(text=readout(data, i0, DEFAULT_UM, narrow), x=0, font=dict(size=13 if narrow else 14)),
        height=1450 if narrow else 720, margin=dict(l=60, r=10, t=150, b=290) if narrow else dict(l=70, r=20, t=110, b=120),
        legend=dict(orientation="h", x=0, y=-0.135 if narrow else -0.32, yanchor="top"),
        sliders=[dict(active=i0, steps=steps, x=0, len=1, y=-0.045 if narrow else -0.12, pad=dict(t=10),
                      currentvalue=dict(prefix="grind size d = ", suffix=" µm", font=dict(size=13)))])
    for row, col in pos[:3]:
        fig.update_xaxes(title_text="grind size d (µm)", row=row, col=col)
    fig.update_yaxes(type="log", exponentformat="power", row=pos[0][0], col=pos[0][1])
    re_lo, re_hi = np.log10(data["Re_b"].min()) - 0.2, np.log10(data["Re_b"].max()) + 0.2
    fp_lo = np.log10(data["f_p"].min()) - 0.2
    fp_hi = np.log10(data["f_p"].max()) + 0.2
    fig.update_xaxes(type="log", range=[min(re_lo, -1.2), max(re_hi, 1.2)], title_text="Re_b (-)", row=pos[3][0], col=pos[3][1])
    fig.update_yaxes(type="log", range=[fp_lo, fp_hi], title_text="f_p (-)", row=pos[3][0], col=pos[3][1])
    if narrow:
        fig.layout.sliders[0].currentvalue.prefix = "d = "
    return fig


def readout(data, i, g, narrow=False):
    """The selected grind's values, with units (one line, or stacked lines on a phone)."""
    parts = [f"d = {g} µm", f"K = {data['k'][i]:.3g} m²", f"Δp = {data['dP'][i]:.3g} Pa", f"F = {data['force'][i]:.3g} N",
             f"Re_b = {data['Re_b'][i]:.3g}", f"inertial share = {100 * data['inertial_share'][i]:.2g} %"]
    return "<br>".join(" · ".join(parts[j:j + 2]) for j in (0, 2, 4)) if narrow else " · ".join(parts)
