# Final submission website: plan v5 (after Muse's review of v3 and Grok's review of v4)

v5 = v4 plus the decisions below. Both reviews are archived verbatim. Grok's review of v4 is a **fresh, independent input**: it responds to v4's specific content (the static explorer, the claim labels, the explanation task) and does not repeat Muse's withdrawn numbers. It counts as a critique. Grok's earlier pasted text stays recorded as a mirror of Muse round 1.

## A. Decisions

| Source | Point | Decision | Change |
|---|---|---|---|
| Muse 1 | Schedule out of order | **Accept** | New order: spike + explorer → freeze → implementations → comparison and archive pages → preview deploy → final deploy. |
| Muse 2 | Hard decision date for submission type and presentation dates | **Accept** | Needed from alex on day 1, before any page that names them is written. |
| Muse 3 | Spike thresholds | **Accept** | Lite fallback if desktop first load > 60 s, one GP suggestion > 30 s, or phone first load > 90 s. |
| Muse 4 | Hidden-test coverage | **Accept** | At freeze, the existing tests are checked against the explorer sweep (K, Re, f_p, Δp, force at named grinds). Gaps are filled from reference values at a8b24b6 by Claude in this planning session, never by an implementer session. Everything is committed before any model runs. |
| Muse 5 | Their point 4 had no row | **Recorded** | It was their agreement list (accepts 1, 3, 4, 5, 6, 7, 9, 11, 13, 15, 17, 18, 19 and the extras). No change was needed. |
| Muse 6 | YouTube comment order | **Accept** | The site is the canonical copy, and the first comment links it. alex checks the comments are public after posting. |
| Muse 7 | Manual transcript ≠ verbatim | **Accept** | Upload at least 48 h before the freeze, with caption language set to English first. If auto-captions still fail, the site states that Req 3 is unmet and why, with no substitute. |
| Muse 8 | Submit the FINAL URL | **Accept** | Pages serves one site at one URL, and the final build replaces the preview there. alex submits only after the final deploy shows no TODO list on the Overview page. |
| Muse 9 | Learnings authorship | **Accept** | alex writes the bullet notes and full text first. Claude only proofreads (spelling and units) and changes no content. |
| Muse 10 | Tolerances need named reference values | **Accept** | Frozen tests list grinds 300, 500, 800, 1000 and 1200 µm at T = 341 K with the defaults in `plunge()`, plus reference values from a8b24b6. "Hard-coded" means any lookup of precomputed outputs (fails). A formula evaluated at the inputs passes. |
| Muse | Grok provenance | **Accept** | Grok's first text is recorded as a mirror, not counted. Its v4 review is counted. |
| Grok 1 | Explorer matches across the full grind range, same porosity/velocity/mesh | **Accept** | Verified at every exposed grind 300–1200 µm in 10 µm steps (the same as the app slider), from the same `plunge()` call. |
| Grok 2 | Still spike CoolProp under the exact stlite/Pyodide combination | **Accept** | Feasible from Claude's sandbox by serving Pyodide 0.29 locally, because the default CDN is blocked here. |
| Grok 3 | Video owner, length, live vs recorded, post-upload checklist | **Accept** | Owner: alex. Length: 7–8 min. Live parts: the Ergun chart and grind explorer. Pre-recorded: none. Claude writes the post-upload checklist page. |
| Grok 5 | Freeze the follow-up prompt budget and record interventions | **Accept** | 3 responses total per model, with every student message logged. The same rules apply to the explanation task. |
| Grok | Explorer first; stlite decided last | **Accept, with Muse's spike kept** | The static explorer is built first. The stlite spike runs time-boxed (half a day) alongside it, because it only informs and does not block. |

## B. Order of work (each: action — verify: check)

1. Static grind explorer — verify: matches `plunge()` to 1e-9 relative at every grind from 300 to 1200 µm in 10 µm steps.
2. stlite spike — verify: the thresholds above, CoolProp water properties within 0.1 %, TDS/EY/Δp within 0.5 %.
3. Freeze the comparison (coding task + explanation task, tests, prompts, rules) — verify: tests pass on a8b24b6 and are committed before any run.
4. Implementations: fresh Claude Opus session, ChatGPT, Muse, Grok — verify: raw outputs committed with timestamps, scores computed by the frozen tests.
5. Course content, AI process, comparison and references pages — verify: strict KaTeX, link check across the whole site, screenshots at 1400 and 390 px.
6. Preview deploy — verify: fresh Chromium; alex checks Safari, Firefox and a phone.
7. alex: video, comments, transcript, learnings — verify: comments are public; the transcript is unedited.
8. Final deploy (`FINAL=1`) — verify: the build passes with no TODO-ALEX markers; alex submits the URL.

## C. ChatGPT's review of v4 (arrived after v5 was drafted)

