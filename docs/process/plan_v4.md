# AI Barista Plant: plan v4 for approval

**What your laminar flow chat showed me about your professor:** he wants every derivation explained step by step, with a **Write** line (the equation) and a **Say** line (plain words), each term described in words, sign conventions made explicit, physical checks (wall, center line, limits), and a list of likely questions. v4 rebuilds the explanations in exactly that format and adds three things an AI-heavy professor won't expect.

No real brewing anywhere.

---

## Grill-me questions (reply "proceed" to accept every recommended answer, or answer by number)

1. **Format of the explanations?** Recommended: **Write / Say steps** for every unit (pipe flow, NPSH, extraction, cooling, filtration, Stokes, Torricelli, the AI), like your 13-step pipe flow script, in both the app and a printable HTML file.
2. **Which units do you present on camera?** Recommended: three hero derivations, the extraction material balance, plunge filtration (Darcy) and Stokes settling, plus a 30-second overview of the rest. The others stay in the guide for questions.
3. **Sign convention?** Recommended: your notes' convention, "forward is positive, τ is a signed number, τ = μ·dv/dr", used the same way in every unit and stated at the top.
4. **Speaking script with timing?** Recommended: yes, a word-for-word script for a 6–8 minute video, with a timestamp on each section.
5. **Which "doesn't expect" features?** Recommended: all three below.

---

## The three things he won't expect

**A. Presenter mode inside the app.** It's a teleprompter for each unit: the equation (Write) on one side, what to say (Say) on the other, a step counter and a timer. You press Next to move through the derivation while the plant diagram highlights the unit you're talking about. There's also a **Grill-me toggle** that turns it into a quiz: the app asks the numbered question and reveals the one-line answer only after you click. That's his own format, built into the software.

**B. The twin calibrates itself against real published lab data.** I digitize the measured extraction curve from Moroney et al. (2016, Fig. 5a), which is real experimental data. A Bayesian fit then updates the uncertain model parameters (the diffusion and dissolution time scales) and shows them with error bars, plus the predicted curve with an uncertainty band over the measured points. It's honest about what's measured versus assumed, which his rules demand.

**C. "Professor-standard" compliance checker.** This is an automated test suite that enforces his own written rules on the project:
- every symbol in every equation appears in the symbol table with SI units;
- every equation passes a strict KaTeX parse;
- every physics function is checked for dimensional consistency with a units library (pint), e.g. that Darcy–Weisbach really returns metres of head;
- no model silently extrapolates: out-of-range inputs must raise errors.

The app shows a green "standards" badge listing what passed. Turning his own rules into automated tests is the part most likely to surprise him.

---

## Steps (each reads: action — verify: check)

1. Rewrite every derivation as Write / Say steps, using one sign convention, with "each term in words" and physical checks — verify: strict KaTeX parse, symbol-table check (step 5), and a screenshot of every equation.
2. Build presenter mode and the grill-me toggle in the app — verify: AppTest clicks through every step of every unit with no errors, and a browser screenshot at laptop and phone widths shows no overlap.
3. Digitize Moroney Fig. 5a (vector extraction first if the PDF figure is vector, otherwise a calibrated digitizer) and overlay the points on the original figure — verify: the overlay image visibly matches the source.
4. Bayesian calibration of the time scales to those points (scipy least squares plus a parameter covariance, or a small Markov-chain sampler) — verify: the fit recovers known parameters on synthetic data first, and the real-data fit is shown with error bars and residuals.
5. Build the compliance checker (symbols, KaTeX, units with pint, extrapolation guards) — verify: it fails on a deliberately broken equation, and passes on the real ones.
6. Write the timed 6–8 minute speaking script and update the study guide with the new questions — verify: every script step points to a Write/Say step in the app.
7. Push to GitHub and deploy on Streamlit Cloud (after you install the Claude app on the repo) — verify: the public link opens on a phone, and a full race against the AI runs.

**Smallest success check:** one unit (Stokes settling) fully done in Write / Say format inside presenter mode, passing the symbol and units checks, before the rest are converted.

## Assumptions

- The assignment is a recorded or live explanation, like your pipe flow one, where you write and say each step.
- Your professor will open the app himself, so the phone layout matters.
- Moroney Fig. 5a is the only real measured extraction data we use. It's a drip-filter fine grind, not a French press, and the app says so.

## Facts I'll research myself

Whether the Moroney figure is vector or raster, and the dimensionless scalings needed to convert it back to physical units.

## Push authorization

Already given ("streamlit app and github"). I'll push as soon as the Claude app is installed on smit23ax/ai-barista-plant.
