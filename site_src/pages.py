"""Page bodies for the submission website. Each function takes the build context and returns HTML.
Math is KaTeX source (\\( \\) inline, $$ $$ display), rendered at build time. Numbers come from ctx["n"]."""
import html

EXP = '<span class="label exp">compared with experimental data</span>'
MODEL = '<span class="label model">model-predicted</span>'
ILLUS = '<span class="label illus">illustrative</span>'


def sci(x, digits=3):
    """KaTeX scientific notation, e.g. 1.09\\times10^{-11}."""
    m, e = f"{x:.{digits - 1}e}".split("e")
    return rf"{m}\times10^{{{int(e)}}}"


def todo(text):
    return f'<div class="todo">{text}</div>'


# ------------------------------------------------------------------ Overview
def index(ctx):
    n, c, items = ctx["n"], ctx["c"], ctx["items"]
    video = (f'<div class="card" style="padding:0;overflow:hidden"><iframe style="width:100%;aspect-ratio:16/9;border:0" '
             f'src="https://www.youtube-nocookie.com/embed/{html.escape(c["video_id"])}" title="Presentation video" allowfullscreen></iframe></div>'
             if c["video_id"] else todo("Upload the 7–8 minute presentation to YouTube and put its video id in <code>site_src/content/youtube_video_id.txt</code>."))
    checks = "".join(f'<li class="{"done" if ok else ""}">{name} <span class="muted">({where})</span></li>' for name, ok, where in items)
    status = ("" if not ctx["missing"] else
              f'<p class="muted">Preview build: {len(ctx["missing"])} of 10 items still need evidence. The final build refuses to run until all ten are ticked.</p>')
    return rf"""
<h1>How does coffee grind size control flow through a packed bed?</h1>
<p class="sub">A French press, treated as a chemical engineering packed bed. Dimensional analysis and the Ergun equation predict how the
grounds resist the plunge, published measurements test the prediction, and an AI optimizer picks the recipe.
<strong>This is an AI project</strong>: the code, the derivations and this site were built with AI models under the group's direction,
and the site documents how, and where the AI was wrong.</p>
<p class="muted">Our professor's framing: <em>"Flow through packed bed ⇒ Ergun equation, dimensional analysis. Apply to some interesting topic (coffee grind size)."</em></p>
{video}

<h2>Main findings</h2>
<div class="grid2">
<div class="card">{EXP}<h3>Ergun over-predicts how easily water flows through real coffee beds</h3>
<p>With our conventions, Ergun's permeability is <strong>{n['c15_min']:.1f}–{n['c15_max']:.0f}×</strong> the value Corrochano et al. (2015)
measured in espresso-style beds (our back-calculation from their data), and <strong>{n['w21']['ratio_ergun']:.0f}×</strong> the value
Wadsworth et al. (2021) measured in a real French press. The model's plunge force is therefore far too low; see
<a href="course.html#experiment">the comparison</a>.</p></div>
<div class="card">{MODEL}<h3>In the model, the fines matter more than the grind setting</h3>
<p>Going from 300 to 1200 µm raises the permeability only from \({sci(n['K300'])}\) to \({sci(n['K1200'])}\ \mathrm{{m^2}}\) (under 2×),
because an assumed 15 % of fines sets most of the surface area. Change the fines fraction instead and the force moves 5×.</p></div>
<div class="card">{MODEL}<h3>The plunge is deep in the viscous regime</h3>
<p>At the standard plunge \(\mathrm{{Re}}_b \approx {n['Re800']:.2f}\), so the inertial term is {100 * n['inert800']:.1f} % of the bed's
pressure drop. The two Ergun terms would only be equal at \(\mathrm{{Re}}_b = 150/1.75 \approx {n['Re_cross']:.0f}\).</p></div>
<div class="card">{MODEL}<h3>The AI optimizer beats simple search, on our own simulator</h3>
<p>In 20 simulated trials with 12 brews each, the Gaussian-process optimizer reached the SCA ideal cup in 20 of 20,
one-factor-at-a-time in 6 and random recipes in 8. This was measured against the project's simulator, not real brews.</p></div>
</div>

<h2>Where each requirement is</h2>
<div class="tablewrap"><table><tr><th>Requirement</th><th>Where</th></tr>
<tr><td>1. Public website, demo and documentation</td><td><a href="demo.html">Demo</a> (instant explorer, full app), and this site</td></tr>
<tr><td>2. YouTube video; practice transcript and AI critique in the comments</td><td>Video above and on <a href="presentation.html">Video &amp; transcript</a></td></tr>
<tr><td>3. Verbatim auto-generated transcript</td><td><a href="presentation.html#transcript">Video &amp; transcript</a></td></tr>
<tr><td>4. Overview, AI process, course content, learnings, references</td><td>This page, <a href="process.html">How it was made</a>, <a href="course.html">Packed bed</a>, <a href="learnings.html">Learnings</a>, <a href="references.html">References</a></td></tr>
<tr><td>5. Plan → critique → accept/reject → two implementations compared</td><td><a href="comparison.html">Model comparison</a></td></tr>
<tr><td>6. Attribution, references, each member's contribution</td><td><a href="references.html">References &amp; credit</a></td></tr>
<tr><td>7. In-class presentations (last day of class and the final exam slot)</td><td><a href="presentation.html#dates">Video &amp; transcript</a>. These are given in person; the site is not a substitute.</td></tr>
</table></div>

<h2>Submission checklist</h2>
<p class="muted">Group project; each member submits separately. The final build of this site checks each item for evidence and refuses to run while any is missing.</p>
<ul class="check">{checks}</ul>
{status}
"""


