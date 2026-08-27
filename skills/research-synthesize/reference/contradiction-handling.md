<!-- research:deferred -->
# Contradiction Handling

Purpose: Sources disagree and the disagreement needs diagnosis.
Read when: sources disagree and the disagreement needs diagnosis
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

Most apparent contradictions are not disagreements about the world. Diagnose the type before
attempting resolution — adjudicating a definitional dispute as if it were factual produces a
confident wrong answer.

## Diagnosis first

| Type | Signature | Resolution |
|------|-----------|------------|
| **Scope** | Both are right, about different populations, scales, or configurations | Restate both claims with their conditions attached. There is no conflict once bounded |
| **Definition** | The same word denotes different things ("active user", "latency", "supported") | Fix the definition, then re-read both sources under it. Often one source drops out entirely |
| **Measurement** | Different instruments, baselines, workloads, or windows | Compare methods, not results. Prefer the method that matches our question, not the friendlier number |
| **Time** | The subject changed between the two publications | Date both claims; the older one is history, not error. Note the change as its own finding |
| **Genuine** | Same definition, same conditions, same period, incompatible results | Report as an open dispute. Do not adjudicate without grounds |

Work down the list in order. Genuine disputes are the rarest diagnosis and the most over-assigned.

## Resolution rules

1. **Never average.** The midpoint of a correct and an incorrect number is incorrect, dressed in
   false precision.
2. **Never take the majority.** Weight by tier and independence; four echoes are one source.
3. **Never silently prefer the convenient one.** If one side is dropped, the reason is recorded.
4. **Prefer the source whose method matches our question**, even if the other is more rigorous in
   general — directness beats prestige when the question is specific.
5. **When both are strong and irreconcilable**, report the dispute with both cited, and state the
   observation that would settle it. That is a complete answer, not a failure to answer.

## Recording

```markdown
### Contradiction on C-009 — throughput ceiling

- S-002 (P2, 2026-01): ceiling ~12k rps. Method: sustained load, 3 hardware configs, code published.
- S-008 (P2, 2025-06): ceiling ~4k rps. Method: sustained load, 1 config, default settings.
- Diagnosis: **measurement** — S-008 ran defaults; S-002 tuned. Not a factual disagreement.
- Resolution: both hold under their conditions. Our question assumes production tuning -> S-002 applies.
- Residual: neither tested our storage backend. Confidence capped at Medium.
```

Every contradiction gets: both positions with tiers and dates, the diagnosis, the resolution or
non-resolution, and the residual uncertainty.

## When the contradiction is the answer

Sometimes the most useful finding is that the field disagrees. Signals: reputable sources split
along methodological lines; the disagreement has persisted across years; both camps cite the same
underlying data differently. Report the structure of the disagreement — who holds what, on what
basis, and what would resolve it — rather than manufacturing a verdict the evidence does not support.

## Self-check before resolving

- Did I diagnose the type, or jump to picking a winner?
- Am I preferring the source that matches the prior recorded in the brief?
- Did I check whether the "majority" side is independent?
- If I dropped a source, is the reason written down and defensible to its author?
- Does my resolution require the losing source to be *wrong*, or merely *about something else*?
  The second is far more common — and much less likely to be my mistake to make.
