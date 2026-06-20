"""Data-integrity tests for the committed test cases and reviewed score files.

These guard the data, not the code: every JSON file validates against its schema, referenced
files exist, and cross-references resolve. They are what let `validate` stay trustworthy as
the dataset grows.
"""

import json

import pytest
from jsonschema import Draft202012Validator

from src import evaluator, schemas

# --- discover files (module level so they become test ids) ---------------------------------

CASE_FILES = sorted(evaluator.TEST_CASES_DIR.glob("*_cases.json"))
REVIEWED_FILES = sorted(evaluator.REVIEWED_DIR.glob("*.json"))


def _load(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _all_case_ids():
    ids = set()
    for path in CASE_FILES:
        for case in _load(path):
            ids.add(case["id"])
    return ids


# --- sanity: the dataset actually exists ---------------------------------------------------

def test_case_files_present():
    assert CASE_FILES, "no test_cases/*_cases.json found"


def test_reviewed_files_present():
    assert REVIEWED_FILES, "no sample_outputs/reviewed/*.json found"


# --- schema validation ---------------------------------------------------------------------

@pytest.mark.parametrize("path", CASE_FILES, ids=lambda p: p.name)
def test_case_file_matches_schema(path):
    errors = list(Draft202012Validator(schemas.TEST_CASE_SCHEMA).iter_errors(_load(path)))
    assert not errors, "; ".join(e.message for e in errors)


@pytest.mark.parametrize("path", REVIEWED_FILES, ids=lambda p: p.name)
def test_reviewed_file_matches_schema(path):
    errors = list(Draft202012Validator(schemas.REVIEWED_SCORE_SCHEMA).iter_errors(_load(path)))
    assert not errors, "; ".join(e.message for e in errors)


# --- referential integrity -----------------------------------------------------------------

@pytest.mark.parametrize("path", CASE_FILES, ids=lambda p: p.name)
def test_case_input_files_exist(path):
    for case in _load(path):
        ref = evaluator.REPO_ROOT / case["input_file"]
        assert ref.is_file(), f"{case['id']}: missing input_file {case['input_file']}"


def test_case_ids_are_unique():
    seen, dupes = set(), set()
    for path in CASE_FILES:
        for case in _load(path):
            cid = case["id"]
            if cid in seen:
                dupes.add(cid)
            seen.add(cid)
    assert not dupes, f"duplicate case ids: {sorted(dupes)}"


@pytest.mark.parametrize("path", REVIEWED_FILES, ids=lambda p: p.name)
def test_reviewed_output_files_exist(path):
    data = _load(path)
    ref = evaluator.REPO_ROOT / data["output_file"]
    assert ref.is_file(), f"missing output_file {data['output_file']}"


@pytest.mark.parametrize("path", REVIEWED_FILES, ids=lambda p: p.name)
def test_reviewed_case_ids_resolve(path):
    data = _load(path)
    assert data["case_id"] in _all_case_ids(), f"unknown case_id {data['case_id']!r}"


# --- the validator agrees ------------------------------------------------------------------

def test_evaluator_validate_passes():
    assert evaluator.cmd_validate(None) == 0
