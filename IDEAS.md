# Where does the cubic Erdős–Gyárfás problem actually live? A framework map

This session steps outside the campaign's toolkit (non-backtracking
traces, local lemmas, discharging, pointwise bounds), which the
moment-LP death result (`AUDIT.md`) proved is structurally pinned. The
goal is to identify the mathematical field whose tools can see what
traces cannot, generate concrete first lemmas in each candidate field,
and kill the dead ones against the 65,000-graph oracle.

The headline finding: the problem belongs to **extremal cycle-spectrum
theory** — the study of which sets of cycle lengths a graph must realise
(Bondy–Vince, Sudakov–Verstraëte, Liu–Montgomery, Gao–Huo–Liu–Ma) —
attacked by **global path/cycle surgery** (DFS trees, Pósa rotations,
ear induction). This is a field the campaign never touched, it passes
the death-test (its arguments are global, not traces or local counts),
and the data supports its central claim overwhelmingly.

---

## 1. Why the problem is hard — four reasons, each a clue to a field

**R1. The short/long-cycle anticorrelation is invisible to local data.**
The terminal open inequality Σ_e d₆(e)·d₁₀(e) ≤ 35n is true only because
edges rich in 6-cycles are poor in 10-cycles (measured class profile of
avg d₁₀ vs d₆: 15.7, 15.3, 12.9, 10.3, 6.4). No bounded-radius rule sees
this; it is a *global conservation law* trading short-cycle mass for
long-cycle mass. The object that natively encodes a conserved quantity
exchanged between scales is a **filtration / spectral sequence** (length
filtration of the cycle space) or a **transfer operator with a sum rule**
— fields: homological algebra, ergodic/transfer-operator theory.

**R2. Trace mass is pinned at the eigenvalue angles.** tr(B¹⁶) ≈ 2¹⁶ is
forced by the Perron eigenvalue alone, and the moment LP shows the
worst-case spectral measure concentrates at θ ∈ {0, π/5, 2π/5} where
cos16θ, cos10θ = 1. The pinning is a statement about the **universal
cover** (the 3-regular tree): closed-walk growth is (d−1)^L no matter
what, and the question is purely how Γ = π₁(G) folds that growth onto
cycles. Field: **geometric group theory / Bass–Serre theory** (graphs as
T₃/Γ; cycle length = translation length of a hyperbolic element).

**R3. Worst cases never co-occur across the 39 Θ-types.** The
union-bound over types loses a factor 4 precisely because the extremal
configuration for one type structurally excludes the others' extremals
on the same edge. "Constraints whose feasible polytope has no vertex
maximising several objectives at once" is the native setting of **linear
& semidefinite programming / flag algebras** — but the campaign already
identified (and the LP-radius work began) that route; it is local-
certificate-shaped and partially under the death-test shadow.

**R4. Powers of 2 are multiplicatively sparse but cycle lengths combine
additively.** Two cycles sharing a path of length t give a cycle of
length |C₁|+|C₂|−2t: cycle lengths live in a **sumset-like additive
system**, while {2^k} has gaps growing like the values themselves. The
Markström graphs exploit exactly this — "truncation" shifts a length by
+1/+2 per triangle, sliding 8 into the forbidden zone 9–15. The object
is the **set of cycle lengths as an additive/interval structure**; field:
**additive combinatorics & extremal cycle-spectrum theory**. This is R4,
and it is the winner — see §3.

---

## 2. Imported frameworks, with first lemmas and verdicts

Each framework gets a concrete first lemma, a death-test verdict (does it
reduce to a trace / local count / pointwise bound?), and a data-test
verdict (does the oracle support or kill its core claim?).

