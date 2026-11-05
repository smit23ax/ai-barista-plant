# Request: critique this plan for a final-project submission website

I am a chemical engineering undergraduate. Below is (A) my project, (B) the course's submission requirements, and (C) a plan written by Claude (Anthropic, Claude Opus 5.5) to build the final submission website. Please give a **detailed critique and specific improvements** (see section D for exactly what I need).

---

## A. The project

**Title:** AI Barista Plant: flow through a packed bed of coffee grounds (Ergun equation, dimensional analysis, grind size).

**Framing from my professor:** "Flow through a packed bed: Ergun equation, dimensional analysis, applied to an interesting topic (coffee grind size)."

**What exists today**
- Live Streamlit app: https://ai-barista-plant-wx5vazaq38wgr9etvrwzkt.streamlit.app/
- Source code (public GitHub): https://github.com/smit23ax/ai-barista-plant
- A French press is modelled as a small chemical plant (process flow diagram): kettle, press (batch extraction material balance + cooling energy balance), plunger filter (the grounds cake is a packed bed: Ergun equation), cup (Stokes settling of fines).
- Core content: Buckingham Pi dimensional analysis to the packed-bed friction factor and particle Reynolds number; Ergun derived from Kozeny–Carman (viscous) + Burke–Plummer (inertial); grind-size explorer (permeability, plunge force, Reynolds number, extraction time, extraction yield); a channeling unit (two parallel Darcy paths).
- Validation against published data: Corrochano et al. 2015 (measured coffee-bed permeability; Ergun over-predicts it 1.9–16x), Moroney et al. 2016 (extraction kinetics, model calibrated by least squares), Cameron et al. 2020 (espresso grind vs extraction yield), Uman et al. 2016 (grind size distributions).
- AI part: a Gaussian-process Bayesian optimizer (scikit-learn) chooses the next recipe (grind size etc.) and is benchmarked against one-factor-at-a-time and random search.
- App views: Plant, Packed bed, Theory (every derivation as "Write the equation / Say it in words" steps with symbol tables), Presenter, Engineering notes. Automated tests (pytest) check physics, units (pint), symbol definitions and equation rendering.
- Supporting documents: KaTeX-rendered derivations and study guide, speaking script, presentation board guide, an optional in-person bench procedure (syringe permeameter).
- How it was made: entirely with Claude (Anthropic) in a cloud coding environment (Claude Code), over five approved plan versions (v1 to v5) between 2026-10-13 and 2026-10-29. My guidance at each step: rejected a physics-informed neural network idea as too familiar to my professor; chose an everyday topic (coffee); trimmed scope; re-centred on my professor's packed-bed framing; asked for real published data instead of made-up numbers; set the visual style; added a theory page and channeling.

---

## B. Submission requirements (verbatim from the course)

1. Publicly accessible website demo/documentation. There are many options for you to choose from; a standalone WebAssembly build hosted on GitHub Pages is recommended, e.g., https://chetools.github.io/claude/packed-bed-runaway/
2. YouTube video of presentation - include as a link in the project website. Copy and paste (Practice transcript, and AI critique to the comments section). Include the link of the AI project and this submission requirements in your prompt requesting for a detailed critique.
3. Verbatim YouTube auto-generated transcript of the presentation - viewable section of the project website
4. Presentation/Documentation. Overview. Demo what you/AI created. Make it clear that it is an AI project exploring AI capabilities. Explain the process, i.e., AI models, local/cloud services, prompts, etc., used to create it. Focus on the planning, iteration steps where you provided guidance and your reasoning. Explain key technical details of content related to this course and what you learned and what you want to learn more of in the future. Attribution/references.
5. Projects should compare the outcomes using different AI models. After generating a plan from one model, have a different AI model critique and suggest improvements. Justify your decisions on what to accept/reject. Implement the plan using at least 2 different AI models and compare.
6. Attribution/references, and what each group member contributed. Each member must submit the project separately (max of 20 points for each member on groups of up to 4, max of 50 points for individual submission)
7. In class presentations on the last day of class and on scheduled final exam time/location.

---

## C. The plan (written by Claude Opus 5.5)

### Goal
One public website on GitHub Pages that satisfies requirements 1–6 on its own: a working in-browser demo plus every documentation section the course asks for.

### Recommended technical approach
- **Demo:** run the existing Streamlit app fully in the browser with **stlite** (Streamlit compiled to WebAssembly via Pyodide). No server; it works from GitHub Pages like the course example. The existing Streamlit Cloud link stays as a backup.
- **Documentation:** plain static HTML pages next to the demo, with equations pre-rendered by KaTeX at build time (no CDN dependency), same visual style as the app (grid background, serif titles, white cards).
- **Hosting:** a `site/` folder in the repo, deployed by a GitHub Actions workflow to GitHub Pages.

