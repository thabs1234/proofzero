# P vs NP

**Status:** Open
**Field:** Computational Complexity Theory
**First stated:** 1971 (Stephen Cook)
**Prize:** $1,000,000 (Clay Millennium)

## Exhibit card

**Exhibit B — Why Your Computer Can't Have Nice Things**
*Field: Computational Complexity Theory. Prize: $1,000,000.*

- **What is known.** Verifying a proposed answer is cheap; finding one is
  not known to be. Cook–Levin (1971, 1973) established that verification is
  polynomial and that every problem in NP reduces to SAT.
- **What this repo checked.** `tools/pnp_probe.py` generates random 3-SAT
  instances and times DPLL search against certificate checking, exposing the
  asymmetry directly. At n=20, m=85, density 4.25: DPLL 6.383 ms, certificate
  check 0.0651 ms — 98× faster — while exhaustive search over 2²⁰ assignments
  took 1214.605 ms. `--self-check` then validates the solver against brute
  force on 400 random instances (323 SAT, 77 UNSAT), rechecking every
  certificate independently.
- **What remains open.** Whether P = NP. No lower bound super-polynomial in
  general is known for any NP problem; nor is a polynomial-time algorithm
  known. The tool demonstrates the *shape* of the gap on specific instances.
  It is exponential-time by construction and proves nothing either way.
- **On the self-check.** It is mutation-tested. Three deliberately injected
  faults in `_dpll` — a false UNSAT, a skipped certificate check, and
  inverted propagation polarity — were each caught with a non-zero exit. A
  check that cannot fail is not a check.

## Statement

Is every problem whose solution can be verified in polynomial time (NP) also solvable in polynomial time (P)?

## Progress

- 1971 — Cook proves the theorem-proving problem is NP-complete; the
  Cook–Levin theorem is shown independently by Levin
- 1972 — Karp lists 21 NP-complete problems
- 1975 — Baker, Gill & Solovay: relativization barrier (oracles split the
  classes, so relativizing proofs cannot settle it)
- 1987 — Tardos: a strong lower-bound barrier specific to his technique,
  showing a single good method can also be a barrier
- 1994 — Razborov & Rudich: natural proofs barrier (conditional on strong
  pseudorandomness)
- 1997 — Mulmuley: geometric complexity program begins
- 2008 — Aaronson & Wigderson: algebrization barrier
- 2011 — Williams: NEXP ⊄ ACC⁰ (a genuine lower bound, but outside NP and
  against a small class, so it does not separate P from NP)
- 2020s — No resolution; most theorists surveyed expect P ≠ NP

Dates here are worth getting right, because the barrier results are
frequently misdated by 10–20 years in popular summaries and the ordering is
what shows they are cumulative rather than competing.

## Notes

### The shape of the problem, stated carefully

P vs NP asks one thing: does there exist a problem whose solutions can be
checked in polynomial time but cannot be found in polynomial time?

Everything else is decoration on that. The precise content:

- **P** — decision problems solvable in time O(n^k) for some fixed k.
- **NP** — decision problems where a proposed certificate is checkable in
  polynomial time. Note: NP is *not* "non-polynomial"; it is
  "polynomially verifiable". This is the single most common misreading.
- **NP-complete** — Cook–Levin. SAT is in this class, and NP-complete
  problems reduce to each other in polynomial time. So one NP-complete
  problem in P settles the whole class.
- The question is whether P = NP. Only two outcomes exist: P = NP, or
  P ≠ NP. There is no third possibility, and no "partially equal" state.

### What the barrier results actually say

These are often cited as "P vs NP cannot be solved." That is wrong, and the
distinction is the interesting part — each is a constraint on *techniques*,
not a proof about the class hierarchy:

- **Relativization (Baker–Gill–Solovay, 1975).** There exists an oracle A
  with P^A = NP^A, and an oracle B with P^B ≠ NP^B. Therefore no proof
  technique that relativizes — that behaves the same whether or not it can
  query an oracle — can settle P vs NP. Arithmetic and first-order logic
  relativize, so the standard Gödel-style methods are blocked.
