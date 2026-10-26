#!/usr/bin/env python3
"""Prove the pre-commit hook checks what is being committed.

The hook once validated the working tree, so a staged violation went through
whenever the file on disk had since been put right but not re-staged. Each case
below builds a throwaway repository from the current files, installs the hook,
and commits.

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
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
from validate import copy_ignore                   # noqa: E402
TARGET = "skills/research-source/playbooks/traps.md"
BREAK = "\n| lonely | row |\n"          # a row outside any table: figures_check fails


# Nothing from the caller's git may steer the throwaway repository: GIT_DIR and
# friends would point every command at the outer one, and a global
# commit.gpgsign would make the base commit prompt for a key.
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-c", "commit.gpgsign=false", "-C", str(repo), *args],
                          capture_output=True, text=True, env=ENV)


def fresh(tmp: Path) -> Path:
    repo = tmp / "repo"
    shutil.copytree(ROOT, repo, symlinks=True,
                    ignore=copy_ignore(ROOT))
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


def intent_to_add_not_committed(repo: Path) -> bool:
    """Must be refused: `git add -N` puts a path in the index that the commit
    does not carry, and the hook used to export it, so a link to it passed."""
    (repo / "NEWPAGE.md").write_text("# New\n", encoding="utf-8")
    (repo / "README.md").write_text((repo / "README.md").read_text(encoding="utf-8")
                                    + "\nSee [new](NEWPAGE.md).\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "add", "-N", "NEWPAGE.md")
    r = git(repo, "commit", "-q", "-m", "links to a file it does not carry")
    return r.returncode != 0 and "NEWPAGE.md" in r.stdout + r.stderr


def sparse_checkout_clean(repo: Path) -> bool:
    """Must be accepted: a path left out of a sparse checkout is still committed,
    and the hook used to skip it, so a link to it read as broken."""
    git(repo, "sparse-checkout", "set", "--no-cone", "/*", "!/docs/")
    if (repo / "docs").exists():
        return False                        # the case would not be testing anything
    (repo / "README.md").write_text((repo / "README.md").read_text(encoding="utf-8") + "\n",
                                    encoding="utf-8")
    git(repo, "add", "README.md")
    return git(repo, "commit", "-q", "-m", "clean").returncode == 0


CASES = (staged_broken_tree_clean, staged_clean_tree_broken, intent_to_add_not_committed,
         sparse_checkout_clean)


def main() -> int:
    if shutil.which("git") is None:
        print("git is not installed; the hook cannot be exercised")
        return 1
    wrong = []
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            if not case(fresh(Path(tmp))):
                wrong.append(case.__name__)
                print(f"  {case.__name__}: {case.__doc__}")
    print(f"{len(CASES)} hook cases exercised, {len(wrong)} wrong")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
