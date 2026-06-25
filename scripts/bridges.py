#!/usr/bin/env python3
"""Realizability of C-bridges on a nearest-to-16 cycle.

G: 3-connected cubic, no cycle of length 4, 8, or 16.
C: cycle of length L minimizing ||C|-16|, L in {12,13,14,15,17,18,19,20}.

A created cycle length r is FORBIDDEN if r in {4,8,16} (no such cycles in G)
or |r-16| < |L-16| (else C would not be nearest-to-16).  We also never
forbid the length L itself (that's C) and lengths r=3,...,  >=3.
"""
import itertools
import networkx as nx

LS = [12, 13, 14, 15, 17, 18, 19, 20]

def bad(r, L):
    """Is a created cycle of length r forbidden, given nearest-cycle C of length L?"""
    if r < 3:
        return True
    if r in (4, 8, 16):
        return True
    if abs(r - 16) < abs(L - 16):   # strictly closer to 16 than C  => contradicts minimality
        return True
    return False

def bad_set(L, hi=40):
    return sorted(r for r in range(3, hi+1) if bad(r, L))

print("=== Forbidden created-cycle lengths per L (the 'bad set') ===")
for L in LS:
    print(f"  L={L} (dist {abs(L-16)} from 16): bad lengths <=30 = "
          f"{[r for r in bad_set(L) if r<=30]}")

# ---------- allowed single-chord distances ----------
print("\n=== Part I prep: allowed chord cyclic-distances d (chord makes cycles d+1, L-d+1) ===")
allowed_d = {}
for L in LS:
    ad = []
    for d in range(2, L-1):           # d>=2 (d=1 is a C-edge); identify d, L-d
        if d > L - d:
            continue
        c1, c2 = d + 1, L - d + 1
        if not bad(c1, L) and not bad(c2, L):
            ad.append(d)
    allowed_d[L] = ad
    print(f"  L={L}: allowed chord distances d (2..L/2) = {ad}"
          + ("   <-- NONE; no chord can exist" if not ad else ""))

# ================= PART I: chord-only (C Hamiltonian) =================
print("\n================ PART I: chord-only configurations ================")

def cyc_dist(i, j, L):
    d = abs(i - j) % L
    return min(d, L - d)

def search_matchings(L, cap=2_000_000):
    """All perfect matchings of C_L using only allowed chord distances;
    yield those whose graph C_L + M has NO forbidden cycle. Return
    (survivors, n_matchings_examined, capped?)."""
    ad = set(allowed_d[L])
    partner = {i: [j for j in range(L) if j != i and cyc_dist(i, j, L) in ad]
               for i in range(L)}
    survivors = []
    examined = [0]
    capped = [False]
    match = {}
    def cycles_ok():
        G = nx.Graph()
        G.add_edges_from((i, (i+1) % L) for i in range(L))
        G.add_edges_from(match.items())
        for c in nx.simple_cycles(G, length_bound=L):
            if bad(len(c), L):
                return False
        return True
    def bt():
        if capped[0]:
            return
        # lowest unmatched
        u = next((v for v in range(L) if v not in match), None)
        if u is None:
            examined[0] += 1
            if examined[0] > cap:
                capped[0] = True
                return
            if cycles_ok():
                survivors.append(dict(match))
            return
        for w in partner[u]:
            if w in match:
                continue
            match[u] = w; match[w] = u
            bt()
            del match[u]; del match[w]
            if capped[0]:
                return
    bt()
    return survivors, examined[0], capped[0]

print(f"{'L':>3} {'matchings':>10} {'survivors':>10}  {'3-connected survivors'}")
part1 = {}
for L in LS:
    if L % 2 == 1:
        print(f"{L:>3} {'--':>10} {'--':>10}  odd L: no perfect matching -> chord-only IMPOSSIBLE")
        part1[L] = ("impossible-odd", 0, 0)
        continue
    survs, exam, capped = search_matchings(L)
    n3 = 0; sep_examples = []
    for m in survs:
        G = nx.Graph()
        G.add_edges_from((i, (i+1) % L) for i in range(L))
        G.add_edges_from(m.items())
        if nx.node_connectivity(G) >= 3:
            n3 += 1
        else:
            if len(sep_examples) < 1:
                # find a separating pair
                sep_examples.append(nx.node_connectivity(G))
    tag = "" if not capped else " (CAPPED)"
    print(f"{L:>3} {exam:>10} {len(survs):>10}  {n3} survivors are 3-connected{tag}")
    part1[L] = (len(survs), n3, exam)

# ================= PART II: one nontrivial 3-attachment bridge =================
print("\n========= PART II: 3-attachment bridge (a,b,c gaps; d_xy,d_yz,d_zx internal) =========")

