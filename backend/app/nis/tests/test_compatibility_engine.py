import pytest  # type: ignore
from app.nis.services.compatibility_engine import NISCompatibilityEngine
from app.nis.schemas.user_signal_profile import UserSignalProfile

def get_base_profile():
    return UserSignalProfile(
        emotional_steadiness="STEADY",
        communication_style="DIRECT",
        conflict_repair_style="CALM",
        family_responsibility="HIGH",
        deen_alignment="STRONG",
        marriage_readiness="READY",
        financial_expectation="MODERATE",
        wali_comfort="COMFORTABLE",
        life_direction="ALIGNED",
        self_awareness_level="HIGH",
        social_lifestyle="BALANCED"
    )

def test_strong_pair():
    p1 = get_base_profile()
    p2 = get_base_profile()
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "STRONG_COMPATIBILITY"
    assert res.confidence_level == "HIGH"
    assert res.review_required is False
    assert len(res.dangerous_mismatches) == 0
    assert len(res.shared_strengths) > 0

def test_weak_pair():
    p1 = get_base_profile()
    p2 = get_base_profile()
    p2.communication_style = "INDIRECT"
    p2.conflict_repair_style = "AVOIDANT"
    p2.life_direction = "UNKNOWN_PATH"
    p2.social_lifestyle = "VERY_SOCIAL"
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "WEAK_COMPATIBILITY"
    assert res.review_required is True
    assert len(res.possible_tension_points) >= 4
    assert len(res.dangerous_mismatches) == 0

def test_incompatible_pair():
    p1 = get_base_profile()
    p2 = get_base_profile()
    p1.deen_alignment = "STRONG"
    p2.deen_alignment = "WEAK"
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "INCOMPATIBLE"
    assert res.review_required is True
    assert len(res.dangerous_mismatches) > 0
    assert "Dangerous mismatch in deen alignment." in res.dangerous_mismatches

def test_insufficient_data():
    p1 = get_base_profile()
    p2 = get_base_profile()
    p1.emotional_steadiness = "UNKNOWN"
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "INSUFFICIENT_DATA"
    assert res.confidence_level == "UNKNOWN"
    assert res.review_required is True
    assert "Insufficient data to calculate compatibility." in res.possible_tension_points

def test_manageable_difference():
    p1 = get_base_profile()
    p2 = get_base_profile()
    p2.communication_style = "INDIRECT"
    p2.social_lifestyle = "HOMEBODY"
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "MODERATE_COMPATIBILITY"
    assert res.review_required is False
    assert any("Manageable difference" in t for t in res.possible_tension_points)

def test_dangerous_mismatch():
    p1 = get_base_profile()
    p2 = get_base_profile()
    p1.financial_expectation = "HIGH"
    p2.financial_expectation = "LOW"
    res = NISCompatibilityEngine.evaluate(p1, p2)
    assert res.compatibility_status == "INCOMPATIBLE"
    assert res.review_required is True
    assert any("Dangerous mismatch in financial expectation." in d for d in res.dangerous_mismatches)

def test_no_output_recommends_marriage():
    res = NISCompatibilityEngine.evaluate(get_base_profile(), get_base_profile())
    notes_dump = " ".join([d.notes.replace("marriage readiness", "readiness") for d in res.dimension_results if d.notes] + res.possible_tension_points + res.dangerous_mismatches + [res.reasoning_summary]).lower()
    assert "marry" not in notes_dump and "marriage" not in notes_dump

def test_no_raw_private_data_exposed():
    res = NISCompatibilityEngine.evaluate(get_base_profile(), get_base_profile())
    dump = res.model_dump_json()
    assert "raw_raya" not in dump
    assert "worship_score" not in dump

def test_no_score_fields_exposed():
    res = NISCompatibilityEngine.evaluate(get_base_profile(), get_base_profile())
    dump = res.model_dump_json()
    assert "overall_score" not in dump
    assert "compatibility_percentage" not in dump
    assert "match_percentage" not in dump
    assert "is_compatible" not in dump
