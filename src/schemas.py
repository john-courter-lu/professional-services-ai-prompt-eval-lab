"""jsonschema definitions for the lab's two JSON shapes.

Reused by ``evaluator.validate`` and by the schema test in Phase 6, so the rules live in one
place. The score-object schema is derived from ``scoring`` so it can never drift from the
dimension list.
"""

from __future__ import annotations

from . import scoring

USE_CASES = ["tax", "assurance", "advisory", "wealth"]

# A test case = one entry in test_cases/<use_case>_cases.json.
TEST_CASE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "id",
            "use_case",
            "title",
            "input_file",
            "description",
            "expected_criteria",
            "edge_case",
        ],
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "use_case": {"enum": USE_CASES},
            "title": {"type": "string", "minLength": 1},
            "input_file": {"type": "string", "minLength": 1},
            "description": {"type": "string", "minLength": 1},
            "expected_criteria": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "edge_case": {"type": "boolean"},
            "notes": {"type": "string"},
        },
    },
}

# The per-dimension score object: every dimension required, integer 1-5, nothing extra.
_SCORES_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": list(scoring.DIMENSIONS),
    "properties": {
        dim: {
            "type": "integer",
            "minimum": scoring.SCORE_MIN,
            "maximum": scoring.SCORE_MAX,
        }
        for dim in scoring.DIMENSIONS
    },
}

# A reviewed score file = one human review of one (case, model) output.
REVIEWED_SCORE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["case_id", "model", "output_file", "scores", "reviewer"],
    "properties": {
        "case_id": {"type": "string", "minLength": 1},
        "model": {"type": "string", "minLength": 1},
        "output_file": {"type": "string", "minLength": 1},
        "scores": _SCORES_SCHEMA,
        "reviewer": {"type": "string", "minLength": 1},
        "notes": {"type": "string"},
        "flags": {"type": "array", "items": {"type": "string"}},
    },
}
