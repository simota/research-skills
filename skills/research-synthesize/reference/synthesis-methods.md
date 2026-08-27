<!-- research:deferred -->
# Synthesis Methods

Purpose: Extracting claims, building the matrix, tracing consensus to origins.
Read when: extracting claims, building the matrix, tracing consensus to origins
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

Summarising is describing what each source says. Synthesis is establishing what is true across
them. The difference is the matrix: a summary runs source-by-source, a synthesis runs claim-by-claim.

## Claim extraction

Atomic means one assertion, one subject, one condition. Split compound statements — their parts
usually carry different confidence.

| Source text | Claims |
|-------------|--------|
| "X is 40% faster and cheaper to operate at scale" | C-001: X is 40% faster (under stated conditions). C-002: X costs less to operate at scale. |
| "Adoption grew rapidly, though churn remains a concern" | C-003: adoption grew (rate, period). C-004: churn is elevated (measure, comparison). |

Rules:
- Carry the source's hedges verbatim into the claim text. "may", "in this configuration", "n=12"
- Carry the conditions: version, scale, population, time window
- Record the claim as the source states it, not as the question wants it — reconciling the two is
  a later step and must be visible
- Note the location (page, section, timestamp) so the claim can be re-checked

## The matrix

Claims down, sources across. Every cell gets one of four values — the fourth is what most
syntheses omit and most need:

| | S-001 (P1) | S-002 (P3) | S-004 (P4) |
|---|---|---|---|
| C-001 | supports | contradicts | silent |
| C-002 | silent | supports | supports |

`supports` / `contradicts` / `partial` (supports under narrower conditions) / `silent`.

**Silence is not agreement.** Without the silent state, a claim mentioned by one source looks
unanimously endorsed by the corpus.

## Consensus vs. corroboration

Before recording agreement, test independence (`_research/CONTRACT.md`):

1. Do the agreeing sources cite each other? -> one source
2. Do they trace to the same dataset, benchmark, or announcement? -> one source
3. Same authors, org, or funder? -> one source
4. Could they have been wrong separately? -> if no, one source

Then re-count. Apparent consensus collapsing to one origin is a routine outcome and is itself a
headline finding: "this figure appears in nine places and originates in one unreplicated 2024
vendor benchmark."

## Weighing

Never count. Weight = tier x independence x directness.

- **Tier**: `P1`/`P2` dominate `P4`/`P5` regardless of number
- **Independence**: correlated sources contribute once
- **Directness**: a source measuring exactly our question beats a stronger source measuring an
  adjacent one. A rigorous study of a different population is weak evidence about ours

When a rigorous outlier contradicts many weak sources, the weight of evidence favours the outlier.
State that explicitly, because it reads as counterintuitive and will be questioned.

## Inference labelling

Anything not directly supported by a source is inference. Keep it, but mark it:

```
C-012 [INFERENCE] Latency will likely regress under 10x load.
  Basis: C-004 (P2, measured to 3x) + C-007 (P3, architecture description).
  Confidence: Low — extrapolation beyond measured range.
```

Chained inference compounds uncertainty. Two `Medium` premises yield a `Low` conclusion. Never let
a chain of reasonable steps output higher confidence than its weakest link.

## Sub-question answers

Answer each explicitly before assembling the primary answer:

```
Q1: Yes — X supports Y since v3.2. Confidence: High [S-001 P1, S-004 P2, independent].
Q2: Unknown — no source measures this; the two that claim it trace to one vendor page [S-006].
Q3: Contested — S-002 (P2) and S-008 (P2) disagree on measurement; see contradiction C-009.
```

Then the primary answer, with the conditions under which it holds and the conditions under which
it does not. An answer with no stated conditions is over-claimed.
