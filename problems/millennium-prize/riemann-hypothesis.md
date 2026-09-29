# Riemann Hypothesis

**Status:** Open
**Field:** Analytic Number Theory
**First stated:** 1859 (Bernhard Riemann)
**Prize:** $1,000,000 (Clay Millennium)

## Exhibit card

**Exhibit A — The Billion-Dollar Question Nobody Can Crack**
*Field: Analytic Number Theory. Prize: $1,000,000.*

- **What is known.** Every non-trivial zero of ζ(s) that has been computed
  lies on the line Re(s) = 1/2. Platt and Trudgian verified this up to height
  3×10¹². More than 41% of zeros are provably on the line unconditionally
  (Bui–Conrey–Young, 2011).
- **What this repo checked.** `tools/rh_zeros.py` locates the first N zeros by
  two-variable Newton iteration started *off* the line, and reports the
  deviation of each real part from 1/2. Default N = 20; the 200-zero run
  finished with a worst deviation of 2.58×10⁻²⁶.
- **What remains open.** That *every* zero is on the line. A verified prefix
  does not imply the general case — the property is not known to be
  inductive. Roughly 1.7×10¹³ zeros are known numerically; infinitely many
  are unaddressed.
- **This is not a contribution.** The check is the published result scaled
  down by about 10¹², and proves nothing Platt–Trudgian did not already prove.
  `tools/_control_rh.py` exists to prove the checker can *fail*: it plants a
  zero at 0.8 ± 14.13i and the tool reports the deviation 0.3.

## Statement

All non-trivial zeros of the Riemann zeta function ζ(s) have real part 1/2.

## Progress

- 1896 — Hadamard & de la Vallée Poussin proved the Prime Number Theorem (equivalent to no zeros on Re(s)=1)
- 1914 — Hardy proved infinitely many zeros on the critical line Re(s)=1/2
- 1942 — Selberg showed a positive proportion of zeros are on the critical line
- 1989 — Conrey proved > 40% of zeros are on the critical line
- 2004 — Gourdon verified the first 10^13 zeros by height lie on the line
- 2020/21 — Platt & Trudgian verified all zeros up to height 3×10¹²

## Notes

### What would count as a proof

RH is equivalent to several other statements, and knowing which one you are
attacking matters:

- **PNT equivalence.** RH ⟺ π(x) = Li(x) + O(√x·log x). The best
  unconditional error is O(x·exp(−c(log x)^{3/5}(log log x)^{−1/5}))
  (Korobov–Vinogradov), which is *far larger* than √x·log x — it saves only
  a power of x over the trivial bound. Getting from the Vinogradov–Korobov
  error down to √x·log x is precisely the unproved step, so the PNT itself
  is long since known and the hard part is the error term.
- **Möbius equivalence.** RH ⟺ M(x) = O(x^{1/2+ε}), where M(x) is the
  Mertens function. A counterexample to RH would be a large excursion in
  M(x); no such excursion is known.
- **Sign changes (and a trap).** Littlewood proved in 1914, *without*
  assuming RH, that E(x) = π(x) − Li(x) changes sign infinitely often.
  So this is not an equivalence with RH at all — it is an unconditional
  theorem. Its real content is the converse: RH is **false** if and only if
  E(x) stays of one sign eventually, i.e. if Ω± is empty. The sign
  oscillation is the known side; the unknown side is whether a
  Landau–Pollak-type massive oscillation Ω (error larger than √x·log x
  infinitely often) ever occurs. Note this cuts against intuition: a
  theorem about the error oscillating does not support RH, and quoting it
  as progress toward RH is a category error.
- **Functional-equation form.** RH ⟺ the completed zeta function
  ξ(s) = ½s(s−1)π^{-s/2}Γ(s/2)ζ(s) is positive for all real s > 1. This
  is a genuine equivalence and is the form most attempts attack. The
  related positivity conditions on the *de Bruijn/Newman* family —
  Λ(t) ≥ 0 for t ≥ 1/2, with the heat flow moving Λ toward the Riemann
  hypothesis — are the other major reformulation; Rodgers and Tao proved
  Newman's conjecture (Λ(t) ≤ 0 for t ≤ 0) in 2018, which is a real
  theorem but an asymptotic one, not a step to Λ(t) ≥ 0 for t ≥ 1/2.
  Both routes are honest places to look: they turn the problem into one
  about a real-valued function, where analytic inequalities apply rather
  than spectral theory.

### Where the state of the art actually sits

- **Zero-free regions.** We cannot reach the critical line. The best
  unconditional region is σ ≥ 1 − c/(log|t|)^{2/3}(log log|t|)^{1/3}
  (Vinogradov–Korobov). Under RH the region is σ ≥ 1/2. Bridging this gap
  is the whole problem.
- **Proportion on the line.** Best unconditional is more than 41% (Bui,
  Conrey, Young 2011, with later refinements). Not 100%, and no known method
  pushes past a constant fraction.
- **Why the "no zero off the line" approach stalls.** The functional
  equation forces symmetry but not location. The pairing of zeros off the
  line cannot be contradicted by the equation alone; the difficulty is that
  ξ(s) is a Fourier transform of a positive-definite theta-type kernel, and
  controlling such transforms well enough to force an oscillation to vanish
  is the missing step.

### The verification result, stated precisely

Platt and Trudgian verified RH up to height 3×10¹². (Gourdon's earlier
2004 result reached 10¹³ zeros by *count*, which is a slightly different
and larger number than a height bound, so the two figures are not
directly comparable — the height bound is the stronger statement about
which zeros are covered.) The conjectured zero count up to height T is
N(T) ~ (T/2π)·log(T/2π), so this is a finite but enormous prefix. There
is no monotonicity principle letting a verified prefix imply the general
case — the property is not known to be inductive.

### What this repo's tool does and does not do

`tools/rh_zeros.py` checks the first N zeros, N=20 by default. It confirms
the numerical phenomenon is real and exactly as described, at trivial cost.
It is the same *kind* of check as the published result scaled down by a
factor of ~10¹², and it proves nothing that Platt–Trudgian did not already
prove. Treat it as a demonstration, not a contribution.

### Honest assessment

There is no credible near-term path to a proof. Any claim of a proof in a
repo like this should be treated as a bug until independently verified. The
useful contributions available here are expository: making the equivalences
above precise, computing zeros, and being scrupulous about the finite/infinite
line. That is what this repo should be good at.


## References

- Edwards, H.M. — Riemann's Zeta Function (1974)
- Bombieri, G. — "The Riemann Hypothesis" (Clay Millennium description)
- Odlyzko, A. — Zeros of the Riemann zeta function
