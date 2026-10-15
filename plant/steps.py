"""Write / Say derivations for every plant unit, in the professor's format.

Each unit is a plain dict:
  title, tag (P&ID tag to highlight), sign (the sign convention for that unit), dof (degree-of-freedom
  analysis), steps: list of {"title", "write" (KaTeX string), "say" (plain words)},
  checks: physical checks, questions: list of (question, answer).
SYMBOLS maps every LaTeX symbol used in a "write" line to (meaning, SI unit).
tests/test_standards.py audits that every symbol in every equation is defined here, with a real SI unit.
Numbers quoted in the "say" lines are for the standard recipe (800 um grind, 93 C kettle, 4 min, 15 g coffee
in 250 g water) and are checked against plant/physics.py in tests/test_standards.py.
"""

# One convention for the whole project, from alex's pipe-flow notes (version A):
SIGN_FLOW = "Forward (the flow direction) is positive. Pressure drop is counted positive in the flow direction."
SIGN_DOWN = "Downward is positive. Every force is a signed number in that direction."
SIGN_IN = "Mass or heat into the system is positive and out of it is negative, so a loss term carries a minus sign."

SYMBOLS = {
    # ---- general ----
    r"t": ("time", "s"),
    r"T": ("brew (or water) temperature", "K"),
    r"g": ("gravitational acceleration, 9.81", "m/s^2"),
    r"\rho": ("density of the water or brew", "kg/m^3"),
    r"\mu": ("dynamic viscosity of the water or brew", "Pa*s"),
    r"\pi": ("pi, 3.14159", "1"),
    r"\Sigma F": ("net (signed) force", "N"),
    # ---- plant overview ----
    r"\mathrm{TDS}": ("strength: dissolved coffee mass / beverage mass", "1"),
    r"\mathrm{EY}": ("extraction yield: dissolved coffee mass / dry coffee mass", "1"),
    r"m_c": ("mass of dry coffee grounds", "kg"),
    r"m_w": ("mass of water from the kettle", "kg"),
    r"m_l": ("mass of coffee solubles dissolved in the bulk liquid", "kg"),
    r"m_{bev}": ("mass of the beverage (bulk liquid plus what is dissolved in it)", "kg"),
    r"R_w": ("brew ratio: water mass / coffee mass", "1"),
    r"T_w": ("kettle water temperature", "K"),
    r"t_s": ("steep time", "s"),
    r"d": ("grind size: diameter of a coffee particle", "m"),
    r"N_{DOF}": ("number of degrees of freedom", "1"),
    r"N_{var}": ("number of variables", "1"),
    r"N_{eq}": ("number of independent equations", "1"),
    # ---- R-101: extraction ----
    r"F": ("undissolved solubles on the broken-cell surfaces of the grains (fast pool)", "kg"),
    r"S": ("solubles still inside the grains (slow pool)", "kg"),
    r"M_E": ("total extractable solubles in the dose, x_E m_c", "kg"),
    r"x_E": ("extractable mass fraction of roasted coffee, 0.30", "1"),
    r"\phi": ("fraction of the solubles sitting in broken surface cells", "1"),
    r"d_c": ("diameter of one coffee cell, 30 micrometres", "m"),
    r"c": ("concentration of solubles in the bulk liquid", "kg/m^3"),
    r"c_k": ("concentration of solubles in the liquid inside the grains", "kg/m^3"),
    r"c_{sat}": ("solubility (saturation concentration) of coffee solubles", "kg/m^3"),
    r"V_b": ("volume of bulk liquid around the grains", "m^3"),
    r"V_k": ("volume of liquid inside the grains' pores", "m^3"),
    r"\tau_s": ("surface dissolution time scale", "s"),
    r"\tau_d": ("diffusion time scale out of the grains", "s"),
    r"D_{eff}": ("effective diffusivity of solubles inside a grain", "m^2/s"),
    r"k_B": ("Boltzmann constant, 1.381e-23", "J/K"),
    r"d_m": ("diameter of a dissolved coffee molecule", "m"),
    r"\mathrm{EY}_{max}": ("highest extraction yield the press can reach", "1"),
    # ---- R-101: energy ----
    r"c_{p,w}": ("specific heat of water", "J/(kg*K)"),
    r"c_{p,c}": ("specific heat of dry coffee grounds", "J/(kg*K)"),
    r"c_{p,v}": ("specific heat of the press (glass)", "J/(kg*K)"),
    r"m_v": ("mass of the press vessel", "kg"),
    r"T_\infty": ("room (ambient) temperature", "K"),
    r"T_v": ("starting temperature of the press vessel", "K"),
    r"T_0": ("brew temperature right after mixing", "K"),
    r"C": ("total heat capacity of water, grounds and vessel", "J/K"),
    r"UA": ("overall heat-loss conductance of the press to the room", "W/K"),
    r"\tau_{th}": ("thermal time constant C / UA", "s"),
    # ---- F-101: plunge filtration ----
    r"\Delta P": ("pressure drop across the grounds cake (and the mesh, where stated)", "Pa"),
    r"f_p": ("packed-bed friction factor (Ergun)", "1"),
    r"\mathrm{Re}_b": ("packed-bed Reynolds number rho u d_s / (mu (1 - epsilon))", "1"),
    r"\Pi_1": ("first dimensionless group: pressure gradient times d_s over rho u^2", "1"),
    r"\Pi_2": ("second dimensionless group: rho u d_s / mu", "1"),
    r"u": ("superficial velocity: liquid flow rate / full press area", "m/s"),
    r"u_i": ("interstitial velocity: actual speed of liquid in the pores", "m/s"),
    r"k": ("permeability of the grounds cake", "m^2"),
    r"L_c": ("thickness of the grounds cake", "m"),
    r"L_e": ("actual (winding) path length through the cake", "m"),
    r"\varepsilon": ("cake porosity: void volume / total cake volume", "1"),
    r"R_h": ("hydraulic radius of the pores: void volume / wetted surface", "m"),
    r"a_v": ("particle surface area per particle volume", "1/m"),
    r"d_{32}": ("Sauter mean diameter (same volume-to-surface ratio as the grind)", "m"),
    r"d_s": ("effective grain diameter for Ergun: sphericity times d32", "m"),
    r"\Phi_s": ("sphericity: surface of the equal-volume sphere / real grain surface, 0.75 for coffee", "1"),
    r"d_f": ("diameter of a fine, 30 micrometres", "m"),
    r"w": ("mass fraction of fines in the grind", "1"),
    r"K_K": ("Kozeny constant (shape factor times tortuosity squared), about 5", "1"),
    r"\tau_t": ("tortuosity: winding path length / cake thickness", "1"),
    r"R_m": ("hydraulic resistance of the mesh", "1/m"),
    r"A_c": ("cross-section area of the press", "m^2"),
    r"F_p": ("force needed on the plunger", "N"),
    r"t_p": ("plunge time", "s"),
    r"V_l": ("volume of liquid pushed through the cake", "m^3"),
    # ---- T-101: Stokes settling ----
    r"v_t": ("terminal settling velocity of a particle", "m/s"),
    r"u_p": ("particle velocity at any instant", "m/s"),
    r"d_p": ("particle (fine) diameter", "m"),
    r"\rho_p": ("wet particle density (solid plus water in its pores)", "kg/m^3"),
    r"\rho_s": ("density of the coffee solid itself", "kg/m^3"),
    r"\varepsilon_p": ("porosity inside one particle (pore volume / particle volume)", "1"),
    r"V_p": ("particle volume", "m^3"),
    r"F_g": ("weight of the particle (gravity force)", "N"),
    r"F_b": ("buoyancy force on the particle", "N"),
    r"F_d": ("viscous drag force on the particle", "N"),
    r"m_p": ("particle mass", "kg"),
    r"\mathrm{Re}_p": ("particle Reynolds number, inertia over viscous forces", "1"),
    r"t_{set}": ("time for a fine to settle through the cup", "s"),
    r"h_c": ("depth of liquid in the cup", "m"),
    # ---- AI operator ----
    r"\mathbf{x}": ("recipe vector: grind, temperature, steep time, ratio (scaled to 0-1)", "1"),
    r"\mathbf{x}'": ("a second recipe vector", "1"),
    r"x_j": ("setpoint j of recipe x, scaled to 0-1", "1"),
    r"x'_j": ("setpoint j of recipe x', scaled to 0-1", "1"),
    r"j": ("index over the four setpoints", "1"),
    r"y": ("a measured outcome (TDS or EY)", "1"),
    r"\hat{y}": ("Gaussian-process prediction (mean) of the outcome", "1"),
    r"\hat{\sigma}": ("Gaussian-process standard deviation (how unsure it is)", "1"),
    r"\sigma_f": ("signal standard deviation (how much outcomes vary)", "1"),
    r"\kappa": ("kernel: similarity between two recipes", "1"),
    r"\ell_j": ("length scale of setpoint j (how far before recipes stop being similar)", "1"),
    r"\delta": ("scaled distance between two recipes", "1"),
    r"\Phi": ("standard normal cumulative distribution function", "1"),
    r"P_{in}": ("probability that a recipe lands in the ideal box", "1"),
    r"y_{lo}": ("lower edge of the target box for an outcome", "1"),
    r"y_{hi}": ("upper edge of the target box for an outcome", "1"),
    r"\epsilon_n": ("random measurement noise", "1"),
    r"g_{true}": ("the plant's true (unknown) response to a recipe", "1"),
}

