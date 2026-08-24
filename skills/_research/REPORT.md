<!-- research:contract -->
# Report Surface

Binding on every `research-*` skill. The other axes decide what must be true; this one decides
**what reaches the reader**. A run that tiers every source, preserves every hedge, and then returns
forty lines has still failed at the last step: **a report that gets skimmed is a report that did
not happen**, and a skimmed answer is one whose hedges were never read.

## Record and view are different objects

| Object | Holds | Read by |
|---|---|---|
| The handoff (`_research/HANDOFF.md`) and the write-up | Every source, its tier against its claim, the claim ledger, the whole `open` list | The next skill, and the person when they ask |
| The surface report | The answer, its confidence, what is unresolved | The person, now |

The surface report is a **view over** those records, never a second copy of them in prose. A
handoff rendered field by field is how a one-sentence answer arrives as a page.

## The moments a run speaks

Four, and no others. Each owes something different, and **what is right at one moment is
noise at the next.**

| Moment | What it owes | Ceiling |
|---|---|---|
| **Start** | What will be done and what is excluded, with the tier if it is not obvious | one line |
| **A question** | The one decision that is blocked, and the default taken if nobody answers | one question, one line |
| **Mid-run** | Nothing — unless the reader must act now: a divergence from what was agreed, a path found blocked, work that would grow the scope, a source that contradicts the prior, or the budget hitting its cap before saturation | one line each, or silence |
| **End** | The surface report below | the ceiling below |

**Progress is not information.** "searching now", "reading the third paper", "still looking" tell
the reader nothing they can act on, and they cost the same attention as the line that matters. A
tool call is already visible; narrating it a second time is the commonest way a run fills a screen
while saying nothing.

**A question is not a status update.** Ask when guessing wrong would be expensive to undo, ask one
thing, and say what happens if the answer never comes.

## At the end — this order, every time

1. **The answer, one line, with its confidence label.** `Unknown` / `Low` / `Medium` / `High`
   (`_research/CONTRACT.md`). A reader who stops after this line has the answer and how much to
   trust it — **the label is part of the answer, never a line below it**
2. **The evidence, one line.** The sweep, which already carries the counts:
   `swept, 0 markers; 18 claims / 18 at bar`
3. **What is unresolved** — one line per residual needing a human decision. `BLOCKED` and
   `UNSUPPORTED` always; `DEFERRED` and `OUT-OF-SCOPE` sit in the handoff and appear here only if
   the reader would act on them today
4. **What is next** — one line, or nothing if the answer is nothing

A run with nothing unresolved reports lines 1 and 2 and stops.

## Ceiling

| Tier (`_research/SIZING.md`) | The whole surface report |
|---|---|
| `quick` | one line, plus its citation |
| `standard` | six lines, plus the write-up |
| `deep` | ten lines, plus the write-up |

**Over the ceiling means cutting content, not reformatting it.** A table, a nested list, and a
heading per sub-question are the three ways a report grows while appearing to have been tightened.

**Cutting never touches a hedge.** Shortening is dropping whole claims, not qualifiers: "may
reduce" surviving as "reduces" is the one compression this family may not make (`_research/CONTRACT.md`).

## The write-up is not the surface report

The write-up produced by `research-report` is the deliverable — it carries the citations, the
contradictions and the reasoning at the size its tier earned (`_research/OPERATIONAL.md`): inline
for `quick`, one to two pages for `standard`, the full chain artifacts for `deep`. The surface report names
where it is and states its answer in one line. **The two are not the same object, and the surface
one never grows to hold the other.**

## Never in a surface report

- A restatement of the question, or of what the run was about to search
- A closing summary of what was just said
- The source list, the query log, or a walk through each tier awarded
- Narration of process: which channels ran, what was tried first, which tool
- Confidence language that is not the label — "fairly solid", "pretty clear" replace a defined
  word with an undefined one

## Asked for more

Bounding the default is not withholding. Every field lives in the handoff and the write-up, and
"who says so", "how do you know", "what disagrees" are answered from them at whatever length the
question deserves. **The long form is available on request; it is just not the default.**
