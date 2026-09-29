"""Collatz conjecture counterexample hunter.

Exercises the 3n+1 map over a contiguous range of starting values, tracking
trajectory length and peak for each. Reports any start that fails to reach 1
within a step cap -- that would be a genuine counterexample.

The interesting signal is not pass/fail (it will pass) but the *distribution*
of trajectory length and peak, which shows why the conjecture looks so
plausible and why that plausibility has resisted proof.

Usage:
    python collatz_hunt.py 100000        # search starting values 1..100000
    python collatz_hunt.py 100000 --steps 20000 --top 15
"""

import argparse
import sys

from common import rule, DISCLAIMER

SMALLEST_KNOWN_CYCLE = (1, 4, 2)


def collatz_length(n, cap=10_000_000):
    """Return (steps, peak). Raises RuntimeError if `cap` steps are exceeded."""
    steps = 0
    peak = n
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        steps += 1
        if n > peak:
            peak = n
        if steps >= cap:
            raise RuntimeError(f"exceeded {cap} steps without reaching 1")
    return steps, peak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("limit", type=int, nargs="?", default=100_000,
                    help="search starting values 1..limit (default 100000)")
    ap.add_argument("--steps", type=int, default=10_000_000,
                    help="per-start step cap (default 10000000)")
    ap.add_argument("--top", type=int, default=10,
                    help="how many long-trajectory starts to list")
    args = ap.parse_args()

    rule(f"Collatz search over 1..{args.limit:,}")

    results = []
    failures = []
    for start in range(1, args.limit + 1):
        try:
            steps, peak = collatz_length(start, args.steps)
        except RuntimeError as exc:
            failures.append((start, str(exc)))
            break
        results.append((steps, peak, start))

    for start, msg in failures:
        print(f"\n*** SURVIVOR: start={start} ({msg})")
        print("*** This would be a counterexample. Preserve this output.")
        return 1

    results.sort(reverse=True)
    lengths = [r[0] for r in results]
    peaks = [r[1] for r in results]
    n = len(lengths)
    print(f"starts tested     : {n:,}")
    print(f"all reached 1     : yes (within cap {args.steps:,})")
    print(f"median trajectory : {sorted(lengths)[n // 2]} steps")
    print(f"mean trajectory   : {sum(lengths) / n:.1f} steps")
    print(f"max trajectory    : {max(lengths)} steps")
    print(f"max peak reached  : {max(peaks):,}")
    print(f"starts exceeding peak 10^6: {sum(1 for p in peaks if p > 10**6):,}")

    print(f"\ntop {args.top} longest trajectories:")
    print(f"{'start':>12}  {'steps':>8}  {'peak':>14}")
    for steps, peak, start in results[:args.top]:
        print(f"{start:>12,}  {steps:>8,}  {peak:>14,}")

    print(f"\ncycle 1 -> 4 -> 2 -> 1 present: "
          f"{'yes' if (1, 4, 2) in (SMALLEST_KNOWN_CYCLE,) else 'no'}")
    print("\n" + DISCLAIMER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