# =====================================================================================================
OVERVIEW = {
    "title": "Plant overview: what the plant does and its degrees of freedom",
    "tag": "R-101",
    "sign": SIGN_IN,
    "dof": {
        "unknowns": ["strength TDS", "extraction yield EY", "dissolved mass m_l", "beverage mass m_bev"],
        "equations": ["TDS definition", "EY definition", "extraction model for m_l", "beverage mass balance"],
        "specified": ["the 4 setpoints the operator controls: grind d, kettle temperature T_w, steep time t_s, "
                      "brew ratio R_w (the coffee dose m_c is fixed)"],
        "result": "4 unknowns − 4 equations = 0 once the 4 setpoints are given. So the operator (human or AI) "
                  "has exactly 4 degrees of freedom to choose: that's the AI's search space.",
    },
    "steps": [
        {"title": "The plant in one line",
         "write": r"\text{kettle} \rightarrow \text{press} \rightarrow \text{filter} \rightarrow \text{cup}",
         "say": "Hot water from the kettle goes into the press, the grounds steep, the plunger filters "
                "them out, and fine particles settle in the cup. The heart of the project is the plunge: the "
                "grounds form a packed bed, and the Ergun equation, built from dimensional analysis, says how "
                "grind size sets the flow. The other units link that to the cup: a material balance, an energy "
                "balance and Stokes' law."},
        {"title": "Strength (what a TDS meter reads)",
         "write": r"\mathrm{TDS} = \frac{m_l}{m_{bev}}",
         "say": "TDS is total dissolved solids: the mass of coffee dissolved, m_l, over the mass of the drink, "
                "m_bev. The target is 1.15 to 1.35 percent."},
        {"title": "Extraction yield",
         "write": r"\mathrm{EY} = \frac{m_l}{m_c}",
         "say": "Extraction yield is the same dissolved mass m_l, but over the dry coffee mass m_c. It says how "
                "much of the coffee we pulled out. The target is 18 to 22 percent."},
        {"title": "Linking them (how you measure EY)",
         "write": r"\mathrm{EY} = \mathrm{TDS} \cdot \frac{m_{bev}}{m_c}",
         "say": "Divide the first definition by the second. A TDS meter plus a kitchen scale gives you EY. "
                "That's how the AI's measurements are built."},
        {"title": "Degree-of-freedom count",
         "write": r"N_{DOF} = N_{var} - N_{eq}",
         "say": "Degrees of freedom are the number of variables minus the number of independent equations. "
                "Whatever is left over has to be chosen by someone."},
        {"title": "The operator's choices",
         "write": r"N_{DOF} = 4: \; (d,\; T_w,\; t_s,\; R_w)",
         "say": "With the coffee dose fixed, the model leaves four free choices: grind size d, kettle "
                "temperature T_w, steep time t_s and brew ratio R_w. Those four dials are what the human and "
                "the AI turn. Everything else follows from the balances."},
    ],
    "checks": [
        "Mass balance: dissolved plus undissolved solubles always equals the extractable total (closure error about 1e-15).",
        "If steep time goes to zero, m_l goes to zero, so TDS and EY both go to zero.",
        "More water for the same coffee (higher R_w) lowers TDS but barely changes EY: dilution, not extraction.",
    ],
    "questions": [
        ("What is the difference between TDS and EY?",
         "Same numerator (dissolved mass). TDS divides by the drink, EY by the dry coffee."),
        ("Why 4 degrees of freedom and not more?",
         "Properties come from temperature, and constants come from the literature. With the dose fixed, "
         "only grind, temperature, steep time and ratio are left."),
        ("Why can't you just set TDS directly?",
         "TDS is an output. You can only set the inputs, and two inputs (grind, time) interact, which is why "
         "an optimizer helps."),
    ],
}

