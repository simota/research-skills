#!/usr/bin/env python3
"""Prove each rule in validate.py fires.

A check only ever seen passing may be checking nothing. Every rule below gets a
deliberate violation injected into a throwaway copy of the repo, and the test
fails if the validator stays quiet.

Run: make test
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True                     # no __pycache__ in the tools dir
import validate                                    # noqa: E402  — for RULES only


def run(root: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(root / "research-tools" / "validate.py")],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def sub(path: Path, old: str, new: str) -> None:
    t = path.read_text(encoding="utf-8")
    assert old in t, f"fixture text not found in {path.name}: {old[:60]!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


# Each case mutates a copy, then expects that rule id in the output — and, where
# it names one, that text in the rule's message, so a case cannot pass on some
# other failure the same rule happens to report.
S = "skills/"

CASES: dict[str, callable] = {}
EXPECT: dict[str, str] = {}
# Mutations the validator must stay quiet about: a fix that makes a rule fire
# on everything passes every case above.
QUIET: dict[str, callable] = {}


def case(rule, says: str | None = None):
    def deco(fn):
        CASES[rule] = fn
        if says:
            EXPECT[rule] = says
        return fn
    return deco


def quiet(name):
    def deco(fn):
        QUIET[name] = fn
        return fn
    return deco


@case("V1")
def _(r): sub(r / f"{S}research-source/SKILL.md", "## Owns", "## Owns\n" + "x\n" * 200)


@case("V2")
def _(r): sub(r / f"{S}research-source/SKILL.md", "Building the corpus",
              "Not for research-appraise. Building the corpus")


@case("V3")
def _(r): (r / f"{S}research-ghost").mkdir(); (r / f"{S}research-ghost/SKILL.md").write_text("x")


@case("V4")
def _(r): (r / f"{S}research-source/playbooks/orphan.md").write_text("<!-- research:guidance -->\n")


@case("V5")
def _(r): (r / f"{S}research-source/playbooks/traps.md").write_text("y\n" * 400)


@case("V6")
def _(r): sub(r / f"{S}_research/VALUES.md", "## 1. Calibration", "z\n" * 200 + "## 1. Calibration")


@case("V2-case", says="'instead of'")
def _(r): sub(r / f"{S}research-source/SKILL.md", "Building the corpus",
              "INSTEAD OF guessing. Building the corpus")


@case("V2-name-case", says="research-source description names research-appraise")
def _(r): sub(r / f"{S}research-source/SKILL.md", "Building the corpus",
              "Feeds Research-Appraise. Building the corpus")


@case("V4-resolved", says="playbooks/traps.md is not linked")
def _(r):
    """Same file name, other directory: a bare-name match counted it as linked."""
    sub(r / f"{S}research-source/SKILL.md", "](playbooks/traps.md)", "](reference/traps.md)")


@case("V7")
def _(r): sub(r / "research-registry/routes.yaml", "chain: [research-scope]",
              "chain: [research-nonexistent]")


@case("V8")
def _(r): sub(r / "README.md", "](skills/_research/CONTRACT.md)", "](skills/_research/GONE.md)")


@case("V8-title", says="GONE.md")
def _(r): sub(r / "README.md", "](skills/_research/CONTRACT.md)",
              '](skills/_research/GONE.md "the contract")')


@quiet("V8-title-resolves")
def _(r): sub(r / "README.md", "](skills/_research/CONTRACT.md)",
              '](skills/_research/CONTRACT.md "the contract")')


@quiet("worktree-under-.claude")
def _(r):
    """A worktree of this repo sits under .claude/; it is not a second corpus."""
    wt = r / ".claude/worktrees/w"
    shutil.copytree(r, wt, symlinks=True, ignore=shutil.ignore_patterns(".claude"))


@case("V9")
def _(r): sub(r / "research-registry/capabilities.yaml", "signals: [corpus, search strategy",
              "signals: [grading, search strategy")


@case("V10")
def _(r): sub(r / "research-registry/fixtures.yaml",
              '- ask: "build the corpus, and run disconfirming queries too"\n  expect: research-source',
              '- ask: "build the corpus, and run disconfirming queries too"\n  expect: research-scope')


@case("V10-empty", says="this rule is checking nothing")
def _(r): (r / "research-registry/fixtures.yaml").write_text("# every fixture removed\n")


@case("V11")
def _(r):
    import shutil
    for i in range(4):
        d = r / f"{S}research-extra{i}"
        d.mkdir()
        shutil.copy(r / f"{S}research-source/SKILL.md", d / "SKILL.md")


@case("V12")
def _(r): (r / f"{S}rogue").mkdir(); (r / f"{S}rogue/SKILL.md").write_text("x")


@case("V13")
def _(r):
    t = (r / "research-registry/routes.yaml").read_text(encoding="utf-8")
    t += "".join(f"\nfiller{i}:\n  pattern: linear\n  when: x\n  chain: [research-source]\n"
                 for i in range(20))
    (r / "research-registry/routes.yaml").write_text(t, encoding="utf-8")


@case("V13-stages", says="stages (max")
def _(r): sub(r / "research-registry/routes.yaml", "chain: [research-scope]",
              "chain: [" + ", ".join(["research-scope"] * 9) + "]")


@case("V14")
def _(r): sub(r / "research-registry/routes.yaml", "  pattern: loop", "  pattern: spiral")


@case("V15")
def _(r): sub(r / f"{S}research-route/SKILL.md", "allowed-tools: Read, Grep, Glob, Skill",
              "allowed-tools: Read, Grep, Glob, Write, Edit")


@case("V15-unclosed", says="allowed-tools is ''")
def _(r):
    """No closing `---` is no frontmatter, not frontmatter running to the end."""
    sub(r / f"{S}research-route/SKILL.md", "\n---\n", "\n")


@case("V16")
def _(r): sub(r / f"{S}research-source/SKILL.md", "## Done when", "## Finished when")


@case("V17")
def _(r): sub(r / f"{S}research-source/SKILL.md", "- **Preserve phase ownership.**",
              "- **Ignore phase ownership.**")


@case("V18")
def _(r): sub(r / f"{S}research-source/SKILL.md", "search log", "query record")


@case("V19")
def _(r): sub(r / f"{S}research-scope/SKILL.md", "`_research/SIZING.md`",
              "`../_research/SIZING.md`")


@case("V19-reference", says="channel-map.md references 'reference/gone.md'")
def _(r): sub(r / f"{S}research-source/reference/channel-map.md", "Verified:",
              "See `reference/gone.md`.\nVerified:")


@case("V19-link", says="links to '../../_research/CONTRACT.md', which leaves")
def _(r):
    """Resolves on disk, so V8 is quiet — and leaves the skill once installed."""
    sub(r / f"{S}research-source/playbooks/traps.md", "<!-- research:guidance -->\n",
        "<!-- research:guidance -->\n[contract](../../_research/CONTRACT.md)\n")


@case("V19-shared-link", says="which a skill reads as 'research-scope/SKILL.md'")
def _(r):
    """Exists on disk, so V8 is quiet; inside an installed skill it is nothing."""
    sub(r / f"{S}_research/ROUTING.md", "# Research Family Boundaries\n",
        "# Research Family Boundaries\n\nSee [scope](../research-scope/SKILL.md).\n")


@quiet("README names the tools directory")
def _(r): sub(r / "README.md", "## Working on it\n", "## Working on it\n\nThe tools live in `research-tools`.\n")


@quiet("playbook links its own reference page")
def _(r):
    """`../reference/` from a playbook normalises inside the skill: V8, V19 and
    V30 all have to accept it, or a playbook can link its reference no way at all."""
    sub(r / f"{S}research-route/playbooks/depth-tiers.md", "# Depth Tiers, Not Research\n",
        "# Depth Tiers, Not Research\n\nSee [chain patterns](../reference/chain-patterns.md).\n")


@case("V19-shared")
def _(r): sub(r / f"{S}_research/CONTRACT.md", "`_research/SOURCE_HYGIENE.md`", "`SOURCE_HYGIENE.md`")


@case("V19-shared-one-skill", says="'playbooks/grading.md', which does not resolve from research-report/")
def _(r):
    """Resolves from research-appraise, the one skill shared pages were checked
    against, and from no other skill that reads the contract."""
    sub(r / f"{S}_research/CONTRACT.md", "`_research/SOURCE_HYGIENE.md`",
        "`_research/SOURCE_HYGIENE.md` (grade with `playbooks/grading.md`)")


@case("V20")
def _(r):
    """The definition row becomes a mention; the word is still on the page."""
    sub(r / f"{S}_research/CONTRACT.md", "| `UNSUPPORTED` |", "| UNSUPPORTED |")


@case("V21")
def _(r): sub(r / f"{S}research-source/SKILL.md",
              "Capture provenance without grading: appraisal will decide whether a named claim\nhas a `P1` primary record.",
              "Capture provenance without grading.")


@case("V22")
def _(r): sub(r / f"{S}research-source/SKILL.md", "## Done when",
              "## Done when\n\n#" + "TODO(agent): tidy this up later\n")


@case("V22-code-span", says="marker carries no residual class")
def _(r):
    """A backtick elsewhere on the line used to excuse the marker."""
    sub(r / f"{S}research-source/SKILL.md", "## Done when",
        "## Done when\n\nfix `x` #" + "TODO(agent): tidy this up later\n")


@case("V23")
def _(r): sub(r / f"{S}_research/CONTRACT.md", "<!-- research:contract -->", "<!-- research:guidance -->")


@case("V24")
def _(r): sub(r / f"{S}_research/ROUTING.md", "`research-synthesize`", "`research-combine`")


@case("V24-hyphen", says="names research-synth-x")
def _(r): sub(r / f"{S}_research/ROUTING.md", "`research-synthesize`", "`research-synth-x`")


@case("V25")
def _(r): sub(r / f"{S}research-source/playbooks/traps.md", "# ", "# pinned at v2.14.0 — ")


@case("V26")
def _(r): sub(r / "research-registry/capabilities.yaml", "      go: research-appraise",
              "      go: research-grade")


@case("V27")
def _(r):
    (r / f"{S}research-source/_research").unlink()
    (r / f"{S}research-source/_research").symlink_to("../_gone")


# Below the top of a skill too: only the entries directly in it were looked at.
@case("V27-nested")
def _(r):
    f = r / f"{S}research-scope/reference/question-design.md"
    outside = r.parent / "question-design.md"
    outside.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    f.unlink()
    f.symlink_to(outside)


# Through a linked directory: research-registry/ is reached by every skill's
# `registry` link, and was checked as a link and never walked.
@case("V27-through-link", says="registry/delivered/outside.md points outside")
def _(r):
    outside = r.parent / "outside.md"
    outside.write_text("x\n", encoding="utf-8")
    (r / "research-registry/delivered/outside.md").symlink_to(outside)


@case("V27-through-link-broken", says="registry/delivered/gone.md is a broken")
def _(r): (r / "research-registry/delivered/gone.md").symlink_to("../nowhere.md")


@case("V27-skill-dir", says="skills/research-report points outside the repo")
def _(r):
    """The skill directory itself linked in from elsewhere: only what sat inside
    it was walked, and its links back into the repo all resolved."""
    outside = r.parent / "research-report"
    (r / f"{S}research-report").rename(outside)
    for name, target in (("_research", r / f"{S}_research"), ("registry", r / "research-registry")):
        (outside / name).unlink()
        (outside / name).symlink_to(target)
    (r / f"{S}research-report").symlink_to(outside)


@case("V28")
def _(r): sub(r / "research-registry/harness.yaml", "set: research", "set: rsrch")


@case("V28-generic-dir")
def _(r): (r / "registry").mkdir()


def git_init(r: Path) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", "init", "-q", str(r)], env=env, check=True)


# Ignored by git is what excuses a directory, not merely being untracked.
@case("V28-untracked-dir", says="stray/ carries no set name")
def _(r): git_init(r); (r / "stray").mkdir()


@quiet("ignored .venv at the top")
def _(r):
    """A virtualenv made to install pyyaml is not a directory this set owns,
    and the markdown pip vendors into it is not a page of the corpus."""
    git_init(r)
    lic = r / ".venv/lib/python3/site-packages/pip-x.dist-info/LICENSE.md"
    lic.parent.mkdir(parents=True)
    lic.write_text("x\n" * 6000, encoding="utf-8")


@case("V29")
def _(r):
    f = r / f"{S}research-source/reference/channel-map.md"
    f.write_text(f.read_text(encoding="utf-8").replace("Verified:", "Checked:"), encoding="utf-8")


@case("V29-not-at-line-start", says="channel-map.md has no 'Verified:'")
def _(r):
    """`**Verified:**` passed here, and V31 and V37, which read the header from
    the start of a line, skipped the page as one V29 had already reported."""
    sub(r / f"{S}research-source/reference/channel-map.md", "Verified:", "**Verified:**")


@case("V30")
def _(r): (r / f"{S}research-source/reference/orphan.md").write_text(
    "<!-- research:deferred -->\n# Orphan\n\nPurpose: x\nRead when: y\nVerified: 2026-08-21\n")


@case("V1-unparsed", says="frontmatter does not parse as YAML")
def _(r): sub(r / f"{S}research-source/SKILL.md", 'description: "Building the corpus:',
              'description: Note: "Building the corpus:')


@case("V1-non-string", says="frontmatter gives ['description'] a non-string value")
def _(r):
    t = (r / f"{S}research-source/SKILL.md").read_text(encoding="utf-8")
    line = next(l for l in t.splitlines() if l.startswith("description:"))
    sub(r / f"{S}research-source/SKILL.md", line, "description: 12345")


@case("V31")
def _(r):
    for f in sorted((r / f"{S}").glob("*/reference/*.md")):
        t = f.read_text()
        i = t.index("Verified:")
        j = t.index("\n\n", i)
        f.write_text(t[:i] + "Verified: 2026-08-21" + t[j:])
        return


@case("V30-resolved", says="channel-map.md is reachable from nothing")
def _(r): sub(r / f"{S}research-source/SKILL.md", "](reference/channel-map.md)",
              "](playbooks/channel-map.md)")


@case("V31-leak", says="channel-map.md states a `Verified:` date")
def _(r):
    """The marker is in the next sentence, not on the header."""
    sub(r / f"{S}research-source/reference/channel-map.md",
        "Verified: 2026-08-21 — no automated check.\n",
        "Verified: 2026-08-21.\nNothing here is re-checked by anyone.\n")


@case("V31-bare-leak", says="channel-map.md states a `Verified:` date and nothing else on its line")
def _(r):
    """No period to end the date, so the old continuation rule read on into the body."""
    sub(r / f"{S}research-source/reference/channel-map.md",
        "Verified: 2026-08-21 — no automated check.\n",
        "Verified: 2026-08-21\nThe table below is re-checked by running nothing at all.\n")


@case("V32")
def _(r):
    sub(r / "research-registry/routes.yaml", "checker: ", "checker: claude  # ")


@case("V32-unknown")
def _(r):
    sub(r / "research-registry/routes.yaml", "checker: ", "checker: nosuchengine  # ")



@case("V32-single")
def _(r):
    sub(r / "research-registry/harness.yaml",
        "runs_on: [claude, codex, agy]", "runs_on: [claude]")



@case("V33")
def _(r):
    sub(r / "research-registry/harness.yaml", "  lens: |", "  lens: ''\n  unused: |")



@case("V34")
def _(r):
    """Reachable and runnable must move together, whichever way they are split."""
    for d in sorted((r / "skills").glob("research-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()                      # runnable, and now out of reach
            return
    # No set-wide link to remove: make a skill runnable instead, and leave it
    # unreachable. Widening a class trips V15 too, which the harness allows —
    # it only asks that V34 appear.
    sub(r / "research-registry/harness.yaml",
        "tools: \"Read, Grep, Glob, Write", "tools: \"Read, Grep, Glob, Bash, Write")


@case("V34-decoration")
def _(r):
    """A link where the class grants no shell reads like a capability and is not one."""
    import yaml as _y
    caps = _y.safe_load((r / "research-registry/capabilities.yaml").read_text())
    cls = _y.safe_load((r / "research-registry/harness.yaml").read_text())["permission_classes"]
    for name, e in caps.items():
        if "Bash" not in cls[e["class"]]["tools"]:
            (r / "skills" / name / "refute.py").symlink_to("../../research-tools/refute.py")
            return
    for d in sorted((r / "skills").glob("research-*")):
        link = d / "refute.py"
        if link.is_symlink():
            link.unlink()
            link.symlink_to("../../research-tools/render.py")   # the set's own, but the wrong tool
            return


@case("V34-undeclared")
def _(r):
    """A tool link nothing declares is a capability nobody decided to grant."""
    (r / "skills/research-source/render.py").symlink_to("../../research-tools/render.py")


@case("V34-missing-tool")
def _(r): sub(r / "research-registry/harness.yaml",
              "  refute.py: all", "  refute.py: all\n  nosuch.py: all")


@case("V34-none-declared")
def _(r): sub(r / "research-registry/harness.yaml", "linked_tools:", "unlinked_tools:")


@quiet("linked_tools names one skill bare")
def _(r):
    """`set()` of a bare name split it into letters, each reported as no skill."""
    sub(r / "research-registry/harness.yaml", "refute.py: all", "refute.py: research-appraise")


@case("V35")
def _(r): sub(r / f"{S}research-report/SKILL.md", "an unopened record and an opened one",
              "a second-hand record and a first-hand one")


@case("V36")
def _(r):
    """An empty required_of has to say why, or the absence is an oversight."""
    h = r / "research-registry/harness.yaml"
    lines = h.read_text(encoding="utf-8").splitlines(keepends=True)
    out, drop = [], False
    for l in lines:
        if l.startswith("  why:"):
            drop = True
            continue
        if drop and (l.startswith("    ") or not l.strip()):
            continue
        drop = False
        out.append(l)
    h.write_text("".join(out), encoding="utf-8")


@case("V36-none-declared")
def _(r): sub(r / "research-registry/harness.yaml", "finding_visuals:", "unused_visuals:")


@case("V7-crash", says="could not run (TypeError")
def _(r):
    """An empty `chain:` crashed the whole run; now V7 says so and the rest report."""
    sub(r / "research-registry/routes.yaml", "chain: [research-scope]", "chain:")


@case("V38-underscored", says="switches on NOT_A_KIND")
def _(r):
    """`trigger.kind` is underscored; the old pattern never saw the line at all."""
    sub(r / f"{S}_research/HANDOFF.md", "| NEEDS_SYNTHESIS | REVISE_SCOPE",
        "| NEEDS_SYNTHESIS | NOT_A_KIND | REVISE_SCOPE")


@case("V20-handoff", says="defines 'STOP' (next_actions)")
def _(r): sub(r / f"{S}_research/HANDOFF.md", "| `STOP` |", "| STOP |")


@case("V38")
def _(r): sub(r / f"{S}research-source/playbooks/traps.md", "<!-- research:guidance -->\n",
              "<!-- research:guidance -->\nverdict: KEEP | DROP\n")


@case("V38-digits", says="switches on P6")
def _(r):
    """The evidence ladder is the vocabulary with digits in it, and a word with
    a digit ended the match, so no listing of it was ever read."""
    sub(r / f"{S}research-source/playbooks/traps.md", "<!-- research:guidance -->\n",
        "<!-- research:guidance -->\ntier: P1 | P2 | P6\n")


@case("V37")
def _(r):
    """Neither a source nor the admission that there is none."""
    sub(r / f"{S}research-scope/reference/question-design.md",
        "Source: none — nothing outside this page can move what it states.", "Source:")


@case("V37-none-word", says="question-design.md names no source")
def _(r):
    """`none` inside another word is not the admission."""
    sub(r / f"{S}research-scope/reference/question-design.md",
        "Source: none — nothing outside this page can move what it states.",
        "Source: nonexistent.")


@case("V37-none-declared")
def _(r): sub(r / "research-registry/harness.yaml", "source_authorities:", "unused_authorities:")


@case("V17-unexpected")
def _(r):
    src = (r / f"{S}research-source/SKILL.md").read_text()
    block = re.search(r"<!-- deliver:reach -->.*?<!-- /deliver:reach -->", src, re.S).group()
    sub(r / f"{S}research-scope/SKILL.md", "## Verify with", "## Verify with\n" + block)


@case("V17-unknown-scope")
def _(r): sub(r / "research-registry/harness.yaml", "only: signature", "only: nowhere")


@case("V17-missing-target")
def _(r):
    p = r / f"{S}research-source/SKILL.md"
    p.write_text(re.sub(r"<!-- deliver:reach -->.*?<!-- /deliver:reach -->", "", p.read_text(), flags=re.S))


# A blank line inside the markers is drift render removes; V17 passed it, so
# the hook was green over a file CI's "Delivered blocks are current" fails.
@case("V17-blank-inside", says="values block differs")
def _(r):
    p = r / f"{S}research-scope/SKILL.md"
    sub(p, "<!-- deliver:values -->\n", "<!-- deliver:values -->\n\n")
    sub(p, "\n<!-- /deliver:values -->", "\n\n<!-- /deliver:values -->")


@case("V17-duplicate", says="reach delivery block more than once")
def _(r):
    p = r / f"{S}research-source/SKILL.md"
    block = re.search(r"<!-- deliver:reach -->.*?<!-- /deliver:reach -->", p.read_text(), re.S).group()
    sub(p, "## Done when", block + "\n\n## Done when")


@case("V35-delivery-scope")
def _(r): sub(r / "research-registry/harness.yaml", ", only: signature", "")


def main() -> int:
    code, baseline = run(ROOT)
    if code != 0:
        print("the working tree is already failing; fix that first:\n" + baseline)
        return 1

    def mutated(mutate) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, symlinks=True,
                            ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
            mutate(copy)
            return run(copy)

    bad: list[str] = []
    for rule, mutate in CASES.items():
        code, out = mutated(mutate)
        expect = rule.split("-")[0]
        lines = re.findall(rf"^\s*{expect}: .*$", out, re.M)
        says = EXPECT.get(rule)
        # A rule that crashed on its own mutation has not fired; only a case
        # about crashing may count that line.
        if not (says and "could not run" in says):
            lines = [l for l in lines if "could not run" not in l]
        if code == 0 or not lines or (says and not any(says in l for l in lines)):
            bad.append(rule)
            print(f"  {rule} did not fire" + (f" saying {says!r}" if says else "") + f"\n{out}")

    loud: list[str] = []
    for name, mutate in QUIET.items():
        code, out = mutated(mutate)
        if code != 0:
            loud.append(name)
            print(f"  {name} should pass and does not\n{out}")

    print(f"{len(CASES)} rules exercised, {len(bad)} silent · "
          f"{len(QUIET)} harmless edits, {len(loud)} flagged")
    if bad or loud:
        if bad:
            print("silent: " + ", ".join(bad))
        if loud:
            print("flagged: " + ", ".join(loud))
        return 1

    # Counting the cases that exist says nothing about the rules that do. A rule
    # added without a case left this printing "every rule fires" about it.
    covered = {c.split("-")[0] for c in CASES}
    declared = {fn.__name__.split("_")[0].upper() for fn in validate.RULES}
    untested = sorted(declared - covered, key=lambda r: int(r[1:]))
    if untested:
        print("no deliberate violation is injected for: " + ", ".join(untested))
        return 1
    print(f"every rule fires ({len(declared)} rules, {len(CASES)} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
