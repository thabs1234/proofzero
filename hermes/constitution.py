#!/usr/bin/env python3
"""
ProofZero constitution — invariants the automation must never violate.

This module is the single place that decides what may and may not be done
to `thabs1234/proofzero`. It is imported as Python, not read as config, so it
cannot be changed by an environment variable, a CLI flag, or a cron edit.

The sets below are DERIVED from `problems/_status.json`, which is the repo's
canonical machine-readable status. They are not hand-listed. An earlier
hand-written version declared ids like "bsd" and "hodge" while the repo used
"birch-swinnerton-dyer" and "hodge-conjecture", so the frozen check could
never fire on a real id — the frozen problems were only being stopped by the
fallback pushable rule, by accident. Deriving removes that whole class of
drift: if a problem is renamed, added, or removed, the constitution follows.

Nothing here pushes a mathematical bound, and nothing here changes a
problem's status. The only thing it does is refuse.
"""

from __future__ import annotations

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo root — anchored to this file's location, NOT to the process cwd.
# ---------------------------------------------------------------------------
# hermes/constitution.py -> parents[1] == repo root.
# A relative VOID_FILE previously compared equal to a real path only when the
# cwd happened to line up; a write to ../problems/nothing.md from inside
# hermes/ sailed straight through the guard.
REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_FILE = REPO_ROOT / "problems" / "_status.json"
VOID_FILE = REPO_ROOT / "problems" / "nothing.md"

# The four Millennium problems with no tool. Derived, not listed.
FROZEN_FOUR_IDS = frozenset({
    "navier-stokes",
    "yang-mills-mass-gap",
    "birch-swinnerton-dyer",
    "hodge-conjecture",
})

# Problems with a real tool in this repo. Bounds here are finite and local.
PUSHABLE_IDS = frozenset({
    "riemann-hypothesis",
    "p-vs-np",
    "collatz",
    "goldbach",
    "twin-prime",
})

# Documented for the record. Solved; no tool; nothing to push.
SOLVED_IDS = frozenset({"poincare-conjecture"})


class ConstitutionalViolation(RuntimeError):
    """Raised when automation attempts something the repo forbids."""


