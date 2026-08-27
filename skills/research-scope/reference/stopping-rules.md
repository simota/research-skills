<!-- research:deferred -->
# Stopping Rules, Evidence Bars, and Budgets

Purpose: Setting saturation conditions, evidence bars, and budgets.
Read when: setting saturation conditions, evidence bars, and budgets
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

Open-ended research does not end on its own. The rule that ends it must be written before the
search starts, or the end condition becomes "when the researcher got tired" — which is neither
reproducible nor defensible.

## Saturation

The primary stopping condition. Saturation is reached when new sources stop changing the answer.

| Signal | Meaning |
|--------|---------|
| The last 3 **independent** sources (post-dedup, distinct origins) added no new claim, only corroboration | Saturated for this sub-question |
| New sources all trace back to sources already in the corpus | Saturated — and check for citation circularity |
| Each new source adds a claim but from a new domain/community | **Not** saturated; the corpus was too narrow |
| New sources contradict the emerging answer | Not saturated; contradiction must be resolved, not outvoted |

Saturation can never be declared below the sub-question's own corroboration requirement in the
evidence bar: three agreeing sources that collapse to one origin are one source, and one source is
not saturation.

Saturation is per sub-question, not per project. Cheap sub-questions saturate in two sources;
contested ones may never saturate — those get a budget cap and a `PARTIAL` status instead.

## Evidence bar

Set per sub-question from the cost of being wrong:

| Cost of error | Minimum tier | Corroboration | Target confidence |
|---------------|--------------|---------------|-------------------|
| One-way door, safety, legal, financial commitment | `P1`-`P2` | >=2 independent | High |
| Reversible but expensive to unwind | `P2`-`P3` | >=2 independent | Medium |
| Cheap to reverse, or directional input only | `P3`-`P4` | 1 acceptable | `Low` — `Medium` requires one `P1`/`P2` or two independent `P3` |
| Background colour | any | none | Low, labelled |

The target-confidence column is a **ceiling derived from `_research/CONTRACT.md`**, not an
independent setting. A bar that admits only `P4` sources cannot target above `Low`, whatever the
decision needs — if the decision needs more than the domain can supply, that is a finding for the
brief, not a number to raise here.

Calibrate against what the domain actually produces. Demanding peer-reviewed corroboration for a
question only vendors have ever measured guarantees a `PARTIAL`. Set the bar the domain allows and
record the ceiling: "no `P1`/`P2` evidence exists on this; best available is `P4` vendor data."

## Budget

Numeric, checkable mid-chain, expressed in units the chain can count:

```
source_total_cap:                  <= N retrieved across the whole chain
full_reads_cap:                    <= M read in full
query_rounds_per_subquestion_cap:  <= K before broadening or escalating
query_rounds_total_cap:            <= T across all sub-questions
escalation: on hitting any cap, report PARTIAL with the next best query — never silently continue
```

Both round caps are required. `K` alone lets a seven-sub-question brief run 21 rounds inside a
"2-3 rounds" budget; `T` alone starves the sub-questions searched last.

Rough calibration:

| Mode | Sources | Query rounds | Output |
|------|---------|--------------|--------|
| Quick answer | 1-3 | 1 per sub-question, 2 total | <=10 lines with confidence label |
| Standard | 5-12 | 2-3 per sub-question, 8 total | 1-2 pages with evidence table |
| Deep | 15-40 | until saturation, capped | Full chain artifacts |

Time is not a budget unit. "30 minutes" cannot be checked at step 4; "12 sources" can.

## Diminishing returns

Stop early — before the cap — when any of these hold:

- The answer has been stable across the last several sources and further work would only add
  citations to a settled claim
- The remaining uncertainty is `Unknown` in a way more sources cannot fix (nobody has published it)
- The cost of further search exceeds the value of the residual uncertainty to the decision
- The blocking uncertainty has moved from evidence to judgement — hand it back to the requester

## Failure to stop

Watch for these; each means the stopping rule is not being honoured:

- **Scope creep by discovery**: an interesting adjacent finding becomes a new sub-question. Log it
  in `gaps` as a future question; do not research it now.
- **Corroboration hoarding**: adding a 9th source for an already-`High` claim while another
  sub-question still sits at `Unknown`. Reallocate to the weakest sub-question, always.
- **Depth substitution**: reading one source exhaustively instead of finding a second independent
  one. Independence beats depth for confidence.
- **Search until agreement**: continuing until sources converge on the prior. Convergence produced
  by selective stopping is not evidence — it is the prior, restated.
