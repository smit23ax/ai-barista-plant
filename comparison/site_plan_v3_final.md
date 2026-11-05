# Final submission website: plan v3 (after Muse's second review)

**Trail so far.** Plan v1 was written by Claude Opus 5.5. Muse critiqued it with 20 points. Claude fact-checked the critique and wrote accept/reject decisions plus plan v2. Muse reviewed that in 25 points and withdrew its unverified numbers. This file records Claude's response to Muse's second review and the plan to build.

---

## A. Response to Muse's second review

| Muse # | Point | Decision | Reason / action |
|---|---|---|---|
| 1–3 | Withdraws the browser-report numbers and the CoolProp 8.1 claim | **Noted** | Recorded on the comparison page as an example of a model correcting itself when shown evidence. |
| 5 | Keep #12 open as a live-site vs repo discrepancy | **Accept** | Evidence so far from the git history: "0–8 bar" and "unrealistic" never appear in any commit. "About 6 minutes" existed in early commits and was removed on 2026-10-15 (commit cb2fd66). So the browser report is either a stale deploy or a mis-read. The live app can't be reached from Claude's sandbox. **alex:** open the Streamlit Cloud app's settings and check which commit it runs, then reboot it on main. The result goes on the comparison page. |
| 6 | Make #10 a binary test | **Accept** | The test: run the AI operator from the default recipe, seed 0, 10 batches. If any batch lands in the SCA box, the off-spec default stays as the teaching point. If none does, the default changes to the model's in-spec recipe. The run is recorded on the site either way. This is in step 5. |
| 7, 15 | Submission type and presentation dates unresolved | **Accept** | These are blockers on alex. The site prints nothing about them until they are given. |
| 8 | Beyond water properties within 0.1 %, rerun calibration and GP | **Accept** | In the browser, the full model reruns: headline TDS, EY and Δp must agree with the server values within 0.5 %. The calibration fit and one GP suggestion must finish without error. |
| 9 | Build fails on a remaining TODO-ALEX marker | **Accept, modified** | There are two modes. The preview build deploys and lists the markers, so you can see the site before the video exists. The final build (`FINAL=1`) fails on any marker and is the one submitted. |
| 10 | Add a Firefox check | **Accept, alex's task** | Only Chromium is installed in Claude's sandbox. alex opens the site in Firefox. |
| 11 | Dates, owners, freeze date | **Accept** | See the schedule in C. The dates are relative until alex gives the class dates. |
| 12 | YouTube comment length limit | **Accept** | YouTube comments are capped at about 10,000 characters. The practice transcript and the critique are split into numbered comments ("1/4, 2/4 …"), and the first comment links the full text on the site. |
| 13 | Auto-transcript availability | **Accept** | YouTube's auto-captions usually appear minutes to hours after upload (English, auto-detected). If they don't appear within 24 h, the site says so, and a manual transcript is labeled as not verbatim. Errors in a verbatim one are kept, with a note. |
| 14 | Content plan for Learnings and References | **Accept** | Learnings has three parts: fluid mechanics (Ergun regimes, why Ergun over-predicts coffee permeability, dimensional analysis), working with AI (fact-check before accepting, caught errors on both sides), and what I want to learn next. **alex writes the first person text, and Claude drafts prompts for it.** References give full citations for 4 papers plus Ergun 1952, the SCA chart, and every software package with its exact version from requirements and the lockfile. |
| 16 | Commit the raw Muse output | **Accept** | Muse's and any other model's outputs are committed exactly as pasted, under `comparison/raw/`, with the date and time. This applies to these critiques too. |
| 17 | Define the lite fallback | **Accept** | Lite stlite means Packed bed and Theory views only, with no GP optimizer, no calibration, no Lab notebook and no AI operator. |
| 18 | Static fallback is selection only | **Accept** | The slider only switches between curves precomputed in Python. There is no JavaScript physics. |
| 19 | Link check across the whole site and Pages config | **Accept** | It covers every page, `.nojekyll`, the base path, and the video and transcript links. |
| 20–21 | Fairness rules | **Accept, plus one fix** | Claude is both an implementer and the plan author, so the hidden tests must not come from an implementer. The frozen tests are built only from existing committed tests (`tests/test_packed_bed.py`, `tests/test_physics.py`) and reference values from the model at commit a8b24b6, which predates this comparison. The Claude implementation runs as a **fresh Claude session** that sees only the frozen prompt and the starting commit, not this conversation. Each model gets 3 responses total including the first, with no extra hints. |
| 22–24 | Rubric and tolerances | **Accept** | Weights: physics correctness 40 %, frozen pytest pass 25 %, SI units and symbol definitions 15 %, rendering at 1400 and 390 px 10 %, clean-checkout reproducibility 10 %. Tolerances: Δp, K and force ±1 %; Re_p and f_p ±0.5 %. Hard-coded answers fail. Lines of code and time are descriptive only. |

## B. Implementers

1. **Claude Opus 5.5**: a fresh session given only the frozen prompt.
2. **Muse**: run by alex, raw output committed.
3. **Grok** (optional third): run by alex, raw output committed.

## C. Steps (action — verify: check), owner, when

| Step | Owner | When |
|---|---|---|
| 0. stlite spike (8 views, CoolProp 7.2.0, pint stripped, full model rerun) — verify: no exceptions; TDS, EY and Δp within 0.5 %; water properties within 0.1 %; calibration and one GP suggestion finish; first-load time recorded. Lite fallback if it fails. | Claude | Day 1 |
| 1. Freeze the comparison task: prompt file, start commit, hidden tests from existing tests — verify: tests pass on the reference and are committed before any run. | Claude | Day 1 |
| 2. Implementations — verify: raw outputs committed, scores from the frozen tests. | Claude (Opus run); alex (Muse, Grok) | Days 1–3 |
| 3. Site pages, reusing the existing KaTeX build — verify: strict KaTeX, screenshots at 1400 and 390 px, no overlaps. | Claude | Days 1–2 |
| 4. Process archive (plans v1–v5, assumptions, scripts, both critiques and these responses) — verify: whole-site link check passes. | Claude | Day 2 |
| 5. Demo fixes: seeded example batches; off-spec binary test — verify: AppTest; AI run recorded. | Claude | Day 2 |
| 6. Pages deploy (preview mode) — verify: public URL in fresh Chromium; alex checks Safari, Firefox and a phone. | Claude; alex checks | Day 2 |
| 7. Video recorded and uploaded; comments posted (split); auto-transcript pasted. | alex | Freeze date minus 3 days |
| 8. Learnings first-person text, submission type, presentation dates. | alex | Freeze date minus 3 days |
| 9. Final build (`FINAL=1`, no TODO-ALEX left) — verify: build passes and the link check passes. | Claude | Freeze date minus 1 day |

**Freeze date:** the submission deadline minus 1 day (alex to give the deadline).

**Smallest success check:** step 0 passes and the preview site is live on GitHub Pages with the Demo page working.
