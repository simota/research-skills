<!-- research:deferred -->
# Writing Standards

Purpose: Uncertainty language, citation mechanics, traceability sweep.
Read when: uncertainty language, citation mechanics, traceability sweep
Verified: 2026-08-21 — no automated check.

## Uncertainty language

Map labels to words consistently. Inconsistent phrasing lets the reader calibrate on tone rather
than on the evidence.

| Label | Write | Never write |
|-------|-------|-------------|
| `High` | "X does Y", "measurements show X" | "X definitely/always Y" |
| `Medium` | "X likely does Y under <conditions>", "the available evidence indicates" | "X does Y" unqualified |
| `Low` | "one source reports X; unverified", "suggestive but thin" | "X may do Y" without saying how thin |
| `Unknown` | "no source addresses this", "nobody appears to have measured this" | Silence, or an inferred answer |

Two `Unknown` phrasings that mean different things — keep them distinct:
- "No evidence was found that X" — we looked, nothing turned up (say where you looked)
- "Evidence indicates X is not the case" — we found disconfirming evidence

Attribute contested claims: "S-002 reports 12k rps; S-008 reports 4k" beats "reports vary".
Naming the sources lets the reader weigh them; "varies" asks them to trust your averaging.

## Citation mechanics

- Inline marker at the claim, not at the end of the paragraph. A paragraph-terminal citation leaves
  the reader guessing which sentence it covers.
- Multiple sources: `[S-001, S-004]` — and if they are not independent, say so once in the text.
- Quote when wording is load-bearing (a spec requirement, a hedge, a definition). Keep it short,
  mark it, and cite the section or page.
- Paraphrase must not strengthen: "may reduce under some conditions" -> "may reduce under some
  conditions", never "reduces".
- Every marker resolves in the source list. Every source list entry is cited somewhere. Both
  directions are checked in `VERIFY`.
- Excluded sources never appear as citations. They may appear in the method appendix as excluded.

## Traceability sweep

Before delivery, walk the draft sentence by sentence:

| Sentence type | Requirement |
|---------------|-------------|
| States a fact about the world | Maps to a `C-nnn` with citations — or to an `S-nnn` on a chain that ran no synthesis |
| Draws a conclusion from claims | Labelled as inference, basis claims named |
| Describes method or coverage | Matches the search log |
| Recommends an action | Marked as recommendation, separated from evidence |
| Sets context or transitions | No factual content — verify it smuggled none in |

Anything that maps to nothing is either cut or promoted into a labelled inference. This sweep is
where invented illustrative numbers and half-remembered background facts get caught, and it is
mandatory — not a final polish.

## Summary/body consistency check

Diff the executive summary against the body on four axes:

1. **Confidence** — same label, both places
2. **Conditions** — every condition in the body claim survives into the summary claim
3. **Scope** — the summary does not generalise beyond the body's population or version
4. **Unknowns** — at least the load-bearing gap appears in the summary

A summary more confident than its body is the most consequential defect this skill exists to
prevent: the summary is what travels.

## Shortening without lying

When the document must be shorter:

- **Do**: cut whole claims, starting with the lowest-impact ones; move detail to an appendix;
  reduce the number of examples
- **Do not**: drop qualifiers, merge distinct claims into one broader one, round ranges to points,
  or remove the confidence labels

Cutting a claim keeps the remaining ones true. Cutting qualifiers makes the remaining ones false.

## Tone

Neutral and specific. No advocacy, no rhetorical questions, no dramatic framing of findings. The
evidence is the argument; adding emphasis substitutes for it and signals to a careful reader that
the underlying support is thin.

## Citation layout

The single definition; `_research/CONTRACT.md` carries the rule, this carries the shape.

Inline marker `[S-007]`, resolved in a Sources section:

```
[S-007] Author/Org. "Title." Publication, YYYY-MM-DD. <URL> (accessed YYYY-MM-DD) — P2
```

Include the access date for anything web-hosted, and the provenance tier. Quote directly when
wording matters; keep quotes short and marked. Paraphrase must not upgrade hedged language:
"may reduce" never becomes "reduces".

