"""The app's look: a light "lab notebook" page (faint grid, serif headings, blue accent, white cards).
One plotly template for every chart (white cards, light gridlines, legends outside the plot area),
the page CSS, and two small HTML helpers for the header and section labels."""
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

INK, MUTED, ACCENT, BORDER, CARD, PAGE, CODE_BG = "#18202b", "#5b6676", "#2f6fd6", "#dbe3ee", "#ffffff", "#f4f7fb", "#eaf0f7"
COLORS = {"water": "#2f6fd6", "coffee": "#9a5b2e", "ok": "#1f9d55", "warn": "#d08300",
          "alarm": "#d64545", "grey": "#7a8696", "ai": "#7b4fd0", "human": "#2f6fd6"}

pio.templates["plant"] = go.layout.Template(pio.templates["plotly_white"])
pio.templates["plant"].layout.update(
    paper_bgcolor=CARD, plot_bgcolor=CARD,
    font=dict(family="IBM Plex Sans, Segoe UI, Helvetica, Arial, sans-serif", size=12, color=INK),
    title=dict(font=dict(family="Fraunces, Georgia, serif", size=16, color=INK)),
    xaxis=dict(gridcolor="#edf1f6", zeroline=False, linecolor="#c6d0dd", ticks="outside", tickcolor="#c6d0dd"),
    yaxis=dict(gridcolor="#edf1f6", zeroline=False, linecolor="#c6d0dd", ticks="outside", tickcolor="#c6d0dd"),
    legend=dict(orientation="h", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="rgba(0,0,0,0)"),
    colorway=[COLORS[k] for k in ["water", "coffee", "ok", "warn", "ai", "alarm", "grey"]],
    margin=dict(l=60, r=20, t=60, b=50),
)
# No floating toolbar: it covered titles and legends. Charts stay interactive (hover, zoom by drag).
CHART_CONFIG = {"displayModeBar": False}
pio.templates.default = "plant"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
:root {{ --ink:{INK}; --muted:{MUTED}; --accent:{ACCENT}; --border:{BORDER}; --card:{CARD}; }}
.stApp {{
  background-color:{PAGE};
  background-image: linear-gradient(rgba(47,111,214,.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(47,111,214,.05) 1px, transparent 1px);
  background-size: 24px 24px;
}}
html, body, .stApp, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {{
  font-family: 'IBM Plex Sans', 'Segoe UI', Helvetica, Arial, sans-serif; color: var(--ink);
}}
h1, h2, h3, h4, h5, [data-testid="stHeadingWithActionElements"] {{
  font-family: 'Fraunces', Georgia, 'Times New Roman', serif !important; color: var(--ink); letter-spacing: -0.01em;
}}
h4 {{ font-weight: 800 !important; }}
h5 {{ font-weight: 600 !important; }}
[data-testid="stHeaderActionElements"] {{ display: none; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 2.2rem; max-width: 1240px; }}
[data-testid="stHeader"] {{ background: transparent; }}

/* header */
.stApp [data-testid="stMarkdownContainer"] p.bp-kicker {{ font-size: 12px !important; }}
.stApp [data-testid="stMarkdownContainer"] p.bp-label {{ font-size: 11px !important; }}
.stApp [data-testid="stMarkdownContainer"] p.bp-sub {{ font-size: 1.05rem !important; }}
.bp-kicker {{ font: 500 12px 'IBM Plex Mono', ui-monospace, Menlo, monospace; letter-spacing: .14em;
  text-transform: uppercase; color: var(--accent); margin: 0 0 6px; }}
.bp-title {{ font: 800 clamp(2.1rem, 5vw, 3.2rem)/1.05 'Fraunces', Georgia, serif; color: var(--ink); margin: 0 0 10px; }}
.bp-sub {{ font: 400 1.05rem/1.55 'IBM Plex Sans', sans-serif; color: var(--muted); max-width: 46rem; margin: 0 0 18px; }}
.bp-label {{ font: 500 11px 'IBM Plex Mono', ui-monospace, monospace; letter-spacing: .14em; text-transform: uppercase;
  color: var(--muted); margin: 6px 0 2px; }}

/* goal box under the header */
.bp-goal {{ background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 12px;
  padding: 12px 16px; margin: 0 0 18px; max-width: 52rem; box-shadow: 0 1px 3px rgba(24,32,43,.05); }}
.stApp [data-testid="stMarkdownContainer"] .bp-goal p {{ margin: 0; font-size: 1rem !important; line-height: 1.55; color: var(--ink); }}
.bp-goal b {{ font: 500 12px 'IBM Plex Mono', ui-monospace, monospace; letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); margin-right: 8px; }}

