# AI Barista: plan for approval (v1)

**One-line pitch:** Treat a cup of coffee as a small chemical process: flow through a packed bed, mass transfer out of the grounds, and heat loss. Fit a physics model to your own brews, then let an AI choose the next recipe so you reach a target cup in as few brews as possible.

The plan has no equations on purpose. Every equation will be derived step by step, with every symbol defined in SI units, in a separate HTML derivation document once the plan is approved.

---

## Grill-me questions (answer with numbers, or just say "proceed" to accept every recommended answer)

1. **Which brewer do you have or can borrow?** Recommended: French press. Immersion brewing makes the material balance a clean well-mixed batch, and pressing gives a measurable flow step. An AeroPress is just as good; pour-over is possible but harder because the mass balance becomes a packed-bed PDE.
2. **How will we measure coffee strength?** Recommended: a cheap conductivity "TDS" meter (about US$10–15) plus a 0.01 g kitchen scale (about US$15), with the meter calibrated against oven-drying samples. That calibration is its own small ChemE analysis. Alternatives: a coffee refractometer (about US$100+, most accurate) or taste scores only (free, but weakest evidence).
3. **How many brews can you make?** Recommended: 15–20 brews over about two weeks, with a blind taste score (1–10) on each.
4. **Where should the notebooks live?** Recommended: marimo notebooks in this project's files folder for now, and a GitHub repo plus MoLab link once the code is stable. The repo step needs your go-ahead, see the push authorization at the end.
5. **What target cup should the AI aim for?** Recommended: the Specialty Coffee Association "brewing control chart" ideal box (strength and extraction yield in the published ideal range), then your own taste score once you have data.

---

## What the project contains

| Part | ChemE subject | What it does |
|---|---|---|
| A. Flow | Fluid mechanics | Darcy's law with Kozeny–Carman permeability predicts how long the press or drawdown takes from grind size, bed depth, water viscosity and pressure. |
| B. Extraction | Material balance | A batch mass balance on dissolved coffee solids, with a fast "surface wash" and a slow diffusion-limited part. Grind size sets the diffusion time. |
| C. Cooling | Energy balance | A lumped energy balance gives the brew temperature over time, including the initial drop when hot water hits room-temperature grounds. Temperature feeds back into diffusion speed. |
| D. Calibration | ChemE analysis | A calibration curve from TDS meter reading to true dissolved solids, built from oven-dried samples, with error bars. |
| E. Model fitting | Analysis + AI | Fit the unknown physical parameters to your measured brews with scipy least squares, with confidence intervals. |
| F. AI barista | AI | Bayesian optimization (a Gaussian process from scikit-learn) proposes the next recipe (grind, temperature, time, coffee-to-water ratio) that is most likely to improve the cup. |
| G. Honest benchmark | Analysis | On a "virtual coffee" built from the fitted model, compare the AI against a tuned grid search and random recipes: how many brews each needs to reach the target. |

**The key insight to show your professor:** grind size controls *both* the fluid mechanics and the mass transfer, in opposite directions. Finer grounds extract faster (the diffusion time scales with particle size squared) but flow slower (the permeability also scales with particle size squared). The best recipe is a trade-off between the two, and the AI finds it with very few experiments.

---

## Steps (each reads: action — verify: check)

1. Look up literature values (coffee bed porosity, soluble fraction of beans, effective diffusivity, the SCA ideal box) from primary papers — verify: every value has a citation, and I flag anything I could not confirm.
2. Write the HTML derivation document (all three balances, every symbol defined with SI units, KaTeX rendered with no internet needed) — verify: strict KaTeX parse passes and a screenshot of every equation is checked.
3. Build notebook 1, the physics model (marimo, plotly, sliders for grind, temperature, time and ratio) — verify: `marimo check --strict` passes, a full kernel run via `marimo export` succeeds, and a standard French press recipe predicts strength inside the published typical range.
4. Build notebook 2, TDS meter calibration from your oven-dried samples — verify: it runs on a synthetic example first, then reports the calibration line with an uncertainty band.
5. Build the brew-log template (a spreadsheet with units in every column header) — verify: notebook 3 reads it without errors and rejects missing or out-of-range values loudly.
6. Build notebook 3, fitting the model to your brews — verify: on synthetic brews with known parameters, the fit recovers them within their confidence intervals.
7. Build notebook 4, the AI barista (Bayesian optimization) — verify: on the virtual coffee, it reaches the target in fewer brews than a tuned grid search and random search, averaged over at least 20 random seeds, shown as "best found".
8. You brew and log; we refit and let the AI pick recipes — verify: predicted vs. measured strength for each new brew, with error bars.
9. Write the study guide of likely professor questions, with answers — verify: every answer points to the notebook cell or derivation section that backs it.

**Smallest success check (before anything else):** Notebook 1 runs end to end, and for a standard French press recipe it predicts a strength inside the published typical range using only literature parameters.

---

## Assumptions (tell me if any are wrong)

- You have a grinder with numbered settings, or can borrow one. Grind size will be estimated from a phone photo of grounds on white paper using scikit-image.
- You have a kitchen thermometer, or can get one cheaply.
- Your brewing water is ordinary tap or bottled water. Very hard water shifts conductivity readings, which the calibration step accounts for.
- Notebooks run on a normal laptop or MoLab's free CPU machine. No GPU is needed.
- No repository exists yet, so nothing gets pushed anywhere until you say so.

## Facts I will research myself (I won't ask you)

- Typical porosity of a coffee bed and how it changes with grind.
- The soluble fraction of roasted coffee and its effective diffusivity.
- The SCA brewing control chart values.
- Water viscosity and density versus temperature (from a property library, not hand-typed).

## Choices that are yours (with costs)

- **Strength measurement:** TDS meter plus scale at about US$25–30, refractometer at about US$100+, or taste only for free with weaker evidence.
- **Brewer:** you may already own one; a French press costs about US$15–25 if not.
- **Time:** about 15–20 brews and roughly 10 minutes of logging each.

## Push authorization (conditional)

If you want the MoLab link, I'd create a GitHub repository for the project and push the notebooks there once each one passes its checks. Reply "push OK" along with your approval and I'll do that without asking again. Otherwise, everything stays in this project's files.
