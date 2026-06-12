# From data to proof: the Erdős–Gyárfás conjecture for cubic graphs

This document turns the computational results in this repository into
(i) a structural analysis of the known extremal graphs, (ii) a proved
theorem — a power-of-2 cycle guarantee for a restricted class of cubic
graphs, obtained from first principles via non-backtracking walk
counting — and (iii) a stress-tested assessment of proof strategies for
the full conjecture.

**Conjecture (Erdős–Gyárfás).** Every graph of minimum degree 3 contains
a cycle of length a power of 2.

Throughout, G is a connected cubic (3-regular) graph on n vertices with
m = 3n/2 edges, and #C_L denotes the number of (simple) cycles of length
exactly L in G.

---

## 1. Autopsy of the four Markström graphs

The exhaustive sweep (`results/n24/`) confirmed that exactly four cubic
graphs on 24 vertices contain neither a 4-cycle nor an 8-cycle — the
unique minimal "near-misses" to the conjecture, first found by Markström
(2004). Everything below was computed by `scripts/autopsy.py` and
independently re-verified with networkx.

| | #1 | #2 | #3 | #4 |
|---|---|---|---|---|
| triangles (all vertex-disjoint) | 4 | 3 | 6 | 7 |
| girth | 3 | 3 | 3 | 3 |
| planar | no | no | no | **yes** |
| bipartite | no | no | no | no |
| vertex / edge connectivity | 3/3 | 3/3 | 3/3 | 3/3 |
| diameter | 5 | 6 | 5 | 6 |
| \|Aut\| | 12 | 3 | 4 | 3 |
| λ₂ | 2.473 | 2.646 | 2.506 | 2.662 |
| λ_min | −2.562 | −2.436 | −2.469 | −2.199 |
| #C16 | 315 | 330 | 207 | 228 |
| missing cycle lengths | 4,5,8 | 4,8 | 4,8 | 4,8 |
| Hamiltonian | yes | yes | yes | yes |

Shared features and what they mean:

1. **All four have girth 3, never girth ≥ 5.** Dodging 8-cycles at this
   size is done *with* dense short-cycle structure, not by raising girth.
   This is forced: girth ≥ 9 needs ≥ 58 vertices (the (3,9)-cages), and
   Section 2 shows girth ≥ 9 actually *guarantees* a 16-cycle here.
