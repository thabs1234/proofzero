# ProofZero Auditor

A scheduled **honesty check** for this repository. It runs the finite tools,
the status schema check, and the board anti-fabrication check, and reports
what it finds.

## What it does NOT do

This is the important part.

- It does not push bounds. It never writes a bound into `_status.json`.
- It never edits a problem note, a tool, or a bound.
- It never merges anything, and never pushes to `main`.
- It has no code path that reaches `problems/nothing.md`.
- It never claims a problem is solved.

There is deliberately no ladder of "next targets" and no bound-increment step.
A bot that moved bounds every six hours would fill this repository with numbers
nobody had reason to defend, and the whole point of ProofZero is that every
number in it is defensible. Four of the ten problems have no tool and never
will; that absence is a property, not a gap.

## Running it

```bash
python hermes/auditor.py --check      # checks only, no git, no remote writes
python hermes/auditor.py --dry-run    # full run, but opens nothing
python hermes/auditor.py              # full run; may open a PR on failure
```

`--check` is the safe default and is what CI runs.

`make` is used when available and falls back to the underlying commands when it
is not, so the auditor runs on a bare Python install.

## What counts as a failure

- any finite tool exits non-zero
- `tools/check_status.py` rejects the status schema
- `tools/check_greenboard.cjs` finds a lie in the page
- a bounded tool goes missing
- a protected file is modified in the worktree

## Reporting

Failures are reported with `gh issue create`. **This repository has issues
disabled**, so the auditor falls back to opening a PR describing the failure.
That PR changes no problem, tool, or bound. A human decides what happens.

## Schedule

`.github/workflows/auditor.yml` runs `--check` daily at 02:17 UTC. It is
read-only (`permissions: contents: read`) and cannot write to the repository
even if the script were changed to try.

To disable:

```bash
gh workflow disable auditor.yml
```

## Run logs

`hermes/runs/YYYY-MM-DD.log`, plus `last_snapshot.json` for drift comparison
between runs. Logs are ignored by git; CI uploads them as artifacts.
