# Verification log

Aggregated outputs of `scripts/sweep.sh` (exhaustive, isomorph-free
enumeration of connected C4-free cubic graphs via `nauty-geng -c -f -d3 -D3`,
checked by `src/checker`). Raw per-part files are not committed; rerun the
sweep to regenerate.

| n | C4-free cubic graphs | firstC8 | firstC16 | no power-of-2 cycle | wall time (4 cores) |
|---|---------------------|---------|----------|--------------------|---------------------|
| 14 | 36 | 36 | 0 | 0 | <1s |
| 16 | 269 | 269 | 0 | 0 | <1s |
| 18 | 2,761 | 2,761 | 0 | 0 | <1s |
| 20 | 36,101 | 36,101 | 0 | 0 | ~30s |
| 22 | 553,227 | 553,227 | 0 | 0 | 9m10s |
| 24 | (in progress) | | | | |

Structured families (`scripts/families.py`): 561 graphs ≤ 62 vertices
(generalized Petersen, Möbius ladders, cubic circulants) — all satisfy
the conjecture via C4 or C8.

Cross-validation (`scripts/validate.py`): all 4,678 connected cubic
graphs with n ≤ 16 (including those with 4-cycles) agree with an
independent networkx cycle enumeration; plus synthetic exact-length
tests for C16/C32 detection.
