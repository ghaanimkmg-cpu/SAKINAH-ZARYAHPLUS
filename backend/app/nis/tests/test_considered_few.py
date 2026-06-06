import pytest  # type: ignore
from app.nis.services.considered_few_service import NISConsideredFewService, ConsideredFewInput
from app.nis.schemas.confidence_thresholds import CandidateConfidenceResult

def get_base_confidence_result(status="HIGH_CONFIDENCE_MATCH", can_show=True):
    return CandidateConfidenceResult(
        candidate_user_id="user_123",
        final_status=status,
        confidence_level="HIGH" if status == "HIGH_CONFIDENCE_MATCH" else "LOW",
        can_show_candidate=can_show,
        requires_human_review=False,
        reasons=["Good match"],
        blocked_reasons=[]
    )

def get_base_input(status="HIGH_CONFIDENCE_MATCH", can_show=True):
    return ConsideredFewInput(
        confidence_result=get_base_confidence_result(status, can_show),
        shared_strengths=["family"],
        possible_tension_points=[]
    )

def test_only_high_confidence_returned():
    inputs = [
        get_base_input("HIGH_CONFIDENCE_MATCH", True),
        get_base_input("LOW_CONFIDENCE_DO_NOT_SHOW", False),
        get_base_input("MODERATE_CONFIDENCE_REVIEW", False),
        get_base_input("HARD_REJECT", False),
        get_base_input("SAFETY_REJECT", False),
    ]
    res = NISConsideredFewService.generate_pool(inputs)
    assert res.status == "HAS_CANDIDATES"
    assert len(res.candidates) == 1
    assert res.candidates[0].confidence_level == "HIGH"

def test_pool_size_never_exceeds_5():
    inputs = [get_base_input() for _ in range(10)]
    res = NISConsideredFewService.generate_pool(inputs)
    assert len(res.candidates) == 5

def test_pool_can_return_fewer_than_3():
    inputs = [get_base_input(), get_base_input()]
    res = NISConsideredFewService.generate_pool(inputs)
    assert len(res.candidates) == 2

def test_empty_candidate_list_returns_no_suitable_matches():
    res = NISConsideredFewService.generate_pool([])
    assert res.status == "NO_SUITABLE_MATCHES_RIGHT_NOW"
    assert len(res.candidates) == 0

def test_weak_candidates_not_added_to_avoid_empty_state():
    inputs = [get_base_input("LOW_CONFIDENCE_DO_NOT_SHOW", False)]
    res = NISConsideredFewService.generate_pool(inputs)
    assert res.status == "NO_SUITABLE_MATCHES_RIGHT_NOW"
    assert len(res.candidates) == 0

def test_no_photos_returned():
    inputs = [get_base_input()]
    res = NISConsideredFewService.generate_pool(inputs)
    assert res.candidates[0].photo_visible is False
    dump = res.model_dump_json()
    assert "photo_url" not in dump

def test_no_raw_private_data_or_percentages_returned():
    inputs = [get_base_input()]
    res = NISConsideredFewService.generate_pool(inputs)
    dump = res.model_dump_json()
    assert "raw_raya" not in dump
    assert "worship_score" not in dump
    assert "percentage" not in dump
    assert "swipe" not in dump
    assert "feed" not in dump

def test_no_marriage_recommendation():
    inputs = [get_base_input()]
    res = NISConsideredFewService.generate_pool(inputs)
    dump = res.model_dump_json().lower()
    assert "marry" not in dump
    assert "marriage" not in dump
    assert "perfect match" not in dump
