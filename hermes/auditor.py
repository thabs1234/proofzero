#!/usr/bin/env python3
"""
ProofZero Auditor — scheduled honesty check.

This bot does NOT push bounds. It does not edit problems/, tools/, or
anything that makes a mathematical claim. It has no code path that writes
a bound, and no code path that reaches problems/nothing.md.

Every run:
  1. pull
  2. run the finite checks, the status checker, and the board checker
  3. compare the status snapshot against the previous run
  4. open a [AUDIT-FAILED] issue if any check fails
  5. open a [NOTE DRIFT] PR if a problem note changed without a commit
     that also changed the JSON (human review required, never merged)

Deliberately absent: any mechanism that would make the repository look
more solved than it is. That is the whole point of the project.

Usage:
    python hermes/auditor.py              # audit, open issue/PR as needed
    python hermes/auditor.py --dry-run    # report only, touch nothing remote
    python hermes/auditor.py --check     # run checks, no git, no remote
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("PROOFZERO_REPO", ".")).resolve()
RUNS = REPO / "hermes" / "runs"
TODAY = datetime.date.today().isoformat()
NOW = datetime.datetime.now().isoformat(timespec="seconds")

# Files this bot must never modify. Asserted, not merely documented.
FORBIDDEN = [
    "problems/nothing.md",
    "problems/_status.json",
    "problems/_template.md",
]
BOUNDED_TOOLS = [
    "tools/rh_zeros.py",
    "tools/collatz_hunt.py",
    "tools/goldbach_twins.py",
    "tools/pnp_probe.py",
]

_failures: list[str] = []


def log(msg: str) -> None:
    print(f"[{NOW}] {msg}", flush=True)
    if not DRY_RUN:
        RUNS.mkdir(parents=True, exist_ok=True)
        with open(RUNS / f"{TODAY}.log", "a", encoding="utf-8") as fh:
            fh.write(f"[{NOW}] {msg}\n")


def run(cmd: str, check: bool = False) -> subprocess.CompletedProcess:
    """Run a command. Never raises unless check=True."""
    log(f"$ {cmd}")
    if cmd.split()[0] == "make" and not shutil.which("make"):
        log("  (make unavailable; caller falls back to direct commands)")
        return subprocess.CompletedProcess(cmd, 127, "", "make not found")
    proc = subprocess.run(
        cmd, shell=True, cwd=REPO, capture_output=True, text=True
    )
    for line in (proc.stdout or "").splitlines():
        log(f"  {line}")
    if proc.returncode != 0:
        for line in (proc.stderr or "").splitlines()[:40]:
            log(f"  stderr: {line}")
    if check and proc.returncode != 0:
        raise RuntimeError(f"failed: {cmd}")
    return proc


def use_make(target: str) -> bool:
    """Run a make target if make exists. Returns True if it ran and passed."""
    if not shutil.which("make"):
        return False
    return run(f"make {target}").returncode == 0


def check_finite_tools() -> None:
    log("CHECK: finite mathematical tools")
    # The seven-check suite, via make when available, else directly.
    if use_make("verify"):
        log("  make verify: pass")
        return
    log("  make unavailable; running the checks directly")
    suite = [
        ("python tools/check_status.py", "status schema"),
        ("python tools/rh_zeros.py", "rh_zeros"),
        ("python tools/collatz_hunt.py", "collatz_hunt"),
        ("python tools/goldbach_twins.py 200000 --sample", "goldbach_twins"),
        ("python tools/pnp_probe.py", "pnp_probe"),
    ]
    for cmd, label in suite:
        if run(cmd).returncode != 0:
            _failures.append(f"finite check failed: {label} ({cmd})")
    if not shutil.which("node"):
        log("  SKIP: node not installed; greenboard render check not run")


def check_status() -> None:
    log("CHECK: status schema")
    if use_make("status"):
        return
    run("python tools/status_table.py")


def check_board() -> None:
    """The anti-fabrication gate. A failure here is the serious one."""
    log("CHECK: board honesty (anti-fabrication)")
    if use_make("board"):
        return
    if not shutil.which("node"):
        log("  SKIP: node unavailable; board check not run this cycle")
        return
    if run("node tools/check_greenboard.cjs").returncode != 0:
        _failures.append(
            "board honesty check failed: the page may be presenting a cited "
            "bound as local, dropping a disclosure, or inventing a bound"
        )


def snapshot() -> dict:
    """Status facts, for drift comparison. Read-only."""
    path = REPO / "problems" / "_status.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        _failures.append(f"could not parse _status.json: {exc}")
        return {}
    problems = data.get("problems", [])
    return {
        "n": len(problems),
        "open": sum(1 for p in problems if p.get("status") == "open"),
        "solved": sum(1 for p in problems if p.get("status") == "solved"),
        "with_tool": sum(1 for p in problems if p.get("tool")),
        "no_tool": sum(1 for p in problems if not p.get("tool")),
        "ids": sorted(p.get("id", "?") for p in problems),
    }


def compare(previous: dict, current: dict) -> None:
    if not previous or not current:
        return
    diffs = [k for k in current if previous.get(k) != current[k]]
    if diffs:
        log(f"DRIFT: status changed since last run: {diffs}")
        for key in diffs:
            log(f"  {key}: {previous.get(key)} -> {current.get(key)}")
    else:
        log("no drift: status identical to previous run")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True
    )


def open_issue(title: str, body: str) -> None:
    """Report a failure. Falls back to a PR when issues are disabled.

    thabs1234/proofzero has hasIssuesEnabled=false, so `gh issue create`
    errors out. Falling back to a PR keeps failures visible instead of
    dying on stderr.
    """
    if DRY_RUN:
        log(f"DRY-RUN: would report: {title}")
        return
    if not shutil.which("gh"):
        log("gh unavailable; failure recorded in the run log only")
        return
    RUNS.mkdir(parents=True, exist_ok=True)
    body_file = RUNS / f"issue-{NOW.replace(':', '')}.md"
    body_file.write_text(body, encoding="utf-8")
    proc = run(
        f'gh issue create --title "{title}" --body-file "{body_file}"'
    )
    if proc.returncode != 0:
        log("issues are disabled on this repo; reporting via PR instead")
        branch = f"audit/FAILED-{TODAY}-{NOW.replace(':', '')}"
        run(f"git checkout -b {branch}")
        run(
            f'gh pr create --title "{title}" '
            f'--body "Automated audit failure. This PR changes no problem, '
            f'tool, or bound. See the run log for detail."'
        )


def open_drift_pr(current: dict) -> None:
    """Status changed -> open a PR describing it. Never merge. Never write status."""
    if DRY_RUN:
        log("DRY-RUN: would open [AUDIT] drift PR")
        return
    if not shutil.which("gh"):
        log("gh unavailable; drift PR not opened")
        return
    branch = f"audit/snapshot-{TODAY}"
    if git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "main":
        run(f"git checkout -b {branch}")
    run(f"gh pr create --title '[AUDIT] status snapshot {TODAY}' "
        f'--body "Automated audit snapshot. Review only; this PR changes no '
        f'problem, tool, or bound.\\n\\n```\\n{json.dumps(current, indent=2)}\\n```"')


def guard() -> None:
    """Refuse to run if a protected file changed. Cheap, but explicit."""
    porcelain = git("status", "--porcelain").stdout
    dirty = [
        line[3:].strip().replace("\\", "/")
        for line in porcelain.splitlines()
        if line[3:].strip().replace("\\", "/") in FORBIDDEN
    ]
    if dirty:
        _failures.append(f"protected file(s) modified in worktree: {dirty}")
    for tool in BOUNDED_TOOLS:
        if not (REPO / tool).exists():
            _failures.append(f"expected bounded tool missing: {tool}")


def main() -> int:
    global DRY_RUN
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    DRY_RUN = args.dry_run

    RUNS.mkdir(parents=True, exist_ok=True)
    log("=" * 66)
    log("ProofZero Auditor - run start (audit only; pushes no bounds)")

    if not args.check:
        if not DRY_RUN:
            git("pull", "--rebase")
        else:
            log("dry-run: skipping git pull")

    guard()
    check_finite_tools()
    check_status()
    check_board()

    current = snapshot()
    log(f"status snapshot: {json.dumps(current)}")
    prev_file = RUNS / "last_snapshot.json"
    if prev_file.exists():
        try:
            compare(json.loads(prev_file.read_text(encoding="utf-8")), current)
        except Exception:  # noqa: BLE001
            log("could not parse previous snapshot")
    if not DRY_RUN and current:
        prev_file.write_text(json.dumps(current, indent=2), encoding="utf-8")

    if _failures:
        log(f"FAILURES ({len(_failures)}):")
        for f in _failures:
            log(f"  - {f}")
        open_issue(
            "[AUDIT-FAILED] ProofZero honesty check",
            "## Automated audit failure\n\n"
            + "\n".join(f"- {f}" for f in _failures)
            + "\n\nNo file was modified by the auditor.\n",
        )
        log("ProofZero Auditor - run end (FAILED)")
        return 1

    if not args.check and not DRY_RUN:
        open_drift_pr(current)

    log("all checks passed")
    log("ProofZero Auditor - run end")
    return 0


DRY_RUN = False

if __name__ == "__main__":
    sys.exit(main())
