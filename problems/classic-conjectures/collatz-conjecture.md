# Collatz Conjecture

**Status:** Open
**Field:** Dynamical Systems / Number Theory
**First stated:** 1937 (Lothar Collatz)

## Exhibit card

**Exhibit C — The 3n+1 Problem That Has Eaten a Century of Coffee Breaks**
*Field: Dynamical Systems / Number Theory. First stated: 1937.*

- **What is known.** Every n up to 2⁶⁸ has been verified to reach 1 by
  computation (Barina 2020 and successors), using verified-forcing methods
  covering a residue-class argument rather than a single trajectory. Tao
  proved (2019) that almost all n, in a density sense, reach values below
  f(n) for any f that grows faster than any logarithm.
- **What this repo checked.** `tools/collatz_hunt.py` searches trajectories
  from a given start and reports the longest and highest-peaking ones
  encountered. A 200,000-start run found a maximum trajectory of 382 steps
  and a peak of 17,202,377,752. Default search is 100,000 starts.
- **What remains open.** Every n. The record bound is 2⁶⁸ — a finite prefix
  of a countably infinite set, with no known monotonicity or induction
  principle that extends it. 2⁶⁸ is roughly 2.95×10²⁰, which is a large
  number and also nothing whatsoever next to infinity.
- **The inverse trap.** The tool is a *counterexample hunter*. A clean run is
  evidence AGAINST a counterexample up to the bound searched, and is never a
  proof. Low results say nothing about the hard cases: the interesting
  behaviour lives in numbers that are not small, and none of them have been
  found.

## Statement

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1
Eventually reach 1.

## Progress

- 1937 — Collatz proposes
- 1976 — Terras: almost all numbers reach a value smaller than themselves
- 1989 — Krasikov & Lagarias: density results
- 2019 — Terence Tao: "almost all" Collatz orbits attain almost bounded values
- Computation verified up to 2^68

## Notes

Tao's 2019 result is the strongest near-miss. Full conjecture remains open.

### The structural reason this is hard

Collatz is a map on the positive integers, and the question is about the
long-run behaviour of a single orbit. The map is not monotonic: the odd
branch, 3n+1, roughly *triples* the value, while the even branch halves
it. Whether the halving wins on average over the long run is a question
about a weighted average that we can compute statistically but not control.

Write an orbit as n → n/2 when even and n → (3n+1)/2 when odd (folding the
guaranteed even step into the odd branch). The per-step multiplier is then
1/2 or 3/2, and log of the product over a window is what matters: the orbit
drifts down when the *geometric* mean of the multipliers over the window is
below 1. If the odd branch occurs with density 1/2 (among odd numbers, 3n+1
is even with probability 1/2, which is the standard independence
assumption), the geometric mean is

√[(1/2)·(3/2)] = √(3/4) ≈ 0.866 < 1,

so the heuristic predicts contraction — each step shrinks the orbit by a
constant factor 0.866, and typical starting values fall geometrically
fast. The famous "1" comes from the *arithmetic* mean,
(1/2)(1/2) + (1/2)(3/2) = 1, which is the correct predictor for an
unweighted sum of multipliers but is not the criterion here. Orbit
growth is exponential, so the relevant quantity is a product, and for a
product the geometric mean governs the drift.

Two caveats keep this from being a proof. First, the density-1/2
assumption treats consecutive steps as independent, and they are not: the
residue structure of an orbit correlates its own future parity. Second,
the argument controls a *typical* orbit, and a drift estimate of that form
says nothing about whether a particular exceptional starting value exists.
So this is a good reason to expect descent, and no reason at all to
expect it for all n.

### The two notions of "almost all", which are easy to confuse

- **Tao (2019).** For any function f : ℕ → ℝ with f(n) → ∞ (f may grow
  arbitrarily slowly, but unboundedly), the set of n whose orbit never
  drops below f(n) has logarithmic density zero. In plain terms: for any
  unbounded threshold f, almost every starting value (in logarithmic
  density) has an orbit that eventually goes below f(n).
- **What this is not.** It does not say every n reaches 1. It leaves open
  the existence of a single n that never does, and it leaves open a set of
  exceptions of density zero — which is exactly where any counterexample
  must live. The result is best read as: the counterexample set, if
  non-empty, is extremely sparse.

Logarithmic density is the right notion here because orbits grow
exponentially, so the natural measure on starting points weights small n
exponentially more — the same weighting that the problem itself has.

### Why finite verification is nearly worthless as evidence

The verification record (2^68, Barina 2020) covers an enormous range.
But stopping time is not monotone in n: 27 takes 111 steps while 26 takes
10. There is no structure guaranteeing that a counterexample near 2^69 would
show any resemblance to one below 2^68. Unlike Goldbach, where the
representation count grows predictably and a local anomaly tends to be
visible early, a Collatz counterexample can be an isolated, locally
invisible feature. So the 2^68 figure is a measure of effort expended, not
of evidence accumulated. This is a genuinely different epistemic situation
from Goldbach's 4×10¹⁸, and conflating the two is a common error.

### What is known about how the work is distributed

Terras (1976) showed the stopping time of a natural fraction of starting
values is finite — that almost all n eventually reach a value below
themselves. Krasikov and Lagarias (1989) sharpened the density results for
several related questions, including how often an orbit reaches 1 without
first falling below roughly x^(1/3) for a starting value n ≤ x. Together
these give a quantitative, verified picture of typical behaviour — the
density of well-behaved starting points is not just positive but close to
1 — and none of it extends to a statement about all n, because density
statements leave open a null set that could still be nonempty.

### Undecidability is not the same as unprovability

Conway proved that the general halting problem for the 3x+1 map — given
arbitrary rational initial values and parameters of the form (3n+1)/k —
is algorithmically undecidable: no algorithm can decide, for every input,
whether the orbit reaches a cycle. (Conway's result on the "3x+1
problem", 1977, reported in Guy and Smith's *Unsolved Problems in Number
Theory*.) It is important and is frequently misused in two directions. It
does not show the specific conjecture "every n reaches 1" is unprovable;
undecidability applies to a more general family, and the specific
instance may still be provable. It does mean that no *general* method for
this family exists, so the undecidability result is a fair reason to
expect the specific case to be difficult without being a reason to
expect it to be impossible.

### What the tool does and does not do

`collatz_hunt.py` searches a finite contiguous range of starting values,
records stopping times and maximum excursion, and reports the record
holders found. The map is deterministic but not injective, so an orbit
that enters the known 1-cycle is a confirmation and an orbit that enters
any *other* cycle would be a genuine counterexample. The tool cannot
detect a divergent orbit at all — it is bounded by a step ceiling and will
report "did not terminate within limit" rather than proving anything. The
bounded step limit is the honest boundary of what the search can say.

### Honest assessment

The conjecture is open, the strongest result is Tao's density theorem, and
the standard heuristic does predict contraction — the geometric mean
√(3/4) ≈ 0.866 is comfortably below 1 — yet it rests on an independence
assumption that is not justified, and it says nothing about exceptional
starting values. Treat any proof here as a bug. The defensible content is
a precise account of what "almost all" means, an explanation of why the
finite verification record carries less evidential weight than it appears
to, and a working bounded search that states its own limits.

## References

- Tao, T. — "Almost all orbits of the Collatz map attain almost bounded values" (2019)
- Lagarias, J. — "The 3x+1 problem" (AML Survey)