# ------------------------------------------------------------------ Demo
def demo(ctx):
    n = ctx["n"]
    return rf"""
<h1>Demo</h1>
<p class="sub">Three ways in, fastest first. The explorer below loads instantly and needs nothing installed.</p>

<h2>1 · Grind-size explorer (instant)</h2>
<p>Drag the slider to change the nominal grind size \(d\) (µm). Every value was computed in Python by the project's tested
<code>plunge()</code> model at the 10 µm steps of the app's slider. The page only shows those precomputed numbers: it runs no physics
and does not interpolate. Bed temperature \(T = 341\ \mathrm{{K}}\) (68 °C), the end-of-steep temperature of the default recipe.</p>
<div class="figure">{ctx['figs']['explorer']}
<p class="caption">{MODEL} Permeability \(K\) (m²), pressure drop \(\Delta p\) (Pa) across cake and mesh, plunge force \(F\) (N, fluid resistance only:
no seal friction, buoyancy or acceleration) and the Ergun chart (friction factor \(f_p\) vs bed Reynolds number \(\mathrm{{Re}}_b\), both dimensionless).
The red dots follow the slider. A test checks that every point equals <code>plunge()</code> exactly (a check against transcription errors, not a check of the physics;
<a href="course.html#experiment">that is here</a>).</p></div>

<h2>2 · The full app (Streamlit Cloud)</h2>
<p>Eight views: Plant (process flow diagram), Theory, Trends, Packed bed, Lab notebook, AI operator, Presenter and Engineering notes.
The first open can take about 30 s while the server wakes up.</p>
<p><a class="big" href="{ctx['APP']}">Open the AI Barista Plant app →</a></p>
<p class="muted">The default recipe (800 µm, 93 °C, 240 s, ratio 16.7) gives TDS {100 * n['TDS']:.2f} % and extraction {100 * n['EY']:.1f} %,
just below the SCA ideal box (1.15–1.35 %, 18–22 %). That is on purpose: the AI operator's job is to bring it into the box.</p>

<h2>3 · In-browser app (experimental)</h2>
<p>A WebAssembly build of the same app (stlite, Pyodide 314) is being tested. It downloads Python into the browser, so first load is slow. It will appear here
only if it passes the speed limits set in the plan (desktop under 60 s, phone under 90 s, one AI suggestion under 30 s).</p>
"""


