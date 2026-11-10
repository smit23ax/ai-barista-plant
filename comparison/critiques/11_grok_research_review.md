<!-- Archived verbatim from the project chat. Message id cmsg_01GsSXTrvaoYWhp6JXGGNW97CN4Gp9xEV4UBLGZAjqhaNq, time 2026-11-05T16:25:26Z. Pasted by alex; the model is as alex named it. -->

1. Physics check (sections 1–2 and 7)
The core Ergun form, Buckingham Pi groups, and low-Re placement are correct and consistent with standard chemical-engineering usage.

* The written Ergun equation matches the classic form (viscous coefficient 150, inertial 1.75).
* fp=(Δp/L)dsε3ρu2(1−ε)f_p = \frac{(\Delta p/L) d_s \varepsilon^3}{\rho u^2 (1-\varepsilon)}fp=ρu2(1−ε)(Δp/L)dsε3 and Reb=ρudsμ(1−ε)Re_b = \frac{\rho u d_s}{\mu (1-\varepsilon)}Reb=μ(1−ε)ρuds are the conventional packed-bed groups; Ergun then collapses to fp=150/Reb+1.75f_p = 150/Re_b + 1.75fp=150/Reb+1.75. Both groups are dimensionless.
* Limits are correct: low RebRe_bReb recovers the Kozeny–Carman / Darcy regime; high RebRe_bReb recovers Burke–Plummer.
* Your computed regime (Reb≈0.76Re_b \approx 0.76Reb≈0.76–1.05, inertial share ~1 %) is firmly viscous-dominated, which is expected for a gentle French-press plunge.

Issues a fluids grader will notice

* Porosity assumption ε=0.40\varepsilon = 0.40ε=0.40. Corrochano et al. (2015) measured wet, consolidated coffee beds in the range ~0.09–0.19 (espresso-style packing). A French-press cake is looser, but 0.40 is still on the high side of typical random-pack values and is presented as a fixed assumption. Flag it explicitly and show sensitivity.
* Effective diameter. Using ds=Φsd32d_s = \Phi_s d_{32}ds=Φsd32 with Φs=0.75\Phi_s = 0.75Φs=0.75 and a bimodal mix (nominal grind + 15 % fines at 30 µm) is a reasonable engineering approximation, but the fines fraction dominates KKK. The 4× change in nominal grind producing <2× change in KKK is a real, important finding; state the assumption clearly.
* Plunge force. Defining it as fluid resistance only ((Δpcake+Δpmesh)×A(\Delta p_\text{cake} + \Delta p_\text{mesh}) \times A(Δpcake+Δpmesh)×A) is clean and matches the code. The AJP (2021) measurements include seal friction, buoyancy, etc., so your 2.5–3.9 N values are lower-bound hydrodynamic forces; label them as such.
* Mesh resistance. The assumed Rmesh=2×108R_\text{mesh} = 2\times10^8Rmesh=2×108 m−1^{-1}−1 contributes ~35 % of Δp\Delta pΔp at 800 µm. That is large enough that it should appear in the validity / assumptions table.
* Missing explicit statement of superficial velocity uuu and that the bed length is obtained from dose / (bulk density × area). Both are present in the code but should be written out with SI units before the first equation.

Overall the physics is defendable once the assumptions (especially ε\varepsilonε and the fines model) are called out with the same honesty already applied to the Corrochano over-prediction.
2. Research questions (section 8) — answers with citations; what could not be verified

