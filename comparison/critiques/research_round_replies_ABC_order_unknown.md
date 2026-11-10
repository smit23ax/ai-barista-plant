1. Physics check (sections 1–2 and 7)
The core physics is sound and well-aligned with a fluid-mechanics grader’s expectations.

* The Ergun form and the two Pi groups are the standard chemical-engineering version (Ergun 1952).
fp=(Δp/L) ds ε3ρu2(1−ε)=150Reb+1.75f_p = \dfrac{(\Delta p/L)\,d_s\,\varepsilon^3}{\rho u^2(1-\varepsilon)} = \dfrac{150}{\mathrm{Re}_b} + 1.75fp=ρu2(1−ε)(Δp/L)dsε3=Reb150+1.75
with Reb=ρudsμ(1−ε)\mathrm{Re}_b = \dfrac{\rho u d_s}{\mu(1-\varepsilon)}Reb=μ(1−ε)ρuds. Low-Reb\mathrm{Re}_bReb limit recovers Kozeny–Carman / Darcy; high-Reb\mathrm{Re}_bReb recovers Burke–Plummer. Your operating point (Reb≈0.8\mathrm{Re}_b \approx 0.8Reb≈0.8–1.1, inertial share ≈ 1 %) sits correctly in the viscous-dominated regime.
* ds=Φs d32d_s = \Phi_s\,d_{32}ds=Φsd32 with Φs=0.75\Phi_s = 0.75Φs=0.75 is the conventional non-spherical correction and is cited from Corrochano.
* Plunge force defined as fluid resistance only (Δpcake+Δpmesh\Delta p_\mathrm{cake}+\Delta p_\mathrm{mesh}Δpcake+Δpmesh) × area is clear and honest; seal friction, buoyancy and acceleration are correctly excluded.
* The fines model (15 % at 30 µm) producing a Sauter diameter that is only weakly sensitive to nominal grind is a real, important finding and should be highlighted.

Issues a grader will notice (already partly flagged in your own checklist):

* Assumed ε=0.40\varepsilon = 0.40ε=0.40 versus Corrochano wet-bed porosities of roughly 0.09–0.33 (and strong consolidation). Constant-porosity assumption while grind changes is the weakest modelling choice.
* Mesh resistance is assumed and contributes ~35 % of Δp\Delta pΔp at 800 µm; it is therefore not a minor correction.
* The 15 % fines fraction and 30 µm size are modelling choices, not measured for the exact grind used.
* Default recipe is off-spec; this is already treated as a teaching point, which is good.

Nothing is mathematically inconsistent. The main risk is presenting assumed values (ε\varepsilonε, mesh resistance, fines parameters) without the same visual weight given to the Corrochano discrepancy.
2. Research questions (section 8) that can be answered
1. Ergun / Kozeny–Carman constants for coffee

Corrochano et al. (J. Food Eng. 150, 106–116, 2015) measured steady-state permeabilities 3×10−143\times10^{-14}3×10−14–3×10−133\times10^{-13}3×10−13 m². Conventional Kozeny–Carman (pre-factor 180) systematically over-predicted; fitted effective constants rose to several hundred–>1000 when a porosity-dependent tortuosity was introduced. The paper attributes the gap mainly to consolidation and packing structure, not merely bulk porosity. Other coffee studies (espresso-focused) show the same qualitative over-prediction. No clean French-press-specific (low-pressure, coarse) data set with a published Ergun constant was located.
2. Fines and Sauter diameter

Uman et al. (Sci. Rep. 6, 24483, 2016) show that ground coffee is strongly bimodal; the fines peak is typically 13–30 µm and the number-based cut-off is ~70–76 µm. Fines are produced by cell-wall fracture and are relatively insensitive to nominal grind setting. Using a mass-weighted d32d_{32}d32 of a bimodal distribution is therefore physically motivated; the exact 15 % / 30 µm values remain a modelling choice.
3. Wet-bed porosity and swelling

Corrochano reports steady-state bed porosities after consolidation of ~0.09–0.19 (bulk densities 360–480 kg m⁻³). A 2021 laser-diffraction / microscopy study (J. Food Eng.) found no statistically significant particle swelling on the 0.5–5 min time scale of typical brewing; apparent size changes were dominated by gas release. Consolidation under even modest pressure is the dominant porosity reduction mechanism.
5. Plunge-force measurements

One direct study exists: American Journal of Physics 89, 769 (2021). For a standard French-press dose they measured steady forces of order 12–32 N depending on plunger speed and coffee mass. Their hydrodynamic component is the closest experimental counterpart to your fluid-resistance calculation.
6. Dimensional-analysis conventions

The form used in the briefing matches Ergun’s 1952 definition and the majority of chemical-engineering textbooks (Bird–Stewart–Lightfoot, McCabe–Smith, etc.). Some authors place the (1−ε)(1-\varepsilon)(1−ε) factor differently; the difference is purely definitional and should be stated once.
8–9. Runtime / YouTube

CoolProp 7.2 (bundled in current Pyodide) and 8.0 both implement IAPWS formulations; differences for liquid water at 60–90 °C are expected to be far smaller than 0.1 % for density and viscosity, but this should be verified numerically in the spike. YouTube auto-captions for a clean 7–8 min English video typically appear within a few hours to ~24 h; comment length is effectively unlimited for practical purposes (API rejects only extremely long strings).
Could not verify from primary sources: quantitative fines-migration / skin-formation data specific to low-pressure French-press plunges; any published plunge-force vs grind-size curve beyond the single AJP paper; exact numerical identity of CoolProp 7.2 vs 8.0 water properties under the precise Pyodide build.
3. Accepted / rejected suggestions
No accepted item in section 6 is a mistake.

The rejection of IndexedDB persistence remains correct (unnecessary risk).

The decision not to build a second Rust/WASM codebase is also correct.
One small strengthening: when the static explorer is verified, explicitly test the near-zero inertial contribution at the coarsest end with an absolute tolerance (already partially accepted).
4. Up to five high-impact improvements (for a professor who set the packed-bed framing)

1. Make the fines-dominated Sauter-diameter result the central “aha” of the grind explorer.
Reason: it is the most original, quantitative insight the project currently owns and directly answers “how does grind size control flow.”
2. Put a single validity box next to every Ergun plot: Reb\mathrm{Re}_bReb range, assumed ε\varepsilonε, assumed mesh resistance, and the measured Corrochano over-prediction factor.
Reason: a fluids professor grades range-of-validity statements at least as highly as the equation itself.
3. Show the viscous ∝d−2\propto d^{-2}∝d−2 vs inertial ∝d−1\propto d^{-1}∝d−1 sensitivity analytically and numerically on the same page as the explorer.
Reason: it demonstrates that the student understands the origin of the two Ergun terms, not merely that the code runs.
4. Explicitly label the mesh-resistance contribution and the constant-porosity assumption as modelling choices, not data.
Reason: honesty about the largest remaining uncertainties prevents a grader from treating them as hidden errors.
5. In the AI-process section, devote one short paragraph to the moment the project was recentred on the professor’s exact framing (packed bed → Ergun → dimensional analysis → grind size).
Reason: that decision is the clearest evidence of student agency and is more impressive than any particular code artefact.

5. Closing
The project is already in good shape. The physics is defensible, the honesty about model–data disagreement is a strength, and the website plan now has the right risk order. The highest remaining leverage is to surface the fines/Sauter finding and the validity limits with the same visual clarity already given to the equations. AI Barista Plant — Independent Physics and Research Review
Based on the November 5, 2026 master briefing, published scientific research, and the project's stated mathematical assumptions.
Executive assessment
The project has a defensible central engineering model, but I found one dimensional-analysis error and two important modeling limitations that deserve more attention before submission.

The most interesting scientific result is not simply that smaller coffee grounds increase flow resistance. It is that your assumed fines distribution makes nominal grind size much less influential than someone might expect from the usual inverse-square relationship.

Your briefing reports that changing nominal grind size from 300 to 1,200 µm increases predicted permeability by less than a factor of two. That is a useful result, but it depends strongly on an assumed 15% fines fraction at 30 µm.

I would present this as a model sensitivity finding, not a validated property of French-press coffee.

The other particularly valuable finding concerns the difference between idealized packed-bed behavior and actual coffee beds. Corrochano and colleagues measured permeability in the \(10^{-14}\)–\(10^{-13}\,\mathrm{m^2}\) range and found that conventional Kozeny–Carman predictions were too high, with consolidation influencing bed structure. Their measurements were made in an espresso-style packed-bed system, not a French press. 
ScienceDirect+1

1. Physics audit
Finding 1 — Buckingham Pi analysis needs a correction
Mathematical correction
Section 1 of the briefing states that Buckingham Pi analysis applied to
\[
\left(\frac{\Delta p}{L},\mu,\rho,u,d_s,\varepsilon\right)
\]

produces two dimensionless groups.

Strictly, it produces three independent dimensionless groups, because porosity \(\varepsilon\) is itself dimensionless.

There are six variables, and the dimensional matrix has rank three, corresponding to mass, length, and time:
\[
N_\Pi=6-3=3
\]

A valid initial choice is:
\[
\Pi_1=\frac{(\Delta p/L)d_s}{\rho u^2}
\]

\[
\Pi_2=\frac{\rho u d_s}{\mu}
\]

\[
\Pi_3=\varepsilon
\]

These can be rearranged into the project's preferred definitions:
\[
f_p=\frac{(\Delta p/L)d_s\varepsilon^3}
{\rho u^2(1-\varepsilon)}
\]

