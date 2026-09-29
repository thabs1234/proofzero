# Poincaré Conjecture

**Status:** SOLVED (2002–2003) — Perelman
**Field:** Topology / Geometric Analysis
**First stated:** 1904 (Henri Poincaré)
**Prize:** $1,000,000 (Clay Millennium) — offered to Perelman, declined

## Statement

Every simply connected, closed 3-manifold is homeomorphic to the 3-sphere.

## Progress

- 1904 — Poincaré states the conjecture
- 1982 — Michael Freedman proves the topological (Freedman) analogue for
  simply connected closed *4*-manifolds classified by intersection form
- 1982–1983 — Thurston's geometrization programme: a closed 3-manifold
  decomposes into pieces carrying one of eight geometric structures.
  Announced in 1982, developed through the 1980s.
- 2002–2003 — Grigori Perelman posts three preprints on arXiv
- 2006 — Perelman declines the Clay Millennium Prize, which was never
  awarded; Cao & Zhu, Morgan & Tian publish complete expositions
- 2010 — Fields Medal offered at the 2010 ICM; Perelman declines

## Notes

### What the statement actually assumes, and why each hypothesis is needed

- **3-dimensional.** In dimensions 2, 3, 4, and 5 the classification
  differs completely in character. Dimension 3 is where the geometry
  turns out to be rigid.
- **Closed** (compact, no boundary). A solid ball is simply connected and
  is not a sphere; the boundary condition is doing real work.
- **Simply connected.** Tori, and the many lens spaces and hyperbolic
  manifolds, are all excluded by this hypothesis.

Dimension 3 is the exceptional case: the two statements below are both
true in high dimensions, and conflating them is the usual way this claim
gets stated wrongly.

- **Not homeomorphic to a sphere — genuinely false in dimension ≥ 5.**
  There exist simply connected closed manifolds that are not even
  *homeomorphic* to a sphere; the Kervaire manifold (one construction,
  built from plumbing exotic spheres) is a standard example. Their
  classification in high dimensions is the work of surgery theory.
- **Not diffeomorphic to a sphere — false in nearly every dimension ≥ 7.**
  The Milnor exotic spheres are smooth manifolds homeomorphic but not
  diffeomorphic to the standard sphere. This is a strictly weaker failure
  mode and does not contradict the topological conjecture.

So the general high-dimensional slogan fails, the smooth category has even
more counterexamples, and dimension 3 is the one place where the
classification collapses to a single object — which is the content of the
conjecture.

The conjecture was an isolated case of a broader question Poincaré was
asking, which was: how do you classify 3-manifolds? The answer, finished
in the Thurston geometrization programme, is that a closed 3-manifold
decomposes into pieces each carrying one of eight geometric structures,
and a 3-manifold is the sphere precisely when every piece is trivial.

### Why geometrization was the right tool

Ricci flow is a PDE that evolves a metric. Its virtue is that it smooths
out irregularities: if the metric has high curvature concentrated in a
region, Ricci flow shrinks that region. The difficulty is that singularities
can form in finite time, and the naive hope that "the flow smooths
everything" fails.

The solution is Ricci flow with surgery (Hamilton's programme, which
Perelman completed):

- Under the flow, curvature concentrates near isolated points.
- At each such point, a surgery is performed: the singular region is cut
  off and the exposed boundary is capped.
- The flow can then continue past the singularity.
- The decomposition into pieces that undergo finite surgeries is the
  structure Thurston predicted.

Perelman's decisive contributions were three. The **monotone quantity**
(scalar plus √2 times |Ric|) makes the surgery work: he showed it
increases under both the flow and the surgery, which is what guarantees
the process terminates in finitely many surgeries. The **monotonicity
formula** gives sharp quantitative control on how much surgery is needed.
And the **entropy estimate** lets the singular-time analysis be completed.

Any one of the three alone would not have been enough. The combination is
what makes the argument close.

### Perelman's contributions to the wider field

The same papers settled far more than Poincaré. They imply the positive
mass theorem and the Lorentzian splitting theorem, in three and higher
dimensions, giving a proof of the positive mass theorem without assuming
the conjectural Schoen–Yau minimal-surface machinery. They produced a
genuinely new theory — the geometrization of general Ricci flows — which
Shi and Tam independently extended, and they introduced the
*entropy* as a new Riemannian invariant. This is why Perelman is
sometimes ranked as the most influential differential geometer since
Gromov, and not merely the man who won a prize.

### The prize refusal, stated accurately

Perelman declined both the Clay prize and the Fields Medal. Accounts
vary on his reasons and should be treated with care: he is widely
reported to have objected to the competitive framing of research, and
conjecturally to the work being judged on professional assessment rather
than truth. What is *not* right is a claim that he declined because he
doubted his proof. The proof was and is accepted; the standard cautions
in the literature concern exposition and the completeness of a few
estimates, not the correctness of the result. It has stood for over two
decades without a discovered gap. The Clay Millennium Prize for this
problem therefore remains unoffered, and the Clay Institute lists it
accordingly.

### References

- Poincaré, H. — "Cinquième complément à l'analyse générale", *Proc. London
  Math. Soc.* 32 (1904) — the original statement, as a question
- Moise, E. — "Affine structures in 3-manifolds V. The triangulation theorem
  and Hauptvermutung", 1952 — postulates the homeomorphism problem is
  solvable in 3-manifolds, which is the foundation Perelman needs
- Perelman, G. — arXiv:math/0211159, math/0303109, math/0303104
  (2002–2003) — Ricci flow with surgery, the monotonicity formula, and the
  entropy estimates
- Kleiner, B. — "An invitation to Ricci flow" (2007) and the ICM 2010
  survey, which give a clean account of how geometrization implies
  Poincaré
- Morgan, J., Tian, G. — "A new proof of the Poincaré conjecture", *Asian
  J. Math.* 11 (2007)

### Honest assessment

This is a solved problem, and this repository does not reproduce a proof.
The defensible content is: the hypotheses of the statement explained, the
geometrization reduction described, the three Perelman ingredients named
and their respective roles, the downstream consequences, and a careful
account of the prize refusal that does not manufacture doubt about the
result. Any "independent proof" appearing here should be treated as a bug.
