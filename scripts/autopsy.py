#!/usr/bin/env python3
"""Structural autopsy of the four Markström graphs (24-vertex cubic graphs
with no 4-cycle and no 8-cycle): every invariant we can compute, plus the
features they share."""
import subprocess
import numpy as np
import networkx as nx
from itertools import combinations

graphs = [l.split()[-1] for l in open("results/n24_special.g6") if l.strip()]

def cycle_counts(G, nmax):
    counts = {}
    for c in nx.simple_cycles(G, length_bound=nmax):
        counts[len(c)] = counts.get(len(c), 0) + 1
    return counts

for i, g6 in enumerate(graphs):
    G = nx.from_graph6_bytes(g6.encode())
    n = G.number_of_nodes()
    A = nx.to_numpy_array(G)
    eig = np.sort(np.linalg.eigvalsh(A))
    cc = cycle_counts(G, 24)
    # automorphism group via nauty
    aut = subprocess.run(["nauty-countg", "-a"],
                         input=g6 + "\n", capture_output=True, text=True)
    planar, _ = nx.check_planarity(G)
    tri = [sorted(t) for t in nx.enumerate_all_cliques(G) if len(t) == 3]
    print(f"--- graph {i+1}: {g6}")
    print(f"  girth=3 triangles={len(tri)} {tri}")
    print(f"  planar={planar} bipartite={nx.is_bipartite(G)} "
          f"vertex_conn={nx.node_connectivity(G)} edge_conn={nx.edge_connectivity(G)} "
          f"diam={nx.diameter(G)} radius={nx.radius(G)}")
    print(f"  {aut.stdout.strip()}")
    print(f"  eigenvalues: min={eig[0]:.4f} second={eig[-2]:.4f} "
          f"(3 - lambda2 = {3-eig[-2]:.4f})")
    print(f"  cycle counts by length: {dict(sorted(cc.items()))}")
    # how do the triangles sit? distance between triangles
    if len(tri) >= 2:
        for t1, t2 in combinations(range(len(tri)), 2):
            d = min(nx.shortest_path_length(G, u, v) for u in tri[t1] for v in tri[t2])
            print(f"  dist(triangle{t1+1}, triangle{t2+1}) = {d}")

# pairwise: how similar are the four? common edges under canonical labeling
print("\n--- pairwise canonical comparison")
canon = subprocess.run(["nauty-labelg", "-q"], input="\n".join(graphs) + "\n",
                       capture_output=True, text=True).stdout.split()
for a, b in combinations(range(4), 2):
    Ga = nx.from_graph6_bytes(canon[a].encode())
    Gb = nx.from_graph6_bytes(canon[b].encode())
    common = len(set(map(frozenset, Ga.edges())) & set(map(frozenset, Gb.edges())))
    print(f"  graphs {a+1},{b+1}: {common}/36 edges identical under canonical labels")
