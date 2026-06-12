/* anneal.c — simulated-annealing hunt for an Erdős–Gyárfás counterexample.
 *
 * Searches the space of cubic (3-regular) graphs on n vertices for one with
 * no cycle of length 4, 8, 16, or 32, by minimizing
 *
 *     f = 10000*(#C4) + 100*(#C8) + (#C16) [+ (#C32) when n >= 32]
 *
 * with random 2-edge-switch moves (the standard degree-preserving rewiring).
 * The expensive long-cycle counts are only computed when the short-cycle
 * counts are already small; otherwise a constant proxy is used, which makes
 * the annealer eliminate short cycles first.
 *
 * Usage: anneal n seed max_iters
 * Prints improvements to stderr; if f reaches 0, prints
 * "COUNTEREXAMPLE <graph6>" to stdout and exits 2.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#define MAXN 62
#define CAP 100000

static int n, nedges;
static uint64_t adj[MAXN];
static int nbr[MAXN][3];
static int deg[MAXN];
static int eu[3*MAXN/2], ev[3*MAXN/2];   /* edge list */
static int dist_s[MAXN];

static uint64_t rng_state;
static uint64_t rng(void) {              /* xorshift64* */
    rng_state ^= rng_state >> 12;
    rng_state ^= rng_state << 25;
    rng_state ^= rng_state >> 27;
    return rng_state * 0x2545F4914F6CDD1DULL;
}
static int rnd(int m) { return (int)(rng() % (uint64_t)m); }

static void bfs(int s) {
    static int q[MAXN];
    for (int i = 0; i < n; i++) dist_s[i] = 1 << 20;
    int head = 0, tail = 0;
    dist_s[s] = 0; q[tail++] = s;
    while (head < tail) {
        int v = q[head++];
        for (int i = 0; i < 3; i++) {
            int w = nbr[v][i];
            if (dist_s[w] > dist_s[v] + 1) { dist_s[w] = dist_s[v] + 1; q[tail++] = w; }
        }
    }
}

static int Lglob, sglob, firstglob;
static long long count_acc;

static void dfs_count(int v, int depth, uint64_t visited) {
    if (depth == Lglob - 1) {
        if ((adj[v] >> sglob & 1) && v > firstglob) count_acc++;
        return;
    }
    if (count_acc >= CAP) return;
    int remaining = Lglob - depth;
    for (int i = 0; i < 3; i++) {
        int w = nbr[v][i];
        if (w <= sglob || (visited >> w & 1)) continue;
        if (dist_s[w] > remaining - 1) continue;
        dfs_count(w, depth + 1, visited | 1ULL << w);
    }
}

static long long count_cycles(int L) {
    count_acc = 0;
    for (int s = 0; s < n && count_acc < CAP; s++) {
        sglob = s; Lglob = L;
        bfs(s);
        for (int i = 0; i < 3; i++) {
            int w = nbr[s][i];
            if (w <= s || dist_s[w] > L - 1) continue;
            firstglob = w;
            dfs_count(w, 1, 1ULL << w);
        }
    }
    return count_acc;
}

#define C16_PROXY 50000LL

static int phase1 = 0;   /* minimize only C4+C8, ignore longer cycles */
static int shortg = 0;   /* if >0: minimize all cycles of length < shortg (girth mode) */

static long long objective(void) {
    if (shortg > 0) {
        long long f = 0;
        for (int L = 3; L < shortg; L++)
            f += (long long)(1 << (shortg - L)) * count_cycles(L);
        return f;
    }
    long long c4 = count_cycles(4);
    long long c8 = count_cycles(8);
    long long f = 10000*c4 + 100*c8;
    if (phase1) return f;
    if (c4 + c8 <= 6) {
        f += count_cycles(16);
        if (n >= 32) f += count_cycles(32);
    } else {
        f += C16_PROXY;
    }
    return f;
}

