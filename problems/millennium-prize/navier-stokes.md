# Navier-Stokes Existence and Smoothness

**Status:** Open
**Field:** PDE / Fluid Dynamics
**First stated:** 1822 (Navier), 1845 (Stokes)
**Prize:** $1,000,000 (Clay Millennium)

## Statement

Do smooth, globally defined solutions to the 3D Navier-Stokes equations exist for all time, given smooth initial conditions?

## Progress

- 1934 — Leray: weak solutions exist
- 1964 — Fujita & Kato: local smooth solutions, small-data global existence
- 1982 — Caffarelli, Kohn, Nirenberg: partial regularity; the singular set
  has one-dimensional Hausdorff measure zero
- 1984 — Beale-Kato-Majda: blow-up criterion
- 1993 — Constantin & Fefferman: geometric singularity analysis
- 2010s — Energy bounds improved; no global existence proof

## Notes

The difficulty: turbulence — solutions may develop singularities in finite time.

### Two halves, and they are not equally hard

The Clay problem has two parts, and the field's partial progress is
extremely uneven between them. Clay's own numbering is Part 1
(existence and smoothness) and Part 2 (uniqueness); the substance is the
same split, and it is worth stating in Clay's own terms because the
usual shorthand gets it backwards:

- **Existence (Clay Part 1, existence half).** A global weak solution
  exists. **This is solved** — Leray (1934), with the Hopf–Lions
  inequality supplying the compactness. Every smooth initial datum has a
  global weak solution.
- **Regularity / uniqueness (Clay Parts 1-smoothness and 2).** That the
  solution is smooth for all time, and that weak solutions are unique.
  **This is open.**

The common shorthand "existence is solved, regularity is open" is accurate
but incomplete, and it invites a specific error: it suggests that the
remaining part is a smoothness question only. It is not. Part 2 asks that
there be exactly one weak solution, whether or not it is smooth, and
uniqueness is the harder of the two. A weak solution that blows up in
finite time would defeat Part 1 even though Part 2 is stated separately.

The reformulation that makes this clear: if weak solutions are unique,
then a global smooth solution exists. Uniqueness implies smoothness, so
uniqueness is the whole problem.

### Why uniqueness is the hard part

Nonlinearity. The equation is roughly
∂u/∂t + (u·∇)u = −∇p + νΔu.
The linear part, viscous diffusion, is well behaved in 3D — energy
estimates control it. The term that breaks everything is the advective
term (u·∇)u. It transports energy between scales without dissipating it,
which is precisely the mechanism of turbulence. No available estimate
controls the advection term tightly enough to close the energy argument in
3D. The dissipation is a viscosity ν so small in scale that the ratio of
advection to diffusion (the Reynolds number) is unbounded in the limit of
interest.

### The BKM criterion — where the problem was usefully localised

Beale, Kato and Majda (1984) gave the sharpest classical reduction: a smooth
solution can only blow up in finite time T if
∫₀ᵀ ‖ω(t)‖_{L∞} dt = ∞,
where ω is the vorticity (curl of velocity). So global smoothness is
equivalent to bounding a time integral of the vorticity supremum norm.

This is a genuine advance and also a good illustration of why the problem
resists. BKM reduces the question to a regularity estimate on vorticity —
the quantity that the advection term feeds nonlinearly, since vortex
stretching is the amplification mechanism. In 2D, vorticity is advected
and diffuses but never amplified, and BKM is trivially satisfied; the 2D
case is solved and global. The 3D obstruction is the single term
(ω·∇)u, the vortex-stretching term, which has no 2D analogue. Constantin
and Fefferman (1993) showed the obstruction is also geometric: the strain
matrix, not the vorticity magnitude, is what allows concentration, and
controlling the alignment between vorticity and strain is the crux.

### What Tao's 2016 result did and did not do

Tao produced finite-time blowup for a slightly *modified* 3D equation —
one with an extra damping term, essentially an averaged/regularised
version. This is a rigorously proved demonstration that the unmodified
equations can blow up under nearby conditions, which is real evidence that
the Clay conjecture is not trivially true.

It is not a counterexample to Navier-Stokes, and the boundary must be
stated precisely: the modified equation is not the equation on R³. Reading
Tao 2016 as "Navier-Stokes is false" is a mistake, and reading it as
"irrelevant" is also a mistake.

### Is the conjecture even believed?

This is unusual among the seven, and worth saying plainly. Many numerical
and physical researchers expect that 3D Navier-Stokes solutions *do* blow
up at high Reynolds number, and that a final answer of "no" (existence
fails) is at least as likely as "yes". Turbulence at Reynolds numbers of
10⁶ to 10⁸ is directly observed in engineering and the ocean, and the
physically correct description at those Reynolds numbers is a
statistical one, not a smooth solution.

So the Clay question may have a negative answer, and the $1M may go to
proving that a smooth 3D solution can blow up. The prize statement asks
for a proof either way. It is one of the very few Millennium problems
where a negative result is a live and respectable outcome.

This has a practical consequence for this repo: any claim here of
"proving" existence would be particularly suspect, because the working
assumption in much of the applied community runs the other way.

### Honest assessment

Global weak existence is done. Uniqueness and regularity are open, with a
good localisation (BKM) and a clear identified obstruction (vortex
stretching, absent in 2D). No proof either way is plausible with current
methods, and unlike most of the seven, a negative answer is considered a
live outcome by much of the applied community. Treat any resolution
appearing here as a bug. The defensible content is: the Clay part
structure stated correctly, the BKM reduction, the 2D/3D contrast used to
locate the obstruction, and Tao's 2016 result described with its
modification intact.
