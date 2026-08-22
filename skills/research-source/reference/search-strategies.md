<!-- research:deferred -->
# Search Strategies

Purpose: Building query sets, chaining, adversarial search, stall recovery.
Read when: building query sets, chaining, adversarial search, stall recovery
Verified: 2026-08-21 — no automated check.

## Query set construction

Every query is an outbound disclosure. Before building the set, check it against
`_research/SOURCE_HYGIENE.md` §Outbound data — no credentials, internal hostnames, private repo or
service names, customer identifiers, unreleased names, or verbatim proprietary text. Generalise
the sensitive parts ("our internal auth gateway" -> "reverse proxy"), and log the generalised form.

Build the set before searching. One phrasing tests one hypothesis about how the field talks.

For each sub-question, write:

| Slot | Contents |
|------|----------|
| Core terms | The concept, in the field's own words |
| Synonyms / eras | What it was called before, what marketing calls it, what academia calls it |
| Entities | Named products, orgs, authors, standards, versions |
| Qualifiers | Time window, region, scale, version, population |
| Negative terms | Homonyms and adjacent fields to exclude |
| Disconfirmers | `failure`, `postmortem`, `retracted`, `does not`, `limitations`, `criticism`, `we moved off` |

Vocabulary rotation is the highest-yield move when a search is dry. Practitioners, vendors,
academics, and regulators name the same thing differently; the term that finds nothing in one
register finds the whole literature in another.

## Operators worth using

| Operator | Use |
|----------|-----|
| `site:` | Scope to a standards body, registry, vendor docs, or a single publication |
| `filetype:pdf` | Reach papers, filings, and specs that HTML search buries |
| exact `"quoted phrase"` | Trace a claim's origin — find every page repeating the same sentence |
| `-term` | Cut a homonym or a dominant unrelated meaning |
| date filters | Separate "current state" from "historical origin" queries; run both |
| `intitle:` / `inurl:` | Find the canonical document rather than commentary about it |

## Chaining from seeds

Keyword search finds the well-indexed middle. Chaining finds the ends.

**Backward** (toward the origin): reference lists, "as described in", linked specs, the paper a
blog post is about, the commit a changelog mentions. Ends when you reach something that observed
the thing directly. Every load-bearing claim gets backward-chained at least once.

**Forward** (toward the current state): who cites this, who depends on this package, who links
here, issues referencing this commit, follow-up papers, "since publication" notes. Forward chaining
is the best way to find both the newest work and the retraction.

**Lateral**: the same author's other work, the same group's later work, competitors' responses.

## Adversarial search

Run explicitly, not as an afterthought. Confirmation is the default outcome of any search phrased
in the terms of the thing being confirmed.

| Target | Query shape |
|--------|-------------|
| Failures | "why we moved off X", "X postmortem", "migrating away from X" |
| Method criticism | "critique of <study>", "failed to replicate", "reanalysis" |
| Retraction | "<claim> retracted", "correction", "erratum" |
| Negative results | "no significant effect", "did not improve", "found no difference" |
| Conflicts | "<author> funding", "<study> sponsored by" |
| Survivorship correction | Search for the abandoned projects, not the launched ones |

Publication bias means failures are systematically under-published. A search that surfaces none is
an audit record of where and how you looked — not evidence that none exist. The proposition stays
`Unknown` until a retrieved source says otherwise; never read silence as endorsement.

## Origin tracing

To find where a widely repeated claim started:

1. Quote the most distinctive sentence exactly; find every page carrying it
2. Sort by date; the earliest is a candidate origin, not necessarily the origin
3. Check whether the earliest cites something older — repeat until a page presents its own data
4. Verify the origin says what the repeaters claim; drift is common and usually directional
   (hedges dropped, ranges become point estimates, conditions disappear)
5. Record the whole chain — the drift itself is often the finding

## Stall recovery

Two dry rounds, then rotate — do not re-phrase a third time:

1. **Channel** — general index -> registry/database -> primary repository -> practitioner community -> archive
2. **Vocabulary** — academic / vendor / practitioner / regulatory register; and the previous era's term
3. **Era** — the thing may predate its current name
4. **Language and region** — the work may exist only in another language or another market's press
5. **Adjacency** — the answer may live in a neighbouring field that solved the same problem

Still dry: report `Unknown` with the full query log. Documenting covered ground is a real result.