1. Ergun / Kozeny–Carman constants for coffee
Corrochano et al., J. Food Eng. 150 (2015) 106–116: experimental permeabilities 10−1310^{-13}10−13–10−1410^{-14}10−14 m²; conventional Kozeny–Carman (constant 150 or 180) systematically over-predicts. They introduce a porosity-dependent tortuosity correction. Equivalent viscous constants implied by the data are hundreds to thousands, consistent with the 280–2400 range you quote. Most published work is for espresso-style high-pressure beds; I found no dedicated French-press (low-pressure, coarse) Ergun re-fits.
2. Fines and Sauter diameter
Uman et al., Sci. Rep. 6 (2016) 24483: grind distributions are essentially independent of bean origin; fine-particle cutoff ~70–76 µm at room temperature (shifts lower when beans are cold). Number modes around 13–27 µm appear. Using a single 30 µm “cell” for the fines fraction is a simplification; real fines are a continuum. Mass fraction of fines for typical French-press grinds is not quantified in that paper; the 15 % you adopted is an engineering assumption.
3. Wet-bed porosity / swelling
Corrochano reports 0.09–0.19 after wetting and consolidation under the pressures used in their rig. Low-pressure French-press data are scarce. Swelling occurs, but quantitative low-pressure French-press porosities were not located in the primary sources I checked.
4. Fines migration / filter-cake skin
Qualitative discussion exists in the espresso literature; quantitative French-press data that would explain the growing Ergun discrepancy with grind size were not found.
5. Plunge-force measurements
American Journal of Physics 89, 769 (2021): measured forces for a standard French press. Steady-state force ~12.5 N at very low speed for the recommended dose; ~32 N to complete the plunge in ~50–60 s. These include seal friction, buoyancy and mesh; your pure fluid-resistance numbers (2.5–3.9 N) are therefore a lower bound. Direct grind-size sweep of plunge force was not reported.
6. Dimensional-analysis conventions
The form you use (RebRe_bReb and fpf_pfp both containing (1−ε)(1-\varepsilon)(1−ε)) matches Ergun (1952) and the majority of chemical-engineering textbooks (Bird–Stewart–Lightfoot, McCabe–Smith, etc.). Some authors absorb the porosity differently; the difference is purely conventional provided the same groups are used consistently on both sides of the equation.
7. Channeling in immersion/press beds
Quantitative evidence is abundant for espresso; far thinner for French-press / immersion. Cameron (2020) is espresso-focused. Treat channeling as illustrative.
8. CoolProp / Pyodide
Pyodide currently ships CoolProp 7.2.0. CoolProp 8.x uses the same IAPWS-95 / IF97 formulations for liquid water in the relevant T–P window; differences for ρ\rhoρ, μ\muμ, cpc_pcp of liquid water near 340 K are expected to be far smaller than 0.1 %. No specific stlite 1.12 + st.segmented_control / Plotly breakage was confirmed in public issue trackers, but version lag is real.
9. YouTube
Comment length limit is still 10 000 characters. Auto-generated English captions for a clean 7–8 min talk normally appear within a few hours to ~24 h; the ≥48 h buffer you already planned is safe.
10. Teaching angle
Standard textbooks present Ergun as an empirical correlation fitted on a limited data set of relatively mono-disperse, non-swelling particles. Students are expected to note the range of validity (roughly Rep<1000Re_p < 1000Rep<1000), the sensitivity to porosity and particle-size distribution, and that real beds (polydisperse, deformable, swelling) routinely require adjusted constants or additional physics.

3. Accepted / rejected suggestions in section 6
No accepted suggestion looks like a clear mistake. The only item I would revive is a short, optional note on the Rust/WASM pure-calculator path (Muse alternative C). It was correctly rejected as a second codebase, but a one-sentence “why we stayed with Python/static” on the How-it-was-made page would pre-empt the question “why not the course’s pure-WASM style?” Everything else in the status tables is sound.
4. Up to five high-impact improvements (professor framing: packed bed → Ergun → dimensional analysis → coffee grind size)

1. Put the dimensional-analysis derivation and the collapse onto fp=150/Reb+1.75f_p = 150/Re_b + 1.75fp=150/Reb+1.75 on the first content page, before any coffee numbers.
2. Show the grind-sweep table with the explicit statement that the 15 % fines dominate d32d_{32}d32 and therefore KKK; that single observation is the most original fluids insight in the project.
3. Add a one-row “where Ergun stops matching coffee” entry to the validity table that cites the Corrochano factor of 1.9–16× and lists the leading candidate causes (porosity, polydispersity, swelling, consolidation).
4. Make the plunge-force definition and the mesh-resistance share visible next to the Ergun equation so a grader sees the hydrodynamic model is complete.
5. Keep every claim label (Compared with experimental data / Model-predicted / Illustrative) on the same page as the number it qualifies; the honesty itself is part of the grade.

5. Closing
 grok