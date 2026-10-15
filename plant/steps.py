"""Write / Say derivations for every plant unit, in the professor's format.

Each unit is a plain dict:
  title, tag (P&ID tag), sign (the one sign convention), dof (degree-of-freedom analysis),
  steps: list of {"title", "write" (KaTeX string), "say" (plain words)},
  checks: physical checks, questions: list of (question, answer).
SYMBOLS maps every LaTeX symbol used in a "write" line to (meaning, SI unit).
tests/test_standards.py audits that every symbol in every equation is in SYMBOLS.
"""

SIGN = "Downward is positive. Every force is a signed number in that direction."

SYMBOLS = {
    r"v_t": ("terminal settling velocity of a particle", "m/s"),
    r"d_p": ("particle (fine) diameter", "m"),
    r"\rho_p": ("wet particle density (solid plus water in its pores)", "kg/m^3"),
    r"\rho_s": ("density of the coffee solid itself", "kg/m^3"),
    r"\rho": ("density of the brew (taken as water)", "kg/m^3"),
    r"\mu": ("dynamic viscosity of the brew (taken as water)", "Pa*s"),
    r"\varepsilon_p": ("porosity inside one particle (pore volume / particle volume)", "1"),
    r"g": ("gravitational acceleration, 9.81", "m/s^2"),
    r"V_p": ("particle volume", "m^3"),
    r"F_g": ("weight of the particle (gravity force)", "N"),
    r"F_b": ("buoyancy force on the particle", "N"),
    r"F_d": ("viscous drag force on the particle", "N"),
    r"\Sigma F": ("net force on the particle", "N"),
    r"m_p": ("particle mass", "kg"),
    r"\mathrm{Re}_p": ("particle Reynolds number, inertia over viscous forces", "1"),
    r"t_{set}": ("time for a fine to settle through the cup", "s"),
    r"h": ("depth of liquid in the cup", "m"),
    r"t": ("time", "s"),
    r"v": ("particle velocity at any instant", "m/s"),
    r"\pi": ("pi, 3.14159", "1"),
}

