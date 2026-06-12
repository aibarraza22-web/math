#!/usr/bin/env python3
"""Non-backtracking (Hashimoto) walk counts vs. cycle counts.

Ihara–Bass: for a cubic graph, the NB operator B has spectrum
  {+1, -1 each with multiplicity m-n = n/2}
  ∪ {roots of mu^2 - lambda*mu + 2 over adjacency eigenvalues lambda}.
tr(B^L) = number of tailless non-backtracking closed walks of length L.

Lemma (proved in THEORY.md): if girth(G) > L/2, every such walk is a
traversal of a simple L-cycle, so tr(B^L) = 2L * (#C_L).

This script verifies the identity / inequality numerically:
  girth > L/2  ->  tr(B^L) == 2L * #C_L      (exact)
  otherwise    ->  tr(B^L) >= 2L * #C_L      (wraps/thetas are extra)
"""
import sys
import numpy as np
import networkx as nx

def tr_B(G, L):
    lam = np.linalg.eigvalsh(nx.to_numpy_array(G))
    n = G.number_of_nodes()
    total = 2 * (n // 2)  # (+1)^L + (-1)^L for even L, multiplicity n/2 each
    for l in lam:
        disc = complex(l * l - 8)
        sq = np.sqrt(disc)
        mu1, mu2 = (l + sq) / 2, (l - sq) / 2
        total += (mu1 ** L + mu2 ** L).real
    return total

def nC(G, L):
    return sum(1 for c in nx.simple_cycles(G, length_bound=L) if len(c) == L)

def girth(G, cap=20):
    """Girth, provided it is <= cap (returns cap+1 otherwise)."""
    best = cap + 1
    for c in nx.simple_cycles(G, length_bound=min(cap, G.number_of_nodes())):
        best = min(best, len(c))
    return best

if __name__ == "__main__":
    tests = [("Petersen", nx.petersen_graph()),
             ("Heawood", nx.heawood_graph()),
             ("McGee", nx.LCF_graph(24, [12, 7, -7], 8)),
             ("Tutte-Coxeter", nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5))]
    for path in sys.argv[1:]:
        for i, line in enumerate(open(path)):
            g6 = line.split()[-1]
            tests.append((f"{path}:{i+1}", nx.from_graph6_bytes(g6.encode())))
    for name, G in tests:
        g = girth(G)
        for L in (8, 16):
            t = tr_B(G, L)
            c = nC(G, L)
            exact = g > L // 2
            ok = (abs(t - 2 * L * c) < 1e-5) if exact else (t >= 2 * L * c - 1e-5)
            print(f"{name:18s} girth={g:2d} L={L:2d} tr(B^L)={t:12.2f} "
                  f"2L*#C_L={2*L*c:8d} {'EXACT' if exact else 'wraps allowed'} "
                  f"{'OK' if ok else '*** VIOLATION ***'}")