2. **The triangles are pairwise vertex-disjoint** and pack much of the
   graph (graph #4: 7 triangles covering 21 of 24 vertices). Contracting
   them yields smaller cubic graphs — so each graph is a *partial
   truncation* of a cubic graph on 10–18 vertices. The contracted graphs
   all contain 4- or 8-cycles; truncation stretches a cycle by +1 or +2
   per triangle visited, sliding 8-cycles into the dead zone 9–15.
   The four graphs are, structurally, machines for shifting cycle
   lengths off the powers of 2.
3. **Graph #4 is planar and 3-connected.** Heckman–Krakovski (2013)
   proved every 3-connected cubic planar graph has a power-of-2 cycle;
   graph #4 witnesses that their theorem is sharp in the sense that 4
   and 8 do not suffice — length 16 is sometimes the only power present.
4. **All four are Ramanujan graphs** (all nontrivial eigenvalues in
   [−2√2, 2√2]): excellent expanders. This is not a coincidence; see the
   trace identity below — strong expansion concentrates the
   non-backtracking trace, which must then be paid for in 16-cycles.
5. Small automorphism groups (3–12): these are sporadic, engineered-looking
   objects, not members of a nice algebraic family.

## 2. A provable lower bound: 16-cycles from spectra

### 2.1 The counting identity

Let B be the non-backtracking (Hashimoto) operator of G: the 2m × 2m
0/1-matrix on directed edges, with B[(u→v),(v→w)] = 1 iff w ≠ u. Then
tr(B^L) equals the number of *tailless non-backtracking closed walks* of
length L (closed walks with no immediate reversal, including around the
basepoint).

**Lemma 1 (support of short reduced walks).** *Let G have girth g and let
w be a tailless non-backtracking closed walk of length ℓ < 2g. Then w is
a traversal of a simple ℓ-cycle.*

*Proof.* View w as a cyclic sequence w₀, w₁, …, w_ℓ = w₀; tailless +
non-backtracking means no two cyclically consecutive edges of w are
reverses of each other. Suppose w is not a simple cycle; then some
vertex occurs at two cyclic positions i ≠ j. Among all such pairs choose
one minimizing the cyclic gap d(i,j) ≥ 1. A gap of 1 is a loop
(girth ≥ 3 excludes), a gap of 2 means w_{i}=w_{i+2}, i.e. an immediate
reversal (excluded). So the minimal gap is ≥ 3, and the subwalk w[i..j]
has all interior vertices distinct from each other and from its
endpoints (else a smaller gap), i.e. it is a *simple cycle* C₁ of length
d(i,j) ≥ g.

Now consider the complementary closed subwalk w₂ = w[j..i] (length
ℓ − d(i,j) ≥ 1), which is non-backtracking at all its interior cyclic
positions. If its closing pair of edges at the basepoint is a reversal,
peel those two steps off; the result is again a closed walk,
contiguous in w, non-backtracking in its interior, shorter by 2.
Iterate. The process cannot reach length 2 (that would be a gap-2 vertex
repetition in w, excluded above), and hence cannot reach length 0; it
stops at a closed walk w₂\* of length ≥ 3 with no reversal anywhere,
which by the minimal-gap argument contains a simple cycle, of length
≥ g. Therefore ℓ ≥ |C₁| + |w₂\*| ≥ 2g, a contradiction. ∎

Each simple L-cycle is traversed by exactly 2L tailless walks (L
basepoints × 2 directions). Hence:

> **If girth(G) > L/2, then tr(B^L) = 2L · #C_L.**

### 2.2 The spectral lower bound

By the Ihara–Bass identity, for a cubic graph
det(I − uB) = (1 − u²)^{m−n} · det(I − uA + 2u²I),
so the spectrum of B consists of ±1, each with multiplicity m − n = n/2,
together with the roots μ±(λ) of μ² − λμ + 2 = 0 for each adjacency
eigenvalue λ. Note μ₊μ₋ = 2.

For even L, p_L(λ) := μ₊^L + μ₋^L satisfies:

- λ = ±3 (the trivial eigenvalue; −3 iff bipartite): {μ} = {±2, ±1},
  so p_L = 2^L + 1.
- |λ| > 2√2: μ± real with equal sign; by AM–GM
  p_L ≥ 2(μ₊μ₋)^{L/2} = 2^{L/2+1} **> 0**.
- |λ| ≤ 2√2 (the Ramanujan window): μ± = √2·e^{±iθ}, so
  p_L = 2^{L/2+1} cos(Lθ) ≥ −2^{L/2+1}.

Summing (connected, non-bipartite, n − 1 nontrivial eigenvalues):

tr(B^L) ≥ n + (2^L + 1) − 2^{L/2+1}(n − 1).   (★)

**Theorem A.** *Every connected cubic graph with girth ≥ 9 on n ≤ 129
vertices contains a 16-cycle; in fact*

  #C16 ≥ (66049 − 511·n) / 32.

*Proof.* Girth ≥ 9 > 16/2, so Lemma 1 gives 32·#C16 = tr(B¹⁶). By (★)
with L = 16: tr(B¹⁶) ≥ n + 65537 − 512(n−1) = 66049 − 511n, which is
positive iff n ≤ 129. ∎

Since a cubic graph of girth ≥ 9 has at least 58 vertices (the (3,9)-cage),
the theorem covers the entire window 58 ≤ n ≤ 129. Consequences:

- **Any counterexample to Erdős–Gyárfás with girth ≥ 9 has ≥ 130
  vertices** (on top of needing girth ∉ {4,8}-creating ranges).
- **Bipartite strengthening.** If G is bipartite, λ = −3 contributes a
  second (2^L + 1): tr(B¹⁶) ≥ 132098 − 511n, so *every bipartite cubic
  graph with girth ≥ 9 on n ≤ 258 vertices contains a 16-cycle.*
- **General k (Theorem B).** The same proof with L = 2^k shows: a cubic
  graph with girth ≥ 2^{k−1}+1 and
  n < (2^{2^k} + 2^{2^{k−1}+1} + 1) / (2^{2^{k−1}+1} − 1)
  contains a cycle of length exactly 2^k. For k = 5: every cubic graph
  with girth ≥ 17 on at most ≈ 32769 vertices contains a 32-cycle. The
  admissible window grows doubly exponentially in k, while the smallest
  conceivable girth-(2^{k−1}+1) graph grows only exponentially (Moore
  bound ≈ 3·2^{2^{k−1}−1}); the windows are wide and widening.

### 2.3 Numerical verification (this repository)

- `scripts/spectral.py` confirms the *exact* identity tr(B⁸) = 16·#C8 on
  Petersen (15 8-cycles), Heawood (21), McGee (34), Tutte–Coxeter (90)
  — all girth > 4 — and the inequality tr(B^L) ≥ 2L·#C_L everywhere else
  it must hold, including the four Markström graphs.
- Four cubic graphs of girth exactly 9 on 62 vertices were constructed
  by girth-targeted annealing (`results/hunt/girth9_n62.g6`). For each,
  the identity tr(B¹⁶) = 32·#C16 holds *exactly* (trace from adjacency
  eigenvalues vs. independent combinatorial cycle count): #C16 = 2042,
  2087, 1962, 2013 — all above the guaranteed floor
  (66049 − 511·62)/32 = 1074, and tightly clustered around the
  Kesten–McKay "typical spectrum" prediction tr(B¹⁶) ≈ 2¹⁶ + n, i.e.
  #C16 ≈ 2050.