### (a) Topological / homological — VERDICT: mostly dead, one live thread
*First lemma tried:* "Filter the cycle space Z(G) over Z by length:
Z_{≤ℓ} = span of cycles of length ≤ ℓ. The jump dim Z_{≤2^k} −
dim Z_{<2^k} is forced positive." *Death-test:* over GF(2), length is
invisible (it is a Z-weight, not a GF(2)-class), so pure homology cannot
see powers of 2 — **dead**. The live thread is the *length filtration as
a persistence module* (persistent homology of the graph filtered by
cycle length): the barcode records exactly when each independent cycle
class is born. EG ⟺ some bar is born at a power-of-2 length. *Data-test:*
the bars (new independent cycle lengths) for C4+C8-free graphs are born
densely on [9, c] (this is R4/§3 in persistence language) — **consistent,
but it is the interval phenomenon re-described, not a new mechanism.**

### (b) Probabilistic / entropy — VERDICT: dead
*First lemma tried:* "Bad events A_v = 'the rotation/DFS branch at v
avoids closing a 16-cycle'; apply Lovász Local Lemma to show ∩ Ā_v ≠ ∅."
*Death-test:* LLL/entropy-compression for cycle existence reduces to
bounding local closure probabilities = local walk counts → **trace-like,
dead.** *Data-test:* #C16 is in the hundreds, not a rare-event regime —
LLL is the wrong tool for an abundant structure an adversary nulls.

### (c) Algebraic / 2-adic / polynomial — VERDICT: one genuinely live sub-idea
*First lemma tried (Combinatorial Nullstellensatz):* "is-a-power-of-2" is
not a congruence, so Nullstellensatz cannot target 2^k exactly — **that
form is dead.** *But* the **cycles-modulo-k machinery of Thomassen** (a
graph of min degree 3 has a cycle of length ≡ 0 mod k for many k, proved
by DFS-tree surgery) is genuinely non-trace and global. *Refined first
lemma:* "Every C4+C8-free cubic graph has a cycle of length ≡ 16 mod 16
in the range [9, 31], i.e. exactly 16." *Death-test:* Thomassen's method
is global DFS surgery — **passes.** *Data-test:* supported — but the
mod-k statement that would isolate 16 is essentially the interval claim
again. This sub-idea **merges into the winner**: its toolkit (DFS-tree
surgery) is exactly what §3 needs.

### (d) Regularity / containers — VERDICT: dead for existence
*First lemma tried:* "sparse-regularity-partition a C16-free cubic graph,
derive a density that contradicts." *Death-test:* regularity/containers
yield density and counting statements → local/trace-shaped, and prove
*scarcity*, not *existence* — **wrong direction, dead.**

### (e) Historical analogues — VERDICT: decisive, points at the winner
- *Liu–Montgomery (2020), EG for large average degree:* the surprising
  ingredient was **sublinear expanders + robust path-length adjustment**
  to realise an interval of even cycle lengths. Cubic graphs are too
  sparse for their expander, but the *idea — realise an interval of
  lengths, then a power of 2 is automatically inside —* is exactly R4.
- *Bondy–Vince (1998):* min degree 3 ⟹ two cycles of lengths differing
  by ≤ 2. **Global longest-path surgery, non-trace.**
- *Gao–Huo–Liu–Ma (2022), unified consecutive-cycle-lengths:* min degree
  ≥ k+1 ⟹ k cycles of consecutive even lengths, via DFS-tree "ordered
  fan" surgery. **This is the modern engine for exactly the kind of
  interval statement §3 needs.**

Every historical crack of a cycle-length problem used global surgery on
paths/trees and additive length-combination — never traces. The
campaign's analytic detour was the anomaly.

---

## 3. The winner: the cycle-spectrum interval reframing

**Empirical law (this session, machine-measured).** Let G be a cubic
graph with no 4-cycle and no 8-cycle, and let c(G) be its circumference.
Then the set L(G) of cycle lengths contains **every** integer in
[9, c(G)] — the upper cycle spectrum is gap-free. Evidence:

- All **1517** C4+C8-free cubic graphs on 30 vertices: 1512 have
  L(G) ⊇ [9,30]; the other 5 are non-Hamiltonian with c = 29 and have
  L(G) ⊇ [9,29]. **Zero** graphs miss any length in [9, c].
