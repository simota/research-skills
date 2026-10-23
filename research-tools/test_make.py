#!/usr/bin/env python3
"""Prove `make link` / `unlink` / `hooks` act on the right paths and nothing else.

Each case runs the real Makefile with a scratch HOME, so nothing outside a
temporary directory is touched.

Run: make test
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(p.parent.name for p in (ROOT / "skills").glob("research-*/SKILL.md"))


def make(home: Path, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    env = dict(os.environ, HOME=str(home))
    for var in ("CLAUDE_DIR", "CODEX_DIR", "AGY_DIR", "MAKEFLAGS"):
        env.pop(var, None)
    return subprocess.run(["make", "-s", *args], cwd=cwd, env=env,
                          capture_output=True, text=True)


def home_with_a_space(tmp: Path) -> str | None:
    """Unquoted, the host loop split the path and linked into its first half."""
    home = tmp / "my home"
    (home / ".claude").mkdir(parents=True)
    r = make(home, "link")
    got = sorted(p.name for p in (home / ".claude/skills").iterdir()) \
        if (home / ".claude/skills").is_dir() else []
    if r.returncode != 0 or got != SKILLS or (tmp / "my").exists():
        return f"exit {r.returncode}, linked {got}, stray: {(tmp / 'my').exists()}"
    make(home, "unlink")
    left = list((home / ".claude/skills").iterdir())
    return None if not left else f"unlink left {left}"


def foreign_link_is_kept(tmp: Path) -> str | None:
    home, other = tmp / "home", tmp / "other" / SKILLS[0]
    other.mkdir(parents=True)
    (home / ".claude/skills").mkdir(parents=True)
    foreign = home / ".claude/skills" / SKILLS[0]
    foreign.symlink_to(other)
    linked = make(home, "link")
    ours = [home / ".claude/skills" / s for s in SKILLS[1:]]
    if linked.returncode != 0 or not all(p.is_symlink() for p in ours):
        return f"link: exit {linked.returncode}, linked {[p.name for p in ours if p.is_symlink()]}"
    unlinked = make(home, "unlink")
    if unlinked.returncode != 0 or any(p.is_symlink() for p in ours):
        return f"unlink: exit {unlinked.returncode}; this checkout's links were left"
    if not foreign.is_symlink() or foreign.resolve() != other.resolve():
        return "a link owned by another checkout was replaced or removed"
    return None


def outside_the_repo_refuses(tmp: Path) -> str | None:
    home = tmp / "home"
    (home / ".claude").mkdir(parents=True)
    r = make(home, "-f", str(ROOT / "Makefile"), "link", cwd=tmp)
    if r.returncode == 0 or (home / ".claude/skills").exists():
        return f"exit {r.returncode}; ran from outside the repo"
    return None


def git_copy(tmp: Path) -> Path:
    """This repository's files in a fresh git repository, so `make hooks` writes
    into a scratch `.git` and never this checkout's."""
    repo = tmp / "repo"
    shutil.copytree(ROOT, repo, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", "init", "-q", str(repo)], env=env, check=True)
    return repo


def foreign_hook_is_kept(tmp: Path) -> str | None:
    """A plain cp replaced whatever pre-commit hook was there, with no word."""
    repo = git_copy(tmp)
    hook = repo / ".git/hooks/pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\necho my-own-lint\n", encoding="utf-8")
    r = make(tmp, "hooks", cwd=repo)
    if r.returncode == 0 or "my-own-lint" not in hook.read_text(encoding="utf-8"):
        return f"exit {r.returncode}; another hook was replaced: {r.stdout}{r.stderr}"
    # An older copy of this set's own hook is replaced: that is how a fix to it arrives.
    hook.write_text("#!/bin/sh\n# Install with: make hooks\nexit 0\n", encoding="utf-8")
    r = make(tmp, "hooks", cwd=repo)
    ours = (repo / "research-tools/githooks/pre-commit").read_text(encoding="utf-8")
    if r.returncode != 0 or hook.read_text(encoding="utf-8") != ours:
        return f"an older copy of this hook was not updated: exit {r.returncode}: {r.stderr}"
    # A link to a hook elsewhere is not this checkout's to write through: cp
    # followed it and replaced the file it pointed at, install line or not.
    shared = tmp / "shared-pre-commit"
    shared.write_text("#!/bin/sh\n# Install with: make hooks\necho shared\n", encoding="utf-8")
    hook.unlink()
    hook.symlink_to(shared)
    r = make(tmp, "hooks", cwd=repo)
    if r.returncode == 0 or "echo shared" not in shared.read_text(encoding="utf-8") \
            or not hook.is_symlink():
        return f"a linked hook was written through: exit {r.returncode}: {r.stdout}{r.stderr}"
    return None


def hooks_path_already_here(tmp: Path) -> str | None:
    """Pointed at research-tools/githooks, cp failed copying the hook onto itself."""
    repo = git_copy(tmp)
    subprocess.run(["git", "-C", str(repo), "config", "core.hooksPath", "research-tools/githooks"],
                   check=True)
    r = make(tmp, "hooks", cwd=repo)
    return None if r.returncode == 0 else f"exit {r.returncode}: {r.stdout}{r.stderr}"


CASES = [home_with_a_space, foreign_link_is_kept, outside_the_repo_refuses,
         foreign_hook_is_kept, hooks_path_already_here]


def main() -> int:
    if shutil.which("make") is None:
        print("make is not installed; the Makefile cannot be exercised")
        return 1
    wrong = 0
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            why = case(Path(tmp))
        if why:
            wrong += 1
            print(f"  {case.__name__}: {why}")
    print(f"{len(CASES)} make cases exercised, {wrong} wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
