# AI Barista Plant: master briefing (every suggestion, every want, what to check, what to research)

Compiled 2026-11-05 by Claude Opus 5.5 from the whole planning thread: plans v1–v5 and the critiques from Muse, ChatGPT and Grok. It is written so that any AI model (or person) can read it cold and be useful. Section 10 says what I want from a model that reads it.

---

## 1. My professor's framing (the centre of everything)

> **"Flow through packed bed ⇒ Ergun equation, dimensional analysis. Apply to some interesting topic (coffee grind size)."**

What this means for the project, in priority order:

1. **Packed-bed flow is the subject.** The coffee grounds cake under a French press plunger is the packed bed. Water is forced through it when the plunger goes down.
2. **The Ergun equation is the main model.** It has a viscous (Kozeny–Carman) term and an inertial (Burke–Plummer) term. For a bed of length L (m), porosity ε (-), particle diameter d_s (m), superficial velocity u (m/s), viscosity μ (Pa·s) and density ρ (kg/m³):
   Δp/L = 150 μ (1−ε)² u / (ε³ d_s²) + 1.75 ρ (1−ε) u² / (ε³ d_s)
3. **Dimensional analysis comes first.** Buckingham Pi on (Δp/L, μ, ρ, u, d_s, ε): six variables, three base dimensions, so three groups, one of which is ε itself. Ergun folds ε into the other two:
   - the packed-bed friction factor f_p = (Δp/L) d_s ε³ / (ρ u² (1−ε))
   - the bed Reynolds number Re_b = ρ u d_s / (μ (1−ε))
   Ergun then reads f_p = 150/Re_b + 1.75.
4. **Coffee grind size is the application.** How does grind size change permeability, pressure drop and plunge force, and what does that do to the cup?
5. **Everything else supports this.** That covers the extraction material balance, the cooling energy balance, Stokes settling of fines, channeling and the AI optimizer.

---

## 2. What exists (verified facts, with sources)

- **Live app** (Streamlit Cloud): https://ai-barista-plant-wx5vazaq38wgr9etvrwzkt.streamlit.app/
- **Public repo:** https://github.com/smit23ax/ai-barista-plant (main at commit a8b24b6)
- **8 app views:** Plant, Theory, Trends, Packed bed, Lab notebook, AI operator, Presenter, Engineering notes (`app.py` line 131).
- **Physics** (`plant/physics.py`):
  - Ergun with d_s = Φ_s·d₃₂, sphericity Φ_s = 0.75 [Corrochano 2015], in the code since commit 8b25da5.
  - d₃₂ is the Sauter mean diameter of a two-part mix: the nominal grind plus a fines fraction w_f = 0.15 at 30 µm (one coffee cell).
  - Bed porosity is ε = 0.40 (assumed). The cake length comes from dose ÷ (bulk density 400 kg/m³ × area).
  - The mesh resistance R_mesh = 2×10⁸ 1/m (assumed) acts in series.
- **Plunge force** = (Δp_cake + Δp_mesh) × press area. This is **fluid resistance only**, with no seal friction, buoyancy or acceleration.
- **Standard plunge** (800 µm, 341 K, 20 s): Re_b ≈ 0.98, inertial share ≈ 1.1 %, Δp ≈ 480 Pa (310 Pa cake + 169 Pa mesh), force ≈ 2.7 N.
- **The temperature 341 K** (68 °C) is the end-of-steep bed temperature for the default recipe. The model gives 340.9 K after 240 s with the kettle at 93 °C.
- **Grind sweep at 341 K** (computed 2026-11-05):

  | grind (µm) | K (m²) | Δp total (Pa) | Δp cake (Pa) | F (N) | Re_b (-) | inertial share |
  |---|---|---|---|---|---|---|
  | 300 | 1.09e-11 | 686 | 517 | 3.89 | 0.76 | 0.9 % |
  | 500 | 1.49e-11 | 547 | 379 | 3.11 | 0.89 | 1.0 % |
  | 800 | 1.81e-11 | 479 | 310 | 2.72 | 0.98 | 1.1 % |
  | 1200 | 2.05e-11 | 444 | 275 | 2.52 | 1.05 | 1.2 % |

  **Notice:** a 4x change in nominal grind changes K by less than 2x. That is because the 15 % fines dominate the Sauter diameter. **This is a real finding worth explaining**, and it also depends on an assumed fines model (see research questions).