- n = 36 and n = 48 samples (120 each): every one contains all of
  [9, 18] ⊇ {16}.
- n = 60 adversarial check (60 annealer-generated graphs, the regime
  where gaps would most plausibly appear): every one contains all of
  [9, 16] ⊇ {16} — 0 gaps.
- The four Markström extremal graphs (n = 24): L = [9,24] ∪ {3,6,7}
  (∪{5} for one), i.e. gap-free on [9,24].
- Even girth-9 graphs (n = 62) fill [9,20].
- **Control:** generic cubic graphs (with 4- or 8-cycles) have internal
  spectrum gaps 17% of the time (n = 14). So gap-freeness is *not*
  automatic — forbidding C8 is doing the work. This is the structural
  hypothesis a proof must consume.

**Why this is the whole ballgame.** The reframing converts EG for cubic
graphs into a single interval statement, with no residual constant:

> **Interval Conjecture (IC).** Every 3-connected cubic graph with no
> 4-cycle and no 8-cycle has a cycle of length 16.
>
> (Stronger, data-backed form: it is weakly pancyclic on [9, c], and
> c ≥ 16.)

**Reduction Theorem (proved).** IC implies the Erdős–Gyárfás conjecture
for all cubic graphs.

*Proof.* By the standard reduction (a minimum counterexample to EG has
minimum degree 3 and is 3-connected; cf. Heckman–Krakovski), take G
3-connected cubic. If G contains a 4-cycle or an 8-cycle, its length is a
power of 2 and we are done. Otherwise G is {C4,C8}-free; for n ≤ 24 the
exhaustive verification in this repository (`results/n24/`) already
exhibits a power-of-2 cycle, and for n ≥ 25, IC supplies a 16-cycle. ∎

**This is genuinely non-local.** "Weakly pancyclic on [9,c]" is a
statement about cycles spanning the whole graph; its proofs (Bondy–Vince,
GHLM) use a longest path/cycle and rotations across all of G. It cannot
be reduced to a trace (traces gave only the *count* tr(B¹⁶), pinned and
Θ-corrupted) nor to a local/pointwise bound (the control experiment shows
the property is global — local structure alone permits gaps). It passes
the death-test cleanly.

### 3.1 The girth partition — the two methods tile the cases

A {C4,C8}-free cubic graph has girth in {3,5,6,7} or ≥ 9 (girth 4 and 8
are excluded by hypothesis). This partitions IC:

- **girth ≥ 9:** Theorem A (`THEORY.md` §2) *already proves* a 16-cycle
  for 58 ≤ n ≤ 129 via trace-positivity — and the data shows these
  graphs fill [9,20], consistent with IC. (Open sub-case: girth ≥ 9 with
  n > 129; large and rare.)
- **girth ∈ {3,5,6,7}:** the new surgery target. Here traces fail (Θ
  absorbs the trace, the whole campaign), but the data shows pristine
  gap-free spectra [9,c]. This is precisely the regime for DFS/rotation
  surgery.

The trace method and the surgery method are **complementary, not
competing**: one owns high girth, the other owns low girth, and together
they cover every {C4,C8}-free cubic graph (modulo the large-n high-girth
sliver). This is the cleanest structural statement to come out of the
whole campaign.

### 3.2 Partial progress and the exact stall

*What is immediately available.* Bondy–Vince gives, in any cubic graph,
two cycles whose lengths differ by 1 or 2 — a single rung of the ladder.
The ear-surgery identity is exact: for a cycle C of length ℓ and an ear
(path through V∖C) of length p attaching at arc-distances a and ℓ−a, the
graph contains cycles of lengths ℓ, a+p, and (ℓ−a)+p. Climbing/​filling
the interval requires controlling the multiset of available (a, p) across
all ears — and **this is exactly where C8-freeness should enter and where
the proof currently stalls.**