/* pill tabs */
[data-testid="stButtonGroup"] [role="radiogroup"] {{ gap: 8px; flex-wrap: wrap; }}
[data-testid="stButtonGroup"] button {{
  border-radius: 999px !important; border: 1px solid var(--border) !important; background: var(--card) !important;
  padding: 6px 18px !important; box-shadow: 0 1px 2px rgba(24,32,43,.04);
}}
[data-testid="stButtonGroup"] button p {{ font-weight: 600; color: var(--ink); }}
[data-testid="stButtonGroup"] button[aria-checked="true"] {{ background: var(--accent) !important; border-color: var(--accent) !important; }}
[data-testid="stButtonGroup"] button[aria-checked="true"] p {{ color: #fff !important; }}

/* cards */
[data-testid="stMetric"], [data-testid="stPlotlyChart"], [data-testid="stImage"], [data-testid="stExpander"] details,
[data-testid="stForm"], [data-testid="stTable"], [data-testid="stDataFrame"] {{
  background: var(--card); border: 1px solid var(--border) !important; border-radius: 14px;
  box-shadow: 0 1px 3px rgba(24,32,43,.05);
}}
[data-testid="stMetric"] {{ padding: 14px 16px; }}
[data-testid="stMetricLabel"] p {{ font: 600 12px 'IBM Plex Sans', sans-serif !important; letter-spacing: .04em; text-transform: uppercase; color: var(--muted); }}
[data-testid="stMetricValue"] {{ font-family: 'Fraunces', Georgia, serif; font-weight: 600; color: var(--ink); }}
[data-testid="stPlotlyChart"] {{ padding: 8px 6px 2px; overflow: hidden; }}
[data-testid="stImage"] {{ padding: 6px; }}
[data-testid="stImage"] img {{ border-radius: 10px; }}
.bp-pfd {{ background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 6px;
  box-shadow: 0 1px 3px rgba(24,32,43,.05); overflow-x: auto; margin-bottom: 14px; }}
.bp-pfd > div {{ min-width: 720px; }}
.bp-swipe {{ display: none; font: 500 12px 'IBM Plex Mono', monospace; color: var(--muted); margin: -8px 0 12px; }}
@media (max-width: 760px) {{ .bp-swipe {{ display: block; }} }}
[data-testid="stCaptionContainer"] {{ color: var(--muted); }}

/* equations: light blue-gray box like a worked-example page */
.katex-display {{ background: {CODE_BG}; border: 1px solid var(--border); border-radius: 12px; padding: 18px 14px; margin: 8px 0 !important;
  overflow-x: auto; overflow-y: hidden; max-width: 100%; }}
@media (max-width: 640px) {{ .katex-display {{ padding: 14px 8px; }} .katex-display > .katex {{ font-size: 0.92em; }} }}

/* sidebar */
[data-testid="stSidebar"] {{ background: #ffffff; border-right: 1px solid var(--border); }}
[data-testid="stSidebar"] [data-testid="stForm"] {{ box-shadow: none; }}
[data-testid="stAlert"] {{ border-radius: 12px; }}
</style>
"""


def header(kicker, title, sub):
    """Page header in the reference style: blue mono kicker, big serif title, muted subtitle."""
    drop = ('<svg width="12" height="14" viewBox="0 0 12 14" style="vertical-align:-2px;margin-right:8px">'
            '<path d="M6 1 C6 1 1.5 6.5 1.5 9 a4.5 4.5 0 0 0 9 0 C10.5 6.5 6 1 6 1 Z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')
    return f'<p class="bp-kicker">{drop}{kicker}</p><h1 class="bp-title">{title}</h1><p class="bp-sub">{sub}</p>'


def label(text):
    """Small uppercase mono section label, e.g. 'START HERE'."""
    return f'<p class="bp-label">{text}</p>'


def card(fig):
    """Apply the page look to a figure explicitly. Streamlit's own chart theme can override the default
    template, so the key colours are set on the figure itself."""
    fig.update_layout(template="plant", paper_bgcolor=CARD, plot_bgcolor=CARD,
                      font=dict(family="IBM Plex Sans, Segoe UI, Helvetica, Arial, sans-serif", size=13, color=INK))
    fig.update_xaxes(gridcolor="#e3e9f1", linecolor="#c6d0dd", zeroline=False, title_font_size=14, title_standoff=8)
    fig.update_yaxes(gridcolor="#e3e9f1", linecolor="#c6d0dd", zeroline=False, title_font_size=14, title_standoff=8)
    return fig


def _pow10(v):
    k = int(round(np.log10(v)))
    return "10" + str(k).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


def _ticks(values):
    """0.0001 ... 10 000 written out. If the axis goes past 10 000, every label is a power of ten (10⁶), so an
    axis never mixes the two styles."""
    if max(values) > 1e4 or min(values) < 1e-4:
        return [_pow10(v) for v in values]
    return [f"{v:g}" if v < 1e4 else "10 000" for v in values]


def log_axis(fig, axis, lo, hi, values=None):
    """Log axis from 10^lo to 10^hi labelled only at powers of ten (or at the given values), so tick labels never crowd."""
    values = values or [10.0**k for k in range(int(np.ceil(lo)), int(np.floor(hi)) + 1)]
    upd = dict(type="log", range=[lo, hi], tickvals=values, ticktext=_ticks(values),
               minor=dict(showgrid=False, ticks=""))
    (fig.update_xaxes if axis == "x" else fig.update_yaxes)(**upd)
    return fig


def top_legend(fig, n_rows, title=None):
    """Legend stacked above the plot, one entry per row, with the top margin sized to fit it, so it can
    never overlap the axes or their titles at any screen width."""
    fig.update_layout(legend=dict(orientation="v", x=0, y=0.995, xanchor="left", yanchor="top", yref="container",
                                  title=dict(text=title) if title else None, font=dict(size=13)),
                      margin=dict(t=14 + 22 * (n_rows + bool(title))))
    return fig


def pfd(svg):
    """Wrap the process flow diagram in a card. On a narrow phone screen it keeps a readable minimum width
    and scrolls sideways instead of shrinking the text."""
    return f'<div class="bp-pfd"><div>{svg}</div></div><p class="bp-swipe">Swipe sideways to see the whole plant.</p>'


def goal(text):
    """The project's goal in one box under the header, so every view starts from the question."""
    return f'<div class="bp-goal"><p><b>Goal</b>{text}</p></div>'
