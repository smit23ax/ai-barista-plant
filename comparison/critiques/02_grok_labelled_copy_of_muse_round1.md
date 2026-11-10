<!-- Archived verbatim from the project chat. Message id cmsg_01GsSXTrvaoYWhp6JXGGNW97UXHsBJX2gaZ9CPx7zG4nmT, time 2026-11-05T15:24:41Z. Pasted by alex; the model is as alex named it. -->

Verdict: The direction is correct and matches the course’s recommended pattern (public site + in-browser demo + documentation that maps cleanly to requirements 1–6). The one-page-per-requirement structure will make grading easy. The three highest-risk failure modes are (1) treating the stlite port as a routine swap, (2) treating Opus vs Sonnet as a genuine “different AI models” comparison, and (3) leaving the video, transcript, evidence trail, and placeholders until the end. Those are the places the submission can fail on the day.
I inspected the live Streamlit app and the public repo (18 commits, progress.txt, requirements.txt, docs/ KaTeX build, plant/, tests/, no site/ folder, no .github/ workflow, no discrete plan files for v1/v2). The observations below are grounded in that material.
1. Requirements — missed, weak, or at risk

* Req 1 (public website demo/documentation): Covered in outline, at risk in execution. No existing GitHub Pages setup, no workflow, and no spike proving the full app runs under stlite/Pyodide. The plan’s “loads in headless Chromium with no Python exceptions” is necessary but insufficient; it does not test phone, fresh browser, campus Wi-Fi, or the GP optimizer actually completing.
* Req 2 (YouTube video + practice transcript + AI critique in comments): Weakly covered. “Add placeholders” is not a plan. There is no script length decision, recording date, live-vs-pre-recorded split, or explicit step to paste the practice transcript and this critique into the YouTube comments as required. The Presenter view timing (“about 6 minutes”) conflicts with the 7–8 minute brief; resolve that before recording.
* Req 3 (verbatim auto-generated transcript as a viewable section): At risk. A placeholder does not guarantee verbatim text. You need a defined process: download the auto-generated transcript after upload, paste it unedited (including errors and timestamps, or state exactly how you handled them), and keep it searchable on the site, not merely a downloadable file. Any cleanup for readability breaks the “verbatim” requirement.
* Req 4 (presentation/documentation: overview, demo, AI process, technical details, learnings, attribution): Mostly covered, with two gaps. Local vs cloud is not sharply distinguished (Claude Code cloud sessions, GitHub, Streamlit Cloud, GitHub Pages; what, if anything, ran locally). Prompt selection is vague—“representative prompts quoted verbatim” will look cherry-picked unless you state the selection rule, dates, and model versions.
* Req 5 (compare outcomes using different AI models; implement with ≥2 different models): Weakly covered and the largest compliance risk. See section 3.
* Req 6 (attribution/references + member contributions): Weak. The plan assumes individual submission “unless told otherwise.” That assumption determines the points ceiling (50 individual vs 20 each in a group of ≤4) and must be stated explicitly on the site. Even for a solo project the contributions page must separate student work, model work, and cited work. References need full citations plus software versions.
* In-class presentations: Not covered. Probably outside website scope, but the plan should at least name them as separate deliverables with dates so a grader does not treat the website as the entire submission.

2. Technical approach (stlite on GitHub Pages)
Good as a goal, risky as an untested commitment. It matches the course recommendation of a standalone WebAssembly build on GitHub Pages and preserves the real app instead of rewriting it in JavaScript. The course example, however, is a lightweight Rust/WASM calculator with a Python reference, not a full stlite app.
Risks (confirmed or highly plausible):

* First-load cost and phone performance. Stlite + Pyodide downloads a large runtime + wheels; guides report multi-tens of MB and “a minute to load,” with code 3–20× slower and poorer mobile behaviour. Your Streamlit Cloud app already shows ~30 s cold start + additional chart time. A blank screen during an in-class demo is a real failure mode.
* Version mismatch is the most likely first failure. Your pins (streamlit 1.66.0, numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, plotly 7.1.0, scikit-learn 1.9.1, CoolProp 8.0.0) are recent. Stlite dictates the Streamlit version; Pyodide package availability and exact versions lag. Treat version/compatibility testing as step 0, not a later verify step.
* CoolProp premise is incorrect. CoolProp has been available in Pyodide (bundled since ~0.24 and with WASM wheels on PyPI from 8.x). Test it first; swapping it for a polynomial/table introduces a new physics error source, forces recalibration, and invalidates the proposed 0.1 % agreement test.
* Most of the scientific stack is plausible (numpy/scipy/pandas/scikit-learn/plotly have Pyodide support or pure-Python paths), but “plausible” is not a test. Unknowns include exact versions, scipy.optimize / solve_ivp, the GP with restarts, st.segmented_control, st.plotly_chart, data files, and overlay PNGs under the browser filesystem. Pint appears only in test/standards code, so guard or strip the import for the browser build.
* Session state does not persist. Lab notebook batches evaporate on reload; the plan does not address seeded examples, export, or the empty first-open state visitors currently see.

