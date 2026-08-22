<!-- research:deferred -->
# Channel Map

Purpose: Choosing where to look for a given question type.
Read when: choosing where to look for a given question type
Verified: 2026-08-21 — no automated check.

Pick the channel before the keywords. Most failed searches are right-keyword/wrong-channel.

## By question type

| Question | Go here first | Not here |
|----------|---------------|----------|
| What does this software actually do | Source repository, official docs, changelog, issue tracker, RFC/spec | Blog roundups |
| Does this API/format/protocol guarantee X | The specification text, by section number | Tutorials |
| How fast / how much | Benchmark methodology + raw numbers; the vendor's own docs for pricing | Comparison articles |
| Who makes X, and are they solvent | Company registry, filings, funding databases, job postings | Press coverage |
| What is the research consensus | Systematic reviews and meta-analyses first, then primary studies | Popular science coverage |
| Is this legal / compliant | The regulation text and official guidance; check for amendments | Law-firm marketing posts |
| What exists in this space | Package indexes, awards lists, conference programmes, curated registries, funding rounds | Ad-hoc search |
| Why did this change | Commit history, changelog, mailing list, issue discussion, meeting minutes | Retrospective articles |
| What do practitioners experience | Practitioner communities, conference talks, incident writeups | Vendor case studies |
| What happened when | Contemporaneous reporting + archived snapshots | Later retellings |

## Channel properties

| Channel | Strength | Systematic blind spot |
|---------|----------|-----------------------|
| General web index | Breadth, recency of commentary | Buries primaries; rewards SEO; heavy synthetic-content contamination |
| Academic index | Method transparency, citation graph | Publication lag; positive-result bias; paywalls |
| Code repositories | Ground truth on behaviour and history | No context on intent; stale forks and mirrors |
| Official docs / specs | Authoritative on the product's own behaviour | Aspirational; silent on limitations and comparisons |
| Registries / filings | Verifiable, structured, hard to fake | Lagging; jurisdiction-limited; format-hostile |
| Package/dependency indexes | Complete enumeration, adoption signals | Popularity != quality; abandoned packages linger |
| Practitioner communities | Failure modes and real conditions | Anecdotal, unrepresentative, often undated |
| News/trade press | Timeliness, access to people | Syndication collapse; press-release passthrough |
| Web archives | Recovers deleted and changed pages | Incomplete crawls; dynamic pages captured badly |

## Language and region

A corpus assembled in one language reflects one market's vendors, regulators, and practitioners.
When the question touches markets, regulation, pricing, or adoption, search in the relevant
language too — or state plainly that the corpus is single-language and what that likely omits.

## Access reality

Note which channels were unreachable in this session (paywalled journals, licensed databases,
credentialed registries). Sub-questions best answered there carry a ceiling on achievable evidence
tier, and that ceiling belongs in the coverage statement, not in a silently weaker answer.
