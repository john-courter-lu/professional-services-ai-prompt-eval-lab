"""Unit tests for src.scoring — the pure scoring logic.

These lock in the rubric's math and classification rules so a future edit to scoring.py that
drifts from rubrics/prompt_evaluation_rubric.md fails loudly.
"""

import pytest

from src import scoring


def perfect_scores(value=5):
    """Helper: a full, valid score dict with every dimension set to ``value``."""
    return {dim: value for dim in scoring.DIMENSIONS}


# --- structure / config --------------------------------------------------------------------

def test_weights_cover_every_dimension():
    assert set(scoring.WEIGHTS) == set(scoring.DIMENSIONS)


def test_weights_sum_to_one():
    assert round(sum(scoring.WEIGHTS.values()), 6) == 1.0


def test_thresholds_ordered():
    assert scoring.FAIL_THRESHOLD < scoring.PASS_THRESHOLD


# --- validate_scores -----------------------------------------------------------------------

def test_validate_scores_accepts_valid():
    s = perfect_scores(3)
    assert scoring.validate_scores(s) is s


def test_validate_scores_rejects_missing_dimension():
    s = perfect_scores()
    del s["accuracy"]
    with pytest.raises(ValueError, match="missing dimension"):
        scoring.validate_scores(s)


def test_validate_scores_rejects_unknown_dimension():
    s = perfect_scores()
    s["made_up"] = 5
    with pytest.raises(ValueError, match="unknown dimension"):
        scoring.validate_scores(s)


@pytest.mark.parametrize("bad", [0, 6, -1, 100])
def test_validate_scores_rejects_out_of_range(bad):
    s = perfect_scores()
    s["accuracy"] = bad
    with pytest.raises(ValueError, match="out of range"):
        scoring.validate_scores(s)


@pytest.mark.parametrize("bad", [3.5, "4", None, True])
def test_validate_scores_rejects_non_integer(bad):
    s = perfect_scores()
    s["accuracy"] = bad
    with pytest.raises(ValueError, match="must be an integer"):
        scoring.validate_scores(s)


# --- aggregate -----------------------------------------------------------------------------

def test_aggregate_all_fives_is_five():
    assert scoring.aggregate(perfect_scores(5)) == 5.0


def test_aggregate_all_threes_is_three():
    assert scoring.aggregate(perfect_scores(3)) == 3.0


def test_aggregate_is_weighted_not_plain_mean():
    # accuracy (weight .20) dropped to 1, rest 5 -> 5 - 4*0.20 = 4.2
    s = perfect_scores(5)
    s["accuracy"] = 1
    assert scoring.aggregate(s) == 4.2


def test_aggregate_low_weight_dimension_moves_little():
    # usefulness_to_reviewer (weight .05) dropped to 1 -> 5 - 4*0.05 = 4.8
    s = perfect_scores(5)
    s["usefulness_to_reviewer"] = 1
    assert scoring.aggregate(s) == 4.8


# --- critical_flags ------------------------------------------------------------------------

def test_no_flags_on_clean_scores():
    assert scoring.critical_flags(perfect_scores(5)) == []


@pytest.mark.parametrize("dim", list(scoring.CRITICAL_DIMENSION_THRESHOLDS))
def test_each_critical_dimension_flags_at_threshold(dim):
    s = perfect_scores(5)
    s[dim] = scoring.CRITICAL_DIMENSION_THRESHOLDS[dim]
    flags = scoring.critical_flags(s)
    assert any(dim in f for f in flags)


def test_critical_dimension_does_not_flag_just_above_threshold():
    s = perfect_scores(5)
    s["accuracy"] = scoring.CRITICAL_DIMENSION_THRESHOLDS["accuracy"] + 1
    assert scoring.critical_flags(s) == []


def test_reviewer_flags_are_always_critical():
    flags = scoring.critical_flags(perfect_scores(5), ["advice_given"])
    assert any("advice_given" in f for f in flags)


# --- classify ------------------------------------------------------------------------------

def test_classify_pass_requires_high_aggregate_and_no_flags():
    assert scoring.classify(4.5, []) == "pass"


def test_classify_pass_boundary_inclusive():
    assert scoring.classify(scoring.PASS_THRESHOLD, []) == "pass"


def test_classify_needs_review_band():
    assert scoring.classify(3.5, []) == "needs-review"


def test_classify_flag_blocks_pass_even_with_high_aggregate():
    assert scoring.classify(4.9, ["reviewer flag: advice_given"]) == "needs-review"


def test_classify_fail_below_threshold():
    assert scoring.classify(2.9, []) == "fail"


def test_classify_fail_wins_over_flag():
    # A genuinely poor output is NOT upgraded to needs-review just because it also has a flag.
    assert scoring.classify(2.0, ["compliance_sensitivity <= 2 (scored 1)"]) == "fail"


# --- evaluate_scores (integration of the three) --------------------------------------------

def test_evaluate_scores_clean_pass():
    result = scoring.evaluate_scores(perfect_scores(5))
    assert result == {"aggregate": 5.0, "flags": [], "classification": "pass"}


def test_evaluate_scores_compliance_breach_needs_review():
    s = perfect_scores(5)
    s["compliance_sensitivity"] = 2
    result = scoring.evaluate_scores(s, ["advice_given"])
    assert result["classification"] == "needs-review"
    assert len(result["flags"]) == 2  # dimension flag + reviewer flag


def test_evaluate_scores_all_twos_fails_with_flags():
    result = scoring.evaluate_scores(perfect_scores(2))
    assert result["classification"] == "fail"
    assert result["aggregate"] == 2.0
    assert result["flags"]  # accuracy/hallucination/compliance all <= 2