# =====================================================================================================
DIMENSIONAL = {
    "title": "Dimensional analysis: flow through a packed bed of coffee",
    "tag": "F-101",
    "sign": SIGN_FLOW,
    "dof": {
        "unknowns": ["pressure gradient across the bed, Delta P / L_c"],
        "equations": ["one unknown relation Delta P / L_c = fn(u, d_s, rho, mu, epsilon), reduced by Buckingham Pi"],
        "specified": ["flow (superficial velocity u), grain size (d_s), liquid (rho, mu), packing (epsilon)"],
        "result": "6 variables in 3 base dimensions leave 3 dimensionless groups: a friction factor, a Reynolds "
                  "number and the porosity. Any packed bed of any size obeys one curve between them.",
    },
    "steps": [
        {"title": "The question",
         "write": r"\frac{\Delta P}{L_c} = \text{fn}\left( u,\; d_s,\; \rho,\; \mu,\; \varepsilon \right)",
         "say": "How hard do you have to push liquid through a bed of coffee grounds? The pressure drop per unit "
                "bed length depends on how fast the liquid moves, u, how big the grains are, d_s, the liquid's "
                "density rho and viscosity mu, and how loosely the grains pack, the porosity epsilon. I don't "
                "know the function yet. Dimensional analysis tells me its form before any experiment."},
        {"title": "Dimensions of every variable",
         "write": r"\left[ \frac{\Delta P}{L_c} \right] = \text{kg m}^{-2}\text{s}^{-2}, \; [u] = \text{m s}^{-1}, \; [d_s] = \text{m}, \; [\rho] = \text{kg m}^{-3}, \; [\mu] = \text{kg m}^{-1}\text{s}^{-1}",
         "say": "Write each variable in kilograms, metres and seconds. Pressure is a force per area, newtons per "
                "square metre, and per metre of bed that's kilograms per metre squared per second squared. "
                "Porosity is already dimensionless: it's a volume fraction."},
        {"title": "Buckingham Pi count",
         "write": r"\text{groups} = 6 \text{ variables} - 3 \text{ dimensions} = 3",
         "say": "Buckingham's Pi theorem: the number of independent dimensionless groups equals the number of "
                "variables minus the number of base dimensions. Six variables, three dimensions (mass, length, "
                "time), so three groups. One of them is epsilon itself."},
        {"title": "Repeating variables",
         "write": r"\text{repeating set: } \rho,\; u,\; d_s",
         "say": "Pick three variables that together contain kilograms, metres and seconds and can't form a group "
                "by themselves: density, velocity and grain size. Every other variable gets made "
                "dimensionless with them."},
        {"title": "Group 1: pressure made dimensionless",
         "write": r"\Pi_1 = \frac{\Delta P}{L_c} \cdot \frac{d_s}{\rho u^2}",
         "say": "rho u squared is a pressure (the kinetic energy per volume). Dividing the pressure gradient times "
                "a length by it cancels every unit. It compares the pressure lost per grain to the flow's "
                "kinetic energy, so it's a friction factor."},
        {"title": "Group 2: Reynolds number",
         "write": r"\Pi_2 = \frac{\rho u d_s}{\mu}",
         "say": "Viscosity made dimensionless with the same three variables gives a Reynolds number based on "
                "grain size: inertia over viscous forces, exactly as in pipe flow."},
        {"title": "The answer has to look like this",
         "write": r"\Pi_1 = \text{fn}(\Pi_2,\; \varepsilon)",
         "say": "The physics can only connect the dimensionless groups. So instead of experiments in five "
                "variables I need one curve, friction factor against Reynolds number, for each porosity."},
        {"title": "Ergun's choice of groups",
         "write": r"f_p = \frac{\Delta P}{L_c} \frac{d_s}{\rho u^2} \frac{\varepsilon^3}{1-\varepsilon}, \quad \mathrm{Re}_b = \frac{\rho u d_s}{\mu (1-\varepsilon)}",
         "say": "Ergun folded the porosity into the two groups so that data for every porosity collapse onto a "
                "single curve. These are the bed friction factor f_p and the bed Reynolds number Re_b. The "
                "porosity factors come from the hydraulic radius of the pores, which is the next unit."},
    ],
    "checks": [
        "f_p and Re_b are dimensionless: pint confirms both in the test suite.",
        "Same groups as pipe flow (Fanning/Darcy friction factor vs Re): a packed bed is a bundle of tiny tortuous pipes.",
        "If you double every length and keep Re_b the same, f_p stays the same: that's how a lab column scales to a plant bed.",
    ],
    "questions": [
        ("Why exactly three groups?",
         "Six variables minus three base dimensions (kg, m, s), by the Buckingham Pi theorem."),
        ("Why choose rho, u and d as repeating variables?",
         "Together they contain all three dimensions and can't form a dimensionless group on their own. Any "
         "valid choice gives equivalent groups."),
        ("What does dimensional analysis not tell you?",
         "The shape of the function. That needs physics (the Ergun derivation) or experiments."),
        ("Why put (1 - epsilon) in the Reynolds number?",
         "It turns the grain size into the pore size scale (through the hydraulic radius), so beds with "
         "different packing line up on one curve."),
    ],
}

