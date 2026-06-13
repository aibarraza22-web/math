# An open correlation inequality for cubic graphs without 4- or 8-cycles

**Setting.** G is a finite cubic (3-regular) graph, n = |V(G)|,
containing no cycle of length 4 and no cycle of length 8. For an edge e
and integer L, d_L(e) denotes the number of L-cycles of G through e.

**Problem.** Prove that
    Σ_e d₆(e)·d₁₀(e) ≤ 35·n + O(1).

**What is known (all proved, machine-verified; this repository).**
- d₆(e) ≤ 4 for every edge, and this is sharp. (Two 5-paths closing the
  same hexagon pair either share their second interior vertex or force
  a 4- or 8-cycle.)
- Σ_e d₆(e) ≤ 8.5n + 49 and, at girth 6, Σ_e d₁₀(e) ≤ 32.5n + 961
  (exact non-backtracking-trace identities via Ihara–Bass).
- Hence Σ d₆d₁₀ ≤ 130n + 3844. The problem asks to close a factor ≈ 4.
- Measured on every available C4+C8-free cubic graph (65,000+ graphs,
  24–62 vertices): the sum is 26n–34n; pointwise max of d₆·d₁₀ is 42.

**Falsified routes (with data).**
1. Pointwise: max d₆·d₁₀ = 42 but no constant ≤ ~20 holds; edges with
   d₆ = 4 still carry d₁₀ up to 8, d₆ = 3 up to 14.
2. Opposite-edge transfer: A(f) = Σ_{10-cycles D ∋ f} d₆(opp_D(f)) has
   mean exactly 2/3·(target constant) by rotation identity, but ranges
   8–38: no pointwise slack.
3. Naive hexagon discharging: hexagon density is ≈ 0.4n, so per-hexagon
   charges reach 105 and the discharging identity is tight-to-violated.
4. Spectral moments: tr(B⁴) = tr(B⁸) = 0 cannot improve the d₁₀-side —
   LP optimum 64/64, attained at spectral angles {0, π/5, 2π/5}.

**The shape of the truth.** Average d₁₀ over edges with d₆ = i is
strictly decreasing: 15.7, 15.3, 12.9, 10.3, 6.4 for i = 0…4. The
inequality is a smooth classwise correlation, not a local wall. d₆ is
radius-3 information and d₁₀ radius-5, so the statement is in principle
certifiable by a rooted-edge-ball LP (flag-algebra style discharging) —
infrastructure not yet built; all local lemmas above become constraints.

**Payoff.** With any constant ≤ ≈ 60 in place of 35, the trace-
positivity method of this repository (32·#C16 = tr(B¹⁶) − Θ, with Θ
classified exactly into 39 finite types) yields: every bipartite cubic
graph of girth ≥ 6 with no 8-cycle on n ≲ 30–37 vertices contains a
16-cycle — an Erdős–Gyárfás theorem beyond the exhaustively verified
frontier (n ≤ 24, this repository and Markström 2004), with d₅/d₇
analogues extending to girth 5.
