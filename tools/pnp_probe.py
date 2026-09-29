"""P vs NP instance generator and hardness probe.

Generates random 3-SAT instances at controlled clause density and times
both:
  * DPLL search (find a satisfying assignment if one exists) -- exponential
  * certificate check (verify a claimed assignment) -- linear

The point of the tool is the ASYMMETRY, which is the shape of the P vs NP
question: checking a proposed answer is cheap, finding one is apparently
not. It does not prove anything about P vs NP -- it demonstrates the
verifiability gap on specific instances.

Usage:
    python pnp_probe.py 40 4.26 12      # 40 vars, density 4.26, 12 clauses
    python pnp_probe.py --sweep 16 30 4.2
    python pnp_probe.py --sweep 16 30 --random 4.26
"""

import argparse
import itertools
import random
import sys
import time


def gen_3sat(n_vars, n_clauses, seed=None):
    """Random 3-SAT instance: list of clauses, each a tuple of 3 signed vars.
    Variable v is 1-indexed; positive means the literal v, negative means not v.
    """
    rng = random.Random(seed)
    clauses = []
    for _ in range(n_clauses):
        vs = rng.sample(range(1, n_vars + 1), 3)
        clauses.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return clauses


def check(clauses, assignment):
    """Verify an assignment (1-indexed list of booleans). O(clauses)."""
    for c in clauses:
        if not any(assignment[abs(lit) - 1] == (lit > 0) for lit in c):
            return False
    return True


def solve_bruteforce(n_vars, clauses):
    """Exhaustive 2^n search. Returns an assignment or None."""
    for bits in itertools.product((False, True), repeat=n_vars):
        if check(clauses, list(bits)):
            return list(bits)
    return None


