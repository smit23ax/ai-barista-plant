# AI Barista Plant: speaking script v2 (about 7½ minutes)

**The question:** how does grind size control flow through the coffee bed, and what does that do to the cup?

Speak at a normal pace (about 140 words a minute). The **Screen** line tells you what to show: a unit in the app's **Presenter** view (with step numbers) or another view. Press **⏱ Start timer** at the start. "Write" means: write that equation by hand, or point to it on screen, while you say the line.

| Time | Section | Screen |
|---|---|---|
| 0:00 | 1. Hook | Plant view |
| 0:35 | 2. Dimensional analysis | Dimensional analysis, steps 1–8 |
| 2:00 | 3. Ergun: two losses, one curve | Ergun equation, steps 1–6, then the Packed bed view |
| 3:40 | 4. Grind size: the trade-off (the middle of the talk) | Ergun steps 7–9, then the Packed bed view |
| 5:30 | 5. The link to the cup: material balance | Extraction balance, steps 1, 5–7, 9 |
| 6:15 | 6. The AI operator | AI operator view |
| 7:00 | 7. Honesty and close | Packed bed view (Corrochano chart), then Engineering notes |

---

## 1. Hook (0:00 – 0:35) · Screen: Plant view

"When you push down a French press, you're forcing water through a packed bed of particles, the same problem as a catalyst bed or a filter in a plant. The question my project answers is: how does grind size control that flow, and what does it do to the coffee? I'll use dimensional analysis and the Ergun equation, check them against measured coffee data, and finish with an AI that uses the model to pick a recipe."

## 2. Dimensional analysis (0:35 – 2:00) · Screen: Dimensional analysis

- **Step 1.** "The pressure gradient through the bed depends on five things: the flow speed u, the grain size d_s, the liquid's density and viscosity, and the porosity."
- **Step 2.** "Write down the dimensions of each. Pressure gradient is kilograms per metre squared per second squared. Porosity is already dimensionless."
- **Step 3.** "Buckingham Pi: six variables minus three base dimensions, kilograms, metres and seconds, gives three dimensionless groups. One of them is porosity itself."
- **Steps 4–6.** "Pick density, velocity and grain size as repeating variables. Group one is the pressure gradient times d_s over rho u squared: pressure lost per grain compared with the kinetic energy, so a friction factor. Group two is rho u d_s over mu, a Reynolds number."
- **Steps 7–8.** "So the friction factor has to be a function of Reynolds number and porosity, and nothing else. Ergun folded the porosity into both groups, f_p and Re_b, so that every bed falls on one curve."
- **Point at the collapse plot in the Packed bed view.** "Here's the payoff. On the left, three different beds give three separate curves. On the right, the same points in f_p and Re_b fall on one curve. Ergun found that measured beds collapse like this."

## 3. Ergun: two losses, one curve (2:00 – 3:40) · Screen: Ergun equation, then Packed bed view

- **Step 1.** "At slow flow, friction on the pore walls dominates, like laminar pipe flow. Treat the pores as tiny Hagen–Poiseuille tubes and you get the Kozeny–Carman term: 150 mu u, one minus epsilon squared, over epsilon cubed d_s squared. Carman's derivation gives 180, and Ergun fitted 150."
- **Step 2.** "At fast flow, the liquid speeds up and slows down around every grain, like minor losses in pipe fittings. That's Burke–Plummer: 1.75 rho u squared, one minus epsilon, over epsilon cubed d_s."
- **Steps 3–4.** "Ergun's idea was to add them. Make it dimensionless and you get f_p equals 150 over Re_b plus 1.75. That's the shape dimensional analysis couldn't give us, now from physics."
- **Step 5.** "Keep only the viscous term and solve for u, and you get exactly Darcy's law from our notes. But now the permeability k isn't a fudge factor. It's set by grain size squared and porosity."
- **Step 6.** "So which term matters for coffee? The ratio of inertial to viscous is 1.75 Re_b over 150. For my plunge, u is about 2 millimetres per second and Re_b is about 1, so the inertial term is only about 1 percent."
- **Switch to the Packed bed view, Ergun chart.** "Here are three brewers on Ergun's chart. Espresso, pour-over and the French press all sit on the viscous line. Espresso uses 9 bar of pressure and its Reynolds number is still only about 0.16: 9 bar, still laminar. Corrochano measured 0.04 to 4 in real coffee beds, this shaded band. All 9 bar goes into viscous friction."

