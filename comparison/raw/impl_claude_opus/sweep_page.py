"""Write sweep.html: k, dP and force versus grind size (300-1200 um) at 341 K."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ergun_plunge import plunge

T_BREW = 341.0  # water temperature (K)


def main(path="sweep.html"):
    d_um = np.linspace(300.0, 1200.0, 91)            # grind size (um)
    res = [plunge(d * 1e-6, T_BREW) for d in d_um]
    k = [r["k"] for r in res]                        # permeability (m^2)
    dP = [r["dP"] for r in res]                      # total pressure drop (Pa)
    dP_cake = [r["dP_cake"] for r in res]            # cake pressure drop (Pa)
    dP_mesh = [r["dP_mesh"] for r in res]            # mesh pressure drop (Pa)
    force = [r["force"] for r in res]                # plunger force (N)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.07,
                        subplot_titles=("Permeability k",
                                        "Pressure drop",
                                        "Plunger force"))
    fig.add_trace(go.Scatter(x=d_um, y=k, name="k (m²)"), 1, 1)
    fig.add_trace(go.Scatter(x=d_um, y=dP, name="dP total (Pa)"), 2, 1)
    fig.add_trace(go.Scatter(x=d_um, y=dP_cake, name="dP cake (Pa)",
                             line=dict(dash="dash")), 2, 1)
    fig.add_trace(go.Scatter(x=d_um, y=dP_mesh, name="dP mesh (Pa)",
                             line=dict(dash="dot")), 2, 1)
    fig.add_trace(go.Scatter(x=d_um, y=force, name="force (N)"), 3, 1)

    fig.update_yaxes(title_text="k (m²)", type="log", row=1, col=1)
    fig.update_yaxes(title_text="ΔP (Pa)", row=2, col=1)
    fig.update_yaxes(title_text="F (N)", row=3, col=1)
    fig.update_xaxes(title_text="Nominal grind diameter d (µm)", row=3, col=1)
    fig.update_layout(
        title=dict(text=f"French press plunge vs grind size, T = {T_BREW:g} K",
                   x=0.0, xanchor="left"),
        autosize=True, height=900, template="plotly_white",
        margin=dict(l=60, r=20, t=70, b=120),
        # Legend placed below the plot area so it never overlaps traces and
        # works on narrow (390 px) as well as wide (1400 px) screens.
        legend=dict(orientation="h", x=0.0, xanchor="left",
                    y=-0.08, yanchor="top"),
        hovermode="x unified",
    )
    fig.write_html(path, include_plotlyjs="cdn", full_html=True,
                   config={"responsive": True},
                   default_width="100%", default_height="900px")
    return path


if __name__ == "__main__":
    print("wrote", main())
