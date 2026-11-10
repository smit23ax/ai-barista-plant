# Implementation 1: Claude Opus 5.5 (fresh session)

- Run: 2026-11-10, a fresh Claude Code sub-session with no project context. It was given only
  `comparison/task/PROMPT.md` and `comparison/task/public_examples.json` and told to read nothing else.
  Disclosure: it ran in a sandbox with file access and a Python shell, so (unlike a chat model) it could run its own
  tests before answering. It reported reading only the two files.
- Follow-ups used: none. The first response is the final response.
- Files here are its output, unedited: `ergun_plunge.py`, `test_ergun_plunge.py`, `sweep_page.py`.
- Its own stated uncertainties (verbatim): "I put the legend below the plots ("outside the plot" may have meant to the
  right), I never opened sweep.html at 1400 or 390 px wide so readability at those widths is unchecked, and I added input
  checks the prompt didn't ask for (fines_fraction, sphericity, positive sizes/times, R_mesh >= 0)."

## Score (RUBRIC.md, frozen before the run)

| Criterion | Points | Evidence |
|---|---|---|
| Physics correctness | 40 / 40 | `python comparison/score.py .../ergun_plunge.py hidden_cases.json` printed `passed 26/26 = 1.000` (SHA-256 of the hidden file matches `hidden_cases.sha256`) |
| Frozen tests | 25 / 25 | Its 20 tests pass; T = 273/374 K, d <= 0 and eps = 0 or 1 raise ValueError |
| SI units and symbols | 15 / 15 | Every input and output defined with units in the docstring; inline unit comments |
| Rendering | 10 / 10 | `impl_claude_sweep_desk.png` (1400 px) and `impl_claude_sweep_phone.png` (390 px): no overlap, no horizontal scroll, legend below the plots, axes labelled with units. Note, not deducted: the k axis uses plotly's SI tick suffix ("20p" = 20e-12 m^2), which is easy to misread. |
| Reproducibility | 10 / 10 | Clean venv with CoolProp 7.2.0, numpy 2.3.3, plotly 6.3.0, pytest 8.4.2: 20 passed, sweep.html written |
| **Total** | **100 / 100** | |

Reported, not scored: 199 lines over the three files; sweep.html loads plotly from cdn.plot.ly (needs internet to view).
