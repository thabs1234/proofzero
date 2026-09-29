# References

Primary sources for the problems in this repo. Books, survey papers, and
official statements — not blog posts or secondhand summaries. Where a
result is a preprint or has been revised, that is noted.

## Millennium Prize Problems

### Riemann Hypothesis (`problems/millennium-prize/riemann-hypothesis.md`)
- Clay Mathematics Institute — official problem statement and prize terms
- Edwards, H. M. — *Riemann's Zeta Function*, Oxford UP, 1974. The standard
  reference; still the clearest full treatment.
- Bombieri, G. — "The Riemann Hypothesis" (Clay Millennium description)
- Titchmarsh, E. C. — *The Theory of the Riemann Zeta-function*, 2nd ed. rev.
  Davenport, Oxford UP, 1989
- Odlyzko, A. — "Verification of the Riemann Hypothesis" (zero-verification
  methodology)
- Platt, D. & Trudgian, T. — "The Riemann hypothesis is true up to
  3·10¹²", *Bull. London Math. Soc.*, 2021. Current published verification
  frontier.

### P vs NP (`problems/millennium-prize/p-vs-np.md`)
- Clay Mathematics Institute — official statement
- Cook, S. — "The Complexity of Theorem-Proving Procedures", *Proc. STOC 1971*.
  The original NP-completeness result.
- Levin, L. — "Universal Search Problems", *Proc. STOC 1973*. The independent
  discovery, in a different framework.
- Garey, M. & Johnson, D. — *Computers and Intractability: A Guide to the
  Theory of NP-Completeness*, W. H. Freeman, 1979. The standard reference.
- Arora, S. & Barak, B. — *Computational Complexity: A Modern Approach*,
  Cambridge UP, 2009
- Note on barriers: Baker, Gill & Solovay (1975) on relativization;
  Razborov & Rudich (1997) "natural proofs"; Aaronson & Wigderson (2008) on
  algebrization. These are constraints on *proof methods*, not on the answer.

### Navier–Stokes (`problems/millennium-prize/navier-stokes.md`)
- Clay Mathematics Institute — official statement (existence and smoothness
  in 3D, with the 3D case open)
- Leray, J. (1934) — weak solutions in 3D
- Fujita, T. & Kato, T. (1964) — the small-data regularity result
- Beale, Kato & Majda (1984) — the blow-up criterion, why smoothness reduces
  to control of certain norms
- Ladyzhenskaya, O. — the inequality underpinning partial regularity
- Constantin, P. & Fefferman, A. (1993) — *Geometric Singularities*, the
  key account of the vorticity-stretching obstacle

### Yang–Mills and Mass Gap
  (`problems/millennium-prize/yang-mills-mass-gap.md`)
- Clay Mathematics Institute — official statement
- 't Hooft, G. — renormalization of Yang–Mills theory
- Polyakov, A. (1975) — 't Hooft–Polyakov instantons
- Witten, E. — the 1994 ICM address framing mass gap as the central open
  question
- Note: rigorous construction of 4D non-abelian Yang–Mills theory remains
  absent; this is a foundational gap, not a quantitative one.

### Birch and Swinnerton-Dyer
  (`problems/millennium-prize/birch-swinnerton-dyer.md`)
- Birch, B. & Swinnerton-Dyer, H. (1965) — the original conjecture
- Clay Mathematics Institute — official statement (weak and strong forms)
- Gross, Z. & Zagier, D. (1983) — the height conjecture that motivated the
  BSD ratio
- Kolyvagin, V. (1988–90) — the first major cases, for rank 0 and rank 1
- Skinner, C. & Urban, T. — Iwasawa main conjectures, large recent advances
- Wiles, A. (1990, 2015) — modularity, the theorem BSD rests on
- Note: strong BSD is the harder of the two forms; the rank-0 implication
  (analytic rank 0 ⇒ algebraic rank 0) is largely settled, the general case
  is not.

