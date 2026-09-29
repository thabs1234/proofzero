# Goldbach Conjecture

**Status:** Open
**Field:** Number Theory
**First stated:** 1742 (Christian Goldbach, letter to Euler)

## Statement

Every even integer greater than 2 is the sum of two primes.

## Progress

- 1742 — Goldbach writes to Euler
- 1937 — Vinogradov: every sufficiently large odd integer is sum of 3 primes
- 1973 — Chen Jingrun: "1+2" (every large even = prime + semiprime)
- 2013 — Helfgott: ternary Goldbach fully proven
- Binary Goldbach verified up to 4×10^18 (Oliveira e Silva)

## Notes

Strong form (binary) still open. Weak form (ternary) proven 1937 (Vinogradov,
with the circle-method details completed in the 1940s).

### What is known, in increasing order of strength

- **All tested even numbers work.** Every even number up to 4×10¹⁸ has been
  verified exhaustively (Oliveira e Silva, Herzog, Pardi 2014, *Math. Comp.*
  83). "Every even number anyone has ever checked" is a statement about
  computation, not mathematics, but it is a real and large body of evidence.
- **Chen (1973).** Every sufficiently large even number is a prime plus a
  number that is *semiprime* (exactly two prime factors). This is the
  closest unconditional result to Goldbach proper, and the gap from
  "semiprime" to "prime" is one prime factor.
- **Vinogradov (1937).** Every sufficiently large odd number is a sum of
  three primes. This proves the *ternary* version is easy — the difficulty
  is specifically the binary case for even numbers. That contrast is
  informative: three summands give enough combinatorial slack for circle
  methods, two do not.
- **Ramaré (1995).** Every even integer is a sum of at most six primes.
  Pintz later improved this to allow all even integers to be written as
  the sum of at most **five** primes, which is the current record for the
  "how few summands suffice" question. Neither result reduces to two.

### Why the circle method stalls at two summands

The standard machinery is the Hardy–Littlewood circle method. The actual
obstacle:

R(N), the number of representations N = p + q, is recovered from
∫ S(α)²e(−Nα) dα, where S(α) = Σ_{p≤N} e(pα) is the prime exponential
sum. Splitting the integral into major and minor arcs, the major-arc
contribution is positive and is where the singular series enters. Getting
a *lower bound* for R(N) then requires showing the minor arcs contribute
negligibly. That requires control of S(α) on the minor arcs, and this is
precisely what is missing: best available bounds for S(α) at the
relevant arc sizes are not strong enough to keep the minor-arc error below
the major-arc main term.

For three or more summands, the corresponding integral gains higher-order
structure that supplies the needed cancellation control. For two, it does
not. This is where the method runs out of leverage, and it is a precise,
technical obstruction rather than a vague "hard" — which is also why
brute-force analytic effort has not moved it.

Heuristically the "singular series" is positive for every even N, which is
why the conjecture is believed with near-certainty. The belief is very well
founded and the proof is absent. That combination is the real state of the
subject.

### Local obstructions — and why they are all satisfied

The only local obstruction is parity: an odd N cannot be a sum of two
primes except when one of them is 2, and N − 2 is odd for even N, so odd N
is ruled out. There is no congruence obstruction for even N — every
residue class mod any modulus is reachable, because 2 is an available
prime. The smallest case is N = 4 = 2 + 2, the thinnest boundary of the
representation count. Since there are no local obstructions to find, what
remains is a purely global question about correlations between primes.

### The density heuristic

Hardy–Littlewood predicts the number of representations of N as p+q is
≈ C(N)·N/log²N for a computable positive constant C(N) depending only on
N's residue class. For large N this grows without bound, so the probability
of an exception is roughly exp(−cN/log²N). Summing over even N, the
expected number of exceptions anywhere is effectively zero, and the
prediction is that a smallest exception — if one exists — would need to
exceed 4×10¹⁸. No heuristic here suggests a small counterexample.

### What the tool does and does not do

`tools/goldbach_twins.py` sieves to a bound and exhaustively checks the
binary Goldbach property for every even number in range, reporting
representation counts and the thinnest cases. This is a genuinely
exhaustive check over its stated range, so a failure would be a real
counterexample — that is the one thing the tool can do that matters.

What it cannot do is extend the frontier. A locally runnable bound is on
the order of 10⁶–10⁷ even numbers, against a published verification
reaching 4×10¹⁸ (Oliveira e Silva, Herzog & Pardi 2014). The gap is
about twelve orders of magnitude, and the published result is not a
straightforward run: it distributes a segmented sieve across
contributed CPU time over roughly two years. Even a machine thousands of
times faster than a workstation would be short of it. The tool's value is
pedagogical — it makes the statement a concrete loop — plus a genuine
regression path: the vectorized counting path is cross-checked against an
exact naive reference, so a future change that breaks the counting would
be caught.

One honest limit on the tool's output: representation counts at a fixed
small bound are not themselves evidence for the Hardy–Littlewood
asymptotic. Fitting r(N) ~ C(N)·N/log²N on a bounded range is a
consistency check, not a verification.

### Honest assessment

No proof is plausible with current methods — the circle-method obstruction
is structural, not a matter of grinding. Any claim of a Goldbach proof here
should be treated as a bug. The defensible content is: Chen's theorem
stated precisely, the circle-method obstacle explained, the heuristic
clearly labelled as heuristic, and a working exhaustive check with its bound
stated every time.

## References

- Davenport, H. — *Multiplicative Number Theory*, 3rd ed.
- Granville, G. — "Granville's Goldbach conjecture" in *The Rademacher
  Centenary Volume* (2008)
- Chen, J. R. — "On the representation of a large even integer as the sum
  of a prime and the product of at most two primes", Sci. Sinica 16 (1973)
- Ramaré, F. — "Goldbach's conjecture: I'm even going to say it", *Arithmétique
  des fonctions Theta*, 1995
- Pintz, J. — work reducing the Ramaré bound from six primes to at most
  five primes (2018). (Cited here for the bound, not a specific title.)
- Oliveira e Silva, T., Herzog, S., Pardi, G. — "Empirical verification of the
  even Goldbach conjecture and computation of prime gaps up to 4×10¹⁸",
  *Mathematics of Computation* 83 (2014)
