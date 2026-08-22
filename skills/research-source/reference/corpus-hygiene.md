<!-- research:deferred -->
# Corpus Hygiene

Purpose: Deduplicating, testing independence, writing the manifest and search log.
Read when: deduplicating, testing independence, writing the manifest and search log
Verified: 2026-08-21 — no automated check.

## Deduplication

Source IDs are minted at retrieval, before dedup, so every duplicate already has an ID to be
recorded under. Collapsing is a recorded relationship, never a deletion.

Collapse before counting. A corpus that counts derivatives as separate sources overstates
corroboration, which overstates confidence — the most common way research goes confidently wrong.

Signals that two entries are one source:
- Publication dates within a day or two, with near-identical numbers and phrasing
- Both trace to the same press release, dataset, benchmark run, or announcement post
- One cites the other, or both cite the same single upstream
- Shared author, shared organisation, shared funder
- Translations, syndications, mirrors, and re-summaries of the same original

Record the collapse rather than deleting it silently:

```
S-004 canonical. S-011, S-013, S-019 collapsed into S-004 (syndicated from same release, 2026-03-11).
```

The collapse note is itself a finding: "this claim has one origin and four echoes" is often the
most useful thing the research learned.

## Independence test

Ask: **could these two sources have been wrong separately?** If a single error upstream would
propagate to both, they are one source for confidence purposes.

| Situation | Independent? |
|-----------|--------------|
| Two studies, different teams, different data | Yes |
| Two studies, same team, same cohort | No |
| Vendor benchmark + press coverage of it | No |
| Vendor benchmark + third-party reproduction with published method | Yes |
| Two docs pages from the same product | No |
| Practitioner report + official docs agreeing | Yes (different failure modes) |

## Read depth

Record honestly, per source: `abstract` / `partial` / `full`. (Lowercase — uppercase `PARTIAL`
is the handoff `status` value and means something else.) Downstream grading depends on it —
a claim resting on an abstract is weaker than the same claim from a full read, because abstracts
systematically overstate. Never upgrade the recorded depth to make a corpus look stronger.

## Corpus manifest

```markdown
## Corpus

| ID | Title | Author/Org | Date | Type | Sub-Q | Depth | Locator |
|----|-------|-----------|------|------|-------|-------|---------|
| S-001 | ... | ... | 2026-02-04 | spec | Q1,Q3 | full | <URL or DOI> (acc. 2026-08-21) |

Collapsed: S-011,S-013 -> S-004 (syndication)
Red flags: S-009 (undated, citations do not resolve) — flagged for appraisal, not excluded here
```

## Search log

```markdown
## Search Log

| # | Sub-Q | Channel | Query | Seen | Kept |
|---|-------|---------|-------|------|------|
| 1 | Q1 | web | "<exact query>" | 10 | 3 |
| 2 | Q1 | repo | site:... "<query>" | 4 | 1 |
| 3 | Q2 | web | "<disconfirming query>" | 12 | 0 |
```

Zero-yield rows stay. They tell the next pass which ground was covered — they are evidence about
search coverage, not evidence about the proposition. An `Unknown` rests on them only in the sense
that nothing was found to settle the question; they never count as disconfirmation.

## Coverage statement

Always present, three lines minimum:

```
Thin: Q3 has one source, vendor-authored. Bar called for an independent measurement.
Structural gaps: English-only; no access to paid analyst databases; failures under-published.
Saturation: Q1 saturated (3 independent post-dedup sources, no new claims). Q2 not saturated, cap hit.
```

A corpus that names its own gaps is far more useful than one that appears complete.
