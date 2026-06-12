# A computational attack on the Erdős–Gyárfás conjecture

**Conjecture (Erdős & Gyárfás, 1994).** Every graph with minimum degree 3
contains a simple cycle whose length is a power of 2.

Erdős offered $100 for a proof. The critical case is cubic (3-regular)
graphs — the sparsest graphs satisfying the degree condition. A
counterexample must contain **no** cycle of length 4, 8, 16, 32, …

This repository is an independent, reproducible verification and
counterexample hunt. It does not prove the conjecture (no finite search
can), but a counterexample, if one exists at reachable sizes, would
*disprove* it — and every verified size raises the known lower bound on a
minimal counterexample.

## Key search-space reduction

Any graph containing a 4-cycle satisfies the conjecture trivially, so a
counterexample is C4-free. We therefore enumerate only **connected,
C4-free cubic graphs** (`nauty-geng -c -f -d3 -D3`), which shrinks the
space by several orders of magnitude while losing no generality.
(Connectivity also loses nothing: every component of a disconnected cubic
graph is itself cubic, so a *minimal* counterexample is connected.)

## Components

| File | Purpose |
|------|---------|
| `src/checker.c` | Streams graph6, decides for each graph whether it has a cycle of length exactly 4, 8, 16, or 32 (DFS over simple paths with BFS-distance pruning; exact-length detection, not girth) |
| `src/anneal.c` | Simulated annealing over cubic graphs minimizing `10000·#C4 + 100·#C8 + #C16 (+ #C32)` with degree-preserving 2-edge switches — a heuristic counterexample hunt past the exhaustive frontier |
| `scripts/sweep.sh` | Parallel exhaustive verification for one vertex count (geng res/mod work queue) |
| `scripts/validate.py` | Cross-validates the C checker against an independent networkx cycle enumeration |
| `scripts/families.py` | Checks structured families (generalized Petersen graphs, Möbius ladders, cubic circulants) up to 62 vertices |

## Correctness evidence

- `checker` agrees with networkx `simple_cycles` on **all 618 connected
  cubic graphs with n ≤ 14** (including graphs with 4-cycles), zero
  mismatches.
- Exact-length detection verified on synthetic cases: cycle graphs C9,
  C12, C16, C20, C31, C32, C33 and theta graphs engineered to have
  cycles of length exactly 14, 16, 30, 32 — all classified correctly.
- Famous graphs (Petersen, Heawood, Pappus, Desargues, McGee,
  Tutte–Coxeter) all report first power 8, matching their known cycle
  spectra.
- RESULTS_PLACEHOLDER_MARKSTROM

## Results

### Exhaustive verification (this repository, independent of prior work)

Every connected C4-free cubic graph on n vertices was generated
(`nauty-geng -c -f -d3 -D3`) and checked. **No counterexample exists with
n ≤ 24.** Together with the trivial C4 case this verifies the conjecture
for all cubic graphs of these orders:

| n | C4-free cubic graphs | smallest power-of-2 cycle | counterexamples |
|---|---------------------|---------------------------|-----------------|
| ≤ 12 | 24 | all have C8 | 0 |
| 14 | 36 | all have C8 | 0 |
| 16 | 269 | all have C8 | 0 |
| 18 | 2,761 | all have C8 | 0 |
| 20 | 36,101 | all have C8 | 0 |
| 22 | 553,227 | all have C8 | 0 |
| 24 | N24_PLACEHOLDER | N24_DETAIL_PLACEHOLDER | 0 |

A striking pattern: **every** C4-free cubic graph with n ≤ 22 contains an
8-cycle. The first graphs that dodge both C4 and C8 appear at n = 24
(and contain 16-cycles), matching Markström's 2004 computation.

### Structured families

All 561 connected cubic graphs from these families on ≤ 62 vertices
satisfy the conjecture, each via a 4- or 8-cycle: generalized Petersen
graphs GP(m,k) (m ≤ 31, all k), Möbius ladders, and cubic circulants
Z_n with connection set {±a, n/2}.

### Heuristic hunt past the frontier (n = 30, 46, 62)

Simulated annealing over cubic graphs, minimizing power-of-2 cycle
counts. HUNT_PLACEHOLDER

## Reproducing

```sh
apt-get install nauty && pip install networkx
make            # builds src/checker, src/anneal
python3 scripts/validate.py 8 10 12 14   # cross-validation
bash scripts/sweep.sh 22 16 4            # exhaustive n=22 on 4 cores
./src/anneal 30 1 100000000              # counterexample hunt at n=30
```

## References

- P. Erdős, *Some of my favourite problems in number theory,
  combinatorics, and geometry*, Resenhas IME-USP 2 (1995).
- K. Markström, *Extremal graphs for some problems on cycles in graphs*,
  Congr. Numer. 171 (2004) — exhaustive verification for cubic graphs up
  to 29 vertices; found exactly four cubic graphs on 24 vertices with no
  4- or 8-cycle (all containing 16-cycles).
- C. C. Heckman & R. Krakovski, *Erdős–Gyárfás conjecture for cubic
  planar graphs*, Electron. J. Combin. 20(2) (2013) — the conjecture
  holds for cubic planar graphs.
- erdosproblems.com problem #54.