ERGUN = {
    "title": "Ergun equation: viscous plus inertial losses in the coffee bed",
    "tag": "F-101",
    "sign": SIGN_FLOW,
    "dof": {
        "unknowns": ["pressure gradient Delta P / L_c", "bed Reynolds number Re_b", "bed friction factor f_p"],
        "equations": ["Ergun equation", "definition of Re_b", "definition of f_p"],
        "specified": ["u from the plunge speed, d_s from the grind, fines and grain shape, epsilon, temperature (rho, mu)"],
        "result": "3 unknowns − 3 equations = 0.",
    },
    "steps": [
        {"title": "Slow flow limit (viscous): Kozeny-Carman",
         "write": r"\frac{\Delta P}{L_c} = 150\, \frac{\mu u (1-\varepsilon)^2}{\varepsilon^3 d_s^2}",
         "say": "When the flow is slow, friction on the pore walls dominates, like laminar flow in a pipe. "
                "Treating the pores as tiny Hagen-Poiseuille tubes gives this (the filtration unit derives it). "
                "Carman's derivation gives a constant of 180; Ergun fitted 150 to measured beds. The loss is "
                "linear in u and goes as one over d squared."},
        {"title": "Fast flow limit (inertial): Burke-Plummer",
         "write": r"\frac{\Delta P}{L_c} = 1.75\, \frac{\rho u^2 (1-\varepsilon)}{\varepsilon^3 d_s}",
         "say": "When the flow is fast, the liquid speeds up and slows down around every grain and loses a fixed "
                "number of velocity heads per grain, like the minor losses in pipe fittings. That loss goes as "
                "rho u squared and doesn't depend on viscosity."},
        {"title": "Ergun: add the two losses",
         "write": r"\frac{\Delta P}{L_c} = 150\, \frac{\mu u (1-\varepsilon)^2}{\varepsilon^3 d_s^2} + 1.75\, \frac{\rho u^2 (1-\varepsilon)}{\varepsilon^3 d_s}",
         "say": "Ergun's idea: the two mechanisms act together, so add them. The first term wins at low speed, "
                "the second at high speed, and in between both matter."},
        {"title": "Make it dimensionless",
         "write": r"f_p = \frac{150}{\mathrm{Re}_b} + 1.75",
         "say": "Multiply both sides by d_s epsilon cubed over rho u squared times one minus epsilon. The "
                "left side becomes f_p, and the right side becomes 150 over Re_b plus 1.75. That's the single "
                "curve the dimensional analysis promised, now with its shape from physics."},
        {"title": "Bridge to Darcy: k from the grind",
         "write": r"u = \frac{k}{\mu} \frac{\Delta P}{L_c}, \quad k = \frac{d_s^2\, \varepsilon^3}{150 (1-\varepsilon)^2}",
         "say": "Keep only the viscous term and solve for u. That's exactly Darcy's law from our notes, but now "
                "the permeability k isn't a fudge factor: it's set by grain size squared and the porosity. "
                "Darcy is Ergun's slow-flow limit."},
        {"title": "Which term matters for coffee?",
         "write": r"\frac{\text{inertial}}{\text{viscous}} = \frac{1.75\, \mathrm{Re}_b}{150}",
         "say": "Divide the two terms. For the standard plunge, u is about 2 millimetres per second and d_s is "
                "about 125 micrometres, so Re_b is about 1.0. The inertial term is only about 1.1 percent of the "
                "loss. The coffee bed is in the viscous (Darcy) regime, and now that's shown with a number "
                "instead of assumed."},
        {"title": "Grind size in the viscous regime",
         "write": r"\frac{\Delta P}{L_c} \propto \frac{1}{d_s^2}",
         "say": "In the viscous regime, halving the effective grain size makes the bed four times harder to push "
                "through. That's why espresso, with a very fine grind, needs a 9 bar pump and a French press "
                "doesn't."},
        {"title": "The surprise: fines control d_32",
         "write": r"\frac{1}{d_{32}} = \frac{w}{d_f} + \frac{1-w}{d}",
         "say": "The Sauter diameter is set by surface area, and the 30 micrometre fines carry most of it. With "
                "15 percent fines, going from an 800 to a 300 micrometre grind only moves d_32 from 165 to 128 "
                "micrometres. The fines, not the average grind, control the flow, which is why baristas obsess "
                "over grinder quality."},
        {"title": "Grains are not spheres: sphericity",
         "write": r"d_s = \Phi_s\, d_{32}",
         "say": "Ergun's constants were fitted to beds of near-spherical particles. Coffee grains are irregular, "
                "and sphericity Phi_s measures that: the surface of a sphere with the grain's volume divided by "
                "the grain's real surface. Corrochano 2015 measured 0.75 for ground coffee, so the effective "
                "diameter d_s is three quarters of d_32: about 125 micrometres for the standard grind. More "
                "surface per volume means more wall friction."},
    ],
    "checks": [
        "Low Re_b: f_p approaches 150/Re_b, the Kozeny-Carman (Darcy) line. High Re_b: f_p approaches 1.75.",
        "The code checks f_p = 150/Re_b + 1.75 to machine precision for every batch.",
        "Doubling the plunge speed doubles the viscous loss but quadruples the inertial one.",
        "Hotter brew has lower mu: the viscous loss falls, the inertial one doesn't change.",
        "Hot vs cold is a number: water at 20 C is 2.4 times more viscous than at our 68 C plunge (3.4 times "
        "more than at 95 C), so a cold plunge needs 2.4 times the cake pressure.",
        "Porosity is a lever: (1 - eps)^2 / eps^3 is 3.2 times bigger at eps = 0.30 than at 0.40, so a bed "
        "squeezed by pushing harder gets harder to push.",
    ],
    "questions": [
        ("Where do 150 and 1.75 come from?",
         "Ergun fitted them to many packed-bed experiments in 1952. 150 is close to Carman's 180 from the "
         "capillary model."),
        ("Is Ergun valid for coffee grounds?",
         "Approximately. It was fitted for near-spherical particles. Coffee grounds are irregular and have fines, "
         "so I use the Sauter diameter and treat the result as an estimate. Corrochano 2015 found the viscous "
         "formula over-predicts coffee permeability by 1.3 to 6 times."),
        ("Why does Re_b include (1 - epsilon)?",
         "It comes from the hydraulic radius of the pores. It makes data for different porosities collapse."),
        ("What Re_b are you at, and is Ergun valid there?",
         "About 1 for the plunge and about 0.16 for espresso. Corrochano measured 0.04 to 4 in real coffee "
         "beds. At low Re_b Ergun reduces to Kozeny-Carman, which is derived "
         "for slow (creeping) flow, so this is the best-founded end of the curve. Wall effects are negligible: the press is about 690 grains wide."),
        ("Espresso uses 9 bar. Isn't that turbulent?",
         "No. The pores are tiny and the flow is slow, so Re_b is about 0.16. All 9 bar goes into viscous "
         "friction: 9 bar and still laminar."),
        ("Coffee grounds aren't spheres.",
         "Right, so I use the effective diameter d_s = sphericity times d_32, with sphericity 0.75 measured by "
         "Corrochano 2015."),
        ("How do you know the porosity?",
         "I don't measure it; 0.40 is assumed for the loose press cake and is the biggest uncertainty. The force "
         "scales as (1 - eps)^2 / eps^3, so 0.35 would raise the cake force 1.75 times and 0.45 would lower it "
         "to 0.59 times. Compressed espresso beds measured 0.12 to 0.33."),
        ("What breaks first?",
         "The uniform-bed assumption: channelling (liquid finds a crack), the bed compressing as you push "
         "(Corrochano measured 0 to 31 percent consolidation under flow), and fines migrating to block the "
         "mesh. So push slow and steady."),
        ("How would you get into the inertial regime?",
         "A much faster flow or bigger particles, for example water through gravel or a catalyst bed in a "
         "reactor. Coffee is always near the viscous end."),
    ],
}

