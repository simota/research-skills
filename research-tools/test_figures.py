#!/usr/bin/env python3
"""Prove each check in figures_check.py fires.

The same discipline test_validate.py holds the validator to: a check only ever
seen passing may be checking nothing. Each case breaks one property in a
throwaway copy and expects figures_check to say so; the baseline must pass.

Run: make test
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = "skills/research-synthesize/reference/confidence-calibration.md"
ROW_HIGH = "| `High` | `Medium` | `Low` | `Low` | `Unknown` |"


def run(root: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(root / "research-tools" / "figures_check.py")],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


# name -> (mutation, text the failure must contain). Monotonicity has no case of
# its own: with strict decay every pair but `High . High` is forced to `Low`, so
# no four-label table breaks monotonicity without first breaking decay.
CASES = {
    "split-table": (lambda r: sub(r / "skills/_research/CONTRACT.md",
                                  "| `Low` | Directionally", "\nA sentence.\n| `Low` | Directionally"),
                    "row sits outside any table"),
    "blank-separator": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                      "<!-- research:guidance -->\n",
                                      "<!-- research:guidance -->\n|   |   |\n| lonely | row |\n"),
                        "row sits outside any table"),
    # GFM makes a table only of a header row whose cells the separator matches
    # one for one; anything else is a paragraph of pipes.
    "separator-short": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                      "<!-- research:guidance -->\n",
                                      "<!-- research:guidance -->\n\n| a | b |\n|---|\n| 1 | 2 |\n"),
                        "row sits outside any table"),
    "no-header": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                "<!-- research:guidance -->\n",
                                "<!-- research:guidance -->\n\n|---|---|\n| 1 | 2 |\n"),
                  "row sits outside any table"),
    "no-header-one-column": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                           "<!-- research:guidance -->\n",
                                           "<!-- research:guidance -->\n\n|---|\n| 1 |\n"),
                             "row sits outside any table"),
    "rises": (lambda r: sub(r / PAGE, ROW_HIGH, "| `High` | `High` | `Low` | `Low` | `Unknown` |"),
              "confidence held along a chain"),
    "unknown-leaks": (lambda r: sub(r / PAGE, ROW_HIGH, "| `High` | `Medium` | `Low` | `Low` | `Low` |"),
                      "Unknown does not absorb"),
    "missing-pair": (lambda r: sub(r / PAGE, ROW_HIGH + "\n", ""), "undefined pairs"),
    "no-table": (lambda r: sub(r / PAGE, "| ∘ |", "| o |"), "no composition table found"),
    "duplicate-row": (lambda r: sub(r / PAGE, ROW_HIGH, "| `High` | `High` | `High` | `High` | `High` |\n"
                                    + ROW_HIGH), "row 'High' appears more than once"),
    "duplicate-header": (lambda r: sub(r / PAGE, "| ∘ | `High` | `Medium` |", "| ∘ | `High` | `High` |"),
                         "header repeats a label"),
    "missing-page": (lambda r: (r / PAGE).unlink(), "missing — the checker has stopped"),
}


def main() -> int:
    code, out = run(ROOT)
    if code != 0:
        print("figures_check already fails on the working tree; fix that first:\n" + out)
        return 1
    silent = []
    for name, (mutate, says) in CASES.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
            mutate(copy)
            code, out = run(copy)
        if code == 0 or says not in out:
            silent.append(name)
            print(f"  {name} did not fire saying {says!r}\n{out}")
    print(f"{len(CASES)} figure checks exercised, {len(silent)} silent")
    return 1 if silent else 0


if __name__ == "__main__":
    sys.exit(main())
