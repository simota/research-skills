<!-- research:contract -->
# Operational Defaults

Applies to every `research-*` skill.

## Output language

Follow the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`). Source
titles, quotations, URLs, identifiers, and technical terms stay in their original language —
never translate a quoted passage without marking it as a translation.

## Output density

The result's shape follows `_research/REPORT.md`. A `quick` chain answers with citations
inline and no assigned confidence label. A `standard` chain may finish with synthesis's
supported answer, conditions and gaps; it does not require a separate write-up. Audience-shaped
writing belongs to report, at the size requested. `deep` keeps the full chain artifacts under
`.research/<slug>/` when a workspace is authorised. A path alone is not the requested answer.

## Reproducibility

Any output that rests on retrieval must be re-runnable by someone else. That means the search log
(queries, sources, dates) is part of the deliverable, not scratch work. A conclusion whose
derivation cannot be retraced is an opinion.

Phases that do not retrieve — `research-scope`, an appraisal of a supplied source, a write-up from
an existing ledger — carry provenance instead: which artifact or prior search log the output rests
on. Never synthesise an empty search log to satisfy this rule.

## Effort budget

Honour the brief's budget or, without a brief, source's bounded entry plan (`_research/SIZING.md`).
Caps limit cost; the observable coverage/sufficiency rule determines whether retrieval is enough.
A cap hit with unmet coverage or evidence produces `PARTIAL`, with the next useful target named;
never quietly overspend, lower the bar, or treat budget exhaustion as success.

## Journal

Optional, off by default. When the user asks for continuity across sessions, append durable
findings to `.research/<slug>/log.md`:

`| YYYY-MM-DD | <skill> | <action> | <artifact> | <outcome> |`

Record insights and dead ends, not narration. A recorded dead end ("vendor benchmarks all trace
to the same 2023 whitepaper") saves the next pass more time than a recorded success.
