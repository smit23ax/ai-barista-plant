# Frozen implementation task (paste this whole file, plus public_examples.json, into a NEW chat)

Rules for the person running it: use a brand-new chat with no earlier messages or uploaded files; paste this file and
`public_examples.json` and nothing else. You may send at most two follow-up messages, and only these exact ones:
"Please fix any errors and give the complete final files again." Save each model reply unedited.

---

You are writing a small, tested Python module for a chemical engineering course on flow through packed beds.
Write clear, minimal code (numpy, scipy, CoolProp, plotly allowed; no classes). Define every symbol with SI units in
docstrings and comments.

## Physical situation
A French press plunger pushes liquid through the wet cake of coffee grounds under it. The cake is a packed bed.
Compute the fluid resistance (only) of the cake plus the mesh filter.

## Function to write: `plunge(d, T, m_coffee=0.015, plunge_time=20.0, fines_fraction=0.15, D_press=0.085, eps_bed=0.40, rho_bulk=400.0, R_mesh=2.0e8, V_liquid=2.3e-4, sphericity=0.75)`
Inputs (SI): nominal grind diameter d (m); temperature T (K); dry coffee mass m_coffee (kg); plunge time (s);
fines mass fraction (-); press inner diameter D_press (m); bed porosity eps_bed (-); cake bulk density rho_bulk (kg/m^3);
mesh resistance R_mesh (1/m); liquid volume pushed through V_liquid (m^3); particle sphericity (-).

Conventions (follow exactly):
1. Water density rho (kg/m^3) and viscosity mu (Pa s) at T and 101325 Pa from CoolProp, fluid "Water" (IAPWS-95).
2. Fines are single particles of diameter d_f = 30e-6 m. Sauter mean diameter: 1/d32 = w_f/d_f + (1 - w_f)/d.
3. Effective (Ergun) particle diameter: d_s = sphericity * d32.
4. Area A = pi D_press^2 / 4; cake thickness L_cake = m_coffee / (rho_bulk A); superficial velocity u = V_liquid / (A plunge_time).
5. Ergun: dP/L = 150 mu (1-eps)^2 u / (eps^3 d_s^2) + 1.75 rho (1-eps) u^2 / (eps^3 d_s).
6. Cake pressure drop dP_cake = (dP/L) L_cake; mesh dP_mesh = mu u R_mesh; total dP = dP_cake + dP_mesh; force = dP A.
7. Permeability (viscous limit) k = d_s^2 eps^3 / (150 (1-eps)^2).
8. Bed Reynolds number Re_b = rho u d_s / (mu (1-eps)); friction factor f_p = (dP/L) d_s eps^3 / (rho u^2 (1-eps)).
9. inertial_share = inertial part of dP/L divided by total dP/L (cake only).

Return a dict with keys: k, dP, dP_cake, dP_mesh, force, Re_b, f_p, inertial_share, d32, d_s, L_cake, u
(all floats, SI units). Raise ValueError for non-physical inputs (T outside 273.16-373 K, d <= 0, eps_bed outside (0, 1)).

Results must be computed from the equations at run time. Do not hard-code or look up output values.

## Also write
- `test_ergun_plunge.py` (pytest): reproduce both cases in public_examples.json to rtol 1e-6, check f_p == 150/Re_b + 1.75,
  and check the limits (inertial_share -> 0 as u -> 0).
- `sweep_page.py`: writes `sweep.html`, a plotly page of k, dP and force against grind size 300-1200 um at T = 341 K,
  readable at 1400 px and 390 px wide (legend outside the plot, labelled axes with units).

Give the three complete files.
