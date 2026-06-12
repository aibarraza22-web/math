#!/usr/bin/env python3
"""Analyze 'special' graphs found by the sweep (C16ONLY / COUNTEREXAMPLE
lines): print order, girth, full cycle-length spectrum, bipartiteness,
diameter. Doubles as an independent networkx re-check that the graph
really has no 4- or 8-cycle.

Usage: analyze_special.py file-with-special-lines...
"""
import sys
import networkx as nx

for path in sys.argv[1:]:
    for line in open(path):
        parts = line.split()
        if len(parts) != 2 or parts[0] not in ("C16ONLY", "COUNTEREXAMPLE"):
            continue
        tag, g6 = parts
        G = nx.from_graph6_bytes(g6.encode())
        n = G.number_of_nodes()
        lengths = sorted({len(c) for c in nx.simple_cycles(G, length_bound=n)})
        girth = lengths[0] if lengths else 0
        pow2 = [l for l in lengths if l in (4, 8, 16, 32)]
        status = "RECHECK-FAIL" if (tag == "C16ONLY") != (bool(pow2) and min(pow2) >= 16) else "ok"
        print(f"{tag} n={n} girth={girth} bipartite={nx.is_bipartite(G)} "
              f"diam={nx.diameter(G)} pow2cycles={pow2} [{status}]")
        print(f"  cycle spectrum: {lengths}")
        print(f"  graph6: {g6}")