\[
Re_b=\frac{\rho u d_s}{\mu(1-\varepsilon)}
\]

Then the Ergun correlation becomes
\[
\boxed{f_p=\frac{150}{Re_b}+1.75}
\]

Your final equation is algebraically correct. The issue is claiming that dimensional analysis alone generates only two independent groups or determines Ergun's functional relationship.

Buckingham Pi establishes dimensionless combinations. The 150 and 1.75 coefficients and the correlation's functional form come from physical modeling and empirical work, not dimensional analysis alone.

Suggested correction for the website: Explain that the dimensional analysis first produces three independent groups, including porosity. The Ergun correlation then combines them into a two-axis friction-factor relationship using a specific porosity scaling.

This is a worthwhile correction because the professor explicitly emphasized dimensional analysis.
Finding 2 — The Reynolds number and friction-factor conventions are consistent
Using the definitions supplied in the briefing, the viscous contribution transforms as
\[
\frac{150\mu(1-\varepsilon)^2u}
{\varepsilon^3d_s^2}
\frac{d_s\varepsilon^3}
{\rho u^2(1-\varepsilon)}
=
\frac{150}{Re_b}
\]

and the inertial contribution transforms to 1.75.

So the nondimensional Ergun equation is internally consistent.

Other textbooks sometimes use
\[
Re_p=\frac{\rho u d_s}{\mu}
\]

without incorporating \((1-\varepsilon)\) into Reynolds number. Neither convention is automatically wrong, but the friction-factor equation must change consistently.

I would define the project's version as a modified packed-bed Reynolds number to prevent confusion.
Finding 3 — The inertial contribution is correctly characterized as small
At the briefing's typical operating point, \(Re_b\approx0.98\).

The inertial fraction of Ergun pressure drop is
\[
\frac{\Delta p_{\mathrm{inertial}}}{\Delta p_{\mathrm{cake}}}
=
\frac{1.75}{150/Re_b+1.75}
\]

which gives approximately 1.13%.

That supports your finding that the modeled coffee bed operates in a strongly viscous-dominated regime.

However, a low Reynolds number supports neglecting inertial resistance; it does not prove the assumed bed permeability is accurate. Particle geometry, porosity, compaction, and nonuniform flow can still produce large prediction errors.
Finding 4 — The reported permeability needs a stronger qualification
The briefing uses \(\varepsilon=0.40\) and a fixed 15% fines fraction. Both are assumptions.

Corrochano's measurements show that bed consolidation and structure can have substantial effects on permeability beyond a simple porosity adjustment. Their results are a strong reason to treat \(\varepsilon=0.40\) as a scenario rather than a known wet-bed value. 
ScienceDirect


There is also an important dimensional distinction: the constant 150 in Ergun's viscous term is not the same as the constant 180 in the conventional Kozeny–Carman equation. Both produce the same general porosity and particle-size dependence but different nominal permeability values.

The website should specify which coefficient is used for every plotted prediction and reference comparison.
Finding 5 — I found direct French-press force measurements
Important new source
This is the most useful new research finding.

The force required to operate the plunger on a French press coffee pot

Wadsworth and colleagues published this paper in American Journal of Physics in 2021. They used kitchen-based and laboratory experiments to study the relationship between plunger force, speed, and coffee mass.
Your model, default conditions
2.7 N
Fluid-resistance prediction at 800 µm, 341 K, and a 20 s plunge
Published French-press study
32 N
Reported maximum calculated force for a recommended preparation with a 50 s press


These values are not directly comparable experimental conditions. They should not be used to calculate model error without matching geometry, coffee mass, plunge speed, bed behavior, and force definitions.

The paper provides something the current project does not yet have: a published force-scale reference for a genuine French press, rather than espresso.

This does not prove that the 2.7 N prediction is incorrect. Your model excludes some mechanical contributions, and the studies have different conditions. But it creates a highly relevant scientific question:

Can the Ergun-based model reproduce the magnitude and trends of measured French-press plunge forces when comparable conditions are used?

That question connects the professor's packed-bed framing directly to an experimentally studied French press.

Sources: University of Liverpool research record and Original journal article. 
The University of Liverpool Repository+1


I would prioritize this paper over adding more general coffee-extraction research.
2. Research findings for the ten questions in Section 8
I found direct primary-source evidence for several questions. The most useful papers are Corrochano (2015), Wadsworth (2021), Smrke (2024), and Ellero and Navarini (2019).
Q1. What Ergun constants have been reported for coffee beds?
Partially answered from primary research

The constants 150 and 180 represent different conventional forms of the viscous packed-bed model. Corrochano uses 180 for the conventional Kozeny–Carman permeability expression and discusses why it can substantially overestimate permeability in consolidated coffee beds. 
Pure OAI


There is one important numerical issue in the briefing:

The reported 1.9–16× overprediction should be identified as a calculation from the project's comparison, rather than a directly reported result from Corrochano.

The paper's Section 4.6 reports errors increasing from approximately 31% to 521% for its conventional model comparison across particle distributions. That corresponds to theoretical-to-measured ratios of approximately 1.31–6.21, not necessarily the same ratios in your project. 
Pure OAI


Both results may be correct for their respective calculations, but they should not be presented as identical.

I did not verify a universally accepted coffee-specific replacement constant for Ergun's 150. In particular, deriving an effective coefficient of 280–2400 from experimental measurements does not mean those values are transferable to every coffee bed.

For non-espresso evidence, the 2021 French-press force study is a stronger starting point than extrapolating espresso permeability data.
Q2. Is the bimodal Sauter-diameter model defensible?
Supported concept; parameters not fully validated

The use of Sauter mean diameter is physically reasonable when representing particle surface-area-to-volume ratios.

For particles of equal density, a two-fraction approximation can be written as:
\[
d_{32}=
\left(
\frac{1-w_f}{d_c}+
\frac{w_f}{d_f}
\right)^{-1}
\]

where \(w_f\) is fines mass fraction, \(d_c\) is coarse diameter, and \(d_f\) is fines diameter.

For your assumptions—15% fines at 30 µm and the remaining 85% at a nominal 800 µm—
\[
d_{32}\approx165\,\mu m
\]

and, using \(\Phi_s=0.75\),
\[
d_s\approx124\,\mu m
\]

This illustrates why the model predicts a much smaller effective diameter than its nominal grind setting.

But I found a relevant experimental paper that should be added:

Smrke, Eiermann, and Yeretzian (2024), The role of fines in espresso extraction dynamics.

The researchers manipulated fines fractions experimentally, adding 1, 2, or 4 g of fines to 20 g coffee samples. Their results support the importance of fines in controlling permeability and extraction time.

However, the experiments were performed in espresso, using fines separated with a 120 µm sieve. They do not independently establish that French-press grinds contain a constant 15% mass fraction of exactly 30 µm particles. 
Scientific Reports


Uman (2016) supports the existence and variability of particle-size distributions, but I could not establish a general French-press fines mass fraction from that study. 
PMC


Conclusion: Keep the bimodal approach, but call the 15%/30 µm combination an assumed scenario.
Q3. What wet-bed porosity should a French press have?
Not conclusively established

Corrochano reported estimated consolidated bed porosities of 0.12–0.33 for the studied coffee beds. The study also reported uncertainty surrounding swelling in a strongly consolidated bed. 
Pure OAI


Those values are relevant, but they should not automatically replace your assumed 0.40 because a French press operates under different packing and loading conditions.

A useful sensitivity calculation illustrates the importance of this uncertainty.

For constant particle size,
\[
K\propto \frac{\varepsilon^3}{(1-\varepsilon)^2}
\]

Changing porosity from 0.40 to 0.30 would reduce predicted permeability to approximately 31% of its original value. Under Darcy-like flow at the same velocity, the viscous pressure drop would increase by approximately 3.2 times.

This is a mathematical sensitivity result, not an experimental prediction of what happens in a real French press.

I could not verify a single published porosity value that should be used universally for an ordinary low-pressure French-press grounds cake.
Q4. Does fines migration contribute to filter-cake resistance?
Supported mechanism; French-press magnitude unverified

Ellero and Navarini's 2019 paper, Mesoscopic modelling and simulation of espresso coffee extraction, directly discusses migration of fine particles and transient bed permeability.

Their model indicates that fines captured by a filter can change water residence time and flow resistance. 
ScienceDirect


This makes your proposed mechanism plausible: fines could accumulate near the French-press mesh and create additional local resistance.

But I did not verify experimental evidence quantifying that effect during French-press plunging.

Conclusion: The mechanism is scientifically defensible as a hypothesis. Do not state that it explains the observed Corrochano discrepancy without further evidence.
Q5. Have French-press plunger forces been measured?
Yes — directly answered

Wadsworth et al. (2021) addresses this question directly, as discussed above.

Their study varies plunger speed and coffee mass and provides a published maximum-force estimate of 32 N for its recommended preparation conditions. 
The University of Liverpool Repository


This paper should become a priority reference because it studies the actual physical process your application represents.

I verified the paper's title, authorship, experimental focus, and abstract, but did not independently reproduce its complete numerical model from the full article.
Q6. Which Reynolds-number convention is correct?
Answered

Both commonly used definitions can be valid:
Definition	Expression
Superficial-velocity particle Reynolds number	\(Re_p=\rho u d_s/\mu\)
Modified packed-bed Reynolds number	\(Re_b=\rho u d_s/[\mu(1-\varepsilon)]\)

The difference is the factor \(1-\varepsilon\).

With the project's modified definition, the friction-factor relationship is correctly written as:
\[
f_p=\frac{150}{Re_b}+1.75
\]

