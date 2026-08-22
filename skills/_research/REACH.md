<!-- research:contract -->
# REACH — how close each claim got to the record

Binding on every `research-*` skill that gathers, grades, weighs or reports a
claim. The evidence ladder says what a source is worth *for* a claim. This
contract says something the ladder cannot: **whether the primary record was
ever actually opened, or only described by somebody who says they opened it.**

## The failure this prevents

A citation to a primary source and a citation to an article *about* that primary
source look identical in a bibliography. Both carry the authoritative name. One
of them is a claim about the record; the other is a claim about what a writer
said the record contains — and writers compress, round, drop the caveat, and
occasionally read the wrong table.

Five sources repeating one primary are one source. **Five sources repeating one
primary that nobody opened are one unopened source**, and a reader given the
bibliography cannot tell which case they are in.

## The five reach states

Every load-bearing claim carries one, next to its tier.

| Reach | Means |
|---|---|
| `primary` | The `P1` record was opened and the claim read off it directly |
| `one-hop` | A source that cites the primary was read; the primary itself was not opened |
| `chain` | Only derivative sources were read — none of them cite a primary either |
| `blocked` | The primary exists and could not be reached. **Names what would unblock it**: a paywall, a login, a library, a request, a fee |
| `no-primary` | No primary record exists for this kind of claim — a prediction, an opinion, a synthesis |

`no-primary` is a legitimate answer, and it is the one most often used
dishonestly. It applies where a record *cannot* exist, never where one exists
and was hard to find.

## The reach rate

The report states it: **claims at `primary`, over load-bearing claims**, with
the count. Not a percentage on its own — `4 of 7` says what `57%` hides.

- **A low rate is not a failure.** It is the honest shape of most research done
  under a budget, and stating it lets the reader discount accordingly
- **A rate of one deserves the same suspicion as a perfect record anywhere
  else.** Either the question was narrow enough that every record was at hand,
  or claims that could not reach a primary were quietly dropped from the ledger
  rather than carried at their real reach

Reach is an input to the confidence ceiling, never a substitute for it: a
`primary` claim read out of context is still wrong, and a `one-hop` claim from a
rigorous secondary can be strong. **Reach says what was opened, not what was
understood.**

## Boundary cases

- **A quotation of the primary inside a secondary** is `one-hop`. The quote may
  be accurate; the surrounding sentence is what selected it
- **A primary opened but not read at the relevant part** — the PDF was fetched,
  the table was not found — is `one-hop`, and saying so costs nothing
- **An archived or cached copy** is `primary` if it is the record itself. Note
  the retrieval date, because the live version may have moved
- **`blocked` with nothing named** is `chain` wearing an excuse. The point of
  the state is to price the missing certainty, and a price nobody wrote down is
  not a price
- **A claim whose reach drops during the run** — the primary turns out to be a
  reprint — is downgraded where it stands. Reach never improves by argument
