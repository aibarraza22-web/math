#!/usr/bin/env python3
"""Exact classification of Theta-contributions to tr(B^16).

A tailless non-backtracking closed 16-walk in a C4+C8-free cubic graph of
girth >= 5 that is NOT a 16-cycle traversal has support S satisfying:
  - connected, min degree 2, max degree 3, cycle rank >= 2 (so e >= v+1)
  - e(S) <= 16 (every edge is traversed at least once)
  - girth(S) >= 5, no cycle of length 8 (inherited from the host graph)

This script enumerates ALL such supports via nauty-geng, computes for each
the exact number N16(S) of tailless NB closed 16-walks whose support is
exactly S (Mobius inversion over the lattice of connected min-degree-2
subgraphs, with exact integer Hashimoto-matrix traces), and prints the
classification table.  Then Theta(G) = sum over types of N16(S) * #copies
of S in G — an identity, checkable against the oracle Theta = tr(B^16) -
32*#C16 on real graphs.
"""
import subprocess
import sys
from itertools import combinations
import numpy as np
import networkx as nx


def hashimoto_trace16(G):
    """Exact integer count of tailless NB closed 16-walks in G."""
    darts = [(u, v) for u, v in G.edges()] + [(v, u) for u, v in G.edges()]
    idx = {d: i for i, d in enumerate(darts)}
    k = len(darts)
    B = np.zeros((k, k), dtype=np.int64)
    for (u, v) in darts:
        for w in G[v]:
            if w != u:
                B[idx[(u, v)], idx[(v, w)]] = 1
    P = np.linalg.matrix_power(B, 16)
    return int(np.trace(P))


def min_deg2_connected_sublattice(G):
    """All connected subgraphs of G (as frozensets of edges) with min
    degree >= 2: cycles, closed under union (if connected) and under
    'union of two pieces joined by a simple path'."""
    def ekey(e): return frozenset(e)
    cycles = []
    for c in nx.simple_cycles(G, length_bound=G.number_of_edges()):
        edges = frozenset(ekey((c[i], c[(i + 1) % len(c)])) for i in range(len(c)))
        cycles.append(edges)
    L = set(cycles)
    # close under union/connecting-path until stable
    changed = True
    while changed:
        changed = False
        cur = list(L)
        for X, Y in combinations(cur, 2):
            U = X | Y
            if U in L or len(U) > G.number_of_edges():
                continue
            H = nx.Graph(list(tuple(e) for e in U))
            if nx.is_connected(H):
                if U not in L:
                    L.add(U); changed = True
            else:
                comps = list(nx.connected_components(H))
                # join with a shortest connecting simple path in G
                for paths in _connecting_paths(G, comps):
                    W = U | paths
                    H2 = nx.Graph(list(tuple(e) for e in W))
                    if nx.is_connected(H2) and W not in L and len(W) <= G.number_of_edges():
                        L.add(W); changed = True
    return L


def _connecting_paths(G, comps, maxlen=12):
    """Simple paths in G joining the first two components (as edge sets)."""
    A, B = comps[0], comps[1]
    out = []
    for a in A:
        for b in B:
            for p in nx.all_simple_paths(G, a, b, cutoff=maxlen):
                if all(x not in A | B for x in p[1:-1]):
                    out.append(frozenset(frozenset((p[i], p[i+1])) for i in range(len(p)-1)))
    return out


def N16_exact_support(G):
    """Mobius: walks with support exactly E(G)."""
    full = frozenset(frozenset(e) for e in G.edges())
    L = min_deg2_connected_sublattice(G)
    L.add(full)
    members = sorted(L, key=len)
    N = {}
    for S in members:
        H = nx.Graph(list(tuple(e) for e in S))
        t = hashimoto_trace16(H)
        N[S] = t - sum(N[S2] for S2 in members if S2 < S)
    return N[full]


def enumerate_supports(maxe=16, girth_at_least=5):
    flags = ["-c", "-t", "-f", "-d2", "-D3", "-q"]  # -t -f => girth >= 5
    found = []
    for v in range(5, maxe):
        emin, emax = v + 1, min(maxe, (3 * v) // 2)
        if emin > emax:
            continue
        out = subprocess.run(["nauty-geng", *flags, str(v), f"{emin}:{emax}"],
                             capture_output=True, text=True).stdout.split()
        for g6 in out:
            G = nx.from_graph6_bytes(g6.encode())
            lens = sorted({len(c) for c in nx.simple_cycles(G, length_bound=16)})
            if 8 in lens:
                continue          # support cannot live inside a C8-free host
            if girth_at_least >= 6 and 5 in lens:
                continue
            n16 = N16_exact_support(G)
            if n16 > 0:
                found.append((g6, G.number_of_nodes(), G.number_of_edges(),
                              lens, n16, nx.is_bipartite(G)))
    return found


if __name__ == "__main__":
    girth = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    types = enumerate_supports(girth_at_least=girth)
    print(f"=== supports with N16 > 0 (girth >= {girth}, no C8, e <= 16) ===")
    tot = 0
    for g6, v, e, lens, n16, bip in sorted(types, key=lambda t: -t[4]):
        print(f"N16={n16:6d}  v={v:2d} e={e:2d} cycles={lens} "
              f"{'bipartite' if bip else '':9s} {g6}")
        tot += 1
    print(f"total types: {tot}")