*The precise stall.* To upgrade "two cycles differing by ≤ 2" (Bondy–
Vince) to "no gaps in [9,c]," one must show: whenever ℓ, ℓ+2 ∈ L(G) with
9 ≤ ℓ < c, also ℓ+1 ∈ L(G). The ear identity produces ℓ+1 from an ear of
the right parity, but a parity obstruction (all relevant ears having even
length difference) is not excluded by the surgery alone. **C8-freeness is
the unused lever:** a graph all of whose ears across a given cycle have
matching parity is forced to contain short even cycles (a 4- or 8-cycle)
by a counting argument that has not been carried out. Stated as the
minimal open lemma:

> **Parity-Bridging Lemma (open).** In a 2-connected cubic graph with no
> 4-cycle and no 8-cycle, for every ℓ with 9 ≤ ℓ < c(G) and ℓ, ℓ+2 ∈
> L(G), the length ℓ+1 ∈ L(G). Data: holds in 1517/1517 n=30 graphs (no
> gap of any size occurs, so in particular no `ℓ,ℓ+2 present, ℓ+1 absent`
> pattern). Mechanism sought: an ear of opposite parity must exist, else
> the parity-uniform ear bundle forces a C4 or C8.

### 3.3 The Hamiltonian special case is a clean chord-diagram problem

When G is Hamiltonian (1512/1517 of the n=30 graphs), G = C_n + a perfect
matching M of "chords," and cycle lengths are the lengths of alternating
cycles in the chord diagram. IC becomes a self-contained statement about
**chord diagrams / circle graphs**:

> A perfect matching on n cyclically-ordered points whose chord diagram
> realises no alternating 4-cycle and no alternating 8-cycle realises
> alternating cycles of every length in [9, n].

This is a concrete, finite-to-state conjecture in the combinatorics of
chord diagrams, a field with its own surgery toolkit (interlacement
graphs, local complementation) entirely disjoint from traces.

---

## 4. Ranked verdict

| Rank | Framework | Death-test | Data-test | Status |
|---|---|---|---|---|
| **1** | **Cycle-spectrum interval / DFS-rotation surgery** (R4, hist. (e)) | **passes** (global surgery) | **strongly supports** (1517/1517 gap-free; 17% control) | **alive; reduces cubic-EG to IC; stall isolated to Parity-Bridging Lemma** |
| 2 | Cycles-mod-k / Thomassen DFS surgery (c) | passes | supports | alive, but merges into #1 (same toolkit) |
| 3 | Geometric group theory / T₃ = universal cover (R2) | partial (length spectrum ↔ trace formula is dead; primitivity is not) | neutral | speculative; the non-trace part (primitive conjugacy classes) unexplored |
| 4 | Persistent homology / length filtration (a) | passes | re-describes #1 | a language for #1, not a new mechanism |
| 5 | Flag-algebra / local LP (R3) | under death-test shadow (local certificate) | supports | the campaign's own next step; complementary to #1 |
| — | Probabilistic/LLL (b); regularity/containers (d); GF(2) homology (a) | **fail** | — | **dead** |

**Bottom line for a working mathematician.** The cubic Erdős–Gyárfás
problem is, after this campaign, an **extremal cycle-spectrum** problem:
prove that forbidding 4- and 8-cycles in a 3-connected cubic graph forces
weak pancyclicity on [9, circumference]. The natural tools are those that
cracked Bondy–Vince and the consecutive-cycle-length conjectures
(Gao–Huo–Liu–Ma): DFS-tree / longest-path surgery, ear induction, and —
in the Hamiltonian case — chord-diagram combinatorics. The single
unproven link is the Parity-Bridging Lemma of §3.2, which is where the
so-far-unused C8-freeness hypothesis must do its work. Traces, the tool
of the entire prior campaign, are provably the wrong field for the
low-girth heart of the problem; they survive only as the high-girth half
of a clean girth partition.
