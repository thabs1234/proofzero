# ProofZero -- bounded verification runner
#
#   make verify    run every finite check in this repository
#   make status    print the bound table from problems/_status.json
#   make lint      syntax-lint the tools (advisory)
#   make help      list targets
#
# This target is named "verify", not "green", on purpose. Nothing here
# advances any of the ten problems. These are regression checks on small
# bounds; four of the Millennium problems have no tool at all, and that is
# a permanent state rather than a gap awaiting effort. A "green" target
# would imply a colour that means "solved", and nothing here is solved.
#
# Exit status is non-zero if any check fails. Timings are printed for
# information only and are never a pass/fail criterion.

PYTHON ?= python
TOOLS  := tools

.PHONY: verify status board lint help

help:
	@echo "ProofZero -- bounded verification"
	@echo ""
	@echo "  make verify   run all finite checks (non-zero exit on failure)"
	@echo "  make status   print the bound table from problems/_status.json"
	@echo "  make board    check that greenboard.html renders honestly"
	@echo "  make lint     syntax-lint tools/ (advisory)"
	@echo ""
	@echo "None of this resolves any of the ten open problems."

verify:
	@fail=0; \
	run() { \
		printf '\n=== %s\n' "$$1"; \
		$(PYTHON) $$2 || { printf '  FAILED (exit %s)\n' "$$?"; fail=$$((fail+1)); }; \
	}; \
	run "Riemann: first 20 zeros, worst deviation from Re(s)=1/2" "$(TOOLS)/rh_zeros.py 20"; \
	run "Riemann negative control: planted off-line zero must be detected" "$(TOOLS)/_control_rh.py"; \
	run "P vs NP: 400 random 3-SAT instances, DPLL vs brute force" "$(TOOLS)/pnp_probe.py --self-check"; \
	run "Collatz: 200000 starting values, counterexample search" "$(TOOLS)/collatz_hunt.py 200000 --top 1"; \
	run "Goldbach: every even n <= 20000, cross-checked" "$(TOOLS)/goldbach_twins.py 20000 --sample"; \
	run "Twin primes: all pairs (p, p+2) up to 200000" "$(TOOLS)/goldbach_twins.py 200000 --sample"; \
	run "P vs NP: verification/search asymmetry at n=20, m=85" "$(TOOLS)/pnp_probe.py 15 4.26"; \
	printf '\n'; \
	if [ "$$fail" -ne 0 ]; then \
		printf 'VERIFY FAILED: %d check(s) did not pass\n' "$$fail"; \
		printf 'A failure here means a tool regressed or stopped detecting a\n'; \
		printf 'planted error. It says nothing about the ten open problems.\n'; \
		exit 1; \
	fi; \
	printf 'All checks passed.\n'; \
	printf 'What that establishes: these tools still work, and still detect\n'; \
	printf 'known-bad input. What it does not establish: any conjecture.\n'

status:
	@$(PYTHON) $(TOOLS)/status_table.py

# Checks that greenboard.html still renders honestly from _status.json.
# Uses .cjs so a parent-directory package.json cannot switch it to ESM.
# If node is unavailable this skips loudly rather than silently passing.
board:
	@if command -v node >/dev/null 2>&1; then \
		node $(TOOLS)/check_greenboard.cjs; \
	else \
		echo "SKIP: node not installed; greenboard render check not run"; \
	fi

lint:
	@$(PYTHON) -m flake8 $(TOOLS) --count --select=E9,F63,F7,F82 --show-source --statistics \
		|| echo "flake8 not installed; skipping (advisory only)"