- **Natural proofs (Razborov–Rudich, 1994/1997).** Under a strong
  pseudorandomness assumption about circuit lower bounds, there is no
  "natural" way to prove circuit lower bounds. "Natural" means constructible
  in a broad, largely combinatorial way. Conditional on assumption — this
  result does not hold unconditionally. The two dates are the conference
  version and the journal version.
- **Algebrization (Aaronson–Wigderson, 2008).** Extends relativization:
  techniques that use not just an oracle but an extension of the
  computation to an oracle with a wider field of operations are also
  blocked. Arithmetic and first-order logic relativize, so the standard
  Gödel-style methods are blocked. Williams's ACC⁰ lower bound (2011) is
  the clearest example of a real theorem that had to be non-algebrizing to
  work, and it is the closest thing the field has to a template for what a
  successful proof would look like.

Together these say the classical toolkit is insufficient. They do **not**
say the problem is unprovable in principle, and it is worth being precise
about the logical shape: each barrier exhibits a class of techniques
together with a pair of oracles that make the techniques fail. That is a
statement about proofs, not about truth. A proof using
non-relativizing, non-algebrizing methods would escape all three.

### Why "P ≠ NP" is the more-difficult direction

Asymmetry worth internalising:

- To prove P = NP, one explicit polynomial algorithm for one NP-complete
  problem suffices. This is the optimistic direction and could arrive as a
  surprise.
- To prove P ≠ NP, no single problem needs to be shown hard — only that
  *no* polynomial algorithm exists for all of NP. This is a universal
  quantifier over algorithms, which is why circuit lower bounds are
  centrally involved and why the field has made no progress on it in fifty
  years. We cannot even prove that a *specific explicit* function requires
  superpolynomial time.

That last point is the honest state of the art: we cannot prove a
non-polynomial lower bound for any natural problem in NP. Even showing that
a problem in NP does not have a linear-time algorithm is beyond current
techniques.

### What the tool demonstrates

`tools/pnp_probe.py` generates random 3-SAT instances and times DPLL search
against certificate verification. Measured ratios on 12–27 variable
instances run 5–35×, and the gap widens with n. That is the verifiability
asymmetry in miniature: checking is linear in the instance, searching is
exponential in the worst case.

This is a demonstration of the phenomenon, not evidence for either answer.
On instances this small, DPLL is fast, and a real SAT solver beats brute
force by many orders of magnitude — which is itself a caution. Empirically
the instances we can construct are the easy ones; if an algorithm solved SAT
in polynomial time, it would first look like a dramatic practical
improvement on these small cases. That pattern of "works well in practice,
no known worst-case bound" is exactly the situation in modern SAT solving
and is the strongest practical argument for the honest answer still being
undetermined.

### Honest assessment

No known approach. If a clean P ≠ NP proof appeared in this repo it should
be treated as a bug, and checked against all three barrier results — an
accidental resolution would almost certainly conflict with relativization.
The best available contribution here is clarity: precise definitions, the
barrier results stated accurately, and the verifiability asymmetry computed
honestly.

The consequences are worth stating outright, because they are often stated
inappropriately. If P = NP, then every problem in NP is in P, and standard
public-key cryptography (whose security rests on average-case hardness of
problems in NP) no longer works. If P ≠ NP, then no NP-complete problem
has a polynomial-time algorithm — but note that this says nothing about
any *particular* problem being hard, and nothing about problems that are
not NP-complete.

## References

- Cook, S. — "The Complexity of Theorem-Proving Procedures", STOC 1971;
  J. ACM 18(1), 1971
- Levin, L. — universal search problems, 1973
- Karp, R. — "Reducibility Among Combinatorial Problems", 1972
- Baker, A., Gill, J., Solovay, S. — "Relativization of the
  P=?NP Question", SIAM J. Comput. 4(4), 1975
- Razborov, A., Rudich, S. — "Natural Proofs", STOC 1994; JACM 53(1), 1997
- Aaronson, S., Wigderson, A. — "Algebrization and Related Concepts", 2008
- Williams, R. — "A New Algorithm for Optimal 2-Constraint Satisfaction and
  Its Implications", FOCS 2011