static void rebuild_from_edges(void) {
    memset(adj, 0, sizeof(adj));
    memset(deg, 0, sizeof(deg));
    for (int e = 0; e < nedges; e++) {
        int a = eu[e], b = ev[e];
        adj[a] |= 1ULL << b; adj[b] |= 1ULL << a;
        nbr[a][deg[a]++] = b; nbr[b][deg[b]++] = a;
    }
}

/* random cubic graph via the pairing model, rejecting loops/multi-edges */
static void random_cubic(void) {
    int stubs[3*MAXN];
    for (;;) {
        int m = 0;
        for (int v = 0; v < n; v++) for (int k = 0; k < 3; k++) stubs[m++] = v;
        for (int i = m - 1; i > 0; i--) { int j = rnd(i+1); int t = stubs[i]; stubs[i] = stubs[j]; stubs[j] = t; }
        memset(adj, 0, sizeof(adj));
        int ok = 1; nedges = 0;
        for (int i = 0; i < m; i += 2) {
            int a = stubs[i], b = stubs[i+1];
            if (a == b || (adj[a] >> b & 1)) { ok = 0; break; }
            adj[a] |= 1ULL << b; adj[b] |= 1ULL << a;
            eu[nedges] = a; ev[nedges] = b; nedges++;
        }
        if (ok) { rebuild_from_edges(); return; }
    }
}

static void print_graph6(FILE *fp) {
    unsigned char buf[600];
    int len = 0;
    buf[len++] = n + 63;
    int bits = 0; unsigned int cur = 0;
    for (int col = 1; col < n; col++)
        for (int row = 0; row < col; row++) {
            cur = (cur << 1) | (unsigned)((adj[row] >> col) & 1);
            if (++bits == 6) { buf[len++] = cur + 63; bits = 0; cur = 0; }
        }
    if (bits) { buf[len++] = (cur << (6 - bits)) + 63; }
    buf[len] = 0;
    fprintf(fp, "%s\n", buf);
}

/* parse a graph6 line into the edge list; returns 0 on success */
static int load_graph6(const char *str) {
    const unsigned char *p = (const unsigned char *)str;
    int nn = *p - 63;
    if (nn != n) return -1;
    p++;
    memset(adj, 0, sizeof(adj));
    nedges = 0;
    unsigned int cur = 0; int curbits = 0;
    for (int col = 1; col < n; col++)
        for (int row = 0; row < col; row++) {
            if (curbits == 0) { if (*p < 63) return -1; cur = *p - 63; curbits = 6; p++; }
            if (cur & (1u << (curbits - 1))) {
                eu[nedges] = row; ev[nedges] = col; nedges++;
            }
            curbits--;
        }
    if (nedges != 3 * n / 2) return -1;
    rebuild_from_edges();
    return 0;
}

static char seedlines[1024][512];
static int nseeds = 0;
static double T0 = 50.0;       /* much colder when starting from seeds */
static int evalmode = 0;

