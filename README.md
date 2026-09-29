<p align="center">
  <img src="assets/logo.svg" width="140" alt="ProofZero logo">
</p>

<h1 align="center">ProofZero</h1>

<p align="center">
  <b>Open collection of unsolved mathematical problems, conjectures, and research notes.</b><br>
  Personal project — free, open, no strings.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License"></a>
  <a href="problems/millennium-prize"><img src="https://img.shields.io/badge/problems-7-informational" alt="Problems"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-6%20open%20%2B%201%20solved-brightgreen" alt="Status"></a>
</p>

## Structure

| Path | Contents |
|---|---|
| `problems/millennium-prize/` | All 7 Clay Millennium Prize Problems (6 open, 1 solved) |
| `problems/classic-conjectures/` | Goldbach, Twin Prime, Collatz |
| `problems/nothing.md` | The one entry with no problem in it. Not counted below. |
| `problems/_template.md` | Template for adding new problems |
| `notes/` | Personal research notes |
| `tools/` | Scripts, helpers, utilities |
| `references/` | Papers, links, sources |

## Problems

### Millennium Prize (6 open, 1 solved)

| Problem | Status |
|---|---|
| Poincaré Conjecture | ✅ Solved (Perelman, 2003) |
| Riemann Hypothesis | 🔴 Open |
| P vs NP | 🔴 Open |
| Navier–Stokes | 🔴 Open |
| Yang–Mills Mass Gap | 🔴 Open |
| Birch–Swinnerton-Dyer | 🔴 Open |
| Hodge Conjecture | 🔴 Open |

### Classic Conjectures

| Problem | Year | Status |
|---|---|---|
| Goldbach Conjecture | 1742 (Euler letter to Goldbach) | 🔴 Open |
| Twin Prime Conjecture | 1849 (de Polignac) | 🔴 Open |
| Collatz Conjecture | 1937 (stated, unattributed origin) | 🔴 Open |

## What this repository is, and is not

This is a **notes repository**. It contains no proofs, no proof
assistant, and no verifier. Every note is written in three layers:

- what is **known**, with the primary source that establishes it;
- what a **tool here can actually check**, and the exact bound it checks;
- what remains **open**, stated as an open edge rather than a soft guess.

`tools/` holds small bounded computations that give **finite evidence**
for each problem. Their outputs are consistent with the conjecture over
the range they cover, and that is all they establish — a bounded search
cannot settle a general statement. Nothing in this repository resolves
any of the ten problems it describes, and no file here should be cited as
if it did. The counts above are ten: `problems/nothing.md` is an eleventh
entry in the folder and is not one of them.

Citations are given to primary sources where the claim is attributed, and
places where a result is conditional, partial, or frequently misreported
are marked as such.

## Adding a Problem

Copy `problems/_template.md` and fill in:
- Statement
- Status (open / solved / partial)
- Progress timeline
- Notes
- References

Then add a matching entry to `problems/_status.json` and run
`python tools/check_status.py`, which will tell you if the JSON and the note
disagree. The exhibit card and the JSON entry are mirrors of each other; the
checker exists to keep them from drifting.

## Running the tools

```bash
make verify    # run every finite check; non-zero exit on any regression
make status    # print the bound table from problems/_status.json
make help      # list targets
```

`make verify` is named for what it does: it confirms these tools still run and still
detect planted errors. It does not advance any conjecture, and it is not a scoreboard.
Four of the Millennium problems have no tool and never will have one here — that is a
permanent state, not a gap awaiting effort.

Please cite this repository as software, not as a result. See `CITATION.cff`.

Every problem note opens with an exhibit card giving what is known, what a
tool here checked at an exact bound, and what remains open. `nothing.md`
has no such card, on purpose, and a new entry without a real bound to
report should say so rather than invent one.

## License

MIT — see [LICENSE](LICENSE)
