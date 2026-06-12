#!/usr/bin/env python3
"""Cross-validate src/checker against an independent networkx implementation.

For every connected cubic graph on n vertices (including ones with 4-cycles),
compute the smallest power of 2 (>= 4) occurring as a cycle length, using
networkx.simple_cycles with a length bound, and compare with the C checker.
"""
import subprocess
import sys
import networkx as nx

GENG = "nauty-geng"
CHECKER = "src/checker"


def first_power_nx(g6: str) -> int:
    G = nx.from_graph6_bytes(g6.encode())
    n = G.number_of_nodes()
    lengths = set()
    for cyc in nx.simple_cycles(G, length_bound=min(n, 32)):
        lengths.add(len(cyc))
    for p in (4, 8, 16, 32):
        if p in lengths:
            return p
    return 0


def main():
    bad = 0
    total = 0
    for n in sys.argv[1:]:
        gen = subprocess.run(
            [GENG, "-c", "-d3", "-D3", "-q", n],
            capture_output=True, text=True, check=True)
        graphs = gen.stdout.split()
        chk = subprocess.run(
            [CHECKER, "-a"], input=gen.stdout,
            capture_output=True, text=True)
        c_results = [int(line.split()[1]) for line in chk.stdout.splitlines()
                     if line.startswith("G ")]
        assert len(c_results) == len(graphs), (len(c_results), len(graphs))
        for g6, c_val in zip(graphs, c_results):
            nx_val = first_power_nx(g6)
            total += 1
            if nx_val != c_val:
                bad += 1
                print(f"MISMATCH n={n} {g6}: checker={c_val} networkx={nx_val}")
        print(f"n={n}: {len(graphs)} graphs validated")
    print(f"total={total} mismatches={bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