# =====================================================================================================
EXTRACTION = {
    "title": "R-101 extraction: three-pool material balance",
    "tag": "R-101",
    "sign": SIGN_IN,
    "dof": {
        "unknowns": ["F(t)", "S(t)", "m_l(t)", "T(t) (from the energy balance)"],
        "equations": ["balance on the surface pool", "balance on the in-grain pool",
                      "balance on the dissolved pool", "energy balance"],
        "specified": ["grind d, kettle temperature T_w, steep time t_s, ratio R_w, coffee dose m_c; "
                      "literature constants x_E, c_sat, tau_s,ref and tau_d,ref"],
        "result": "4 unknown functions − 4 ODEs = 0, plus 4 initial conditions. Then TDS and EY follow from m_l.",
    },
    "steps": [
        {"title": "Where the solubles sit at the start",
         "write": r"M_E = x_E\, m_c, \quad F(0) = \phi M_E, \quad S(0) = (1-\phi) M_E",
         "say": "Only x_E, about 30 percent of roasted coffee, can dissolve. Grinding breaks cells at the grain "
                "surface. That fraction phi is exposed and dissolves fast (pool F). The rest is locked inside "
                "the grain and must diffuse out (pool S)."},
        {"title": "Fraction in broken surface cells",
         "write": r"\phi = 1 - \left( 1 - \frac{2 d_c}{d} \right)^3",
         "say": "A shell one cell thick (d_c = 30 micrometres) around a sphere of diameter d. One minus the "
                "inner core's volume fraction is the shell. At 800 micrometres phi is about 21 percent: finer "
                "grind, more broken cells."},
        {"title": "Surface pool: dissolution",
         "write": r"\frac{\mathrm{d}F}{\mathrm{d}t} = -\frac{F}{\tau_s}\left( 1 - \frac{c}{c_{sat}} \right)",
         "say": "Accumulation equals minus what dissolves. First order in F with time scale tau_s, and it slows "
                "as the liquid approaches saturation c_sat. With c at about 11 kilograms per cubic metre "
                "against 212, that factor stays near 1."},
        {"title": "In-grain pool: diffusion out",
         "write": r"\frac{\mathrm{d}S}{\mathrm{d}t} = -\frac{V_k}{\tau_d}\,(c_k - c)",
         "say": "Solubles leave the grains at a rate driven by the concentration difference between the "
                "liquid inside the pores, c_k = S/V_k, and the bulk, c. tau_d is the diffusion time scale. "
                "If c_k equals c, the transfer stops."},
        {"title": "Dissolved pool: what the other two lose",
         "write": r"\frac{\mathrm{d}m_l}{\mathrm{d}t} = -\frac{\mathrm{d}F}{\mathrm{d}t} - \frac{\mathrm{d}S}{\mathrm{d}t}, \quad c = \frac{m_l}{V_b}",
         "say": "Everything leaving the grains enters the liquid: no generation, no reaction. The bulk "
                "concentration is the dissolved mass over the bulk liquid volume V_b."},
        {"title": "Conservation check",
         "write": r"\frac{\mathrm{d}}{\mathrm{d}t}(F + S + m_l) = 0",
         "say": "Add the three equations: the total is constant. The app checks this every batch numerically, "
                "and the error is about 10 to the minus 15."},
        {"title": "Why the time scales depend on grind size",
         "write": r"\tau_d \propto \frac{d^2}{D_{eff}}, \quad \tau_s \propto d^3",
         "say": "The diffusion time grows with distance squared over diffusivity: halve the grind and "
                "diffusion is 4 times faster. For the surface time, d cubed is the scaling that fits both of "
                "Moroney's measured grinds. They're anchored at 42.2 s and 1.18 s for a 322 micrometre grind at "
                "90 °C."},
        {"title": "Why temperature matters (Stokes-Einstein)",
         "write": r"D_{eff} = \frac{k_B T}{3 \pi \mu d_m}",
         "say": "A dissolved molecule of size d_m moving through water is a tiny Stokes sphere: thermal energy "
                "k_B T pushes it and viscous drag 3 pi mu d_m resists. Hot water has a lower mu and a higher "
                "T, so diffusion speeds up. Both time scales are multiplied by mu over T."},
        {"title": "Solve and report",
         "write": r"\mathrm{TDS} = \frac{m_l(t_s)}{m_{bev}}, \quad \mathrm{EY} = \frac{m_l(t_s)}{m_c}",
         "say": "The equations are coupled and temperature changes with time, so scipy's solve_ivp integrates "
                "them to the steep time. For the standard recipe that gives TDS 1.10 percent and EY 17.9 "
                "percent, just under the ideal box."},
        {"title": "The ceiling on extraction",
         "write": r"\mathrm{EY}_{max} = x_E \frac{V_b}{V_b + V_k}",
         "say": "At equilibrium c_k = c everywhere, so the liquid trapped in the grounds holds the same "
                "concentration and is thrown away. That caps EY at about 28.5 percent, not 30."},
    ],
    "checks": [
        "At t = 0 nothing is dissolved, so TDS = 0. As t gets large, EY approaches EY_max.",
        "Doubling d makes tau_d 4 times longer, so coarse grinds need much longer steeps.",
        "If c reached c_sat, surface dissolution would stop. In coffee c is far below, so it never does.",
        "Units: F/tau_s is kg/s, and (V_k/tau_d)(c_k − c) is (m^3/s)(kg/m^3) = kg/s.",
    ],
    "questions": [
        ("Why two pools and not one?",
         "Moroney's data show a fast early rise then a slow tail: two mechanisms with time scales about 40 times apart."),
        ("Why is the model 'lumped'?",
         "Real diffusion is a PDE inside each grain. I replace it with one time constant per pool, which is the "
         "undergraduate-level simplification, and I state it."),
        ("Where do your constants come from?",
         "Moroney et al. 2016 (time scales, x_E, c_sat, cell size) and Corrochano et al. 2015 (densities, porosity)."),
        ("What does 'well mixed' assume and is it valid?",
         "One concentration throughout the liquid. It's reasonable after a stir, and it's the standard "
         "assumption in Moroney's model. A real press has some gradients, which is a stated limitation."),
    ],
}

