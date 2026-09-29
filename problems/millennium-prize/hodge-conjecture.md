# Hodge Conjecture

**Status:** Open
**Field:** Algebraic Geometry
**Formulated:** 1950 (Jean-Pierre Serre, in honour of Hodge)
**Prize:** $1,000,000 (Clay Millennium), one of the seven official
Millennium Prize Problems
**Note:** The conjecture as usually stated is the **rational** Hodge
conjecture. Its integral and complex variants are a different matter —
see the note on that below, which matters for reading any claim of
progress.

## Statement

On a non-singular projective algebraic variety X over ℂ, every Hodge class
(a rational class of type (p,p) in H^{2p}(X, ℚ)) is a rational linear
combination of classes of algebraic cycles.

## Progress

- 1950 — Serre formulates the conjecture, naming Hodge
- 1950s — Weil conjectures, and the birth of the Weil conjectures programme
- 1951 — Lefschetz (1,1) theorem (with later refinements, incl. Kōhlhauer):
  Hodge classes of type (1,1) come from divisors
- 1973 — Griffiths describes the Hodge filtration, and the Hodge theory
  that supports the conjecture's structure
- 2016 — Voisin proves the integral Hodge conjecture for codimension-2
  (1-)cycles on Abelian fourfolds — the first new complete case in decades
- Open in general; the rational version is open, and the unrestricted
  integral version is false (Kollár), so it is not a live conjecture

## Notes

### The gap between Hodge theory and algebraic geometry

The statement is a mismatch between two theories of the same object. On
one side, Hodge theory assigns to X a rich complex cohomology group
H*(X, ℂ) with a decomposition into pieces of type (p,q). On the other,
algebraic geometry assigns to X subvarieties, and therefore cycle classes
in H^{2p}(X, ℤ). The conjecture says the intersection of the two
structures is exactly what the second one produces.

The reason this is hard is that Hodge theory is insensitive to the
algebraic data. Hodge theory classifies X by its cohomology ring and
intersection numbers. There are pairs of non-isomorphic varieties with
identical Hodge structure but different algebraic geometry — deformations
of K3 surfaces are the standard example. So no argument internal to Hodge
theory can distinguish the algebraic classes, because it cannot see them.
An argument from algebraic geometry must be found instead.

### What the (1,1) case taught us

Lefschetz's (1,1) theorem is the case where the statement is a theorem,
and it is instructive because it uses an extra ingredient Hodge theory
does not have: a holomorphic Lefschetz (1,1) theorem showing that a
rational (1,1) class lifts to a complex one, then to a holomorphic line
bundle, then by the exponential sequence to a divisor. The chain works
because divisor-valued line bundles have a well-understood Picard group.

Codimension ≥ 2 has no analogous elementary chain. The Voisin result for
codimension 2 on Abelian fourfolds succeeded by finding a substitute
construction, not by generalizing Lefschetz — and it required several
additional hypotheses, so the general codimension-2 case remains open.
That pattern is the honest summary of the field: each advance has been a
new construction for a special case, not a general method.

### The rational/integral distinction is essential

The conjecture as stated is over ℚ. A stronger, integral version requires
the class to be an integral combination of algebraic cycles, with no
denominators.

The integral version is **known to be false in general**, not merely
suspected: Kollár constructed counterexamples in codimension 2 on smooth
projective threefolds, so the failure occurs inside the smooth projective
setting the conjecture is stated in. Earlier counterexamples
(Atiyah–Hirzebruch, Zucker) concerned non-projective or non-smooth
varieties and therefore sit outside the standard statement. This is a rare
and instructive situation: the stronger statement is known to be wrong, so
the conjecture as formulated has to be the rational one, and any
"strengthening" of the Hodge conjecture by dropping the ℚ is a mistake
rather than an improvement.

### Why no natural candidate for a proof exists

The obstacle is not a specific estimate that could be sharpened. A
principled approach would need either:

- a generalisation of the Lefschetz (1,1) chain to higher codimension, for
  which no analogue of the Picard group of divisors is known, or
- a way to inject algebraic geometry into the Hodge-theoretic
  classification, which the K3 deformation examples show is impossible
  on Hodge data alone.

Both roads run into established obstructions. This is a case where the
reason the problem is open is well understood at the level of method, not
merely in terms of missing technical estimates.

### Honest assessment

The conjecture is open, the (1,1) case is a theorem, codimension 2 is
known in restricted settings (Voisin 2016), and the integral version is
known to be false. Treat any general proof here as a bug. The
defensible content is: the Hodge-theoretic/algebraic mismatch stated
clearly, the Lefschetz chain described as the one case that works, the
rational/integral distinction and its counterexamples, and the honest
statement that no general method is on the table.
