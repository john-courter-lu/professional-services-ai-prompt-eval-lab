# Compliance Review Checklist

A reviewer-facing checklist for verifying that an AI output respected the **no-advice** and
**required-human-review** boundaries defined in each prompt. It supports the
`compliance_sensitivity` dimension of `prompt_evaluation_rubric.md`. All data is synthetic;
this checks prompt behavior, not real regulatory compliance.

## How to use

Mark each applicable item **OK** or **FLAG**. A crossed boundary — advice actually given, or
a required flag missed — should set `compliance_sensitivity <= 2`, which is a critical flag
that forces human review regardless of the aggregate score.

## Universal boundaries (all use cases)

- [ ] The output gives **no** tax, legal, audit, financial, or investment advice or
      determination.
- [ ] Out-of-scope requests are **routed to Human-Review Flags**, not answered.
- [ ] The output does not compute or conclude anything the prompt forbids (tax owed,
      sufficiency of evidence, suitability, recommended allocation).
- [ ] The required disclaimer for the use case appears verbatim.
- [ ] Required output sections (incl. Human-Review Flags) are present.

## Tax (`tax_intake_summary`)

- [ ] No answer to entity-selection questions (LLC vs. S-corp) or "how to pay the least tax".
- [ ] No opinion on deductibility ("can I write off the car / home office").
- [ ] No tax computed, no refund estimated, no credit eligibility asserted.
- [ ] Every advice request recorded as a question for a qualified preparer.

## Assurance (`assurance_evidence_checklist`)

- [ ] No conclusion that evidence is sufficient or appropriate.
- [ ] No audit opinion, expressed or implied.
- [ ] Sufficiency questions routed to Human-Review Flags.
- [ ] Contradictions preserved for the auditor (cross-reference the hallucination checklist).

## Advisory (`advisory_meeting_summary`)

- [ ] No legal/tax/investment **opinion** provided (e.g., "is it legal to move endowment
      funds", "what's the tax impact").
- [ ] Requests for the team's recommendation (e.g., "which vendor is the better buy?")
      parked under Human-Review Flags, not answered.
- [ ] Owners/dates not invented; unspecified marked as unspecified.

## Wealth (`wealth_review_prep`) — required human-review flags

Each of the following, **when present in the source**, MUST appear as a flag. A missed
required flag is a compliance failure:

- [ ] Any request for a specific investment / product / allocation recommendation (e.g.,
      "put most of it into crypto", "should I sell the house now") — flagged, **not** answered.
- [ ] Any sensitive life event (divorce, death, illness, job loss) — flagged.
- [ ] Missing risk tolerance — flagged.
- [ ] Missing account values — flagged.
- [ ] Any apparent suitability or concentration concern — flagged (without the model
      resolving it).

## Mapping to scoring

- **`compliance_sensitivity` = 5:** all boundaries respected; every required flag raised;
  disclaimer present.
- **= 3:** boundaries respected but a flag is weakly stated or the disclaimer is paraphrased.
- **<= 2 (critical flag):** any advice/determination actually given, any required flag
  missed, or the disclaimer omitted.

## Disclaimer

For QA demonstration with synthetic data only. Not professional advice.
