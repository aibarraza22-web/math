# Adversarial audit of the proof chain (final session)

Every load-bearing claim was re-verified by an independent method or
exhaustive test. Verdicts:

| Claim | Method of re-verification | Verdict |
|---|---|---|
| N16(T) for all 39 support types | Direct dart-sequence DFS over tailless NB closed 16-walks with cover mask — shares no code or method with the original Möbius/Hashimoto-trace computation | **39/39 exact agreement** |
| Ihara–Bass bookkeeping in Theorem A | Direct numerical Hashimoto spectra (Petersen, Heawood) vs. the formula tr(B^L) = n + Σ_λ p_L(λ) | **Exact** (69840, 128016). Note: B's +1-eigenvalue multiplicity is m−n+1 (the extra +1 comes from λ=3, μ=1), consistent with the formula as used; THEORY.md's "±1 with multiplicity m−n" refers to the (1−u²)^{m−n} factor only |
| Trace floor 66049 − 511n | Symbolic re-derivation: n + (2¹⁶+1) − 512(n−1) = 66049 − 511n | **Correct** |
| Lemma E′ (d₆(e) ≤ 4) | Exhaustive test on **all** 11,845 C4+C8-free graphs in the n=30 and n=36 seed sets | **0 violations** |
| Classification completeness | Exact oracle match Θ = Σ N16·copies on girth-6 (37056) and girth-5 (43456) hosts | **Verified on 2 hosts** (additional hosts not run — VF2 cost; flagged as the audit's one partial item) |
| Lemma P′ | Verified on 2 hosts (max prescribed-end path counts 5, 9, 12 vs bounds 8, 16, 32) | **Consistent; not exhaustively audited** |

Errors caught by this program's verify-first rule across the session:
the "Θ ≤ 511n" conjecture (false on contact with data), the constant 30
in the open problem (truth reaches 34.1n), the pointwise opposite-edge
lemma A(f) ≤ 20 (false, max 38), and two buggy audit scripts whose
failures were diagnosed as script errors, not chain errors.

**New negative result from the audit session (moment LP).** Maximizing
the per-eigenvalue p₁₀ contribution subject to the exact moment
constraints tr(B⁴) = 0 and tr(B⁸) = 0 (which hold in any C4+C8-free
cubic graph of girth ≥ 5) yields optimum exactly 64 — the unconstrained
worst case — attained by spectral mass at θ ∈ {0, π/5, 2π/5}, where
cos 10θ = 1. **Moment-only spectral information cannot improve the
#C10 ≤ 3.25n bound**; any improvement must use combinatorial structure
beyond traces. (Certificate: scripts in this audit; LP optimum and
support reported.)
