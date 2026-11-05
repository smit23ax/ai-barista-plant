# AI Barista Plant (trimmed core): the simplifying assumptions that make it undergraduate-solvable

**Short answer for your professor:** yes. Every unit uses one or two limiting assumptions that turn a hard problem (3-D, turbulent, multi-phase, a distribution of particle sizes) into an equation from our courses: a force balance, Darcy's law, or an ordinary differential equation from a material or energy balance. The computer then does the quantitative part: it solves those equations numerically, runs thousands of virtual batches, and fits the model to published data. Each assumption is checked with a number the app computes. If an assumption breaks, the code raises an error instead of quietly returning a wrong answer.

Numbers below are for the standard recipe: 800 µm grind, 93 °C water, 4 min steep, 15 g coffee in 250 g water.

---

## 1. Plant-wide assumptions

| Assumption | What it buys you | How we know it's OK |
|---|---|---|
| Water properties (ρ, μ, cₚ) from IAPWS-95 via CoolProp, as functions of T only | No typed-in property values; liquid is incompressible | Pressures are close to 1 atm; the code raises an error outside 0–100 °C |
| Brewed coffee has water's density and viscosity | One fluid, not a solution with changing properties | TDS is only about 1.1 %, so the solution is dilute |
| One grind size per batch (not a size distribution), except for a fines fraction in the filter | A single diameter d sets every time scale | Disclosed limitation; a distribution is listed as future work |

## 2. R-101 press: extraction (material balance)

- **Assumptions:**
  - The liquid is **well mixed** (one bulk concentration c).
  - Solubles sit in **two pools**: fast (on broken cell surfaces) and slow (inside the grains).
  - Each pool empties with a **first-order (linear) rate**, so a diffusion PDE inside each grain becomes a single time constant (the lumped "two-pool" model of Moroney et al. 2016).
  - Time constants scale with grain size (τ_diffusion ∝ d², τ_surface ∝ d³) and with temperature through Stokes–Einstein (D ∝ T/μ).
- **Reduces to:** three coupled first-order ODEs (surface pool, in-grain pool, dissolved coffee) that add up to zero, so mass is conserved exactly.
- **Computational part:** solved numerically (scipy solve_ivp) because the equations are coupled and the temperature changes during the brew.
- **Check:** the mass balance closes to about 1×10⁻¹⁵. The time constants are τ_surface ≈ 22 s and τ_diffusion ≈ 320 s at this grind, consistent with Moroney's coarse-grind values (19 s and 270 s).

## 3. Cooling (energy balance)

- **Assumptions:**
  - **Adiabatic mixing** at t = 0 (kettle water, cold grounds, cold glass reach one temperature instantly).
  - Then a **lumped-capacitance** brew (one uniform temperature) losing heat with a constant UA.
  - Heat of dissolution is neglected.
- **Reduces to:** one algebraic mixing balance, then C dT/dt = −UA (T − T_ambient), which integrates to an exponential decay.
- **Check:** the brew starts at 76.5 °C and is at 67.7 °C after 4 minutes. The time constant C/UA is about 23 min. UA is an assumed value, and that's disclosed.

## 4. F-101 plunger filter (flow through the grounds)

- **Assumptions:**
  - **Creeping (Darcy) flow** through the packed bed of grounds.
  - Permeability from **Kozeny–Carman**: pores are treated as small Hagen–Poiseuille tubes.
  - The bed and the mesh are **resistances in series**.
  - The Sauter mean diameter accounts for fines.
- **Reduces to:** ΔP = μuL/k for the bed plus the mesh term. Force = ΔP × plunger area.
- **Check:** the pore Reynolds number is ≈ 0.9, inside Darcy's range (below about 1 to 10). Honest caveat: Kozeny–Carman over-predicts coffee-bed permeability by about 1.3–6 times (Corrochano 2015), so the plunge force (≈ 2 N) is an estimate.

## 5. T-101 cup: fines settling (Stokes' law)

- **Assumptions:** fines are **rigid spheres** (30 µm, water-filled), in **creeping flow**, far from walls and from each other (dilute).
- **Reduces to:** a force balance: weight − buoyancy − drag = 0 at terminal velocity, so v = (ρ_p − ρ) g d² / (18μ).
- **Check:** at the end-of-brew temperature (≈ 68 °C) the particle Reynolds number is ≈ 0.014, well below the 0.1 limit. The settling time through the cup is ≈ 7 min. The app flags any case where Re_p > 0.1.

## 6. The AI operator

- **Assumptions:**
  - Strength (TDS) and extraction (EY) are modelled as **independent** Gaussian processes.
  - The meter has Gaussian noise (σ_TDS = 0.03 %).
  - Setpoints are rounded to real dial steps.
- **Computational part:** fit 2 GPs, score 3000 candidate recipes by their probability of landing in the ideal box, and benchmark over 20 random seeds against one-factor-at-a-time and random recipes.
- **Result (best found, not proof of optimality):** the AI succeeded in 20/20 runs (median 7 batches), one-at-a-time in 6/20 and random in 8/20.

## 7. Calibration (being built now)

- **Assumptions:** Moroney's measured extraction curve (Fig. 5a, a drip-filter fine grind) is used to fit the two time constants by least squares, with error bars from the parameter covariance. It isn't a French press, and the app says so.

---

## The one-paragraph version to say out loud

"A real coffee brew is a 3-D, multi-phase problem with a distribution of particle sizes. I made it solvable with the same assumptions we use in class: a well-mixed tank with lumped first-order mass transfer, lumped-capacitance cooling, and creeping flow for Darcy's law and Stokes' law. Each one turns the physics into a force balance, an energy balance or an ODE. The computer solves those, checks every assumption with a dimensionless number like the Reynolds number, and then an AI uses the model to find the best recipe with as few experiments as possible."