## 4. Grind size: the trade-off (3:40 – 5:30) · Screen: Ergun steps 7–9, then Packed bed view

- **Step 7.** "In the viscous regime the pressure drop goes as one over d_s squared. Halve the grain size and the bed is four times harder to push through. That's why a small grinder adjustment can choke an espresso shot."
- **Step 8.** "But which size? Pressure drop is set by surface area, so the right average is the Sauter diameter, d_32, and fines carry most of the surface. With 15 percent fines at 30 micrometres, going from an 800 to a 300 micrometre grind only moves d_32 from 165 to 128 micrometres. The fines, not the average grind, control the flow."
- **Step 9.** "And grains aren't spheres. Corrochano measured a sphericity of 0.75 for ground coffee, so the effective diameter is three quarters of d_32."
- **Switch to the Packed bed view, grind-size explorer.** "Now the trade-off. Move the grind from 1200 down to 300 micrometres. Extraction goes from 11 percent to 28 percent: finer grinds extract much faster. But the plunge force only goes from 2.5 to 3.9 newtons, because the fines already set the flow. The dashed line is the same grind with no fines: about 1 newton, mostly the mesh. Fine wants extraction, coarse wants flow, and the best recipe is in between, inside this green band. It's the same design trade-off as heat-exchanger area against pumping cost."

## 5. The link to the cup: material balance (5:30 – 6:15) · Screen: Extraction balance

- **Step 1.** "Only about 30 percent of roasted coffee can dissolve. Some sits in broken cells at the surface and dissolves fast; the rest has to diffuse out of the grain. That's Moroney's two-stage model from 2016."
- **Steps 5–6.** "Everything that leaves the grains enters the liquid, so the three pools always add up. The app checks that every batch: the error is about ten to the minus fifteen."
- **Steps 7, 9.** "Diffusion time goes as grain size squared, which is why grind size moves extraction so much. The standard recipe gives 1.10 percent strength and 17.9 percent extraction, just under the ideal box."

## 6. The AI operator (6:15 – 7:00) · Screen: AI operator view

"So there are four dials, grind, temperature, steep time and ratio, and they interact. The AI doesn't see the equations. Like a real operator, it brews a recipe and reads a noisy TDS meter. It fits a Gaussian process, a model that predicts the result and how unsure it is, and brews the recipe most likely to land in the ideal box. Over 20 runs it reached the ideal cup every time, with a median of 7 batches. Changing one factor at a time managed only 6 out of 20, because grind and steep time interact."

*(Press the AI button a few times to show it closing in.)*

## 7. Honesty and close (7:00 – 7:30) · Screen: Packed bed view (Corrochano chart), then Engineering notes

"One honest check. Corrochano measured the permeability of real espresso beds. Ergun over-predicts it by 1.9 to 16 times, and the gap grows with grind size, because those beds are squeezed far below normal packing. My press bed is loose, so I keep 150, but the porosity of 0.40 is assumed and is the biggest uncertainty. The app lists every assumption and checks every equation's units automatically. So: dimensional analysis gave the groups, Ergun gave the shape, and grind size, through the fines, sets the trade-off between flow and flavour. Thank you."

---

## If you run short or long on time

- **Too long:** cut Dimensional analysis steps 4–6 (say "the two groups are a friction factor and a Reynolds number") and Extraction step 1.
- **Too short:** add the Ergun unit's Grill-me questions as a self-quiz, or show the Stokes settling unit: why the last sip is gritty.

## Backup material (not in the timed talk)

- **Energy balance:** pouring is adiabatic mixing, so 93 °C water starts the brew at 76.5 °C; then lumped cooling with a time constant of about 23 minutes.
- **Stokes settling:** a 30 µm fine settles at about 0.2 mm/s (Re_p ≈ 0.014), so an 8 cm cup takes about 7 minutes to clear.
- **Plunge filtration unit:** the full Kozeny–Carman derivation from Hagen–Poiseuille in a winding pore.
