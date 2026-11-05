# Round 6: fact-check and decisions on the three research reviews of the master briefing

Reviewed by Claude Opus 5.5 on 2026-11-05. The uploaded file holds three replies, called **A** (short physics + research), **B** ("Independent Physics and Research Review") and **C** (the long page with chips and a calculator). Which model wrote each is not stated in the file. **alex: please name them** for the comparison page.

---

## 1. Fact-check (what was verified, and how)

| Claim | Said by | Check | Result |
|---|---|---|---|
| Wadsworth et al. 2021 measured French-press plunger force (Am. J. Phys. 89, 769; doi:10.1119/10.0004224); "maximum force is 32 N to complete the pressing action in 50 s" | A, B | Durham research repository record (web, 2026-11-05) | **Verified.** Authors are Wadsworth, Vossen, Heap, Kushnir, Farquharson, Schmid, Dingwell, Belohlavek, Huebsch, Carbillet and Kendrick. |
| "No scientific measurement of French-press plunge force exists" | C | Same record | **Wrong.** C missed Wadsworth 2021. |
| "12–32 N" force range | A | Not in the abstract | **Unverified** (only 32 N is in the abstract) |
| Briefing says Pi gives "two groups"; it should be three (ε is the third) | B, C | `plant/steps.py` lines 223–227 already say "six variables, three dimensions, so three groups. One of them is epsilon itself." | **Right about the briefing's wording; the app was already correct.** The briefing sentence is fixed. |
| "Corrochano 0.12–0.33 porosity can't be verified" | C | The repo's `data/corrochano2015.json` was digitized from the paper's own Fig. 13 (alex uploaded the PDF on 2026-10-15). `tests/test_packed_bed.py` asserts it lies within 0.11–0.33. | **Verified from the primary source by us.** C couldn't reach the paywalled paper. |
| Corrochano consolidated porosity "0.09–0.19" | A | Conflicts with our digitized 0.11–0.33 | **Rejected** |
| Our 1.9–16x is our own back-calculation; the paper reports 31–521 % errors for its own model | B | `progress.txt`: "the paper's own 31–521 % errors were not reproduced exactly from its printed inputs" | **Correct.** The two must be labeled separately. |
| The live app uses an 8.0 cm press / 50.5 cm² | C | `D_press = 0.085` in `physics.plunge`. "50.5" and "0.080" appear nowhere in the code. | **Not found in code** (the same pattern as the earlier browser-report numbers) |
| ρ_bulk = 400 kg/m³ and ε = 0.40 are linked through particle density | C | Code constants: envelope density = 1337 × (1 − 0.53) = 628 kg/m³, so ε = 1 − 400/628 = **0.36** | **Valid point.** The code's own constants imply 0.36, not 0.40. This must be stated and the sensitivity shown. |
| Viscous and inertial terms are equal at Re_b = 150/1.75 ≈ 86 | C | Arithmetic | **Correct** |
| Sweep table recomputes from the stated model | C | Matches the code | **Correct** |
| Mo et al. 2023 (Sci. Rep. 13, 15970) exists: coffee microstructure, microCT + SPH | C | Web search (DOAJ, Swansea and arXiv records) | **Paper exists.** Its specific numbers (9.7–29.2 % below 100 µm, ε 0.13–0.24) are **not yet checked**. They must be checked before use. |
| YouTube comment limit 10,000 characters (API-enforced, not officially published) | C | — | Plausible and consistently reported. Split with headroom. |
| stlite moved to Pyodide 314.0.3 | C | Matches the stlite CHANGELOG we read | **Verified.** C says 1.11.0; the changelog entry is what matters. |

**What this shows for the comparison page:** A and B found the one directly relevant French-press measurement, while C, the most detailed reply, said none exists. C also repeated a not-in-code app number. Detail and confidence did not track accuracy.

---

## 2. The biggest new finding

The model predicts **2.7 N** (fluid resistance, 800 µm, 20 s plunge). Wadsworth et al. report a **32 N maximum for a 50 s press**. That is about 12x higher, even though their press is 2.5x slower, and a slower press should *lower* the viscous force.

The conditions are not yet matched (dose, press diameter, grind and the force definition all need checking), so this is **not yet a model error**. But it is the only direct French-press experiment, it sits squarely in the professor's framing, and it is the most important thing to add.

**Plan:**
1. Read the open-access copy (Liverpool and Durham repositories) and extract their geometry, dose, grind, speed and force definition.
2. Run `plunge()` at their conditions.
3. Show model vs measured, labeled *Compared with experimental data*.
4. Discuss the likely causes, kept as hypotheses: their total vs our fluid-only force, cake compaction during the press, wet-bed porosity, mesh resistance, and fines.

---

## 3. Decisions