Original Ergun-era publications and packed-bed textbooks use related definitions and transformations. Your version is acceptable, provided it is clearly identified and consistently applied. 
Fluid Flow Through Packed Columns+1

Q7. Is channeling experimentally established for French presses?
Not verified

The literature supports nonuniform flow and particle migration in pressurized coffee systems. However, I did not find primary evidence that would justify treating the project's two-parallel-Darcy-path channeling model as a quantitatively validated French-press model.

Your existing decision to label channeling Illustrative is appropriate.
Q8. Will CoolProp and stlite produce equivalent results?
Compatibility supported; numerical equivalence not tested

Pyodide documents the 314.0.3 release, and CoolProp documents support for Pyodide, including bundled versions and WebAssembly-compatible packages. 
GitHub+1


The relevant question is not merely whether CoolProp imports successfully. It is whether the exact browser implementation reproduces the original application's water properties and subsequent simulation outputs.

I did not execute the browser build or verify the required 0.1% property agreement.

I also could not verify a specific unresolved stlite 1.12 problem involving st.segmented_control or Plotly from the primary documentation examined.

The agreed compatibility spike remains the correct way to answer this question.
Q9. How long do YouTube captions take, and what is the comment limit?
Partially answered

YouTube officially states that automatic captions may be unavailable immediately after upload and that processing time depends on audio complexity. It does not provide a guaranteed processing duration for a seven- or eight-minute presentation. 
YouTube Help


Therefore, the planned 48-hour allowance is a reasonable precaution, not a guaranteed caption-processing window.

I could not verify a currently guaranteed maximum YouTube comment length from YouTube's official documentation.

YouTube also warns that repeated comments, large amounts of pasted text, and links may trigger moderation or spam filtering. 
YouTube Help


I would preserve the original critique and practice transcript on the website, divide YouTube comments as needed, and check their public visibility from a logged-out browser.
Q10. What should a fluids professor expect students to conclude?
This is partly an educational judgment rather than a single factual claim.

The strongest engineering conclusion is:

The Ergun equation correctly expresses the expected scaling of pressure drop with velocity and effective particle size under its modeling assumptions, but the accuracy of an actual coffee-bed prediction depends on representing bed structure and particle-size distributions appropriately.

A complete explanation should distinguish:
- Derivation of dimensionless groups.
- Physical interpretation of viscous and inertial resistance.
- Empirically established coefficients and their limits.
- Parameter uncertainty, especially porosity and fines.
- Comparison with measurements outside the exact conditions used for calibration.
That is more scientifically convincing than treating a close numerical match to the application's own reference code as validation of the physical system.
3. Accepted and rejected suggestions: what should change?
I agree with most decisions in Section 6 of the briefing. I would reconsider three specific areas, rather than reopen the whole plan.
Existing decision	My assessment	Recommendation
Use fixed porosity \(\varepsilon=0.40\)	Accept as a baseline, but its uncertainty is consequential	Make porosity an explicit sensitivity parameter in the engineering analysis
Keep a fixed 15% fines fraction	Accept as an illustrative assumption, not a validated distribution	Include alternative fines scenarios and explain their impact
Use only a fixed-geometry, steady-state pressure-drop model	Appropriate as a first approximation	Discuss the changing bed geometry during plunging and compare it with Wadsworth's French-press study

I would not reverse the decisions to omit browser persistence, avoid a full Rust rebuild, or treat stlite as optional. Those choices remain reasonable.

One important distinction: passing the static explorer's reference tests proves that it accurately reproduces the existing Python model. It does not prove that either model accurately predicts a real French press.

Both types of verification have value, but the website should clearly identify which one has been performed.
4. Five improvements most likely to strengthen the project
These are additions to the existing plan, not repetitions of previously accepted website requirements.

1. Add Wadsworth et al. (2021) as a direct French-press comparison.

Reason: it provides published measurements and force estimates for the exact type of apparatus being modeled, making the project more relevant than an espresso-only comparison.




2. Run a two-parameter sensitivity study of porosity and fines fraction.

Reason: it shows whether uncertain bed structure matters more than the nominal grind size the user controls.




3. Correct the Buckingham Pi derivation to show three independent groups before rearranging into the Ergun relationship.

Reason: dimensional analysis is explicitly central to the assignment, and this removes a mathematical weakness a professor could identify.




4. Add a resistance-decomposition graph showing cake resistance versus mesh resistance.

Reason: at the default conditions, the assumed mesh contributes roughly 35% of total pressure drop, so it materially affects how grind-size changes translate into force.




5. Add a short discussion of the changing coffee-bed thickness during the plunge.

Reason: a growing or consolidating bed introduces time dependence that a constant-bed-length Ergun calculation cannot fully represent.



5. What I would show in the final presentation
The current 7–8-minute presentation plan does not need to become longer. I would use the new research to make its technical explanation stronger.
Suggested central demonstration: what actually controls flow?

Coffee-bed pressure dropMesh pressure drop

0 Pa150 Pa300 Pa450 Pa600 Pa3005008001200









Values from the briefing's model sweep at 341 K; not experimental measurements.





The mesh values are approximate residuals calculated from the rounded total and cake pressure drops in the briefing. This visualization is model-predicted, not experimentally validated.
I would narrate the demonstration in this sequence: start with the dimensional analysis, introduce Ergun, show the grind-size sweep, explain why the fines suppress the expected change in permeability, then contrast the idealized calculation with published experimental research.

This provides a clear progression from theory to model behavior to real-world limitations.
Final assessment
The most consequential new discoveries from this review are:
- The Buckingham Pi derivation should acknowledge porosity as a third independent dimensionless group.
- The model's 15% fines assumption deserves sensitivity testing because it strongly controls the result.
- Wadsworth et al. (2021) provides directly relevant published French-press force research that was missing from the bibliography.
- Corrochano's published model errors and your project's recalculated overprediction factors need to be distinguished.
- Changing bed geometry and consolidation are important physical limitations of the current steady-state model.
I would keep the approved website architecture and model-comparison protocol, correct the dimensional-analysis explanation, and prioritize the Wadsworth paper and parameter-sensitivity work.

Those additions are more likely to impress a fluid-mechanics professor than another website feature or another round of AI critiques. They also strengthen the central claim of the project: AI can build a useful engineering model, but understanding its assumptions, limitations, and relationship to experimental evidence remains essential. Physics checked, questions answered, suggestions judged
A cold read of the master briefing (plans v1–v5, compiled 2026-11-05): the physics in §§1–2 and 7 re-derived and recomputed, the ten research questions in §8 answered from the finished primary-source research, a verdict on the accepted and rejected suggestions in §6, and five new improvements aimed at the professor's framing — packed bed ⇒ Ergun ⇒ dimensional analysis ⇒ coffee grind size.

Briefing dated 2026-11-05
Research read 5 Nov 2026
Reference model: commit a8b24b6
Labels: Compared with experimental data · Model-predicted · Illustrative
How to read the chips: Holds re-derived or recomputed and it matches · Inconsistent two parts of the briefing disagree · Wrong / unsupported do not put it in front of a grader as stated · Could not verify the research could not confirm it from an accessible primary source.

Verdict
1 · Physics check
2 · Research Q1–Q10
3 · §6 verdicts
4 · Five improvements
Open items
Sources
Bottom line
The physics core is sound — the exposure is in three assumed numbers
The Ergun form, the Pi groups, and the grind sweep in §2 are internally consistent: I recomputed the sweep from the stated fines model and recovered every tabulated permeability to the printed precision (workings in §1 below). The dimensional-analysis convention in the code is exactly Ergun (1952)'s own. Nothing in §§1–2 is algebraically wrong.

What a fluids grader will press on is not the algebra. It is (a) porosity: the model assumes ε = 0.40 while §7 itself quotes wet coffee beds at 0.12–0.33 — and the research could not verify that range as Corrochano's; (b) the fines model: a single assumed 15% at 30 µm does almost all the work in the headline "grind barely matters" result, and no French-press fines fraction exists in the literature to support the 15%; and (c) the mesh: an assumed resistance supplies ~35% of the headline pressure drop, so the "packed-bed" force is part packed bed, part guess. All three are fixable with sensitivity ranges rather than new physics.

On §8: seven of the ten questions have solid, citable answers. Three — French-press plunge force, wet French-press cake porosity, and quantitative channeling in a press bed — have no published answer at all. That absence is itself a result: your plunge-force curve would be, as far as the research could establish, a novel dataset.

Task 1 · §§1–2 and 7 of the briefing
Physics check
Each finding is marked. Workings are shown where a number was recomputed, so you can defend them.

First, the recomputation — the §2 sweep checks out
With mass fractions and equal particle density, the Sauter diameter of the stated two-part mix (nominal grind + wf = 0.15 at 30 µm) is 1/d32 = (1−wf)/dnom + wf/30 µm, the effective diameter is ds = Φs·d32 with Φs = 0.75, and the Darcy-limit permeability is K = ε³ds² / [150(1−ε)²] at ε = 0.40:

Recomputed from the briefing's own stated model vs §2 table
Nominal grind	d₃₂ recomputed	d_s = 0.75·d₃₂	K recomputed	K in §2
300 µm	127.7 µm	95.7 µm	1.09×10⁻¹¹ m²	1.09×10⁻¹¹ m²
500 µm	149.3 µm	111.9 µm	1.49×10⁻¹¹ m²	1.49×10⁻¹¹ m²
800 µm	165.0 µm	123.7 µm	1.81×10⁻¹¹ m²	1.81×10⁻¹¹ m²
1200 µm	175.2 µm	131.4 µm	2.05×10⁻¹¹ m²	2.05×10⁻¹¹ m²
All four rows match to the printed digits — the §2 sweep is exactly what the stated model produces, with no transcription drift between the fines model, the Sauter diameter, and the permeability column. (You can reproduce any row yourself with the calculator below.)

