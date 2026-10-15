"""Build docs/derivations.src.html from plant/steps.py, so the printable guide and the app's presenter mode
show the same Write / Say steps. Render to HTML with:  node docs/render_katex.js docs/derivations.src.html docs/derivations.html
"""
import html
from pathlib import Path

from plant.steps import SYMBOLS, UNITS

out = ['<h1>AI Barista Plant: derivations</h1>',
       '<p class="lead">Every unit in the professor\'s format: a numbered <b>Write</b> line (the equation) and a '
       '<b>Say</b> line (plain words), the sign convention, a degree-of-freedom analysis, physical checks and likely '
       'questions. The same steps drive the app\'s Presenter view. Numbers are for the standard recipe: 800 µm grind, '
       '93 °C kettle, 4 min steep, 15 g coffee in 250 g water.</p>',
       '<div class="toc">' + "".join(f'<a href="#u{i}">{i}. {html.escape(n)}</a>' for i, n in enumerate(UNITS, 1))
       + '<a href="#symbols">Symbol table</a></div>']

for i, (name, u) in enumerate(UNITS.items(), 1):
    d = u["dof"]
    out.append(f'<h2 id="u{i}">{i}. {html.escape(u["title"])}</h2>')
    out.append(f'<p class="phys"><b>Sign convention.</b> {html.escape(u["sign"])}</p>')
    out.append('<h3>Degrees of freedom</h3><ul>'
               f'<li><b>Unknowns:</b> {html.escape("; ".join(d["unknowns"]))}</li>'
               f'<li><b>Equations:</b> {html.escape("; ".join(d["equations"]))}</li>'
               f'<li><b>Specified:</b> {html.escape(", ".join(d["specified"]))}</li>'
               f'<li><b>Result:</b> {html.escape(d["result"])}</li></ul>')
    out.append('<h3>Steps</h3>')
    for k, st in enumerate(u["steps"], 1):
        out.append(f'<p><b>{k}. {html.escape(st["title"])}</b></p>'
                   f'<p><b>Write:</b></p>$${html.escape(st["write"], quote=False)}$$'
                   f'<p><b>Say:</b> {html.escape(st["say"])}</p>')
    out.append('<h3>Physical checks</h3><ul>' + "".join(f'<li>{html.escape(c)}</li>' for c in u["checks"]) + '</ul>')
    out.append('<h3>Likely questions</h3>' + "".join(
        f'<p><b>Q{k}. {html.escape(q)}</b><br>{html.escape(a)}</p>' for k, (q, a) in enumerate(u["questions"], 1)))

out.append('<h2 id="symbols">Symbol table (SI units)</h2><table><tr><th>Symbol</th><th>Meaning</th><th>Unit</th></tr>')
for sym, (meaning, unit) in SYMBOLS.items():
    out.append(f'<tr><td>\\({html.escape(sym, quote=False)}\\)</td><td>{html.escape(meaning)}</td>'
               f'<td>{html.escape(unit)}</td></tr>')
out.append('</table>')
out.append('<h2>Sources</h2><ul>'
           '<li>Moroney et al. (2016), Coffee extraction kinetics in a well mixed system, J. Math. Industry 7: '
           'time scales, extractable fraction, solubility, cell size.</li>'
           '<li>Corrochano et al. (2015), J. Food Eng. 150: coffee solid density, particle porosity, bulk density, '
           'Kozeny–Carman accuracy for coffee beds.</li>'
           '<li>SCAA Golden Cup brewing control chart: strength 1.15–1.35 %, extraction 18–22 %.</li>'
           '<li>Water properties: CoolProp (IAPWS-95).</li></ul>')

Path(__file__).resolve().parents[1].joinpath("docs", "derivations.src.html").write_text("\n".join(out) + "\n")
print("wrote docs/derivations.src.html:", sum(len(u["steps"]) for u in UNITS.values()), "steps,", len(SYMBOLS), "symbols")