# ------------------------------------------------------------------ Course content
def course(ctx):
    n, w = ctx["n"], ctx["n"]["w21"]
    eps_i = n["eps_implied"]
    return rf"""
<h1>Flow through a packed bed of coffee</h1>
<p class="sub">Dimensional analysis first, then the Ergun equation, then grind size, then the test against measurements.
Full Write/Say derivations: <a href="derivations.html">derivations</a> · <a href="study_guide.html">study guide</a>.</p>

<h2>The physical system</h2>
<p>When the plunger of a French press goes down, the brewed liquid flows up through the mesh and the cake of wet grounds trapped under it.
That cake is a packed bed. In the plunger's frame, liquid passes through it at the superficial velocity
\(u = V_l/(A\,t_p)\), with \(V_l\) the liquid volume pushed through (m³), \(A\) the press cross-section (m²) and \(t_p\) the plunge time (s).
With the model's defaults (\(V_l = 2.3\times10^{{-4}}\ \mathrm{{m^3}}\), 85 mm press, \(t_p = 20\ \mathrm{{s}}\)), \(u \approx 2\ \mathrm{{mm/s}}\). The cake length follows from the dose:
\(L = m_c/(\rho_b A)\), with \(m_c\) the dry coffee mass (kg) and \(\rho_b\) the cake bulk density (kg/m³); 15 g at 400 kg/m³ in an 85 mm press gives \(L \approx 6.6\ \mathrm{{mm}}\).
The plunge force is the fluid resistance of cake and mesh in series, \(F = (\Delta p_\text{{cake}} + \mu u R_m)\,A\), with \(R_m\) the mesh resistance (1/m).
It leaves out seal friction, buoyancy and acceleration, so it is a lower bound on the force a hand feels. At 800 µm the assumed mesh carries {100 * n['mesh_share800']:.0f} % of \(\Delta p\).</p>

<h2 id="pi">1 · Dimensional analysis</h2>
<p>The pressure gradient \(\Delta p/L\) (Pa/m) across a bed depends on the superficial velocity \(u\) (m/s), the grain diameter \(d_s\) (m),
the liquid density \(\rho\) (kg/m³), its viscosity \(\mu\) (Pa·s) and the bed porosity \(\varepsilon\) (–, void volume over bed volume).
Write each in the base dimensions mass M, length L and time T:</p>
<div class="tablewrap"><table><tr><th></th><th>\(\Delta p/L\)</th><th>\(\mu\)</th><th>\(\rho\)</th><th>\(u\)</th><th>\(d_s\)</th><th>\(\varepsilon\)</th></tr>
<tr><td>M</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>L</td><td>−2</td><td>−1</td><td>−3</td><td>1</td><td>1</td><td>0</td></tr>
<tr><td>T</td><td>−2</td><td>−1</td><td>0</td><td>−1</td><td>0</td><td>0</td></tr></table></div>
<p>The matrix has rank 3 (\(\rho, u, d_s\) alone already span M, L and T), so Buckingham's Pi theorem gives \(6 - 3 = 3\) independent groups.
Using \(\rho, u, d_s\) as the repeating variables:</p>
<div class="eqbox">$$\Pi_1 = \frac{{(\Delta p/L)\,d_s}}{{\rho u^2}},\qquad \Pi_2 = \frac{{\rho u d_s}}{{\mu}},\qquad \Pi_3 = \varepsilon$$</div>
<p class="say">Say: a dimensionless pressure gradient, a Reynolds number, and the porosity, which is already dimensionless.
Check \(\Pi_1\): \((\mathrm{{M\,L^{{-2}}T^{{-2}}}})(\mathrm{{L}}) / (\mathrm{{M\,L^{{-3}}}}\cdot\mathrm{{L^2T^{{-2}}}}) = 1\).</p>
<p>Dimensional analysis says \(\Pi_1 = \phi(\Pi_2, \Pi_3)\) but not what \(\phi\) is. Ergun folded the porosity into the other two groups:</p>
<div class="eqbox">$$f_p = \frac{{\Delta p}}{{L}}\,\frac{{d_s}}{{\rho u^2}}\,\frac{{\varepsilon^3}}{{1-\varepsilon}},\qquad \mathrm{{Re}}_b = \frac{{\rho u d_s}}{{\mu(1-\varepsilon)}}$$</div>
<p>so that beds of every porosity fall on one curve \(f_p(\mathrm{{Re}}_b)\). The friction factor \(f_p\) (–) and bed Reynolds number \(\mathrm{{Re}}_b\) (–)
always travel as a pair: textbooks that keep \((1-\varepsilon)\) in \(f\) instead of \(\mathrm{{Re}}\), or that base \(f\) on wetted surface,
have different constants for the same physics.</p>

<h2 id="ergun">2 · The Ergun equation</h2>
<div class="eqbox">$$\frac{{\Delta p}}{{L}} = \underbrace{{\frac{{150\,\mu\,(1-\varepsilon)^2\,u}}{{\varepsilon^3 d_s^2}}}}_{{\text{{viscous (Kozeny–Carman)}}}} + \underbrace{{\frac{{1.75\,\rho\,(1-\varepsilon)\,u^2}}{{\varepsilon^3 d_s}}}}_{{\text{{inertial (Burke–Plummer)}}}}
\quad\Longleftrightarrow\quad f_p = \frac{{150}}{{\mathrm{{Re}}_b}} + 1.75$$</div>
<p class="say">Say: viscous friction in the pores (pores treated as Hagen–Poiseuille tubes sized by the hydraulic radius) plus a fixed number of velocity heads lost per grain.
150 and 1.75 are Ergun's 1952 fit to beds of near-spherical particles; they are fitted constants, not derived ones.</p>
<p><strong>Limits.</strong> As \(\mathrm{{Re}}_b \to 0\) the viscous term dominates and Ergun becomes Darcy's law, \(u = (K/\mu)\,\Delta p/L\), with permeability
\(K = d_s^2\varepsilon^3/[150(1-\varepsilon)^2]\) (m²). As \(\mathrm{{Re}}_b \to \infty\), \(f_p \to 1.75\) (Burke–Plummer). The terms are equal at
\(\mathrm{{Re}}_b = 150/1.75 \approx {n['Re_cross']:.0f}\). The standard plunge sits at \(\mathrm{{Re}}_b \approx {n['Re800']:.2f}\): inertia is {100 * n['inert800']:.1f} % of the cake's pressure drop.</p>
<p><strong>Which diameter.</strong> Coffee grains are irregular and the grind is bimodal, so the model uses the Sauter mean diameter \(d_{{32}}\) (m), the diameter with the
same surface-to-volume ratio as the whole grind, times a sphericity \(\Phi_s = 0.75\) (–) from Corrochano et al.: \(d_s = \Phi_s d_{{32}}\).
The model's grind is two sizes: the nominal grind \(d\) and a fines mass fraction \(w_f = 0.15\) (–) of single coffee cells, 30 µm across:</p>
<div class="eqbox">$$\frac{{1}}{{d_{{32}}}} = \frac{{1-w_f}}{{d}} + \frac{{w_f}}{{d_f}},\qquad d_f = 30\ \mu\mathrm{{m}}$$</div>

<h2 id="grind">3 · What grind size does</h2>
<p>At constant \(\varepsilon\), \(u\), \(L\) and liquid properties, the viscous term scales as \(d_s^{{-2}}\) and the inertial term as \(d_s^{{-1}}\):
halving the grain diameter makes the viscous pressure drop 4× and the inertial one 2×. Real beds break the "constant \(\varepsilon\)" part as the grind changes.</p>
<div class="card">{MODEL} <strong>The fines dominate.</strong> In the model, going from 300 to 1200 µm moves \(K\) only from \({sci(n['K300'])}\) to \({sci(n['K1200'])}\ \mathrm{{m^2}}\)
and the force from {n['F300']:.2f} to {n['F1200']:.2f} N, because the 15 % fines carry most of the surface (\(w_f/d_f \gg (1-w_f)/d\)).
This depends on the assumed, grind-independent \(w_f\); measured fines fractions fall as grinds get coarser, which would make grind size matter more.</div>

<h3>Three "fines" sizes, kept separate</h3>
<ul><li>30 µm: one coffee cell (Moroney et al. 2016), the fines size in the model.</li>
<li>About 70–76 µm: the valley between the two peaks of measured grind distributions (Uman et al. 2016).</li>
<li>100 µm: the fines cut-off used by Cameron et al. (2020).</li></ul>

<h2 id="experiment">4 · Compared with measurements</h2>
<div class="figure">{ctx['figs']['parity']}
<p class="caption">{EXP} Ergun's permeability (viscous limit, \(d_s = 0.75\,d_{{32}}\), each study's own porosity) against measured permeability.
Every point is above the 1:1 line: Ergun over-predicts how easily water gets through coffee.</p></div>
<div class="grid2">
<div class="card"><h3>Corrochano et al. 2015 (espresso-style beds)</h3>
<p>Four grinds at three bulk densities, steady pressure-driven flow at 90 °C. Using their measured \(d_{{32}}\), sphericity and porosity
(porosity digitized from their Fig. 13, 0.11–0.33), Ergun gives {n['c15_min']:.1f}–{n['c15_max']:.0f}× the measured permeability.
Equivalently, the viscous constant that would fit is \(C_\text{{eff}} = {n['c15_Ceff_min']:.0f}\)–\({n['c15_Ceff_max']:.0f}\) instead of 150.
This is <em>our</em> back-calculation; the paper reports its own model's errors (31–521 %) differently.</p></div>
<div class="card"><h3>Wadsworth et al. 2021 (a real French press)</h3>
<p>1 L press (radius 4.75 cm), 54 g coffee, cake porosity 0.53, Sauter radius about 80 µm; lab-fitted permeability
\((1.34\pm0.10)\times10^{{-12}}\ \mathrm{{m^2}}\). Ergun with our conventions predicts \({sci(w['k_ergun'])}\ \mathrm{{m^2}}\), {w['ratio_ergun']:.0f}× too high.
At their lab speed (about \(10^{{-4}}\) m/s; the caption gives \(2.8\times10^{{-4}}\)), Darcy with their permeability gives about {w['F_measured_k']:.0f} N
(they measured about 12.5 N), with Ergun's only {w['F_ergun']:.1f} N. Their recommended 54 g press needs a peak of 32 N; the model's default 15 g press predicts {n['F800']:.1f} N.</p></div>
</div>
<div class="figure">{ctx['figs']['ceff']}
<p class="caption">{EXP} The fitted constant grows with grain size and with packing density. Candidate causes, not yet separated: a single \(d_{{32}}\)
summarizes an increasingly bimodal grind worse; consolidation; swelling; wall effects. A fines "skin" at the filter would predict the opposite trend.</p></div>
<p><strong>Why this matters.</strong> Ergun's form (the \(d_s^{{-2}}\) and \(\varepsilon\) scaling) is a good guide to trends, but its constants come from beds of rigid,
near-spherical, narrowly sized particles. Coffee is irregular, bimodal, porous and soft. The extraction model shows the same pattern independently: the fitted
diffusion time matches Moroney's fine grind (41 s vs 42.2 s) but not the coarse one (647 s vs 270 s), and since \(\tau_d \propto d^2\), one effective size cannot carry both grinds.</p>

<h2 id="validity">5 · Validity and assumptions</h2>
<div class="tablewrap"><table><tr><th>Quantity</th><th>Model</th><th>Evidence</th></tr>
<tr><td>Bed Reynolds number \(\mathrm{{Re}}_b\)</td><td>0.76–1.05 over 300–1200 µm</td><td>Viscous regime; terms equal at 86; Corrochano's beds 0.04–4</td></tr>
<tr><td>Porosity \(\varepsilon\)</td><td>0.40 (assumed)</td><td>The model's own bulk density (400 kg/m³) and grain envelope density ({eps_i['rho_env']:.0f} kg/m³) imply {eps_i['eps']:.2f}.
Espresso-style beds 0.11–0.33 (Corrochano); French press 0.53 (Wadsworth). See the sensitivity chart.</td></tr>
<tr><td>Mesh resistance \(R_m\)</td><td>\(2\times10^8\ \mathrm{{m^{{-1}}}}\) (assumed)</td><td>{100 * n['mesh_share800']:.0f} % of the default pressure drop; not measured</td></tr>
<tr><td>Fines</td><td>15 % by mass at 30 µm, same at every grind (assumed)</td><td>Bimodality is measured (Uman, Cameron); a French-press fines fraction is not published</td></tr>
<tr><td>Where Ergun stops matching coffee</td><td>everywhere it has been tested</td><td>Over-predicts permeability {n['c15_min']:.1f}–{n['c15_max']:.0f}× (Corrochano, espresso-style) and {w['ratio_ergun']:.0f}× (Wadsworth, French press). Leading candidates: porosity, polydispersity, swelling, consolidation</td></tr>
<tr><td>Grain shape</td><td>\(\Phi_s = 0.75\)</td><td>Corrochano, image analysis</td></tr>
<tr><td>Wall effects</td><td>none</td><td>Press diameter / grain ≈ 690</td></tr>
<tr><td>Bed</td><td>fixed thickness, no compaction during the plunge</td><td>Not tested</td></tr>
<tr><td>Force</td><td>fluid resistance only</td><td>Excludes seal friction, buoyancy, acceleration</td></tr>
<tr><td>Temperature</td><td>one value, 341 K</td><td>The bed cools during a real plunge</td></tr></table></div>
<div class="figure">{ctx['figs']['sens']}
<p class="caption">{MODEL} Plunge force at 800 µm when one assumed input changes (dotted line: default, {n['F800']:.2f} N).
The fines fraction and porosity move the answer more than a 4× change in grind does.</p></div>

<h2>Supporting units</h2>
<div class="grid2">
<div class="card"><h3>Extraction (material balance)</h3>
<p>Three pools of solubles (kg): undissolved at the grain surface \(F\), inside the grains \(S\), dissolved in the bulk \(m_l\), with \(F + S + m_l = x_E m_c\) at all times
(\(x_E = 0.30\), extractable mass fraction; \(m_c\), dry coffee mass, kg). Surface dissolution and diffusion out of the grains move solubles between pools (Moroney et al. 2016). {EXP}</p></div>
<div class="card"><h3>Cooling (energy balance)</h3>
<p>Adiabatic mixing of water, grounds and glass, then loss to the room: \(C\,dT/dt = -UA\,(T - T_\infty)\), with \(C\) the heat capacity (J/K), \(UA = 1\ \mathrm{{W/K}}\) (assumed)
and \(T_\infty\) room temperature (K). It sets the 341 K plunge temperature. {MODEL}</p></div>
<div class="card"><h3>Settling of fines (Stokes)</h3>
<p>\(v = (\rho_p - \rho)\,g\,d^2/(18\mu)\), valid for particle Reynolds number below 0.1, with \(\rho_p\) the wet particle density (kg/m³) and \(g\) gravity (m/s²). A 30 µm cell takes minutes to settle through the cup. {MODEL}</p></div>
<div class="card"><h3>Extension: channeling</h3>
<p>Two parallel Darcy paths: a looser 10 % of the area carries a quarter of the flow. Motivated by Cameron et al.'s espresso data, but there is no French-press
measurement, so it is a teaching sketch. {ILLUS}</p></div>
</div>
"""


