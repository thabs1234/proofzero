# Twin Prime Conjecture

**Status:** Open
**Field:** Number Theory
**First stated:** 1849 (Alphonse de Polignac)

## Statement

There are infinitely many primes p such that p+2 is also prime.

## Progress

- 1849 — de Polignac states the more general claim that every even
  difference occurs infinitely often between consecutive primes
- 1919 — Brun: the sum of reciprocals of twin primes converges
  (Brun's constant, ≈1.9021605831)
- 2013 — Zhang: bounded gaps, unconditionally ≤ 70,000,000
- 2013/14 — Maynard (independently of Tao): a fixed admissible tuple yields
  bounded gaps
- 2014 — Polymath8b: the unconditional bound is reduced to 246
- Open — gap = 2 infinitely often

The 1849 date refers to de Polignac's general statement, not to the
specific twin-prime case; the twin prime conjecture is older as a natural
question and de Polignac's contribution is that he stated it as a
conjecture with a proof-of-infinity claim attached.

## Notes

Still no proof of gap = 2. Zhang's breakthrough was the first finite bound.

### An important distinction in the results above

Three separate claims are often run together. They are not the same:

1. **Bounded gaps exist (proved).** There is a constant H such that
   infinitely many consecutive primes differ by less than H. Established
   by Zhang (2013) with H = 70,000,000, reduced to H = 246 by the
   Polymath8b collaboration (2014).
2. **A specific H is achieved infinitely often (proved).** There are
   infinitely many prime pairs differing by *at most* 246. The Maynard–Tao
   sieve methods prove this.
3. **A gap of exactly 2 occurs infinitely often (open).** This is the twin
   prime conjecture.

The gap between (2) and (3) is the entire remaining problem. Bounded gaps
say the small gaps recur; they do not say which small gap. Getting from
"some gap ≤ 246 infinitely often" to "gap = 2 infinitely often" requires
detecting a specific configuration, which the sieves cannot currently do.

### Why sieves run into a wall at 2

The Bombieri–Vinogradov theorem gives average control of primes in
arithmetic progressions with modulus up to about √x, with a usable
error term — this is what powers both Goldbach and the bounded-gap
results. Zhang's key move was to find a single well-chosen finite set of
shifts (multiples of a product of small primes) for which a Bombieri–
Vinogradov-type average over residues is still enough to guarantee
admissibility, and a pigeonhole argument then forces one shift to recur.

The limit is structural. The sieve needs a hypothesis covering moduli up
to roughly √x, and that is not an artifact of the proof — it is the scale
at which the underlying distribution of primes is genuinely beyond
current analytic reach. Proving a *specific* pair, such as the shift 2,
requires information about residues that excludes 0 mod every small prime
in a coordinated way; admissibility of the whole shift set is a much
weaker condition. Averaging can force *some* member of a large admissible
set to work, and has nothing to say about any individual member. This is
why bounded gaps are the ceiling of the present method, and it is a real
barrier rather than bookkeeping slack.

The hoped-for escape is the generalized Elliott–Halberstam conjecture,
which is stronger than the Bombieri–Vinogradov-type information currently
available. Under GEH, Polymath8b proved the gap bound 6 would follow.
Still no route to 2.

### A frequent error in the literature

The two conditional figures are different hypotheses, and conflating them
is the standard error:

- Under the **Elliott–Halberstam** conjecture, Zhang's own argument yields
  gaps of at most **12**.
- Under the stronger **generalized Elliott–Halberstam** conjecture, the
  Polymath8b refinement yields gaps of at most **6**.

Both are conditional, and both stop at an even gap larger than 2. So
"Zhang proved 12 under EH" is right, and reading that as "12 under GEH",
or as an unconditional result, is the error.

### Brun's constant, and what convergence means

Brun (1919) proved the sum of reciprocals of primes p with p+2 also prime
converges, i.e. Σ_{p, p+2 prime} 1/p < ∞ (Brun's constant, ≈1.902). This
is often misread as evidence *against* infinitely many twin primes. It is
not: the reciprocals of all primes diverge, but the reciprocals of any
sufficiently sparse subset converge. Infinitely many twin primes is entirely
consistent with convergent reciprocal sum — the twin primes are just very
sparse. Convergence here is a fact about their thinness, not their
finiteness.

### The Hardy–Littlewood prediction

If twin primes are infinite, their count up to x is predicted to be
≈ 2C₂·x/(log x)², where C₂ ≈ 0.6601618158 is the twin prime constant.
The constant absorbs the local residue density — both primes are drawn
from the odd classes mod 6, which is where the factor 2 comes from. This
is a well-specified asymptotic conjecture, still unproved.
`goldbach_twins.py` counts twin pairs up to a bound, so its output is a
finite sample of exactly this quantity, and comparing that count against
2C₂x/log²x at a small bound is a consistency check only: at small x the
asymptotic is not expected to be accurate, and agreement would not
distinguish the true density from a plausible wrong one.

### Honest assessment

The bounded-gaps theorems are genuine and major, and they are the closest
thing to a partial resolution. The remaining step to gap = 2 has resisted
every strengthening of sieve methods, and the barrier is understood well
enough to state precisely. Treat any "proof" of the twin prime conjecture
appearing here as a bug.


## References

- Polignac, A. de — "Essai sur les nombres premiers et les autres puissances",
  1849
- Brun, S. — "Siebensätze und die Anwendung auf die Goldbachsche Vermutung",
  1919
- Zhang, Y. — "Bounded gaps between primes", *Annals of Mathematics* 179(3),
  2014
- Maynard, J. — "Small gaps between primes", *Annals of Mathematics* 181(1),
  2015
- Maynard, J. — "Dense clusters of primes in subsets", *Annals of Mathematics*
  183(1), 2016
- Tao, T. — "Constellations in the primes", 2013/14
- Polymath, D. H. J. — "Variants of the Selberg sieve, and bounded intervals
  containing many primes", *Research in the Mathematical Sciences* 1, 2014
- Hardy, G., Littlewood, J. — "Some problems of 'Partitio numerorum'; III: On
  the expression of a number as a sum of primes", *Acta Mathematica* 44
  (1923)
