<!-- research:deferred -->
# Request Classification

Purpose: Classifying depth, answer shape, and whether it is research.
Read when: classifying depth, answer shape, and whether it is research
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

Classify on three axes before choosing a chain. Getting depth wrong is the most expensive routing
error in both directions.

## Axis 1 — Cost of error (sets depth)

| Cost | Examples | Tier |
|------|----------|------|
| Trivial, reversible | Satisfying curiosity, background colour | `quick` |
| Moderate, reversible | Choosing a library for a prototype, sizing an effort | `standard` |
| High, hard to reverse | Architecture commitment, vendor contract, public claim, compliance posture | `deep` |
| Safety, legal, financial | Anything with regulatory or personal consequence | `deep`, and say the bar plainly |

This axis, not the request's phrasing, sets the tier. "Just a quick question — which database
should we standardise on?" is `deep`. Say so and confirm before proceeding.

## Axis 2 — Answer shape (sets the chain)

Quantity, ranking, binary, mechanism, landscape, trajectory (see `research-scope`). Rankings and
landscapes always need `research-scope` first — criteria and inclusion rules must precede
retrieval, or the first candidate found sets them.

## Axis 3 — Contestedness (sets whether appraisal is mandatory)

| Signal | Appraisal |
|--------|-----------|
| Documented fact from a primary source (spec, changelog, filing) | Optional |
| Commercial claim, vendor comparison, or benchmark | Mandatory |
| Active academic or practitioner debate | Mandatory |
| Recent, fast-moving, or heavily marketed topic | Mandatory |
| Anything where the answer favours someone financially | Mandatory |

## Is it research?

Research answers questions about the world from external evidence. It is **not**:

- Reading this repository or its history — that is codebase comprehension
- Producing content from facts already agreed — that is writing
- Running an experiment to generate new data — that is experimentation
- Choosing among options given the evidence — that is a decision, and it belongs to the user
- Building the case for a predetermined position — that is advocacy, and the family declines it

Half-research asks are split: run the research half, hand the other half back by name. Say which
half you are answering.

## Ambiguity resolution

When the tier is genuinely unclear, ask exactly one question — the decision behind the ask:

> "What are you deciding with this? That sets how deep the evidence needs to go."

The answer sets the tier, the evidence bar, and the format simultaneously. It is the highest-yield
question in the family, and the only one worth blocking on.

## Trigger ownership

`research-route` owns the bare research trigger — "research X", "look into Y", "what's the state
of Z". `research-scope` fires only when a brief is asked for explicitly ("sharpen this question",
"scope this") or when route dispatches to it. Two skills competing for the same opening phrase
resolve non-deterministically, and if scope wins the budget is never held across phases, which is
route's only job.

## Classification output

State it in one line before dispatching, so the user can redirect cheaply:

```
Classified: standard depth (reversible tooling choice), ranking shape, contested (vendor claims).
Chain: scope -> source -> appraise -> synthesize -> report. Budget: 10 sources, 3 query rounds.
```
