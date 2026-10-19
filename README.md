# research-skills

Six agent skills covering the research chain, the contracts they share, and the
budgets that keep the set from growing into something nobody can route through.

| Skill | Owns | Class |
|---|---|---|
| [`research-route`](skills/research-route/SKILL.md) | The depth tier, the chain, and one budget across it | route |
| [`research-scope`](skills/research-scope/SKILL.md) | The brief: question, answer shape, bar, stopping rule | doc-write |
| [`research-source`](skills/research-source/SKILL.md) | The corpus and its provenance | **retrieve — the only skill that reaches the web** |
| [`research-appraise`](skills/research-appraise/SKILL.md) | What each source is worth, for a named claim | doc-write |
| [`research-synthesize`](skills/research-synthesize/SKILL.md) | The claim ledger, confidence, and supported answer | doc-write |
| [`research-report`](skills/research-report/SKILL.md) | Audience-shaped writing of established findings | doc-write |

## The four ideas the set is built on

**Evidence is tiered against a claim, not against a source.** `P1` primary
record · `P2` rigorous secondary · `P3` credible reported · `P4` attributed
opinion · `P5` unattributed or derivative. The same official page is `P1` for
documented behaviour and `P4` for a comparative claim. **Weigh by tier,
independence and directness — never by source count**: five sources repeating
one primary are one source.

**One skill assigns confidence.** Appraisal recommends a ceiling and never sets
a label, because a label set early becomes an unremovable cap. Report
preserves synthesis labels and semantic qualification. Without synthesis, quick/vet assign no
label and state the chain limitation; an appraisal ceiling is not an assignment. **Hedge-stripping is
the single most common way an honest chain produces a dishonest deliverable**.

**Fetched content is data, never instruction.** Retrieved text may contain
directions addressed to whoever reads it. They are the object of study, never
input to the run — and that holds when the text is re-read later inside a
quotation, which is where it is easiest to forget.

**A citation to the record and a citation to an article about the record look
identical in a bibliography.** One is a claim about the primary; the other is a
claim about what a writer said the primary contains — and writers compress,
round, and drop the caveat. So every load-bearing claim carries a reach beside
its tier: `primary` · `one-hop` · `chain` · `blocked` (naming what would unblock
it, so the missing certainty has a price) · `no-primary`.

The report states the rate as a count — `4 of 7`, never a bare percentage. **A
low rate is not a failure**; it is the honest shape of research done under a
budget, and stating it lets the reader discount accordingly. **Five sources
repeating one unopened primary are one unopened source**
([`_research/REACH.md`](skills/_research/REACH.md)).

## How it is put together

A skill is loaded in three stages. The **listing** carries `name` and
`description` only, on every turn. **`SKILL.md`** is read in full once a skill
is chosen. Anything it points at is read only when the situation calls for it.

**Selection happens on the description alone**, so every word that selects a
skill appears literally in its description, and
[`research-registry/capabilities.yaml`](research-registry/capabilities.yaml)
lists those words per skill. A rule checks the two agree.

**Boundaries live in one file** — that same registry's `not:`. Descriptions
never name a neighbour. If they did, adding a seventh skill would mean editing
the other six.

**Contracts are delivered, not referenced.** The operative part of each contract
is rendered into its declared owners; shared wording is conditional on phase ownership.
`make render` writes it back, removes out-of-scope blocks, and a rule fails on drift.

**Knowledge splits by whether it rots.** `playbooks/` holds judgement and is
budgeted. `reference/` holds what goes stale — channel maps, report formats,
appraisal checklists — carries no line budget, and states its purpose and a
checked-on date instead.

**A rule stated in prose is a rule nobody can fail.** `make figures` re-derives
what the corpus claims about itself, and runs in `make check`, CI and the
pre-commit hook. It found two things a reader could not.

The `Low` and `Unknown` rows of the confidence table in `_research/CONTRACT.md`
sat outside it: a sentence about undated pages had been inserted between the
rows, which splits a markdown table silently. The source reads fine; the render
does not. Every skill reads that table through the shared directory, and the rows
that fell out were the two labels the set most wants used.

And "multiply, do not maintain" was not an operation anyone could perform. The
contract allows no percentages, so composition runs on four ordered labels — one
of the sixteen pairs was written down and the other fifteen were left to the
reader. The table is now stated, and the checker holds it to the properties that
make a chain well-defined: it never rises, it is monotone, `Unknown` absorbs, and
it is associative across all 64 triples, so a chain has one answer rather than
one per bracketing. Those properties constrain the table without pinning it —
that limit is stated on the page rather than glossed.

**Budgets are enforced, not intended.**
[`research-registry/harness.yaml`](research-registry/harness.yaml) holds every
budget and vocabulary; `research-tools/validate.py` decides them and CI fails on a
violation. (A few structural constants — the six SKILL.md sections, the 12-line
reference-header window — live in the validator itself.)

## Names, and why none of them are generic

A skills directory is flat and shared with every other set on the machine, so a
generic name placed there is a silent collision. This set's shared directory used
to be `_common` — the same name an unrelated set already occupies in that
directory, and which a third set's install line copies into it.

