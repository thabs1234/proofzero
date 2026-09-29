#!/usr/bin/env python3
"""
Constitutional tests. These are the proof, not the claim.

Run:  python hermes/tests/test_constitution.py
Exit: 0 if every guard holds, 1 otherwise.

Two of these tests exist specifically because an earlier hand-written
constitution had those exact bugs:

  * `test_void_guard_holds_from_any_cwd` — a relative VOID_FILE let a write to
    ../problems/nothing.md through when the cwd was hermes/.
  * `test_frozen_rule_fires_on_real_ids` — hand-written ids ("bsd", "hodge")
    never matched the repo's real ones, so the frozen rule was dead code and
    the frozen problems were only stopped by the fallback pushable rule.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import constitution as C
from constitution import ConstitutionalViolation

PASS = 0
FAIL = 0


def check(name, fn, should_raise=False):
    global PASS, FAIL
    try:
        fn()
    except ConstitutionalViolation as exc:
        if should_raise:
            print(f"  PASS  {name}\n          refused: {exc}")
            globals()["PASS"] = PASS + 1
        else:
            print(f"  FAIL  {name}\n          unexpected refusal: {exc}")
            globals()["FAIL"] = FAIL + 1
        return
    except Exception as exc:  # noqa: BLE001
        print(f"  FAIL  {name}\n          unexpected {type(exc).__name__}: {exc}")
        globals()["FAIL"] = FAIL + 1
        return
    if should_raise:
        print(f"  FAIL  {name}\n          expected a refusal, got none")
        globals()["FAIL"] = FAIL + 1
    else:
        print(f"  PASS  {name}")
        globals()["PASS"] = PASS + 1


print("ProofZero constitutional tests")
print("=" * 72)

# --- The real ids, read from the repo rather than retyped --------------------
problems = C.load_problems()
REAL_IDS = [p["id"] for p in problems]
REAL_FROZEN = [p["id"] for p in problems
               if p.get("status") == "open" and p.get("tool") is None]
REAL_SOLVED = [p["id"] for p in problems if p.get("status") == "solved"]
REAL_PUSHABLE = [p["id"] for p in problems
                 if p.get("status") == "open" and p.get("tool")]

print(f"\nRepo classification (read from problems/_status.json)")
print(f"  frozen   ({len(REAL_FROZEN)}): {REAL_FROZEN}")
print(f"  pushable ({len(REAL_PUSHABLE)}): {REAL_PUSHABLE}")
print(f"  solved   ({len(REAL_SOLVED)}): {REAL_SOLVED}")

# --- 1. Invariants agree with the canonical file -----------------------------
print("\n[1] derived sets agree with the declared sets")
check("assert_invariants_hold() passes on the real repo",
      C.assert_invariants_hold)

# --- 2. THE REAL-ID TEST: the frozen rule must actually fire -----------------
print("\n[2] the frozen rule fires on the repo's REAL frozen ids")
for pid in REAL_FROZEN:
    def frozen(pid=pid):
        try:
            C.assert_not_frozen(pid)
        except ConstitutionalViolation as e:
            # Must be the FROZEN rule, not the generic pushable fallback.
            if "FROZEN PROBLEM" not in str(e):
                raise ConstitutionalViolation(
                    f"refused, but by the wrong rule: {e}"
                ) from None
            raise
    check(f"assert_not_frozen('{pid}') refuses via the FROZEN rule", frozen,
          should_raise=True)

# --- 3. The cwd test: the void guard must not depend on where you run from --
print("\n[3] the void guard holds from ANY working directory")
for label, path, cwd in (
    ("relative, from repo root", "problems/nothing.md", C.REPO_ROOT),
    ("dot-relative, from repo root", "./problems/nothing.md", C.REPO_ROOT),
    ("parent-relative, from hermes/", "../problems/nothing.md", C.REPO_ROOT / "hermes"),
    ("bare, from problems/", "nothing.md", C.REPO_ROOT / "problems"),
    ("absolute", str(C.VOID_FILE), C.REPO_ROOT),
    ("absolute, from /", str(C.VOID_FILE), Path(C.REPO_ROOT.anchor)),
):
    def cwd_case(path=path, cwd=cwd):
        orig = os.getcwd()
        os.chdir(cwd)
        try:
            C.assert_void_untouched(Path(path))
        finally:
            os.chdir(orig)
    check(f"refused: {label} — path={path}", cwd_case, should_raise=True)

# Precision: a same-named file that is NOT the repo's void must be allowed.
# From the repo root, ../problems/nothing.md is C:/Users/<user>/problems/nothing.md.
# Refusing that would be a guard that blocks innocent writes, not a guard.
def not_the_void():
    orig = os.getcwd()
    os.chdir(C.REPO_ROOT)
    try:
        target = (C.REPO_ROOT / ".." / "problems" / "nothing.md").resolve()
        if target == C.VOID_FILE.resolve():
            raise ConstitutionalViolation("test setup is degenerate")
        C.assert_void_untouched(Path("../problems/nothing.md"))
    finally:
        os.chdir(orig)
check("ALLOWED: a same-named file outside the repo is not the void", not_the_void)

check("ordinary write to a non-void path is ALLOWED",
      lambda: C.assert_void_untouched(Path("problems/_status.json")))
check("write outside the repo is ALLOWED",
      lambda: C.assert_void_untouched(Path("/tmp/anything.txt")))

# --- 4. Pushable bounds are permitted ---------------------------------------
print("\n[4] real pushable problems may be pushed")
for pid in REAL_PUSHABLE:
    check(f"assert_pushable('{pid}') allows",
          lambda p=pid: C.assert_pushable(p))

# --- 5. Solved, frozen, and unknown ids are all refused ---------------------
print("\n[5] non-pushable ids are refused")
for pid in REAL_SOLVED:
    check(f"assert_pushable('{pid}') refuses (solved)",
          lambda p=pid: C.assert_pushable(p), should_raise=True)
check("assert_pushable('hodge') — the old WRONG id — is still refused",
      lambda: C.assert_pushable("hodge"), should_raise=True)
check("assert_pushable('bsd') — the old WRONG id — is still refused",
      lambda: C.assert_pushable("bsd"), should_raise=True)
check("assert_pushable('made-up-problem') refuses",
      lambda: C.assert_pushable("made-up-problem"), should_raise=True)
check("assert_known_id('made-up-problem') refuses",
      lambda: C.assert_known_id("made-up-problem"), should_raise=True)
check("assert_known_id('hodge-conjecture') allows the real id",
      lambda: C.assert_known_id("hodge-conjecture"))

# --- 6. A dirty ladder halts before any tool runs ---------------------------
print("\n[6] a ladder containing a real frozen problem halts")
def dirty_ladder(pid):
    def fn():
        try:
            C.assert_not_frozen(pid)
        except ConstitutionalViolation as e:
            if "FROZEN PROBLEM" not in str(e):
                raise ConstitutionalViolation(f"wrong rule: {e}") from None
            raise
    return fn
for pid in REAL_FROZEN:
    check(f"ladder entry '{{\"id\": \"{pid}\"}}' halts via the frozen rule",
          dirty_ladder(pid), should_raise=True)

# --- 7. Status fields are protected from automation -------------------------
print("\n[7] mathematical status fields are protected")
for field in ("status", "verified_here", "verified_elsewhere", "open_edge",
              "tool", "source", "solved_on"):
    check(f"assert_no_status_mutation('{field}') refuses",
          lambda f=field: C.assert_no_status_mutation(f), should_raise=True)
check("a non-status field is allowed",
      lambda: C.assert_no_status_mutation("note"))

# --- 8. Drift detection: edit the canonical file, guards must notice --------
print("\n[8] drift between _status.json and the constitution is detected")
def drift_test(label, mutate, guard):
    """Copy the repo status file, apply a mutation, and assert a guard fires."""
    data = json.loads(C.STATUS_FILE.read_text(encoding="utf-8"))
    mutate(data)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as fh:
        json.dump(data, fh)
        tmp = fh.name
    orig = C.STATUS_FILE
    try:
        C.STATUS_FILE = Path(tmp)
        guard()
    except ConstitutionalViolation:
        print(f"  PASS  {label}")
        globals()["PASS"] = PASS + 1
    except Exception as exc:  # noqa: BLE001
        print(f"  FAIL  {label}  ({type(exc).__name__}: {exc})")
        globals()["FAIL"] = FAIL + 1
    else:
        print(f"  FAIL  {label}  (drift went undetected)")
        globals()["FAIL"] = FAIL + 1
    finally:
        C.STATUS_FILE = orig
        os.unlink(tmp)

def give_hodge_a_tool(d):
    for p in d["problems"]:
        if p["id"] == "hodge-conjecture":
            p["tool"] = "tools/hodge/verify.py"
drift_test("hodge gaining a tool in _status.json is caught",
           give_hodge_a_tool, C.assert_invariants_hold)

def flip_poincare_to_open(d):
    for p in d["problems"]:
        if p["id"] == "poincare-conjecture":
            p["status"] = "open"
drift_test("poincare being marked open is caught",
           flip_poincare_to_open, C.assert_invariants_hold)

def add_unknown_toolless(d):
    d["problems"].append({
        "id": "brand-new-open-problem", "title": "New", "status": "open",
        "tool": None, "verified_here": None, "verified_elsewhere": None,
        "open_edge": "x", "file": "problems/x.md",
    })
drift_test("an undeclared new tool-less open problem is caught",
           add_unknown_toolless, C.assert_invariants_hold)

def strip_collatz_tool(d):
    for p in d["problems"]:
        if p["id"] == "collatz":
            p["tool"] = None
drift_test("collatz losing its tool is caught",
           strip_collatz_tool, C.assert_invariants_hold)

# --- 9. VOID_FILE must be absolute, not a cwd-relative literal --------------
# This is the ROOT of the original bypass, and it is checked directly. When
# VOID_FILE was relative, the absolute-path cases still "passed" vacuously:
# comparing two relative paths matches regardless of where you run, which is
# exactly why the bug survived. Pinning absoluteness catches it at the source.
print("\n[9] VOID_FILE is anchored to the repo root, not the cwd")
check("VOID_FILE.is_absolute()",
      lambda: None if C.VOID_FILE.is_absolute() else
      (_ for _ in ()).throw(AssertionError(
          "VOID_FILE is relative — resolves against cwd, which is the bypass")))
check("VOID_FILE is inside REPO_ROOT",
      lambda: None if C.VOID_FILE.is_relative_to(C.REPO_ROOT) else
      (_ for _ in ()).throw(AssertionError("VOID_FILE is outside the repo")))
check("STATUS_FILE.is_absolute()",
      lambda: None if C.STATUS_FILE.is_absolute() else
      (_ for _ in ()).throw(AssertionError("STATUS_FILE is relative")))
check("VOID_FILE points at problems/nothing.md",
      lambda: None if C.VOID_FILE.name == "nothing.md"
      and C.VOID_FILE.parent.name == "problems" else
      (_ for _ in ()).throw(AssertionError(f"unexpected {C.VOID_FILE}")))

# --- 10. The void file must still exist --------------------------------------
print("\n[10] repo state")
check("problems/nothing.md exists", lambda: None
      if C.VOID_FILE.is_file() else (_ for _ in ()).throw(AssertionError("missing")))
print(f"  INFO  void file: {C.VOID_FILE}")
print(f"  INFO  repo root: {C.REPO_ROOT}")
print(f"  INFO  status:    {C.STATUS_FILE}")

print("\n" + "=" * 72)
print(f"PASS: {PASS}   FAIL: {FAIL}")
sys.exit(0 if FAIL == 0 else 1)
