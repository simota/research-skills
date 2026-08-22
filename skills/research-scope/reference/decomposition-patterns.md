<!-- research:deferred -->
# Decomposition Patterns

Purpose: Splitting into sub-questions — comparative, causal, landscape, claim-check patterns.
Read when: splitting into sub-questions — comparative, causal, landscape, claim-check patterns
Verified: 2026-08-21 — no automated check.

Sub-questions must be **independently answerable** (answering one does not require assuming
another's answer) and **jointly sufficient** (answering all of them answers the primary question).
Test both before handing off: overlap doubles search cost and double-counts evidence downstream;
insufficiency guarantees a `PARTIAL` finish.

## Comparative (A vs B vs C)

Wrong order: find candidates, then notice what distinguishes them. The first candidate found sets
the criteria and everything after is judged on its terms.

Right order:
1. **Criteria** — what would make one option better, derived from the decision, not from the options
2. **Weights** — which criteria are disqualifying, which are tiebreakers
3. **Candidate set + inclusion rule** — what makes something a candidate at all
4. **Per-criterion evidence** — one sub-question per criterion, applied uniformly to every candidate
5. **Switching cost** — what the comparison ignores (migration, lock-in, team familiarity)

Rule: never let a candidate contribute a criterion that only it satisfies. That is a feature list
masquerading as an evaluation.

## Causal ("why does X happen")

1. What exactly is X, and how is it measured? (definition and instrument)
2. When did X start, and what changed then? (temporal bracketing)
3. What are the candidate mechanisms, from most to least mundane?
4. What evidence distinguishes them from each other?
5. What would we see if the leading explanation were false?

Enumerate mundane explanations first — measurement change, composition shift, seasonality,
reporting artefact — before interesting ones. Most surprising findings are measurement artefacts.

## Landscape ("what exists / who is doing X")

1. **Inclusion criteria** — what counts as being in the landscape, what is adjacent-but-out
2. **Axes** — 2-3 dimensions to place entrants on, chosen before enumeration
3. **Enumeration sources** — where a complete-enough list can come from (registries, indexes,
   awards, funding databases, package repositories), not ad-hoc search
4. **Per-entrant facts** — the same small fact set for everyone; resist deep-diving the first few
5. **Coverage check** — what class of entrant this method would systematically miss

The coverage check is the deliverable most landscape research omits and most needs: search-driven
enumeration systematically misses the unmarketed, the non-English, and the recently launched.

## Claim check ("is it true that…")

1. Atomise: split the claim into separately checkable assertions. "X is 10x faster and cheaper to
   run" is two claims, usually with different answers.
2. For each atom: what would count as confirming evidence, what as disconfirming
3. Trace to origin: who said it first, on what basis — most repeated claims trace to one source
4. Check the conditions: benchmarks, populations, versions, and time windows under which it holds
5. Check the negation: has anyone credible contested it, and on what grounds

## Feasibility ("can we do X")

1. Has anyone done it? (existence proof, closest analogue)
2. Under what conditions did they do it? (scale, constraints, resources)
3. Where do our conditions differ, and which differences are load-bearing?
4. What failed for those who tried and did not succeed? (survivorship correction — actively search
   for failures; success stories are over-published)
5. What are the irreducible prerequisites?

## Dependency ordering

Order sub-questions so that no question's search depends on a later question's answer. A common
correct order:

```
definitional -> existence -> measurement -> comparison -> causal -> projective
```

Mark blocking dependencies explicitly (`Q3 blocked-by Q1`). Independent sub-questions can be
searched in parallel and should be marked as such — that is what lets a chain fan out.

## Sizing

3-7 sub-questions for a standard investigation. Fewer than 3 usually means the decomposition did
not happen. More than 7 means the primary question is really two questions — split it and say so
rather than delivering a brief nobody can execute.
