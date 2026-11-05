# Final submission website: plan v4 (after the ChatGPT and Grok critiques)

**Critique trail.** Plan v1 was written by Claude Opus 5.5 and then reviewed by three other models.

- **Muse** critiqued v1 (20 points). Claude fact-checked it and wrote v2. Muse reviewed v2 (25 points) and withdrew numbers it couldn't verify. That produced v3.
- **ChatGPT** critiqued v1 together with Muse's first critique. It is independent: it says plainly that it could not load the live app, so it doesn't repeat the app numbers Muse later withdrew.
- **Grok**'s critique is a near-verbatim copy of Muse's round 1 (same 20 points, same headings, same withdrawn numbers). It is archived and reported on the comparison page as a finding ("Grok mirrored the critique it was shown"), but it is **not counted as an independent critique**.

v4 = v3 plus the decisions below.

---

## A. ChatGPT's points that change v3

| ChatGPT point | Decision | Reason / change |
|---|---|---|
| Streamlit Cloud as the primary full demo, a static Ergun explorer as the dependable browser demo, stlite only if the spike passes (#4–6) | **Accept** | Shifts v3's emphasis. The Demo page order becomes: (1) a static grind-size explorer that loads instantly from GitHub Pages, (2) the full app on Streamlit Cloud, (3) the stlite in-browser full app, labeled "experimental". The stlite spike still runs on day 1, but it no longer blocks anything. |
| "Different models" is not literally "different providers" | **Accept** | The site describes the cross-provider choice as a methodological improvement, not as what the rule requires. |
| Supplementary explanation task: "why can Ergun disagree with measured coffee-bed permeability?" | **Accept** | Cheap and directly on topic. Every model answers the same frozen question. Scoring checks whether each answer separates particle size distribution, particle shape (sphericity), porosity, compaction/consolidation, and correlation limits. It sits next to the coding test and does not replace it. |
| Iteration table: original approach → your intervention → engineering reason → AI change → verification → learning (#11) | **Accept** | This becomes the format for each iteration on the AI-process page (v1→v5, plus this submission plan). |
| Preserve originals and label reconstructions | **Accept** | Originals of plans v1–v5, assumptions v1–v2 and speaking scripts v1–v3 exist in the project folder and are copied unchanged. Anything reconstructed after the fact is labeled "retrospective summary". |
| Three claim labels: Validated / Model-predicted / Illustrative (#12) | **Accept** | Each result on the site carries one label. Ergun vs Corrochano is Validated (against data). Extraction vs Moroney is Validated (fine grind) and Model-predicted (coarse). Channeling is Illustrative. The AI optimizer benchmark is Model-predicted: **it was measured against the project's own simulator, not real brews**, and the site says so. |
| Sensitivity example: viscous ΔP ∝ d_p⁻², inertial ΔP ∝ d_p⁻¹ (#13) | **Accept** | Added to Course content, stating what is held constant (porosity, velocity, bed length, fluid properties). The halving result is checked numerically against `physics.ergun`. The page also notes that real beds break the constant-porosity assumption as grind changes. |
| Clarify what plunge force includes (#15) | **Accept** | Checked in code: `physics.plunge` returns fluid resistance only, the Ergun cake drop plus the mesh drop times the press area. Seal friction, buoyancy and acceleration are not included, and the site will say so. |
| The frozen task must fix the diameter convention | **Accept** | The prompt specifies d_s = Φ_s · d₃₂ with Φ_s = 0.75, the porosity, and the velocity definition, exactly as in the reference code. |
| Record model versions, tools, follow-up prompts and student interventions for each implementation | **Accept** | Added to the frozen protocol. |
| CDN dependence of Pyodide | **Accept as disclosure** | The stlite page loads its runtime from a CDN, and the site says so. The static explorer has no CDN dependency. |
| IndexedDB persistence for the Lab notebook | **Reject** | Seeded example batches cover the first-open state. Persistence adds risk for little gain. |
| Seven pages; video and transcript on one page; no Learnings page | **Accept merge, reject drop** | Video and transcript share a "Presentation" page. Learnings stays as its own visible section because requirement 4 names it. |
| Off-spec default as a teaching example (modify Muse #10) | **Already in v3** | v3 has the binary test: the AI operator runs from the default, recorded either way. |
| Auto-generated missing-items checklist is low priority | **Keep v3** | It costs about 20 lines, and Muse asked for the final build to fail on leftover TODO markers. |
| ChatGPT's agree/disagree table on Muse's critique | **Noted** | It matches v2/v3 decisions everywhere except the two rows above. Shown on the comparison page as a two-critic agreement table. |

## B. Grok

- **Archive verbatim.** Report the duplication honestly.
- **Optional, alex:** give Grok only `site_plan_v4_final.md` plus the requirements and ask for a fresh critique. If it brings anything new, it gets its own accept/reject table.
- **Grok stays a candidate implementer.** Implementers are: a fresh Claude Opus 5.5 session; ChatGPT (alex runs it); Muse (alex runs it); Grok optional.

## C. Pages (final)

1. Overview: the question, main findings (with claim labels), requirements map, submission checklist (website, YouTube video, comments, transcript, comparison, contributions, two in-class presentations)
2. Demo: static explorer, Streamlit Cloud, stlite (experimental)
3. Course content: dimensional analysis, Ergun, sensitivity example, validation and validity table, extraction (material balance), cooling (energy balance), Stokes; channeling under Extensions
4. How it was made: iteration tables, local vs cloud, prompt selection rule
5. Model comparison: plan → critiques (all verbatim) → decision log → frozen implementation test → explanation task → scores
6. Presentation: video, verbatim auto-transcript
7. Learnings
8. References and contributions

## D. Steps

These are the same as v3, with three changes. Step 0 (stlite spike) no longer gates anything. A new step 0b builds the static explorer first; verify that its curves match `physics.plunge` at every precomputed grind to within 1e-9 relative. The explanation task is added to step 2.

**Still needed from alex:** approval and permission to push and set up GitHub Pages; individual or group; the submission deadline and presentation dates; which commit Streamlit Cloud is running.
