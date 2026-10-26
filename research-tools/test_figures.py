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


def mutated(mutate) -> tuple[int, str]:
    """figures_check on a throwaway copy with one edit made."""
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "repo"
        shutil.copytree(ROOT, copy, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
        mutate(copy)
        return run(copy)


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def five_labels(r: Path) -> None:
    """With strict decay every four-label pair but `High . High` is forced, so no
    four-label table breaks monotonicity without first breaking decay. A fifth
    label leaves room: this table passes every other property, and weakening
    its second argument raises the result."""
    sub(r / "research-registry/harness.yaml", "confidence_labels: [Unknown, Low, Medium, High]",
        "confidence_labels: [Unknown, Low, Medium, High, VeryHigh]")
    p = r / PAGE
    t = p.read_text(encoding="utf-8")
    start = t.index("| ∘ |")
    end = t.index("\n\n", start)
    rows = ["| ∘ | `VeryHigh` | `High` | `Medium` | `Low` | `Unknown` |", "|---|---|---|---|---|---|",
            "| `VeryHigh` | `Low` | `Medium` | `Low` | `Low` | `Unknown` |"]
    rows += [f"| `{x}` | `Low` | `Low` | `Low` | `Low` | `Unknown` |" for x in ("High", "Medium", "Low")]
    rows += ["| `Unknown` |" + " `Unknown` |" * 5]
    p.write_text(t[:start] + "\n".join(rows) + t[end:], encoding="utf-8")


# name -> (mutation, text the failure must contain).
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
    # A line of text heads a table too, but only one of the separator's width.
    "text-header-short": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                        "<!-- research:guidance -->\n",
                                        "<!-- research:guidance -->\n\nHeader\n|---|---|\n| a | b |\n"),
                          "row sits outside any table"),
    # An HTML comment, as the delivery markers are, ends a table: a row after
    # it is a paragraph, though a line of text there would be one more row.
    "comment-ends-table": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                         "<!-- research:guidance -->\n",
                                         "<!-- research:guidance -->\n\n| a |\n|---|\n"
                                         "<!-- note -->\n| lonely |\n"),
                           "row sits outside any table"),
    # A tilde fence ends a table as a backtick one does, and what follows its
    # close is no row of it.
    "tilde-fence-ends-table": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                             "<!-- research:guidance -->\n",
                                             "<!-- research:guidance -->\n\n| a |\n|---|\n"
                                             "~~~\ncode\n~~~\n| lonely |\n"),
                               "row sits outside any table"),
    # A list item's later paragraph runs on lazily into a table glued under it
    # flush left: pipe soup inside the item, never a table.
    "item-later-paragraph": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                           "<!-- research:guidance -->\n",
                                           "<!-- research:guidance -->\n\n1. Step one\n\n"
                                           "   Details here.\n| a | b |\n|---|---|\n"),
                             "row sits outside any table"),
    # A paragraph that failed one delimiter row never becomes a table.
    "failed-delimiter": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                       "<!-- research:guidance -->\n",
                                       "<!-- research:guidance -->\n\nSome text.\n"
                                       "|---|---|\n|---|---|\n"),
                         "row sits outside any table"),
    # Indented four or more, a delimiter row is one more line of the paragraph.
    "indented-delimiter": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                         "<!-- research:guidance -->\n",
                                         "<!-- research:guidance -->\n\n| a | b |\n"
                                         "     |---|---|\n"),
                           "row sits outside any table"),
    # A line short of an item's column closes the item and the fence in it.
    "after-item-fence": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                       "<!-- research:guidance -->\n",
                                       "<!-- research:guidance -->\n\n- a\n  ```\n  x\n| a |\n"),
                         "row sits outside any table"),
    # Inside a quote a row starts with `>`, and was never read as a row at all.
    "split-table-in-quote": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                           "<!-- research:guidance -->\n",
                                           "<!-- research:guidance -->\n\n> | a | b |\n> |---|---|\n"
                                           "> | 1 | 2 |\n>\n> | lonely | row |\n"),
                             "row sits outside any table — | lonely | row |"),
    # A comment ends on the line holding `-->`; a row after it is text again.
    "row-after-comment": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                        "<!-- research:guidance -->\n",
                                        "<!-- research:guidance -->\n\n<!-- held back:\n"
                                        "| a | b |\n-->\n| lonely | row |\n"),
                          "row sits outside any table — | lonely | row |"),
    # A comment opened in a list item closes with it, and leaves the row as text.
    "comment-closes-with-item": (lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                               "<!-- research:guidance -->\n",
                                               "<!-- research:guidance -->\n\n- item\n"
                                               "  <!-- x\n| lonely | row |\n  -->\n"),
                                 "row sits outside any table — | lonely | row |"),
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
    # A row the ladder does not have was counted as checked and checked by nothing.
    "label-outside-ladder": (lambda r: sub(r / PAGE, "| `Unknown` | `Unknown` | `Unknown` | `Unknown` | `Unknown` |",
                                           "| `Unknown` | `Unknown` | `Unknown` | `Unknown` | `Unknown` |\n"
                                           "| `Certain` | `High` | `High` | `High` | `High` |"),
                             "rows or columns outside the vocabulary: ['Certain']"),
    "second-argument": (five_labels, "weakening VeryHigh to High after VeryHigh"),
}


