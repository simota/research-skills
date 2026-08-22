#!/usr/bin/env python3
"""Check the claims the corpus makes about its own structure.

A `Verified:` date records that someone looked once; it cannot fail. These
checks are derived from the documents themselves, so an edit that breaks a
stated property breaks the build.

    make figures

Two checks today:

* every markdown table renders as a table. A paragraph inserted between rows
  splits it silently — the source reads fine and the reader gets pipe soup.
* the confidence composition table has the algebraic properties the page claims
  for it. A chain is composed pairwise, so associativity is not decoration:
  without it, `(a . b) . c` and `a . (b . c)` disagree and the answer depends on
  the order someone happened to combine the hops in. The ladder itself is read
  from the registry, and decay is checked against the page's opening sentence
  rather than against one hardcoded cell.
"""
import itertools
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEP = re.compile(r"^\|[\s:|-]+\|$")
failures: list[str] = []


def fail(where: str, msg: str) -> None:
    failures.append(f"  {where}: {msg}")


# --- every table row is inside a table -------------------------------------

def orphan_rows(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    out, in_table, fenced = [], False, False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("```"):
            fenced, in_table = not fenced, False
            continue
        if fenced:
            continue
        is_row = s.startswith("|") and s.endswith("|") and len(s) > 1
        if not is_row:
            if s == "" or not s.startswith("|"):
                in_table = False
            continue
        if SEP.match(s):
            in_table = True
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if SEP.match(nxt):          # a header row, followed by its separator
            continue
        if not in_table:
            out.append((i + 1, s[:70]))
    return out


def check_tables() -> int:
    n = 0
    for f in sorted(ROOT.rglob("*.md")):
        if ".git" in f.parts:
            continue
        n += 1
        for line, text in orphan_rows(f.read_text()):
            fail(f"{f.relative_to(ROOT)}:{line}",
                 f"row sits outside any table — {text}")
    return n


# --- the confidence composition table --------------------------------------

PAGE = ROOT / "skills/research-synthesize/reference/confidence-calibration.md"
# Weakest to strongest, from the registry rather than from a copy kept here: a
# checker holding its own vocabulary grades a renamed ladder against the old one.
LABELS = yaml.safe_load(
    (ROOT / "research-registry" / "harness.yaml").read_text(encoding="utf-8")
)["vocabulary"]["confidence_labels"]
RANK = {l: i for i, l in enumerate(LABELS)}
ABSORBING, FLOOR = LABELS[0], LABELS[1]              # Unknown settles nothing; Low is the floor
CELL = re.compile(r"`([A-Za-z]+)`")


def parse_composition() -> dict[tuple[str, str], str]:
    """Read the ∘ table out of the page rather than restating it here."""
    lines = PAGE.read_text().splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.strip().startswith("| ∘ ")), None)
    if start is None:
        fail("confidence-calibration.md", "no composition table found — the "
                                          "checker has stopped checking anything")
        return {}
    header = CELL.findall(lines[start])
    table: dict[tuple[str, str], str] = {}
    for raw in lines[start + 2:]:
        s = raw.strip()
        if not (s.startswith("|") and s.endswith("|")):
            break
        cells = CELL.findall(s)
        if len(cells) != len(header) + 1:
            fail("confidence-calibration.md",
                 f"row {s[:40]!r} has {len(cells)} labels, expected {len(header) + 1}")
            continue
        row, values = cells[0], cells[1:]
        for col, val in zip(header, values):
            table[(row, col)] = val
    return table


def check_composition() -> int:
    t = parse_composition()
    if not t:
        return 0
    missing = [(a, b) for a in LABELS for b in LABELS if (a, b) not in t]
    if missing:
        fail("composition", f"undefined pairs: {missing}")
        return len(t)
    bad = [v for v in t.values() if v not in RANK]
    if bad:
        fail("composition", f"cells naming labels outside the vocabulary: {sorted(set(bad))}")
        return len(t)

    def c(a: str, b: str) -> str:
        return t[(a, b)]

    for a, b in itertools.product(LABELS, repeat=2):
        if RANK[c(a, b)] > min(RANK[a], RANK[b]):
            fail("composition", f"{a} . {b} = {c(a, b)} is stronger than an input — "
                                "confidence rose along a chain")
    for a, b in itertools.product(LABELS, repeat=2):
        for weaker in LABELS:
            if RANK[weaker] <= RANK[a] and RANK[c(weaker, b)] > RANK[c(a, b)]:
                fail("composition", f"weakening {a} to {weaker} against {b} "
                                    f"raised the result to {c(weaker, b)}")
    for a, b, x in itertools.product(LABELS, repeat=3):
        if c(c(a, b), x) != c(a, c(b, x)):
            fail("composition", f"not associative: ({a}.{b}).{x} = {c(c(a, b), x)} "
                                f"but {a}.({b}.{x}) = {c(a, c(b, x))}")
    for a in LABELS:
        if c(ABSORBING, a) != ABSORBING or c(a, ABSORBING) != ABSORBING:
            fail("composition", f"{ABSORBING} does not absorb against {a}")

    # "Confidence falls along a chain and never holds" is the page's first line, and
    # "never rises" above does not say it: a table where High . High is High passes
    # every other property here and contradicts the sentence the page opens with.
    # It falls strictly, unless it is already resting on the floor.
    for a, b in itertools.product(LABELS, repeat=2):
        if ABSORBING in (a, b):
            continue
        weaker_input = a if RANK[a] <= RANK[b] else b
        if RANK[weaker_input] == RANK[FLOOR]:
            if c(a, b) != FLOOR:
                fail("composition", f"{a} . {b} = {c(a, b)}; {FLOOR} is the floor, so a "
                                    f"chain through it stays there")
        elif RANK[c(a, b)] >= RANK[weaker_input]:
            fail("composition", f"{a} . {b} = {c(a, b)}, which is no weaker than "
                                f"{weaker_input} — confidence held along a chain")
    return len(t)


def main() -> int:
    files = check_tables()
    cells = check_composition()
    if failures:
        print(f"{len(failures)} problem(s):")
        print("\n".join(failures[:20]))
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
        return 1
    print(f"figures green - {files} files scanned for split tables, "
          f"{cells} composition cells checked over {len(LABELS) ** 3} triples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