Two further cross-checks pass cleanly:

Inertial share. From fp = 150/Reb + 1.75, the inertial share is 1.75 / (150/Reb + 1.75). At Reb = 0.98 that is 1.13% — the table's 1.1%. At 300 µm (Reb = 0.76) it gives 0.88% — the table's 0.9%. Holds
Force and geometry back out consistently. Δp ≈ 480 Pa with F ≈ 2.7 N implies a plunger area of ≈ 5.6×10⁻³ m² (≈ 85 mm diameter — a real French press). The cake term (310 Pa) at 341 K then implies a cake length of ≈ 6–7 mm, consistent with 15 g at a bulk density of 400 kg/m³ over that area. The model's hidden geometry is coherent. Holds
Ceff arithmetic. Since K ∝ 1/C, an over-prediction of 1.9–16× maps to Ceff = 150 × (1.9–16) = 285–2400 — the briefing's 280–2400. Holds
RECOMPUTE IT YOURSELF — NOMINAL GRIND (µm), FINES MODEL AS STATED IN §2 
Slider snaps to the same 10 µm grid as the app. Only formulas stated in §§1–2 are used: the two-part Sauter mix, ds = 0.75·d32, and K = ε³ds²/[150(1−ε)²] at ε = 0.40. No interpolation of briefing data.
Nominal grind
800 µm
d₃₂ (Sauter)
164.9 µm
d_s = 0.75 · d₃₂
123.7 µm
K (Darcy limit)
1.81 ×10⁻¹¹ m²
Fines share of 1/d₃₂
82%
Watch the last figure: even at the coarsest grind, the assumed 15% fines supply most of 1/d32 — which is why K moves so little. That is the model's most important and most assumption-driven result.

Permeability vs grind (§2)
Model-predicted. K rises less than 2× for a 4× grind change.

0
0.5
1
1.5
2
2.5
300
500
800
1200
nominal grind (µm)
K
K (×10⁻¹¹ m²)
Data: master briefing §2 grind sweep at 341 K (300 / 500 / 800 / 1200 µm).
Pressure drop vs grind (§2)
Model-predicted. Total Δp falls as the cake term falls; the mesh term (~169 Pa at 800 µm) does not depend on grind.

0
200
400
600
800
300
500
800
1200
nominal grind (µm)
Δp (Pa)
Δp total
Δp cake only
Total Δp and cake-only Δp from the same §2 sweep. The gap between the lines is the assumed mesh resistance.
1 · The Pi-group count is stated loosely Inconsistent
§1 says Buckingham Pi on (Δp/L, μ, ρ, u, ds, ε) "gives two groups." There are six variables and three fundamental dimensions, so there are three Pi groups — ε is itself the third, already dimensionless. What is meant is "two non-trivial groups plus ε." A dimensional-analysis-first professor will circle this. Fix the sentence; the resulting pair (fp, Reb) is correct, and §6 of the research below proves the code convention is Ergun's own.

2 · Porosity: the model assumes 0.40, §7 quotes coffee at 0.12–0.33 Wrong / unsupported
Two problems compound. First, the physics: ε enters K as ε³/(1−ε)², which changes by roughly a factor of 5 between ε = 0.30 and ε = 0.50 — and by far more if the true wet-cake ε is near 0.25. An assumed ε = 0.40 sitting outside the range §7 quotes for wet coffee beds is the single largest error source in the model, larger than the 150-vs-180 question. Second, the citation: the research could not verify any Corrochano porosity range — the paper is paywalled and no secondary source quoted one. The verified dense-bed numbers are Mo et al. (2023)'s: ε ≈ 0.17 matched for an espresso capsule, local samples 0.131–0.236 — tamped espresso beds, a lower bound for a loose press cake, not a measurement of one. Do not present "0.12–0.33 (Corrochano)" to a grader. Present ε = 0.40 as an assumption inside Ergun's original calibration range (0.38–0.47), show the ε-sensitivity, and say plainly that no wet French-press cake porosity exists in the literature (Q3).

3 · Cake length and porosity are not independent — and §2 treats them as if they were Inconsistent
The cake length comes from dose ÷ (bulk density 400 kg/m³ × area), while ε = 0.40 is assumed separately. But bulk density and porosity are linked through the particle (true) density: ε = 1 − ρbulk/ρtrue. With ρbulk = 400 kg/m³, ε = 0.40 implies ρtrue ≈ 667 kg/m³ — low for coffee solids, and complicated by the particles' own internal porosity (Mo et al. report cell pockets of 30–60 µm inside particles). Either state the implied true density and defend it, or derive L from a measured bed height instead. As written, a grader can make L and ε contradict each other with one line of arithmetic.

4 · The mesh is 35% of the headline Δp — and it is a pure assumption Inconsistent
§7's own checklist concedes Rmesh = 2×10⁸ m⁻¹ (assumed) supplies ~35% of Δp at 800 µm (169 of 479 Pa). That means the headline "packed-bed plunge force" is roughly one-third a number nobody measured, with a Darcy-only (viscous) form and no stated sensitivity. The briefing already separates cake and mesh in the §2 table — keep that separation in every headline figure and plot, and add a ±factor-of-2 mesh sensitivity next to the ε sensitivity. Otherwise the Ergun-vs-data comparison is partly a comparison of the mesh guess.

5 · The fines model carries the headline result, on an unverified 15% Could not verify
"A 4× change in nominal grind changes K by less than 2×" is presented as "a real finding." It is a real property of the assumed model: with wf = 0.15 fixed at every grind, the fines term contributes 0.005 µm⁻¹ of the 0.0061 µm⁻¹ in 1/d32 at 800 µm — over 80% — so d32 is nearly pinned. But measured fines fractions are not grind-independent: Mo et al. (2023) measure volume <100 µm falling from 29.2% (espresso) to 9.7% (coarsest, drip-filter). If wf falls with coarseness, d32 rises faster and the "grind barely matters" result weakens. Label the result Model-predicted and conditional on fixed wf, and show one curve with a grind-dependent fines fraction alongside it. Q2 below covers what Uman et al. do and do not say.

6 · Sphericity enters once, correctly — but say where Holds
Using ds = Φs·d32 in both Ergun terms gives Φs² in the viscous term and Φs in the inertial term, matching the standard form (Duda et al. 2002 write sphericity as 1/φ² viscous, 1/φ inertial). With Φs = 0.75 the viscous term alone is 1/0.75² ≈ 1.78× larger than for spheres — worth one sentence on the Theory page, because it means a chunk of the "Ergun is wrong for coffee" gap is already being absorbed by an assumed sphericity attributed to Corrochano 2015 that the research could only confirm second-hand. Keep Φs in the assumed-values table, not the measured-values table.

7 · Velocity and temperature bases are defensible but under-stated Inconsistent
Reb uses the superficial velocity u — correct for Ergun — but §§1–2 never state how u is obtained (plunger stroke ÷ 20 s ÷ press area), and a reader who assumes interstitial velocity u/ε gets a Reynolds number 2.5× larger. State the derivation of u next to its definition. The 341 K basis is justified in §2 (end-of-steep bed temperature; the cooling model gives 340.9 K after 240 s from a 93 °C kettle) — keep that sentence wherever 341 K appears, because water viscosity at 68 °C is roughly 40% higher than at 93 °C, so the choice moves Δp materially and looks arbitrary without it. One simplification to name: properties are evaluated at a single temperature for a plunge that happens across a cooling bed.

8 · Limits and regime — §7's checklist is right, with one addition Holds
The checklist's limit claims are correct: Reb → 0 recovers Kozeny–Carman/Darcy, Reb → ∞ recovers Burke–Plummer, and at Reb ≈ 0.8–1.1 the bed is deep in the viscous regime (inertial share ≈ 1%). The crossover the checklist doesn't give: the two terms are equal when 150/Reb = 1.75, i.e. Reb ≈ 86 — two orders of magnitude above the operating point. That one number is the fastest possible defence of "why we could almost use Darcy alone, and why we keep the inertial term anyway" (because the frozen comparison task and the fine-grind regime need it). Also add to the validity table: Ergun's original calibration spans ε ≈ 0.38–0.47 and the 2015 revisit advises against use above Rem ≈ 500 — the project sits comfortably inside both, which is worth saying.

9 · "Ergun error grows with grind size" needs its sign checked against the fines story Inconsistent
§2 reports Ceff drifting from ~280 to ~2400 as grind grows, i.e. Ergun gets worse for coarser beds. But the fines-skin explanation offered in §8 Q4 predicts the opposite trend: coarser grinds carry a smaller fines fraction (Mo et al.), so migration/skin effects should weaken with coarseness. The briefing holds both claims without noting the tension. The research points to more plausible coarse-bed mechanisms — wall effects as D/dp shrinks, inertial (Forchheimer) effects at larger pores, and d32 becoming a worse summary as the distribution gets more bimodal. Present the growing gap as an open question with competing explanations, not as evidence for the skin (Q4).

