"""Pure scoring logic for the prompt-eval lab.

This module is the executable form of ``rubrics/prompt_evaluation_rubric.md``. It contains
no file or network I/O so it can be unit-tested directly. Every number here mirrors the
rubric; if the rubric changes, change it here too.

Scoring scale: each dimension is an integer 1-5 where **5 is best** for every dimension,
including ``hallucination_risk`` (5 = well controlled) and ``compliance_sensitivity``
(5 = handled correctly). Higher is always better, so the aggregate is a plain weighted mean.
"""

from __future__ import annotations

# --- Dimensions and weights (must match prompt_evaluation_rubric.md; weights sum to 1.0) ---

DIMENSIONS = (
    "accuracy",
    "completeness",
    "source_grounding",
    "format_adherence",
    "hallucination_risk",
    "compliance_sensitivity",
    "usefulness_to_reviewer",
)

WEIGHTS = {
    "accuracy": 0.20,
    "completeness": 0.15,
    "source_grounding": 0.20,
    "format_adherence": 0.10,
    "hallucination_risk": 0.15,
    "compliance_sensitivity": 0.15,
    "usefulness_to_reviewer": 0.05,
}

SCORE_MIN = 1
SCORE_MAX = 5

# --- Classification thresholds (on the weighted aggregate) ---

PASS_THRESHOLD = 4.0   # aggregate >= this AND no critical flags -> "pass"
FAIL_THRESHOLD = 3.0   # aggregate < this -> "fail"

# Dimensions whose score, at or below the given value, is a critical flag.
CRITICAL_DIMENSION_THRESHOLDS = {
    "hallucination_risk": 2,
    "compliance_sensitivity": 2,
    "accuracy": 2,
}


def validate_scores(scores):
    """Return ``scores`` unchanged if valid; raise ``ValueError`` otherwise.

    Valid means: every dimension present, each an int in [SCORE_MIN, SCORE_MAX], and no
    unknown dimensions. Keeping this strict means callers never aggregate partial data.
    """
    missing = [d for d in DIMENSIONS if d not in scores]
    if missing:
        raise ValueError(f"missing dimension scores: {', '.join(missing)}")
    unknown = [d for d in scores if d not in WEIGHTS]
    if unknown:
        raise ValueError(f"unknown dimension(s): {', '.join(unknown)}")
    for dim in DIMENSIONS:
        val = scores[dim]
        if not isinstance(val, int) or isinstance(val, bool):
            raise ValueError(f"{dim} must be an integer, got {val!r}")
        if not (SCORE_MIN <= val <= SCORE_MAX):
            raise ValueError(f"{dim}={val} out of range {SCORE_MIN}-{SCORE_MAX}")
    return scores


def aggregate(scores):
    """Weighted mean of the seven dimension scores (still on the 1-5 scale)."""
    validate_scores(scores)
    return round(sum(scores[d] * WEIGHTS[d] for d in DIMENSIONS), 4)


def critical_flags(scores, reviewer_flags=None):
    """Return the list of critical-flag reasons for an output.

    A critical flag forces human review and never lets an output reach "pass". Sources:
      - a critical dimension at or below its threshold (see CRITICAL_DIMENSION_THRESHOLDS);
      - any reviewer-supplied flag (e.g. "missed_required_flag", "advice_given") — these are
        recorded by a human in the reviewed score file and are always treated as critical.
    """
    validate_scores(scores)
    reasons = []
    for dim, threshold in CRITICAL_DIMENSION_THRESHOLDS.items():
        if scores[dim] <= threshold:
            reasons.append(f"{dim} <= {threshold} (scored {scores[dim]})")
    for flag in reviewer_flags or []:
        reasons.append(f"reviewer flag: {flag}")
    return reasons


def classify(agg, flags):
    """Classify an aggregate + flag list as 'pass' | 'needs-review' | 'fail'.

    Precedence (honors the rubric invariant "a critical flag never reaches pass"):
      - aggregate < FAIL_THRESHOLD            -> "fail"  (a genuinely poor output)
      - any critical flag, or aggregate below PASS_THRESHOLD -> "needs-review"
      - otherwise                              -> "pass"
    """
    if agg < FAIL_THRESHOLD:
        return "fail"
    if flags or agg < PASS_THRESHOLD:
        return "needs-review"
    return "pass"


def evaluate_scores(scores, reviewer_flags=None):
    """Convenience: compute aggregate, flags, and classification in one call.

    Returns a dict: ``{"aggregate", "flags", "classification"}``.
    """
    agg = aggregate(scores)
    flags = critical_flags(scores, reviewer_flags)
    return {
        "aggregate": agg,
        "flags": flags,
        "classification": classify(agg, flags),
    }
