# Realizability of C-bridges on a nearest-to-16 cycle

Local realizability analysis for a hypothetical counterexample. **G** is
3-connected cubic with no cycle of length 4, 8, or 16; **C** is a cycle
of length **L** minimizing ‖C|−16|, so L ∈ {12,13,14,15,17,18,19,20}. All
tables are exhaustive finite computations (`scripts/bridges.py`).

A created cycle of length r is **forbidden** if r ∈ {4,8,16} or
|r−16| < |L−16| (the latter would make that cycle nearer to 16 than C,
contradicting minimality). The forbidden ("bad") sets:

| L | dist to 16 | forbidden created-cycle lengths (≤30) |
|---|---|---|
| 12 | 4 | 4,8,13,14,15,16,17,18,19 |
| 13 | 3 | 4,8,14,15,16,17,18 |
| 14 | 2 | 4,8,15,16,17 |
| 15 | 1 | 4,8,16 |
| 17 | 1 | 4,8,16 |
| 18 | 2 | 4,8,15,16,17 |
| 19 | 3 | 4,8,14,15,16,17,18 |
| 20 | 4 | 4,8,13,14,15,16,17,18,19 |

**Standing fact A (cubicity).** Each of the L vertices of C has exactly
one incident edge off C (its *leg*). So the C-bridges' attachment
multiset is exactly V(C): every leg belongs to exactly one bridge, and a
single small bridge never stands alone — the other legs must also be
covered. A nontrivial bridge (with internal vertices) has ≥ 3 attachments
(else its 2 attachments form a 2-cut, violating 3-connectivity).

**Standing fact B (exhaustive base).** Every cubic graph on ≤ 24 vertices
has a 4-, 8-, or 16-cycle (`results/n24/`, this repository: the only
{C4,C8}-free cubic graphs on ≤ 24 vertices are the four Markström graphs
on exactly 24 vertices, and all four contain a 16-cycle). Hence any
counterexample has **n ≥ 25**.

---

## Part I — chord-only configurations: IMPOSSIBLE (rigorous)

If every C-bridge is a chord then C is Hamiltonian, so n = L ≤ 20. By
Fact B no {C4,C8,C16}-free cubic graph that small exists. The matching
enumeration confirms it independently:

| L | perfect matchings (allowed chord-distances) | forbidden-cycle-free survivors |
|---|---|---|
| 12 | 225 | **0** |
| 14 | 5 238 | **0** |
| 18 | 18 915 | **0** |
| 20 | 123 | **0** |
| 13,15,17,19 | — (odd: no perfect matching) | **impossible** |

**Result.** No chord-only counter-configuration exists, for any L. ∎

---

## Part II — one 3-attachment bridge: arithmetic alone is insufficient

Enumerating gap-triples (a,b,c), a+b+c=L, and internal distances
(d_xy,d_yz,d_zx) ∈ [2,L], applying the six forbidden-cycle constraints,
the triangle inequalities, and tree-realizability (α,β,γ ≥ 0 integers):

| L | 12 | 13 | 14 | 15 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|
| arithmetic survivors | 136 | 1098 | 9642 | 45267 | 104259 | 78204 | 62967 | 57219 |

This **confirms the prior negative finding**: pure length arithmetic
(even with metric + tree constraints) leaves thousands of survivors. The
kill must come from cubicity and 3-connectivity, below.

---

## Part III — cubicity collapses tree bridges

A 3-attachment **tree** bridge is a tripod with legs (α,β,γ) meeting at a
centre. Internal leg vertices have tree-degree 2; cubicity forces every
leg length = 1, i.e. **legs (1,1,1), distances (2,2,2): a single internal
vertex w adjacent to x,y,z.** Any longer leg needs an extra edge and the
bridge ceases to be a tree. The minimal **non-tree** cubic 3-attachment
bridge is the **triangle** p_x p_y p_z (3 internal vertices, distances
(3,3,3)). Arithmetic validity of these two shapes:

| L | single-vertex (2,2,2) valid gap-triples | triangle (3,3,3) valid gap-triples |
|---|---|---|
| 12 | 2: (3,4,5),(4,4,4) | 2 |
| 13 | 2: (3,5,5),(4,4,5) | 2 |
| 14 | 2: (3,4,7),(4,5,5) | 3 |
| 15 | 4: (3,4,8),(3,5,7),(4,4,7),(5,5,5) | 4 |
| 17 | 6: (1,4,12),(1,7,9),(1,8,8),(4,4,9),… | 5 |
| 18 | 2: (1,7,10),(1,8,9) | 3 |
| 19 | 2: (1,8,10),(1,9,9) | **0** |
| 20 | **0** | **0** |

**Two clean local results (pure arithmetic, no exhaustive input):**

- **L = 20:** *no* single-vertex bridge and *no* triangle bridge — every
  gap placement creates a forbidden cycle in the band {13,…,19}.
- **L = 19:** no triangle bridge.

For all other L the small bridges survive arithmetic, but each adds only
1 or 3 internal vertices, giving n = L+1 ≤ 21 or n = L+3 ≤ 23 ≤ 24 —
killed by Fact B.

---

## Part IV — 4-attachment H-bridge

The minimal cubic 4-attachment tree is the **H-bridge**: two internal
degree-3 vertices u ~ {two attachments}, v ~ {other two}, u ~ v (2
internal vertices, both cubic). Over all gap-4-compositions of L and all
three pairings, applying the 12 forbidden-cycle constraints:

| L | 12 | 13 | 14 | 15 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|
| H-bridge survivors | 2 | 8 | 18 | 28 | 136 | 26 | **0** | **0** |

**Result.** For **L ∈ {19,20}** no 4-attachment H-bridge exists either.
Combined with Part III, **L = 20 admits none of the three minimal cubic
bridges (single-vertex, triangle, H-bridge), and L = 19 admits no
triangle and no H-bridge** — purely from forbidden-cycle arithmetic.

---

## Part V — 3-connectivity and genuinely cubic minimal realizations

The toy "single bridge" graphs are **not cubic** (Fact A: the other L−3
legs dangle at degree 2). A correct minimal cubic model for odd L is:
one single-vertex 3-attachment bridge **plus a perfect matching on the
remaining L−3 legs** (L−3 even). Exhaustive search for any such graph
that is cubic, 3-connected, and forbidden-cycle-free:

| L | cubic covers examined | 3-connected forbidden-free survivors |
|---|---|---|
| 13 | 14 949 (complete) | **0** |
| 15 | 242 875 (complete) | **0** |
| 17 | 400 000 (capped) | **0** |
| 19 | 400 000 (capped) | **0** |

All such graphs have n = L+1 ≤ 20, so the zeros also follow from Fact B;
the direct search confirms the smallest cubic realizations are
unrealizable.

---

## Part VI — deliverables

### 1. What the previous arithmetic failed to prove
Length arithmetic (one bridge, two crossing bridges, even with metric and
tree-realizability) leaves 10²–10⁵ surviving assignments per L (Part II).
It cannot, by itself, exclude a nearest-to-16 cycle. The missing
ingredients are **cubicity** (Fact A: all L legs must be covered; tree
bridges collapse to a single vertex) and the **exhaustive base** (Fact B:
n ≥ 25).

### 2–3. Realizable vs non-realizable (by bridge type)

| bridge type | internal verts | realizable as a *cubic* counter-config? |
|---|---|---|
| chord-only (Hamiltonian C) | 0 | **No** — n=L≤20 (Fact B); 0 survivors (Part I) |
| single-vertex 3-attach (2,2,2) | 1 | survives arithmetic for L≤19 (none L=20), but n=L+1≤21 → **No** (Fact B; Part V) |
| triangle 3-attach (3,3,3) | 3 | survives arithmetic for L≤18 (none L=19,20), n=L+3≤23 → **No** (Fact B) |
| H-bridge 4-attach | 2 | survives arithmetic for L≤18 (none L=19,20), n=L+2≤22 → **No** (Fact B) |
| k≥4 / large multi-vertex bridges | ≥ 25−L | **not excluded** — see item 5 |

### 4. Candidate lemma (proved by exhaustive arithmetic)

> **Lemma (B-20).** In a 3-connected cubic graph with no 4-, 8-, or
> 16-cycle, a nearest-to-16 cycle C of length 20 has **no** 3-attachment
> bridge with internal distances (2,2,2) or (3,3,3), and **no**
> 4-attachment H-bridge. Equivalently, every bridge on a length-20
> nearest cycle that has ≤ 3 internal vertices and ≤ 4 attachments creates
> a forbidden cycle of length in {13,…,19}.
>
> *Proof.* Finite check over all gap-compositions of 20 and the named
> bridge shapes (Parts III–IV); in each case some created cycle d+gap or
> d+(20−gap) lands in {13,…,19}. ∎

A stronger hybrid statement holds for **all** L ∈ {12,…,20}:

> **Lemma (small-bridge).** A counterexample's nearest-to-16 cycle C
> (L ≤ 20) cannot be covered by bridges of total internal size ≤ 24−L; in
> particular C is not Hamiltonian, and the bridges on C have at least
> 25−L ≥ 5 internal vertices in total. *Proof.* Otherwise n ≤ 24,
> contradicting Fact B. ∎

### 5. Smallest surviving realizable template (the genuine obstruction)

No counter-configuration with a *small* bridge survives: every
single-vertex, triangle, or H-bridge realization has n ≤ 24 and dies by
Fact B, and L=19,20 die already by arithmetic. **The smallest surviving
template is therefore not local at all:** it is any bridge B with
≥ 25−L internal vertices. Such a B is, by 3-connectivity, a cubic graph
with three degree-2 "ports" (the attachment-neighbours) whose internal
cycles avoid C entirely and so must themselves avoid lengths 4, 8, 16 and
the nearness band — i.e. **B is a strictly smaller instance of the same
forbidden-cycle structure.** The bridge analysis does not bottom out
locally: it recurses into a {C4,C8,C16}-free cubic-with-ports subproblem.
This is the precise obstruction — and it is why the realizability attack,
like the trace attack before it, controls the small cases completely but
cannot close the large-bridge regime.

**Honest verdict.** The local realizability attack **rigorously
eliminates** chord-only configurations and all bridges of internal size
≤ 24−L (Parts I–V + Fact B), and eliminates the three minimal cubic
bridge shapes outright for L ∈ {19,20} by arithmetic alone. It **does
not** eliminate large bridges, which recurse to a smaller copy of the
same problem. The smallest possible obstruction is a {C4,C8,C16}-free
cubic 3-port bridge on ≥ 25−L internal vertices.
