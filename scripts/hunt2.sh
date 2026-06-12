#!/bin/bash
# Two-phase hunt at one size: collect C4+C8-free cubic graphs via phase-1
# annealing, deduplicate, then evaluate the full objective (#C16 + #C32)
# on each.  Any graph evaluating to 0 is a counterexample.
set -u
N=$1
SEED=${2:-1}
ITERS=${3:-30000000}
mkdir -p results/hunt
./src/anneal "$N" "$SEED" "$ITERS" --phase1 \
    > "results/hunt/p1_n$N.out" 2> "results/hunt/p1_n$N.log"
cut -d' ' -f2 "results/hunt/p1_n$N.out" > "/tmp/p1_n$N.raw"
nauty-shortg -q "/tmp/p1_n$N.raw" "results/hunt/seeds_n$N.g6" 2>/dev/null
./src/anneal "$N" 1 1 --seeds "results/hunt/seeds_n$N.g6" --eval 2>/dev/null \
    | sort -n > "results/hunt/seeds_n${N}_eval.txt"
echo "n=$N: $(wc -l < "results/hunt/seeds_n$N.g6") distinct C4+C8-free graphs;"
echo "  best full objective (#C16+#C32): $(head -1 "results/hunt/seeds_n${N}_eval.txt" | cut -d' ' -f1)"
grep -l '^0 ' "results/hunt/seeds_n${N}_eval.txt" && echo "!!! COUNTEREXAMPLE CANDIDATE !!!"