STOKES = {
    "title": "T-101 cup: fines settling (Stokes' law)",
    "tag": "T-101",
    "sign": SIGN,
    "dof": {
        "unknowns": ["terminal velocity v_t"],
        "equations": ["force balance on one particle at terminal velocity (sum of forces = 0)"],
        "specified": ["particle diameter d_p", "particle density rho_p", "brew density rho",
                      "brew viscosity mu (from temperature)", "gravity g"],
        "result": "1 unknown − 1 equation = 0 degrees of freedom, so v_t is fixed once the specified "
                  "variables are given.",
    },
    "steps": [
        {"title": "Picture and sign convention",
         "write": r"\text{downward} = +",
         "say": "Picture one tiny fine of ground coffee, about 30 micrometres across, sinking in the cup. "
                "I pick downward as positive, and every force is a signed number in that direction. "
                "Three forces act: gravity pulls it down, buoyancy pushes it up, and drag from the "
                "liquid pushes up against its motion."},
        {"title": "Newton's second law on the particle",
         "write": r"m_p \frac{\mathrm{d}v}{\mathrm{d}t} = \Sigma F = F_g + F_b + F_d",
         "say": "Mass times acceleration equals the sum of the forces. m_p is the particle's mass and "
                "dv/dt is how fast its speed changes. Released from rest, it speeds up until the forces "
                "cancel."},
        {"title": "Terminal velocity: the force balance",
         "write": r"\frac{\mathrm{d}v}{\mathrm{d}t} = 0 \;\Rightarrow\; F_g + F_b + F_d = 0",
         "say": "At terminal velocity the speed stops changing, so acceleration is zero and the forces "
                "balance. That's a force balance, the same idea as the pipe flow balance, just on a "
                "sphere instead of a cylinder of fluid."},
        {"title": "Particle volume",
         "write": r"V_p = \frac{\pi d_p^3}{6}",
         "say": "The volume of a sphere written with the diameter d_p instead of the radius: four thirds "
                "pi r cubed, with r equal to d_p over 2."},
        {"title": "Weight (gravity)",
         "write": r"F_g = +\rho_p V_p g = +\rho_p g \frac{\pi d_p^3}{6}",
         "say": "Weight is mass times g, and mass is density times volume. rho_p is the wet particle "
                "density. It's positive because gravity points down, our positive direction."},
        {"title": "Buoyancy (Archimedes)",
         "write": r"F_b = -\rho V_p g = -\rho g \frac{\pi d_p^3}{6}",
         "say": "Buoyancy equals the weight of liquid the particle pushes aside. rho is the density of "
                "the brew. The minus sign means it points up."},
        {"title": "Drag in creeping flow (Stokes drag)",
         "write": r"F_d = -3 \pi \mu d_p v_t",
         "say": "For very slow flow around a sphere, drag is 3 pi times viscosity times diameter times "
                "speed. mu is the viscosity, the liquid's resistance to layers sliding past each other. "
                "Drag opposes the motion, so with the particle moving down it points up and is negative. "
                "The 3 pi comes from solving the creeping-flow equations around a sphere: two thirds of "
                "it is from viscous shear on the surface and one third from pressure."},
        {"title": "Substitute into the balance",
         "write": r"\rho_p g \frac{\pi d_p^3}{6} - \rho g \frac{\pi d_p^3}{6} - 3 \pi \mu d_p v_t = 0",
         "say": "Put the three forces into the force balance: weight minus buoyancy minus drag equals zero."},
        {"title": "Group the first two terms",
         "write": r"(\rho_p - \rho)\, g \frac{\pi d_p^3}{6} = 3 \pi \mu d_p v_t",
         "say": "Weight and buoyancy share the same volume, so they combine into the density difference "
                "times g times volume. That's the net downward pull, and it equals the drag."},
        {"title": "Solve for the terminal velocity",
         "write": r"v_t = \frac{(\rho_p - \rho)\, g\, d_p^2}{18 \mu}",
         "say": "Divide both sides by 3 pi mu d_p. Pi cancels, one d_p cancels, and 6 times 3 gives 18. "
                "This is Stokes' law."},
        {"title": "Wet particle density",
         "write": r"\rho_p = \rho_s (1 - \varepsilon_p) + \rho\, \varepsilon_p",
         "say": "A coffee fine is porous and its pores fill with water. Its density is the solid's "
                "density, rho_s = 1337 kilograms per cubic metre, times the solid fraction, plus water's "
                "density times the pore fraction epsilon_p = 0.53. That gives about 1144 kilograms per "
                "cubic metre, only a bit heavier than the brew, which is why fines settle slowly."},
        {"title": "Check the assumption: particle Reynolds number",
         "write": r"\mathrm{Re}_p = \frac{\rho v_t d_p}{\mu} < 0.1",
         "say": "Stokes drag assumes creeping flow, where viscous forces dominate inertia. The particle "
                "Reynolds number compares the two. For a 30 micrometre fine it's about 0.02, below 0.1, "
                "so Stokes' law holds. The app flags any case above 0.1."},
        {"title": "Settling time through the cup",
         "write": r"t_{set} = \frac{h}{v_t}",
         "say": "The time to fall the depth h of the cup at constant speed. For 30 micrometre fines in "
                "8 centimetres of coffee at about 77 °C, v_t is about 0.23 millimetres per second, so "
                "settling takes about 6 minutes. That's why the last sip of French press coffee is gritty."},
    ],
    "checks": [
        "If rho_p = rho, v_t = 0: a particle with the liquid's density is neutrally buoyant and doesn't sink.",
        "If rho_p < rho, v_t is negative: the particle rises (negative means up in our convention), "
        "like coffee oils and foam.",
        "Doubling d_p makes v_t four times faster (d squared), so big grounds sink at once and fines linger.",
        "Hotter brew has lower mu, so v_t rises: water's viscosity at 80 °C is about 40 % of its value at 25 °C.",
        "Units: (kg/m^3)(m/s^2)(m^2) / (Pa*s) = m/s.",
    ],
    "questions": [
        ("Where does the 18 come from?",
         "6 from the sphere's volume, pi d^3/6, times 3 from the Stokes drag, 3 pi mu d v."),
        ("Why does Stokes' law fail for large particles?",
         "Larger, faster particles have Re_p well above 0.1, so inertia matters and drag is no longer "
         "linear in speed. You'd need a drag-coefficient correlation instead."),
        ("Why does hot coffee settle faster?",
         "Viscosity drops strongly with temperature, and v_t is proportional to 1/mu."),
        ("What happens if a particle is lighter than the liquid?",
         "The density difference is negative, so v_t is negative and the particle rises."),
        ("Why use the wet density and not the solid density?",
         "Water fills the particle's pores and moves with it, so the effective mass includes that water."),
        ("Does the cup wall or other particles matter?",
         "I assumed one sphere far from walls and other particles. Fines are dilute and much smaller "
         "than the cup, so the effect is small. It's a stated assumption."),
    ],
}

UNITS = {"Stokes settling (T-101)": STOKES}
