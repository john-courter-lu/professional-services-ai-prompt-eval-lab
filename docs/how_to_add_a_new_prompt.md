# How to Add a New Prompt

The end-to-end workflow for extending the lab with a new prompt (or a new use case), so the
evaluator and tests keep passing. All data must be **synthetic**; every output must carry the
no-advice disclaimer.

## Overview

A prompt is only "done" in this lab when it has: synthetic inputs, test cases, at least one
reviewed output, and a green `validate` + `pytest`. The steps below produce exactly that.

## 1. Write the prompt

Create `prompts/<use_case>_<purpose>.md` following the structure in
`prompt_library_taxonomy.md`:

- YAML frontmatter: `id`, `version: 1.0.0`, `use_case`, `title`, `last_updated`, `owner`,
  `status: active`.
- Sections: Purpose, Input contract, Instructions, Output format, Disclaimer.
- Bake the defenses in: "summarize only what's present", "do not invent", "flag what's
  missing", "do not give advice — route to Human-Review Flags", and a verbatim disclaimer.

If the use case is new (not tax/assurance/advisory/wealth), add it to the `USE_CASES` list in
`src/schemas.py` so the schema will accept it.

## 2. Add synthetic inputs

Create `sample_inputs/<use_case>/<name>_001.txt` and at least one `_002_edge.txt`. Make them
realistically messy, and design the edge case to exercise a failure mode from
`known_failure_modes.md` (missing data, a contradiction, an out-of-scope advice request).

## 3. Add test cases

Add (or create) `test_cases/<use_case>_cases.json` — a JSON array of cases. Each case needs:

```json
{
  "id": "<use_case>_001",
  "use_case": "<use_case>",
  "title": "...",
  "input_file": "sample_inputs/<use_case>/<name>_001.txt",
  "description": "...",
  "expected_criteria": ["...", "..."],
  "edge_case": false,
  "notes": "..."
}
```

`expected_criteria` is the heart of the case — list the specific things a good output must do,
grounded in the input. Case ids must be unique across all files.

## 4. Produce and save an output

Run the prompt against an input in whatever tool you like (this lab is offline and does not
call a model), then save the raw Markdown to `sample_outputs/<model>/<case_id>.md`. Use
`claude` / `copilot` subdirs, or add another model's subdir.

## 5. Score the output

Following `human_review_guidelines.md`, create
`sample_outputs/reviewed/<case_id>_<model>.json` with the seven dimension scores, `reviewer`,
`notes`, and any `flags`.

## 6. Validate and evaluate

```bash
python3 -m src.evaluator validate              # schema + reference checks must pass
python3 -m src.evaluator evaluate --report      # regenerates reports/evaluation_summary.md
python3 -m pytest -q                            # schema tests pick up new files automatically
```

`validate` confirms every new file matches its schema and that all `input_file` / `output_file`
references resolve and `case_id`s are unique. The schema test in `tests/` is parametrized over
the files on disk, so your new files are covered without editing the tests.

## 7. Commit

Commit the prompt, inputs, cases, outputs, scores, and the regenerated report together with a
conventional message (e.g. `feat: add <use_case> prompt and evaluation cases`). The diff is
the reviewable record of the new capability.

## Improving an existing prompt

Same loop, plus version discipline: edit the prompt, bump `version` and `last_updated` per the
semver rules in `prompt_library_taxonomy.md`, add a test case for the behavior you changed, and
re-run steps 6–7. The git history then shows the prompt improving against a stable rubric.
