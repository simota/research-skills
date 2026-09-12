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

**A `quick` chain caps its confidence.** No cross-source reconciliation ran, so
independence was never tested and the top label is unavailable to it by
construction — not as a penalty, but because the chain did not do the work the
label claims.

## One budget, held across the chain

Not one per phase. The four caps — total sources, total query rounds, rounds per
sub-question, full reads — are named identically everywhere and consumption is
reported at every handoff.

**Never dispatch retrieval on a brief that omits either round cap.** A search
with no round cap does not end; it is abandoned, and what it abandoned is
invisible in the output.

## Stop when the rule says so, not when it feels done

The brief carries a stopping rule, and it is the thing that ends retrieval. The
alternative — stopping when the answer feels supported — stops earliest exactly
where the prior was strongest, which is where research is least useful.

## When a dialogue is required first

Before executing, any of these makes the dialogue mandatory:

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
