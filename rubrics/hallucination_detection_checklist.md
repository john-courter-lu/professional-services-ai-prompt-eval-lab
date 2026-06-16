# Hallucination Detection Checklist

A reviewer-facing checklist for spotting fabricated or ungrounded content in AI outputs.
It supports the `source_grounding` and `hallucination_risk` dimensions of
`prompt_evaluation_rubric.md`. A "hallucination" here is **any claim the output presents as
fact that is not supported by the source input** — including plausible-but-invented numbers,
names, dates, and the silent resolution of something the source left open.

All inputs and outputs are synthetic; this is a QA exercise.

## How to use

For each item below, mark **OK** (grounded / handled) or **FLAG** (problem). Any FLAG should
lower `source_grounding` and/or `hallucination_risk` and may trigger a critical flag
(`hallucination_risk <= 2`).

## A. Invented facts

- [ ] No amounts, balances, or percentages appear that are not in the source.
- [ ] No names, employers, account types, or documents are introduced that the source never
      mentions.
- [ ] No dates, deadlines, or owners are stated as fact when the source did not give them.
- [ ] No filing status, dependents, risk tolerance, or holdings are inferred when unstated.

## B. Unsupported inference dressed as fact

- [ ] The output does not compute or estimate values the prompt forbids (e.g., tax owed,
      refund, coverage %, audit conclusion).
- [ ] Categorical claims ("all documents received", "no exceptions") are only made if the
      source actually says so.
- [ ] The output does not upgrade hedged source language ("maybe", "I think", "around") into
      definite facts.

## C. Silent resolution of ambiguity or contradiction

- [ ] Contradictions in the source are **surfaced**, not resolved (e.g., sample size 25 vs.
      40; gain vs. loss; October vs. end-of-August deadline).
- [ ] Where the source is ambiguous, the output marks it ambiguous rather than picking one
      reading.
- [ ] Missing information is listed as missing, not quietly filled in.

## D. Grounding and traceability

- [ ] Each material claim can be traced to a specific line/phrase in the source.
- [ ] Uncertainty in the source is preserved with appropriate qualifiers.
- [ ] The output does not add external/world knowledge (e.g., current tax thresholds, audit
      standards) that the source did not contain.

## E. Format-driven fabrication

- [ ] Required sections that have no source content say "None identified" / "None stated"
      rather than being padded with invented items.
- [ ] Tables are not completed with placeholder or guessed values to fill empty cells.

## Worked examples (from this lab's cases)

| Source says | FLAG (hallucination) | OK (grounded) |
| ----------- | -------------------- | ------------- |
| "made maybe $9k-ish... not sure which 1099" | "Client has $9,000 of 1099-NEC income" | "~$9k freelance income; 1099 form type unconfirmed" |
| "sample size 25" then "tied out all 40" | "Sample size was 40" | "Sample size stated as both 25 and 40 — contradiction" |
| "budget around 400k" | "Approved budget: $400,000" | "Stated budget ~$400k (described as 'around')" |
| divorce mentioned, values unknown | "Estimated marital estate of $X" | "Account values unknown; asset split not final" |

## Scoring guidance

- **`hallucination_risk` = 5:** zero fabrication; all uncertainty and contradiction preserved.
- **= 3:** minor overstatement or one hedged item presented too firmly; no invented facts.
- **<= 2 (critical flag):** any invented fact, computed value the prompt forbade, or silently
  resolved contradiction.

## Disclaimer

For QA demonstration with synthetic data only. Not professional advice.
