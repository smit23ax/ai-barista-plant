<!-- Archived verbatim from the project chat. Message id cmsg_01GsSXTrvaoYWhp6JXGGNW97Mu3NcYyR16kusAK8UyzwWx, time 2026-11-05T15:27:05Z. Pasted by alex; the model is as alex named it. -->

Independent critique of the plan (C) against requirements (B), grounded in the live app and public repo.
I examined the GitHub repo (https://github.com/smit23ax/ai-barista-plant), the pinned requirements.txt, progress.txt, the existing KaTeX build under docs/, and the Streamlit Cloud deployment. The plan is directionally sound—one public GitHub Pages site that tries to satisfy most of requirements 1–6 in a single place is the right shape—but several execution assumptions are fragile and the compliance story for the hardest requirements is thin.
1. Requirements missed, weakly covered, or at risk
Req 1 (public website demo + documentation)

Covered in structure, high risk in delivery. The plan correctly points at GitHub Pages + an in-browser demo, matching the course’s preferred pattern. However the repo today has no site/ directory, no GitHub Actions workflow, and no evidence that the full Streamlit app has ever been exercised under stlite/Pyodide. The verification step (“loads in headless Chromium with no Python exceptions”) is incomplete; it does not speak to cold-start time on a phone, campus Wi-Fi, or whether the Gaussian-process optimizer actually finishes.
Req 2 (YouTube video of the presentation + practice transcript + AI critique in the comments)

Weak. The plan only says “add placeholders.” There is no decision on script length, what will be shown live versus pre-recorded, when the recording will happen, or an explicit step to paste the practice transcript and this critique into the YouTube comments. The Presenter view timing also appears shorter than the 7–8 minute target implied by the project brief.
Req 3 (verbatim auto-generated YouTube transcript as a viewable section of the site)

At risk. A placeholder is not a process. You need a concrete pipeline: upload → download the auto-generated transcript → paste it unedited (including timestamps and recognition errors, or state exactly how you treated them) into a searchable page. Any silent clean-up breaks the “verbatim” requirement.
Req 4 (overview, demo of what you/AI created, clear AI-project framing, process description, technical content from the course, learnings, attribution)

Mostly addressed by the proposed page list, but two gaps stand out. The distinction between local and cloud work is fuzzy (Claude Code sessions, Streamlit Cloud, GitHub Pages). The selection rule for “representative prompts” is missing; without dates, model versions, and a stated sampling method the quotes will look curated.
Req 5 (compare outcomes of different AI models; implement the plan with at least two different models)

The weakest point. The plan proposes Opus 5.5 versus Sonnet 5.5 (same provider, same family) for a narrow documentation-plus-widget task. That is unlikely to satisfy a grader looking for genuine model diversity. The comparison criteria (lines of code, time taken, number of corrections) are also noisy and easy to game.
Req 6 (attribution/references + member contributions)

Under-specified. The plan assumes an individual submission. That assumption must be stated on the site because it changes the points ceiling. Even for a solo project the contributions section must cleanly separate student decisions, model-generated artefacts, and third-party literature/software. Software versions are required, not just package names.
In-class presentation slots are outside the website but should be named as separate deliverables so the site is not read as the complete submission.
2. Technical approach: stlite on GitHub Pages
Viable in principle, risky as currently scoped. It keeps the existing Python physics and UI instead of a full rewrite, and it matches the spirit of the course example. The course example itself, however, is a lightweight WebAssembly calculator, not a full scientific Streamlit stack.
Main risks:

* Cold-start size and latency. Pyodide + wheels is a multi-tens-of-MB download; first open is often 30–60+ seconds and slower still on phones. Your current Streamlit Cloud app already shows a noticeable cold start. An empty browser tab while you talk is a live-demo failure mode.
* Version pinning. Your requirements.txt uses very recent packages (streamlit 1.66, numpy 2.5, scipy 1.18, pandas 3.0, scikit-learn 1.9, CoolProp 8.0). Stlite locks the Streamlit version; Pyodide package availability and exact wheels lag. This must be validated before any further design work.
* CoolProp. The plan assumes it is unavailable in the browser and must be replaced. CoolProp has had Pyodide support for some time (bundled historically and with WASM wheels on PyPI). Test it first; a forced replacement introduces a new source of numerical discrepancy and invalidates the proposed 0.1 % water-property check.
* Session state and data files. Lab-notebook batches live in Streamlit session state and disappear on reload. Overlay images and JSON data must be correctly mounted in the browser filesystem. Pint appears to be used mainly for tests; it should be guarded or stripped for the browser build.
* Scope. Porting all eight views plus the GP optimizer is the heavy path. A lite port that keeps only the packed-bed / grind explorer plus core charts would be far safer.

Safer alternatives, ranked:

1. Keep the existing Streamlit Cloud link as the primary working demo; ship a full or reduced stlite build on Pages; add a pure static HTML/JS grind-size explorer (pre-computed Ergun numbers) as an instant fallback.
2. Lite stlite only (Packed-bed view + theory charts). Matches the professor’s framing with far fewer moving parts.
3. Keep the full app on Streamlit Cloud and build a minimal independent Ergun calculator (JS or small WASM) for the Pages site, closer to the course example.

The existing offline KaTeX pipeline under docs/ (render_katex.js + build_guide.py) should be reused rather than reinvented.
3. Two-model comparison design
Not yet fair or convincing.

* Same-provider models (Opus vs Sonnet) do not demonstrate the independence the requirement asks for. Use a clearly different model (ChatGPT or Gemini) as the primary second implementation.
* The chosen task (documentation page + Ergun chart widget) is mostly front-end. It does not stress the physics, dimensional analysis, or the optimiser that the course actually cares about.
* Scoring on lines of code, wall-clock time, and “number of corrections” mixes your prompting skill and network conditions into the result. Prefer objective, pre-registered checks: equations match the tested Python model within stated tolerances, every symbol has SI units, and the existing pytest physics suite still passes.

A better design freezes the prompt, the starting code snapshot, the iteration budget, and a numeric test suite before either model runs. Keep both outputs and the diff in the repo and state the acceptance decision in numbers.
4. What would make the “AI process” documentation convincing to a fluids professor
A professor who teaches packed-bed flow will look for three things: (1) evidence that the numbers are real, (2) clear student agency, and (3) honest failure modes.
Right now the plan’s “v1→v5 timeline with links to plan files” cannot be verified; the repo contains only sections inside progress.txt for v3–v5, all dated the same day, and no discrete v1/v2 files. Broken links will undermine trust immediately.
Make the page persuasive by showing:

* Exact prompt text, date, model version, and the resulting code/doc change for the critical turns (especially the rejection of the PINN idea, the switch to coffee, the re-centring on Ergun + dimensional analysis, and the decision to use real published data).
* Concrete AI mistakes with before/after numbers (the early mis-reading of the Moroney experiment, the Ergun constants that do not match measured coffee-bed permeability).
* What you personally verified (Corrochano over-prediction range, Reynolds-number regime, calibration residuals, the automated symbol/unit/KaTeX tests).
* Explicit model limits written in your own voice (display bounding of Δp, the remaining TDS gap the optimiser cannot close, places where the model extrapolated).

Surface the actual pytest output and the Corrochano 1.9–16× discrepancy rather than merely claiming “validation.”
5. Course-content section — missing or cuttable
The core (Buckingham-Pi derivation of the friction factor / particle Reynolds number, Ergun from Kozeny–Carman + Burke–Plummer, grind-size effects on permeability and plunge force) is solid and should stay.
Missing or under-emphasised:

* A compact validity statement: particle Reynolds-number range, porosity, bed aspect ratio, the single-sphere assumption versus real grind distributions, consolidation, and the regime where Ergun diverges. The Corrochano over-prediction belongs on this page, not buried.
* Material and energy balances treated as first-class content rather than secondary links.
* Explicit disclosure of the 0–8 bar display bound on plunge pressure and the unbounded values next to it.

Demote or clearly label:

* Channeling (two parallel Darcy paths) currently lacks published validation data; call it illustrative or move it to an extensions section.
* Presenter, quiz, and Lab-notebook views are useful for the talk and the live demo but are not course content. Keep them in the demo, not as equal peers on the documentation pages.

Before any recording, decide whether the default recipe remains off-spec (current TDS and extraction miss the target) and whether that off-spec state is the teaching point or a bug that should be fixed for the first impression.
6. Concrete improvements, ordered by importance

1. Perform a short, dedicated stlite/Pyodide compatibility spike with the exact pinned versions, CoolProp, the GP optimiser, and the multi-view UI before locking the architecture.
Reason: version and package availability failures are the most probable show-stoppers.
2. Test CoolProp under Pyodide first; keep it if it works.
Reason: the plan’s assumption that it must be replaced is incorrect and a replacement adds unnecessary physics risk.
3. Change the second implementation model to a non-Anthropic model as the primary comparison.
Reason: same-family models do not meet the spirit of “different AI models.”
4. Redesign the comparison task around a physics-bearing, testable unit (e.g. the grind explorer or channeling module) scored by the existing pytest suite and numeric tolerances.
Reason: a documentation page cannot demonstrate that a model understands Ergun or dimensional analysis.
5. Put the working Streamlit Cloud link first on the Demo page and ship a static HTML/JS grind-size explorer as a zero-load fallback.
Reason: a long WASM download can fail during a live presentation.
6. Archive discrete plan artefacts (or permanent commit links) for every claimed version and make every process-page statement resolve to evidence.
Reason: currently the claimed v1–v5 trail is incomplete.
7. Write the presentation script, recording plan, and YouTube-comments checklist before further site work.
Reason: the video and transcript are graded deliverables, not afterthoughts.
8. Define and document the exact process for capturing and displaying the auto-generated transcript (verbatim, searchable).
Reason: any post-edit destroys compliance with Req 3.
9. Surface the Corrochano permeability discrepancy and the Moroney calibration residuals on the course-content page with brief explanation.
Reason: these are the project’s strongest honest results; burying them invites a grader to discover them first.
10. Add an explicit validity/assumptions box (Re_p range, porosity, L/D, grind distribution, display bounds) and disclose the 0–8 bar Δp clip.
Reason: fluids faculty grade the range of applicability at least as heavily as the equation itself.
11. State on the site whether the submission is individual (and the corresponding points ceiling) and cleanly separate student, model, and literature contributions.
Reason: the current assumption is invisible to a grader.
12. Reuse the existing offline KaTeX build rather than constructing a parallel one.
Reason: the pipeline already produces self-contained, CDN-free pages; duplication creates regression risk.
13. Seed the Lab notebook with example runs or remove it from the default first-open path of the browser demo.
Reason: an empty notebook is a poor first impression.
14. Expand the acceptance criteria for the browser build to include measured cold-start time, GP completion, and screenshots on phone-width and desktop-width viewports in more than one browser.
Reason: “no Python exceptions in headless Chromium” does not prove the demo works for a grader on a phone.
15. Add a machine-generated “still missing” checklist on the home page that disappears only when the video link, transcript, critique, and contribution statements are actually present.
Reason: lingering placeholders are the simplest way to lose points on an otherwise complete site.

Decide for each item, record the accept/reject decision and a one-line justification on the site itself. That transparency strengthens the AI-process narrative more than any polished prose.