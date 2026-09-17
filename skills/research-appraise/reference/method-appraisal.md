<!-- research:deferred -->
# Method Appraisal

Purpose: Assessing studies, benchmarks, surveys, and statistical claims.
Read when: assessing studies, benchmarks, surveys, and statistical claims
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

How a source knows determines what its claim is worth. Read the method section before the
conclusion — reading in the other order anchors the assessment to the finding.

## Universal questions

1. What exactly was measured, and with what instrument?
2. On what, how many, selected how?
3. Compared against what?
4. What was held constant, and what varied?
5. Could the result have been produced by something other than the stated cause?
6. Has anyone reproduced it?

An empirical measurement that cannot answer 1-3 is `P4` regardless of presentation. A literal
authoritative-record claim is checked by the bounded case in `_research/CONTRACT.md`, not by
inventing an experimental method for a specification or published term.

## Benchmarks and performance claims

Missing any of these makes the number unusable — say which is missing rather than repeating it:

- Baseline: what is it faster/cheaper/better *than*, at which version, on which hardware
- Workload: what was run; synthetic or representative; tuned for which side
- Configuration: was the comparison target configured competently, or at defaults
- Variance: single run or distribution; percentiles or averages
- Who ran it: the vendor of the winning entry is not a neutral referee

`40% faster` with no baseline is marketing in numeric form. `p50 latency 12ms -> 7ms on <workload>,
<hardware>, n=20 runs, code linked` is a measurement.

## Studies and experiments

| Check | Weak signal | Strong signal |
|-------|-------------|---------------|
| Sample | Self-selected, convenience, tiny | Random or fully enumerated, pre-registered size |
| Control | None, or historical comparison | Concurrent control, randomised assignment |
| Blinding | Outcome assessed by the interested party | Independent or blinded assessment |
| Pre-registration | Hypothesis stated after seeing data | Pre-registered protocol and endpoints |
| Effect | Statistically significant but tiny | Effect size reported with intervals, practically meaningful |
| Replication | One study, novel finding | Independently replicated |

A novel, surprising, single-study finding is the profile most likely not to replicate. Treat it as
`Medium` at best regardless of the venue.

## Surveys

- Who was asked, how were they reached, what was the response rate (low response = self-selection)
- Question wording — leading questions manufacture their answers
- Self-report vs. observed behaviour; the two diverge systematically
- Who sponsored it, and does the result favour the sponsor's product
- Sample frame: a survey of a vendor's own customers describes that vendor's customers, nobody else

## Statistical red flags

| Flag | What it hides |
|------|---------------|
| Percentage with no denominator | "Grew 300%" from 1 to 4 |
| Relative risk without absolute | 50% increase on a 0.02% base rate |
| Average without distribution | A few extreme values driving the mean |
| Truncated or dual y-axis | Trivial differences rendered dramatic |
| Cherry-picked window | A trend that reverses when the range extends |
| Missing base rate | Accuracy claims that ignore prevalence |
| Composite index | Weights chosen after the fact to produce a ranking |
| p just under 0.05, many outcomes | Multiple comparisons, unreported |
| Survivorship framing | Ten successes; the failures were never counted |

## Documentation, specs, and code as evidence

- Official and vendor docs are `P1` for *what the product is documented to do* and `P4` for any
  comparative or promotional claim — the same page, two tiers, per `_research/CONTRACT.md`
- Source code is `P1` for behaviour, but only at a specific commit — pin the SHA
- Specs are `P1` for requirements; check for errata, amendments, and the version in force
- Docs describe intent; issue trackers describe reality. Reading only one gives half the picture

## What would raise the grade

Always record it. "Would be `P2` with an independent replication" or "would be `P1` if the raw
response data were published" tells the next pass exactly what to look for, and tells the reader
precisely how uncertain the current answer is.