| # | Suggestion | From | Decision | Change |
|---|---|---|---|---|
| 1 | Add Wadsworth 2021 as the direct French-press comparison | A, B | **Accept, top priority** | See section 2 |
| 2 | Pi: three groups (ε third), then Ergun's folding into two | B, C | **Accept** | The briefing wording is fixed; the app is already right. Add a dimensional matrix with its rank and null space on the Course page. |
| 3 | Sensitivity: ε 0.30–0.50, mesh ×0.5–2, fines fraction (fixed vs grind-dependent) | A, B, C | **Accept** | One chart: K and force vs grind for each scenario, labeled Model-predicted. |
| 4 | Link ε to bulk and particle density | C | **Accept** | State that the code's own constants imply ε = 0.36. Treat 0.40 as a scenario. |
| 5 | Label 1.9–16x as our back-calculation, separate from the paper's 31–521 % | B, C | **Accept** | |
| 6 | Ergun error growing with grind clashes with the fines-skin story | C | **Accept** | Present it as an open question: wall effects (D/d), bimodality, inertia. The skin stays a hypothesis. |
| 7 | Coarse-grind Moroney miss: τ_d ∝ d² links it to the same bimodality problem | C | **Accept** | One sentence ties the two mismatches together. |
| 8 | Crossover Re_b ≈ 86 | C | **Accept** | Add to the validity table and the Q&A prep. |
| 9 | Define the three "fines" cut-offs once (30 µm cell, ~70 µm distribution valley, 100 µm sieve) | C | **Accept** | |
| 10 | CoolProp 0.1 % becomes a reported measurement; gate only on TDS/EY/Δp within 0.5 % | C | **Accept** | |
| 11 | Freeze the fines rule and name both extra temperatures in the hidden tests | C | **Accept** | The fines rule is fixed at w_f = 0.15. The temperatures are 333.15 K and 353.15 K. |
| 12 | Seeded notebook rows labeled in the UI; add a CSV export of batches | C | **Accept** (reverses part of the earlier persistence rejection) | Uses `st.download_button`. No stored state. |
| 13 | Describe the explorer check as "no transcription error", not "verification" | C | **Accept** | |
| 14 | Name the trigger for the Rust/WASM fallback | C | **Accept** | The trigger is: the stlite spike fails **and** the static explorer proves too limited in rehearsal. |
| 15 | Show the f_p–Re_b collapse plot first | C | **Already in the app** | Promoted to the Course page's lead figure. |
| 16 | Cross-study permeability parity plot | B, C | **Accept, conditionally** | Only points we verify from the source: Corrochano (have it), plus Gianino, King, Navarini and Mo after checking. |
| 17 | Plot C_eff against D/d_p | C | **Accept** | Cheap, from the existing Corrochano data. |
| 18 | One blind plunge-force measurement | C | **alex's choice** | The bench procedure already exists (lab_procedure/). One measured point would be the project's only first-hand data. |
| 19 | Changing bed thickness during the plunge | B | **Accept as a limitation** | Stated in the validity table. Not modelled. |
| 20 | Corrochano porosity 0.09–0.19 | A | **Reject** | It conflicts with our primary-source digitization. |
| 21 | "No plunge-force study exists" | C | **Reject** | Wadsworth 2021 verified. |

## 4. Still open for alex

1. Name the models behind replies A, B and C.
2. Decide on the blind measurement (#18).
3. Approve the push and GitHub Pages.
4. Individual or group.
5. Deadline and presentation dates.
6. Which commit Streamlit Cloud runs.

## 5. Update 16:17: which model wrote reply B

alex pasted a "ChatGPT Independent Review" (2026-11-05). It matches **reply B** point for point:
- Pi correction "strictly ... three"
- Smrke 2024 and Ellero & Navarini 2019
- Wadsworth 32 N
- porosity 0.40 → 0.30 gives 31 % of K and 3.2× the pressure drop

So **B = ChatGPT**, and A and C are Muse and Grok in an unknown order.

It adds no new points. The cake-vs-mesh split, the porosity and fines sensitivity, and the fixed-geometry limitation are already accepted as #3, #4 and #19. On the site the cake and mesh split is shown in the explorer (Δp cake vs Δp mesh), and the sensitivity chart covers ε, R_m and w_f.

## 6. Update 16:25: which model wrote reply A

alex pasted Grok's reply, and it matches **reply A**: Corrochano "0.09–0.19" and "12–32 N". So **A = Grok, B = ChatGPT, and C = Muse** (Muse by elimination).

Grok's points and decisions:

| Point | Decision |
|---|---|
| Write u and the cake length L = m_c/(ρ_b A) with SI units before the first equation | **Accept.** Added to the Packed bed page. |
| Label model forces as a lower bound (fluid only) | **Accept.** Added. Note that Wadsworth also attributes their force mainly to flow through the pack; they neglected friction and mesh, and found the force without coffee "substantially less". So Grok's claim that their numbers *include* seal friction is only partly right. |
| Mesh share visible near the Ergun equation | **Accept.** Added. |
| Validity-table row "where Ergun stops matching coffee" | **Accept.** Added, with the 1.9–16× and 48× factors. |
| One sentence on why there is no Rust/WASM calculator | **Accept.** Added to How it was made. |
| Corrochano porosity 0.09–0.19 | **Reject.** It conflicts with our digitized 0.11–0.33 from the paper's Fig. 13. |
| Ergun valid to Re_p < 1000 | **Not used.** A different reviewer said 500; neither was verified, and the project sits at Re_b ≈ 1 anyway. |
