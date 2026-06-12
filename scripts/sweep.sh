#!/bin/bash
# Exhaustive Erdős–Gyárfás verification for C4-free connected cubic graphs
# on $1 vertices: $2 work-queue parts, $3 parallel workers.
# Any graph containing a 4-cycle satisfies the conjecture trivially, so
# restricting generation to C4-free graphs (geng -f) loses no generality.
set -u
N=$1
PARTS=${2:-16}
JOBS=${3:-4}
OUT=results/n$N
mkdir -p "$OUT"
seq 0 $((PARTS-1)) | xargs -P "$JOBS" -I{} sh -c \
  'nauty-geng -c -f -d3 -D3 -q '"$N"' {}/'"$PARTS"' 2>/dev/null \
     | ./src/checker > '"$OUT"'/part{}.special 2> '"$OUT"'/part{}.stats'
echo "=== n=$N complete ==="
awk '{for(i=1;i<=NF;i++){split($i,kv,"=");s[kv[1]]+=kv[2]}}
     END{for(k in s) printf "%s=%d ", k, s[k]; print ""}' "$OUT"/part*.stats
echo "--- special graphs (C16-only and any counterexamples) ---"
cat "$OUT"/part*.special
