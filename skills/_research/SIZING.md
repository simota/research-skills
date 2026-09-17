<!-- research:contract -->
# SIZING — how much research the question is worth

**Over-researching a settled fact is a failure of the same weight as
under-researching a contested one.** Both come from choosing the tier for
comfort, so the tier is read off the question and declared before any retrieval.

## Depth tiers

| Tier | The question is | Chain | Budget shape |
|---|---|---|---|
| `quick` | Settled, but somebody wants a source | source → appraise → report | A handful of sources, one round |
| `standard` | Real, with a decision behind it | scope → source → appraise → synthesize | Bounded rounds per sub-question |
| `deep` | Contested, consequential, must survive challenge | the full chain, ending in a report | Caps set explicitly in the brief |

**A no-synthesis chain assigns no confidence label.** `quick` and `vet` report a
source-bound answer and "no synthesis pass; confidence unassigned". An appraisal
ceiling is advice, not a label. New reconciliation or inference belongs to synthesis.

## One budget, held across the chain

Not one per phase. The four caps — total sources, total query rounds, rounds per
sub-question, full reads — are named identically everywhere and consumption is
reported at every handoff.

**Never begin retrieval without both round caps.** Use the brief when present; do not
silently repair or relax its limits. Without one, source first records an inline retrieval plan:
exact requested target(s) as sub-questions, required version/date or source type, observable
capture/coverage condition, and all four caps. Default to the existing quick envelope: at most
3 sources, 3 full reads, 1 round per sub-question, 2 rounds total; tighter supplied caps prevail.
These are maxima, not quotas. A multi-question request can exhaust this small default and return
`PARTIAL`; it does not gain a bigger budget automatically. Unsettled question/criteria need scope,
not invented priors, exclusions or evidence grades. No search is needed to invent this plan.

## Stop when the rule says so, not when it feels done

The brief or source's bounded entry plan carries an observable stopping rule. For a record
lookup, capture the relevant passage at the requested version/as-of, including applicable
conditions or amendments. Corpus-only uses the requested coverage/read-depth condition; source
does not certify truth or assign tiers. Appraisal checks the evidence bar for a findings answer.
Sufficiency may stop retrieval before a cap; a cap stops it even when insufficient. Unmet coverage
or evidence remains `PARTIAL` (or `BLOCKED` if no work could proceed), never `DONE` merely at a cap.

## When a dialogue is required first

For an unsettled question, these require dialogue when they change the decision or corpus.
An exact record or corpus request uses the bounded entry plan above; an unstated downstream
evidence grade alone is not a reason to invent a framing interview.

- The **answer shape** is not determined — a number, a ranked list, a yes/no with
  conditions, a mechanism, a landscape map. Get it wrong and the corpus is wrong
- What counts as answered does not fit in one sentence
- The **evidence bar** is implied but unstated. "Reliable sources" is not a bar;
  a tier is
- The request carries a word with no achievement condition — "look into",
  "get a sense of", "see what is out there"
- A term in the question or the field carries two meanings, or one concept goes
  by two names, and the host's glossary does not settle it

**Reading to find out is not executing**, and neither is retrieval: a search run
to work out what the question is has already spent budget on a question nobody
settled. Never open a dialogue over a single settled fact.

## Terms — one name per concept, one concept per name

The host's glossary is `.agents/glossary.md` when it exists. Read it before the
brief is settled and write with its names only — sub-questions, claims, report
alike. A term the work has to coin goes into the brief's `terms`, and at
`standard` or above it is proposed in the dialogue rather than invented on the
way.

**An ambiguous or inconsistent term is never resolved by a silent choice.**
Two meanings for one word, or two names for one concept, is a question
(`_research/REPORT.md`): one question, with the default named — the spelling
the sources and the host already use most. The answer lands in `terms`, travels
in `carried`, and is appended to the glossary as `term · means · not to be
called`, so the next chain inherits the decision rather than the ambiguity. A
`standard` run may create the glossary for its first settled term; a `quick`
one never does — it marks what it found `OUT-OF-SCOPE` and moves on.

## Constraints do not loosen mid-run

The bar, the caps, the stopping rule and the out-of-scope lines are fixed at the
start. About to break one — stop and hand back. **A bar quietly lowered to let a
claim through is the most expensive kind of false report**, because the citation
still looks like a citation.
