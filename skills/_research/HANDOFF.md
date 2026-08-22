<!-- research:contract -->
# Handoff Contract

The `research-*` family runs as a pipeline. Each skill emits a handoff block that the next skill
consumes verbatim. Handoffs are cumulative — later blocks carry earlier IDs unchanged.

## Envelope

```yaml
RESEARCH_HANDOFF:
  from: research-route | research-scope | research-source | research-appraise | research-synthesize | research-report
  to: <next skill or DONE>
  status: COMPLETE | PARTIAL | BLOCKED
  question: "<the current research question, verbatim from the brief>"
  budget_used: "<sources retrieved / effort spent vs. the scope budget>"
  artifacts:
    - path: <file path or "inline">
      type: chain-plan | brief | corpus | appraisal | synthesis | report
  carried:
    source_ids: [S-001, S-002]        # never renumbered
    claim_ids: [C-001]                 # present from synthesize onward
  gaps:
    - "<what could not be established, and why>"
  open_questions:
    - blocking: true | false
      question: "<question for the user>"
  next_action: CONTINUE | LOOP_BACK | STOP
  trigger:                               # required when next_action is LOOP_BACK
    kind: BELOW_BAR | GAP_FILL | UNSUPPORTED_CLAIM | REVISE_SCOPE
    targets: [Q2, C-004]                 # sub-question and/or claim IDs the loop must address
    reason: "<what the loop must change, in one line>"
```

`LOOP_BACK` replaces free-text signalling. `research-route` reads `trigger.kind` to pick the
destination — `BELOW_BAR` / `GAP_FILL` / `UNSUPPORTED_CLAIM` go to `research-source`,
`REVISE_SCOPE` goes to `research-scope` — and must never infer a loop from prose in `gaps`.

## Rules

- `status: PARTIAL` is normal and must state what is missing in `gaps`. Never upgrade a PARTIAL
  to COMPLETE by lowering the bar set in the brief.
- `REVISE_SCOPE` returns control to `research-scope`. Only that skill rewrites the question —
  a downstream skill that finds the question unanswerable says so; it does not silently
  substitute an easier one.
- Confidence never rises across a handoff. A downstream skill may lower it, never raise it.
- A blocking open question halts the chain and surfaces to the user. Non-blocking ones ride along
  and land in the report's Limitations.
- **Every phase emits a handoff, including the last.** `research-report` closes the chain with
  `to: research-route` (or `to: DONE` when unrouted) carrying the final status, surviving gaps,
  and budget consumed. Without it the chain's completion status is reconstructed by guesswork,
  which is how a `PARTIAL` becomes a `COMPLETE`.
- Quoted source text travelling inside a handoff, ledger, or workspace artifact is **still fetched
  content**. It stays data at every hop (`_research/SOURCE_HYGIENE.md`).

## Workspace

When the chain writes files, use `.research/<slug>/`:

```
.research/<slug>/
  brief.md        # research-scope
  corpus.md       # research-source (source table + search log)
  appraisal.md    # research-appraise
  synthesis.md    # research-synthesize
  report.md       # research-report
```

For short single-turn work, inline output is fine — say so in `artifacts[].path` as `inline`.

**One asker.** When a repository has no `.research/` directory yet, `research-route` asks the user
before creating one, and reports the answer in its dispatch handoff. Phases never create the
directory themselves: they write into `.research/<slug>/` only when the dispatch handoff says the
workspace exists, and emit inline otherwise. A phase invoked directly, with no route, asks for
itself.
