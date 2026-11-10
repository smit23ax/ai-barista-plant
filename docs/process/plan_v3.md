# AI Barista Plant: plan for approval (v3)

**What changed in v3:** fluid mechanics is now the backbone of the plant. Five more fluid units were added; see the new section "Fluid mechanics in the plant".

**What changed from v1:** the project becomes an **interactive website that looks like a chemical plant control room**. The coffee brewer is drawn as a process flow diagram, the same way you'd draw a distillation column, with real unit operations, instrument tags and live trend charts. Real brewing becomes optional validation instead of the core.

Equations stay out of this plan. They'll go into a separate HTML derivation document with every symbol defined in SI units.

---

## What the website looks like

**Screen 1, Process flow diagram (the "plant")**, drawn in the style of a P&ID:

| Coffee equipment | Shown as | ChemE subject behind it |
|---|---|---|
| Kettle | E-101 heater, with heat duty in W | Energy balance |
| Hot water line | P-101 pump and pipe to the brewer | Fluid mechanics (see below) |
| Grinder | SR-101 size reduction unit, with a particle size distribution | Particle analysis |
| French press chamber | R-101 batch extractor | Material balance (extraction kinetics) |
| Plunger and filter | F-101 packed-bed filter | Fluid mechanics (Darcy's law, Kozeny–Carman) |
| Carafe | D-101 decanter, drained by gravity into the mug | Fluid mechanics (Bernoulli / Torricelli) |
| Mug | T-101 product tank, cooling to ambient | Energy balance (lumped cooling) |
| TDS meter | AT-101 analyzer | Calibration, ChemE analysis |

Instrument tags appear on the diagram: TI for temperature, AT for strength, FI for flow and PI for pressure. Streams light up and fill as the batch runs.

**Screen 2, Control room.** Set the setpoints (grind size, water temperature, steep time, coffee-to-water ratio, plunge force) and press RUN BATCH. Live trend charts show temperature, dissolved solids and flow rate over time, like an operator's console. Alarms fire for out-of-spec batches (too weak, over-extracted, or a filter that "plugs" when the grind is too fine).

**Screen 3, Lab mode.** Every batch adds realistic measurement noise and lands in a lab notebook table, so the website behaves like a real experiment. You can download the data as CSV and compute the mass balance closure yourself.

**Screen 4, AI operator.** Bayesian optimization looks at all the batches so far and proposes the next setpoints, explaining *why* (exploring vs. exploiting). A head-to-head mode lets a human (your professor) and the AI each get 10 batches to hit the target cup, and a scoreboard shows who gets there first.

**Screen 5, Engineering notes.** Each unit operation links to its derivation, with every symbol defined.

---

## Fluid mechanics in the plant

| Unit | Fluid mechanics topic | What you can do on the website |
|---|---|---|
| P-101 hot water transfer line | Darcy–Weisbach pressure drop, friction factor from the Colebrook equation, minor losses in fittings, and pump curve vs. system curve | Change the pipe diameter, length and fittings, then watch the operating point move on the pump and system curves. |
| P-101 cavitation check | NPSH available vs. required, with the water vapor pressure rising sharply near 93 °C | Push the water temperature up and see the cavitation alarm trip. This is why real plants put pumps below hot tanks. |
| R-101 stirring | Impeller Reynolds number, and the power number to stirring power | Stir faster and see the flow go from laminar to turbulent, and how mixing speeds up extraction. |
| F-101 plunge filtration | Darcy's law through the grounds "cake" plus the filter-mesh resistance in series (classic filtration theory), with Kozeny–Carman permeability from grind size and porosity | Too fine a grind makes the plunge force spike, and a "filter plugged" alarm fires. |
| Fines settling in the cup | Stokes' law terminal velocity, with a check that the particle Reynolds number stays small enough for Stokes' law to hold | See how long you should wait before the last sip to avoid sludge, as a function of grind. |
| D-101 carafe drain | Bernoulli and Torricelli draining with a discharge coefficient | Drain time vs. spout size, compared against the measured pour if you brew for real. |

Every fluid unit shows its key dimensionless numbers (Reynolds, and the friction factor where it applies) live on the diagram. All water properties (density, viscosity, vapor pressure) come from a property library, not typed-in numbers.

---

## Grill-me questions (answer with numbers, or say "proceed" to accept every recommended answer)

1. **How do we build the website?** Recommended: a Streamlit app, which is Python with scipy, scikit-learn and plotly and is your professor's stated preference. It deploys free on Streamlit Community Cloud from a GitHub repo, and you click "Deploy" once on your own free account. Alternative: a single web page hosted here as a shareable link. That's instant with no accounts, but the physics would be hand-written in JavaScript, which breaks your professor's "use library routines" rule.
2. **Do you also brew real coffee?** Recommended: yes, 5–10 real French press brews as a validation section ("does the virtual plant match reality?"). That takes about US$25–30 for a TDS meter and a 0.01 g scale. If you'd rather not, the project is purely virtual and the model uses literature values, stated plainly as such.
3. **What's the head-to-head target?** Recommended: hit the Specialty Coffee Association ideal box for strength and extraction yield in the fewest batches.
4. **Where does the code live?** Recommended: a new GitHub repo under your account, which Streamlit Cloud needs anyway.
5. **What visual style?** Recommended: a dark industrial control-room look, like a real plant control system, with a light theme toggle.

---

## Steps (each reads: action — verify: check)

1. Research the literature values (bed porosity, soluble fraction, effective diffusivity, SCA ideal box) from primary papers — verify: every value is cited, and anything unconfirmed is flagged.
2. Write the derivation document (HTML, KaTeX rendered with no internet needed, every symbol in SI units) — verify: strict KaTeX parse plus a screenshot check of every equation.
3. Write the physics core as plain Python functions with no Streamlit calls: transfer line and pump, cavitation, stirring, filtration, settling, carafe drain, extraction and cooling. Use scipy's ODE and root solvers, and take water properties from a library — verify: unit tests, mass balance closure under 0.1%, a standard French press recipe predicting strength in the published typical range, friction factors matching a Moody chart check value, and each Stokes result flagged as invalid when the particle Reynolds number is too high.
4. Build the plant diagram and control room screens — verify: headless browser screenshots at desktop and phone widths, no overlapping labels, and charts render.
5. Build lab mode with noise and CSV export — verify: the exported CSV round-trips, and invalid setpoints are rejected with a clear message instead of failing silently.
6. Build the AI operator (scikit-learn Gaussian process with expected improvement) — verify: averaged over 20+ random seeds, it reaches the target in fewer batches than a tuned grid search and random search. Results are shown as "best found", with the baseline search visible.
7. Build the head-to-head mode and scoreboard — verify: a scripted full game runs through Streamlit's AppTest.
8. Deploy — verify: the public link loads on a fresh browser, and a full batch runs.
9. Optional real brews and validation page — verify: predicted vs. measured strength, with error bars.
10. Write the study guide of likely professor questions — verify: every answer points to the code or derivation section that backs it.

**Smallest success check:** the physics core alone (step 3) predicts a sensible French press strength from literature values and closes its mass balance, before any website work starts.

---

## Assumptions

- The model is lumped (well-mixed chamber, average particle size). It's simple enough for you to defend every line, and the website says so plainly.
- Plant tags and the diagram are teaching dress-up. The physics underneath is the real content.
- You can create free GitHub and Streamlit Community Cloud accounts.
- No GPU or paid services are needed.

## Facts I'll research myself (I won't ask you)

Coffee bed porosity, soluble fraction, diffusivity, the SCA chart values, and water properties versus temperature.

## Push authorization (conditional)

To deploy, the code has to live in a GitHub repo. Reply "push OK" with your approval and I'll create the repo and push each piece once it passes its checks, without asking again. I'll need the repo attached to this project, which I'll walk you through when we get there.