10 · Moroney numbers: correct, and the interesting half is under-played Holds
The fine-grind fit (τd 41 s vs 42.2 s) and coarse-grind miss (647 s vs 270 s, a factor of ~2.4) are stated accurately, labelled Compared with experimental data, and they mirror the permeability story: the model works where the bed is fine and fails as it coarsens. One missing sentence a grader will want: a diffusion time should scale roughly as τd ∝ d², so a fitted τd that must stretch 2.4× for the coarse grind is evidence that a single effective grain size cannot carry both grinds — the same bimodality problem as in finding 5, appearing in the extraction model independently. Say so; it turns two separate mismatches into one coherent finding.

11 · Two different "fines cut-offs" are used interchangeably Inconsistent
§2 cites Uman 2016 for a "fines cutoff about 70–76 µm," while the fines model uses 30 µm cells and the comparison literature (Mo et al., Smrke et al.) defines fines as <100 µm. These are three different definitions — a distribution valley (~70 µm), a cell size (~30 µm), and a sieve cut (100 µm) — and the briefing slides between them. Define each once, with its source, and never use one study's fraction with another study's cut-off. This is also why "15% fines" cannot be checked against Uman: Uman report no fines fraction by mass for any brew method (Q2).

12 · What §7 gets right — keep it Holds
The checklist questions themselves are the right ones, and two answers are already honest: plunge force is defined as fluid resistance only (no seal friction, buoyancy, or acceleration — §2 states this), and the GP benchmark is described as simulator-only. The off-spec default (TDS 1.10%, EY 17.9% vs the SCA box 1.15–1.35% / 18–22%) is also stated plainly. The gaps in §7 are findings 2, 4, and 5 above: porosity provenance, mesh share, and the unverified fines fraction should each appear in the checklist as open items with owners, not only as questions.

Task 2 · §8 of the briefing
Research questions, answered with citations
From the finished deep-research report (primary sources where accessible, read 5 Nov 2026). Every hedge the report attaches to a value is carried with it. Where the report could not verify something, the answer says so rather than filling the gap.

Q1Ergun constants for coffee beds
Short answer: no published coffee study reports a fitted Ergun viscous constant to replace 150 (or 180) — including Corrochano et al. (2015). Corrochano et al. did not fit Ergun at all; they measured steady-state Darcy permeability and fitted a modified Kozeny–Carman correlation. A secondary thesis summary reports the classic Kozeny–Carman form erring by up to 300% against their coffee data. Their reported permeability range, as cited by Mo et al. (2023), is k = 2.59×10⁻¹⁴ – 3.36×10⁻¹³ m² at ~1 bar overpressure. So the briefing's "Ceff = 280–2400 implied by Corrochano" is your own back-calculation from the permeability gap — legitimate, but label it as your derived quantity, not a constant Corrochano report.

The 150 vs 180 distinction is generic, not coffee-specific: 150/1.75 is Ergun (1952)'s fit; 180 is the Carman–Kozeny laminar-limit constant (Carman 1937; Kozeny 1927). Coulson & Richardson attribute the difference to "differences in shape and packing of the particles." Macdonald et al. (1979) give 180 with an inertial range of 1.8–4.0. If your project fits its own data, reporting your own fitted A and B with intervals, against 150/1.75 and 180/1.8, is the publishable result.

Coarse, low-pressure beds: none for French press. The nearest analogues are moka-pot studies at ~0.01 bar: Gianino (2007), k = 2.3×10⁻¹² m²; King (2008), k = 8.98×10⁻¹³ m² — an order of magnitude above the ~1 bar values (Navarini et al. 2009: 0.7–4×10⁻¹³ m²). Mo et al. attribute part of that pressure gap to inertial (Forchheimer) effects, not only compaction. A French-press plunge is low-Δp, so the Gianino/King end is the more relevant analogue — but those are still fine/medium moka grinds.

Sources: Corrochano et al. 2015, J. Food Eng. 150, 106–116 — doi:10.1016/j.jfoodeng.2014.11.006 (paywalled; permeability via Mo et al.); Mo et al. 2023, Sci. Rep. 13, 15970 — PMC10541431; Gianino 2007, Am. J. Phys. 75(1), 43–47, doi:10.1119/1.2358157; Navarini et al. 2009, Appl. Therm. Eng. 29, 998–1004, doi:10.1016/j.applthermaleng.2008.05.014. Could not verify Corrochano's exact modified-Kozeny–Carman formula: the secondary transcription's denominator (72·λp², λp = 7.5) conflicts with a patent's generalised form (factor 36) — check the original paper before quoting either.

Q2Fines and the Sauter diameter
d32 is the right diameter in principle; the single-30 µm-cell fines model is a defensible first approximation, not a measurement. Kozeny–Carman is a surface-area argument (specific surface S = 6/d32 for spheres), so the surface–volume mean is the theoretically correct input, it is what Corrochano et al. use, and Breard et al. (2019) confirm Φ·d32 predicts mixture permeability in other granular systems. Using a volume mean instead would over-predict k by roughly (d4,3/d3,2)² ≈ 10×.

But d32 alone is not sufficient for coffee: the distribution is bimodal, d32 is dominated by the fines, and the fines are irregular cell-wall fragments that agglomerate dry, erode wet, and migrate. Mo et al. (2023, Table 1, verified) locate the fines peak at ~30–40 µm — "inner walls cellular fragments," cell size 25–50 µm — so a ~30 µm mode position is defensible. The mode has width, though, and wet PSDs show more fines than dry ones (fines are agglomerated onto coarse particles when dry), so a dry-measured d32 biases permeability high.

Fines fraction for French press: Uman et al. (2016) do not give one. They establish bimodality — fines contribute the majority of accessible surface area — and that PSD is independent of bean origin, with cold grinding giving a narrower distribution. No French-press setting, and no fines fraction by mass or volume for any brew method, appears in the paper. The only measured proxy is Mo et al.'s volume fraction <100 µm: 29.21% (espresso), 27.52% (capsule), 20.26% (moka), 9.7% (drip-filter — the coarsest, closest to French press), with d3,2 from 81.0 µm (espresso) to 214 µm (filter) against d4,3 of 308–673 µm. Note that is a volume fraction; it equals a mass fraction only if particle density is size-independent, which is not established for porous coffee. Recommendation from the research: compute d32 from a measured full distribution and report the sensitivity of k ∝ d32² to the fines cut-off (<100 µm, <50 µm, full distribution), rather than hard-coding 30 µm.

Sources: Uman et al. 2016, Sci. Rep. 6, 24483 — PMC4834475, doi:10.1038/srep24483; Mo et al. 2023 — PMC10541431; Smrke et al. 2024, Sci. Rep. 14, 5612, doi:10.1038/s41598-024-55831-x (fines = <100 µm by volume; more fines → lower permeability); Breard et al. 2019, J. Geophys. Res. Solid Earth, doi:10.1029/2018JB016544.

Q3Wet-bed porosity and swelling
No published wet French-press cake porosity exists — do not quote a single literature value. The closest measured beds are dense espresso/capsule beds: Mo et al. matched ε ≈ 0.17 for a type-E capsule, with local 708 µm samples at 0.131–0.236. A "loose bed of 0.3–0.5" appears in a secondary review as an assumption, not a measurement. Ergun's own calibration range is ε ≈ 0.38–0.47. The research recommendation: measure your own, ε = 1 − mdry/(ρtrueVbed), for dry-loose, wet-settled, and wet-after-plunge states, and run Ergun across ε = 0.3–0.5 — the factor ε³/(1−ε)² changes ≈5× across that range, which alone can swamp the 150-vs-180 question.

Swelling is a genuine literature conflict — present both papers. Hargarten et al. (2020) report ≈15% diameter increase (≈52% volume, since 1.15³ ≈ 1.52), 60–80% of it within 30 s, complete in 4 min, independent of initial size and roast. Maille et al. (2021) report no statistically significant swelling by laser diffraction or in-situ microscopy, and conclude particle expansion "need not be considered" in brewing models. If swelling is real and the bed is wall-constrained, intergranular porosity must fall — a first-order effect on k. Bed consolidation under pressure is reported for espresso (Navarini et al. 2009; a 2026 poroelastic preprint reports Darcy-linear flow below ~5 bar); at French-press stresses it is likely small, but that is an inference.

Sources: Mo et al. 2023 — PMC10541431; Hargarten et al. 2020, J. Sci. Food Agric. 100(10), 3960–3970, doi:10.1002/jsfa.10440 — AGRIS record; Maille et al. 2021, J. Food Eng., doi:10.1016/j.jfoodeng.2020.110420. Could not verify any Corrochano (2015) porosity range, and any low-pressure (French-press-range) wet-bed consolidation measurement.

Q4Fines migration and filter-cake formation
Evidence exists — for espresso. Nothing quantifies a skin, and nothing was found for a French press. Fasano et al. (2000) inferred fines transport from flow-reversal experiments: flow starts fast, slows, stays slow on restart (so it is not puck compression), and the fast-then-slow pattern repeats when flow is reversed — explained by fines carried to the downstream face, obstructing flow and trapping further fines. Ellero & Navarini (2019) model fines as independent moving particles in SPH with reported good agreement. No source quantifies skin thickness, mass, or permeability. Mo et al. (2023) complicate the picture: their post-extraction microCT shows higher porosity at the outlet, which they attribute to pressure-driven erosion — the opposite signature to a fines skin.

Would it explain Ergun error growing with grind size? Probably not — the sign is wrong. Fines fraction falls as grind coarsens (29.2% → 9.7% by volume <100 µm, Mo et al.), while the fines mode stays at 30–40 µm (set by cell size, not the grinder). A skin mechanism should therefore weaken for coarse grinds. Error growing with coarseness points instead to wall effects at small D/dp (a 2011 wall-effect paper: Ergun "would differ significantly from measurements" if D/d ≲ 40), inertial effects in larger pores, and d32 summarising a more strongly bimodal distribution ever worse. The geometry in a press is at least analogous — during plunging, fines are carried toward the mesh, the downstream face — so the skin is a legitimate hypothesis for press resistance, testable by sectioning a plunged cake and comparing top vs bottom layers, or by plunging a fines-depleted grind at the same d32.