# =====================================================================================================
COOLING = {
    "title": "R-101 energy balance: mixing and cooling",
    "tag": "R-101",
    "sign": SIGN_IN,
    "dof": {
        "unknowns": ["mixed temperature T_0", "brew temperature T(t)"],
        "equations": ["adiabatic mixing balance", "transient lumped energy balance"],
        "specified": ["masses and specific heats of water, grounds and vessel; T_w; room temperature; UA"],
        "result": "2 unknowns − 2 equations = 0.",
    },
    "steps": [
        {"title": "Mixing: heat lost by water = heat gained by grounds and glass",
         "write": r"m_w c_{p,w} (T_w - T_0) = m_c c_{p,c} (T_0 - T_\infty) + m_v c_{p,v} (T_0 - T_v)",
         "say": "Right after pouring, in the first seconds, heat loss to the room is negligible, so mixing is "
                "adiabatic. The hot water cools to T_0, while the room-temperature grounds and the press "
                "vessel warm up to T_0."},
        {"title": "Total heat capacity",
         "write": r"C = m_w c_{p,w} + m_c c_{p,c} + m_v c_{p,v}",
         "say": "Add up mass times specific heat for everything that changes temperature together: water, "
                "grounds and glass. C is about 1370 joules per kelvin, and the glass is a fifth of it."},
        {"title": "Solve for the starting temperature",
         "write": r"T_0 = \frac{m_w c_{p,w} T_w + m_c c_{p,c} T_\infty + m_v c_{p,v} T_v}{C}",
         "say": "A heat-capacity-weighted average temperature. With a cold 350 gram glass press, 93 °C water "
                "starts the brew at only 76.5 °C. Preheating the press (T_v = T_w) removes most of that drop."},
        {"title": "Transient energy balance on the press",
         "write": r"C \frac{\mathrm{d}T}{\mathrm{d}t} = -UA\,(T - T_\infty)",
         "say": "Accumulation equals minus the heat lost to the room. Lumped: one temperature for everything, "
                "because the brew is stirred and the glass is thin. UA is the overall conductance, assumed "
                "to be 1 watt per kelvin."},
        {"title": "Separate and integrate",
         "write": r"T = T_\infty + (T_0 - T_\infty)\, e^{-t/\tau_{th}}, \quad \tau_{th} = \frac{C}{UA}",
         "say": "Exponential decay toward room temperature with time constant tau_th. C is about 1370 joules "
                "per kelvin, so tau_th is about 23 minutes and a 4 minute steep loses about 9 degrees."},
    ],
    "checks": [
        "At t = 0, T = T_0. As t gets large, T approaches room temperature.",
        "Double UA (a thinner glass or a draft) and the brew cools twice as fast.",
        "Heating the brew back up would need a positive term: a heater, which the press doesn't have.",
    ],
    "questions": [
        ("Why is mixing adiabatic but brewing is not?",
         "Mixing takes seconds and cooling takes tens of minutes, so over the first seconds the loss is negligible."),
        ("When is the lumped model valid?",
         "When the temperature inside is nearly uniform: stirred liquid and a thin wall. A Biot-number argument "
         "would make it formal."),
        ("Which numbers are assumed?",
         "UA, the specific heat of the grounds and the vessel mass. Water properties come from CoolProp."),
    ],
}

