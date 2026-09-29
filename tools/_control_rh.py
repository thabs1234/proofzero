"""Negative control for rh_zeros.py.

Confirms the verifier can actually FAIL. We replace the function being
solved with a synthetic one whose ONLY roots sit off the critical line,
then check that locate_zeros reports a large deviation instead of passing.

Note: an earlier version of this control multiplied zeta by an off-line
factor, which left all the genuine on-line zeros in place. The solver
then correctly found those, and the control wrongly declared the verifier
vacuous. A control must isolate the property under test.
"""
import mpmath
import rh_zeros

TRUE_ROOT = mpmath.mpc(mpmath.mpf("0.8"), mpmath.mpf("14.13"))
CONJ_ROOT = mpmath.conj(TRUE_ROOT)

real_zeta = mpmath.zeta
real_zetazero = mpmath.zetazero


def fake_zeta(s):
    """Only roots: the off-line pair. Nothing on Re(s)=1/2."""
    return (s - TRUE_ROOT) * (s - CONJ_ROOT)


def fake_zetazero(i):
    """Supply an imaginary part near the planted root, as a starting guess."""
    return mpmath.mpc(mpmath.mpf("0.5"), mpmath.im(TRUE_ROOT) + 0.01 * i)


mpmath.zeta = fake_zeta
mpmath.zetazero = fake_zetazero
try:
    rows, tol = rh_zeros.locate_zeros(5, dps=25)
finally:
    mpmath.zeta = real_zeta
    mpmath.zetazero = real_zetazero

print("synthetic function with roots ONLY at "
      f"Re(s) = {mpmath.nstr(mpmath.re(TRUE_ROOT), 6)} "
      f"(nothing on Re(s)=1/2)")
found = [r for r in rows if r[1] is not None]
print(f"converged roots: {len(found)}/5")
if not found:
    print("RESULT: solver failed to converge -- control inconclusive")
    raise SystemExit(2)

worst = max(r[2] for r in found)
print(f"worst deviation seen: {mpmath.nstr(worst, 6)}")
if worst > tol:
    print("RESULT: CONTROL PASSED -- the verifier detects an off-line root.")
    raise SystemExit(0)
print("RESULT: CONTROL FAILED -- verifier reported no deviation on a")
print("        planted off-line root. The check is vacuous.")
raise SystemExit(1)