static void init_state(void) {
    if (nseeds > 0) {
        int k = rnd(nseeds);
        if (load_graph6(seedlines[k]) == 0) return;
        fprintf(stderr, "bad seed line %d\n", k);
        exit(1);
    }
    random_cubic();
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: anneal n seed iters [--phase1] [--seeds file]\n");
        return 1;
    }
    n = atoi(argv[1]);
    rng_state = strtoull(argv[2], 0, 10) * 0x9E3779B97F4A7C15ULL + 1;
    long long iters = atoll(argv[3]);
    if (n % 2 || n < 4 || n > MAXN) { fprintf(stderr, "bad n\n"); return 1; }
    for (int i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "--phase1")) phase1 = 1;
        else if (!strcmp(argv[i], "--short") && i + 1 < argc) shortg = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--seeds") && i + 1 < argc) {
            FILE *fp = fopen(argv[++i], "r");
            if (!fp) { perror("seeds"); return 1; }
            while (nseeds < 1024 && fscanf(fp, "%511s", seedlines[nseeds]) == 1) nseeds++;
            fclose(fp);
            fprintf(stderr, "loaded %d seed graphs\n", nseeds);
            T0 = 1.5;
        }
        else if (!strcmp(argv[i], "--T0") && i + 1 < argc) T0 = atof(argv[++i]);
        else if (!strcmp(argv[i], "--eval")) evalmode = 1;
    }

    if (evalmode) {
        /* print the objective of every seed graph and exit */
        for (int k = 0; k < nseeds; k++) {
            if (load_graph6(seedlines[k]) != 0) { fprintf(stderr, "bad seed %d\n", k); continue; }
            printf("%lld %s\n", objective(), seedlines[k]);
        }
        return 0;
    }

    init_state();
    long long f = objective(), best = f;
    double T = T0;
    long long since_improve = 0;
    int beu[3*MAXN/2], bev[3*MAXN/2];     /* best graph seen */
    memcpy(beu, eu, sizeof(beu)); memcpy(bev, ev, sizeof(bev));
    int reheats = 0;

    for (long long it = 0; it < iters; it++) {
        /* pick two disjoint edges and a rewiring */
        int e1 = rnd(nedges), e2 = rnd(nedges);
        int a = eu[e1], b = ev[e1], c = eu[e2], d = ev[e2];
        if (rng() & 1) { int t = c; c = d; d = t; }
        if (a == c || a == d || b == c || b == d) continue;
        if ((adj[a] >> c & 1) || (adj[b] >> d & 1)) continue;

        /* apply switch: (a,b),(c,d) -> (a,c),(b,d) */
        eu[e1] = a; ev[e1] = c; eu[e2] = b; ev[e2] = d;
        rebuild_from_edges();
        long long nf = objective();
        long long delta = nf - f;
        if (delta <= 0 || (double)rng() / (double)UINT64_MAX < exp(-(double)delta / T)) {
            f = nf;
            if (f < best) {
                best = f;
                memcpy(beu, eu, sizeof(beu)); memcpy(bev, ev, sizeof(bev));
                since_improve = 0;
                fprintf(stderr, "iter=%lld T=%.3f best=%lld\n", it, T, best);
                if (best == 0) {
                    if (phase1 || shortg) {
                        /* found a C4+C8-free graph: record it and keep
                         * hunting for more from a fresh start */
                        printf(phase1 ? "C8FREE " : "HIGHGIRTH ");
                        print_graph6(stdout);
                        fflush(stdout);
                        init_state();
                        f = objective(); best = f;
                        memcpy(beu, eu, sizeof(beu)); memcpy(bev, ev, sizeof(bev));
                        T = T0; since_improve = 0;
                        continue;
                    }
                    printf("COUNTEREXAMPLE ");
                    print_graph6(stdout);
                    fflush(stdout);
                    return 2;
                }
            }
        } else {
            /* revert */
            eu[e1] = a; ev[e1] = b; eu[e2] = c; ev[e2] = d;
            rebuild_from_edges();
        }
        since_improve++;
        T *= 0.999995;
        if (T < 0.05) T = 0.05;
        if (since_improve > 400000) {
            /* mostly reheat from the best graph seen; occasionally do a
             * full random restart to keep exploring new basins */
            if (++reheats % 5 == 0) {
                init_state();
                T = T0;
                fprintf(stderr, "iter=%lld RESTART (best so far %lld)\n", it, best);
            } else {
                memcpy(eu, beu, sizeof(beu)); memcpy(ev, bev, sizeof(bev));
                rebuild_from_edges();
                T = T0 < 3.0 ? T0 : 3.0;
                fprintf(stderr, "iter=%lld REHEAT from best=%lld\n", it, best);
            }
            f = objective();
            since_improve = 0;
        }
    }
    fprintf(stderr, "done: best=%lld\n", best);
    return 0;
}
