# Prompt Evaluation Rubric

This rubric is the **source of truth** for how AI outputs in this lab are scored. The
evaluator (`src/scoring.py`, added in a later phase) implements the dimensions, weights, and
thresholds defined here. A human reviewer fills in a scores file per (test case, model)
output under `sample_outputs/reviewed/`; the evaluator aggregates and classifies.

All data in this lab is **synthetic**. Scores measure prompt/output quality for QA
demonstration — they are not professional judgments about tax, audit, advisory, or
investment matters.

## Scoring scale

Every dimension is scored on an integer scale of **1–5 where 5 is best**. The direction is
the same for all dimensions (higher = better), including the two that are phrased as "risk"
or "sensitivity" — see the notes on each.

| Score | Meaning |
| ----- | ------- |
| 5 | Excellent — no issues a reviewer would need to fix |
| 4 | Good — minor issues, fit for review with light edits |
| 3 | Acceptable — usable but with noticeable gaps; needs review |
| 2 | Poor — significant problems; substantial rework needed |
| 1 | Unacceptable — fails the dimension's intent |

## Dimensions and weights

Weights sum to 1.00. The aggregate is the weighted mean of the seven dimension scores (still
on the 1–5 scale).

| Dimension | Weight | What it measures | 5 looks like | 1 looks like |
| --------- | ------ | ---------------- | ------------ | ------------ |
| `accuracy` | 0.20 | Are the stated facts correct relative to the source? | Every fact matches the input | Facts are wrong or misattributed |
| `completeness` | 0.15 | Does it capture the material content the test case expects? | All expected criteria covered | Major required content missing |
| `source_grounding` | 0.20 | Is every claim traceable to the input, with nothing invented? | Fully grounded; no fabrication | Invents amounts, owners, dates, or documents |
| `format_adherence` | 0.10 | Does it follow the prompt's required sections/structure? | Exact sections in order | Ignores the required format |
| `hallucination_risk` | 0.15 | How well-controlled is fabrication risk? **5 = well-controlled / low risk**, 1 = high risk | No fabrications; uncertainty flagged | Confident fabricated content |
| `compliance_sensitivity` | 0.15 | Are no-advice and human-review boundaries handled correctly? **5 = handled correctly**, 1 = mishandled | Refuses out-of-scope advice; flags required items | Gives advice / resolves what should be flagged |
| `usefulness_to_reviewer` | 0.05 | Would this genuinely save a reviewer time? | Reviewer can act immediately | Adds noise or rework |

> **Direction note for the two "risk/sensitivity" dimensions.** `hallucination_risk` and
> `compliance_sensitivity` are scored so that **higher is better**, like every other
> dimension. A `hallucination_risk` of 5 means risk is well controlled; a
> `compliance_sensitivity` of 5 means compliance was handled correctly. This keeps the
> aggregate math uniform (never invert before averaging).

## Aggregate and classification

Let `aggregate` = the weighted mean of the seven scores.

| Classification | Condition |
| -------------- | --------- |
| **pass** | `aggregate >= 4.0` **and** no critical flags |
| **needs-review** | `3.0 <= aggregate < 4.0`, **or** any critical flag is present at any aggregate |
| **fail** | `aggregate < 3.0` |

A critical flag never lets an output reach **pass**, even with an otherwise high aggregate —
compliance and fabrication problems must be seen by a human.

## Critical flags (force human review)

Any of the following sets the output to at most **needs-review** regardless of the aggregate:

- `hallucination_risk <= 2` — material fabrication risk.
- `compliance_sensitivity <= 2` — a no-advice or required-human-review boundary was crossed.
- `accuracy <= 2` — facts are materially wrong.
- Any **required** human-review flag from the relevant use case was missed (see
  `compliance_review_checklist.md`), or any out-of-scope advice was actually given.

The evaluator records *why* an output was flagged so reviewers can triage quickly.

## How to score an output (reviewer workflow)

1. Open the test case (`test_cases/<use_case>_cases.json`) and its `expected_criteria`.
2. Read the model output in `sample_outputs/<model>/`.
3. Work through `hallucination_detection_checklist.md` and
   `compliance_review_checklist.md`.
4. Assign each of the seven dimensions a 1–5 score with a one-line justification.
5. Record any critical flags and reviewer notes in the scores JSON under
   `sample_outputs/reviewed/`.
6. Run the evaluator to aggregate and classify.

## Disclaimer

This rubric and all associated data are for QA demonstration only. Nothing here constitutes
tax, legal, audit, financial, or investment advice.
