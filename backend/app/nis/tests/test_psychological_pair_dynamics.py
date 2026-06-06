import pytest
from app.nis.services.compatibility_engine import NISCompatibilityEngine
from app.nis.schemas.user_signal_profile import UserSignalProfile
from app.nis.services.confidence_threshold_service import NISConfidenceThresholdService, CandidateInputs
from app.nis.schemas.hard_filters import HardFilterResult

def get_base_profile() -> UserSignalProfile:
    return UserSignalProfile(
        emotional_steadiness="STEADY",
        anger_intensity="MODERATE",
        conflict_repair_style="PROACTIVE",
        communication_style="DIRECT",
        attachment_needs="SECURE",
        ego_humility="BALANCED",
        family_responsibility="HIGH",
        financial_responsibility="BALANCED",
        financial_expectation="MODERATE",
        marriage_readiness="READY",
        social_lifestyle="BALANCED",
        deen_alignment="STRONG",
        boundary_respect="RESPECTFUL",
        stability_risk="LOW",
        wali_comfort="COMFORTABLE",
        life_direction="BUILDING",
        self_awareness_level="HIGH",
        safety_risk_level="LOW"
    )

def evaluate_pair(p1: UserSignalProfile, p2: UserSignalProfile):
    comp = NISCompatibilityEngine.evaluate(p1, p2)
    inputs = CandidateInputs(
        candidate_user_id="test_candidate",
        hard_filter_result=HardFilterResult(passed=True, status="PASSED", failed_filters=[]),
        compatibility_result=comp,
        safety_risk_level="LOW",
        profile_data_complete=True,
        preference_data_complete=True
    )
    conf = NISConfidenceThresholdService.evaluate_candidate(inputs)
    return comp, conf

def test_angry_plus_angry_is_blocked():
    p1 = get_base_profile()
    p1.anger_intensity = "HIGH"
    
    p2 = get_base_profile()
    p2.anger_intensity = "HIGH"
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.compatibility_status == "INCOMPATIBLE" or comp.review_required is True
    assert "unsafe conflict pressure" in str(comp.dangerous_mismatches)
    assert conf.can_show_candidate is False

def test_calm_plus_expressive_repair_oriented_passes():
    p1 = get_base_profile()
    p1.emotional_steadiness = "STEADY"
    
    p2 = get_base_profile()
    p2.emotional_steadiness = "EXPRESSIVE"
    p2.conflict_repair_style = "PROACTIVE"
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.compatibility_status in ["STRONG_COMPATIBILITY", "MODERATE_COMPATIBILITY"]
    assert conf.can_show_candidate is True
    assert any("Healthy balance of steady calm and expressive communication" in s for s in comp.shared_strengths)

def test_avoidant_plus_emotionally_needy_is_flagged():
    p1 = get_base_profile()
    p1.attachment_needs = "AVOIDANT"
    
    p2 = get_base_profile()
    p2.attachment_needs = "ANXIOUS"
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.review_required is True
    assert "Anxious-avoidant loop risk" in str(comp.dangerous_mismatches)
    assert conf.can_show_candidate is False

def test_strong_deen_but_dangerous_conflict_is_blocked():
    p1 = get_base_profile()
    p1.deen_alignment = "STRONG"
    p1.anger_intensity = "HIGH"
    p1.conflict_repair_style = "AVOIDANT"
    
    p2 = get_base_profile()
    p2.deen_alignment = "STRONG"
    p2.anger_intensity = "HIGH"
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.review_required is True
    assert conf.can_show_candidate is False

def test_financial_irresponsibility_pair_blocked():
    p1 = get_base_profile()
    p1.financial_responsibility = "IRRESPONSIBLE"
    p2 = get_base_profile()
    p2.financial_responsibility = "IRRESPONSIBLE"
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.review_required is True
    assert conf.can_show_candidate is False

def test_not_ready_mismatch_weakens_or_blocks():
    p1 = get_base_profile()
    p1.marriage_readiness = "READY"
    p2 = get_base_profile()
    p2.marriage_readiness = "NOT_READY"
    
    comp, conf = evaluate_pair(p1, p2)
    assert any("marriage readiness" in d for d in comp.dangerous_mismatches)

def test_insufficient_data_gives_insufficient_data():
    p1 = get_base_profile()
    p1.emotional_steadiness = "UNKNOWN"
    p2 = get_base_profile()
    
    comp, conf = evaluate_pair(p1, p2)
    assert comp.compatibility_status == "INSUFFICIENT_DATA"
    assert conf.final_status == "INSUFFICIENT_DATA"
    assert conf.can_show_candidate is False

def test_healthy_complementarity_detected():
    p1 = get_base_profile()
    p1.social_lifestyle = "STRUCTURED"
    p2 = get_base_profile()
    p2.social_lifestyle = "FLEXIBLE"
    
    comp, conf = evaluate_pair(p1, p2)
    assert any("Complementary lifestyle rhythm" in s for s in comp.shared_strengths)

def test_no_compatibility_percentage_exposed():
    comp, conf = evaluate_pair(get_base_profile(), get_base_profile())
    dump = comp.model_dump_json().lower()
    assert "percentage" not in dump
    assert "score" not in dump

def test_forbidden_language_blocked():
    comp, conf = evaluate_pair(get_base_profile(), get_base_profile())
    dump = comp.model_dump_json().lower()
    assert "perfect match" not in dump
    assert "you should marry" not in dump
    assert "guaranteed" not in dump
    assert "allah chose this" not in dump
    assert "soulmate" not in dump
    assert "diagnosis" not in dump