# Edits that must stay green: a check that fires on a table GitHub renders is
# as wrong as one silent on a table it does not.
HARMLESS = {
    # cmark-gfm makes this a one-column table whose header cell reads `---`.
    "hyphen-header": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                   "<!-- research:guidance -->\n",
                                   "<!-- research:guidance -->\n\n| --- |\n| --- |\n| x |\n"),
    # And this one whose header is a line of text: GFM needs no pipes on it.
    "text-header": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                 "<!-- research:guidance -->\n",
                                 "<!-- research:guidance -->\n\nOne column\n|---|\n| x |\n"),
    # Text that only looks like a block opener is one more row of the table.
    "not-a-heading": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                   "<!-- research:guidance -->\n",
                                   "<!-- research:guidance -->\n\n| a |\n|---|\n#tag\n"
                                   "####### x\n-*-\n| b |\n"),
    # A fence inside a nested item sits past four spaces, and is still a fence.
    "fence-in-nested-item": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                          "<!-- research:guidance -->\n",
                                          "<!-- research:guidance -->\n\n- a\n  - b\n\n"
                                          "    ```text\n    | x | y |\n    ```\n"),
    # Read from the item's column on, the row on its marker's line heads a table.
    "table-in-item": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                   "<!-- research:guidance -->\n",
                                   "<!-- research:guidance -->\n\n- | a | b |\n  |---|---|\n"),
    # GFM's delimiter row needs no outer pipes.
    "pipeless-delimiter": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                        "<!-- research:guidance -->\n",
                                        "<!-- research:guidance -->\n\na | b\n--- | ---\n"
                                        "| c | d |\n"),
    # Rows in indented code are code.
    "indented-code": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                   "<!-- research:guidance -->\n",
                                   "<!-- research:guidance -->\n\nText.\n\n    | a | b |\n"),
    # A bare `>` closes the quote's paragraph: the table below it is one.
    "table-after-quote": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                       "<!-- research:guidance -->\n",
                                       "<!-- research:guidance -->\n\n> Note.\n>\n| a | b |\n"
                                       "|---|---|\n| 1 | 2 |\n"),
    # A table inside a quote is a table, and a fenced quote is code.
    "table-in-quote": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                    "<!-- research:guidance -->\n",
                                    "<!-- research:guidance -->\n\n> | a | b |\n> |---|---|\n"
                                    "> | 1 | 2 |\n\n```\n> | lonely |\n```\n"),
    # Rows inside a multi-line HTML comment are not drawn at all.
    "rows-in-comment": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                     "<!-- research:guidance -->\n",
                                     "<!-- research:guidance -->\n\nText.\n<!-- held back:\n"
                                     "| P3 trade press | one-hop |\n-->\n"),
    # A table is no paragraph, so nothing runs on lazily from a quoted one: the
    # table under it is a table of its own.
    "table-under-quoted-table": lambda r: sub(r / "skills/research-source/playbooks/traps.md",
                                              "<!-- research:guidance -->\n",
                                              "<!-- research:guidance -->\n\n> | a | b |\n"
                                              "> |---|---|\n> | 1 | 2 |\n| c | d |\n"
                                              "|---|---|\n| 3 | 4 |\n"),
}


def main() -> int:
    code, out = run(ROOT)
    if code != 0:
        print("figures_check already fails on the working tree; fix that first:\n" + out)
        return 1
    silent = []
    for name, (mutate, says) in CASES.items():
        code, out = mutated(mutate)
        if code == 0 or says not in out:
            silent.append(name)
            print(f"  {name} did not fire saying {says!r}\n{out}")
    flagged = []
    for name, mutate in HARMLESS.items():
        code, out = mutated(mutate)
        if code != 0:
            flagged.append(name)
            print(f"  harmless edit {name} was flagged\n{out}")
    print(f"{len(CASES)} figure checks exercised, {len(silent)} silent · "
          f"{len(HARMLESS)} harmless edits, {len(flagged)} flagged")
    return 1 if silent or flagged else 0


if __name__ == "__main__":
    sys.exit(main())
