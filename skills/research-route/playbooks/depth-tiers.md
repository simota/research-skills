<!-- research:guidance -->
# Depth Tiers, Not Research

## Depth Tiers

| Tier | Trigger | Chain | Budget |
|------|---------|-------|--------|
| `quick` | Settled fact, single answer shape, low cost of error | `source -> appraise -> report` (no ledger; report traces to `S-nnn` and caps confidence at `Medium`) | 1-3 sources, 1 query round total |
| `standard` | Multi-part question, some contestation, reversible decision | `scope -> source -> appraise -> synthesize -> report` | 5-12 sources, 8 rounds total (2-3 per sub-question) |
| `deep` | High cost of error, contested field, landscape or comparison | Full chain + gap-fill loops | 15-40 sources, 3 per sub-question / 20 total |
| `vet` | A specific **source** to check | `appraise -> report` (+ `source` first for origin tracing) | 1-5 sources, 2 query rounds total |
| `verify` | A specific **claim** to check | `source -> appraise -> synthesize -> report` | 3-8 sources, 2 per sub-question / 5 total |
| `write` | Findings already exist | `report` | no retrieval |

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
