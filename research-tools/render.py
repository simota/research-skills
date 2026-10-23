#!/usr/bin/env python3
"""Write the delivered blocks back into every SKILL.md.

A contract kept only in the shared directory is not read on most launches, so the operative
part is carried verbatim in each skill. That only stays true if changing one
line does not cost six hand edits — this is that cost, paid once.

Idempotent: run it, commit the diff. A file it cannot render safely is refused, left
as it was, and the run exits non-zero.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "research-registry" / "harness.yaml").read_text(encoding="utf-8"))
PREFIX = H["prefix"]
SKILLS_ROOT = ROOT / H["skills_dir"] if H.get("skills_dir") else ROOT


def render(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for key, spec in H["delivered"].items():
        only = spec.get("only")
        if only not in (None, "signature"):
            raise ValueError(f"unknown delivery scope {only!r} for {key}")
        if only == "signature" and path.parent.name not in H["signature"]["required_of"]:
            # Only whole blocks are removed, so the markers must pair up in order
            # first: a stray open marker above a block made the removal run from
            # it to the block's close and take the prose between them. A lone
            # marker is no block to remove, and V17 refuses it all the same.
            marks = re.findall(rf"<!-- (/?)deliver:{key} -->", text)
            if marks != ["", "/"] * (len(marks) // 2):
                raise ValueError(f"{path.parent.name}/SKILL.md has an unmatched {key} marker "
                                 "outside its scope; repair or remove it, then render")
            text = re.sub(rf"<!-- deliver:{key} -->.*?<!-- /deliver:{key} -->\n?",
                          "", text, flags=re.S)
            continue
        # Blank lines are stripped at both ends, as V17 compares them: a leading
        # one otherwise rendered a block V17 could never accept.
        block = (ROOT / "research-registry" / "delivered" / f"{key}.md").read_text(
            encoding="utf-8").strip("\n")
        open_m, close_m = f"<!-- deliver:{key} -->", f"<!-- /deliver:{key} -->"
        payload = f"{open_m}\n{block}\n{close_m}"
        # Rewriting the first copy and leaving a second untouched would report
        # a clean render over a stale block. Which one is meant is a person's call.
        if text.count(open_m) > 1 or text.count(close_m) > 1:
            raise ValueError(f"{path.parent.name}/SKILL.md carries the {key} block "
                             "more than once; remove the extra copy, then render")
        # One marker without the other, or the two reversed, would send this to
        # the insert branch and leave the old body behind as unmarked text.
        if (open_m in text) != (close_m in text) or \
                (open_m in text and text.index(close_m) < text.index(open_m)):
            raise ValueError(f"{path.parent.name}/SKILL.md has an unmatched {key} marker; "
                             "repair or remove it, then render")
        if open_m in text:
            head, rest = text.split(open_m, 1)
            _, tail = rest.split(close_m, 1)
            text = head + payload + tail
        else:
            m = re.search(rf"^## {re.escape(spec['section'])}[ \t]*\n", text, re.M)
            if not m:
                raise ValueError(f"{path.parent.name}/SKILL.md has no section "
                                 f"{spec['section']!r} to carry the {key} block")
            heading = m.group(0)
            head, rest = text[:m.start()], text[m.end():]
            # append at the end of that section, before the next heading. Matched
            # at a line start, so an empty section — its heading straight after
            # this one — ends here rather than at the heading after that.
            nxt = re.search(r"^## ", rest, re.M)
            body, tail = (rest[:nxt.start()], "\n" + rest[nxt.start():]) if nxt else (rest, "")
            text = head + heading + body.rstrip("\n") + "\n" + payload + "\n" + tail
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed, refused = [], []
    for d in sorted(SKILLS_ROOT.glob(f"{PREFIX}*")):
        if not (d / "SKILL.md").exists():
            continue
        try:
            if render(d / "SKILL.md"):
                changed.append(d.name)
        except ValueError as e:              # that file is left exactly as it was
            refused.append(str(e))
    print(f"rendered: {len(changed)} changed" + (f" ({', '.join(changed)})" if changed else ""))
    for r in refused:
        print(f"  refused: {r}", file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
