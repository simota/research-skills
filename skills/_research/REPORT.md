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

Four. Each owes something different, and **what is right at one moment is noise at the next.**

| Moment | What it owes | Ceiling |
|---|---|---|
| **Start** | What will be done and what is excluded, with the tier if it is not obvious | one line |
| **A question** | The one decision that is blocked, and the default taken if nobody answers | one question, one line |
| **Mid-run** | What the reader can act on: a divergence from what was agreed, a path found blocked, work that would grow the scope, a source that contradicts the prior, the budget hitting its cap before saturation, or a change of plan | one line each |
| **End** | The surface report below | the ceiling below |

A mid-run line carries something the reader would decide or do differently for knowing it. The
tool call itself is already visible, so the line says what it changed, not that it happened.

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

The surface report is the four items above and nothing that is already in the write-up. A
`quick` chain has no write-up, so its citation rides on the answer line. A `standard` or `deep`
chain names where the write-up is and stops: the reader who wants the evidence table opens it
(`_research/SIZING.md`).

**Too long means cutting content, not reformatting it.** A table earns its place when it makes
the answer faster to read than the sentences it replaces, never as a container for claims that
should have been cut.

**Cutting never touches a hedge.** Shortening is dropping whole claims, not qualifiers: "may
reduce" surviving as "reduces" is the one compression this family may not make (`_research/CONTRACT.md`).

## The write-up is not the surface report

The write-up produced by `research-report` is the deliverable — it carries the citations, the
contradictions and the reasoning at the size its tier earned (`_research/OPERATIONAL.md`): inline
for `quick`, one to two pages for `standard`, the full chain artifacts for `deep`. The surface report names
where it is and states its answer in one line. **The two are not the same object, and the surface
one never grows to hold the other.**

## Not bigger than it is

The requested scope is the deliverable. Neighbouring concerns, future possibilities and general
principles are not folded into the answer, and a small ask does not come back as a survey. **Being
thoughtful and diverging are not the same thing** — thought goes deeper into the one thing asked,
never wider. Option lists are given when they were asked for, or when the choice is the reader's
to make.

**A real problem is the exception.** If the request would break something, is unsafe, or rests on
a false premise, say what is wrong, why, and the options, at whatever length that takes. **Cut
noise, never risk.**

## What the surface report leaves to the record

The surface report opens on the answer and ends on what is next; the question, the source list,
the query log, the tiers awarded and the path the run took live in the handoff and the write-up
and are answered from there. Confidence is stated as the label and only the label — "fairly
solid" and "pretty clear" replace a defined word with an undefined one (`_research/CONTRACT.md`).

## Asked for more

Bounding the default is not withholding. Every field lives in the handoff and the write-up, and
"who says so", "how do you know", "what disagrees" are answered from them at whatever length the
question deserves. **The long form is available on request; it is just not the default.**
