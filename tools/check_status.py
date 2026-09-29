"""Check that problems/_status.json still agrees with the notes and tools.

_status.json is a machine-readable mirror of the exhibit cards. A mirror
is only useful while it is true, so this runs in CI and fails when the
JSON claims something the repository no longer supports.

It checks the things that can be checked cheaply and mechanically:
  * every declared problem file exists, and exists at the stated path
  * every "file" field points at a note that exists
  * the counts block matches the entries
  * every named tool exists in tools/
  * every entry with a tool has a verified_here record with a command
  * every entry without a tool says so, and says why
  * nothing.md is NOT counted as a problem
  * no runtime is ever used as a pass/fail criterion

What it deliberately does NOT check: that a published bound in
"verified_elsewhere" is correct. Those are cited, not reproduced here,
and this repository does not claim to have verified them.

Exit 0 if consistent, 1 with a list of problems otherwise.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_PATH = os.path.join(ROOT, "problems", "_status.json")
TOOLS_DIR = os.path.join(ROOT, "tools")

# The four Millennium problems with no honest finite check, plus Poincare
# which is solved and needs no tool.
EXPECT_NO_TOOL = {
    "navier-stokes",
    "yang-mills-mass-gap",
    "birch-swinnerton-dyer",
    "hodge-conjecture",
    "poincare-conjecture",
}

# Values that must reproduce exactly on a passing run. A change here is a
# real behavioural change and should fail CI.
EXACT_RESULTS = {
    "riemann-hypothesis": {"worst_deviation": "0.0 at working precision (2.58e-26 at 200 zeros)"},
    "p-vs-np": {"result": "323 SAT / 77 UNSAT; DPLL vs brute-force disagreements 0; invalid certificates 0"},
    "collatz": {"result": "max trajectory 382 steps; max peak 17202377752"},
    "goldbach": {"result": "min representations 1; 0 violations"},
    "twin-prime": {"result": "2160 pairs; largest in range (199931, 199933)"},
}


def main():
    problems = []
    with open(STATUS_PATH, encoding="utf-8") as handle:
        data = json.load(handle)

    entries = data["problems"]

    # --- files referenced actually exist, at the stated path -------------
    for entry in entries:
        rel = entry.get("file")
        if not rel:
            problems.append("%s: no 'file' field" % entry.get("id"))
            continue
        if not os.path.isfile(os.path.join(ROOT, rel)):
            problems.append("%s: note not found at %s" % (entry["id"], rel))

    # --- counts block matches the entries ---------------------------------
    counts = data["counts"]
    open_n = sum(1 for e in entries if e["status"] == "open")
    solved_n = sum(1 for e in entries if e["status"] == "solved")
    with_tool = sum(1 for e in entries if e.get("tool"))

    if counts["problems"] != len(entries):
        problems.append("counts.problems=%d but %d entries"
                        % (counts["problems"], len(entries)))
    if counts["open"] != open_n:
        problems.append("counts.open=%d but %d open" % (counts["open"], open_n))
    if counts["solved"] != solved_n:
        problems.append("counts.solved=%d but %d solved"
                        % (counts["solved"], solved_n))
    if counts["with_tool"] != with_tool:
        problems.append("counts.with_tool=%d but %d entries carry a tool"
                        % (counts["with_tool"], with_tool))
    if counts["without_tool"] != len(entries) - with_tool:
        problems.append("counts.without_tool=%d but %d lack a tool"
                        % (counts["without_tool"], len(entries) - with_tool))

    # --- tool coherence ---------------------------------------------------
    for entry in entries:
        ident = entry["id"]
        tool = entry.get("tool")
        checked = entry.get("verified_here")

        if tool is None:
            if checked:
                problems.append("%s: no tool but claims verified_here" % ident)
            if ident not in EXPECT_NO_TOOL:
                problems.append("%s: has no tool but is not in EXPECT_NO_TOOL; "
                                "if that is deliberate, list it there" % ident)
        else:
            if not os.path.isfile(os.path.join(ROOT, tool)):
                problems.append("%s: tool not found at %s" % (ident, tool))
            if not checked:
                problems.append("%s: has a tool but no verified_here" % ident)
            elif not checked.get("command"):
                problems.append("%s: verified_here has no command" % ident)

    # every tool-less entry must carry a note explaining the absence
    for entry in entries:
        if entry.get("tool") is None and not entry.get("note"):
            problems.append("%s: no tool and no note explaining why" % entry["id"])

    # --- nothing.md is not a problem --------------------------------------
    if any("nothing" in (e.get("file") or "") for e in entries):
        problems.append("nothing.md must not appear as a problem entry")
    note_path = os.path.join(ROOT, "problems", "nothing.md")
    if os.path.isfile(note_path):
        with open(note_path, encoding="utf-8") as handle:
            if re.search(r"^## Exhibit card", handle.read(), re.M):
                problems.append("nothing.md has an Exhibit card; it must not")

    # --- exact results still match what the notes claim --------------------
    for ident, fields in EXACT_RESULTS.items():
        entry = next((e for e in entries if e["id"] == ident), None)
        if entry is None:
            problems.append("EXACT_RESULTS lists %s but it is not in _status.json" % ident)
            continue
        checked = entry.get("verified_here") or {}
        for key, expected in fields.items():
            actual = checked.get(key)
            if actual != expected:
                problems.append("%s: %s changed\n      expected: %s\n      actual:   %s"
                                % (ident, key, expected, actual))

    # --- runtimes are never load-bearing -----------------------------------
    # A runtime that varies by machine must not decide pass/fail. Assert the
    # file declares that, and that no runtime field doubles as a result.
    if "runtime" in json.dumps(data["counts"]).lower():
        problems.append("counts must not contain runtime data")
    for entry in entries:
        checked = entry.get("verified_here") or {}
        for key in ("result", "worst_deviation"):
            value = checked.get(key)
            if isinstance(value, str) and "sec" in value:
                problems.append("%s: %s mentions a time; timings must be "
                                "informational only" % (entry["id"], key))

    # --- report ------------------------------------------------------------
    if problems:
        print("_status.json is out of step with the repository:\n")
        for item in problems:
            print("  - %s" % item)
        print("\nFix the JSON or the note, whichever is now wrong.")
        return 1

    print("_status.json is consistent with the notes and tools.")
    print("  %d problems, %d open, %d solved, %d with a tool"
          % (len(entries), open_n, solved_n, with_tool))
    print("  %d cited-without-reproduction, as intended."
          % sum(1 for e in entries if e.get("verified_elsewhere")))
    print("  Timings are informational; only the exact results above are asserted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
