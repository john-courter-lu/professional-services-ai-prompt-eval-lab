# professional-services-ai-prompt-eval-lab

A **prompt evaluation lab** for professional-services workflows. This repository treats
prompts as **testable assets** — it is *not* a chatbot app. It is a QA harness for
writing, testing, scoring, and versioning prompts and AI outputs across four
professional-services use cases:

| Use case | What the prompt does |
| --- | --- |
| **Tax** | Summarize client tax intake notes and identify missing information. |
| **Assurance** | Review audit evidence notes and generate an evidence-completeness checklist. |
| **Advisory** | Turn messy meeting notes into risks, decisions, and follow-up questions. |
| **Wealth Management** | Turn client profile notes into a review-prep summary with human-review flags. |

> ⚠️ **Disclaimer — synthetic data, no advice.** Every input, output, and scenario in
> this repository is **synthetic** and created for demonstration only. Nothing here is
> real client data, and nothing here is tax, legal, financial, audit, or investment
> advice. The lab is a QA / prompt-evaluation demo; all AI outputs are assumed to
> require qualified human review before any real-world use.

---

## The problem this repo solves

Generative AI is being pushed into professional-services work (Tax, Assurance, Advisory,
Wealth) faster than teams can answer the obvious QA questions:

- Does the output actually say what the source says, or did the model **hallucinate**?
- Is it **complete** — did it flag the missing intake fields, the missing audit evidence?
- Does it follow the **required format** every time?
- Does it stay inside **compliance** boundaries (no unauthorized advice, proper caveats)?
- Is it genuinely **useful to the human reviewer**, or just plausible-sounding text?

Without a repeatable way to answer these, "the prompt works" is an opinion. This lab makes
it a **measurement**: prompts are versioned, test cases are explicit, outputs are scored
against a rubric, failure modes are documented, and the whole thing runs from the command
line and produces a report.

## Why it matters for AI Prompt & Skills Engineering

Operationalizing prompts and skills is not "prompt golf." It is the same discipline as
test automation, applied to a non-deterministic system:

- **Prompts as versioned assets** — each prompt has an id, a version, an input contract,
  and an output format, so improvements are reviewable in git like any other code change.
- **Explicit test cases** — messy synthetic inputs plus the criteria a good output must
  meet, including deliberate **edge cases** (missing data, contradictions, requests for
  advice the model should decline).
- **Structured evaluation** — a fixed rubric scores every output on the same dimensions,
  so two reviewers (or the same reviewer over time) stay consistent.
- **Documented failure modes** — known hallucination and compliance traps are written
  down, not rediscovered each time.

## How this maps to my QA / SDET background

I am John Lu, an SDET / QA Automation Engineer moving into prompt and skills engineering.
The translation is direct:

| QA / SDET practice | How it shows up in this lab |
| --- | --- |
| Test case design & edge-case coverage | `test_cases/*.json` with explicit `expected_criteria` and `edge_case` flags |
| Test data management | Synthetic `sample_inputs/` modeling messy, realistic source notes |
| Assertion / pass-fail criteria | Rubric dimensions + scoring thresholds in `src/scoring.py` |
| Defect triage & documentation | `docs/known_failure_modes.md`, reviewer `flags` on scored outputs |
| Schema / contract validation | `jsonschema` validation of every test case and scored output |
| Regression reporting | `reports/evaluation_summary.md` generated from saved results |
| Version control discipline | Prompts versioned in `prompts/`, reviewable per-commit |

This project is intended to demonstrate: prompt engineering, prompt-library organization,
AI output QA, hallucination detection, edge-case testing, compliance-minded review,
version-controlled prompt improvement, and technical documentation for non-technical
reviewers.

---

## How it works (offline by design)

The lab does **not** call any AI model and needs **no API keys or network access**. The
workflow is:

1. A prompt (`prompts/`) is run against a synthetic input (`sample_inputs/`) — outside
   this repo, in whatever tool you like — and the raw output is saved under
   `sample_outputs/claude/` or `sample_outputs/copilot/`.