# ------------------------------------------------------------------ How it was made
def process(ctx):
    return rf"""
<h1>How it was made</h1>
<p class="sub">Every line of code, every derivation and this website were written by AI models. The group chose the topic, rejected directions,
set the rules, supplied the papers and checked the results. This page records who decided what.</p>

<h2>Models and services</h2>
<div class="tablewrap"><table><tr><th>What</th><th>Used for</th><th>Where it ran</th></tr>
<tr><td>Claude (Anthropic), in Claude Code cloud sessions; Claude Opus 5.5 for the submission plan and this site</td><td>Plans v1–v5, all code, tests, derivations, study guide, speaking script, this website</td><td>Cloud (Anthropic-managed containers)</td></tr>
<tr><td>Muse, ChatGPT, Grok</td><td>Critiques of the submission plan; research questions</td><td>Cloud, run by the group in each app</td></tr>
<tr><td>GitHub</td><td>Code and history: <a href="{ctx['REPO']}">{ctx['REPO'].removeprefix("https://")}</a></td><td>Cloud</td></tr>
<tr><td>Streamlit Community Cloud</td><td>The full app</td><td>Cloud</td></tr>
<tr><td>GitHub Pages</td><td>This website</td><td>Cloud</td></tr></table></div>
<p class="muted">Nothing was run on our own computers. The papers we supplied (Moroney, Corrochano, Cameron, Uman) were uploaded to the AI session.
Model versions for the October sessions were not recorded in the plan files, so they are given only as "Claude".</p>
<p><strong>Prompt selection rule.</strong> Every message that changed a plan is listed below with its date. Full plans and critiques are in <a href="records.html">Records</a>, unedited.</p>

<h2>Iterations</h2>
<div class="tablewrap"><table><tr><th>Step</th><th>What the AI had</th><th>Our intervention and reason</th><th>What changed</th><th>How it was checked</th><th>What we learned</th></tr>
<tr><td>2026-10-13</td><td>A physics-informed neural network (PINN) for pipe flow, two notebooks built</td><td>Rejected: our professor already knows PINNs; we wanted something original</td><td>Dropped; kept as background</td><td>—</td><td>A technically impressive idea can still be the wrong project</td></tr>
<tr><td>Plan v1, 10-15</td><td>Coffee as a process: packed bed, mass transfer, heat loss, real brews + AI</td><td>Chose an everyday topic; said we cannot brew in person</td><td>Plan v2: a virtual plant drawn like a control room</td><td>Plan approval gate</td><td>Constraints shape the design as much as the physics does</td></tr>
<tr><td>Plans v2–v3</td><td>Ten units, including pump, NPSH, stirrer, carafe</td><td>"Too extensive": trimmed to the core units</td><td>Extraction, cooling, filtration, Stokes, AI</td><td>Tests per unit</td><td>Breadth is not depth</td></tr>
<tr><td>Plan v4</td><td>Made-up parameters</td><td>Asked for real published data; supplied Moroney 2016</td><td>Extraction model fitted to Moroney's data with uncertainty</td><td>Least squares with a 95 % band; synthetic recovery test</td><td>The AI first misread Moroney as a drip-filter experiment; it is a well-mixed immersion, like a French press</td></tr>
<tr><td>Plan v5</td><td>Darcy filtration as one unit among many</td><td>Passed on our professor's framing: packed bed ⇒ Ergun ⇒ dimensional analysis ⇒ grind size</td><td>Ergun and Buckingham Pi became the core; Corrochano, Cameron, Uman data added</td><td>Pint unit checks, strict KaTeX, symbol audit</td><td>Ergun over-predicts real coffee permeability; that became the main finding, not a bug to hide</td></tr>
<tr><td>Submission plan, 11-05</td><td>Plan v1 for this website</td><td>Sent it to Muse, ChatGPT and Grok for critique, five rounds</td><td>Plan v5 of the website; <a href="comparison.html">decision log</a></td><td>Claude fact-checked every critique against the code</td><td>Critics that saw another critique copied its errors</td></tr>
</table></div>

<h2>Things the AI got wrong, and how they were caught</h2>
<ul>
<li>Read Moroney 2016 as a drip-filter study. Caught when the paper was read in full: it is a well-mixed 60 g / 0.5 L immersion.</li>
<li>Planned to replace CoolProp because "it does not run in the browser". Muse pointed out it does; confirmed in Pyodide's package recipes (CoolProp 7.2.0).</li>
<li>Planned the stlite test on the wrong Pyodide version (0.29). A reviewer asked; the stlite changelog shows 314.0.3.</li>
<li>The master briefing said Buckingham Pi gives "two groups". Reviewers corrected it to three (porosity is the third); the app already said three.</li>
<li>Why not a Rust/WebAssembly calculator like the course example? It would be a second codebase that must agree with the tested Python model. The static explorer gives the same instant, install-free demo from the Python numbers themselves.</li>
<li>Critics also made mistakes: Muse quoted app numbers that were never in the code and withdrew them; one critic said no French-press force measurement exists, but Wadsworth et al. 2021 does.</li>
</ul>
"""


