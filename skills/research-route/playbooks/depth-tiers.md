<!-- research:guidance -->
# Depth Tiers, Not Research

## Depth Tiers

| Depth | Trigger | Chain | Budget |
|------|---------|-------|--------|
| `quick` | Settled fact, single answer shape, low cost of error | `source -> appraise -> report` (no ledger; report traces to `S-nnn`, confidence unassigned) | Entry-plan default: ≤3 sources, ≤2 rounds total |
| `standard` | Multi-part question, some contestation, reversible decision | `scope -> source -> appraise -> synthesize` — the chain in `registry/routes.yaml`; add `report` only when a write-up was asked for | 5-12 sources, 8 rounds total (2-3 per sub-question) |
| `deep` | High cost of error, contested field, landscape or comparison | Full chain + gap-fill loops | 15-40 sources, 3 per sub-question / 20 total |

Three bounded asks are chain patterns, not depths (`reference/chain-patterns.md`). With no brief
they run on the entry-plan default; a bigger budget needs scope to write one.

| Pattern | Trigger | Chain |
|------|---------|-------|
| `vet` | A specific **source** or record to check | `source -> appraise -> report` — the route in `registry/routes.yaml`; source may be a stated skip when a retrieval handoff is supplied |
| `verify` | A specific **claim** to check | `source -> appraise -> synthesize -> report` |
| `write` | Findings already exist | `report` — no retrieval |

Depth comes from the cost of being wrong, not from how the request was phrased. "Quick question"
before a one-way-door decision is a `standard` at minimum — say so and confirm.

## Not Research

Route these out rather than running the chain:

| Ask | Why it is not research | Where it goes |
|-----|------------------------|---------------|
| "Read our codebase and explain X" | Internal comprehension, not external evidence | A codebase-comprehension skill |
| "Write a post about X" | Communication from known facts | A writing skill |
| "Build a prototype to test X" | Experimentation, not evidence review | An implementation or experiment skill |
| "Decide whether we should do X" | A decision; research informs it but cannot make it | Return with the evidence, decision to the user |
| "Make the case for X" | Advocacy | Say plainly that research cannot be pre-committed to a conclusion; offer the neutral question |

A request that is half research is split: run the research half, hand back the other half named.
