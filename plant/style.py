"""One shared plotly look for every chart: dark control-room background, minimal gridlines,
legend outside the plot area, fixed monospace font."""
import plotly.graph_objects as go
import plotly.io as pio

COLORS = {"water": "#58a6ff", "coffee": "#c08a5b", "ok": "#7ee787", "warn": "#f2b84b",
          "alarm": "#ff5f56", "grey": "#8b95a1", "ai": "#d2a8ff", "human": "#58a6ff"}

pio.templates["plant"] = go.layout.Template(pio.templates["plotly_dark"])
pio.templates["plant"].layout.update(
    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
    font=dict(family="ui-monospace, Menlo, monospace", size=12, color="#c9d1d9"),
    xaxis=dict(gridcolor="#21262d", zeroline=False, linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", zeroline=False, linecolor="#30363d"),
    legend=dict(x=1.02, y=1.0, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=60, r=170, t=50, b=50),
)
pio.templates.default = "plant"
