# AI Barista Plant

A French press, modelled and operated like a chemical plant. The coffee brewer is drawn as a process flow diagram, and every unit has real chemical engineering behind it:

| Unit | What it is | Engineering |
|---|---|---|
| E-101 | kettle | hot water feed |
| R-101 | French press | batch extraction (material balance) + cooling (energy balance) |
| F-101 | plunger filter | Darcy flow through the grounds cake, Kozeny–Carman |
| T-101 | cup | Stokes settling of fines |

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
- `plant/steps.py` holds every derivation as Write / Say steps (used by the Presenter view and `docs/derivations.html`).
- `tests/test_standards.py` enforces the professor's rules: every symbol defined with SI units, strict KaTeX, pint unit checks, no silent extrapolation.

## Rebuild the math documents

`docs/*.html` are rendered from `docs/*.src.html` with KaTeX on the server, so they open offline with no CDN:

```bash
(cd docs && npm install)
PYTHONPATH=. python scripts/build_guide.py      # derivations.src.html from plant/steps.py
NODE_PATH=docs/node_modules node docs/render_katex.js docs/derivations.src.html docs/derivations.html
NODE_PATH=docs/node_modules node docs/render_katex.js docs/study_guide.src.html docs/study_guide.html
```