def part2(L, dmax=None):
    if dmax is None:
        dmax = L
    survivors = []
    for a in range(1, L-1):
        for b in range(1, L-a):
            c = L - a - b
            if c < 1: continue
            # gaps a,b,c with arcs: x->y = a, y->z = b, z->x = c
            for dxy in range(2, dmax+1):
                # quick: cycles dxy+a, dxy+(L-a)
                if bad(dxy+a, L) or bad(dxy+(L-a), L): continue
                for dyz in range(2, dmax+1):
                    if bad(dyz+b, L) or bad(dyz+(L-b), L): continue
                    for dzx in range(2, dmax+1):
                        if bad(dzx+c, L) or bad(dzx+(L-c), L): continue
                        # metric (triangle) on internal distances
                        if not (dxy+dyz>=dzx and dyz+dzx>=dxy and dzx+dxy>=dyz):
                            continue
                        # tree realizability
                        s = dxy+dyz+dzx
                        if s % 2 != 0: continue
                        al = (dxy+dzx-dyz)//2; be=(dxy+dyz-dzx)//2; ga=(dyz+dzx-dxy)//2
                        if (dxy+dzx-dyz)%2 or (dxy+dyz-dzx)%2 or (dyz+dzx-dxy)%2: continue
                        if al<0 or be<0 or ga<0: continue
                        survivors.append((a,b,c,dxy,dyz,dzx,al,be,ga))
    return survivors

part2res = {}
print(f"{'L':>3} {'#survivors':>11} {'(2,2,2) present?':>17} {'min legs (a,b,g) seen':>22}")
for L in LS:
    s = part2(L)
    part2res[L] = s
    has222 = any(d==(2,2,2) for *_, d in [(x[3:6],) for x in s]) if s else False
    has222 = any((x[3],x[4],x[5])==(2,2,2) for x in s)
    # minimal total leg length (al+be+ga) among survivors = minimal internal tree size
    if s:
        minlegs = min(x[6]+x[7]+x[8] for x in s)
        ex = [x for x in s if x[6]+x[7]+x[8]==minlegs][0]
        legtxt = f"sum={minlegs} e.g. legs=({ex[6]},{ex[7]},{ex[8]}) d=({ex[3]},{ex[4]},{ex[5]})"
    else:
        legtxt = "NONE"
    print(f"{L:>3} {len(s):>11} {str(has222):>17}   {legtxt}")

# ============ PART III: cubicity collapses tree bridges ============
print("\n========= PART III: cubic-realizable tree bridges =========")
print("Fact: a 3-attachment TREE bridge is a tripod with legs (al,be,ga). Internal")
print("leg vertices have tree-degree 2, so cubicity forces every leg length = 1,")
print("i.e. legs=(1,1,1), d=(2,2,2): a SINGLE internal vertex w ~ x,y,z. Longer legs")
print("need extra edges => the bridge stops being a tree.\n")
print(f"{'L':>3}  single-vertex bridge d=(2,2,2) arithmetic-valid gap-triples (a,b,c)")
for L in LS:
    triples = sorted(set((x[0],x[1],x[2]) for x in part2res[L] if (x[3],x[4],x[5])==(2,2,2)))
    # dedupe cyclic/reflection
    canon = sorted(set(tuple(sorted(t)) for t in triples))
    print(f"{L:>3}  count={len(canon):3d}  e.g. {canon[:6]}" if canon else f"{L:>3}  NONE (single-vertex bridge impossible by arithmetic)")

# minimal non-tree cubic bridge = triangle, d=(3,3,3); check arithmetic validity
print("\nMinimal NON-tree cubic 3-attachment bridge = triangle p_x p_y p_z, d=(3,3,3), +3 verts:")
def triangle_ok(L):
    res=[]
    for a in range(1,L-1):
        for b in range(1,L-a):
            c=L-a-b
            if c<1: continue
            cyc=[3+a,3+(L-a),3+b,3+(L-b),3+c,3+(L-c)]
            if not any(bad(x,L) for x in cyc):
                res.append(tuple(sorted((a,b,c))))
    return sorted(set(res))
for L in LS:
    t=triangle_ok(L)
    print(f"  L={L}: d=(3,3,3) valid gap-triples count={len(t)}  e.g. {t[:5]}" if t else f"  L={L}: NONE")

# ============ PART V: explicit 3-connectivity of minimal bridges ============
print("\n========= PART V: 3-connectivity of explicit minimal bridge graphs =========")
def build_singlevertex(L,a,b):
    G=nx.Graph(); G.add_edges_from((i,(i+1)%L) for i in range(L))
    w='w'; x,y,z=0,a,a+b
    G.add_edges_from([(w,x),(w,y),(w,z)])
    return G
def build_triangle(L,a,b):
    G=nx.Graph(); G.add_edges_from((i,(i+1)%L) for i in range(L))
    px,py,pz='px','py','pz'; x,y,z=0,a,a+b
    G.add_edges_from([(px,py),(py,pz),(pz,px),(px,x),(py,y),(pz,z)])
    return G