# ------------------------------------------------------------------ Model comparison
def comparison(ctx):
    impl = ctx["c"]["implementations"]
    impl_block = todo("Run the frozen implementation task in a fresh ChatGPT chat (and optionally Muse and Grok), and commit the raw outputs as <code>comparison/raw/impl_&lt;model&gt;.md</code>.") if len(impl) < 2 else "<p>Implementations: " + ", ".join(p.name for p in impl) + "</p>"
    R = ctx["REPO"] + "/blob/main/comparison/"
    return rf"""
<h1>Comparing AI models</h1>
<p class="sub">Two different comparisons: how models <em>critique a plan</em>, and how they <em>implement engineering code</em> under identical conditions.</p>

<h2>Part 1 · Plan and critiques</h2>
<p>Claude Opus 5.5 wrote plan v1 for this website. Muse, ChatGPT and Grok critiqued it, each version was revised, and Claude fact-checked every critique against the repository before accepting or rejecting it.</p>
<div class="tablewrap"><table><tr><th>Round</th><th>Model</th><th>Saw</th><th>Independent?</th><th>Main effect</th></tr>
<tr><td>1</td><td>Muse</td><td>Plan v1</td><td>Yes</td><td>20 points: test CoolProp before replacing it, non-Anthropic second implementer, physics-based comparison task, Streamlit Cloud first</td></tr>
<tr><td>—</td><td>"Grok" (first paste)</td><td>Plan v1 and, apparently, Muse's critique</td><td><strong>No</strong>: near-verbatim copy of Muse, including numbers Muse later withdrew</td><td>Recorded, not counted</td></tr>
<tr><td>—</td><td>Unnamed model</td><td>Plan v1 and Muse's critique</td><td><strong>No</strong>: reworded Muse</td><td>Recorded, not counted</td></tr>
<tr><td>2</td><td>Muse</td><td>Plan v2 + responses</td><td>Yes</td><td>Withdrew its unverified numbers; spike thresholds, schedule, test coverage</td></tr>
<tr><td>2</td><td>ChatGPT</td><td>Plan v1 + Muse's critique</td><td>Yes; said what it could not verify</td><td>Static explorer first, claim labels, sensitivity example, plunge-force definition</td></tr>
<tr><td>3</td><td>Grok, ChatGPT</td><td>Plan v4</td><td>Yes</td><td>"Validated" → "compared with experimental data"; separate critique and implementation comparisons; release checklist</td></tr>
<tr><td>4</td><td>Muse and others</td><td>Plan v5</td><td>Yes</td><td>Fresh sessions, hidden tests, two freezes, tolerances with units</td></tr>
<tr><td>Research</td><td>Grok (A), ChatGPT (B), Muse (C, by elimination)</td><td>Master briefing</td><td>Yes</td><td>Found Wadsworth et al. 2021 (two of three); three Pi groups; porosity/bulk-density link. One reply wrongly said no force measurement exists</td></tr>
</table></div>
<h3>What we noticed</h3>
<ul><li>Models shown another model's critique mostly repeated it, unverified claims included. Models given only the plan produced new, checkable points.</li>
<li>Length and confidence did not predict accuracy: the most detailed research reply missed the one French-press measurement that the shorter ones found.</li>
<li>Every critic invented at least one specific number about the live app that is not in the code. Claude also made errors (CoolProp, Pyodide version, the Pi count) that critics caught.</li></ul>
<p>Every accept/reject decision, with its one-line reason: <a href="{R}site_plan_v2_response_for_muse.md">v2</a> ·
<a href="{R}site_plan_v3_final.md">v3</a> · <a href="{R}site_plan_v4_final.md">v4</a> · <a href="{R}site_plan_v5_final.md">v5</a> ·
<a href="{R}round6_research_review_decisions.md">research round</a>. The critiques themselves are in <a href="records.html">Records</a>.</p>

<h2>Part 2 · Implementations under a frozen protocol</h2>
<p>Each model gets the same written specification of an Ergun plunge and grind-sweep module (not the repository, which contains the answer), in a fresh session with no plan history,
and at most three responses. Primary: a fresh Claude Opus 5.5 session and ChatGPT; optional: Muse and Grok. Hidden tests (inputs 300, 455, 500, 735, 800, 1000, 1200 µm at 333.15, 341 and 353.15 K,
fines fixed at 15 %) are kept private, with only their SHA-256 fingerprint published before any model runs.</p>
<div class="tablewrap"><table><tr><th>Criterion</th><th>Weight</th><th>Pass bar</th></tr>
<tr><td>Physics correctness</td><td>40 %</td><td>\(\Delta p, K, F\) within ±1 %; \(\mathrm{{Re}}_b, f_p\) within ±0.5 %</td></tr>
<tr><td>Frozen tests</td><td>25 %</td><td>All hidden tests pass; none skipped</td></tr>
<tr><td>SI units and symbols</td><td>15 %</td><td>Every symbol defined with units</td></tr>
<tr><td>Rendering</td><td>10 %</td><td>1400 px and 390 px, no overlaps</td></tr>
<tr><td>Reproducibility</td><td>10 %</td><td>Runs from a clean checkout</td></tr></table></div>
<p class="muted">First and final responses are both scored. Lines of code and time are reported, not scored. A separate explanation task
("why can Ergun disagree with measured coffee-bed permeability?") is scored out of 10 on its own.</p>
{impl_block}
"""