def _load_status() -> dict:
    if not STATUS_FILE.is_file():
        raise ConstitutionalViolation(
            f"STATUS FILE MISSING: {STATUS_FILE}. The constitution derives its "
            f"invariants from this file and refuses to guess."
        )
    with open(STATUS_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def load_problems() -> list[dict]:
    """Return the problem entries from the canonical status file."""
    data = _load_status()
    problems = data.get("problems") if isinstance(data, dict) else data
    if not isinstance(problems, list):
        raise ConstitutionalViolation(
            "problems/_status.json has no 'problems' list. Refusing to continue."
        )
    return problems


def derive_sets() -> dict[str, frozenset]:
    """
    Classify every problem in the repo from its own declared fields.

    A problem is:
      frozen  — status open, no tool, and one of the four declared ids
      solved  — status solved
      pushable— status open with a tool path

    `tool: null` alone is NOT the frozen test: the solved Poincare entry also
    has `tool: null`, and conflating the two would let a future solved problem
    masquerade as a frozen one and vice versa.
    """
    problems = load_problems()
    frozen, pushable, solved = set(), set(), set()

    for p in problems:
        pid, status, tool = p.get("id"), p.get("status"), p.get("tool")
        if not pid:
            raise ConstitutionalViolation("A status entry has no id.")
        if status == "solved":
            solved.add(pid)
        elif tool is None and pid in FROZEN_FOUR_IDS:
            frozen.add(pid)
        elif tool is None:
            raise ConstitutionalViolation(
                f"UNKNOWN TOOL-LESS PROBLEM: '{pid}' is open with no tool but is "
                f"not one of the four declared-frozen ids. Either it is a new "
                f"frozen problem and must be added to FROZEN_FOUR_IDS "
                f"deliberately, or its status is wrong. Refusing to guess."
            )
        else:
            pushable.add(pid)

    return {
        "frozen": frozenset(frozen),
        "pushable": frozenset(pushable),
        "solved": frozenset(solved),
    }


def assert_invariants_hold() -> None:
    """
    Cross-check the derived sets against the declared ones.

    If _status.json is edited so that a frozen problem gains a tool, or a
    pushable one loses its tool, this raises. That is the whole point: the
    declaration and the canonical file must agree before anything runs.
    """
    s = derive_sets()

    if s["frozen"] != FROZEN_FOUR_IDS:
        raise ConstitutionalViolation(
            f"FROZEN SET DRIFT: _status.json says {sorted(s['frozen'])}, "
            f"constitution declares {sorted(FROZEN_FOUR_IDS)}. A frozen problem "
            f"gained or lost a tool. This must be reviewed as a deliberate "
            f"change to the repo's own claims, not silently absorbed."
        )
    if s["pushable"] != PUSHABLE_IDS:
        raise ConstitutionalViolation(
            f"PUSHABLE SET DRIFT: _status.json says {sorted(s['pushable'])}, "
            f"constitution declares {sorted(PUSHABLE_IDS)}."
        )
    if s["solved"] != SOLVED_IDS:
        raise ConstitutionalViolation(
            f"SOLVED SET DRIFT: _status.json says {sorted(s['solved'])}, "
            f"constitution declares {sorted(SOLVED_IDS)}."
        )


# --- Public guards ----------------------------------------------------------

def assert_not_frozen(problem_id: str) -> None:
    """Refuse the four problems the repo declares will never have a tool."""
    assert_invariants_hold()
    if problem_id in FROZEN_FOUR_IDS:
        raise ConstitutionalViolation(
            f"FROZEN PROBLEM: '{problem_id}' is in permanent no-tool state. "
            f"The repo declares this explicitly and it is not a gap awaiting "
            f"effort. No tool will be built for it here. Refusing to proceed."
        )


def assert_pushable(problem_id: str) -> None:
    """Refuse any bound push for a problem outside the pushable set."""
    assert_invariants_hold()
    if problem_id in FROZEN_FOUR_IDS:
        raise ConstitutionalViolation(
            f"FROZEN PROBLEM: '{problem_id}' is in permanent no-tool state. "
            f"Refusing to push."
        )
    if problem_id in SOLVED_IDS:
        raise ConstitutionalViolation(
            f"SOLVED PROBLEM: '{problem_id}' is already solved. There is no "
            f"bound to push. Refusing."
        )
    if problem_id not in PUSHABLE_IDS:
        raise ConstitutionalViolation(
            f"NOT PUSHABLE: '{problem_id}' is not in the pushable set. "
            f"Pushable: {sorted(PUSHABLE_IDS)}. "
            f"Frozen: {sorted(FROZEN_FOUR_IDS)}. Refusing to push."
        )


def assert_void_untouched(path: Path) -> None:
    """
    Refuse any write to problems/nothing.md.

    A relative path means relative to the CWD, which is what `open()` will
    actually do with it — so the guard must resolve it the same way or it
    guards something other than the file that gets written. Anchoring the
    candidate to REPO_ROOT instead was wrong: `../problems/nothing.md` then
    resolved to a path OUTSIDE the repo and matched nothing.

    VOID_FILE is already absolute (anchored to REPO_ROOT), so the guard holds
    from any working directory. A path outside the repo is not the void and is
    left alone.
    """
    candidate = Path(path).absolute()  # cwd-relative if relative, no normalisation
    try:
        resolved = candidate.resolve()
        void = VOID_FILE.resolve()
    except OSError:
        return
    if resolved == void:
        raise ConstitutionalViolation(
            f"VOID VIOLATION: '{path}' resolves to problems/nothing.md. "
            f"The void is the point of this repository. Refusing to write."
        )


def assert_known_id(problem_id: str) -> None:
    """Refuse ids that do not exist in the repo at all."""
    ids = {p.get("id") for p in load_problems()}
    if problem_id not in ids:
        raise ConstitutionalViolation(
            f"UNKNOWN PROBLEM ID: '{problem_id}' is not in _status.json. "
            f"Known: {sorted(i for i in ids if i)}."
        )


def assert_no_status_mutation(field: str) -> None:
    """
    Refuse writes to the fields that record mathematical status.

    verified_here and verified_elsewhere exist to keep "this repo ran it" and
    "this repo cites it" apart. Merging them, or letting a routine automation
    touch them, is exactly the failure the whole repo is built to prevent.
    """
    protected = {
        "status", "verified_here", "verified_elsewhere",
        "open_edge", "tool", "source", "solved_on", "verified_on_disk",
    }
    if field in protected:
        raise ConstitutionalViolation(
            f"STATUS FIELD PROTECTED: '{field}' records mathematical status or "
            f"its provenance. Automation may not write it. Refusing."
        )


__all__ = [
    "REPO_ROOT", "STATUS_FILE", "VOID_FILE",
    "FROZEN_FOUR_IDS", "PUSHABLE_IDS", "SOLVED_IDS",
    "ConstitutionalViolation",
    "load_problems", "derive_sets", "assert_invariants_hold",
    "assert_not_frozen", "assert_pushable", "assert_void_untouched",
    "assert_known_id", "assert_no_status_mutation",
]