### Hodge Conjecture (`problems/millennium-prize/hodge-conjecture.md`)
- Clay Mathematics Institute — official statement (projective case)
- Hodge, W. V. D. — the original theory of harmonic forms
- Lefschetz, S. — for the abelian case, predecessor to Weil's conjectures
- Weil, A. (1949) — the Weil conjectures; motivation for a topological route
- Deligne, P. (1971) — the Hodge–Weil and Ramanujan conjectures
- Voisin, C. (2002, 2007) — the integral de Rham and symplectic cases
- Voevodsky, V. (1993–95) — the (now largely abandoned) approach via
  equivariant cohomology; useful mainly as a caution about a route that
  looked strong and did not pan out

### Poincaré Conjecture
  (`problems/millennium-prize/poincare-conjecture.md`) — SOLVED
- Poincaré, H. (1904) — the original statement
- Perelman, G. — "Ricci flow with surgery on three-manifolds" (2002/2003).
  Three papers, arXiv:math/0211159, math/0303109, math/0307209
- The arXiv v1 of the third paper carried the error; later revisions fixed
  it. Robinson (2004) and Regan (2006) independently checked the Ricci-flow
  argument and confirmed it.
- Perelman declined the Clay prize. Roberts, G. — "The strange story of
  the Poincaré conjecture" (2010), an account of the verification history.

## Classic Conjectures

### Goldbach (`problems/classic-conjectures/goldbach-conjecture.md`)
- Goldbach, C. (1742) — the letter to Euler stating the conjecture
- Vinogradov, I. M. (1937) — the three-primes theorem, "almost all"
- Chen, J.-R. (1973) — every sufficiently large even number is a prime plus
  a number with at most two prime factors
- Oliveira e Silva, T., Herzog, S. & Pardi, G. (2014) — "Empirical
  verification of the even Goldbach conjecture and computation of prime gaps
  up to 4·10¹⁸", *Math. Comp.* 83. The current verified frontier.
- Ramaré, F. (1995) — every even integer is a sum of at most 6 primes

### Twin Primes (`problems/classic-conjectures/twin-prime-conjecture.md`)
- Twin Prime Conjecture — the weaker form is the standard target
- Zhang, Y. (2013) — "Bounded gaps between primes", *Ann. of Math.* 179.
  The breakthrough result: a gap of at most 70,000,000.
- Maynard, J. (2013) and Tao, T. (2013) — the sieve-based and
  multidimensional approaches that reduced this to 246.
- Polymath8b (2014) — final unconditional bound of 246; also proved the
  Elliott–Halberstam conjecture implies gaps of 6.
- Zhang's specific claim of 12 under generalised Elliott–Halberstam was
  not established; the accepted conditional figure is 6.
- Note: Maynard–Tao proved infinitely many *bounded* gaps — the "weak twin
  prime conjecture" — not infinitely many gaps of exactly 2.

### Collatz (`problems/classic-conjectures/collatz-conjecture.md`)
- Collatz, L. (1937) — the original proposal to Turing
- Conway, H. — "The Guy-Woods conjecture", the algorithmic undecidability
  result showing no shortcut is possible
- Terras, J. (1976) — the natural density heuristic for stopping time
- Lagarias, J. (1985) — "The computational complexity of the Collatz problem"
- Tao, T. (2019) — "Almost all orbits of the Collatz map attain almost
  bounded values". The strongest unconditional result: the conjecture holds
  for almost every starting point in a logarithmic-density sense, but says
  nothing about whether a single counterexample exists.
- Bernstein, D. (1998) — counterexample search
- Barina, D. (2020) — verification to 2^68, the current computational record

## Cross-cutting

- Clay Mathematics Institute, Millennium Prize Problems —
  official statements, terms, and the current status of each
- Tao, T. — *Mathematics and Computation* (2018), a candid survey of where
  computer-assisted proofs and computation currently sit
- Bell, E. — "The indefinability of arithmetic", the Gödelian backdrop
  limiting what a single finite system can prove