| # | Point | Decision | Change |
|---|---|---|---|
| 1 | "Validated" overstates the evidence | **Accept** | The labels become **Compared with experimental data**, **Model-predicted** and **Illustrative**. The Ergun vs Corrochano result is "compared with experimental data", and its disagreement is the finding. |
| 2 | Separate the critique comparison from the implementation comparison, and disclose unequal inputs | **Accept** | The Model comparison page gets two sections. Inputs are disclosed: Muse saw v1 and v2, ChatGPT saw v1 plus Muse's critique and then v4, and Grok's first text mirrored Muse. Every implementer gets the identical frozen prompt and nothing else. |
| 3 | 1e-9 is wrong if the explorer interpolates | **Accept in part** | The explorer does not interpolate. Its slider snaps to the precomputed 10 µm grid, the same as the app slider. So strict agreement at every grid point is the right test, run at the minimum, maximum and every point between. An absolute tolerance is added for near-zero outputs (the inertial share at the coarse end). |
| 4 | Keep the main flow focused | **Accept** | The main path runs physical problem → demo → engineering → experimental comparison → AI process. Full critiques, old plans and logs move to a "Records" appendix linked from the pages. The comparison page shows summaries and measured results. |
| 5 | Final-release checklist | **Accept** | ChatGPT's 10 items become the Overview checklist. The `FINAL=1` build fails while any item lacks its evidence (a link, a file or a marker removed). |

## D. Two meta-reviews of ChatGPT's v4 review (pasted 15:31)

| Point | Decision | Reason |
|---|---|---|
| Check 1e-9 on full-precision arrays, not rounded display values; display check 1e-6 | **Accept** | Arrays are compared at full float64. Displayed hover text is checked separately against rounding (1e-6 relative). |
| Label d_s = Φ_s·d₃₂ as a change if it changes numbers | **Not a change** | `SPHERICITY = 0.75` and d_s = Φ_s·d₃₂ have been in `physics.plunge` since commit 8b25da5 (2026-10-15). v4 only writes the existing convention into the frozen prompt. |
| Interpolation tolerance | **Not needed** | The explorer has no interpolation (the slider snaps to the 10 µm grid). Stated on the site. |
| Release gate as human-enforced checklist | **Keep automated + human** | The build fails on missing evidence. alex also ticks the checklist. |

## E. Final review round on v5 (Muse, plus three other reviews pasted 15:33). All approve; protocol fixes below.

| Point | Decision | Change |
|---|---|---|
| Why T = 341 K | **Accept** | 341 K (68 °C) is the end-of-steep bed temperature for the default recipe: the model gives 340.9 K after 240 s, with the kettle at 93 °C. Stated in the frozen tests. |
| Pyodide version in the spike | **Accept, with a correction** | Checked in the @stlite/browser 1.12.1 package: its CHANGELOG says the runtime was upgraded "from Pyodide 0.29.3 to 314.0.3". The spike therefore serves **Pyodide 314.0.3** locally (the release tarball is downloadable). The exact Pyodide and CoolProp versions are recorded. |
| Explanation-task rubric | **Accept** | Scored out of 10, separately from coding, with no combined score. Correct physics: 4 (names and correctly explains particle size distribution/fines, shape (sphericity), porosity, compaction/consolidation, and correlation constants fitted to sphere beds; 0.8 each). Every symbol defined with SI units: 2. Uses the project's numbers correctly (1.9–16x, direction of the error): 2. States what is known vs hypothesized: 2. |
| Who runs ChatGPT | **Accept** | alex, like Muse and Grok. |
| Primary vs optional implementers | **Accept** | Primary: fresh Claude Opus 5.5 and ChatGPT. Optional: Muse and Grok. The sample size is stated on the page. |
| Fresh sessions for every implementer | **Accept** | Each runs in a new conversation with no plan history, given the frozen prompt only. That includes Muse, whose critique chat can't be reused. |
| Explorer lookup vs "no lookup" rule | **Accept** | The website explorer is a demonstration and may use the precomputed grid (disclosed). The implementation challenge must compute from the equations at runtime. |
| Two freezes | **Accept** | The *comparison freeze* locks prompts, tests and rules before any implementer runs. The *final-submission freeze* comes after the video upload (≥ 48 h before), comments and transcript. |
| atol + rtol per output, with units; intermediate inputs | **Accept** | Explorer vs `plunge()`: rtol 1e-9, with atol of 1e-20 m² for K, 1e-9 Pa for Δp, 1e-12 N for force, and 1e-12 (dimensionless) for Re_p and f_p. Implementers: rtol 1e-2 (Δp, K, force) or 5e-3 (Re_p, f_p), with the atol above. Hidden inputs add 455 and 735 µm and two temperatures. |
| Public vs hidden tests; hidden really hidden | **Accept, plus a fix** | Implementers do **not** get the repo, because it contains `physics.py` and copying it would be trivial. They get a written spec: equations, conventions, inputs, and 2 public worked examples. Hidden tests are kept in the private project folder, and only their SHA-256 hash is committed before the runs. The tests are published after scoring so the hash can be checked. |
| First vs final response | **Accept** | Both are scored and shown (initial accuracy and response to correction). The model identifier, tools and environment are recorded for each. |
| Label consistency | **Accept** | Corrochano, Moroney and Cameron are all "Compared with experimental data". All three labels are defined on the site. The build fails on any leftover "validated" wording. |
| Records one click from Comparison; scores on the page | **Accept** | |
| Release gate checks evidence | **Accept** | The ten items are: public URL opens; explorer verification passes; Streamlit Cloud link works; ≥ 2 implementations documented; decisions published; video embedded; comments posted; verbatim transcript shown; references and contributions complete; presentation dates confirmed. `FINAL=1` checks each by file existence, a non-empty field, or a link that responds. Items 7 and 10 need alex's tick. |
| Video retake fallback | **Accept** | Static explorer screenshots ready before recording. |
| Day-1 alex items | **Accept** | Push approval, Streamlit Cloud commit check and reboot, individual or group, deadline and presentation dates. |
