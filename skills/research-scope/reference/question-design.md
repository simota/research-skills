<!-- research:deferred -->
# Question Design

Purpose: Framing the primary question, answer shapes, presupposition stripping.
Read when: framing the primary question, answer shapes, presupposition stripping
Verified: 2026-08-21 — no automated check.

## Recovering the real question

Run these four in order. Stop early only when the answer is already on the record.

1. **What decision does this inform?** If nothing changes based on the answer, the research is
   entertainment. Say so, or find the decision hiding behind the ask.
2. **What happens if the answer is wrong?** The cost of error sets the evidence bar. A reversible
   `P4`-supported call and a one-way door needing `P1` corroboration are different jobs.
3. **What do you already believe?** Record the prior and its confidence now — see `Priors` below.
4. **When would you stop reading?** The requester's honest answer is usually the right budget.

## Answer shapes

Fix the shape before searching. The shape dictates the search strategy and the report format.

| Shape | Question form | Search implication | Report form |
|-------|---------------|--------------------|-------------|
| Quantity | "How much / how many / how fast" | Need measurements with methods; watch units and conditions | Number + range + as-of date + method |
| Ranking | "Which is best / who leads" | Need criteria first, then per-candidate evidence on each criterion | Criteria table, per-cell evidence |
| Binary | "Does X do Y / is it true that" | Need direct evidence; absence of evidence is a real answer | Yes/No/Unknown + conditions |
| Mechanism | "How does X work / why does Y happen" | Need primary specs, source, or first-hand accounts of the pathway | Stage-by-stage walkthrough |
| Landscape | "Who is doing X / what exists" | Need inclusion criteria and axes before enumeration | Map along declared axes + coverage note |
| Trajectory | "Where is X heading" | Need historical series + named forecasters; separate observed from projected | Observed trend, then projections labelled as such |

Mixed asks are common ("what exists and which is best") — split them into two sub-questions with
different shapes rather than one blurred question.

## Presupposition stripping

A question that embeds its conclusion cannot be answered honestly.

| Asked | Presupposes | Reframed |
|-------|-------------|----------|
| "Why is X better than Y?" | X is better | "On which criteria does X outperform Y, and on which does it not?" |
| "How do we get users to adopt X?" | Adoption is desirable and blocked | "What evidence exists on demand for X, and on the causes of low adoption?" |
| "Prove that this approach scales" | It scales | "At what load does this approach degrade, and what is the reported ceiling?" |
| "What's the best tool for Z?" | A single best exists | "Under which constraints does each candidate win?" |

Strip the presupposition, show the requester both versions, and proceed with the neutral one
unless they explicitly want the advocacy version — which is no longer research, and should be
labelled as such in the deliverable.

## Priors

Record before any retrieval:

```
Prior: <what we currently believe> — confidence Low | Medium | High
Basis: <where that belief came from: experience, a source, an assumption>
Falsifier: <the specific finding that would overturn it>
```

Two uses. It makes confirmation bias visible (a search that only confirms the prior is a search
that was too narrow), and it makes the research's value measurable: if the posterior equals the
prior, the work either confirmed something usefully or found nothing — and the brief lets you
tell those apart.

## Unanswerable asks

| Type | Example | Response |
|------|---------|----------|
| Normative | "Should we open-source this?" | Answer the empirical sub-questions (what comparable projects experienced) and hand the value judgement back |
| Private fact | "What is competitor X's churn rate?" | Say it is unpublished; offer proxies (job postings, pricing changes, review volume) explicitly labelled as proxies |
| Unobserved future | "Will framework X still be maintained in 2030?" | Substitute leading indicators: commit cadence, maintainer count, funding, dependent count |
| Definitional | "Is X really AI?" | Fix the definition first, or answer under two stated definitions |
| Counterfactual | "Would we have grown faster with Y?" | Not answerable; offer the nearest natural experiment and mark the inference gap |

Naming an ask unanswerable and offering the nearest answerable substitute is a complete
deliverable. Producing a confident answer to an unanswerable question is the failure mode.
