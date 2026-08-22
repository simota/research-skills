<!-- research:contract -->
# Operational Defaults

Applies to every `research-*` skill.

## Output language

Follow the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`). Source
titles, quotations, URLs, identifiers, and technical terms stay in their original language —
never translate a quoted passage without marking it as a translation.

## Output density

Lead with the answer, then the evidence. No preamble, no restatement of the request, no closing
summary of what was just delivered. Tables for anything with more than three parallel items.

Length envelopes:
- Quick answer: <=10 lines, 1-3 sources, confidence label required
- Standard: 1-2 pages, evidence table, gaps section
- Deep: full chain artifacts under `.research/<slug>/`

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