# ------------------------------------------------------------------ Video and transcript
def presentation(ctx):
    c = ctx["c"]
    video = (f'<div class="card" style="padding:0;overflow:hidden"><iframe style="width:100%;aspect-ratio:16/9;border:0" '
             f'src="https://www.youtube-nocookie.com/embed/{html.escape(c["video_id"])}" title="Presentation video" allowfullscreen></iframe></div>'
             f'<p><a href="https://www.youtube.com/watch?v={html.escape(c["video_id"])}">Watch on YouTube</a> (the practice transcript and the AI critique are in the comments).</p>'
             if c["video_id"] else todo("Video not uploaded yet. Plan: 7–8 minutes; live parts are the Ergun chart and the grind explorer; upload at least 48 hours before the final freeze with the video language set to English."))
    transcript = (f'<p class="muted">Copied from YouTube\'s auto-generated captions without any edits; recognition errors and timestamps are kept.</p><pre class="transcript">{html.escape(c["transcript"])}</pre>'
                  if c["transcript"] else todo("After upload, open the video on YouTube → ⋯ → Show transcript, copy all of it, and paste it unedited into <code>site_src/content/youtube_transcript.txt</code>. If YouTube produces no transcript, this page will say requirement 3 is unmet instead of substituting one."))
    comments = ("" if c["comments_url"] else todo("Post the practice transcript and the AI critique as numbered comments (1/n, 2/n …, under 10,000 characters each), check they are public from a signed-out browser, and put the video link in <code>site_src/content/youtube_comments_posted.txt</code>."))
    dates = c["dates"] or todo("Add the two in-class presentation dates (last day of class, final exam slot) to <code>site_src/content/presentation_dates.html</code>.")
    return rf"""
<h1>Video and transcript</h1>
{video}
{comments}
<h2 id="transcript">Verbatim auto-generated transcript</h2>
{transcript}
<h2 id="dates">In-class presentations</h2>
{dates}
"""