# =====================================================================================================
FILTER = {
    "title": "F-101 plunge filter: Darcy's law and Kozeny-Carman",
    "tag": "F-101",
    "sign": SIGN_FLOW,
    "dof": {
        "unknowns": ["superficial velocity u", "permeability k", "Sauter diameter d32", "cake thickness L_c",
                     "pressure drop dP", "plunger force F_p"],
        "equations": ["u = V_l / (A_c t_p)", "Kozeny-Carman", "Sauter mean", "cake mass / bulk density",
                      "Darcy plus mesh in series", "F_p = dP A_c"],
        "specified": ["grind d, fines fraction w, plunge time t_p, coffee dose, porosity, mesh resistance, temperature"],
        "result": "6 unknowns − 6 equations = 0.",
    },
    "steps": [
        {"title": "Superficial velocity",
         "write": r"u = \frac{V_l}{A_c\, t_p}",
         "say": "The liquid volume pushed through in the plunge time, over the full press area. It's "
                "'superficial' because it pretends the grounds aren't there. About 2 millimetres per second."},
        {"title": "Darcy's law for the cake",
         "write": r"\Delta P = \frac{\mu\, u\, L_c}{k}",
         "say": "For slow flow through a porous bed, the pressure drop is proportional to viscosity, velocity "
                "and cake thickness, and inversely proportional to permeability k. It's the porous-media "
                "version of Hagen-Poiseuille."},
        {"title": "Pores as tiny pipes: hydraulic radius",
         "write": r"R_h = \frac{\varepsilon}{a_v (1-\varepsilon)}, \quad a_v = \frac{6}{d_s}",
         "say": "The hydraulic radius is pore volume over wetted surface. epsilon is the void fraction, and "
                "a_v is the surface area per particle volume, 6 over d for a sphere."},
        {"title": "Hagen-Poiseuille in a winding pore",
         "write": r"u_i = \frac{R_h^2\, \Delta P}{2 \mu L_e}, \quad u_i = \frac{u\, \tau_t}{\varepsilon}, \quad L_e = \tau_t L_c",
         "say": "In a round tube, the mean speed is D squared Delta P over 32 mu L, and D = 4 R_h gives R_h "
                "squared over 2. The real path L_e winds, with tortuosity tau_t, and the liquid moves faster "
                "in the pores than u by tau_t over epsilon."},
        {"title": "Kozeny-Carman permeability",
         "write": r"k = \frac{d_s^2\, \varepsilon^3}{36 K_K (1-\varepsilon)^2} = \frac{d_s^2\, \varepsilon^3}{180 (1-\varepsilon)^2}",
         "say": "Combine the last two steps and compare with Darcy. The shape factor and tortuosity squared "
                "make the Kozeny constant K_K of about 5, so 36 times 5 gives 180. Permeability goes as d "
                "squared: finer grounds are much harder to push through. Ergun later fitted 150 instead of 180 "
                "to measured beds, and the code uses Ergun's 150."},
        {"title": "Fines and the Sauter mean diameter",
         "write": r"\frac{1}{d_{32}} = \frac{w}{d_f} + \frac{1-w}{d}",
         "say": "Permeability is set by surface area, and fines carry a huge share of it. Just 15 percent "
                "fines by mass at 30 micrometres pulls d32 from 800 down to about 165 micrometres."},
        {"title": "Cake plus mesh in series, then force",
         "write": r"\Delta P = \mu u \left( \frac{L_c}{k} + R_m \right), \quad F_p = \Delta P\, A_c",
         "say": "Like resistors in series, the cake and the mesh add. Pressure times plunger area is the force. "
                "It's about 3 newtons for the standard recipe. The mesh resistance and porosity are assumed "
                "values, so this is an estimate."},
    ],
    "checks": [
        "Halving the plunge time doubles u and so doubles the force: Darcy is linear in velocity.",
        "As epsilon goes to 1 (no grounds), k becomes infinite and the cake adds no resistance.",
        "Bed Reynolds number Re_b is about 1.0, so Ergun's inertial term is only about 1 percent: Darcy is fine here.",
        "Units: (Pa*s)(m/s)(m)/(m^2) = Pa.",
    ],
    "questions": [
        ("Where does 180 come from?",
         "36 from the hydraulic-radius algebra (6 squared) times the Kozeny constant of about 5."),
        ("Is Kozeny-Carman accurate for coffee?",
         "No. Corrochano 2015 found it over-predicts coffee-bed permeability by about 1.3 to 6 times, so I treat "
         "it as an estimate."),
        ("Why does a too-fine grind make the press hard to push?",
         "k goes as d32 squared, and fines drag d32 down, so the pressure drop shoots up."),
    ],
}

