<!-- research:deferred -->
# Chain Patterns

Purpose: Choosing the chain, handling loops, managing partials.
Read when: choosing the chain, handling loops, managing partials
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

## Standard chains

| Pattern | Chain | Use |
|---------|-------|-----|
| Lookup | `source -> appraise -> report` | Documented fact, primary source exists, low error cost. No ledger: report traces to `S-nnn` and cannot exceed `Medium` |
| Vet | `appraise -> report` | A supplied source to check |
| Trace | `source -> appraise` | "Where did this source come from and is it sound" |
| Verify | `source -> appraise -> synthesize -> report` | "Is this claim true" — claim truth needs cross-source reconciliation, not just source quality |
| Standard | `scope -> source -> appraise -> synthesize -> report` | The default for real questions |
| Deep | Standard + gap-fill loops to saturation | High error cost, contested field |
| Reconcile | `appraise -> synthesize -> report` | A corpus already exists |
| Write-up | `report` | The ledger already exists |

Never insert a phase because the chain looks short. Insert it because its contract is needed.

## Loop triggers

Four trigger kinds in three routing groups. Each is named by the phase that raises it.

All four arrive as `next_action: LOOP_BACK` with `trigger.kind` set (`_research/HANDOFF.md`).

| `trigger.kind` | Raised by | Goes to |
|----------------|-----------|---------|
| `BELOW_BAR` | `research-appraise` | `research-source` |
| `GAP_FILL` / `UNSUPPORTED_CLAIM` | `research-synthesize` | `research-source` |
| `REVISE_SCOPE` | `research-synthesize` | `research-scope` |

**One global counter, capped by `max_cycles` in `registry/routes.yaml`, of which at most 1 may be
`REVISE_SCOPE`.** There are no per-trigger allowances — three counters would license three times
the cap inside a single rule.

A second loop that returns the same sources means the evidence does not exist. Stop and report
`Unknown` — that is the finding, and looping a third time only spends budget confirming it.

A `REVISE_SCOPE` loop rewrites the question. Confirm with the user first: they asked the original
question for a reason, and substituting an easier one without saying so is the quiet failure this
family exists to prevent.

## Budget across phases

One budget, held across the chain, checked at every handoff:

```
Allotted: source_total_cap 12, query_rounds_total_cap 8, query_rounds_per_subquestion_cap 3, full_reads_cap 6.
After source: 9 retrieved, 5 rounds. After GAP_FILL loop 1: 12 retrieved, 8 rounds — caps reached.
```

Both round caps bind. Per-sub-question alone lets seven sub-questions run 21 rounds inside a
"2-3 rounds" budget; total alone starves whichever sub-question is searched last.

At the cap: stop retrieval, synthesize what exists, and report `PARTIAL` with the next query that
would have run. Do not silently overspend, and do not silently under-deliver by stopping early
without saying so.

## Parallelism

Independent sub-questions can be retrieved concurrently — `research-scope` marks which are
independent and which are `blocked-by` another. Appraisal is per source and parallel by nature.
Synthesis is a barrier: it needs the whole graded corpus before it can map contradictions, because
the contradiction matrix is defined across sources.

## Escalation timing

Surface a blocking question the moment a phase raises it. A blocking question delivered at the end
of the chain has already wasted every phase that ran after it. Non-blocking questions ride along in
the handoff and land in the report's limitations.

## Aggregation

Assembling the deliverable, verify:

1. Source IDs are unchanged from `research-source`; claim IDs unchanged from `research-synthesize`
2. Confidence labels match the synthesis exactly — nothing was upgraded in transit
3. Every phase's `gaps` appear in the final output (this is the one that silently fails)
4. Excluded sources are not cited anywhere in the body
5. Budget consumed vs. allotted is reported, in scope's units
6. `research-report` emitted a terminal handoff — the chain's status comes from it, not from inference
7. Status is `COMPLETE` only if every sub-question met its bar; otherwise `PARTIAL` with specifics

## Failure modes

- **Ceremony** — running all five phases on a lookup. Costs budget, adds nothing.
- **Under-run** — a confident answer to a contested question from three ungraded sources.
- **Loop churn** — repeated gap fills returning the same corpus.
- **Late escalation** — a blocking question raised at assembly.
- **Gap evaporation** — unknowns lost during aggregation; the deliverable reads more complete
  than the research was.
