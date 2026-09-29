"""Riemann Hypothesis zero verifier.

IMPORTANT -- why this does a two-dimensional root solve:
    mpmath.zetazero(i) finds a zero by bracketing and refining ALONG the
    line Re(s) = 1/2. Its returned real part is therefore exactly 0.5 by
    construction, so any "distance from the critical line" computed from
    it is identically zero regardless of the mathematics. That is a
    tautology, not evidence, and the check could never fail.

    So this tool instead solves zeta(s) = 0 in the full complex plane by
    Newton's method in two real variables, starting from a point offset
    off the critical line. The real part of the resulting root is then a
    genuinely computed quantity: if a root were off the line, the solver
    would have to move sideways to find it and the reported deviation
    would be non-zero.

What this establishes: the first n non-trivial zeros, as located by a
genuine 2-D solve, have real part 0.5 to within the reported tolerance.
It says nothing about zeros beyond index n, and it is emphatically not a
proof of the Riemann Hypothesis.

It is also a much weaker check than the rigorous verifications of the
first 10^13 zeros, which bound zeta on intervals with error estimates
rather than running a root finder. See the Notes section of
problems/millennium-prize/riemann-hypothesis.md.

Usage:
    python rh_zeros.py            # first 20 zeros
    python rh_zeros.py 200        # first 200 zeros
"""

import sys

import mpmath

mpmath.mp.dps = 25


def zeta_2d_newton(s0, tol, max_iter=60):
    """Solve zeta(s) = 0 in C by Newton iteration in two real variables.

    s0 is an mpmath complex starting point. Returns the converged root, or
    None if the iteration fails to converge.
    """
    s = mpmath.mpc(s0)
    for _ in range(max_iter):
        f = mpmath.zeta(s)
        if abs(f) < tol:
            return s
        df = mpmath.diff(lambda z: mpmath.zeta(z), s)
        if df == 0:
            return None
        s = s - f / df
    if abs(mpmath.zeta(s)) < tol:
        return s
    return None


def locate_zeros(n_zeros, dps=25):
    """Return (rows, tol). Each row is (i, root, deviation); root is None
    on solver failure."""
    mpmath.mp.dps = dps
    tol = mpmath.mpf(10) ** (-(dps - 5))
    half = mpmath.mpf("0.5")
    rows = []
    for i in range(1, n_zeros + 1):
        t = mpmath.im(mpmath.zetazero(i))
        # Alternate the sign of the offset so that a solver failure is not
        # masked by one unlucky starting point.
        offset = mpmath.mpf("0.01") * (1 if i % 2 else -1)
        root = zeta_2d_newton(mpmath.mpc(half + offset, t), tol=tol)
        if root is None:
            rows.append((i, None, None))
        else:
            rows.append((i, root, abs(mpmath.re(root) - half)))
    return rows, tol


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print(f"Checking the first {n} non-trivial zeros of zeta(s)")
    print("Solver: 2-D Newton on zeta(s)=0, started OFF the critical line.\n")

    rows, tol = locate_zeros(n)

    failed = [i for i, root, _ in rows if root is None]
    if failed:
        print("Solver did not converge for zero indices: "
              + ", ".join(str(i) for i in failed))
        print("This is a SOLVER failure, not a mathematical FAIL. A missing")
        print("zero must not be read as a zero off the critical line.")
        return 1

    print(f"{'#':>4}  {'Re(s)':>24}  {'Im(s)':>24}  {'|Re(s)-1/2|':>16}")
    print("-" * 74)
    worst = mpmath.mpf(-1)
    worst_idx = 1
    for i, root, dev in rows:
        if dev > worst:
            worst, worst_idx = dev, i
        if i <= 20:
            print(f"{i:>4}  {mpmath.nstr(mpmath.re(root), 22):>24}  "
                  f"{mpmath.nstr(mpmath.im(root), 20):>24}  "
                  f"{mpmath.nstr(dev, 8):>16}")
    if n > 20:
        print(f"     ... {n - 20} more checked")

    print("-" * 74)
    print(f"worst deviation: {mpmath.nstr(worst, 8)}  (zero #{worst_idx})")
    print(f"tolerance at dps={mpmath.mp.dps}: {mpmath.nstr(tol, 3)}")
    if worst == 0:
        print("NOTE: deviation is exactly 0 at this precision. The real parts")
        print("      converged onto 0.5 to within working precision, so the")
        print("      residual rounds to zero. Raise dps to expose it. Read")
        print("      this as the limit of the arithmetic, not as extra")
        print("      confirmation of the hypothesis.")
    elif worst < tol:
        print(f"PASS: all {n} roots lie on Re(s)=1/2 within tolerance.")
    else:
        print("FAIL: at least one root deviates from Re(s)=1/2 beyond tolerance.")
        print("      Re-run at higher dps before drawing any conclusion.")
        return 1

    print(f"\nScope: the first {n} non-trivial zeros only. Zeros beyond index")
    print(f"{n} are unconstrained by this run. Finite verification, not a proof")
    print("of the Riemann Hypothesis.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