def learnings(ctx):
    body = ctx["c"]["learnings"] or todo("Each member writes this in their own words (Claude only proofreads spelling and units). Prompts: what surprised you about packed-bed flow? "
                                         "What did dimensional analysis tell you that the equation alone did not? Where did the AI go wrong, and how did you notice? "
                                         "What would you measure next? What do you want to learn more about?")
    return rf"""<h1>What we learned</h1>{body}"""


def references(ctx):
    members = ctx["c"]["members"] or todo("Group project, individual submissions: list each member's name and what they did, in <code>site_src/content/members.html</code>.")
    return rf"""
<h1>References and credit</h1>
<h2>Contributions</h2>
{members}
<div class="tablewrap"><table><tr><th>Who</th><th>Contribution</th></tr>
<tr><td>The group</td><td>Topic, every accept/reject decision, scope cuts, the papers, the critique rounds with other models, video and presentation</td></tr>
<tr><td>Claude (Anthropic)</td><td>All code, tests, derivations, documents and this website; fact-checks of every critique</td></tr>
<tr><td>Muse, ChatGPT, Grok</td><td>Critiques of the submission plan; literature found for the research questions</td></tr>
<tr><td>Cited authors</td><td>All measured data (below)</td></tr></table></div>

<h2>Papers</h2>
<ol>
<li>Ergun, S. (1952). Fluid flow through packed columns. <em>Chem. Eng. Prog.</em> 48, 89–94.</li>
<li>Corrochano, B. R., Melrose, J. R., Bentley, A. C., Fryer, P. J., Bakalis, S. (2015). A new methodology to estimate the steady-state permeability of roast and ground coffee in packed beds. <em>J. Food Eng.</em> 150, 106–116. doi:10.1016/j.jfoodeng.2014.11.006</li>
<li>Moroney, K. M. et al. (2016). Coffee extraction kinetics in a well mixed system. <em>J. Math. Industry</em> 7.</li>
<li>Cameron, M. I. et al. (2020). Systematically improving espresso: insights from mathematical modeling and experiment. <em>Matter</em> 2, 631–648. doi:10.1016/j.matt.2019.12.019</li>
<li>Uman, E. et al. (2016). The effect of bean origin and temperature on grinding roasted coffee. <em>Sci. Rep.</em> 6, 24483. doi:10.1038/srep24483</li>
<li>Wadsworth, F. B. et al. (2021). The force required to operate the plunger on a French press. <em>Am. J. Phys.</em> 89, 769. doi:10.1119/10.0004224</li>
<li>Specialty Coffee Association. Coffee brewing control chart (strength 1.15–1.35 %, extraction 18–22 %).</li>
</ol>
<h2>Software</h2>
<p>Python with streamlit 1.66.0, numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, plotly 7.1.0, scikit-learn 1.9.1, CoolProp 8.0.0 (IAPWS-95 water), pint 0.26.1 (tests);
KaTeX 0.16.22 for equations, rendered at build time. Exact pins: <a href="{ctx['REPO']}/blob/main/requirements.txt">requirements.txt</a>.</p>
"""


