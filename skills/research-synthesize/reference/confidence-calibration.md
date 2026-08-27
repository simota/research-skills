<!-- research:deferred -->
# Confidence Calibration

Purpose: Assigning confidence, running sensitivity, writing gaps.
Read when: assigning confidence, running sensitivity, writing gaps
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — the composition table below is re-checked by `make figures` on every run:
all 16 pairs defined, all 64 triples associative, monotone, never-rising, `Unknown` absorbing, and
agreeing with this page's own `Medium` x `Medium` = `Low`. The ceiling table above it is a
convention and carries no check.

Confidence attaches to a claim, not to a source, and never exceeds what tier x independence x
directness permits. Labels are defined in `_research/CONTRACT.md` — those four and no others; this
file is how to apply them, and is the single authority on the ceiling table.

## Assignment procedure

Per claim:

1. List supporting sources with tiers; drop correlated ones to a single entry
2. List contradicting sources with tiers
3. Check directness: does the evidence measure *our* question's conditions?
4. Take the ceiling from the table below
5. Lower it for: unresolved contradiction, abstract-only reads, extrapolation beyond measured
   range, single-origin corroboration, staleness
6. Never raise it for: intuitive plausibility, volume of weak agreement, alignment with the prior
7. Never exceed a `CEILING` recommended by `research-appraise`

| Support | Contradiction | Ceiling |
|---------|---------------|---------|
| >=2 independent `P1`/`P2` | none | `High` |
| 1 `P1`/`P2` | none | `Medium` |
| >=2 independent `P3` | none | `Medium` |
| 1 `P3` | none | `Low` — `Medium` needs a second independent `P3`, or one `P1`/`P2` |
| Any volume of `P4`/`P5` | none | `Low` |
| Anything | unresolved genuine contradiction | `Low` or `Unknown` |
| Nothing addresses it | — | `Unknown` |

Supporting `P3`s alongside an `P1`/`P2` do not raise the ceiling; contradicting ones must be
explained before `Medium` stands.

## Chained inference

Confidence falls along a chain and never holds. `_research/CONTRACT.md` allows no percentages, so
"multiply" is an operation on four ordered labels rather than on numbers — which means it has to be
written down, or every reader performs a different one.

| ∘ | `High` | `Medium` | `Low` | `Unknown` |
|---|---|---|---|---|
| `High` | `Medium` | `Low` | `Low` | `Unknown` |
| `Medium` | `Low` | `Low` | `Low` | `Unknown` |
| `Low` | `Low` | `Low` | `Low` | `Unknown` |
| `Unknown` | `Unknown` | `Unknown` | `Unknown` | `Unknown` |

Compose the hops pairwise, in any order. The table is built so the order cannot matter, and
`make figures` checks that it still holds:

- **it never rises** — no cell is stronger than either of its inputs
- **it falls** — two hops that both settle something land strictly weaker than the weaker
  of them, unless that is already `Low`. "Never rises" does not say this, and a table
  where `High` ∘ `High` is `High` passes every other property while contradicting the
  first line of this section
- **it is monotone** — weakening one hop never strengthens the conclusion
- **it is associative** — `(a ∘ b) ∘ c` equals `a ∘ (b ∘ c)` for all 64 triples, so a chain has one
  answer rather than one per bracketing
- **`Unknown` absorbs** — a hop that settles nothing settles the chain
- **`Low` is the floor, not `Unknown`** — chaining suggestive links keeps the conclusion
  suggestive. Only an `Unknown` hop makes a chain `Unknown`, because "the evidence does not settle
  this" is a claim about the evidence, not a thing weak evidence decays into

**The six properties constrain the table; they do not pin it.** A table where `High` ∘ `High`
is `Low` satisfies every one of them — checked, it passes. `Medium` is a decision, not a
derivation: sending two act-on-this hops straight to `Low` collapses the scale at the first
composition and the labels stop distinguishing anything afterwards. What `make figures`
guarantees is that the table stays *consistent*, not that this is the only consistent table.

Consequences worth stating plainly: two `High` hops give `Medium`, not `High`. Two `Medium` hops
give `Low`, which is the rule this table was built to satisfy. Beyond two hops the label stops
discriminating — everything is already `Low` — so **say the hop count** rather than leaning on the
label. Long chains are where research fabricates its most confident errors, and the label alone
will not warn anyone.

## Sensitivity check

Required on every conclusion:

```
Load-bearing source: S-004 (P2). If its benchmark method is flawed, C-002 and the primary answer
both fall. Nothing else in the corpus independently measures this.
Robustness: one independent replication would move C-002 from Medium to High.
```

If a single source can overturn the conclusion, the conclusion is `Medium` at best regardless of
that source's tier. Naming the load-bearing source tells the reader exactly where to push.

## Gaps

A gap is not "more research needed". It is a named unknown with a named closing action:

```
GAP-1: No independent measurement of throughput under mixed workloads.
  Affects: C-002, C-005, the primary answer's scale claim.
  Closes with: a replication on <workload>, or vendor raw data if published.
  Searched: 3 query rounds, 2 channels — see corpus.md log rows 7-11.
```

The "searched" line matters. It separates "nobody has published this" from "we did not look".

## Prior vs. posterior

Close by comparing against the prior recorded in the brief:

```
Prior: X is the faster option (Medium).
Posterior: X is faster only under tuned configuration (Medium); at defaults Y wins (Medium).
Changed: the unconditional form of the belief. Confirmed: the tuned-case direction.
```

This is what tells the requester whether the research earned its cost — and it is only possible
because the prior was written down before searching.

## Calibration self-check

- Would I bet on this claim at the odds my label implies?
- Have I labelled anything `High` that rests on a single source?
- Have I labelled anything `Low` merely because it contradicts what I expected?
- Is every `Unknown` genuinely unresolved, rather than unresearched? If unresearched, say so.
- Does any claim in the ledger lack a source ID? If so, it is inference — label it.
