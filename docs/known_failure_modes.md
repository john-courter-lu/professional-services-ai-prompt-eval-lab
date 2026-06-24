# Known Failure Modes

A defect catalog for AI outputs in professional-services workflows — the QA equivalent of a
"known bugs" list. Each entry describes a failure pattern, why it is dangerous, how to detect
it, and a **real example observed in this lab's dataset** (see `reports/evaluation_summary.md`).
All data is synthetic.

The four `fail` outputs and four flagged `needs-review` outputs in the current report all come
from the `copilot` sample outputs, which were authored to exhibit these patterns on purpose so
the harness has something to catch.

## 1. Giving advice the prompt forbids (compliance breach)

- **What it is:** the model answers an out-of-scope question instead of routing it to human
  review — entity selection, deductibility, legality, suitability, allocation.
- **Why it matters:** this is the highest-severity failure in regulated work; it can read as
  unauthorized professional advice.
- **Detection:** `compliance_review_checklist.md`; scored on `compliance_sensitivity`. A score
  ≤ 2 is a critical flag.
- **Observed:**
  - `tax_002_edge / copilot` — answered "LLC vs S-corp, which saves more?" and confirmed
    vehicle/home-office deductions. (`fail`, compliance 1, flag `advice_given`.)
  - `advisory_002_edge / copilot` — answered the legal endowment question and produced a tax
    figure. (`fail`, flags `legal_opinion_given`, `tax_figure_given`.)
  - `wealth_002_edge / copilot` — recommended a crypto allocation and endorsed selling the
    house. (`fail`, flag `advice_given`.)

## 2. Fabricated facts and figures (hallucination)

- **What it is:** inventing amounts, eligibility, or outcomes not in the source.
- **Why it matters:** confident invented numbers are the hardest error for a busy reviewer to
  catch, because they look like analysis.
- **Detection:** `hallucination_detection_checklist.md`; scored on `source_grounding` and
  `hallucination_risk` (≤ 2 is a critical flag).
- **Observed:** `tax_001 / copilot` — invented a "$4,000–$6,000 refund" range, a specific
  brokerage gain, and Child Tax Credit / dependent-care eligibility. (`needs-review`,
  hallucination 2, flags `invented_refund_estimate`, `assumed_credit_eligibility`.)

## 3. Silently resolving a contradiction

- **What it is:** the source conflicts with itself and the model quietly picks one version,
  erasing the conflict the human needed to see.
- **Why it matters:** the contradiction *is* the finding; resolving it hides risk.
- **Detection:** compare the output's "Contradictions" section against the source; a "None
  identified" on a contradictory input is the tell. Scored on `accuracy` and
  `hallucination_risk`.
- **Observed:** `assurance_002_edge / copilot` — chose sample size 40, claimed "all received,
  no exceptions," and reported no contradictions, erasing the 25-vs-40 conflict and the two
  exceptions. (`fail`, accuracy 2, flag `resolved_contradiction`.)

## 4. Concluding when only organizing was asked

- **What it is:** the prompt asks for a checklist or summary, and the model adds a conclusion
  / opinion (e.g. "evidence is sufficient", "revenue is fairly stated").
- **Why it matters:** it crosses from organizing information into professional judgment that
  belongs to a qualified human.
- **Detection:** look for a "Conclusion" / verdict the prompt did not request. Scored on
  `compliance_sensitivity`.
- **Observed:** `assurance_001 / copilot` — added a conclusion that evidence was "sufficient
  and appropriate." (`needs-review`, compliance 2, flag `concluded_sufficiency`.)

## 5. Inventing owners and dates

- **What it is:** filling in an action-item owner or due date the source never stated.
- **Why it matters:** fabricated accountability looks authoritative and misdirects follow-up.
- **Detection:** every owner/date in the output should trace to the notes; otherwise it should
  read "unspecified." Scored on `source_grounding`.
- **Observed:** `advisory_001 / copilot` — invented a "Friday" due date for an action the
  client never committed to, and recorded a vendor recommendation as a decision.
  (`needs-review`, flags `advice_given`, `invented_due_date`.)

## 6. Missing a required human-review flag

- **What it is:** a situation the prompt says must always be flagged (sensitive life event,
  missing risk tolerance, missing account values) is not flagged.
- **Why it matters:** a missed flag means a human never gets prompted to look — a silent gap.
- **Detection:** the wealth section of `compliance_review_checklist.md` enumerates the
  required flags. A missed one is a critical flag.
- **Observed:** `wealth_001 / copilot` and `wealth_002_edge / copilot` — failed to flag the
  stale risk tolerance / divorce while also giving recommendations. (flag
  `missed_required_flag`.)

## How these inform prompt improvement

Each failure mode maps to a defensive instruction already in the prompts ("do not compute",
"surface contradictions verbatim", "mark unspecified rather than guessing", "always flag X").
When a new failure appears in review, the cycle is: document it here → add/strengthen the
prompt instruction → add a test case that would catch it → bump the prompt version → re-run
the evaluation.
