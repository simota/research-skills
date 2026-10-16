#!/usr/bin/env python3
"""Prove the pre-commit hook checks what is being committed.

The hook once validated the working tree, so a staged violation went through
whenever the file on disk had since been put right but not re-staged. Each case
below builds a throwaway repository from the current files, installs the hook,
and commits.

Run: make test
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = "skills/research-source/playbooks/traps.md"
BREAK = "\n| lonely | row |\n"          # a row outside any table: figures_check fails


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def fresh(tmp: Path) -> Path:
    repo = tmp / "repo"
    shutil.copytree(ROOT, repo, symlinks=True,
                    ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "hook@test")
    git(repo, "config", "user.name", "hook test")
    # Outside the repository: a stray directory inside it would fail V28 and
    # refuse every commit, which is the right answer for the wrong reason.
    hooks = tmp / "hooks"
    hooks.mkdir()
    git(repo, "config", "core.hooksPath", str(hooks))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--no-verify", "-m", "base")
    shutil.copy(repo / "research-tools/githooks/pre-commit", hooks / "pre-commit")
    (hooks / "pre-commit").chmod(0o755)
    return repo


def staged_broken_tree_clean(repo: Path) -> bool:
    """Must be refused: the commit would carry the violation."""
    f = repo / TARGET
    clean = f.read_text(encoding="utf-8")
    f.write_text(clean + BREAK, encoding="utf-8")
    git(repo, "add", TARGET)
    f.write_text(clean, encoding="utf-8")
    r = git(repo, "commit", "-q", "-m", "broken")
    return r.returncode != 0 and "lonely" in r.stdout + r.stderr


def staged_clean_tree_broken(repo: Path) -> bool:
    """Must be accepted: the violation is not part of the commit."""
    (repo / "README.md").write_text((repo / "README.md").read_text(encoding="utf-8") + "\n",
                                    encoding="utf-8")
    git(repo, "add", "README.md")
    f = repo / TARGET
    f.write_text(f.read_text(encoding="utf-8") + BREAK, encoding="utf-8")
    return git(repo, "commit", "-q", "-m", "clean").returncode == 0


def main() -> int:
    if shutil.which("git") is None:
        print("git is not installed; the hook cannot be exercised")
        return 1
    wrong = []
    for case in (staged_broken_tree_clean, staged_clean_tree_broken):
        with tempfile.TemporaryDirectory() as tmp:
            if not case(fresh(Path(tmp))):
                wrong.append(case.__name__)
                print(f"  {case.__name__}: {case.__doc__}")
    print(f"2 hook cases exercised, {len(wrong)} wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