- **Comparison with experimental data:**
  - Corrochano 2015 (measured coffee-bed permeability): Ergun **over-predicts** permeability by 1.9–16x. The equivalent constant C_eff is 280–2400 instead of 150, and the gap grows with grind size.
  - Moroney 2016 (extraction kinetics, well-mixed immersion): the fine grind fits (τ_d 41 s vs 42.2 s), the coarse grind doesn't (647 s vs 270 s).
  - Cameron 2020 (espresso): EY peaks at grinder setting 1.7.
  - Uman 2016: grind distributions (fines cutoff about 70–76 µm).
- **Default recipe is off-spec:** TDS 1.10 %, EY 17.9 % (SCA box 1.15–1.35 % / 18–22 %).
- **AI optimizer:** a Gaussian process with Bayesian optimization (scikit-learn). It is benchmarked **only against the project's own simulator**, not real brews.
- **Tests:** pytest covering physics, units (pint), symbol definitions and KaTeX rendering. Docs are server-rendered KaTeX (offline).
- **Browser runtime facts** (checked 2026-11-05):
  - @stlite/browser 1.12.1 runs **Pyodide 314.0.3** (Python 3.14), per its CHANGELOG.
  - Pyodide builds CoolProp 7.2.0, scikit-learn 1.8.0 and pandas 3.0.2. These are older than the repo pins (CoolProp 8.0.0, scikit-learn 1.9.1, pandas 3.0.5).
  - PyPI's latest CoolProp is 8.0.0, with no emscripten wheel.
- **How it was built:** entirely with Claude in cloud sessions, through plans v1–v5 (2026-10-13 to 10-29).

## 3. Course submission requirements (verbatim)

1. Publicly accessible website demo/documentation. There are many options for you to choose from; a standalone WebAssembly build hosted on GitHub Pages is recommended, e.g., https://chetools.github.io/claude/packed-bed-runaway/
2. YouTube video of presentation - include as a link in the project website. Copy and paste (Practice transcript, and AI critique to the comments section). Include the link of the AI project and this submission requirements in your prompt requesting for a detailed critique.
3. Verbatim YouTube auto-generated transcript of the presentation - viewable section of the project website
4. Presentation/Documentation. Overview. Demo what you/AI created. Make it clear that it is an AI project exploring AI capabilities. Explain the process, i.e., AI models, local/cloud services, prompts, etc., used to create it. Focus on the planning, iteration steps where you provided guidance and your reasoning. Explain key technical details of content related to this course and what you learned and what you want to learn more of in the future. Attribution/references.
5. Projects should compare the outcomes using different AI models. After generating a plan from one model, have a different AI model critique and suggest improvements. Justify your decisions on what to accept/reject. Implement the plan using at least 2 different AI models and compare.
6. Attribution/references, and what each group member contributed. Each member must submit the project separately (max of 20 points for each member on groups of up to 4, max of 50 points for individual submission)
7. In class presentations on the last day of class and on scheduled final exam time/location.

## 4. What I (alex) want

