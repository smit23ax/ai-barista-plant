# Implementation 2: ChatGPT

- Run: 2026-11-10 by alex in ChatGPT. Model name shown in the chat and whether the chat was fresh: **pending from alex**.
  alex uploaded the three files (`ergun_plunge.py`, `test_ergun_plunge.py`, `sweep_page.py`). They are kept here unedited,
  together with the run commands from the end of the reply (`pip install numpy scipy CoolProp plotly pytest`,
  `pytest -v test_ergun_plunge.py`, `python sweep_page.py`). The reply's prose was not pasted.
- Follow-ups used: none so far. This is the **first response**.
- Explanation task: `explanation.md`.

## Score, first response (RUBRIC.md, frozen before the run): 80 / 100

| Criterion | Points | Evidence |
|---|---|---|
| Physics correctness | 40 / 40 | `comparison/score.py` printed `passed 26/26 = 1.000` (hidden-file SHA-256 matches) |
| Frozen tests | 10 / 25 | Own test file: 11 passed, **1 failed** (`test_inertial_share_tends_to_zero`: the share at plunge_time 2e5 s is 1.08e-6, and the test asserts < 1e-6; the physics is right but the threshold is wrong, so the tests were evidently not run) = 0/15. Invalid inputs raise ValueError = 10/10. |
| SI units and symbols | 15 / 15 | Every input and output defined with units in the docstring; inline unit comments |
| Rendering | 5 / 10 | `impl_chatgpt_sweep_desk.png` (1400 px) and `impl_chatgpt_sweep_phone.png` (390 px): no horizontal scroll and axes labelled with units, but **the legend overlaps the title at both widths** (legend placed at y = 1.10 over the title). |
| Reproducibility | 10 / 10 | Clean venv with CoolProp 7.2.0, numpy 2.3.3, plotly 6.3.0, pytest 8.4.2: code runs, sweep.html written (the failing test is scored above) |
| **Total** | **80 / 100** | |

Reported, not scored: 189 lines over the three files; sweep.html embeds plotly.js inline (4.8 MB, works offline).
