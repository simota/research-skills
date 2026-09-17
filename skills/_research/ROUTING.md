<!-- research:guidance -->
# Research Family Boundaries

The `research-*` family splits one research job into six owners. Each phase has exactly

**Boundaries are defined in `registry/capabilities.yaml`, not here and not in any skill's
description.** Each entry carries what a skill does, what it does not (`not:`, with where that
work goes instead), and the words that select it. Writing an exclusion into a description makes
every skill added rewrite its neighbours; keeping it in one file makes an addition cost O(1).
What follows is a reading of that file, plus the family invariants no registry can hold.

The chains that recur are in `registry/routes.yaml`, with their control structure. Where a stage
repeats until a condition holds, the entry carries the stopping condition, the judge, and a hard
cycle limit — and **the phase that wanted a claim may not certify its own support**.

one owner; a skill that finds itself doing another's job hands off instead of absorbing it.

| Skill | Owns | Does NOT own |
|-------|------|--------------|
| `research-scope` | The question. Decomposition, out-of-scope lines, success criteria, the stopping **rule** and the caps it sets, effort budget. | Running searches, judging whether the rule has been met, judging sources, writing prose. |
| `research-source` | Retrieval. Query design, source-type selection, snowballing, dedup, the search log, and **judging whether the capture/saturation condition has been met**; bounded entry plan when no brief exists (`_research/SIZING.md`). | Reframing an unsettled question or relaxing supplied caps (→ scope), assigning provenance tiers or excluding sources (→ appraise), deciding what sources *mean* (→ synthesize). |
| `research-appraise` | Per-source judgment. Provenance, method quality, bias, recency, independence, evidence grade, include/exclude. May **recommend** a confidence ceiling. | Assigning confidence labels (→ synthesize), cross-source reconciliation (→ synthesize), finding more sources (→ source). |
| `research-synthesize` | Cross-source claims. Claim extraction, agreement/contradiction matrix, weight of evidence, gaps, confidence. | Grading individual sources (→ appraise), audience-shaped prose (→ report). |
| `research-report` | Communication. Audience shaping, structure, citation rendering, limitations, executive summary. | Forming new claims not present in the synthesis ledger. |
| `research-route` | Orchestration. Request classification, minimum viable chain, budget enforcement, aggregation. | Doing any phase's work itself. |

## Family-wide invariants

1. **Every claim traces to a source ID.** IDs are minted once by `research-source` (`S-001`) at
   retrieval time and never renumbered downstream. Claims are minted by `research-synthesize`
   (`C-001`).
2. **No skill invents evidence.** If a needed source does not exist, that is a *gap* — report it,
   do not reason around it.
3. **Assigned confidence is stated, never implied.** The four labels in `_research/CONTRACT.md`
   are the whole vocabulary; an unassigned label is not `Unknown` or an advisory ceiling.
4. **Only `research-synthesize` assigns a confidence label.** `research-appraise` may recommend a
   ceiling (`CEILING: Low`); it does not set the label, because a label set before cross-source
   reconciliation becomes an unremovable floor under invariant 5.
   On a chain with no synthesis (`quick`, `vet`), no skill assigns a confidence label. Report
   the source-bound answer and "no synthesis pass; confidence unassigned". Reconciliation or
   inference not established upstream must go to synthesis, not to an implicit report verdict.
5. **Uncertainty flows forward undiluted.** A `Low`-confidence claim in synthesis must still read
   as `Low`-confidence in the report. Downstream skills may not upgrade confidence.
6. **Evidence tiers belong to `research-appraise`.** `research-source` records what a document *is*
   (type, provenance, read depth, red flags); it does not grade or exclude.
7. **The stopping rule is set before searching, not after.** Scope writes the brief; without
   one, source records the bounded entry plan in `_research/SIZING.md`. Hard caps are not sufficiency.

## Outside the family

Route out when the task is primarily:

- reading or tracing *this repository's own code*: a codebase-comprehension skill, not research
- writing product/marketing copy from known facts: a writing skill
- deciding what to build from research already done: a product/prioritisation skill
- executing an experiment rather than reviewing evidence about one: an experimentation skill

Research ends where advocacy begins. These skills describe the evidence; they do not argue a
predetermined position, and they do not make the decision the evidence informs.
