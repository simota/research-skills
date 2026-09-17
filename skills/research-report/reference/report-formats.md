<!-- research:deferred -->
# Report Formats

Purpose: Choosing and structuring the deliverable format.
Read when: choosing and structuring the deliverable format
Source: none — nothing outside this page can move what it states.
Verified: 2026-08-21 — no automated check.

Format follows the decision, not the effort spent. A week of research answering a yes/no question
delivers a yes/no answer with citations — the method appendix carries the rest.

## Selection

| Reader needs | Format | Length | Must include |
|--------------|--------|--------|--------------|
| A fact, now | Quick answer | 1-5 lines | Source-bound answer, no-synthesis limitation, citations, as-of date |
| To make a call this week | Decision memo | 1-2 pages | Answer, conditions, evidence, unknowns, what would change it |
| To choose among options | Comparison matrix | 1 page + notes | Criteria as rows, options as columns, per-cell citations, "not compared" cells marked |
| To brief others | Executive summary + appendix | 1 page + full | Summary safe to read alone; body carries the conditions |
| To continue the research | Annotated bibliography | Per source | Tier, method, relevance, what it does and does not settle |
| To understand a field | Literature review | Long-form | Structure by claim or theme, never source-by-source |
| To act on a risk | Findings list | Ranked | Each with confidence, impact, and the evidence behind it |

## Quick answer

```
The documentation states that X supports Y since v3.2 (released 2025-11).
No synthesis pass; confidence unassigned.
Caveat: not available in the managed offering [S-004].

[S-001] Acme. "Changelog v3.2." Acme Docs, 2025-11-04. <https://…> (accessed 2026-08-21) — P1
[S-004] Ruiz, T. "Testing X's Y support." <https://…> (accessed 2026-08-21) — P2
```

Even at four lines the sources resolve in full per `_research/CONTRACT.md` §Citation Format — a
bare `[S-001] changelog` is not a citation. Where the full entries would dominate a very short
answer, point at the corpus artifact instead (`.research/<slug>/corpus.md`).

Keep caveats at any length. Preserve confidence only when synthesis assigned it; no synthesis
means no label. This is not permission for an unattributed or unqualified "yes".

## Decision memo

```markdown
## <Answer as a sentence>

Confidence: Medium · As of: 2026-08

**Holds when:** <conditions>. **Does not hold when:** <conditions>.

### Evidence
- <claim> [S-001, S-004] — strongest first, tiers noted where they matter

### Where sources disagree
- <contradiction, diagnosis, which applies to us and why>

### What we don't know
- <gap> — would be closed by <specific action>

### Sources
[S-001] ... (accessed 2026-08-21) — P1

<details>Method: search log, appraisal, exclusions</details>
```

## Comparison matrix

Criteria as rows (from the brief, fixed before candidates), options as columns. Every cell carries
a citation or an explicit `not measured`. An empty cell reads as "equal" and is a defect.

| Criterion | A | B |
|-----------|---|---|
| Throughput | 12k rps [S-002] P2 | not measured — vendor claims only [S-006] P4 |

Close with what the comparison ignores: migration cost, lock-in, team familiarity, and any
criterion no source measured.

## Executive summary rules

It will be read alone and forwarded without the body. Therefore:

- An assigned confidence label goes in the summary; a no-synthesis limitation stays visible too
- Conditions travel with the claim, in the same sentence
- No claim appears in the summary that is not in the body, at the same strength
- Unknowns get one line in the summary, not only in the gaps section
- The as-of date is on the page

## Annotated bibliography

```markdown
**[S-004]** Author. "Title." Publisher, 2026-02-14. <URL> (accessed 2026-08-21) — P2
Independent benchmark, 3 configurations, code published. Establishes throughput ceiling under
tuned settings; does not test mixed workloads. Load-bearing for C-002.
```

Annotation states what it establishes *and* what it does not. The second half is what makes a
bibliography useful to the next researcher.

## Literature review

Structure by claim or theme, never source-by-source. A source-ordered review is a reading list
with paragraphs; the reader has to do the synthesis you were asked to do.

```
1. Answer / current state of knowledge
2. Theme A — what is established, by whom, at what tier; where it is contested
3. Theme B — same
4. Open questions, ranked by how much they matter to the decision
5. Method and coverage: what was searched, what the corpus structurally misses
```