Alternatives (ordered by practicality for grading safety):

* A (recommended): Keep Streamlit Cloud as the primary demo link; ship a full or lite stlite build on Pages; add a pure static HTML/JS grind-size explorer (pre-computed Ergun numbers) as instant fallback.
* B: Lite stlite only (Packed-bed / grind explorer + core charts). Fewer dependencies, faster load, still matches the professor’s framing.
* C: Follow the course example more literally (keep full app on Streamlit Cloud; small Rust/JS or Python-WASM Ergun calculator on Pages). Best performance, but a second codebase to keep consistent.
* D: Do not rebuild the KaTeX pipeline from scratch. You already have offline, server-rendered derivations (docs/render_katex.js, scripts/build_guide.py, KaTeX 0.16.x). Reuse that build.

3. Two-model comparison design
Not fair or convincing as written. Three problems:

* Opus 5.5 vs Sonnet 5.5 is same-provider, same-family. Requirement 5 asks for different AI models and implementation with at least two. A professor can reasonably expect cross-provider independence. Make a non-Anthropic model (ChatGPT or Gemini) the primary second implementation; keep Sonnet only as an optional third.
* The scoped task (How-it-was-made page + Ergun-chart widget) is too cosmetic. It tests HTML/CSS and chart styling, not Ergun physics, dimensional analysis, WASM constraints, or the GP optimizer. A model can “win” that task while being wrong on the course content.
* The scoring criteria reward the wrong things. Lines of code, wall-clock time, and “number of corrections” are noisy and depend on prompting style and network. Only “equations correct + every symbol defined with SI units” and “numbers match the tested Python model” are strong; they need explicit tolerances and a frozen test suite.

Improvements: Freeze one prompt, one starting snapshot, one iteration budget, and one pre-registered test suite (existing pytest physics tests + numeric tolerances) before either model starts. Give both models a physics-bearing task (e.g., standalone channeling unit or grind-size explorer that must pass the existing tests). Keep both outputs and diffs in the repo. State the winner in numbers, not impressions. Explicitly note on the comparison page that this critique itself comes from a different model (Grok), so the plan → critique trail is already cross-model.
4. Making the “AI process” page convincing to a fluids professor who likes AI
Evidence, agency, and failure—in that order. A v1→v5 timeline is not evidence if the files are missing. Currently v1/v2 do not exist as discrete files; v3–v5 live only as sections in progress.txt (all dated 2026-10-15). “Every claim links to a plan file or a commit” will produce broken links for a grader who clicks.
Show:

* Exact prompt, date, model version, and the resulting diff for key steps.
* What you rejected and why (PINN as too familiar to the professor, coffee as everyday topic, scope trim, re-centring on packed-bed framing).
* What the AI got wrong with before/after numbers (early Moroney drip-filter misreading, Ergun constants not fitting real coffee beds, Corrochano 1.9–16× over-prediction).
* What you checked yourself (Re_p range, calibration residuals, test output).
* Explicit limits of the model in your own words (where it extrapolated, the 0–8 bar display bound, the remaining TDS gap the AI operator cannot close).

Your existing standards (symbol tables with SI units, automated physics/unit/KaTeX tests) are already strong; surface the test output rather than the claim.
5. Course-content section — missing or to cut
Keep the core; do not let the page become a dump of the Theory view.
Must add:

* One-page validity map: Re_p range, porosity, L/D, grind distribution vs single-sphere assumption, bed consolidation, and where Ergun breaks at fine grind. Put the Corrochano over-prediction (1.9–16×) and the Moroney τ_d/τ_s fit mismatch on the Course content (or Home) page with an explanation; hiding your strongest honest discrepancy invites a grader to find it first.
* Material and energy balances as first-class content (they already exist in the app Trends view).
* Assumptions and bounding box. The live app notes that Carman–Kozeny overestimates and Ergun “blows up” at fine grind and is bounded 0–8 bar for display. Disclose the bound as a display choice and show unbounded values alongside.

