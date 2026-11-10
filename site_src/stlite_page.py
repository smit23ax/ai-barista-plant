"""Write site/app/index.html: the full Streamlit app running in the browser with stlite (Python compiled to
WebAssembly by Pyodide). Experimental: the static explorer and Streamlit Cloud remain the main demos.

The page loads @stlite/browser STLITE_VERSION from jsDelivr, which loads Pyodide and its packages (numpy, scipy,
pandas, scikit-learn, CoolProp) from jsDelivr as well; plotly and pint are pure-Python wheels installed from PyPI.
The app's own files are embedded in the page as strings, so the browser runs exactly the repository's code.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STLITE_VERSION = "1.12.1"
CDN = f"https://cdn.jsdelivr.net/npm/@stlite/browser@{STLITE_VERSION}/build"
REQUIREMENTS = ["numpy", "scipy", "pandas", "scikit-learn", "CoolProp", "plotly", "pint"]


def app_files():
    """Every file the app reads at run time, keyed by its path relative to the repository root."""
    paths = [ROOT / "app.py", *sorted((ROOT / "plant").glob("*.py")), ROOT / "plant" / "benchmark.json",
             *sorted((ROOT / "data").glob("*.json"))]
    return {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8") for p in paths if p.exists()}


def page(cdn=CDN):
    files = json.dumps(app_files())
    reqs = json.dumps(REQUIREMENTS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Barista Plant (in-browser)</title>
<link rel="stylesheet" href="{cdn}/stlite.css">
<style>body{{margin:0;background:#f7f9fc;font-family:system-ui,sans-serif}}
#note{{padding:10px 16px;font-size:14px;background:#fff8e1;border-bottom:1px solid #e5d9a8}}</style></head>
<body><div id="note">Experimental: this is the full app running in your browser (Python via WebAssembly). The first load downloads
about 60 MB and can take a minute. If it does not start, use the <a href="../demo.html">static explorer</a>.</div>
<div id="root"></div>
<script type="module">
import {{ mount }} from "{cdn}/stlite.js";
const t0 = performance.now();
window.__stliteStart = t0;
mount({{ requirements: {reqs}, entrypoint: "app.py", files: {files} }}, document.getElementById("root"));
</script></body></html>"""


def write(out=ROOT / "site" / "app" / "index.html", cdn=CDN):
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(cdn), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(write())
