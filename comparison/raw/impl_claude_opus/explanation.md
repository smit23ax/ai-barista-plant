<!-- Explanation task, Claude Opus 5.5, fresh session with no tools used and no project context, 2026-11-10. Prompt: comparison/task/EXPLANATION_PROMPT.md. Reply below is unedited. -->

Ergun equation vs. coffee-bed permeability

**The model and its symbols.** The Ergun equation gives the pressure gradient across a packed bed:

−ΔP/L = 150 μ (1−ε)² U / (ε³ d²) + 1.75 ρ (1−ε) U² / (ε³ d)

The symbols are:
- ΔP: pressure change across the bed (Pa)
- L: bed depth in the flow direction (m)
- μ: dynamic viscosity of the liquid (Pa·s)
- ρ: liquid density (kg/m³)
- U: superficial velocity, the volumetric flow rate divided by the empty cross-section (m/s)
- ε: interparticle void fraction, meaning the open space between particles (dimensionless)
- d: equivalent particle diameter (m), properly d = ψ·d_v, where ψ is sphericity (dimensionless) and d_v is the diameter of a sphere with the same volume as the particle (m). Equivalently, d = 6/a_v, where a_v is particle surface area per unit particle volume (m⁻¹).

Darcy's law, −ΔP/L = μU/k, defines the permeability k (m²). When only the viscous term matters, Ergun predicts k = ε³d² / [150 (1−ε)²].

That condition holds in espresso. Take U ≈ 1×10⁻³ m/s, d ≈ 3×10⁻⁴ m and μ ≈ 3×10⁻⁴ Pa·s (water near 90 °C). The particle Reynolds number is then Re_p = ρUd/[μ(1−ε)], which is about 1–2. The inertial term is roughly 1.75·Re_p/150, or about 1–2% of the viscous term. So the constant 1.75 hardly matters, and the disagreement comes from the viscous term and its inputs.

The 150 was fitted to data for fairly uniform, rigid, non-porous particles at ε ≈ 0.35–0.5. A coffee bed differs from that in almost every respect. The predicted k scales as d² and as ε³/(1−ε)². That means modest errors in d or ε grow into the factor-of-2-to-50 errors reported.

**Explanations that rest on measurements or simple arithmetic.**

1. **Particle size distribution.** Laser diffraction studies show that coffee grinds are broad and usually bimodal. They contain a "fines" population of roughly 10–50 µm alongside coarse particles of a few hundred µm. Flow resistance depends on surface area, so the right d is the surface-weighted (Sauter) mean, multiplied by ψ. The fines dominate a_v while making up little of the volume. If d is taken as the volume median d₅₀, it can easily be 2–4 times too large, and k then comes out 4–16 times too large. This is plain arithmetic, but how much of any given discrepancy it accounts for depends on which d the study actually used.
2. **Shape.** Ground fragments are angular and flaky, with ψ well below 1. Using a sieve or diffraction size without ψ overstates d.
3. **Viscosity.** Water viscosity drops from about 1.0×10⁻³ Pa·s at 20 °C to about 0.31×10⁻³ Pa·s at 90 °C, and dissolved solids raise it a little. Comparing predictions and data at mismatched μ produces an error of up to about 3. These are tabulated property data, not hypotheses.
4. **Channelling cannot be the cause.** Preferential flow paths make the measured k *higher* than a uniform-bed prediction. They therefore cannot explain an Ergun *over*-prediction.

**Explanations that are hypotheses or only partly measured.**

1. **Porosity is not what was assumed.** Roasted coffee particles are porous inside (cellular structure), and they absorb water and swell when wetted. If ε is computed from bulk density and true density, it includes internal pores that do not carry flow. Swelling then shrinks the true interparticle ε further. Swelling and internal porosity have been observed, but their size during an actual brew is not well quantified. Because k ∝ ε³/(1−ε)², an error in ε from 0.40 to 0.30 alone changes k by about 2.6 times.
2. **Fines migration.** Fines may be carried downstream and pack against the basket or filter, forming a thin, low-permeability layer that controls the overall resistance. Flow rates that fall during a shot, and fines found at the bed exit, support this. Direct measurements of the resistance profile through the bed are scarce.
3. **Compaction under flow.** Tamping and a 9 bar pressure gradient may consolidate the bed unevenly, giving lower ε near the outlet. This is plausible, but evidence for it is mainly indirect.
4. **Gas and dissolution.** Freshly roasted coffee releases CO₂, and bubbles may block pores. About 20% of the mass dissolves, which changes particle size and ε over time. Both are hypothesised to change k, and both work in time-dependent directions.

**Why the French press differs so much.** A French press is not a packed bed with a known ε. When the plunger is pushed down, the grounds are compressed against the mesh into a filter cake. That cake is likely enriched in fines and much denser than the bulk grind. The mesh itself adds resistance. Inputs taken from the loose grind would then over-predict k badly, which is consistent with about 48 times. That reading is my interpretation, not something I can confirm the cited study measured.

**What to take away.** The Ergun constants are not "wrong". The equation's inputs (d, ψ, ε and μ) are hard to define and measure for a polydisperse, porous, swelling, deformable, partly dissolving solid. The discrepancy is mostly about characterising the bed, not about the form of the equation. I can't confirm which of these mechanisms each cited study tested directly. Check its methods before treating any one of them as the established cause.

---

## Score (RUBRIC.md): 9 / 10

| Criterion | Points | Note |
|---|---|---|
| Correct physics | 4 / 4 | Size distribution and fines, shape, porosity and swelling, compaction, and constants fitted to uniform rigid beds are all covered |
| Symbols with SI units | 2 / 2 | All defined with units |
| Uses the given numbers correctly | 1 / 2 | "ε from 0.40 to 0.30 changes k by about 2.6 times" is wrong: ε³/(1−ε)² gives 3.2 times |
| Established vs hypothesised | 2 / 2 | Two explicit lists, and it says it cannot confirm what each study tested |
