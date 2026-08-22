<!-- research:guidance -->
# Traps — scope

- **The stated ask is usually a proxy.** "What's the best vector DB" is almost never the question;
  "will our retrieval quality survive 10x corpus growth" is. Ask what breaks if the answer is wrong.
- **Comparative questions need criteria before candidates.** Fix the criteria first, or the
  candidate that turns up first silently sets them.
- **Broad first, narrow later inverts the cost.** Decompose *then* search — one narrow searchable
  sub-question is cheaper than a broad search you narrow afterwards by discarding most of it.
- **"Comprehensive" is not a scope.** It is the absence of one. Convert to a coverage rule:
  which source types, how many, over what period.
- **A prior recorded after the search is not a prior.** Write it down before any retrieval, or the
  work cannot distinguish learning from confirmation.
- **Effort budget is set in sources and iterations, not in time.** "Spend 30 minutes" is
  unmeasurable mid-chain; "at most 12 sources, 3 query rounds" is checkable at every step.