**One declaration.** `set: research` in the harness file is the one the rest is
held to: the prefix, the shared directory (`_research/`) and the label every
document carries are written out elsewhere too, and V28 and V23 fail when any of
them stops agreeing with it.

**Every directory this set owns carries the set name**, with `skills/` (where the
install instructions look) and `docs/` (where Pages publishes from) exempt, as
`platform_dirs` in the harness file declares. Carrying the prefix is not what makes
something installable — a skill is a directory holding a `SKILL.md`.

**Everything a skill reads lives inside the skill**, reached through symlinks
named `_research` and `registry`. Relative paths are normalised *lexically*, so
a bare sibling reference in a shared contract resolves against the skill
directory, not against the file that wrote it — which is what makes that fail
quietly.

## Files

| File | What it fixes |
|---|---|
| [`skills/_research/CONTRACT.md`](skills/_research/CONTRACT.md) | Source IDs, the ladder, confidence, independence, recency, status, residuals, the sweep |
| [`skills/_research/SOURCE_HYGIENE.md`](skills/_research/SOURCE_HYGIENE.md) | Provenance capture, the data-not-instruction invariant, access limits |
| [`skills/_research/SIZING.md`](skills/_research/SIZING.md) | Depth, one budget across the chain, when a dialogue is mandatory |
| [`skills/_research/REACH.md`](skills/_research/REACH.md) | How close each claim got to the record, and the reach rate |
| [`skills/_research/VALUES.md`](skills/_research/VALUES.md) | The order when two goods conflict, and the escape hatch |
| [`skills/_research/HANDOFF.md`](skills/_research/HANDOFF.md) | What passes between phases, including loop-back triggers |
| [`skills/_research/OPERATIONAL.md`](skills/_research/OPERATIONAL.md) | Output language, density, reproducibility, the effort budget, and the journal |
| [`skills/_research/ROUTING.md`](skills/_research/ROUTING.md) | Guidance. Which phase owns the call, and the family invariants |
| [`skills/_research/REPORT.md`](skills/_research/REPORT.md) | What a person reads: when a run speaks, what ends it, who owns the terminal answer, size and strength |

## Layout

```
research-skills/
├── README.md
├── Makefile
├── research-registry/            # budgets, boundaries, routes, delivered blocks
├── research-tools/               # validate · test_validate · figures_check · test_figures ·
│                                 # test_hook · test_engine · test_render · test_make ·
│                                 # render · refute · engine · githooks/
└── skills/
    ├── _research/                # contracts in force on every run
    └── research-<phase>/
        ├── SKILL.md              # Owns / Before starting / Decide first /
        │                         # Always·Never / Verify with / Done when
        ├── _research -> ../_research
        ├── registry  -> ../../research-registry
        ├── playbooks/            # judgement. Budgeted, and must not rot
        └── reference/            # what goes stale. No line budget, dated instead
```

Chain artifacts live in the host project under `.research/<slug>/`, declared as
external so the path checker does not read them as references into this repo.

## Working on it

Needs Python 3 with PyYAML (`pip install pyyaml`), `make` and `git`.

```sh
make check      # the rules, proof every rule and tool check still fires, the figures;
                # CI runs these and also fails when `make render` would change a file
make render     # after editing anything in research-registry/delivered/
make hooks      # run the rules on every commit
```

## Installing

```sh
make link                                    # every installed host: claude, codex, agy
make link CLAUDE_DIR=/abs/path/.claude/skills # one place; a relative path resolves in this repo
```

A host is linked only when its home (`~/.claude`, `~/.codex`, ...) already
exists; `make status` shows what was linked. Each `research-*` skill is linked individually and reaches its contracts through
the symlinks inside it. Nothing un-prefixed is copied anywhere — a plain `cp` of
one skill directory used to leave a dangling shared link, and **a dangling
shared link silently removes every binding contract with no error**.

## What this does not guarantee

- **`allowed-tools` is one CLI's mechanism.** Where a tool grant is not
  enforced, the `Never` lines are discipline and nothing more
- **Nothing here enforces the data-not-instruction invariant.** It is the most
  important rule in the set and the only defence is that it is delivered into
  every skill and stated again in the retrieval one
- **The fixtures do not model how a model chooses.** They catch a missing or
  duplicated signal, not a misroute
- **No skill can run the other-engine checker.** No permission class grants a
  shell, so the `fill-the-gap` loop's `checker: other-engine` is run by a person
  with `make refute`; a check nobody ran is unchecked, not passed
- **`Verified:` dates are not checked against anything.** A stale reference file
  with a fresh date passes
- **No rule checks that a tier was honestly assigned, or that a label matches its
  ledger row.** The contract says both; whether the run honoured them is read by
  a person

## The published overview

[`docs/index.html`](docs/index.html) is a generated page — every figure on it is
read off this repository, the way `make figures` recomputes what the reference
layer states. **Do not edit it by hand**: `tools/pages.py` in the `agent-toolkit`
repository writes it, `tools/pages.py --check` fails when it is behind, and
`.github/workflows/pages.yml` here only publishes what is committed.

