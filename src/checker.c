/* checker.c — Erdős–Gyárfás conjecture checker for cubic graphs.
 *
 * Reads graph6 lines on stdin (n <= 62). For each graph, decides whether it
 * contains a cycle whose length is a power of 2 (4, 8, 16, 32).
 *
 * Output (stdout):
 *   COUNTEREXAMPLE <graph6>      — graph with NO power-of-2 cycle
 *   C16ONLY <graph6>             — graph whose only power-of-2 cycles have
 *                                  length >= 16 (interesting near-misses)
 * Summary statistics go to stderr.
 *
 * Cycle-of-exact-length-L test: for each start vertex s (taken as the
 * minimum vertex of the candidate cycle, so the path may only use vertices
 * > s), DFS over simple paths from s, pruning a branch when the BFS
 * distance from the current vertex back to s exceeds the number of edges
 * remaining.  In a cubic graph the branching factor after the first step
 * is at most 2, so the search is small for L <= 16 and the distance
 * pruning keeps L = 32 tractable.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 62

static int n;
static uint64_t adj[MAXN];          /* adjacency bitmasks */
static int nbr[MAXN][MAXN];         /* neighbour lists */
static int deg[MAXN];
static int dist_s[MAXN];            /* BFS distances from current start */

/* ---- graph6 parsing (short form, n <= 62) ---- */
static int parse_graph6(const char *line) {
    const unsigned char *p = (const unsigned char *)line;
    if (*p == '>') return -1;                 /* header, skip */
    int nn = *p - 63;
    if (nn < 1 || nn > MAXN) return -1;
    n = nn;
    memset(adj, 0, sizeof(adj));
    memset(deg, 0, sizeof(deg));
    p++;
    int bitpos = 0, need = n * (n - 1) / 2;
    unsigned int cur = 0; int curbits = 0;
    for (int col = 1; col < n; col++) {
        for (int row = 0; row < col; row++) {
            if (curbits == 0) {
                if (*p < 63) return -1;
                cur = *p - 63; curbits = 6; p++;
            }
            if (cur & (1u << (curbits - 1))) {
                adj[row] |= 1ULL << col;
                adj[col] |= 1ULL << row;
                nbr[row][deg[row]++] = col;
                nbr[col][deg[col]++] = row;
            }
            curbits--; bitpos++;
        }
    }
    (void)bitpos; (void)need;
    return 0;
}

/* BFS distances from s */
static void bfs(int s) {
    static int q[MAXN];
    for (int i = 0; i < n; i++) dist_s[i] = 1 << 20;
    int head = 0, tail = 0;
    dist_s[s] = 0; q[tail++] = s;
    while (head < tail) {
        int v = q[head++];
        for (int i = 0; i < deg[v]; i++) {
            int w = nbr[v][i];
            if (dist_s[w] > dist_s[v] + 1) { dist_s[w] = dist_s[v] + 1; q[tail++] = w; }
        }
    }
}

static int Lglob, sglob, firstglob;
static long long dfs_nodes;

/* DFS: current vertex v, 'depth' vertices placed after s (v included),
 * 'visited' bitmask. Looking for v_{L-1} adjacent to s. Only vertices > s
 * allowed. Returns 1 if a cycle of length exactly L through s is found. */
static int dfs(int v, int depth, uint64_t visited) {
    dfs_nodes++;
    if (depth == Lglob - 1) {
        /* close the cycle: v must be adjacent to s, and break the
         * direction symmetry by requiring v > first vertex of the path */
        return (adj[v] >> sglob & 1) && v > firstglob;
    }
    int remaining = Lglob - depth;   /* edges still to use to get back to s */
    for (int i = 0; i < deg[v]; i++) {
        int w = nbr[v][i];
        if (w <= sglob) continue;
        if (visited >> w & 1) continue;
        if (dist_s[w] > remaining - 1) continue;
        if (dfs(w, depth + 1, visited | 1ULL << w)) return 1;
    }
    return 0;
}

static int has_cycle_len(int L) {
    Lglob = L;
    for (int s = 0; s < n; s++) {
        sglob = s;
        bfs(s);
        for (int i = 0; i < deg[s]; i++) {
            int w = nbr[s][i];
            if (w <= s) continue;
            if (dist_s[w] > L - 1) continue;
            firstglob = w;
            if (dfs(w, 1, 1ULL << w)) return 1;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    int quiet = (argc > 1 && strcmp(argv[1], "-q") == 0);
    int all   = (argc > 1 && strcmp(argv[1], "-a") == 0);  /* per-graph output for validation */
    char line[1024];   /* graph6 for n=62 is ~317 chars */
    long long total = 0, counter = 0;
    long long byfirst[6] = {0};      /* index: 0->C4, 1->C8, 2->C16, 3->C32, 4->none */
    long long need16 = 0;
    while (fgets(line, sizeof(line), stdin)) {
        size_t len = strlen(line);
        while (len && (line[len-1] == '\n' || line[len-1] == '\r')) line[--len] = 0;
        if (!len) continue;
        if (parse_graph6(line) != 0) continue;
        total++;
        int found = -1;
        int powers[4] = {4, 8, 16, 32};
        for (int k = 0; k < 4; k++) {
            int L = powers[k];
            if (L > n) break;
            if (has_cycle_len(L)) { found = k; break; }
        }
        if (all) printf("G %d\n", found == -1 ? 0 : powers[found]);
        if (found == -1) {
            counter++;
            byfirst[4]++;
            printf("COUNTEREXAMPLE %s\n", line);
            fflush(stdout);
        } else {
            byfirst[found]++;
            if (found >= 2) {
                need16++;
                if (!quiet) { printf("C16ONLY %s\n", line); fflush(stdout); }
            }
        }
        if (total % 10000000 == 0)
            fprintf(stderr, "...processed %lld\n", total);
    }
    fprintf(stderr, "graphs=%lld firstC4=%lld firstC8=%lld firstC16=%lld firstC32=%lld NONE=%lld\n",
            total, byfirst[0], byfirst[1], byfirst[2], byfirst[3], byfirst[4]);
    return counter ? 2 : 0;
}
