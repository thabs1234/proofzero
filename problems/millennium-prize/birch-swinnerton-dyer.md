# Birch and Swinnerton-Dyer Conjecture

**Status:** Open
**Field:** Arithmetic Geometry / Elliptic Curves
**Prize:** $1,000,000 (Clay Millennium)

## Statement

For an elliptic curve E over ℚ, the rank of E(ℚ) equals the order of vanishing of L(E,s) at s=1.

## Progress

- 1965 — Birch & Swinnerton-Dyer formulate the conjecture from numerical
  evidence; the rank statement is sharpened in later work
- 1977 — Coates–Wiles: for CM curves, L(E,1) ≠ 0 ⟹ E(ℚ) finite
- 1986 — Gross–Zagier: L(E,1) = 0 and L'(E,1) ≠ 0 ⟹ rank 1
- 1988–1990 — Kolyvagin: the rank-0 and rank-1 cases are resolved
- 2001 — Modularity is proved (Wiles; Taylor–Wiles; Breuil–Conrad–Diamond–Taylor),
  removing the main conditional assumption
- 1990s onward — Iwasawa main conjecture, Skinner–Urban, and p-adic
  approaches extend the picture
- Open for rank ≥ 2 in general; also open in two other directions (see below)

## Notes

### The two halves, and where BSD is *least* famous

BSD has three parts, and the famous identity is only the first.

1. **The rank identity.** ord_{s=1} L(E,s) = rank E(ℚ).
2. **The leading coefficient formula.** The exact value
   L(E,1)/ord₁ L(E,1) = (#Sha(E)·Reg(E)·Ω(E)·∏c_p)/|E(ℚ)_tors|²,
   where Sha is the Tate–Shafarevich group, Reg the regulator, Ω the real
   period, c_p the Tamagawa numbers.
3. **Sha is finite.**

Part 1 is the conjecture as usually stated. Part 2 is quantitatively far
harder and would be the practically useful one. Part 3 is a finiteness
question about an explicitly-defined group that is nonetheless unsolved in
general.

BSD is thus best read as a single hypothesis standing behind three
separate open problems, and reporting only "rank = order of vanishing"
understates it considerably.

### Rank 0 and 1 are proved; the general case is not

The Kolyvagin–Gross–Zagier machinery settles BSD in ranks 0 and 1,
conditionally on modularity of E over ℚ. Modularity itself was proved
completely (Wiles, Taylor–Wiles, Breuil–Conrad–Diamond–Taylor, 2001), so
the reduction is unconditional for curves over ℚ.

The rank-1 result has a beautiful structure worth understanding. The
Gross–Zagier formula converts the derivative L'(E,1) into a *height
difference* between two points on E, via a Heegner point. This is applied
in the setting where L(E,1) = 0 and L'(E,1) ≠ 0; the nonzero height
difference then forces the Heegner point to be infinite order, so the rank
is at least 1. Kolyvagin's Euler-system argument then shows this is
exactly the rank, bounding the dual Selmer group and forcing Sha
to be finite in this case.

The essential feature is the existence of a formula linking an analytic
quantity to a geometric one. For rank ≥ 2, no such formula is known.
Higher-rank Heegner points are the natural candidate and are the subject
of active work (Darmon–Dasgupta–Pollack, Mok), but nothing comparable to
Gross–Zagier is available. This is a genuine gap in method, not a gap in
arithmetic bookkeeping.

### The direction "Sha is finite" is arguably the deeper one

Note the asymmetry in the proved cases: Kolyvagin shows Sha finite when
the rank is 0 or 1. But Sha can be nontrivial even when the rank is low,
and no one has proved Sha is always finite. Because Sha is a cohomology
group defined by torsors that are locally — and, so far, globally —
unobvious, its finiteness is the kind of statement that would require
genuinely new methods.

### What the rank-0/1 theorems do and do not give you

Kolyvagin's argument, combined with modularity, does prove for E/ℚ that
L(E,1) ≠ 0 implies rank 0. So the Clay statement is unconditional in rank
0 today. Two things are commonly conflated with it and should be kept
apart:

- The **leading-coefficient formula** is not proved by the rank-0/1
  machinery in general. Knowing the rank does not determine the value of
  the quotient L(E,1)/ord₁L(E,s).
- Extending to **arbitrary number fields** is a separate and much harder
  question; the results there are more recent and more restricted than
  the E/ℚ case, and this note makes no claim about them.

The historically important detail is that Coates–Wiles (1977) proved only
the CM case; extending it off the CM locus required the modularity results
of 1990–2001.

### Why numerics are not the answer

BSD is one of the most heavily tested conjectures in mathematics: the rank
identity has been verified on very large numbers of curves, up to and
beyond conductor 500,000, with no counterexample found. But the tests are
not convergent — nothing in a finite test forces the formula to hold at
the next curve — and Sha in particular is defined as a quotient of a
locally finite group by a subgroup, so its order can only be computed
after already knowing it is finite. The verification data is genuine
evidence and should not be dismissed; it simply has the same
epistemic status as Goldbach's 4×10¹⁸, for the same reason.

### Honest assessment

Ranks 0 and 1 are done. The general identity, the leading-coefficient
formula, and Sha-finiteness are open. Any proof here should be treated as
a bug. The defensible content is: the three-part structure stated
accurately, the Gross–Zagier mechanism described, the rank ≥ 2 gap
located in the absence of any higher-rank analogue, and an honest
account of the numerical evidence.