Sources: Fasano, Talamucci & Petracco 2000, doi:10.1007/978-1-4612-1348-2_8 (via Barista Hustle's summary — secondary; no skin quantity in sources accessed); Ellero & Navarini 2019, J. Food Eng., doi:10.1016/j.jfoodeng.2019.05.038; Mo et al. 2023 — PMC10541431; Navarini & Rivetti 2010, Food Chem. 122, 424–428.

Q5Plunge force measurements
None. No peer-reviewed — or any scientific — measurement of French-press plunge force vs grind size was found. The only quantitative claim anywhere is an unsourced blog statement of "about 15–20 lbs" (≈67–89 N) of ideal plunge force (CafeKerva, 2024): no grind dependence, no beaker diameter (force without area is not a pressure), no method. Do not cite it as data; at most as anecdotal guidance circulating online. Note how far it sits from the model's 2.7 N fluid-resistance-only prediction at the default — that gap is exactly why the force definition (fluid resistance only, no seal friction) matters, and why a measurement would be valuable.

What can be said from first principles: F ≈ Δp × Aplunger + friction + weight, so a measured Δp (or an Ergun-predicted one) plus plunger area predicts a force. Your force-vs-grind curve would, as far as this research could establish, be a novel dataset — frame it that way, and report force, plunger diameter, plunge speed, dose, and grind distribution together, since none are standardised in the literature. Tamping-pressure studies (Kuhn et al. 2017; Cameron et al. 2020) are about bed preparation in espresso, not plunging, and give no press force number.

Sources: research report §5 (systematic search, negative result); Kuhn et al. 2017, J. Food Eng. 206, 37–47, doi:10.1016/j.jfoodeng.2017.03.002. Could not verify any numeric plunge force, any Δp during a press plunge, or any standard plunge speed.

Q6Dimensional-analysis variants — which convention is Ergun's?
The code's convention is exactly Ergun (1952)'s, in its modified-Reynolds-number form. The research verifies it by algebra. Starting from the standard form:

Ergun, Δp/L form
Δp/L = 150·μu(1−ε)²/(d_s²ε³) + 1.75·ρu²(1−ε)/(d_sε³)
Multiplying through by dsε³/[ρu²(1−ε)] gives fp = 150/Reb + 1.75 with Reb = ρuds/[μ(1−ε)] — identically the briefing's §1 pair. It is also the form on Wikipedia's "Ergun equation" (where Reb is called Grp).

The variants are bookkeeping, not physics. Ergun's Δp/L carries (1−ε)² in the viscous term and (1−ε) in the inertial term; non-dimensionalising, you either absorb one power of (1−ε) into the Reynolds number (the code's clean form) or leave it in the friction factor, giving fk = 150(1−ε)/Re + 1.75 with the unmodified Re = ρud/μ. Bird–Stewart–Lightfoot define f from the total wetted particle surface area, making their f a further factor of 3 smaller (f = fk/3, i.e. 50(1−ε)/Re + 0.583); the Blake / Richardson–Harker–Backhurst convention is fk/6. The 2015 revisit (Powder Technology 283, 488–504) tabulates the whole family.

"The (1−ε) is not physics; it is bookkeeping… The constants 150 and 1.75 belong to one specific (f, Re) pair; transplanting them to a different pair without the accompanying (1−ε) or 1/3 factor is a dimensional-analysis error, not a different physical model." — recommended wording from the research report, §6
Sources: Ergun 1952, Chem. Eng. Prog. 48, 89–94; "A revisit of pressure drop–flow rate correlations for packed beds of spheres" 2015, Powder Technol. 283, 488–504 — ScienceDirect; Duda et al. 2002, Chem. Eng. Sci. 57, 527–534 (Buckingham-π derivation in Re and Ga, with sphericity entering as 1/φ² viscous, 1/φ inertial).

Q7Channeling beyond espresso
All quantitative evidence is espresso. No quantitative channeling study for a French press or cafetière was found. Cameron et al. (2020) infer inhomogeneous flow: a homogeneous-flow model predicts extraction yield falling monotonically as grind coarsens, but measured yield peaks and then falls at fine settings, with a critical minimum grind size below which yield drops and variability rises. That is inference from yield-vs-grind data plus a model — the paper publishes no channel width, bypass fraction, or velocity map. (A secondary summary quotes shortfalls of 2.6%, 6.1%, 13.1% below the homogeneous model at settings 1.5, 1.3, 1.1 — secondary, not verified against the paper.) Lee et al. (2023) supply a mechanism — a two-pathway model where an initial porosity/permeability imbalance is amplified by flow-coupled dissolution until one path is fully extracted — again espresso, and a model, not a measurement.

The most directly quantitative heterogeneity data are Mo et al. (2023)'s: permeability of 708 µm samples from the same capsule bed ranges from 0 (clogged) to 27.6×10⁻¹³ m² (type E) and 1.19–66.6×10⁻¹³ m² (type F) at porosities 0.13–0.24 — order-of-magnitude spatial variation, in espresso capsules. For immersion, Moroney et al. (2015) model the cafetière bed as a saturated, static, doubly porous medium with a single grain size — homogeneous by construction; their experiments measured extraction kinetics, not flow distribution. Reasoning (not a cited measurement): during steeping there is no imposed gradient to amplify Lee et al.'s instability, so channeling can only occur during the short plunge. A clean student test from the research: a dye pulse placed on the bed before plunging, photographed as it emerges through the mesh; and sieved (narrow-PSD) vs unsieved grinds at the same d32.

Sources: Cameron et al. 2020, Matter 2(3), 631–648 — doi:10.1016/j.matt.2019.12.019, PNNL record; Lee, Smith & Arshad 2023, Phys. Fluids — arXiv:2206.12373; Moroney et al. 2015, Chem. Eng. Sci. 137, 216–234, doi:10.1016/j.ces.2015.06.003; Mo et al. 2023 — PMC10541431.

Q8Web runtime — CoolProp 7.2.0 vs 8.0.0, stlite 1.12
CoolProp: same water formulation, different builds — agreement expected, not proven. "Pyodide 314" is real (Pyodide now tracks Python versioning; stlite 1.11.0 moved the runtime from Pyodide 0.29.3 to 314.0.3, Python 3.13 → 3.14). Under Pyodide 314 the bundled CoolProp is 7.2.0, and a default install serves that, not 8.0.0. CoolProp's own docs note that from 8.1.0, WebAssembly wheels are on PyPI and a micropip request for CoolProp>=8.1.0 overrides the bundled version — note this sits awkwardly with the earlier finding that PyPI's latest was 8.0.0 with no emscripten wheel; treat the 8.1 route as to be tested in the spike, not as settled. For water, both 7.2.0 and 8.0.0 implement the same IAPWS-95 EOS (Wagner & Pruss 2002) with the same IAPWS viscosity (Huber et al. 2009) and conductivity (Huber et al. 2012) formulations, and the 8.0.0 changelog lists no water-EOS change (its breaking changes are API-level: Props/HAProps removed, AbstractState reworked). But no side-by-side numeric comparison was found or run — solver tolerances and saturation routines could shift last digits. Run both at your actual state points (ρ, μ, cp, h at 20 °C and 90–95 °C, 1 atm) and report the measured difference; and never compare the IF97 backend against HEOS numbers and call the gap a version difference.