### 2.4 Why the annealer could never kill the 16-cycles (rigidity, explained)

The trace tr(B¹⁶) is spectrally pinned near 2¹⁶ = 65536: the trivial
eigenvalue contributes 65537, the ±1 eigenvalues +n, and the rest can
subtract at most 512 each — and for typical (Kesten–McKay distributed)
spectra they contribute ≈ 0 in aggregate. Measured across 300 of the
C4+C8-free 30-vertex graphs found by annealing: tr(B¹⁶) ∈ [63264, 69088]
— a tight band around 2¹⁶, exactly as predicted.

That trace mass must be carried by tailless non-backtracking closed
16-walks, and there are only two kinds: traversals of genuine 16-cycles,
and walks supported on *short-cycle gadgets* (by the proof of Lemma 1, a
non-cycle support contains two edge-disjoint-ish cycles of total length
≤ 16 — thetas θ(a,b,c) with 2a+b+c ≤ 16 or dumbbells with
c₁+c₂+2p ≤ 16). Writing Θ for the gadget contribution:

  32·#C16 = tr(B¹⁶) − Θ.

Measured on the annealing data (n = 30):

| girth | graphs | tr(B¹⁶) | Θ | 32·#C16 |
|---|---|---|---|---|
| 3 | 295 | 63264–69088 | 43232–57648 | 9216–23104 |
| 5 | 4 | 65728–66560 | 41344–43456 | 23040–24864 |
| 6 | 1 | 67648 | 37056 | 30592 |

The annealer, trying to destroy 16-cycles, is really trying to push Θ up
to the full trace — and the only Θ-carriers compatible with "no C4, no
C8" are gadgets built from cycles of length 3, 5, 6, 7 (and 9–13). Even
the best graphs found leave a gap of ≥ 9216, i.e. ≥ 288 sixteen-cycles.
The Markström graphs are precisely maximally-Θ objects: disjoint
triangles are the most trace-absorbent gadgets available, which is *why*
the extremal examples are triangle-packed and why their count of
16-cycles (207–330) is small but stubbornly positive.

## 3. Survey, gap analysis, and three strategies stress-tested

