#!/bin/bash
# Launch simulated-annealing counterexample hunts at the open frontier.
# n=30 is the first size beyond the literature's exhaustive verification
# (n <= 29, Markström); since 30 < 32 a counterexample there needs only
# to avoid C4, C8, C16.  Larger sizes must also avoid C32.
set -u
ITERS=${1:-50000000}
mkdir -p results/hunt
for spec in "30 1" "30 2" "30 3" "46 1" "62 1"; do
  set -- $spec
  n=$1; seed=$2
  ./src/anneal "$n" "$seed" "$ITERS" \
      > "results/hunt/n${n}_s${seed}.out" \
      2> "results/hunt/n${n}_s${seed}.log" &
done
wait
echo "hunt finished"
grep -l COUNTEREXAMPLE results/hunt/*.out 2>/dev/null || echo "no counterexample found"
for f in results/hunt/*.log; do echo "== $f"; tail -1 "$f"; done