### Site structure (one page per item, shared navigation)
1. **Home / Overview** — what the project is, the one-sentence question ("How does grind size control flow through the coffee bed, and what does that do to the cup?"), a clear statement that this is an AI project exploring AI capabilities, embedded YouTube video.
2. **Demo** — the stlite app (with a loading indicator; first load downloads Python in the browser).
3. **Course content** — dimensional analysis, Ergun, grind size, channeling, material/energy balance links; reuses the existing rendered derivations.
4. **How it was made (AI process)** — models, services (Claude Code cloud sessions, GitHub, Streamlit Cloud, GitHub Pages), the plan timeline v1→v5 with what I asked for and why at each step, representative prompts quoted verbatim, what the AI got wrong and how it was caught (e.g. an early mis-reading of the Moroney experiment as drip filter; Ergun constants not fitting real coffee beds).
5. **Model comparison** — this plan, the other model's critique (pasted verbatim), a table of each suggestion with accept/reject and the reason, and a comparison of the same task implemented by two different models (see below).
6. **Learnings** — what I learned about packed-bed flow and about working with AI, and what I want to learn next.
7. **Transcript** — verbatim YouTube auto-generated transcript (placeholder until the video is posted).
8. **References and contributions** — all papers and software with versions; member contributions.

### Two-model implementation (requirement 5)
- A clearly scoped, identical task given to two models with the same prompt: build the **"How it was made" page plus the Ergun-chart widget** as standalone pieces.
- Model 1: Claude Opus 5.5. Model 2: Claude Sonnet 5.5 (different model, same provider) and, if I run it myself, one non-Anthropic model (e.g. ChatGPT or Gemini).
- Compare on fixed criteria: equations correct and every symbol defined with SI units; numbers match the tested Python model; renders on laptop and phone without overlap; lines of code; number of corrections needed; time taken. Show both outputs side by side; the better one ships, and the reason is stated.

### Build steps (each: action — verify: check)
1. Port the app to stlite: swap CoolProp (not available in the browser) for an in-browser water-property source, keep everything else — verify: water density/viscosity agree with CoolProp within 0.1 % from 20–100 °C in a test; app loads in headless Chromium with no Python exceptions.
2. Build static pages and navigation in the app's style — verify: KaTeX strict-parse passes; screenshots at 1400 px and 390 px with no overlaps.
3. Write the AI-process page from the saved plans v1–v5, commit history and progress log — verify: every claim links to a plan file or a commit.
4. Run the two-model implementation and fill the comparison page — verify: both outputs saved in the repo; the scoring table is filled from measurements, not impressions.
5. Add placeholders for video link, transcript, critique and member contributions, clearly marked — verify: one checklist of what is still missing shown on the home page until filled.
6. GitHub Actions deploy to Pages — verify: the public URL opens on a phone in a fresh browser and the demo runs.

### Assumptions
- Individual submission (no group members) unless told otherwise.
- The repo stays public.
- The existing app's physics and tests are not changed, only made browser-compatible.

### Open questions
- Facts to check: whether every Python dependency (scikit-learn, scipy, pandas, plotly, pint) loads in Pyodide; first-load time of the browser app; whether GitHub Pages needs to be switched on in repo settings by the owner.
- Choices: (a) full stlite demo (more impressive, slower first load) vs a lighter static demo with only the grind-size explorer; (b) second implementation model: Sonnet only, or also a non-Anthropic model.

### Things only I (the student) can do
- Record the presentation and upload it to YouTube; paste the practice transcript and the AI critique into the comments.
- Copy the YouTube auto-generated transcript into the site.
- Run any non-Anthropic model (this critique, and optionally a second implementation).
- Switch on GitHub Pages in the repo settings if required.

---

## D. What I need from you

Please give a **detailed critique** of the plan in section C against the requirements in section B (and with the live app and repo in section A in mind):

1. Which requirements are missed, weakly covered, or at risk? Be specific.
2. Is the technical approach (stlite on GitHub Pages) a good choice? Risks and alternatives.
3. Is the two-model comparison design fair and convincing? How would you improve it?
4. What would make the "AI process" documentation more convincing to a professor who teaches fluid mechanics and likes AI?
5. Anything in the course-content section that is missing or should be cut?
6. A numbered list of concrete improvements, each with a one-line reason, ordered by importance.

Be direct; I will decide which suggestions to accept or reject and justify each decision on the website.
