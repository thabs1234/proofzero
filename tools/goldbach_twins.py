"""Goldbach and twin-prime counterexample hunter.

Two conjectures, one sieve pass:

  * Goldbach (strong)  -- every even integer > 2 is the sum of two primes.
  * Twin primes         -- infinitely many primes p with p+2 also prime.

The search is exhaustive over a range, so a failure would be a real
counterexample. A pass only extends the verified frontier, which for
Goldbach already reaches 4*10^18 (Oliveira e Silva, Herzog, Pardi 2014) and
for twins is unbounded but unproven.

Usage:
    python goldbach_twins.py 1000000
    python goldbach_twins.py 1000000 --sample
"""

import argparse
import sys

from common import DISCLAIMER, primes_upto, rule, sieve


def _goldbach_counts_naive(is_prime, limit):
    """Reference implementation, kept for the cross-check and for no-numpy use."""
    reps = [0] * (limit + 1)
    for n in range(4, limit + 1, 2):
        total = 0
        for p in range(2, n // 2 + 1):
            if is_prime[p] and is_prime[n - p]:
                total += 1
        reps[n] = total
    return reps


def _goldbach_counts_fast(is_prime, limit, plist):
    """Ordered pair counts via vectorized slice accumulation.

    ordered[n] = #{(p,q) prime : p+q = n}, counting (p,q) and (q,p) separately
    and counting p == q once. Unordered counts follow as
    (ordered[n] + is_prime[n//2]) // 2.
    """
    import numpy as np

    arr = np.frombuffer(is_prime, dtype=np.uint8)
    ordered = np.zeros(limit + 1, dtype=np.int64)
    for p in plist:
        # q ranges over 2 .. limit-p  ->  indices p+2 .. limit
        ordered[p + 2:limit + 1] += arr[2:limit - p + 1]
    return ordered


def goldbach_verify(is_prime, limit, cross_check=20000):
    """Return (violations, min_reps, max_reps, thin).

    Counts *unordered* representations n = p + q with p <= q, so a
    representation with p == q counts once. This matters: the naive
    "for each p up to n/2" loop is O(limit^2) and stops being usable
    around 10^5, so the count is done by prime-pair accumulation instead.
    For limits up to `cross_check` the fast count is compared against the
    naive reference; a disagreement is reported rather than hidden.
    """
    # Every prime p with 2 <= p <= limit-2 must be accumulated: a pair
    # (p, q) summing to some n <= limit is counted when iterating over p,
    # and p is not restricted to n/2. Truncating this list to limit//2
    # silently drops the pairs whose smaller prime exceeds limit//2.
    plist = [p for p in range(2, limit - 1) if is_prime[p]]

    try:
        import numpy  # noqa: F401
        import numpy as np
        have_np = True
    except ImportError:
        have_np = False

    if have_np:
        ordered = _goldbach_counts_fast(is_prime, limit, plist)
        # unordered reps: the p == q case appears once in `ordered`, all
        # other representations appear twice.
        reps = [
            (int(ordered[n]) + (1 if is_prime[n // 2] else 0)) // 2
            for n in range(limit + 1)
        ]
    else:
        reps = _goldbach_counts_naive(is_prime, limit)

    note = None
    if 0 < cross_check <= limit:
        ref = _goldbach_counts_naive(is_prime, cross_check)
        for n in range(4, cross_check + 1, 2):
            if ref[n] != reps[n]:
                raise AssertionError(
                    f"goldbach count mismatch at n={n}: "
                    f"fast={reps[n]} naive={ref[n]}"
                )
        note = (f"fast count cross-checked against the naive reference "
                f"for every even n <= {cross_check:,}")

    violations = []
    min_reps, max_reps = None, 0
    thin = []
    for n in range(4, limit + 1, 2):
        r = reps[n]
        if r == 0:
            violations.append(n)
            if len(violations) > 20:
                break
        if min_reps is None or r < min_reps:
            min_reps = r
        max_reps = max(max_reps, r)
        thin.append((n, r))
    return violations, min_reps, max_reps, thin, note


def twin_pairs(is_prime, limit):
    return [p for p in range(3, limit - 1) if is_prime[p] and is_prime[p + 2]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("limit", type=int, nargs="?", default=1_000_000)
    ap.add_argument("--sample", action="store_true",
                    help="print the 15 even numbers with fewest Goldbach reps")
    args = ap.parse_args()
    limit = args.limit

    rule(f"Goldbach + twin-prime search up to {limit:,}")
    is_prime = sieve(limit)

    print("\n-- Goldbach (strong) --")
    violations, min_reps, max_reps, thin, note = goldbach_verify(
        is_prime, limit, cross_check=min(20000, limit)
    )
    checked = len(range(4, limit + 1, 2))
    if violations:
        print(f"*** COUNTEREXAMPLE(S): {violations[:20]}")
        return 1
    print(f"even integers checked : {checked:,}  (4 .. {limit:,})")
    print(f"counterexamples      : 0")
    print(f"min representations  : {min_reps}")
    print(f"max representations  : {max_reps:,}")
    if note:
        print(f"cross-check          : {note}")
    if args.sample:
        thin_sorted = sorted(thin, key=lambda x: x[1])[:15]
        print("thinnest even numbers (fewest prime-pair reps):")
        for n, reps in thin_sorted:
            print(f"  {n:>10,}  {reps} rep(s)")

    print("\n-- Twin primes --")
    pairs = twin_pairs(is_prime, limit)
    print(f"pairs (p, p+2) up to {limit:,} : {len(pairs):,}")
    if pairs:
        print(f"first five          : {pairs[:5]}")
        print(f"last five           : {pairs[-5:]}")
        biggest = max(pairs)
        print(f"largest pair in range: ({biggest:,}, {biggest + 2:,})")

    print("\n" + DISCLAIMER)
    print("Verified frontier for Goldbach is 4e18, far beyond any local search.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
