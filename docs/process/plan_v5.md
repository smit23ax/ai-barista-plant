# AI Barista Plant: plan v5 for approval

**What changed:** your professor framed the project as **"Flow through a packed bed: the Ergun equation and dimensional analysis, applied to coffee grind size."** v5 makes that the centrepiece. Everything already built stays, but it moves into a supporting role around one question:

> **How does grind size control flow through the coffee bed, and what does that do to the cup?**

---

## Grill-me questions (reply "proceed" to accept every recommendation, or answer by number)

1. **Which brewer is the packed bed?**
   - **French press plunge (recommended).** Keep the current plant; the grounds cake under the plunger is the packed bed. No rework.
   - Pour-over. Water drains through the bed by gravity, so grind sets the drawdown time. It's a classic packed bed, but the plant and extraction model need rebuilding.
2. **Show where other brewers sit on the Ergun chart?** Recommended: **yes, as context only.** One dot each for espresso, pour-over and French press on the friction-factor vs Reynolds chart. No extra models.
3. **Keep the AI operator?** Recommended: **yes, as the finishing touch.** It now chooses grind size with the packed-bed physics in the loop. Two minutes of the talk at most.
4. **Check Ergun against measured coffee-bed data?** Recommended: **yes, if you can upload Corrochano et al. 2015** (J. Food Eng. 150, "A new methodology to estimate the steady-state permeability of roast and ground coffee in packed beds"). I can't download it myself. Without it, I'll show the paper's published finding: Kozeny–Carman over-predicts coffee permeability by 1.3–6 times.
5. **What goes on camera?** Recommended:
   - (1) dimensional analysis: Buckingham Pi to the two groups
   - (2) Ergun: viscous plus inertial terms, and which one matters for coffee
   - (3) grind size: permeability, plunge force, extraction time and the trade-off
   - the material balance as the short link to the cup

---

## Steps (each reads: action — verify: check)

1. **Dimensional analysis unit** in Write/Say format. List the variables (ΔP/L, μ, ρ, u, d, ε), count the base dimensions, apply Buckingham Pi, and get the packed-bed friction factor f_p and particle Reynolds number Re_p — verify: the symbol audit and pint check that both groups are dimensionless.
2. **Ergun unit** in Write/Say format. The viscous term comes from Kozeny–Carman (Hagen–Poiseuille in pores; 150 vs 180 explained), and the inertial term from Burke–Plummer. Adding them gives f_p = 150/Re_p + 1.75 — verify: the code matches the closed form, and the limits are checked (low Re_p gives Kozeny–Carman, high Re_p gives Burke–Plummer).
3. **Replace Darcy with Ergun** in `physics.plunge` and report Re_p and the inertial share — verify: the existing tests still pass, and a new test confirms the inertial term is under 5 % for the standard recipe (so the Darcy assumption is shown, not assumed).
4. **Ergun chart in the app.** f_p vs Re_p on log axes (pinned ranges, legend outside), with the two asymptotes and the current batch as a live dot. Brewer dots are optional per Q2 — verify: AppTest plus a screenshot at laptop and phone widths.
5. **Grind-size explorer.** One slider sweeps grind size, with linked plots of permeability, plunge force, Re_p, extraction time scale and predicted EY. The trade-off is visible: finer grinds extract faster but are harder to push and leave more fines — verify: AppTest, plus monotonic trends asserted in tests.
6. **Coffee-bed data check** (only if the Corrochano PDF is uploaded). Digitize the measured permeability vs grind and compare with Kozeny–Carman/Ergun, with error bars — verify: an overlay on the source figure.
7. **Re-centre the guide, the presenter mode and the speaking script** on steps 1–5. The existing units stay as supporting sections — verify: every script section points to a presenter step, and the timing is 6–8 min.
8. **Push**, then deploy on Streamlit Cloud — verify: the public link opens on a phone.

**Smallest success check:** the dimensional analysis and Ergun units in Write/Say format inside presenter mode, passing the symbol and unit checks, plus the live Ergun chart dot, before anything else changes.

## Assumptions

- Ergun's constants (150, 1.75) come from beds of near-spherical particles. Coffee grounds are irregular and contain fines, so I use the Sauter diameter and treat the constants as estimates. The app says so.
- Bed porosity ε ≈ 0.4 is still assumed until measured data is available (Q4).
- The French press plunge is slow (pore Re ≈ 1), so the inertial term should be small. Showing that with numbers is part of the analysis.

## Facts I'll check myself

Typical espresso, pour-over and French press flow rates and bed depths for the chart dots (Q2). The standard Ergun derivation and its constants.

## Choices for you

Questions 1–5 above. Push authorization stays as you gave it ("streamlit app and github").