Weaken or demote: Channeling (two parallel Darcy paths) currently receives equal weight to validated Ergun content with no named validation data. Label it illustrative/hypothesis or move it to an extensions section.
Cut or demote from graded course-content pages: Presenter mode, quiz mode, and Lab notebook as primary content. They are useful for the talk and demo but are not fluids content. Condense the Theory view’s many sections to dimensional analysis, Ergun derivation, grind-size trade-off, extraction, and Stokes.
Fix before filming: The default recipe is off-spec (TDS 1.25 % vs 1.35 % target, extraction ~19.4 %, Δp ~4.74 bar) and the AI operator warns it cannot set d below 300 µm or close the gap. Either choose an in-spec default for the demo or explicitly frame the off-spec default as the teaching point on the Home page. Do not let the first impression be “Off spec.”
6. Numbered concrete improvements (ordered by importance)

1. Run a 1-day stlite spike first, testing the exact pinned versions, CoolProp, sklearn GP, and st.segmented_control in headless Chromium (and on a phone). Reason: version/compatibility mismatch is the most likely silent failure.
2. Test CoolProp in Pyodide/stlite first and keep it if it works. Reason: the plan’s “not available” premise is contradicted by CoolProp’s own docs; a swap creates new physics error.
3. Make the primary second implementation model non-Anthropic. Reason: Opus vs Sonnet does not convincingly satisfy “different AI models.”
4. Replace the cosmetic two-model task with a physics-bearing task scored by frozen pytest tests and numeric tolerances. Reason: a documentation page cannot test whether a model gets Ergun right.
5. Put the Streamlit Cloud link first on the Demo page and add a lightweight static grind-size explorer as fallback. Reason: a 30–60 s WASM load can fail live in class.
6. Add a Home-page requirements map linking each of reqs 1–6 to its page/anchor. Reason: graders should find compliance in two clicks.
7. Archive plans v1–v5 as discrete files (or commit-hash links) and make every process-page claim resolve. Reason: v1/v2 do not exist today; the current claim is false.
8. Define the video before building more pages: 7–8 min script, live vs pre-recorded, recording date, and explicit YouTube-comments plan. Reason: video + transcript are separate graded requirements, not placeholders.
9. Paste the YouTube auto-generated transcript verbatim and unedited in a searchable section; state how timestamps/errors were handled. Reason: any cleanup breaks the verbatim requirement.
10. Choose an in-spec default recipe for the demo, or explicitly frame the off-spec default as the teaching point. Reason: first impression is currently “Off spec.”
11. Surface the Corrochano 1.9–16× over-prediction and the Moroney τ mismatch on the Course content page with explanation. Reason: hiding the strongest honest discrepancy invites a grader to find it.
12. Disclose the 0–8 bar Δp bound as a display limit and show unbounded values. Reason: clipping a diverging model without disclosure looks like hiding physics.
13. Audit imports (runtime vs test-only) and guard/strip pint in the browser build. Reason: a test-only dependency should not block the demo.
14. Expand the verify list with a performance/compatibility budget (first-load time, GP run time, 1400 px / 390 px screenshots, Chrome/Safari/Firefox, fresh browser). Reason: “loads in headless Chromium” does not prove it works for a grader on a phone.
15. Seed the Lab notebook with example batches + export, or remove it from the first-open path. Reason: visitors currently see an empty state.
16. State individual submission and the 50-point ceiling explicitly; separate student vs model vs cited contributions. Reason: the plan’s assumption decides grading and is currently unstated.
17. Reuse the existing KaTeX build instead of starting a new one. Reason: you already have offline, server-rendered derivations; rebuilding risks regressions.
18. Label channeling as illustrative (no validation data) or move it to extensions. Reason: equal weight to validated Ergun content without evidence is misleading.
19. Add a validity/assumptions table (Re_p, ε, L/D, single-sphere grind, consolidation, breakdown regime). Reason: a fluids professor grades range of validity, not just equations.
20. Make the Home missing-items checklist generated from the repo state and remove it only when video, transcript, critique, and contributions are actually present. Reason: placeholders that remain placeholders are the easiest way to lose points.

Accept or reject each item on the site with a one-line reason (especially 2, 3 and 5, where the current plan is weakest). That transparency itself strengthens the AI-process narrative.