- **Impress my professor**, who teaches fluid mechanics and loves AI, with an original, fully explainable AI + fluids project. It should be the best version I can get.
- **The right size**: a good project, not too complicated and not too simple. Classmates did single-topic calculators (pancake batter viscosity, pipe sizing, pipe networks, fluidized beds).
- **I must be able to defend every part.** That means every equation is written out, said in plain words, every term defined with SI units, limits checked, and likely questions prepared (my professor's explanation style).
- **Real published data**, never made-up numbers. Honest about where the model fails.
- **The visual style I like:** faint grid background, bold serif titles, blue monospace kickers, pill tabs, white rounded cards, equation boxes.
- **What I already decided against:** a PINN project (too familiar to my professor) and real brewing for the main project (I can't brew in person; an optional bench procedure exists).
- **Clear credit**: what I decided vs what the AI built vs cited work.

## 5. The critique trail (who said what)

| Round | Model | Reviewed | Independent? | Main contribution |
|---|---|---|---|---|
| Plan v1 | Claude Opus 5.5 | — | — | stlite on Pages, 8 pages, Opus vs Sonnet comparison |
| 1 | Muse | v1 | Yes | 20 points: CoolProp does run in Pyodide; spike first; non-Anthropic implementer; physics-bearing frozen test; Streamlit Cloud first + static fallback; archive plans; video/transcript process |
| 1 | Claude fact-check | Muse r1 | — | Confirmed CoolProp, version lag, 8 views, off-spec default. Could **not** find Muse's "0–8 bar bound", 4.74 bar or TDS 1.25 % in code. Rejected #12. |
| 2 | Muse | v2 | Yes | Withdrew its unverified browser-report numbers; asked for spike thresholds, schedule order, test coverage, dates, verbatim-transcript honesty |
| — | "Grok" (first paste) | v1 | **No.** Near-verbatim copy of Muse r1, including the withdrawn numbers | Recorded as a finding, not counted |
| — | Unnamed model | v1 | **No.** Reworded Muse r1 | Recorded, not counted |
| 2 | ChatGPT | v1 + Muse r1 | Yes (says what it couldn't verify) | Demo order (static explorer → Streamlit Cloud → stlite experimental); claim labels; sensitivity example d⁻²/d⁻¹; plunge-force definition; explanation task; iteration table |
| 3 | Grok | v4 | Yes | Explorer full-range check; spike CoolProp under the exact runtime; video owner and length; freeze follow-up budget |
| 3 | ChatGPT | v4 | Yes | "Validated" → "Compared with experimental data"; separate critique vs implementation comparisons; 10-item release checklist; focused main path |
| 4 | Muse + three other reviews | v5 | Mixed | All approve. Protocol fixes: T = 341 K justification, Pyodide version, explanation rubric, fresh sessions, public vs hidden tests, two freezes, atol + rtol with units, first vs final response |

**What I learned about the critics:** models that were shown another model's critique mostly echoed it, including its unverified claims. The models that worked from the plan alone, and said what they couldn't verify, gave new and checkable points.

## 6. Every suggestion, grouped, with its status

### 6.1 Demo and hosting (Req 1)

| Suggestion | Source | Status |
|---|---|---|
| Static grind explorer first (instant, no Python in the browser; the slider only selects precomputed values) | ChatGPT, Muse, Grok | **Accepted.** Being built. |
| Streamlit Cloud as the full working demo | Muse, ChatGPT | **Accepted** |
| stlite (Streamlit in WebAssembly) as an experimental extra, time-boxed spike | everyone | **Accepted.** Fall back to lite if desktop load > 60 s, a GP suggestion > 30 s, or phone load > 90 s. |
| Keep CoolProp rather than replacing it; test it in the real runtime | Muse, ChatGPT | **Accepted.** Test under Pyodide 314.0.3; water ρ, μ, c_p within 0.1 %. |
| Strip pint (test-only) from the browser build | Muse | **Accepted** |
| Seed the Lab notebook with example batches | Muse | **Accepted** |
| Browser persistence (IndexedDB) | ChatGPT | **Rejected.** Risk with little gain. |
| Rust/WASM calculator like the course example | Muse (alternative C) | **Not chosen.** It would be a second codebase. |
| Explorer verification: exact match at every grid point (rtol 1e-9 plus a per-output atol with units); separate rounding check on displayed text | Grok, ChatGPT, meta-reviews | **Accepted** |
| Test in Chromium (Claude), Safari, Firefox and a phone (alex) | Muse, ChatGPT | **Accepted** |

### 6.2 Video, comments and transcript (Req 2, 3)

| Suggestion | Source | Status |
|---|---|---|
| Video owner alex, 7–8 min, live parts = Ergun chart + explorer | Grok, Muse | **Accepted** |
| Upload ≥ 48 h before the final-submission freeze; set caption language to English first | Muse, ChatGPT | **Accepted** |
| Practice transcript + AI critique as numbered YouTube comments; the site is the canonical copy | Muse | **Accepted** |
| Paste the auto-transcript **unedited**. If YouTube makes none, say Req 3 is unmet; no substitute | Muse | **Accepted** |
| Explorer screenshots ready as a retake fallback | Muse | **Accepted** |

### 6.3 Documentation and AI process (Req 4)

| Suggestion | Source | Status |
|---|---|---|
| Iteration table: original approach → my intervention → engineering reason → AI change → verification → learning | ChatGPT | **Accepted** |
| Copy original plans v1–v5 unchanged; label reconstructions | Muse, ChatGPT | **Accepted.** The originals exist. |
| Local vs cloud stated (everything cloud) | Muse | **Accepted** |
| Prompt selection rule: every message that changed a plan, with date and model | Muse | **Accepted** |
| Show real mistakes with numbers (the Moroney drip-filter misreading, Ergun vs coffee data, CoolProp premise, critics' withdrawn numbers) | Muse, ChatGPT | **Accepted** |
| Learnings written by me; Claude proofreads only | Muse | **Accepted** |
| Main path: physical problem → demo → engineering → experimental comparison → AI process; records in an appendix one click away | ChatGPT | **Accepted** |

### 6.4 Course content (fluid mechanics)

| Suggestion | Source | Status |
|---|---|---|
| Lead with dimensional analysis → Ergun → grind size | Professor | **Core** |
| Sensitivity example: viscous Δp ∝ d⁻², inertial ∝ d⁻¹ at constant ε, u, L and fluid | ChatGPT | **Accepted** |
| Validity table: Re_b range, ε, L/D, single sphere vs distribution, consolidation, where Ergun stops matching | Muse, ChatGPT | **Accepted** |
| Corrochano 1.9–16x over-prediction shown prominently, with possible causes separated into supported vs hypothesized | everyone | **Accepted** |
| Claim labels: Compared with experimental data / Model-predicted / Illustrative | ChatGPT | **Accepted** |
| Channeling moved to Extensions as Illustrative | Muse, ChatGPT | **Accepted** |
| Material and energy balances visible as supporting content | Muse, ChatGPT | **Accepted** |
| Condense the Theory view; Presenter, quiz and Lab notebook stay in the demo only | Muse | **Accepted** |
| Plunge force defined as fluid resistance only | ChatGPT | **Accepted** (checked in code) |
| Off-spec default: binary test (does the AI operator reach the SCA box from it?), recorded either way | Muse | **Accepted** |

### 6.5 Model comparison (Req 5)

| Suggestion | Source | Status |
|---|---|---|
| Two separate sections: critique comparison vs implementation comparison; disclose who saw what | ChatGPT | **Accepted** |
| Primary implementers: fresh Claude Opus 5.5 session + ChatGPT. Muse and Grok optional | meta-review | **Accepted** |
| Every implementer in a **new session**, with the frozen prompt only | Muse | **Accepted** |
| Implementers do **not** get the repo (it contains the answer); they get a written spec + 2 public worked examples | meta-review + Claude | **Accepted** |
| Hidden tests kept private; SHA-256 hash committed before the runs; published after scoring | Claude | **Accepted** |
| Hidden inputs: 300, 455, 500, 735, 800, 1000, 1200 µm at 341 K and two other temperatures | ChatGPT | **Accepted** |
| Tolerances: Δp, K, F ±1 %; Re_b, f_p ±0.5 %; per-output atol with units | Muse, meta-review | **Accepted** |
| At most 3 responses per model; score both the first and the final response | Muse, ChatGPT | **Accepted** |
| Scoring weights: physics 40 %, frozen tests 25 %, SI units and symbols 15 %, rendering 10 %, reproducibility 10 % | Muse | **Accepted** |
| Lines of code and time are descriptive only | Muse | **Accepted** |
| Explanation task ("why can Ergun disagree with measured coffee-bed permeability?"), scored /10 separately | ChatGPT | **Accepted** |
| Cross-provider described as a methodological choice, not a literal rule | ChatGPT | **Accepted** |

### 6.6 Attribution, deliverables and release (Req 6, 7)

| Suggestion | Source | Status |
|---|---|---|
| State individual vs group and the points ceiling on the site | everyone | **Waiting on alex** |
| Full citations + software versions; contributions split into me / each model / cited work | Muse, ChatGPT | **Accepted** |
| In-class presentations listed as separate deliverables with dates | everyone | **Waiting on alex** for dates |
| 10-item final checklist; `FINAL=1` build fails until each item has evidence | ChatGPT, Muse | **Accepted** |
| Two freezes: comparison freeze (before any run) and final-submission freeze (after video and captions) | ChatGPT | **Accepted** |
| Check which commit Streamlit Cloud runs, and reboot it on main | Muse | **Waiting on alex** |

## 7. What a reviewer should look for (checklist)

**Physics:**
1. Is every symbol defined with SI units before use?
2. Is the Ergun form consistent (which diameter, which porosity, superficial vs interstitial velocity)?
3. Do the Pi groups come out dimensionless?
4. Do the limits work? Low Re_b should give Kozeny–Carman / Darcy, and high Re_b should give Burke–Plummer.
5. Is Re_b inside the range where Ergun was fitted? Coffee sits around 0.8–1.1, so the regime is viscous and the inertial share is about 1 %.
6. Is the fines treatment defensible? It dominates K (see the table in section 2).
7. Is a constant porosity ε = 0.40 reasonable, when Corrochano reports wet coffee beds at 0.12–0.33?
8. Is the mesh resistance (assumed) a large part of Δp? Yes, about 35 % at 800 µm, so it matters.

**Honesty:**
- Is anything labeled "validated" that is only compared?
- Is any assumed value presented as measured?
- Is the GP benchmark described as simulator-only?

**Requirements:** can a grader find each of Req 1–7 in two clicks?

**Fair comparison:** did every implementer get identical inputs, and could any have seen the answer?

**Reproducibility:** pinned versions, seeds, clean-checkout run.

## 8. Research questions (where more research would help)

Please answer from primary sources, cite them, and say plainly when you can't verify something.

1. **Ergun constants for coffee.** What values of the viscous constant (150 in Ergun, 180 in Carman–Kozeny) do published coffee-bed studies report, and why? Corrochano 2015 implies 280–2400. Are there other measurements for French-press-like (coarse, low-pressure) beds rather than espresso?
2. **Fines and the Sauter diameter.** Is using d₃₂ of a bimodal distribution, with fines as single 30 µm cells, a good effective diameter for permeability? What do Uman 2016 and others say about the fines fraction (by mass) for French press grinds?
3. **Wet-bed porosity and swelling.** Coffee particles swell and the bed consolidates when wet. What porosity should a French-press cake have? Do any measurements apply at low pressure?
4. **Fines migration and filter cake formation.** During the plunge, fines may move toward the mesh and form a skin. Is there literature quantifying this, and would it explain Ergun's error growing with grind size?
5. **Plunge force measurements.** Has anyone measured French press plunge force vs grind size? Any number would be a direct comparison with experimental data.
6. **Dimensional analysis variants.** Some textbooks put (1−ε) differently in Re_b and f_p. Which convention matches Ergun 1952 and our code, and how should the difference be explained?
7. **Channeling.** Is there quantitative evidence of preferential flow in immersion/press beds, not only espresso (Cameron 2020)?
8. **Web runtime.** Does CoolProp 7.2.0 in Pyodide 314 give the same IAPWS-95 water properties as CoolProp 8.0.0? Is there any known stlite 1.12 issue with `st.segmented_control` or Plotly?
9. **YouTube.** What is the current comment length limit, and how long do auto-generated captions usually take to appear for a 7–8 min English video?
10. **Teaching angle.** What would a fluid mechanics professor expect students to conclude about the limits of empirical correlations like Ergun, and how do standard textbooks phrase them?

## 9. Still open (my to-dos)

- Approve the push to the repo and the GitHub Pages preview.
- Individual or group? (This sets the points ceiling.)
- Deadline and presentation dates.
- Which commit Streamlit Cloud is running (then reboot on main).
- Video, YouTube comments and transcript; my Learnings text.
- Run ChatGPT (and optionally Muse and Grok) on the frozen implementation prompt once it's ready.

## 10. What I want from you (any AI reading this)

1. Check the physics in sections 1–2 and 7. Is anything wrong, inconsistent, or missing for a fluid mechanics grader?
2. Answer whichever research questions in section 8 you can, **with citations**. Mark what you could not verify.
3. Tell me if any accepted suggestion in section 6 is a mistake, or if a rejected one should come back.
4. Suggest up to 5 improvements that would most impress a professor who framed the project as "packed bed ⇒ Ergun ⇒ dimensional analysis ⇒ coffee grind size". One line each, with a reason.
5. Don't repeat points already in section 6 unless you disagree with them.
