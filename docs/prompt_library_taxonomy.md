# Prompt Library Taxonomy

How the prompts in this lab are organized, named, and versioned, so the library stays
navigable as it grows. All data is synthetic; nothing here is professional advice.

## Organizing principle

One prompt per **professional-services use case**. Each prompt is a self-contained, versioned
asset that turns a messy synthetic input into a structured, review-ready output — and
explicitly stays inside a no-advice boundary.

| Use case | Prompt id | Title | Input → Output |
| -------- | --------- | ----- | -------------- |
| Tax | `tax_intake_summary` | Tax Intake Summary & Missing-Information Finder | Intake notes → summary + missing-info + advice-request flags |
| Assurance | `assurance_evidence_checklist` | Audit Evidence Completeness Checklist | Evidence notes → Present/Partial/Missing checklist + gaps |
| Advisory | `advisory_meeting_summary` | Advisory Meeting Notes → Risks, Decisions & Follow-ups | Meeting notes → decisions / risks / action items |
| Wealth | `wealth_review_prep` | Wealth Client Review-Prep Summary | Profile notes → review prep + required human-review flags |

## Anatomy of a prompt

Every `prompts/*.md` file has the same shape, which the test cases and rubric rely on:

- **YAML frontmatter** — `id`, `version` (semver), `use_case`, `title`, `last_updated`,
  `owner`, `status`.
- **Purpose** — what it does and, just as important, what it does **not** do.
- **Input contract** — what the input is and what to assume about it (messy, partial,
  possibly contradictory).
- **Instructions** — the numbered rules, always including "summarize only what's present,
  don't invent, flag what's missing, do not give advice."
- **Output format** — the exact named sections the output must contain (this is what
  `format_adherence` is scored against).
- **Disclaimer** — a verbatim no-advice line that must appear in every output.

## Versioning convention

Prompts use **semantic versioning** in the frontmatter `version` field:

- **patch** (`1.0.0 → 1.0.1`) — wording/clarity fix that does not change expected output.
- **minor** (`1.0.0 → 1.1.0`) — new section or instruction that adds capability without
  breaking existing test cases.
- **major** (`1.0.0 → 2.0.0`) — output-format or contract change that requires updating test
  cases and re-reviewing saved outputs.

Because prompts are plain Markdown in git, every change is a reviewable diff. When a prompt's
behavior changes, bump the version, update `last_updated`, and re-run the evaluation so the
report reflects the new version.

## Naming conventions

- Prompt files: `<use_case>_<purpose>.md` (e.g. `tax_intake_summary.md`).
- Sample inputs: `sample_inputs/<use_case>/<name>_NNN[ _edge].txt`; `_edge` marks an
  edge-case input.
- Test cases: `test_cases/<use_case>_cases.json`; case ids are `<use_case>_NNN[_edge]`.
- Reviewed scores: `sample_outputs/reviewed/<case_id>_<model>.json`.

Keeping these aligned is what lets the evaluator join inputs → cases → outputs → scores
without any central index.

## Related docs

- `how_to_add_a_new_prompt.md` — the step-by-step for extending the library.
- `known_failure_modes.md` — the failure patterns these prompts are designed to resist.
- `human_review_guidelines.md` — how a reviewer scores outputs against the rubric.
