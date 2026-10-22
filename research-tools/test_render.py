#!/usr/bin/env python3
"""Prove render.py refuses what it cannot render safely, and agrees with V17.

render.py writes the delivered blocks into every SKILL.md; V17 checks them.
Each case breaks one thing in a throwaway copy, runs render, and checks the
exit code, what happened to the file, and whether the validator then agrees.

Run: make test
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = "skills/research-scope/SKILL.md"


def run(root: Path, tool: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(root / "research-tools" / tool)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def without_surface(f: Path, old_heading: str, new_heading: str) -> None:
    """Drop the surface block, so render has to insert it, and rename its section."""
    t = f.read_text(encoding="utf-8")
    start = t.index("<!-- deliver:surface -->")
    end = t.index("<!-- /deliver:surface -->\n") + len("<!-- /deliver:surface -->\n")
    f.write_text((t[:start] + t[end:]).replace(old_heading, new_heading, 1), encoding="utf-8")


def clean_is_idempotent(r: Path) -> str | None:
    code, out = run(r, "render.py")
    return None if code == 0 and "rendered: 0 changed" in out else f"exit {code}: {out}"


def unmatched_marker_is_refused(r: Path) -> str | None:
    """Without its close marker, the old body used to stay behind as stale text."""
    f = r / SCOPE
    sub(f, "<!-- /deliver:values -->\n", "")
    before = f.read_text(encoding="utf-8")
    code, out = run(r, "render.py")
    if code == 0 or "unmatched values marker" not in out:
        return f"exit {code}: {out}"
    return None if f.read_text(encoding="utf-8") == before else "the refused file was rewritten"


def leading_blank_line_agrees(r: Path) -> str | None:
    """A blank first line in a delivered file: render and V17 must settle together."""
    d = r / "research-registry/delivered/values.md"
    d.write_text("\n" + d.read_text(encoding="utf-8"), encoding="utf-8")
    run(r, "render.py")
    code, out = run(r, "validate.py")
    return None if code == 0 else f"validate after render: {out}"


def heading_with_trailing_space_renders(r: Path) -> str | None:
    without_surface(r / SCOPE, "## Done when\n", "## Done when \n")
    code, out = run(r, "render.py")
    if code != 0:
        return f"render: exit {code}: {out}"
    code, out = run(r, "validate.py")
    return None if code == 0 else f"validate after render: {out}"


def empty_section_keeps_its_block(r: Path) -> str | None:
    """A section with no body yet: the block used to land under the next heading,
    render said it succeeded, and V17 then failed on a file render could not fix."""
    f = r / SCOPE
    t = f.read_text(encoding="utf-8")
    start = t.index("## Before starting\n") + len("## Before starting\n")
    f.write_text(t[:start] + t[t.index("## Decide first\n"):], encoding="utf-8")
    code, out = run(r, "render.py")
    if code != 0:
        return f"render: exit {code}: {out}"
    t = f.read_text(encoding="utf-8")
    if not t.index("## Before starting\n") < t.index("<!-- deliver:sizing -->") \
            < t.index("## Decide first\n"):
        return "the sizing block was not written under 'Before starting'"
    code, out = run(r, "validate.py")
    return None if code == 0 else f"validate after render: {out}"


def missing_section_is_refused(r: Path) -> str | None:
    without_surface(r / SCOPE, "## Done when\n", "## Finished when\n")
    code, out = run(r, "render.py")
    return None if code != 0 and "research-scope/SKILL.md has no section 'Done when'" in out \
        else f"exit {code}: {out}"


CASES = [clean_is_idempotent, unmatched_marker_is_refused, leading_blank_line_agrees,
         heading_with_trailing_space_renders, empty_section_keeps_its_block,
         missing_section_is_refused]


def main() -> int:
    wrong = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
            why = case(copy)
        if why:
            wrong += 1
            print(f"  {case.__name__}: {why}")
    print(f"{len(CASES)} render cases exercised, {wrong} wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
