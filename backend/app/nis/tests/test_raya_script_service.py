import pytest  # type: ignore
from app.nis.services.raya_script_service import NISRayaScriptService
from app.nis.schemas.raya_explanations import RayaScriptInputs, RayaExplanationResult

def test_strong_candidate_explanation():
    inputs = RayaScriptInputs(
        shared_strengths=["steadiness", "family responsibility"],
        possible_tension_points=[],
        final_status="HIGH_CONFIDENCE_MATCH"
    )
    res = NISRayaScriptService.generate_explanation(inputs)
    assert res.title == "A gentle point of alignment"
    assert "steadiness" in res.preview
    assert "exploring gently" in res.explanation
    assert res.tone == "GENTLE"

def test_tension_point_explanation():
    inputs = RayaScriptInputs(
        shared_strengths=["deen"],
        possible_tension_points=["communication rhythm"],
        final_status="HIGH_CONFIDENCE_MATCH"
    )
    res = NISRayaScriptService.generate_explanation(inputs)
    assert "thoughtful point to discuss" in res.preview
    assert "communication rhythm" in res.preview
    assert res.tone == "BALANCED"

def test_no_match_explanation():
    inputs = RayaScriptInputs(no_match_status=True)
    res = NISRayaScriptService.generate_explanation(inputs)
    assert res.title == "Nothing suitable enough right now"
    assert res.tone == "PROTECTIVE"
    assert "better to wait" in res.explanation

def test_review_required_explanation():
    inputs = RayaScriptInputs(review_required=True)
    res = NISRayaScriptService.generate_explanation(inputs)
    assert res.tone == "CAUTIOUS"
    assert "invitation to reflect" in res.explanation

def test_forbidden_phrases_blocked():
    # Verify the service never generates these phrases
    inputs = RayaScriptInputs(shared_strengths=["something"])
    res = NISRayaScriptService.generate_explanation(inputs)
    dump = res.model_dump_json().lower()
    
    forbidden = [
        "you should marry",
        "perfect match",
        "allah chose",
        "guaranteed",
        "you should proceed",
        "do not miss this",
        "soulmate",
        "definitely right"
    ]
    for f in forbidden:
        assert f not in dump

def test_no_compatibility_percentage_appears():
    inputs = RayaScriptInputs(shared_strengths=["something"])
    res = NISRayaScriptService.generate_explanation(inputs)
    dump = res.model_dump_json().lower()
    assert "percentage" not in dump
    assert "%" not in dump

def test_raw_fields_ignored():
    # Pydantic ConfigDict(extra='ignore') should drop extra fields like worship_score and raw_raya
    data = {
        "shared_strengths": ["test"],
        "worship_score": 100,
        "raw_raya": "hello",
        "raw_barakah": "world"
    }
    inputs = RayaScriptInputs(**data)
    assert not hasattr(inputs, "worship_score")
    assert not hasattr(inputs, "raw_raya")
    assert not hasattr(inputs, "raw_barakah")