2. A human reviewer scores that output against the rubric and saves a structured JSON
   record under `sample_outputs/reviewed/`.
3. The evaluator validates everything against a schema, aggregates the scores, and
   generates `reports/evaluation_summary.md`.

This keeps the repo reproducible: anyone can clone it and re-run the evaluation from
committed data alone.

## Repository layout

```
prompts/             Versioned prompt definitions (one per use case)
test_cases/          JSON test cases: synthetic inputs + expected criteria
sample_inputs/       Synthetic source notes (tax / assurance / advisory / wealth)
sample_outputs/
  claude/            Raw AI outputs (synthetic)
  copilot/           Raw AI outputs from a second tool, for comparison
  reviewed/          Human-scored output records (JSON)
rubrics/             Evaluation rubric + hallucination & compliance checklists
src/
  scoring.py         Pure scoring logic (dimensions, weights, pass/fail)
  evaluator.py       CLI: validate test cases & outputs, run evaluation
  report_generator.py  Builds reports/evaluation_summary.md
reports/             Generated evaluation summaries
docs/                Taxonomy, failure modes, review guidelines, how-to-add-a-prompt
tests/               pytest unit tests for scoring and schema
```

## Quick start

Requires Python 3.10+. The lab is offline — no API keys or network needed.

```bash
# 1. Set up an isolated environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Validate all test cases and reviewed outputs against the schema
python -m src.evaluator validate

# 3. Run the evaluation and (re)generate the summary report
python -m src.evaluator evaluate --report

# 4. Run the test suite
pytest -q
```

> No virtualenv? If `jsonschema` and `pytest` are already on your system Python, you can skip
> step 1 and run steps 2–4 directly with `python3 -m src.evaluator ...` and `python3 -m pytest -q`.

The committed [`reports/evaluation_summary.md`](reports/evaluation_summary.md) shows the
current results: 16 outputs across 4 use cases × 2 models, with the deliberately flawed
`copilot` outputs surfacing as `needs-review` / `fail` via critical flags.

## Evaluation dimensions

Every output is scored **1–5 (5 = best)** on seven dimensions:

| Dimension | Question it answers |
| --- | --- |
| Accuracy | Are the stated facts correct relative to the source? |
| Completeness | Did it capture everything required (incl. what's missing)? |
| Source grounding | Is every claim traceable to the input, with nothing invented? |
| Format adherence | Does it match the required output structure? |
| Hallucination risk | *(5 = well controlled)* How free is it of unsupported claims? |
| Compliance sensitivity | *(5 = handled correctly)* Does it stay within scope and caveat properly? |
| Usefulness to reviewer | Does it actually save the human reviewer time? |

Dimension definitions and scoring guidance live in `rubrics/prompt_evaluation_rubric.md`.

## Adding a new prompt

See [`docs/how_to_add_a_new_prompt.md`](docs/how_to_add_a_new_prompt.md). In short: add the
versioned prompt to `prompts/`, add synthetic inputs and test cases, save at least one
reviewed output, then re-run `validate` and `evaluate`.

## Documentation

- [`docs/prompt_library_taxonomy.md`](docs/prompt_library_taxonomy.md) — how prompts are organized, named, and versioned.
- [`docs/known_failure_modes.md`](docs/known_failure_modes.md) — the AI-output defect catalog, with real examples from the dataset.
- [`docs/human_review_guidelines.md`](docs/human_review_guidelines.md) — how a reviewer scores an output against the rubric.
- [`docs/how_to_add_a_new_prompt.md`](docs/how_to_add_a_new_prompt.md) — the end-to-end workflow for extending the lab.

## Current limitations

- **Human-in-the-loop scoring.** Scores are assigned by a reviewer, not computed
  automatically; the lab structures and aggregates judgment rather than replacing it.
- **Offline only.** It evaluates saved outputs; it does not generate them or call a model.
- **Synthetic, small dataset.** It demonstrates method and discipline, not statistical
  significance.
- **Not a substitute for professional review.** Outputs are illustrative; no result here
  should be treated as tax, legal, financial, audit, or investment advice.