print(f"{'L':>3} {'bridge':>14} {'(a,b,c)':>10} {'cubic?':>7} {'conn':>5} {'forbidden cycle?':>17}")
for L in [12,15,20]:
    for name,build in [("single-vertex",build_singlevertex),("triangle",build_triangle)]:
        # pick a balanced gap
        a=L//3; b=L//3; c=L-a-b
        G=build(L,a,b)
        cubic=all(d==3 for _,d in G.degree())
        conn=nx.node_connectivity(G)
        badcyc=any(bad(len(cy),L) for cy in nx.simple_cycles(G,length_bound=G.number_of_nodes()))
        print(f"{L:>3} {name:>14} {str((a,b,c)):>10} {str(cubic):>7} {conn:>5} {str(badcyc):>17}")

# ============ PART IV: 4-attachment cubic H-bridge arithmetic ============
print("\n========= PART IV: 4-attachment cubic 'H' bridge (2 internal verts u~{i,j}, v~{k,l}) =========")
print("H-bridge IS internally cubic (u,v have degree 3). Pairing = which 2 attachments share u.")
def part4(L):
    # attachments at 0,a,a+b,a+b+c (positions p0<p1<p2<p3), gaps a,b,c,e sum L
    surv=[]
    for a in range(1,L-2):
        for b in range(1,L-a-1):
            for c in range(1,L-a-b):
                e=L-a-b-c
                if e<1: continue
                pos=[0,a,a+b,a+b+c]
                def arc(i,j):
                    d=(pos[j]-pos[i])%L; return min(d,L-d)
                # three pairings of {0,1,2,3} into 2 pairs sharing internal node
                for pairing in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]:
                    (i,j),(k,l)=pairing
                    cyc=[]
                    # within-pair distance 2, cross-pair distance 3
                    for (p,q),dd in [((i,j),2),((k,l),2),((i,k),3),((i,l),3),((j,k),3),((j,l),3)]:
                        ar=arc(p,q); cyc+= [dd+ar, dd+(L-ar)]
                    if not any(bad(x,L) for x in cyc):
                        surv.append((a,b,c,e,pairing))
    return surv
for L in LS:
    s=part4(L)
    print(f"  L={L}: 4-attachment H-bridge arithmetic survivors={len(s)}"
          + (f"  e.g. gaps={s[0][:4]} pairing={s[0][4]}" if s else "  -> NONE"))

# ============ PART V (corrected): genuinely CUBIC minimal realizations ============
print("\n========= PART V (corrected): cubic 3-connected realizations =========")
print("Cubicity (Fact A): all L legs must be absorbed. Minimal nontrivial model =")
print("one 3-attachment bridge (single vertex w) + perfect matching on the other L-3 legs")
print("(needs L-3 even, i.e. L odd). Search for any forbidden-cycle-free 3-connected one.\n")

def search_onebridge_plus_matching(L, cap=400000):
    """C_L + center w on {0,a,a+b} + perfect matching (allowed chords) on rest.
    Return survivors that are cubic, 3-connected, forbidden-cycle-free."""
    assert (L-3) % 2 == 0
    ad=set(range(2,L-1))  # chords; we'll check cycles on the built graph anyway
    survivors=[]
    examined=[0]; capped=[False]
    # choose attachment triple (0,a,a+b)
    for a in range(2, L-2):
        for b in range(2, L-a-1):
            attach={0,a,a+b}
            rest=[v for v in range(L) if v not in attach]
            # backtrack perfect matching on rest using non-adjacent (cyclic dist>=2) pairs
            match={}
            def cyc_ok():
                G=nx.Graph(); G.add_edges_from((i,(i+1)%L) for i in range(L))
                G.add_edges_from([('w',0),('w',a),('w',a+b)])
                G.add_edges_from(match.items())
                if not all(d==3 for _,d in G.degree()): return None
                for cy in nx.simple_cycles(G,length_bound=G.number_of_nodes()):
                    if bad(len(cy),L): return None
                return G
            def bt():
                if capped[0]: return
                u=next((v for v in rest if v not in match),None)
                if u is None:
                    examined[0]+=1
                    if examined[0]>cap: capped[0]=True; return
                    G=cyc_ok()
                    if G is not None and nx.node_connectivity(G)>=3:
                        survivors.append((a,b,dict(match)))
                    return
                for w2 in rest:
                    if w2==u or w2 in match: continue
                    if cyc_dist(u,w2,L)<2: continue
                    match[u]=w2; match[w2]=u; bt(); del match[u]; del match[w2]
                    if capped[0]: return
            bt()
            if capped[0]: break
        if capped[0]: break
    return survivors, examined[0], capped[0]

for L in [13,15,17,19]:
    survs,exam,capped=search_onebridge_plus_matching(L)
    print(f"  L={L}: examined {exam} cubic covers; 3-connected forbidden-free survivors = {len(survs)}"
          + (" (CAPPED)" if capped else ""))
