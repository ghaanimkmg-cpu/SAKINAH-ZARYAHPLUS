import pytest  # type: ignore
from app.nis.services.confidence_threshold_service import NISConfidenceThresholdService, CandidateInputs
from app.nis.schemas.hard_filters import HardFilterResult
from app.nis.schemas.compatibility import CompatibilityResult
from app.nis.schemas.confidence_thresholds import NoMatchResult

def get_base_inputs():
    return CandidateInputs(
        candidate_user_id="user_123",
        hard_filter_result=HardFilterResult(passed=True, status="PASSED", failed_filters=[]),
        compatibility_result=CompatibilityResult(
            compatibility_status="STRONG_COMPATIBILITY",
            confidence_level="HIGH",
            dimension_results=[],
            shared_strengths=["Lots in common"],
            possible_tension_points=[],
            dangerous_mismatches=[],
            reasoning_summary="Great match",
            review_required=False
        ),
        safety_risk_level="LOW",
        profile_data_complete=True,
        preference_data_complete=True
    )

def test_strong_candidate_becomes_high_confidence():
    inputs = get_base_inputs()
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "HIGH_CONFIDENCE_MATCH"
    assert res.can_show_candidate is True
    assert res.requires_human_review is False

def test_weak_candidate_becomes_low_confidence():
    inputs = get_base_inputs()
    inputs.compatibility_result.compatibility_status = "WEAK_COMPATIBILITY"
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "LOW_CONFIDENCE_DO_NOT_SHOW"
    assert res.can_show_candidate is False
    assert res.requires_human_review is False

def test_missing_data_becomes_insufficient_data():
    inputs = get_base_inputs()
    inputs.profile_data_complete = False
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "INSUFFICIENT_DATA"
    assert res.can_show_candidate is False
    assert res.requires_human_review is True

def test_hard_filter_failure_becomes_hard_reject():
    inputs = get_base_inputs()
    inputs.hard_filter_result.passed = False
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "HARD_REJECT"
    assert res.can_show_candidate is False

def test_high_safety_risk_becomes_safety_reject():
    inputs = get_base_inputs()
    inputs.safety_risk_level = "HIGH"
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "SAFETY_REJECT"
    assert res.can_show_candidate is False
    assert res.requires_human_review is True

def test_moderate_unclear_case_becomes_moderate_confidence_review():
    inputs = get_base_inputs()
    inputs.compatibility_result.compatibility_status = "MODERATE_COMPATIBILITY"
    res = NISConfidenceThresholdService.evaluate_candidate(inputs)
    assert res.final_status == "MODERATE_CONFIDENCE_REVIEW"
    assert res.can_show_candidate is False
    assert res.requires_human_review is True

def test_no_suitable_candidates_returns_no_match():
    inputs1 = get_base_inputs()
    inputs1.hard_filter_result.passed = False
    
    inputs2 = get_base_inputs()
    inputs2.compatibility_result.compatibility_status = "WEAK_COMPATIBILITY"
    
    pool = [inputs1, inputs2]
    res = NISConfidenceThresholdService.evaluate_pool(pool)
    assert isinstance(res, NoMatchResult)
    assert res.status == "NO_SUITABLE_MATCHES_RIGHT_NOW"

def test_threshold_is_never_lowered():
    # A moderate candidate in an empty pool should NOT become HIGH_CONFIDENCE
    inputs = get_base_inputs()
    inputs.compatibility_result.compatibility_status = "MODERATE_COMPATIBILITY"
    
    res = NISConfidenceThresholdService.evaluate_pool([inputs])
    assert isinstance(res, NoMatchResult)
    assert res.status == "NO_SUITABLE_MATCHES_RIGHT_NOW"
    
def test_no_compatibility_percentage_is_returned():
    res = NISConfidenceThresholdService.evaluate_candidate(get_base_inputs())
    dump = res.model_dump_json()
    assert "percentage" not in dump

def test_no_perfect_match_or_marriage_recommendation():
    res = NISConfidenceThresholdService.evaluate_candidate(get_base_inputs())
    dump = res.model_dump_json().lower()
    assert "perfect match" not in dump
    assert "marriage" not in dump
    assert "marry" not in dump

def test_no_raw_private_data_exposed():
    res = NISConfidenceThresholdService.evaluate_candidate(get_base_inputs())
    dump = res.model_dump_json()
    assert "raw_raya" not in dump
