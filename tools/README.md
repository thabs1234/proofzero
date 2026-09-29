# Tools

Runnable search and verification utilities for the problems in this repo.

These are **not** proof assistants and nothing here resolves a conjecture.
Each tool searches a finite range and reports what it found. A clean run is
evidence *against* a counterexample up to the bound searched — never a proof
of the general statement. Keep that distinction in anything you write up from
these results.

## Setup

```
python -m pip install mpmath
```

Only `rh_zeros.py` needs a third-party package; the rest are pure Python.
Verified on Python 3.14.

## Running

```
cd tools
python rh_zeros.py 200              # check 200 zeros of zeta(s)
python collatz_hunt.py 100000       # Collatz over 1..100000
python goldbach_twins.py 200000 --sample
python pnp_probe.py 20 4.26        # one 3-SAT instance + brute force
python pnp_probe.py --sweep 40 30 --random
python pnp_probe.py --self-check         # mutation-tested cross-validation
python _control_rh.py                 # negative control for rh_zeros
```

## The tools

### `rh_zeros.py` — Riemann hypothesis zero verifier

Solves `zeta(s) = 0` by Newton's method in two real variables, starting
from a point deliberately offset off the critical line, and measures
`|Re(s) - 1/2|` for each root.

The offset matters, and it is the whole point of the tool. The obvious
implementation — take `mpmath.zetazero(i)`, subtract `0.5` — is
**vacuous**: `zetazero` brackets and refines *along* the line
`Re(s) = 1/2`, so its real part is `0.5` by construction and the reported
deviation is identically zero no matter what the mathematics says. The
check cannot fail, so it is not evidence. Solving in two variables forces
the solver to move sideways if a root is genuinely off the line, which
makes the reported real part a computed quantity rather than an input.

`_control_rh.py` is the negative control that proves this. It swaps in a
synthetic function whose only roots sit at `Re(s) = 0.8` and asserts that
`locate_zeros` reports a large deviation. If the verifier ever silently
degrades back into a tautology, the control fails.

Scope: finite verification of the first *n* zeros, reported as a residual
against a precision-dependent tolerance. It is far weaker than the
rigorous interval-arithmetic verifications of the first 10^13 zeros, and
it is not a proof of the Riemann Hypothesis.

### `collatz_hunt.py` — counterexample hunter

Runs the 3n+1 map from every start in `1..limit`, tracking trajectory length
and peak, with a step cap. A start that fails to reach 1 within the cap
exits non-zero and is reported as a survivor — that would be a real
counterexample and its output should be preserved. The interesting output is
the distribution: median ~99 steps, but peaks routinely exceed 10^6, and the
growth from typical to extreme is what makes the conjecture hard rather than
obvious.

### `goldbach_twins.py` — two number-theory searches

One sieve pass serves both. Goldbach: every even number in range is counted
as a sum of two primes, and thin cases are listed. Twin primes: all pairs
`(p, p+2)` in range. Both are exhaustive, so a failure would be a genuine
counterexample. For calibration, the published Goldbach frontier is 4×10^18
(Oliveira e Silva, Herzog, Pardi 2014) — 13 orders of magnitude beyond any
local search, which is the point.

### `pnp_probe.py` — P vs NP hardness probe

Generates random 3-SAT at controlled density, then times DPLL search,
brute-force 2ⁿ search, and verification of a found assignment. The output
that matters is the ratio between search and certificate check — typically
5–35× on small instances, and the gap widens with n. That asymmetry is the
shape of the P vs NP question, demonstrated concretely. It is not progress
toward resolving it.

Re-run this self-check after any edit to the solver, since a SAT solver that
silently returns wrong answers is worse than none:

```python
import random, pnp_probe as P
rng = random.Random(11); bad = 0
for _ in range(600):
    n = rng.randint(4, 13); m = rng.randint(1, int(n * 6))
    c = P.gen_3sat(n, m, seed=rng.randint(0, 10**6))
    a, b = P.solve_dpll(n, c), P.solve_bruteforce(n, c)
    if (a is None) != (b is None) or (a is not None and not P.check(c, a)):
        bad += 1
print("mismatches:", bad)   # must be 0
```

#### Built-in self-check

```
python pnp_probe.py --self-check    # exits 0 on clean run, 1 on any fault
```

This is the comparison above packaged as a command. It cross-validates
`solve_dpll` against `solve_bruteforce` on 400 random 3-SAT instances
(n in [4,14]) and independently re-verifies every returned certificate with
`check()`.

Two properties make it meaningful rather than decorative:

1. **The two solvers are genuinely independent algorithms.** DPLL
   unit-propagates and branches; brute force enumerates all `2**n`
   assignments. A bug in either shows up as disagreement. Comparing a solver
   against itself — or against two calls to the same deterministic function —
   can never fail, and would print a confident "PASS" no matter how broken
   the tool was.

2. **It is mutation-tested.** A check that cannot fail is worthless, so three
   real bugs were injected into `_dpll` and confirmed caught:

   | injected bug | result |
   |---|---|
   | report UNSAT without validating the certificate | caught — 323 disagreements |
   | return the assignment without validating it | caught — 77 disagreements, 131 invalid certificates |
   | invert literal polarity in unit propagation | caught — 197 disagreements |

   All three failed loudly and exited 1. The clean tree passes with 0
   disagreements (323 SAT, 77 UNSAT — both branches exercised).

It exploits the asymmetry that matters: a wrongly-pruning solver reporting
**UNSAT** is the dangerous failure mode, and brute force bounds it
independently.


## Honesty rules for this directory

- Never present a clean run as confirmation of a conjecture.
- Always print the bound searched alongside the result.
- When reporting a survivor or counterexample, say so loudly and preserve
  the output — that would be the only genuinely new result in this repo.
- If a tool is modified, re-run its cross-check before trusting output.
