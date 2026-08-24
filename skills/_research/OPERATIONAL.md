<!-- research:contract -->
# Operational Defaults

Applies to every `research-*` skill.

## Output language

Follow the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`). Source
titles, quotations, URLs, identifiers, and technical terms stay in their original language —
never translate a quoted passage without marking it as a translation.

## Output density

The shape, the order and the ceiling of what a person reads are `_research/REPORT.md` — one
place, delivered into every skill. What this file adds is the size of the **deliverable** behind
it: a `quick` chain produces its answer and citations inline, `standard` a one-to-two-page
write-up with an evidence table and a gaps section, `deep` the full chain artifacts under
`.research/<slug>/`. **Those are the write-up, never the surface report.**

## Reproducibility

Any output that rests on retrieval must be re-runnable by someone else. That means the search log
(queries, sources, dates) is part of the deliverable, not scratch work. A conclusion whose
derivation cannot be retraced is an opinion.

Phases that do not retrieve — `research-scope`, an appraisal of a supplied source, a write-up from
an existing ledger — carry provenance instead: which artifact or prior search log the output rests
on. Never synthesise an empty search log to satisfy this rule.

## Effort budget

`research-scope` sets a budget (source count ceiling, iteration ceiling, stopping rule). Honour
it. When the budget is hit before saturation, stop and report `PARTIAL` with what a further pass
would target — do not quietly overspend, and do not quietly under-deliver.

## Journal

Optional, off by default. When the user asks for continuity across sessions, append durable
findings to `.research/<slug>/log.md`:

`| YYYY-MM-DD | <skill> | <action> | <artifact> | <outcome> |`

Record insights and dead ends, not narration. A recorded dead end ("vendor benchmarks all trace
to the same 2023 whitepaper") saves the next pass more time than a recorded success.
