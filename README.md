# AI Barista Plant

A French press, modelled and operated like a chemical plant. The coffee brewer is drawn as a process flow diagram, and every unit has real chemical engineering behind it:

| Unit | What it is | Engineering |
|---|---|---|
| E-101 | kettle | energy balance |
| P-101 | pump + transfer line | Darcy–Weisbach, Colebrook, minor losses, pump vs system curve, NPSH / cavitation |
| R-101 | French press | batch extraction (material balance) + cooling (energy balance) |
| A-101 | stirrer | impeller Reynolds number and power |
| F-101 | plunger filter | Darcy flow through the grounds cake, Kozeny–Carman |
| T-101 | cup | Stokes settling of fines |
| D-101 | carafe | Torricelli draining |

An **AI operator** (Gaussian process models from scikit-learn) chooses the next recipe with the highest chance of landing in the SCA ideal cup, and you can race it head to head.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Test it

```bash
pip install pytest
pytest -q
python scripts/benchmark.py   # re-run the AI vs. baseline benchmark (a few minutes)
```

## Layout

- `app.py` is the Streamlit user interface, kept thin.
- `plant/physics.py` holds every model as plain functions, in SI units, with the sources listed at the top.
- `plant/ai.py` contains the AI operator and the baselines (one factor at a time, and random).
- `plant/diagram.py` draws the SVG process flow diagram.
- `docs/derivations.html` derives every equation, with every symbol defined.

## Rebuild the math documents

`docs/*.html` are rendered from `docs/*.src.html` with KaTeX on the server, so they open offline with no CDN:

```bash
npm install katex@0.16.22
node docs/render_katex.js docs/derivations.src.html docs/derivations.html
node docs/render_katex.js docs/study_guide.src.html docs/study_guide.html
```
