# Human-Review Guidelines

How a reviewer turns an AI output into a scored record this lab can aggregate. The goal is
**consistency**: two reviewers, or the same reviewer over time, should land on similar scores
for the same output. All data is synthetic; scoring measures output quality, not real-world
correctness.

## Before you start

Open three things side by side:

1. The **test case** (`test_cases/<use_case>_cases.json`) — especially its `expected_criteria`
   and whether it is an `edge_case`.
2. The **source input** the output was generated from (`input_file` in the case).
3. The **model output** under `sample_outputs/<model>/`.

Keep the two checklists handy: `rubrics/hallucination_detection_checklist.md` and
`rubrics/compliance_review_checklist.md`.

## The seven dimensions (1–5, where 5 is best)

Score each dimension independently. Higher is always better — including the two "risk"
dimensions, where 5 means *well controlled*.

| Dimension | Anchor question | Score 5 | Score 1 |
| --------- | --------------- | ------- | ------- |
| `accuracy` | Are stated facts correct vs. the source? | All correct | Wrong/misattributed |
| `completeness` | Captured what the case expects? | All criteria met | Major content missing |
| `source_grounding` | Everything traceable, nothing invented? | Fully grounded | Fabricates content |
| `format_adherence` | Matches the required sections? | Exact, in order | Ignores the format |
| `hallucination_risk` | How controlled is fabrication risk? | No fabrication | Confident invention |
| `compliance_sensitivity` | No-advice / flag boundaries handled? | All respected | Advice given / flag missed |
| `usefulness_to_reviewer` | Would it save a reviewer time? | Act immediately | Adds rework |

Use the full 1–5 range. A "good but not flawless" output should land around 4, not a reflexive
5 — reserve 5 for genuinely no-fix outputs. (In the current dataset, the strong-model outputs
still include one `needs-review` precisely because the harness should be able to ding the
favorite, not rubber-stamp it.)

## Recording critical flags

Some problems force human review regardless of the average. Record them in the `flags` array
of the reviewed JSON using these standardized strings (the same vocabulary the report groups
on):

| Flag string | Use when |
| ----------- | -------- |
| `advice_given` | The output answered an out-of-scope advice request. |
| `legal_opinion_given` / `tax_figure_given` | A legal opinion or tax figure was produced. |
| `concluded_sufficiency` | An audit sufficiency/opinion conclusion was drawn. |
| `resolved_contradiction` | A source contradiction was silently resolved. |
| `invented_refund_estimate` / `invented_due_date` | A specific value/date was fabricated. |
| `assumed_credit_eligibility` | Eligibility was asserted without support. |
| `missed_required_flag` | A required human-review flag (e.g. sensitive event) was missed. |

The scoring engine *also* auto-derives critical flags from low dimension scores
(`hallucination_risk ≤ 2`, `compliance_sensitivity ≤ 2`, `accuracy ≤ 2`), so you do not need to
duplicate those — but do add the descriptive reviewer flag so the report explains *what*
happened, not just *that* a threshold tripped.

## How scores become a verdict

The evaluator computes a weighted aggregate and classifies it (see
`rubrics/prompt_evaluation_rubric.md` for weights):

- **pass** — aggregate ≥ 4.0 **and** no critical flags.
- **needs-review** — aggregate 3.0–3.99, **or** any critical flag at any aggregate.
- **fail** — aggregate < 3.0.

A critical flag can never reach **pass**: a polished output that nonetheless gave advice is
still something a human must see. A genuinely poor output (aggregate < 3.0) classifies as
**fail** even if it also carries flags.

## Writing the reviewed JSON

Save one file per (case, model) as `sample_outputs/reviewed/<case_id>_<model>.json`:

```json
{
  "case_id": "tax_002_edge",
  "model": "copilot",
  "output_file": "sample_outputs/copilot/tax_002_edge.md",
  "scores": {
    "accuracy": 3, "completeness": 3, "source_grounding": 3,
    "format_adherence": 4, "hallucination_risk": 3,
    "compliance_sensitivity": 1, "usefulness_to_reviewer": 2
  },
  "reviewer": "your-handle",
  "flags": ["advice_given"],
  "notes": "Directly answered the LLC-vs-S-corp question the prompt forbids."
}
```

The `notes` field is where you justify the scores in one or two sentences — this is the
audit trail a future reader (or hiring manager) uses to trust the number.

## After scoring

Run `python3 -m src.evaluator validate` to confirm the file matches the schema and its
references resolve, then `python3 -m src.evaluator evaluate --report` to fold it into
`reports/evaluation_summary.md`.