# =====================================================================================================
STOKES = {
    "title": "T-101 cup: fines settling (Stokes' law)",
    "tag": "T-101",
    "sign": SIGN_DOWN,
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
         "write": r"m_p \frac{\mathrm{d}u_p}{\mathrm{d}t} = \Sigma F = F_g + F_b + F_d",
         "say": "Mass times acceleration equals the sum of the forces. m_p is the particle's mass and "
                "du_p/dt is how fast its speed changes. Released from rest, it speeds up until the forces "
                "cancel."},
        {"title": "Terminal velocity: the force balance",
         "write": r"\frac{\mathrm{d}u_p}{\mathrm{d}t} = 0 \;\Rightarrow\; F_g + F_b + F_d = 0",
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
                "density times the pore fraction epsilon_p = 0.53. That gives about 1145 kilograms per "
                "cubic metre, only a bit heavier than the brew, which is why fines settle slowly."},
        {"title": "Check the assumption: particle Reynolds number",
         "write": r"\mathrm{Re}_p = \frac{\rho v_t d_p}{\mu} < 0.1",
         "say": "Stokes drag assumes creeping flow, where viscous forces dominate inertia. The particle "
                "Reynolds number compares the two. For a 30 micrometre fine at the end of the brew it's about 0.014, below 0.1, "
                "so Stokes' law holds. The app flags any case above 0.1."},
        {"title": "Settling time through the cup",
         "write": r"t_{set} = \frac{h_c}{v_t}",
         "say": "The time to fall the depth h_c of the cup at constant speed. For 30 micrometre fines in "
                "8 centimetres of coffee at the end of the brew (about 68 °C), v_t is about 0.2 millimetres "
                "per second, so settling takes about 7 minutes. That's why the last sip of French press coffee is gritty."},
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

# =====================================================================================================
AI = {
    "title": "AI operator: Gaussian process and Bayesian optimization",
    "tag": "R-101",
    "sign": "Higher probability of hitting the target box is better. The AI maximises P_in.",
    "dof": {
        "unknowns": ["the next recipe (4 setpoints)"],
        "equations": ["choose the recipe that maximises P_in over 3000 random candidates"],
        "specified": ["all batches brewed so far (recipe, measured TDS, measured EY)", "the target box"],
        "result": "The 4 operator degrees of freedom from the plant overview are fixed by an optimisation, "
                  "not by an equation.",
    },
    "steps": [
        {"title": "What the AI sees",
         "write": r"y = g_{true}(\mathbf{x}) + \epsilon_n",
         "say": "The AI doesn't know the physics. It sends a recipe x and gets back a noisy measurement y "
                "of TDS or EY, like a real operator reading a meter. The noise epsilon_n is the meter's scatter."},
        {"title": "Similarity between recipes: the kernel",
         "write": r"\delta = \sqrt{\sum_j \left( \frac{x_j - x'_j}{\ell_j} \right)^2}",
         "say": "Two recipes are close if their setpoints are close, measured in units of a length scale "
                "ell_j for each setpoint. A long length scale means that setpoint barely matters. The AI "
                "learns them from data."},
        {"title": "Matérn 5/2 kernel",
         "write": r"\kappa(\mathbf{x}, \mathbf{x}') = \sigma_f^2 \left( 1 + \sqrt{5}\,\delta + \frac{5}{3}\delta^2 \right) e^{-\sqrt{5}\,\delta}",
         "say": "Similarity is 1 for identical recipes and fades with distance. It encodes 'similar recipes "
                "give similar cups', with smoothness like a real physical response. Plus a noise term "
                "sigma_n for the meter."},
        {"title": "Prediction with uncertainty",
         "write": r"y(\mathbf{x}) \approx \hat{y}(\mathbf{x}) \pm \hat{\sigma}(\mathbf{x})",
         "say": "From the batches so far, each Gaussian process gives a best guess y-hat and how unsure it is, "
                "sigma-hat. Near brewed recipes sigma-hat is small, and far away it's large. scikit-learn "
                "does the matrix algebra."},
        {"title": "Probability of landing in the box",
         "write": r"P_{in} = \left[ \Phi\!\left( \frac{y_{hi} - \hat{y}}{\hat{\sigma}} \right) - \Phi\!\left( \frac{y_{lo} - \hat{y}}{\hat{\sigma}} \right) \right]_{\mathrm{TDS}} \times \left[ \text{same for EY} \right]",
         "say": "For each outcome, the chance that a normal variable with mean y-hat and spread sigma-hat lands "
                "between the lower and upper target. Multiply the TDS and EY chances (treated as independent). "
                "The AI brews the recipe with the highest P_in out of 3000 random candidates."},
        {"title": "Benchmark (best found, not a proof)",
         "write": r"\text{AI } 20/20, \quad \text{one-factor-at-a-time } 6/20, \quad \text{random } 8/20",
         "say": "20 independent runs, at most 12 batches each. The AI reached the ideal box every time, with a "
                "median of 7 batches. One-at-a-time fails because grind and time interact."},
    ],
    "checks": [
        "With no data, every recipe is equally uncertain, so the AI explores. That's why it starts with 3 random batches.",
        "Once one recipe hits the box, nearby recipes get high P_in, so the AI exploits.",
        "The seed is fixed, so every benchmark run is reproducible.",
    ],
    "questions": [
        ("Why a Gaussian process and not a neural network?",
         "There are only a handful of data points, and I need uncertainty to decide what to try next. GPs give both."),
        ("What is the exploration vs exploitation trade-off?",
         "Trying unknown recipes (high sigma-hat) versus refining good ones (good y-hat). P_in balances both automatically."),
        ("What are the weaknesses?",
         "TDS and EY are treated as independent, it's only tested on the virtual plant, and GPs scale poorly "
         "beyond a few dimensions."),
    ],
}

UNITS = {
    "Plant overview & DOF": OVERVIEW,
    "Dimensional analysis (packed bed)": DIMENSIONAL,
    "Ergun equation (F-101)": ERGUN,
    "Extraction balance (R-101)": EXTRACTION,
    "Energy balance (R-101)": COOLING,
    "Plunge filtration (F-101)": FILTER,
    "Stokes settling (T-101)": STOKES,
    "AI operator": AI,
}
