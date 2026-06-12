#!/usr/bin/env python3
"""Oracle test for the Theta classification.

For a C4+C8-free cubic host graph G of girth >= g, the classification
predicts the identity
    Theta(G) := tr(B^16) - 32*#C16  ==  sum over types T of N16(T)*copies(T,G)
where copies(T,G) counts subgraphs of G isomorphic to T (monomorphic
embeddings / |Aut(T)|).  Any mismatch means the type list is incomplete.

Usage: oracle_check.py <typesfile> <hostfile.g6> [maxhosts]
"""
import sys
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
sys.path.insert(0, 'scripts')
from spectral import tr_B, girth


def load_types(path):
    types = []
    for line in open(path):
        if not line.startswith("N16="):
            continue
        n16 = int(line.split("N16=")[1].split()[0])
        g6 = line.split()[-1]
        T = nx.from_graph6_bytes(g6.encode())
        aut = sum(1 for _ in GraphMatcher(T, T).isomorphisms_iter())
        types.append((g6, T, n16, aut))
    return types


def copies(host, T, autT):
    gm = GraphMatcher(host, T)
    cnt = sum(1 for _ in gm.subgraph_monomorphisms_iter())
    assert cnt % autT == 0, (cnt, autT)
    return cnt // autT


def main():
    types = load_types(sys.argv[1])
    hosts = [l.split()[-1] for l in open(sys.argv[2]) if l.strip()]
    maxh = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    for g6 in hosts[:maxh]:
        G = nx.from_graph6_bytes(g6.encode())
        g = girth(G, cap=16)
        t = tr_B(G, 16)
        c16 = sum(1 for c in nx.simple_cycles(G, length_bound=16) if len(c) == 16)
        theta_true = round(t - 32 * c16)
        theta_pred = 0
        detail = []
        for tg6, T, n16, aut in types:
            cnt = copies(G, T, aut)
            if cnt:
                theta_pred += n16 * cnt
                detail.append(f"{tg6}:{cnt}x{n16}")
        status = "MATCH" if theta_pred == theta_true else "MISMATCH"
        print(f"host girth={g} Theta_true={theta_true} Theta_pred={theta_pred} [{status}]")
        for d in detail:
            print(f"   {d}")


if __name__ == "__main__":
    main()