def records(ctx):
    R = ctx["REPO"] + "/blob/main/"
    plans = " · ".join(f'<a href="{R}docs/process/plan_v{i}.md">v{i}</a>' for i in range(1, 6))
    return rf"""
<h1>Records</h1>
<p class="sub">Original files, unedited.</p>
<h2>Project plans (October 2026)</h2>
<p>Plans {plans} · assumptions <a href="{R}docs/process/assumptions_v1.md">v1</a>, <a href="{R}docs/process/assumptions_v2.md">v2</a> ·
speaking scripts <a href="{R}docs/process/speaking_script_v1.md">v1</a>, <a href="{R}docs/process/speaking_script_v2.md">v2</a>, <a href="{R}docs/process/speaking_script_v3.md">v3</a> ·
<a href="{R}progress.txt">progress log</a> · <a href="{ctx['REPO']}/commits/main">commit history</a></p>
<h2>Submission plan and critiques (November 2026)</h2>
<ul>
<li>Plan v1 as sent for critique: <a href="{R}comparison/site_plan_v1_for_critique.md">site_plan_v1_for_critique.md</a></li>
<li>Responses and decisions: <a href="{R}comparison/site_plan_v2_response_for_muse.md">v2</a>, <a href="{R}comparison/site_plan_v3_final.md">v3</a>, <a href="{R}comparison/site_plan_v4_final.md">v4</a>, <a href="{R}comparison/site_plan_v5_final.md">v5</a></li>
<li>Plan v5 as sent for the final round: <a href="{R}comparison/site_plan_v5_for_critique.md">site_plan_v5_for_critique.md</a></li>
<li>Master briefing sent to every model: <a href="{R}comparison/master_briefing_all_suggestions.md">master_briefing_all_suggestions.md</a></li>
<li>Research round decisions: <a href="{R}comparison/round6_research_review_decisions.md">round6_research_review_decisions.md</a></li>
<li>Critiques, verbatim: <a href="{ctx['REPO']}/tree/main/comparison/critiques">comparison/critiques/</a></li>
</ul>
"""
