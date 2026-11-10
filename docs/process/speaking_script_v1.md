# AI Barista Plant: speaking script (about 7½ minutes)

Speak at a normal pace (about 140 words a minute). The **Screen** line tells you what to show in the app's **Presenter** view (unit, then step number). Press **⏱ Start timer** at the beginning. Each "Write" means: write that equation by hand (or point to it on screen) while you say the line.

| Time | Section | Screen |
|---|---|---|
| 0:00 | 1. Hook | Plant view |
| 0:40 | 2. The plant and its degrees of freedom | Plant overview & DOF, steps 1–6 |
| 1:30 | 3. Extraction material balance (hero 1) | Extraction balance, steps 1–10 |
| 3:30 | 4. Plunge filtration, Darcy's law (hero 2) | Plunge filtration, steps 1–7 |
| 4:45 | 5. Stokes settling (hero 3) | Stokes settling, steps 1–13 |
| 5:50 | 6. Energy balance in 30 seconds | Energy balance, steps 1–5 |
| 6:20 | 7. The AI operator and a live race | AI operator steps, then the AI operator view |
| 7:15 | 8. Honesty and close | Engineering notes view |

---

## 1. Hook (0:00 – 0:40) · Screen: Plant view

"Every morning, millions of people run a small chemical plant without realising it. Hot water flows through a packed bed of particles, solids dissolve, heat is lost to the room, and the product has to meet a quality spec. That's a cup of coffee.

I modelled a French press as a plant, using the same tools we use in this course: force balances, material and energy balances, Darcy's law and Stokes' law. Then I built an AI operator that finds the best recipe in as few experiments as possible."

## 2. The plant and its degrees of freedom (0:40 – 1:30) · Screen: Plant overview & DOF

- **Step 1.** "Kettle, press, filter, cup. Each unit has one main equation."
- **Steps 2–4.** "The product spec has two numbers. Strength, TDS, is the dissolved mass over the drink mass, and the target is 1.15 to 1.35 percent. Extraction yield, EY, is the same dissolved mass over the dry coffee, 18 to 22 percent. Dividing one by the other, EY equals TDS times drink mass over coffee mass. That's how you measure EY with a TDS meter and a scale."
- **Steps 5–6.** "Degrees of freedom equal variables minus independent equations. With the dose fixed, four are left: grind size, water temperature, steep time and brew ratio. Those four dials are what a human or the AI has to choose."

## 3. Extraction material balance (1:30 – 3:30) · Screen: Extraction balance

- **Step 1.** "Only about 30 percent of roasted coffee can dissolve. Grinding breaks the cells at the surface of each grain. Those solubles dissolve fast, and I call that pool F. The rest is locked inside the grain and has to diffuse out. That's pool S."
- **Step 2.** "The fast fraction is the volume of a shell one cell thick, 30 micrometres, around a sphere. Write: phi equals one minus, open bracket, one minus two d_c over d, close bracket, cubed. At 800 micrometres that's about 21 percent."
- **Step 3.** "Balance on the surface pool: accumulation equals minus dissolution. dF/dt equals minus F over tau_s, times one minus c over c_sat. It's first order in F and slows near saturation. Coffee is far from saturation, so that factor stays near one."
- **Step 4.** "Balance on the grains: dS/dt equals minus V_k over tau_d, times c_k minus c. The driving force is the concentration difference between the liquid inside the grain and the bulk."
- **Steps 5–6.** "Everything that leaves the grains enters the liquid, so dm_l/dt is minus the sum of the other two. Add all three and the derivative of the total is zero: mass is conserved exactly. The app checks this every batch, and the error is about ten to the minus fifteen."
- **Steps 7–8.** "The time scales come from Moroney's 2016 paper. Diffusion time goes as d squared over the diffusivity, so halving the grind makes it four times faster. Temperature enters through Stokes–Einstein, D equals k_B T over 3 pi mu d_m. Hot water has a lower viscosity, so diffusion is faster."
- **Steps 9–10.** "These are coupled ODEs with temperature changing in time, so I solve them numerically. The standard recipe gives 1.10 percent strength and 17.9 percent extraction, just under the ideal box. And extraction can never pass about 28.5 percent, because the liquid trapped in the spent grounds holds coffee you throw away."

