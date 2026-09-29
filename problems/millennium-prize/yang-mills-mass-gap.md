# Yang-Mills Mass Gap

**Status:** Open
**Field:** Quantum Field Theory / Mathematical Physics
**Prize:** $1,000,000 (Clay Millennium)

## Exhibit card

**Exhibit G — The Problem Where the Physics Is More Precise Than the Math**
*Field: Quantum Field Theory / Mathematical Physics. Prize: $1,000,000.*

- **What is known.** Non-abelian gauge theories are the ones that describe
  the Standard Model, and they are mathematically ill-defined at the level
  needed for anything rigorous. The mass gap is empirically confirmed across
  the Standard Model to extraordinary precision. Existence and construction
  of a suitable Yang–Mills theory in four dimensions is proved only in
  restricted settings — notably supersymmetric, small-Higgs cases, and
  Abelian theories, which are *not* the case the Prize asks about.
- **What this repo checked.** **Nothing.** There is no computational tool in
  this repository for this problem. Lattice QCD provides overwhelming
  numerical evidence for a mass gap, but a simulation that never closes
  predicts an open trajectory's worth of mass; it cannot exclude a
  discontinuity. This card states a bound of *no* bound.
- **What remains open.** Existence of a well-defined, complete, Lorentz-
  invariant quantum Yang–Mills theory in 3+1 dimensions with a mass gap, and
  the Clay formulation's stronger quantitative form. This is a problem of
  existence, not of approximation, and computation is structurally the wrong
  tool.
- **The trap worth naming.** The Abelian and supersymmetric results are
  often cited as if they substantially reduce the hard case. They do not:
  asymptotic freedom in 4D non-supersymmetric Yang–Mills is precisely the
  regime the theory is conjectured to need, and that is the part still
  unproved.

## Statement

Prove that for any compact simple gauge group, Yang-Mills theory on ℝ⁴ has a mass gap Δ > 0.

## Progress

- 1954 — Yang & Mills introduce non-abelian gauge theory (classical)
- 1971 — 't Hooft & Veltman establish perturbative renormalizability
- 1973 — Gross, Wilczek, Politzer: asymptotic freedom
- 1975 — 't Hooft & Polyakov: finite-action (instanton) solutions
- 1979 — 't Hooft: dimensional transmutation
- 1980s–90s — rigorous non-perturbative constructions in lower
  dimensions, including 3D Yang-Mills
- Lattice QCD simulations indicate a mass gap numerically
- No rigorous four-dimensional construction; no proof

## Notes

### The statement hides a much bigger problem

The mass gap is the stated target, but it is conditional on a prior
achievement that has not happened. The Clay problem asks for a
construction of four-dimensional non-abelian Yang-Mills theory that is:

1. **Mathematically well-defined.** A rigorous construction, not a
   formal series of diagrams. This is the hard prerequisite.
2. **Relativistic.** Consistent with special relativity.
3. **Quantized.** With a well-defined quantum vacuum.
4. **Locally finite.** The theory is defined at a point, not only in a
   perturbative expansion around a chosen scale.
5. **Renormalizable.** Removing infinitely many divergences by adjusting a
   finite number of parameters.

Yang and Mills wrote down a consistent **classical** non-abelian gauge
theory, which is the origin of (2)–(4) in classical form. They did not
quantize it, and they proved nothing about the quantum theory. What is
missing is (1) combined with (5): a rigorous, non-perturbative
construction of the *quantum* four-dimensional theory. 't Hooft and
Veltman showed the perturbation series is renormalizable, and there are
rigorous constructions of the **three-dimensional** theory, but the
four-dimensional, fully quantum, non-perturbative case is exactly the one
that has not been constructed.

So a proof of the mass gap would, in practice, require first constructing
the theory. This is why the problem is sometimes characterised as
understating its own difficulty.

### Why 4D specifically is the hard case

Yang-Mills theory is well understood in **two** dimensions (it is a
scale-invariant, essentially topological theory there) and has rigorous
constructions in **three** dimensions. In 4D:

- **Perturbative renormalizability works** (r = 0, the gauge coupling is
  dimensionless at the fixed point). Asymptotic freedom (Gross, Wilczek,
  Politzer, 1973) explains why: the theory is free at high energy and
  strongly coupled at low energy.
- **Non-perturbative control is absent.** The coupling becomes strong at
  low energies — precisely where the mass gap lives. There is no small
  parameter to expand in, and the functional integral defining the theory
  is not known to be well-posed in continuum.

The relationship is suggestive but not deductive: asymptotic freedom is
what one *expects* to underlie a mass gap and it fixes the running of the
coupling, but asymptotic freedom is a statement about the perturbative
ultraviolet, and it does not by itself establish the non-perturbative
infrared. The physics is in the infrared.

### What a mass gap would mean

The mass gap Δ > 0 says the theory is not a massless, scale-invariant
(CFT-like) theory: there is a finite energy cost Δ, to creating a single
physical excitation above the vacuum. Operationally: correlators of
separately-created fields at widely separated points decay exponentially
rather than as a power law.

The distinction between Δ > 0 and Δ = 0 is the distinction between a mass
and a conformal field theory, and it is the dividing line between the
Standard Model's behaviour and what we observe in the strong interactions.
The gluon, if massless (Δ = 0 in the pure gauge theory), would mean the
strong force is mediated by a massless boson. Every experiment we have
says gluons are not free, light, and long-range — the strong force is
confined and short-range, which requires a gap. So the empirical answer is
not seriously in doubt; what is missing is the proof.

### The lattice approach, and what it does and does not establish

Lattice QCD discretises spacetime onto a finite grid, making the path
integral a large but finite sum — computable, and genuinely
non-perturbative. Lattice calculations confirm a mass gap and are among
the best quantitative successes in the field. Gauge fixing, chiral
continuum limit, and infinite-volume control remain open issues, and
continuum extrapolation is not a theorem. Numerical confirmation of the
mass gap, however convincing, is not a proof; the limit in which the
lattice spacing tends to zero is exactly the limit no finite computation
reaches.

### Honest assessment

This is a construction problem, not a technical estimate. Even if the mass
gap statement alone were isolated, a proof would need the theory to exist
first. Treat any proof here as a bug. The defensible content is: the
distinction between the stated goal and the prerequisite construction, the
role of asymptotic freedom as a UV result, the meaning of Δ > 0
operationally, and an honest account of why lattice evidence is evidence
and not proof.
