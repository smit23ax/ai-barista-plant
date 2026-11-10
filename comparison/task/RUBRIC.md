# Scoring (frozen 2026-11-10, before any model run)

## Coding task (100 points)
| Criterion | Points | How measured |
|---|---|---|
| Physics correctness | 40 | Hidden cases (26) via `comparison/score.py`: k, dP, dP_cake, dP_mesh, force, d32, d_s, L_cake, u within rtol 1e-2; Re_b, f_p, inertial_share within 5e-3. Points = 40 x fraction of cases fully passing. Any looked-up output = 0. |
| Frozen tests | 25 | The model's own test file runs and passes (15); invalid inputs raise ValueError as specified (10) |
| SI units and symbols | 15 | Every symbol in docstrings/comments defined with units (reviewer checklist) |
| Rendering | 10 | `sweep.html` at 1400 px and 390 px: no overlaps, axes labelled with units, legend outside |
| Reproducibility | 10 | Runs in a clean environment with requirements.txt pins |

Scored separately for the first response and the final response (after at most two fixed follow-ups).
Lines of code and wall time are reported, not scored.

## Explanation task (10 points)
Correct physics 4 (0.8 each: size distribution/fines, particle shape, porosity/packing, compaction/swelling, constants fitted to sphere beds);
symbols with SI units 2; uses the given numbers correctly 2; separates established from hypothesised 2.

Hidden cases: stored privately; SHA-256 of the file is in `hidden_cases.sha256`, committed before any run.
