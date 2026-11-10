"""Build the submission website into site/ (served by GitHub Pages).

    PYTHONPATH=. python site_src/build.py            # preview build: lists open TODO-ALEX items on the Overview
    FINAL=1 PYTHONPATH=. python site_src/build.py    # final build: fails while any required evidence is missing

Pages are written as HTML with KaTeX math (\\( \\) inline, $$ $$ display), then rendered on the server by
site_src/render_katex.js (strict parse, no CDN). Every number comes from site_src/analysis.py.
Owner-supplied content lives in site_src/content/ (video id, transcript, members, learnings, dates).
"""
import html
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import plotly.io as pio

from site_src import analysis, explorer, pages

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
CONTENT = ROOT / "site_src" / "content"
REPO = "https://github.com/smit23ax/ai-barista-plant"
APP = "https://ai-barista-plant-wx5vazaq38wgr9etvrwzkt.streamlit.app/"

NAV = [("index.html", "Overview"), ("demo.html", "Demo"), ("course.html", "Packed bed"),
       ("process.html", "How it was made"), ("comparison.html", "Model comparison"),
       ("presentation.html", "Video & transcript"), ("learnings.html", "Learnings"),
       ("references.html", "References & credit"), ("records.html", "Records")]


def owner_content():
    """Files alex fills in. A missing or empty file means the item is still to do."""
    read = lambda name: (CONTENT / name).read_text().strip() if (CONTENT / name).exists() else ""
    return {"video_id": read("youtube_video_id.txt"), "transcript": read("youtube_transcript.txt"),
            "comments_url": read("youtube_comments_posted.txt"), "members": read("members.html"),
            "learnings": read("learnings.html"), "dates": read("presentation_dates.html"),
            "streamlit_commit": read("streamlit_cloud_check.txt"),
            "implementations": sorted((ROOT / "comparison" / "raw").glob("impl_*")) if (ROOT / "comparison" / "raw").exists() else []}


def checklist(c):
    """The ten release items (ChatGPT's list, adopted in plan v5) and whether each has its evidence."""
    return [
        ("Public website opens without signing in", True, "this page is public on GitHub Pages"),
        ("Static Ergun explorer matches the Python model at every grid point", True, "tests/test_site.py"),
        ("Streamlit Cloud demo link works and runs current code", bool(c["streamlit_commit"]), "content/streamlit_cloud_check.txt"),
        ("At least two AI-model implementations documented and scored", len(c["implementations"]) >= 2, "comparison/raw/impl_*"),
        ("Accept/reject decisions published", True, "comparison.html"),
        ("YouTube presentation embedded", bool(c["video_id"]), "content/youtube_video_id.txt"),
        ("Practice transcript and AI critique posted in YouTube comments", bool(c["comments_url"]), "content/youtube_comments_posted.txt"),
        ("Verbatim YouTube auto-generated transcript displayed", bool(c["transcript"]), "content/youtube_transcript.txt"),
        ("References and every member's contributions complete", bool(c["members"]), "content/members.html"),
        ("Presentation dates confirmed", bool(c["dates"]), "content/presentation_dates.html"),
    ]


def layout(filename, title, body):
    nav = "".join(f'<a href="{f}"{" class=\"on\"" if f == filename else ""}>{label}</a>' for f, label in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="Flow through a packed bed of coffee grounds: Ergun equation, dimensional analysis and grind size. An AI project.">
<link rel="stylesheet" href="katex.css"><link rel="stylesheet" href="style.css">
<script src="plotly.min.js"></script>
</head><body>
<header class="site"><p class="kicker">AI Barista Plant · fluid mechanics final project</p>
<nav class="pills">{nav}</nav></header>
<main>{body}</main>
<script>window.addEventListener("load",()=>document.querySelectorAll(".js-plotly-plot").forEach(d=>{{if(d.offsetParent)Plotly.Plots.resize(d)}}));</script>
<footer>An AI project: built with Claude (Anthropic) and critiqued by Muse, ChatGPT and Grok, directed by the student group.
Source: <a href="{REPO}">{REPO.removeprefix("https://")}</a>. Labels: <span class="label exp">compared with experimental data</span>
<span class="label model">model-predicted</span><span class="label illus">illustrative</span></footer>
</body></html>"""


def fig_html(fig, div_id):
    return pio.to_html(fig, include_plotlyjs=False, full_html=False, div_id=div_id,
                       config={"displayModeBar": False, "responsive": True})


def build():
    final = os.environ.get("FINAL") == "1"
    c = owner_content()
    items = checklist(c)
    missing = [name for name, ok, _ in items if not ok]
    if final and missing:
        sys.exit("FINAL build refused. Missing evidence for:\n  - " + "\n  - ".join(missing))

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "site_src" / "style.css", OUT / "style.css")
    plotly_js = Path(pio.__file__).resolve().parents[1] / "package_data" / "plotly.min.js"
    shutil.copy(plotly_js, OUT / "plotly.min.js")
    (OUT / ".nojekyll").write_text("")
    for doc in ["derivations.html", "study_guide.html"]:
        shutil.copy(ROOT / "docs" / doc, OUT / doc)

    n = analysis.numbers()
    figs = {"explorer": '<div class="wide">' + fig_html(explorer.figure(), "explorer") + '</div><div class="narrow">'
                        + fig_html(explorer.figure(narrow=True), "explorer_narrow") + "</div>",
            "parity": fig_html(analysis.parity_figure(), "parity"),
            "ceff": fig_html(analysis.ceff_figure(), "ceff"),
            "sens": fig_html(analysis.sensitivity_figure(), "sens")}
    ctx = {"n": n, "c": c, "items": items, "missing": missing, "final": final, "figs": figs, "REPO": REPO, "APP": APP}
    written = []
    for filename, title in NAV:
        body = getattr(pages, filename.removesuffix(".html"))(ctx)
        (OUT / filename).write_text(layout(filename, title + " · AI Barista Plant", body))
        written.append(str(OUT / filename))
    env = {**os.environ, "NODE_PATH": str(ROOT / "docs" / "node_modules")}
    subprocess.run(["node", str(ROOT / "site_src" / "render_katex.js"), str(OUT / "katex.css"), *written], check=True, env=env)
    (OUT / "build.json").write_text(json.dumps({"final": final, "missing": missing}, indent=1))
    print("built", len(written), "pages;", "FINAL" if final else "preview", "; missing:", missing)


if __name__ == "__main__":
    build()
