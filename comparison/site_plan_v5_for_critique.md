# Request: final critique of my submission-website plan (v5)

I am a chemical engineering undergraduate. Below are (A) my project, (B) the course's submission requirements, verbatim, and (C) plan v5 for my final submission website. Claude Opus 5.5 wrote it, and it was revised after four rounds of critique from other AI models (Muse, ChatGPT and Grok). Please critique it as described in (D). Work only from this document and the links. You have not seen the earlier critiques, and that is deliberate.

---

## A. The project

- **Title:** AI Barista Plant: flow through a packed bed of coffee grounds (Ergun equation, dimensional analysis, grind size).
- **Professor's framing:** "Flow through a packed bed: Ergun equation, dimensional analysis, applied to an interesting topic (coffee grind size)."
- **Live Streamlit app:** https://ai-barista-plant-wx5vazaq38wgr9etvrwzkt.streamlit.app/
- **Public repo:** https://github.com/smit23ax/ai-barista-plant (main at commit a8b24b6)
- **What it is:** a French press modelled as a small plant. Units are the kettle, the press (batch extraction material balance, cooling energy balance), the plunger filter (the grounds cake is a packed bed, handled with the Ergun equation) and the cup (Stokes settling). It has 8 app views. It includes Buckingham Pi to the packed-bed friction factor and particle Reynolds number, and Ergun built from Kozeny–Carman plus Burke–Plummer. It also has a grind-size explorer, comparison with published data, and a Gaussian-process Bayesian optimizer that picks recipes (benchmarked against its own simulator only, not real brews).
- **Published data:** Corrochano 2015 (Ergun over-predicts measured coffee-bed permeability 1.9–16x), Moroney 2016 (extraction kinetics; fine grind fits, coarse doesn't), Cameron 2020, Uman 2016.
- **Model conventions:** Ergun uses d_s = Φ_s · d₃₂ with Φ_s = 0.75. Plunge force = (Ergun cake Δp + mesh Δp) × press area, so it is fluid resistance only, with no seal friction or buoyancy.
- **Known state:** the default recipe is off-spec (TDS 1.10 %, EY 17.9 %, SCA box 1.15–1.35 % / 18–22 %). Pyodide bundles CoolProp 7.2.0, scikit-learn 1.8.0 and pandas 3.0.2, which are older than the repo pins. The latest stlite is @stlite/browser 1.12.1.
- **How it was made:** entirely with Claude in cloud sessions (Claude Code), through five student-approved plans (v1–v5, 2026-10-13 to 10-29). The student rejected a PINN idea, chose coffee, trimmed scope, re-centred on the professor's framing, required real published data, and set the visual style.

## B. Submission requirements (verbatim)

1. Publicly accessible website demo/documentation. There are many options for you to choose from; a standalone WebAssembly build hosted on GitHub Pages is recommended, e.g., https://chetools.github.io/claude/packed-bed-runaway/
2. YouTube video of presentation - include as a link in the project website. Copy and paste (Practice transcript, and AI critique to the comments section). Include the link of the AI project and this submission requirements in your prompt requesting for a detailed critique.
3. Verbatim YouTube auto-generated transcript of the presentation - viewable section of the project website
4. Presentation/Documentation. Overview. Demo what you/AI created. Make it clear that it is an AI project exploring AI capabilities. Explain the process, i.e., AI models, local/cloud services, prompts, etc., used to create it. Focus on the planning, iteration steps where you provided guidance and your reasoning. Explain key technical details of content related to this course and what you learned and what you want to learn more of in the future. Attribution/references.
5. Projects should compare the outcomes using different AI models. After generating a plan from one model, have a different AI model critique and suggest improvements. Justify your decisions on what to accept/reject. Implement the plan using at least 2 different AI models and compare.
6. Attribution/references, and what each group member contributed. Each member must submit the project separately (max of 20 points for each member on groups of up to 4, max of 50 points for individual submission)
7. In class presentations on the last day of class and on scheduled final exam time/location.

## C. Plan v5

### Site: one GitHub Pages site
The main path is: physical problem → demo → engineering → comparison with experiment → AI process. Supporting records sit in an appendix.

1. **Overview.** The question ("How does grind size control flow through the coffee bed, and where does the classical model become unreliable?"), the main findings with claim labels, a requirements map (Req 1–7 → page anchors), and a final-release checklist.
2. **Demo.** In order: (a) a static grind-size explorer that loads instantly. It is a Plotly figure whose slider selects curves precomputed in Python from the tested model at the app's 10 µm steps, 300–1200 µm, with no JavaScript physics. (b) The full app on Streamlit Cloud. (c) An experimental stlite (Streamlit-in-WebAssembly) build, with a disclosed CDN dependency.
3. **Course content.** Dimensional analysis; Ergun; a sensitivity example (viscous Δp ∝ d⁻², inertial ∝ d⁻¹ at constant ε, u, L and fluid); comparison with Corrochano data and the Moroney fit; a validity table (Re_p, ε, L/D, single-sphere vs distribution, consolidation, where Ergun stops matching); material and energy balances; Stokes. Channeling sits under Extensions as Illustrative. Equations are pre-rendered with the repo's existing offline KaTeX build.
4. **How it was made.** Each iteration is a row: original approach → student intervention → engineering reason → AI change → verification → learning. It records local vs cloud (everything cloud) and the prompt selection rule (every message that changed a plan, with date and model). Original plan files are copied unchanged, and reconstructions are labeled.
5. **Model comparison.** It has two separate sections.
   - **Critiques:** the plan, each critique, and the accept/reject log with reasons. It discloses which model saw which inputs, and records that one pasted "Grok" critique mirrored another model's and was not counted.
   - **Implementations:** see below.
6. **Presentation.** The YouTube video plus the verbatim auto-transcript.
7. **Learnings.** Written by the student; Claude proofreads only.
8. **References and contributions.** Full citations, software versions, and student / model / cited-work contributions, plus submission type and points ceiling.
9. **Records appendix.** Verbatim critiques, old plans, implementation logs, raw model outputs.

**Claim labels:** Compared with experimental data / Model-predicted / Illustrative.

### Implementation comparison (Req 5)
- **Coding task:** a standalone Ergun plunge/grind-sweep module (permeability K, Re_p, f_p, Δp, force), with fixed conventions (d_s = Φ_s·d₃₂, ε, velocity, mesh drop).
- **Explanation task:** "Why can Ergun disagree with measured coffee-bed permeability?" It is scored on whether the answer separates size distribution, shape, porosity, compaction and correlation limits.
- **Implementers:** a fresh Claude Opus session that sees only the frozen prompt; ChatGPT; Muse; Grok. The student runs the non-Claude models.
- **Frozen before any run:** the prompt, start commit a8b24b6, and hidden tests built from the existing repo tests plus reference values at grinds 300, 500, 800, 1000 and 1200 µm, T = 341 K. The planning session fills coverage gaps, never an implementer. Each model gets at most 3 responses including the first, with no extra hints. Every student message is logged, and raw outputs are committed with timestamps.
- **Scoring:**

  | Criterion | Weight |
  |---|---|
  | Physics correctness | 40 % |
  | Frozen tests | 25 % |
  | SI units and symbols | 15 % |
  | Rendering at 1400 and 390 px | 10 % |
  | Clean-checkout reproducibility | 10 % |

  Tolerances are Δp, K and force within ±1 %, and Re_p and f_p within ±0.5 %. A lookup of precomputed answers fails. Lines of code and time are descriptive only.

### Order of work (action — verify)
1. Static explorer — verify: exact match to `plunge()` at every grid point, with an absolute tolerance for near-zero values.
2. stlite spike (half a day, non-blocking) — verify: CoolProp water properties within 0.1 %, TDS/EY/Δp within 0.5 %. Fall back to lite (Packed bed + Theory only) if desktop load > 60 s, a GP suggestion > 30 s, or phone load > 90 s.
3. Freeze the comparison — verify: tests pass on a8b24b6 and are committed first.
4. Implementations — verify: raw outputs committed, scores from the frozen tests.
5. Pages — verify: strict KaTeX, whole-site link check, screenshots at 1400 and 390 px.
6. Preview deploy — verify: fresh Chromium; the student checks Safari, Firefox and a phone.
7. Student tasks — verify: comments are public and the transcript is unedited.
   - Video, 7–8 min, live parts are the Ergun chart and explorer, uploaded at least 48 h before the freeze.
   - Practice transcript and AI critique as numbered YouTube comments; the site is the canonical copy.
   - Auto-transcript pasted unedited. If YouTube doesn't generate one, the site says Req 3 is unmet rather than substituting.
8. Final deploy (`FINAL=1`) — verify: the build fails until every checklist item has evidence; the student submits only that URL.

**Still open:** individual or group, the deadline, the presentation dates, and which commit Streamlit Cloud runs.

## D. What I need from you

1. Any requirement in B still missed or at risk under plan C? Be specific.
2. Any step in C that is wrong, unnecessary, or likely to fail? Say why.
3. Is the implementation comparison fair and convincing? What would you change?
4. Anything a fluid mechanics professor would find missing or weak in the course content?
5. A numbered list of concrete improvements, most important first, one line each with a reason.

Please work from the repo and this document, and say plainly when you could not verify something.
