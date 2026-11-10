"""Create a responsive HTML sweep of French-press flow resistance."""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ergun_plunge import plunge


def main():
    """Write sweep.html for d=300–1200 micrometers and T=341 K."""
    diameters_um = np.linspace(300.0, 1200.0, 181)  # Grind size (um)
    temperatures_K = 341.0  # Water temperature (K)
    results = [plunge(d_um * 1e-6, temperatures_K) for d_um in diameters_um]

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.09,
                        subplot_titles=("Permeability", "Pressure drop", "Plunger force"))
    for row, (key, label, legend_name) in enumerate((
        ("k", "Permeability k (m²)", "Permeability"),
        ("dP", "Pressure drop ΔP (Pa)", "Pressure drop"),
        ("force", "Force F (N)", "Plunger force"),
    ), start=1):
        fig.add_trace(go.Scatter(x=diameters_um, y=[r[key] for r in results],
                                 mode="lines", name=legend_name), row=row, col=1)
        fig.update_yaxes(title_text=label, row=row, col=1, automargin=True)
    fig.update_xaxes(title_text="Nominal grind diameter (µm)", row=3, col=1)
    fig.update_layout(
        title="French press cake + mesh resistance at 341 K",
        height=1050,
        margin=dict(l=75, r=25, t=110, b=235),
        legend=dict(orientation="v", x=0, y=-0.20, xanchor="left", yanchor="top",
                    bgcolor="rgba(255,255,255,0)", title_text="Series"),
        template="plotly_white",
    )
    chart = fig.to_html(full_html=False, include_plotlyjs=True,
                        config={"responsive": True, "displaylogo": False})
    html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>French press resistance sweep</title>"
            "<style>body{margin:0;font-family:Arial,sans-serif;}"
            ".chart{width:100%;max-width:1400px;margin:auto;}"
            "@media(max-width:500px){.chart{font-size:12px;}}"
            "</style></head><body><main class='chart'>" + chart + "</main></body></html>")
    Path("sweep.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