## 4. Plunge filtration, Darcy's law (3:30 – 4:45) · Screen: Plunge filtration

- **Steps 1–2.** "Plunging pushes the liquid through a cake of grounds. The superficial velocity is volume over area over time, about 2 millimetres per second. Darcy's law: delta P equals mu times u times cake thickness, over the permeability k."
- **Steps 3–5.** "Where does k come from? Treat each pore as a tiny Hagen–Poiseuille pipe, the same derivation as laminar pipe flow, sized by the hydraulic radius, epsilon d over 6 times one minus epsilon. Add the winding path and you get Kozeny–Carman: k equals d squared epsilon cubed over 180, one minus epsilon squared. The 180 is 36 from the hydraulic radius times the Kozeny constant, about 5."
- **Steps 6–7.** "Fines matter. Permeability is set by surface area, and 15 percent fines pull the effective diameter from 800 down to about 165 micrometres. The cake and the mesh add like resistors in series, and pressure times area is the force, about 2 newtons. Kozeny–Carman over-predicts coffee permeability by up to six times, so I treat this as an estimate."

## 5. Stokes settling (4:45 – 5:50) · Screen: Stokes settling

- **Steps 1–3.** "Why is the last sip of French press coffee gritty? Take one 30 micrometre fine, with downward as positive. At terminal velocity the acceleration is zero, so the forces balance: weight plus buoyancy plus drag equals zero."
- **Steps 4–7.** "Weight is plus rho_p g pi d cubed over 6. Buoyancy is minus rho g pi d cubed over 6, because it points up. Stokes drag is minus 3 pi mu d v_t, opposing the motion."
- **Steps 8–10.** "Group weight and buoyancy into the density difference and divide by 3 pi mu d. v_t equals rho_p minus rho, times g d squared, over 18 mu. The 18 is 6 from the volume times 3 from the drag."
- **Steps 11–13.** "The fine is porous and full of water, so its density is only about 1145 kilograms per cubic metre. The check is the particle Reynolds number, about 0.014, below 0.1, so Stokes' law holds. v_t is about 0.2 millimetres per second, so an 8 centimetre cup takes about 7 minutes to clear."

## 6. Energy balance in 30 seconds (5:50 – 6:20) · Screen: Energy balance

"Pouring is adiabatic mixing: heat lost by the water equals heat gained by the grounds and the cold glass, so 93 degree water starts the brew at only 76.5. Then it's lumped cooling: C dT/dt equals minus UA times T minus room temperature, which is an exponential with a time constant of about 23 minutes. Preheating the press removes most of the drop."

## 7. The AI operator (6:20 – 7:15) · Screen: AI operator steps, then the AI operator view

"Now the AI. It doesn't see any of these equations. Like a real operator, it sends a recipe and reads a noisy TDS meter. For each output it fits a Gaussian process: a model that predicts the result *and* how unsure it is. It then brews the recipe with the highest probability of landing in the ideal box. Over 20 runs, the AI reached the ideal cup every time, with a median of 7 batches. Changing one factor at a time managed 6 out of 20, because grind and time interact."

*(Switch to the AI operator view and press the AI button a few times to show it closing in.)*

## 8. Honesty and close (7:15 – 7:40) · Screen: Engineering notes

"Some numbers are assumed, like the heat-loss coefficient and the mesh resistance. The app lists them, and the code refuses to extrapolate outside its range. Every symbol has SI units, and every equation is checked automatically. So that's coffee as a chemical plant: balances we learned in class, solved numerically, and an AI that uses them to experiment efficiently. Thank you."

---

## If you run short or long on time

- **Too long:** skip Extraction steps 7–8 (say "the time scales come from Moroney 2016") and Plunge steps 3–5 (say "permeability comes from Kozeny–Carman").
- **Too short:** add the Grill-me questions from the Stokes unit as a self-quiz at the end.