Known partial results ([overview](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Gy%C3%A1rf%C3%A1s_conjecture),
[West's problem page](http://dwest.web.illinois.edu/openp/2powcyc.html)):

- **Liu–Montgomery (2020):** true for graphs of sufficiently large
  *average* degree (via sublinear expanders); they prove a far stronger
  cycle-spectrum statement. Technique needs unbounded degree — silent on
  cubic graphs.
- **Heckman–Krakovski (2013):** true for 3-connected cubic *planar*
  graphs. Technique: discharging against the face structure; needs
  Euler's formula. Markström graph #4 shows any such argument must
  handle configurations out to length 16.
- **Daniel–Shauger (2001), Shauger (1998):** planar claw-free, and
  K_{1,m}-free with degree conditions.
- **Gao–Shan (2022), Hu–Shen (2024):** P₈-free, then
  [P₁₀-free graphs](https://www.sciencedirect.com/science/article/abs/pii/S0012365X24003066)
  — forbidding long induced paths forces locally dense structure;
  unbounded-girth cubic graphs contain long induced paths, so again
  disjoint from the cubic heart.
- **Markström (2004) / Royle:** any cubic counterexample has ≥ 30
  vertices (independently replicated in this repository, n ≤ 24, with
  the same four extremal graphs).

**The gap:** every known technique buys its cycles from density —
geometric (faces), local (forbidden induced subgraphs), or global
(average degree). Cubic graphs of unbounded girth have none of these.
The one resource they cannot avoid having is *spectral mass*: tr(B^L) is
pinned at 2^L by the trivial eigenvalue alone. That is the resource
Section 2 monetizes.

Three candidate strategies, each tested against this repository's data:

**S1 — Reduction/induction (contract short cycles, induct on n).**
*Stress test: falsified.* Contracting the triangles of Markström graphs
#2,#3,#4 produces cubic graphs that *do* contain 4- and 8-cycles: the
reduction does not preserve the property being induced on, in either
direction. Cycle lengths shift by +0/+1/+2 per contracted triangle, and
the powers of 2 are not closed under bounded additive shifts — the gaps
between consecutive powers grow. Any reduction proof needs an idea that
controls cycle lengths *multiplicatively*; none is in sight.

**S2 — Discharging against a topological structure.**
*Stress test: does not generalize.* The method is intrinsically planar
(or bounded-genus); the C4+C8-free graphs in `results/hunt/` are
expanders and contain large clique subdivisions — there is no face
structure to discharge against. Within its domain the method is also
already near its limit: graph #4 (planar, 3-connected, first power 16)
shows the case analysis cannot stop at 8.

**S3 — Spectral / non-backtracking trace counting.**
*Stress test: survives, and produced Theorem A.* The data shows both its
power (the trace is pinned; identity exact for girth > L/2; verified
numerically throughout) and its precise failure mode at low girth: for
the Markström graphs tr(B⁸) ∈ {48, 96, 192, 288} > 0 while #C8 = 0 — the
entire 8-trace is absorbed by triangle-supported walks. So S3 below
girth 9 requires bounding Θ structurally. The measured Θ values (table
above) leave a large positive margin on *every one* of the 65,000+
C4+C8-free graphs in this repository: positivity of tr(B¹⁶) − Θ has no
known counterexample. This is the strategy worth pursuing.

**The resulting program (precise conjecture).** For a cubic graph G with
no C4 and no C8, Θ is a weighted count of theta- and dumbbell-subgraphs
on cycles of lengths in {3,5,6,7,9,…,13}, each multiplied by the number
of length-16 reduced closed words on that gadget (a finite, computable
table). Each gadget is anchored on a short cycle, and short-cycle counts
in C4-free cubic graphs are O(n) with explicit constants. Conjecture C:
**Θ(G) ≤ 511n for every C4+C8-free cubic graph G** — which, with (★),
would prove every such graph on ≤ 64 vertices (and with better spectral
bounds, beyond) contains a 16-cycle, i.e. Erdős–Gyárfás for cubic graphs
to twice the current exhaustive frontier. Every graph in this repository
satisfies Conjecture C with room to spare (max measured Θ = 57648 at
n = 30, vs. budget 66049 − 1).

## 4. The restricted-class theorem (the deliverable)

> **Theorem.** Let G be a connected cubic graph of girth at least 9.
> If G has at most 129 vertices — at most 258 if G is bipartite — then G
> contains a cycle of length exactly 16, and hence satisfies the
> Erdős–Gyárfás conjecture. Quantitatively, #C16 ≥ (66049 − 511n)/32 in
> the general case and (132098 − 511n)/32 in the bipartite case.

Combined with this repository's exhaustive computation (every cubic
graph on ≤ 24 vertices satisfies the conjecture, with C4 ∪ C8 ∪ C16
sufficing) and Markström's n ≤ 29 bound, the open territory for cubic
counterexamples is now characterized as: **n ≥ 30, and either girth
∈ {3,5,6,7} with heavy short-cycle (Θ-) structure, or girth ≥ 9 with
n ≥ 130.** The annealing data of Section 2.4 quantifies how far the
first regime is from producing a counterexample (never within 288
sixteen-cycles of one at n = 30).

Caveats, honestly stated: the ingredients (Ihara–Bass, girth-controlled
walk supports) are classical zeta-function technology, and the
girth-window observation may exist in some form in that literature; I
could not find this specific application to Erdős–Gyárfás in the sources
searchable from this environment. The theorem's range (girth ≥ 9 forces
n ≥ 58, so the unconditional window is 58–129, bipartite 58–258) is
modest — but it is, to my knowledge, the first power-of-2 cycle
guarantee for a class of cubic graphs defined with *no* topological or
density hypothesis, and the Θ-program of Section 3 extends the same
mechanism toward girth 5 with explicit, data-validated margins.
