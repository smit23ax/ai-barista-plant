<!-- Archived verbatim from the project chat. Message id cmsg_01GsSXTrvaoYWhp6JXGGNW974MimSHY9AbAcodZggqrKNp, time 2026-11-05T15:20:06Z. Pasted by alex; the model is as alex named it. -->

1. Correction on my numbers: the TDS 1.25%, EY 19.4% and Δp 4.74 bar came from the delegated browser inspection of the Plant view at default load on 10:08–10:10, not from code I read myself, so Claude's code check (TDS 1.10%, EY 17.9%, Δp 480 Pa) outranks them and I withdraw mine.
2. Same source, same withdrawal: the “bounded 0–8 bar”, AI-operator “cannot set d below 300 µm”, Presenter “about 6 minutes”, and Trends 22.5 kJ / 8.4 kJ / 63% figures were all in that browser report, I did not verify them in code, and they should be treated as unverified until the deployed commit is reconciled with the repo.
3. CoolProp 8.1 wheels: my claim came from a CoolProp docs snippet, not a PyPI check, so I accept Claude's PyPI check (latest 8.0.0, no emscripten wheel) and the Pyodide-bundled 7.2.0 as the version to test.
4. I agree with accepts 1, 3, 4, 5, 6, 7, 9, 11, 13, 15, 17, 18 and 19, and with the extra accepts on local-vs-cloud, prompt-selection rule, descriptive-only LOC/time, and condensed course content.
5. I agree with rejecting 12 as a plan item, but not with closing it: keep it open as a live-site vs repo-commit discrepancy to reconcile, because a browser agent reporting text that is absent from code needs an explanation, not just a dismissal.
6. I partly disagree with 10 as written: “teaching point if the AI reaches the box, otherwise change the default” is a conditional, not a decision, so make it a binary test with a date and record the AI run either way.
7. I disagree that 16 is resolved: “alex confirms individual or group” is still a to-do, so the site cannot yet state the submission type or points ceiling.
8. I agree with 2, but water ρ/μ/cp within 0.1% alone is insufficient: also rerun the calibration and GP regression and require the headline TDS/EY/Δp to move by less than the stated test tolerance.
9. I agree with 20, but strengthen it: make the build fail if any TODO-ALEX marker remains, rather than just listing it.
10. I agree with 14 as split, but add one Firefox check: Chromium + Safari + phone does not cover the browser where stlite historically had issues.
11. Plan v2 still missing: no dates, owners, or freeze date for any step, so the video, transcript and Pages switch-on can all slip to the last day.
12. Plan v2 still at risk: YouTube comments have a character limit, so pasting a full practice transcript plus this critique verbatim may need splitting or linking, and v2 does not address that.
13. Plan v2 still at risk: the verbatim auto-transcript depends on YouTube generating it after upload, with no stated delay, language, or fallback if it is unavailable or largely wrong.
14. Plan v2 still at risk: Learnings and References have pages named but no content plan, so “what I learned / want to learn next” and full citations with software versions could end up as afterthoughts.
15. Plan v2 still at risk: in-class presentation dates remain an Alex to-do with no date in the plan, and the Home page cannot name them until that is supplied.
16. Plan v2 still at risk: Muse is run by you manually pasting the result back, so v2 must require the raw, unedited output file to be committed, with timestamps, to avoid transcription or formatting loss.
17. Plan v2 still at risk: the lite-stlite fallback in step 0 is undefined — state now whether it is Packed-bed view only, whether it includes the GP, and what is cut.
18. Plan v2 still at risk: the static fallback is described as a Plotly figure “with a grind slider” and “no new JavaScript physics”, so clarify the slider only selects precomputed curves.
19. Plan v2 still at risk: the link check in step 4 covers only the process archive, so extend it to the whole site plus Pages config (.nojekyll, base path, video/transcript links).
20. Two-model fairness: yes, steps 1–2 are fair in structure, provided the hidden tests are written by you or from existing tests, not by either implementer, and are frozen and committed before either model starts.
21. Fairness rules: same frozen prompt file, same starting commit, 3 rounds defined as 3 model responses including the first, no extra hints to either model, and both raw outputs committed under comparison/ with timestamps.
22. Scoring rubric, weights: physics correctness 40%, frozen pytest pass 25%, SI units and symbol definitions 15%, rendering on 1400 px and 390 px 10%, clean-checkout reproducibility 10%.
23. Scoring tolerances: Δp, permeability K and plunge force within ±1% of the reference model, Re_p and f_p within ±0.5%, all outputs in SI with every symbol defined, and zero hard-coded answers for the swept grind sizes.
24. Scoring penalties: fail the physics criterion if any frozen test fails or is skipped, fail reproducibility if it does not run from a clean checkout, and treat lines of code and time taken as descriptive only, not scored.
25. Overall: v2 is shippable if the step-0 spike passes, but the top remaining risks are the spike itself, the unconfirmed submission type, and the YouTube transcript/comments handling.