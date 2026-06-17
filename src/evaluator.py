"""Command-line entry point for the prompt-eval lab.

Usage:
    python -m src.evaluator validate              # schema-check cases + reviewed files
    python -m src.evaluator evaluate              # join scores to cases, print results
    python -m src.evaluator evaluate --report     # also write reports/evaluation_summary.md

The evaluator is fully offline: it reads committed test cases and committed reviewed score
files only. No model is called.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from . import report_generator, scoring, schemas

REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_CASES_DIR = REPO_ROOT / "test_cases"
REVIEWED_DIR = REPO_ROOT / "sample_outputs" / "reviewed"
REPORT_PATH = REPO_ROOT / "reports" / "evaluation_summary.md"


# --- Loading -------------------------------------------------------------------------------

def _load_json(path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_test_cases():
    """Return {case_id: case_dict} across all test_cases/*_cases.json files.

    Raises ValueError on duplicate case ids so the index is unambiguous.
    """
    cases = {}
    for path in sorted(TEST_CASES_DIR.glob("*_cases.json")):
        for case in _load_json(path):
            cid = case.get("id")
            if cid in cases:
                raise ValueError(f"duplicate case id {cid!r} (in {path.name})")
            cases[cid] = case
    return cases


def load_reviewed():
    """Return a list of (path, dict) for every sample_outputs/reviewed/*.json file."""
    if not REVIEWED_DIR.exists():
        return []
    return [(p, _load_json(p)) for p in sorted(REVIEWED_DIR.glob("*.json"))]


# --- validate ------------------------------------------------------------------------------

def _schema_errors(validator, data):
    return [
        f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
        for e in validator.iter_errors(data)
    ]


def cmd_validate(_args):
    """Schema-check all test cases and reviewed files; verify referenced files exist."""
    case_validator = Draft202012Validator(schemas.TEST_CASE_SCHEMA)
    reviewed_validator = Draft202012Validator(schemas.REVIEWED_SCORE_SCHEMA)
    problems = []
    checked = 0

    case_files = sorted(TEST_CASES_DIR.glob("*_cases.json"))
    if not case_files:
        problems.append(f"no *_cases.json found in {TEST_CASES_DIR}")

    case_ids = set()
    for path in case_files:
        data = _load_json(path)
        for err in _schema_errors(case_validator, data):
            problems.append(f"{path.name}: {err}")
        for case in data if isinstance(data, list) else []:
            checked += 1
            cid = case.get("id")
            if cid in case_ids:
                problems.append(f"{path.name}: duplicate case id {cid!r}")
            case_ids.add(cid)
            ref = case.get("input_file")
            if ref and not (REPO_ROOT / ref).is_file():
                problems.append(f"{path.name}: {cid}: input_file not found: {ref}")

    for path, data in load_reviewed():
        checked += 1
        errs = _schema_errors(reviewed_validator, data)
        for err in errs:
            problems.append(f"{path.name}: {err}")
        if errs:
            continue  # structure invalid; skip cross-checks
        if data["case_id"] not in case_ids:
            problems.append(f"{path.name}: case_id {data['case_id']!r} has no matching test case")
        out = data["output_file"]
        if not (REPO_ROOT / out).is_file():
            problems.append(f"{path.name}: output_file not found: {out}")

    if problems:
        print(f"VALIDATION FAILED — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"VALIDATION PASSED — {checked} file/case record(s) checked, no problems.")
    return 0


# --- evaluate ------------------------------------------------------------------------------

def build_records(cases, reviewed):
    """Join reviewed scores to their test cases and compute scoring outcomes."""
    records = []
    for path, data in reviewed:
        case = cases.get(data["case_id"], {})
        outcome = scoring.evaluate_scores(data["scores"], data.get("flags"))
        records.append({
            "case_id": data["case_id"],
            "use_case": case.get("use_case", "unknown"),
            "title": case.get("title", ""),
            "model": data["model"],
            "output_file": data["output_file"],
            "reviewer": data["reviewer"],
            "scores": data["scores"],
            "aggregate": outcome["aggregate"],
            "flags": outcome["flags"],
            "classification": outcome["classification"],
            "source": path.name,
        })
    return records


def cmd_evaluate(args):
    """Join reviewed scores to cases, print a table, and optionally write the report."""
    cases = load_test_cases()
    reviewed = load_reviewed()

    if not reviewed:
        print("No reviewed outputs found under sample_outputs/reviewed/.")
        print("Add scored JSON files there (Phase 5) and re-run.")
        if args.report:
            path = report_generator.write_report([], REPORT_PATH)
            print(f"Wrote empty report to {path.relative_to(REPO_ROOT)}")
        return 0

    records = build_records(cases, reviewed)

    print(f"Evaluated {len(records)} output(s):\n")
    header = f"{'case_id':22} {'model':10} {'agg':>5}  {'result':12} flags"
    print(header)
    print("-" * len(header))
    for r in sorted(records, key=lambda x: (x["use_case"], x["case_id"], x["model"])):
        flag_note = f"{len(r['flags'])} flag(s)" if r["flags"] else "-"
        print(f"{r['case_id']:22} {r['model']:10} {r['aggregate']:5.2f}  "
              f"{r['classification']:12} {flag_note}")

    if args.report:
        path = report_generator.write_report(records, REPORT_PATH)
        print(f"\nWrote report to {path.relative_to(REPO_ROOT)}")
    return 0


# --- CLI wiring ----------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python -m src.evaluator",
        description="Offline evaluator for the prompt-eval lab (synthetic data only).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="schema-check cases + reviewed files")
    p_validate.set_defaults(func=cmd_validate)

    p_evaluate = sub.add_parser("evaluate", help="join scores to cases and report results")
    p_evaluate.add_argument("--report", action="store_true",
                            help="write reports/evaluation_summary.md")
    p_evaluate.set_defaults(func=cmd_evaluate)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
