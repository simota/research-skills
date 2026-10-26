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
  from the registry. Decay is the rule the page opens with ("falls along a chain
  and never holds") written as a check over every pair, not one hardcoded cell;
  the sentence itself is not parsed.
"""
import itertools
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
# A delimiter row as cmark-gfm reads one: each cell dashes, a colon at either
# end, the outer pipes optional but one pipe somewhere (without, `---` is a
# heading's underline). `| |` or `|:|` is a row of empty cells, not a separator.
SEP = re.compile(r"^(?=.*\|)\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?$")


def git_ignored(root: pathlib.Path) -> set[str]:
    """The top-level directories git ignores, as validate.py reads them."""
    names = [d.name for d in root.iterdir() if d.is_dir()]
    try:
        r = subprocess.run(["git", "check-ignore", "--stdin"], cwd=root, input="\n".join(names),
                           capture_output=True, text=True)
    except OSError:
        return set()
    return {n.rstrip("/") for n in r.stdout.splitlines()} & set(names)


# Not corpus: git's store, `.claude/`, where a worktree of this repo lives, and
# what git ignores at the top — a `.venv` holding pip's own markdown.
NOT_CORPUS = {".git", ".claude"}
IGNORED = git_ignored(ROOT)
failures: list[str] = []


def fail(where: str, msg: str) -> None:
    failures.append(f"  {where}: {msg}")


# --- every table row is inside a table -------------------------------------

# Whether a line opens a block depends on what is open above it, as CommonMark
# has it. After a blank line, any of these does: heading, quote, list item
# (empty, or any number), HTML comment, thematic break, indented code.
_BREAK = r"(-[ \t]*){3,}$|(\*[ \t]*){3,}$|(_[ \t]*){3,}$"
OPENS_BLOCK = re.compile(rf"( {{4}}|\t| {{0,3}}(#{{1,6}}(\s|$)|>|[-*+](\s|$)"
                         rf"|\d{{1,9}}[.)](\s|$)|<!--|{_BREAK}))")
# Inside a paragraph only these do: an empty item, a list starting at any
# number but 1, and indented code are more of the paragraph.
INTERRUPTS = re.compile(rf" {{0,3}}(#{{1,6}}(\s|$)|>|[-*+]\s+\S|1[.)]\s+\S|<!--|{_BREAK})")
# Inside a quote or list item's paragraph, any item starts a sibling.
SIBLING = re.compile(rf" {{0,3}}(#{{1,6}}(\s|$)|>|[-*+](\s|$)|\d{{1,9}}[.)](\s|$)|<!--|{_BREAK})")
# A quote: the lines that run on from it are its paragraph's, though written
# flush left, and never head a table. List items are followed by column.
CONTAINER = re.compile(r" {0,3}>")
# A list item's marker, and the spaces after it that set its content column.
ITEM = re.compile(r"( {0,3})([-*+]|\d{1,9}[.)])( +|$)")
# A code fence, backticks or tildes, closed only by a run of the same
# character at least as long.
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")
QUOTE = re.compile(r" {0,3}> ?")


def width(row: str) -> int:
    """Cells in a row, as GFM splits it: on every pipe no backslash precedes,
    inside a code span too. The pipes at either end are optional."""
    row = row[1:] if row.startswith("|") else row
    row = row[:-1] if re.search(r"(?<!\\)\|$", row) else row
    return len(re.split(r"(?<!\\)\|", row))


def is_row(s: str) -> bool:
    return s.startswith("|") and s.endswith("|") and len(s) > 1


def lead(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def step(state: str | None, raw: str) -> str | None:
    """What is open after `raw`: a paragraph a table can grow from ("para"), one
    no header can be read from ("lazy"), or nothing a table could grow from
    (None)."""
    if not raw.strip():
        return None
    # In a list, a sibling item starts even empty; only a paragraph of its own
    # holds an empty item off.
    opens = INTERRUPTS if state == "para" else OPENS_BLOCK if state is None else SIBLING
    if not opens.match(raw):
        return state or "para"
    # A quote line with nothing after its `>` closes the quote's paragraph, so
    # nothing below runs on from it and a table may start there.
    return "lazy" if CONTAINER.match(raw) and raw.lstrip(" >") \
        and not re.fullmatch(rf" {{0,3}}({_BREAK})", raw) else None


def heads(header: str, open_: str | None, sep: str) -> bool:
    """A paragraph's last line and the separator under it make a table only
    when the separator has one cell per header cell, pipes on the header or
    none: `Header` heads a one-column table, not a two-column one, and
    `| --- |` heads one too. A short separator, or one with no paragraph of
    its own above it, renders as text. A pipe after any backslash is escaped,
    as cmark-gfm splits cells (pandoc counts parity)."""
    return open_ == "para" and SEP.match(sep) is not None \
        and width(header.strip()) == width(sep)


def orphan_rows(text: str) -> list[tuple[int, str]]:
    """Every row GFM renders as text. A list item is followed by its content
    column, as CommonMark has it: a line indented to it is inside the item and
    is read from that column on, so a fence or a table inside a nested item is
    one; a line short of it closes the item, unless it runs on lazily from the
    item's paragraph, which keeps it text."""
    lines = [line.expandtabs(4) for line in text.splitlines()]
    return sorted(scan(lines)[0] + quoted_rows(lines))


def scan(lines: list[str]) -> tuple[list[tuple[int, str]], bool]:
    """The rows outside any table, and whether the page ends inside one."""
    out: list[tuple[int, str]] = []
    in_table, fence, state, prev = False, "", None, ""
    cols: list[int] = []      # content column of each open list item, outermost first
    depth = 0                 # how many items the open fence or table sits in
    empty = False             # the innermost item has had no content yet
    tried = False             # this paragraph has failed a delimiter row
    comment = False           # inside an HTML comment, which renders nothing
    # The quote's own text so far, read as a page of its own: only a paragraph
    # runs on lazily, so a line under a quoted table starts a block of its own.
    quote: list[str] = []
    qtab = False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s:
            k, empty = 0, False
            while k < len(cols) and lead(raw) >= cols[k]:
                k += 1
        else:
            # An item begins with at most one blank line: an empty one ends
            # here, unless the line is spaces out to its content column.
            if empty and not fence and lead(raw) < cols[-1]:
                cols.pop()
                empty = False
            k = len(cols)
        rel = raw[cols[k - 1]:] if s and k else raw
        if fence:
            if k >= depth:
                if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", rel):
                    fence = ""
                continue
            fence = ""                # its item closed, and the fence with it
        if comment:
            # An HTML block ends on the line holding `-->`, or when its item closes.
            if k >= depth:
                comment = "-->" not in rel
                continue
            comment = False
        if CONTAINER.match(rel):
            quote.append(QUOTE.sub("", rel, count=1))
            qtab = scan(quote)[1]
        else:
            quote, qtab = [], False
        if k < len(cols):
            # Short of the innermost item: a paragraph runs on lazily unless the
            # line starts a block of its own; anything else closes the item.
            if state in ("para", "lazy") and not in_table and not SIBLING.match(rel) \
                    and not FENCE.match(rel):
                if is_row(s):
                    out.append((i + 1, s[:70]))
                # cmark-gfm reads a lazy line flush left as a header, never one indented.
                state, prev = "para" if lead(raw) == 0 else "lazy", s
                continue
            del cols[k:]
            in_table, state = in_table and depth <= k, None
        if in_table:
            # A table runs on through a line without pipes, which GFM reads as
            # one more row; a blank line or another block's opening ends it.
            if s and not OPENS_BLOCK.match(rel) and not FENCE.match(rel):
                continue
            in_table, state = False, None
        m = ITEM.match(rel) if s else None
        if m and not re.fullmatch(rf" {{0,3}}({_BREAK})", rel) \
                and (state != "para" or INTERRUPTS.match(rel)):
            mark = (cols[k - 1] if k else 0) + len(m.group(1)) + len(m.group(2))
            spaces = len(m.group(3))
            # One space past the marker when the item is empty or starts with code.
            cols.append(mark + 1 if spaces > 4 or not raw[mark:].strip() else mark + spaces)
            rel, state = raw[cols[-1]:], None
            if not rel.strip():
                prev, empty, tried = "", True, False
                continue
        s2 = rel.strip()
        f = FENCE.match(rel)
        if f:
            fence, depth, state = f.group(1), len(cols), None
            continue
        if re.match(r" {0,3}<!--", rel):
            comment, depth, state = "-->" not in rel.split("<!--", 1)[1], len(cols), None
            prev = ""
            continue
        if state == "para" and re.fullmatch(r" {0,3}(-+|=+)[ \t]*", rel):
            state, prev, tried = None, s2, False     # a setext heading's underline
            continue
        if state is None and s2 and lead(rel) >= 4:
            continue                  # indented code
        if i and not tried and lead(rel) < 4 and heads(prev, state, s2):
            in_table, depth, state = True, len(cols), None
            if out and out[-1][0] == i:       # it was a header row after all
                out.pop()
            prev = s2
            continue
        if is_row(s):
            out.append((i + 1, s[:70]))
        # A paragraph that has failed one delimiter row never becomes a table;
        # a line indented four or more is not tried as one.
        tried = state in ("para", "lazy") and (
            tried or state == "para" and lead(rel) < 4 and SEP.match(s2) is not None)
        state = step(state, rel)
        if qtab and state == "lazy":
            state = None
        prev = s2
    return out, in_table


def quoted_rows(lines: list[str]) -> list[tuple[int, str]]:
    """Rows inside a quote, read as the quote's own text. `> | a |` never starts
    with a pipe, so a table split inside a callout was never looked at. Each run
    of quoted lines outside a fence is stripped of one `>` and read as a page of
    its own, which reaches a quote inside it too. A quote indented into a list
    item past three spaces is not followed."""
    out: list[tuple[int, str]] = []
    fence, run, start = "", [], 0
    for i, raw in enumerate(lines + [""]):
        m = None if fence else QUOTE.match(raw)
        if m:
            start = start if run else i
            run.append(raw[m.end():])
            continue
        if run:
            out += [(start + n, row) for n, row in orphan_rows("\n".join(run))]
            run = []
        if fence:
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*", raw):
                fence = ""
        elif f := FENCE.match(raw):
            fence = f.group(1)
    return out


def check_tables() -> int:
    n = 0
    for f in sorted(ROOT.rglob("*.md")):
        parts = f.relative_to(ROOT).parts
        if NOT_CORPUS & set(parts) or parts[0] in IGNORED:
            continue
        n += 1
        for line, text in orphan_rows(f.read_text(encoding="utf-8")):
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
    if not PAGE.exists():
        fail(str(PAGE.relative_to(ROOT)), "missing — the checker has stopped checking anything")
        return {}
    lines = PAGE.read_text(encoding="utf-8").splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.strip().startswith("| ∘ ")), None)
    if start is None:
        fail("confidence-calibration.md", "no composition table found — the "
                                          "checker has stopped checking anything")
        return {}
    header = CELL.findall(lines[start])
    if len(set(header)) != len(header):
        fail("confidence-calibration.md", f"header repeats a label: {header}")
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
        # A second row for the same label would silently win, while a reader
        # stops at the first one — the one this checker never saw.
        if any((row, col) in table for col in header):
            fail("confidence-calibration.md", f"row {row!r} appears more than once")
            continue
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
    # A row or column the ladder does not have is never put through a property
    # below, and the run reports its cells as checked.
    extra = sorted({x for k in t for x in k} - set(LABELS))
    if extra:
        fail("composition", f"rows or columns outside the vocabulary: {extra}")
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
            # In either argument: the table need not commute.
            if RANK[weaker] <= RANK[b] and RANK[c(a, weaker)] > RANK[c(a, b)]:
                fail("composition", f"weakening {b} to {weaker} after {a} "
                                    f"raised the result to {c(a, weaker)}")
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
