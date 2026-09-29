"""Print the bound table from problems/_status.json.

Every bound shown under LOCAL CHECK is one this repository's own tools
actually ran. Larger published bounds live in the notes and are cited,
never reproduced here.

Usage:  python tools/status_table.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = os.path.join(ROOT, "problems", "_status.json")

NO_TOOL = {"navier-stokes", "yang-mills-mass-gap",
           "birch-swinnerton-dyer", "hodge-conjecture"}


def local_bound(entry):
    """What a tool in this repo checked, or why there is none."""
    if entry["id"] in NO_TOOL:
        return "no honest finite check exists"
    if entry.get("status") == "solved":
        return "solved %s (proof; not reproduced here)" % entry.get("solved_on", "")
    checked = entry.get("verified_here")
    if not checked:
        return "cited only"
    return checked.get("bound", "unknown")


def main():
    with open(STATUS, encoding="utf-8") as handle:
        data = json.load(handle)

    counts = data["counts"]
    print("ProofZero -- %d problems, %d open, %d solved"
          % (counts["problems"], counts["open"], counts["solved"]))
    print()

    rows = [("PROBLEM", "STATUS", "BOUND ACTUALLY CHECKED IN THIS REPO")]
    for entry in data["problems"]:
        rows.append((entry["title"][:30], entry["status"], local_bound(entry)[:58]))

    widths = [max(len(r[i]) for r in rows) for i in range(3)]
    for index, row in enumerate(rows):
        print("%-*s  %-*s  %s" % (widths[0], row[0], widths[1], row[1], row[2]))
        if index == 0:
            print("-" * (sum(widths) + 4))

    print()
    print("Larger published bounds are CITED in each note, not reproduced here.")
    print("No tool, and none coming: %s"
          % ", ".join(sorted(NO_TOOL)) + ", poincare (solved, needs no tool).")
    print("None of this resolves any open problem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