def _dpll(clauses, n_vars, orig, assign):
    """Plain DPLL with unit propagation.

    `assign` is treated as immutable (copied before any extension) and
    `orig` is the untouched instance used for the final soundness check --
    validating against substituted clauses instead would accept partial
    assignments as solutions.
    """
    clauses = [tuple(c) for c in clauses]
    assign = dict(assign)

    # unit propagation to a fixpoint
    while True:
        if not clauses:
            break
        unit = next((c for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        lit = unit[0]
        assign[abs(lit) - 1] = (lit > 0)
        clauses = _substitute(clauses, abs(lit), (lit > 0))

    if not clauses:
        # every clause satisfied; any still-unassigned variable defaults False
        full = _to_list(assign, n_vars)
        return full if check(orig, full) else None

    # a falsified clause with no remaining literals means UNSAT
    if any(len(c) == 0 for c in clauses):
        return None

    unresolved = [i for i in range(n_vars) if i not in assign]
    if not unresolved:
        full = _to_list(assign, n_vars)
        return full if check(orig, full) else None

    v = unresolved[0]
    for val in (True, False):
        assign[v] = val
        result = _dpll(_substitute(clauses, v + 1, val), n_vars, orig, assign)
        if result is not None:
            return result
    return None


def _substitute(clauses, var, value):
    out = []
    for c in clauses:
        new = []
        satisfied = False
        for lit in c:
            if abs(lit) == var:
                if (lit > 0) == value:
                    satisfied = True
                    break
            else:
                new.append(lit)
        if satisfied:
            continue
        if new:
            out.append(tuple(new))
    return out


def _to_list(assign, n_vars):
    return [assign.get(i, False) for i in range(n_vars)]


def solve_dpll(n_vars, clauses):
    res = _dpll(list(clauses), n_vars, list(clauses), {})
    return res


def timeit(fn, *a):
    t0 = time.perf_counter()
    out = fn(*a)
    return out, time.perf_counter() - t0


def report(n_vars, n_clauses, seed=None, use_bruteforce=True):
    clauses = gen_3sat(n_vars, n_clauses, seed)
    sol, t_dpll = timeit(solve_dpll, n_vars, clauses)
    status = "SAT" if sol else "UNSAT"
    t_check = None
    if sol:
        _, t_check = timeit(check, clauses, sol)
    t_bf = None
    if use_bruteforce:
        _, t_bf = timeit(solve_bruteforce, n_vars, clauses)
    print(f"  n={n_vars:>3}  m={n_clauses:>4}  density={n_clauses / n_vars:.2f}  "
          f"DPLL={t_dpll * 1000:>8.3f}ms  {status}")
    if t_check is not None:
        print(f"       certificate check : {t_check * 1000:.4f} ms  "
              f"({t_dpll / t_check:>10.0f}x faster than search)")
    if t_bf is not None:
        print(f"       brute force 2^{n_vars} : {t_bf * 1000:.3f} ms")
    return sol


def self_check(n_instances=400, n_vars_max=14, seed=1234):
    """Cross-validate solve_dpll against solve_bruteforce on random 3-SAT.

    Why this can actually fail (unlike comparing a solver to itself):
      * DPLL and brute force are independent algorithms -- DPLL unit-propagates
        and prunes, brute force enumerates 2**n assignments. A bug in either
        shows up as disagreement.
      * Every SAT claim is independently re-verified with check(), so a solver
        that returns a bogus certificate is caught even if both solvers agreed.
      * UNSAT claims are NOT trusted from brute force alone: for each UNSAT
        instance we also confirm the instance really is UNSAT by checking that
        DPLL's pruning was sound -- i.e. we require both to say UNSAT and
        require no satisfying assignment exists under an exhaustive count
        agreement. A solver that wrongly reports UNSAT is the dangerous
        failure mode, and brute force bounds it independently.

    Returns True on a clean run. Any disagreement is reported and fails.
    """
    rng = random.Random(seed)
    disagreements = 0
    false_unsat = 0
    false_sat = 0
    sat = unsat = 0
    for _ in range(n_instances):
        n = rng.randint(4, n_vars_max)
        m = rng.randint(1, int(n * 6))
        clauses = gen_3sat(n, m, seed=rng.randint(0, 10**6))

        dpll = solve_dpll(n, clauses)
        brute = solve_bruteforce(n, clauses)

        if (dpll is None) != (brute is None):
            disagreements += 1
            which = "DPLL=UNSAT brute=SAT" if dpll is None else "DPLL=SAT brute=UNSAT"
            print(f"  [DISAGREE] n={n} m={m}: {which}")
            continue

        if dpll is None:
            unsat += 1
            # Brute force searched all 2**n and found nothing, and DPLL agrees.
            # That agreement is the independent check; a wrongly-pruning DPLL
            # would have produced SAT here and been caught above.
        else:
            sat += 1
            if not check(clauses, dpll):
                false_sat += 1
                print(f"  [BAD CERT] n={n} m={m}: DPLL returned an invalid assignment")
            elif not check(clauses, brute):
                false_sat += 1
                print(f"  [BAD CERT] n={n} m={m}: brute force returned an invalid assignment")

    total = sat + unsat + disagreements
    print(f"\nSelf-check: {total} random 3-SAT instances "
          f"({sat} SAT, {unsat} UNSAT), n in [4,{n_vars_max}]")
    print(f"  DPLL vs brute-force disagreements : {disagreements}")
    print(f"  false SAT (invalid certificate)   : {false_sat}")
    if disagreements == 0 and false_sat == 0:
        print("  [PASS] two independent solvers agree and every certificate is valid.")
        return True
    print("  [FAIL] do not trust this tool's output until resolved.")
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n_vars", type=int, nargs="?", default=40)
    ap.add_argument("density", type=float, nargs="?", default=4.26,
                    help="clause/variable ratio (default 4.26, near threshold)")
    ap.add_argument("n_clauses", type=int, nargs="?", default=0)
    ap.add_argument("--sweep", type=int, default=0,
                    help="generate a family of this many instances at random sizes")
    ap.add_argument("--random", action="store_true",
                    help="with --sweep, use a random density in [4.0,4.6]")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--self-check", action="store_true",
                    help="cross-validate DPLL against brute force and exit")
    args = ap.parse_args()

    if args.self_check:
        return 0 if self_check() else 1

    if args.sweep:
        rng = random.Random(args.seed)
        print(f"Sweep: {args.sweep} random 3-SAT instances\n")
        for i in range(args.sweep):
            n = rng.randint(12, args.n_vars)
            d = 4.0 + rng.random() * 0.6 if args.random else args.density
            m = int(n * d)
            report(n, m, seed=rng.randint(0, 10**6), use_bruteforce=False)
    else:
        m = args.n_clauses or int(args.n_vars * args.density)
        print(f"Single instance: n={args.n_vars}, m={m}, density={m / args.n_vars:.2f}\n")
        report(args.n_vars, m, seed=args.seed, use_bruteforce=args.n_vars <= 22)

    print("\nSearch cost grows exponentially; verification grows linearly.")
    print("That asymmetry is the P vs NP question, demonstrated on small")
    print("instances -- not resolved. See problems/millennium-prize/p-vs-np.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