stlite 1.12: no known stlite-1.12-specific bug for st.segmented_control or Plotly was found. segmented_control arrived in Streamlit 1.40 and was ported in stlite 0.73.0; the only failure found was an old version-pinning issue. The known Plotly issue (#1302, "can't find a pure Python 3 wheel") predates Pyodide 314. Two cautions from stlite 1.11.0 that carry forward: Pyodide 314 needs module workers (Firefox <114 cannot run it), and dataframe serialisation moved to pyarrow/Arrow IPC, which is the path st.plotly_chart depends on. Keep a Matplotlib fallback (st.pyplot; Matplotlib is explicitly bundled in Pyodide 314).

Sources: CoolProp Python/Pyodide docs — coolprop.sourceforge.net; CoolProp water (7.2.0) — coolprop.github.io; CoolProp 8.0.0 changelog — coolprop.org/coolprop/changelog.html; stlite changelog (to 1.11.0) — github.com/whitphx/stlite; stlite issue #1302 — github.com/whitphx/stlite/issues/1302. Could not verify the contents of stlite 1.12.0 (the changelog snapshot accessed stops at 1.11.0), Plotly working under stlite 1.12 / Pyodide 314, or any numeric 7.2.0-vs-8.0.0 water comparison.

Q9YouTube — comment limit and auto-caption timing
Comment limit: 10,000 characters — consistently reported and API-enforced (the API returns a "comment text too long" error), but YouTube's Help Centre does not publish a comment-length figure (it publishes title 100 and description 5,000). Cite it exactly that way on the site: "limited to 10,000 characters (widely reported; enforced by the API, though not published by YouTube)." Practical notes for the numbered-comments plan: long comments collapse behind "Read more," and some Unicode/emoji count as two UTF-16 units — so split with headroom, not at exactly 10,000.

Auto-captions: YouTube gives no fixed time. Its Help Centre says only that automatic captions "may not be ready at the time that you upload" and that processing "depends on the complexity of the video's audio." Practitioner reports put a short, clear video at typically 5–30 minutes after processing completes, occasionally a few hours; UC Berkeley's accessibility guide allows several minutes to 24 hours. For a 7–8 minute clear-English video, plan on usually well under an hour but allow up to 24 h before treating it as failed — which is what the ≥48 h upload buffer in §6 is for. Set the video language to English in Studio first, upload unlisted, and check the Subtitles panel for the "(auto-generated)" track. If timing ever matters more than the verbatim requirement, uploading your own SRT is the reliable route — but it is not a substitute for Req 3, as already decided.

Source: YouTube Help, "Use automatic captioning" — support.google.com/youtube/answer/6373554 (no fixed time given). Comment limit: widely reported secondary sources and the YouTube Community forum (Feb 2024), per the research report §9. Could not verify the 10,000 figure from any official YouTube page.

Q10Teaching angle — what a professor expects about Ergun's limits
The defensible student conclusion, per the research: Ergun is a semi-empirical fit, not a derived law. Its constants are regression constants for near-spherical, rigid, monodisperse packings; coffee violates every one of those adjectives. A factor-of-2–3 error is a successful Ergun prediction for coffee; 10% agreement would be luck or tuning. The experiment's job is to measure the effective constants for your bed and Δp range and show how far — and why — they drift from 150/1.75. Sensitivity dominates reporting precision: k ∝ d²ε³/(1−ε)², so a 20% error in d32 is a 44% error in k, and ε = 0.35 vs 0.45 changes k ≈2.5×. And a fit at one grind size does not extrapolate to another, because the mechanism changes (fines migration, channeling, inertial effects).

Verified literature phrasings you can quote: the 2015 revisit (Powder Technology 283) — Ergun "should not be used above Rem ≈ 500," and among the many packed-bed correlations "there appears to be no general agreement regarding which correlation is the most accurate." Du Plessis (2008, pore-scale derivation): strictly, the equation applies only for porosities 0.38–0.47 and only for Newtonian fluids. Ergun (1952) himself assumed a column of effectively infinite diameter relative to the particles — no wall effects; a 2011 wall-effect paper concludes Ergun predictions "would differ significantly from measurements" for D/d ≲ 40. Coulson & Richardson's hedge on 150 vs 180 — "probably due to differences in shape and packing of the particles" — is a good model sentence for how textbooks treat fitted constants.

Could not verify the exact wording of Bird–Stewart–Lightfoot, Cengel & Cimbala, or Munson on Ergun's limits — textbook text is not freely indexed at that granularity, and the research quotes none of them. If the site needs a verbatim textbook line, take it from a library copy of the edition your course uses, with the page number. What is verified about BSL is the factor-of-3 friction-factor definition in Q6 — itself a good exam-style illustration of why definitions travel in pairs.

Task 3 · §6 of the briefing
Verdicts on the accepted and rejected suggestions
Most of §6 stands — the demo order, the claim labels (in their final wording: Compared with experimental data / Model-predicted / Illustrative), the frozen comparison protocol, and the two freezes are all sound. The disagreements below are the exceptions, per your instruction not to repeat points already in §6 unless I disagree with them.

Accepted, but a mistake as specified: the 1e-9 explorer check as the headline verification Disagree in part
§6.1 accepts an exact match (rtol 1e-9 plus per-output atol) between the static explorer and physics.plunge. But the explorer's values are precomputed by that same code — so the check verifies transcription and rounding, not correctness, and presenting it as the explorer's main verification invites the grader's question "verified against what?" Keep the check (it is a good regression guard, and the later decisions correctly add that the slider only snaps to the precomputed grid, with an atol for near-zero outputs) — but demote it in the write-up to "no transcription error," and let the experimental comparison carry the word "verification."

Accepted, but a mistake: freezing hidden test inputs at 455 and 735 µm without freezing the fines fraction there Disagree in part
§6.5 accepts hidden inputs at 300, 455, 500, 735, 800, 1000, 1200 µm "at 341 K and two other temperatures." At off-grid grinds the expected outputs depend entirely on how wf behaves between the named grinds — and per finding 5, measured fines fractions vary with grind while the model holds wf fixed. If the frozen spec doesn't state the fines rule (fixed 15%? interpolated? measured?) and name the two other temperatures, implementers are being scored against an unstated convention, and a "failure" may be a spec gap, not a model error. Freeze the fines rule and the temperatures in the same commit as the test hash.

Accepted, but risky: the 0.1% CoolProp gate stated before any measurement exists Disagree in part
§6.1 accepts "water ρ, μ, cp within 0.1%" as the CoolProp test under Pyodide 314. Q8: the two versions share the IAPWS-95 formulation and no numeric comparison has ever been run or found. A hard 0.1% gate risks failing the spike on a solver-tolerance technicality — or worse, being quietly relaxed later, which reads badly in the records. Restate it as a measurement to report (with the measured max relative difference across 20–100 °C published either way), and gate the spike only on the downstream criterion already accepted elsewhere: headline TDS/EY/Δp moving by less than the 0.5% tolerance.

Accepted, with a condition: seeded Lab-notebook batches Disagree in part
Seeding fixes the empty first-open problem, and the accepted version labels them "example batches (simulated)." The condition: in a browser build where session state evaporates, seeded batches are also the only batches most visitors will ever see — so the label must survive next to every seeded row in the UI itself, not only in documentation, or the demo's most-seen data is simulator output wearing a lab notebook's clothes. Given the claim-label system you adopted, hold the notebook to it.

Rejected, and should come back in reduced form: browser persistence Bring back
§6.1 rejects IndexedDB persistence as "risk with little gain." Full persistence, agreed — but the stlite demo's Lab notebook losing every batch on reload is a real demo defect (finding: visitors see either seeded data or nothing). Bring back the narrow version already implied by the demo's needs: an export/download of the batch log (and import, if cheap), with no promise of stored state. That is a one-afternoon feature, it makes the notebook demonstrably usable during a live presentation, and it does not commit you to a storage story.

Rejected, and should stay rejected — but with its trigger stated: the Rust/WASM calculator Keep rejected
"Not chosen: second codebase" is the right call while the static explorer exists — the explorer already fills the instant, dependable slot the course example occupies. But §6 records no condition under which this returns. State the trigger now, while it's cheap: if the stlite spike fails and the static explorer proves too limited in rehearsal, a single-purpose WASM Ergun calculator becomes the fallback — not before. A rejected option with a named trigger reads as engineering judgement; without one it reads as taste.

Task 4 · New — not in §6
Five improvements for this professor's framing
Make the headline figure a log–log fp vs Reb collapse plot — Ergun line, your operating band (Reb ≈ 0.8–1.1), and the Corrochano-implied points on the same axes — because it makes dimensional analysis, not coffee, the visual centrepiece, exactly as the framing orders it.
Publish a cross-study permeability parity plot (predicted vs measured K for Gianino, King, Navarini, Corrochano, and Mo, coded by overpressure) — because it turns four scattered literature numbers into one figure that shows when Ergun fails, which is the lesson empirical-correlation limits are meant to teach.
Show the Buckingham Pi derivation as a dimensional matrix with its null space, not just the answer — because the professor put dimensional analysis in the framing before Ergun, and exhibiting the rank/null-space step is the part of the method a grader cannot get from the final groups alone.
Take one blind measurement: predict plunge force for a grind the model wasn't tuned on, then measure it (kitchen scale under the press, or the syringe permeameter) — because Q5 shows no published plunge-force data exists, so a single honest measured point converts your weakest claim label into your only first-hand Compared with experimental data result.
Report Ceff as a curve against D/dp (and Reb), not just a range of 280–2400 — because a fitted constant that drifts systematically with a dimensionless group is a publishable-style finding about which Ergun assumption breaks first, and it sets up the wall-effect explanation your coarse-grind gap needs.
One derived number worth memorising for the Q&A
The viscous and inertial Ergun terms are equal at Reb = 150/1.75 ≈ 86. Your bed runs at Reb ≈ 1 — two orders of magnitude into the viscous regime. If the professor asks "why not just Darcy?", the answer is: at the operating point you nearly can (inertial share ≈ 1%), and Ergun is retained because the comparison task, the fine-grind end, and the course framing all require showing where the second term would switch on.

Marked plainly
What could not be verified
Corrochano et al. (2015) primary text — paywalled. Its porosity range, the exact modified-Kozeny–Carman formula (72 vs 36 denominator; λp = 7.5), and any Ergun-constant discussion are not primary-verified. This includes the briefing §7's "wet beds at 0.12–0.33" — do not attribute that range to Corrochano. Read the paper via the library before quoting it.
French-press fines fraction by mass — not found anywhere. Only Mo et al.'s volume fractions <100 µm (9.7–29.2%, espresso-to-filter).
Wet French-press cake porosity — no published value found.
Low-pressure wet-bed consolidation — no French-press-range measurement found.
Fines skin thickness or mass in any brewer; any French-press fines-migration study — not found.
French-press plunge force vs grind size — no scientific measurement found; only an unsourced 15–20 lb blog claim.
Quantitative channeling in immersion/press beds — not found; all quantitative evidence is espresso.
CoolProp 7.2.0 vs 8.0.0 numeric equality for water — expected (same IAPWS-95), never measured or published.
stlite 1.12.0 changelog contents; Plotly under stlite 1.12 / Pyodide 314 — not verified; no 1.12-specific bug found, but absence of a bug report is not proof it works.
YouTube's 10,000-character comment limit as an official figure — not published by YouTube; widely reported and API-enforced.
Auto-caption timing for any specific video — YouTube gives no fixed time; ranges are practitioner reports.
Verbatim textbook wording (Bird–Stewart–Lightfoot / Cengel / Munson) on Ergun's limits — not verified; nothing from those books is quoted in this briefing.
Attribution
Sources
Primary research: the deep-research report on this project's §8 questions (primary sources where accessible, read 5 Nov 2026), including its per-source notes. Project facts, model numbers, and the §6 suggestion record: the master briefing compiled 2026-11-05 by Claude Opus 5.5 (plans v1–v5 and the Muse, ChatGPT, and Grok critiques), against the public repo at commit a8b24b6. Recomputations in §1 of this page were done from the briefing's stated model during this review.

Ergun, S. (1952). Fluid flow through packed columns. Chem. Eng. Prog. 48, 89–94.
Corrochano, B. R. et al. (2015). A new methodology to estimate the steady-state permeability of roast and ground coffee in packed beds. J. Food Eng. 150, 106–116. doi:10.1016/j.jfoodeng.2014.11.006
Mo, C. et al. (2023). Exploring the link between coffee matrix microstructure and flow properties using combined X-ray microtomography and SPH simulations. Sci. Rep. 13, 15970. PMC10541431
Uman, E. et al. (2016). The effect of bean origin and temperature on grinding roasted coffee. Sci. Rep. 6, 24483. PMC4834475
Cameron, M. I. et al. (2020). Systematically improving espresso. Matter 2(3), 631–648. doi:10.1016/j.matt.2019.12.019
Moroney, K. M. et al. (2015). Modelling of coffee extraction during brewing using multiscale methods. Chem. Eng. Sci. 137, 216–234. doi:10.1016/j.ces.2015.06.003
Hargarten, V. B., Kuhn, M. & Briesen, H. (2020). Swelling properties of roasted coffee particles. J. Sci. Food Agric. 100(10), 3960–3970. doi:10.1002/jsfa.10440
Maille, M. J. et al. (2021). Critical examination of particle swelling during wetting of ground coffee. J. Food Eng. doi:10.1016/j.jfoodeng.2020.110420
Gianino, C. (2007). Experimental analysis of the Italian coffee pot "moka". Am. J. Phys. 75(1), 43–47. doi:10.1119/1.2358157 · King, W. D. (2008). Am. J. Phys. 76(6), 558–565 · Navarini, L. et al. (2009). Appl. Therm. Eng. 29, 998–1004. doi:10.1016/j.applthermaleng.2008.05.014
Fasano, A., Talamucci, F. & Petracco, M. (2000). The Espresso Coffee Problem. doi:10.1007/978-1-4612-1348-2_8 · Ellero, M. & Navarini, L. (2019). J. Food Eng. doi:10.1016/j.jfoodeng.2019.05.038 · Lee, W. T., Smith, A. & Arshad, A. (2023). Phys. Fluids; arXiv:2206.12373
Smrke, S., Eiermann, A. & Yeretzian, C. (2024). The role of fines in espresso extraction dynamics. Sci. Rep. 14, 5612. doi:10.1038/s41598-024-55831-x · Breard, E. C. P. et al. (2019). J. Geophys. Res. Solid Earth. doi:10.1029/2018JB016544 · Duda, J. L. et al. (2002). Chem. Eng. Sci. 57, 527–534
"A revisit of pressure drop–flow rate correlations for packed beds of spheres" (2015). Powder Technol. 283, 488–504. ScienceDirect
CoolProp: 8.0.0 changelog · Water, 7.2.0 docs · Pyodide wrapper docs · stlite: changelog, issue #1302 · YouTube Help: automatic captioning Your research page is ready above — it answers all five asks from the master briefing, with the full citations and a dedicated “what could not be verified” section.
Physics check first: the algebra is right, the table recomputes, and three numbers don't line up
The Ergun form and Pi groups are correct — f_p = 150/Re_b + 1.75 with your (f_p, Re_b) pair is algebraically identical to Ergun 1952, and I recomputed the grind sweep from your fines model and got every permeability to the printed digits: K goes 1.09×10⁻¹¹ at 300 µm to 2.05×10⁻¹¹ m² at 1200 µm, because the 15% fines dominate d₃₂.
But a grader will spot these: your force numbers imply a press diameter of 8.50 cm, not the 8.0 cm / 50.5 cm² in the live app — at 800 µm that’s 2.72 N on 56.8 cm², versus 2.42 N on the app’s area. Porosity ε = 0.40 is assumed, and the “Corrochano 0.12–0.33” wet range quoted in §7 could not be verified in the primary paper, which is paywalled — don’t quote it without reading it. And cake length and porosity are treated as independent in the briefing when they’re linked through true density and dose, so a sensitivity run over ε alone understates the coupling.
The ten research questions, in brief

1. Ergun constants for coffee: no coffee study fits an Ergun viscous constant to replace 150/180. Corrochano et al. 2015, J. Food Eng. 150, 106–116, fits a modified Kozeny–Carman correlation, not Ergun, with k = 2.59×10⁻¹⁴–3.36×10⁻¹³ m². Nearest low-pressure analogues are moka: Gianino 2007, 2.3×10⁻¹² m² at ~0.01 bar, and King 2008, 8.98×10⁻¹³ m².
2. Fines / d₃₂: d₃₂ is the theoretically correct diameter — it preserves surface area, S = 6/d₃₂ — and Corrochano uses it, but it’s not sufficient alone for a bimodal, non-spherical, migrating fines population. Uman et al. 2016, Sci. Rep. 6, 24483, proves bimodality but gives no French-press fines mass fraction. Best proxy: Mo et al. 2023, Sci. Rep. 13, 15970 — 9.7% by volume <100 µm for the coarsest powder, versus 29.2% for espresso.
3. Porosity / swelling: no wet French-press porosity was found — don’t quote one. Mo’s espresso capsules are ε ≈ 0.13–0.24. Swelling is genuinely contested: Hargarten et al. 2020 reports ~15% diameter (~52% volume) swelling, Maille et al. 2021 reports no significant swelling.
4. Fines migration: real in espresso — Fasano et al. 2000 flow-reversal, Ellero & Navarini 2019 modelling — but no skin thickness is quantified, none for French press, and it predicts the wrong sign: fines fraction falls as grind coarsens, so a skin should weaken, not strengthen, with coarseness.
5. Plunge force: no scientific measurement found. Only an unsourced blog claim of 15–20 lb — don’t cite it as data. Your own force-vs-grind curve would be novel.
6. Dimensional analysis: your code form is Ergun 1952. Other textbooks put (1−ε) in f instead of Re, and Bird–Stewart–Lightfoot’s f is f_k/3 — always quote the (f, Re) pair together, or the 150/1.75 constants are wrong by that factor.
7. Channeling: quantitative evidence is espresso only — Cameron et al. 2020, Matter 2, 631–648, yield peaks then falls at fine grind; Lee et al. 2023 two-path model; Mo et al. permeability varying 0 to 66.6×10⁻¹³ m² within one bed. No French-press quantification found.
8. Web runtime: Pyodide 314 bundles CoolProp 7.2.0, not 8.0.0; to get newer you need micropip `CoolProp>=8.1.0` for the wasm wheels. Both use the same IAPWS-95 water formulation, so agreement is expected, but no numeric 7.2-vs-8.0 comparison was found — don’t claim bit-identical. No stlite 1.12-specific `segmented_control` or Plotly bug was found; `segmented_control` was ported in stlite 0.73.0.
9. YouTube: comment limit is 10,000 characters, widely reported and API-enforced, but YouTube Help doesn’t publish it. Auto-captions have no fixed time from YouTube — typically 5–30 minutes, up to a few hours, allow 24 hours.
10. Teaching angle: Ergun is semi-empirical, fitted, not derived — expect a factor-of-2–3 error for coffee to count as success, not 10%. The 2015 revisit says don’t use it above Re_m ≈ 500, and du Plessis notes it strictly applies only for porosities 0.38–0.47 in its original calibration. Verbatim BSL/Cengel/Munson wording could not be verified, so the page doesn’t quote any.

Section 6 — where I disagree, in part
Four accepted suggestions are challenged in part on the page: the 1e-9 check framing, the hidden-test fines rule at 455/735 µm, the unmeasured 0.1% CoolProp gate, and the seeded notebook labelling. Browser persistence, which was rejected, should come back in reduced form as an export, not IndexedDB. The Rust/WASM rejection stands, but with a trigger for revisiting it.
Five improvements that would most impress your professor

1. Add an f_p–Re_b collapse plot with your data and Corrochano’s points on it — Reason: it tests the dimensional analysis itself, not just the Δp numbers.
2. Add a cross-study parity plot, predicted vs measured permeability for Corrochano, Gianino, King, and Navarini — Reason: it makes the 1.9–16× disagreement visual instead of a sentence.
3. Show the Buckingham-Pi derivation as a dimensional matrix, not just the resulting groups — Reason: that’s the part a fluids professor grades, and it proves the groups are dimensionless.
4. Do one blind plunge-force measurement, sieved vs unsieved grind at the same d₃₂ — Reason: it’s the only direct experimental check in the project, and no literature value exists to compare against.
5. Plot the fitted C_eff against D/d_p across grind sizes — Reason: it turns “Ergun disagrees” into a testable hypothesis about wall effects versus fines migration.

The page also has an interactive slider that recomputes d₃₂, d_s, and K from your stated formulas — at 800 µm it shows d₃₂ 164.9 µm, d_s 123.7 µm, K 1.81×10⁻¹¹ m² — plus the sweep charts and the full source list.