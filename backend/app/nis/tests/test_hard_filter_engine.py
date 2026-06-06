import pytest  # type: ignore
from app.nis.services.hard_filter_engine import NISHardFilterEngine, FilterCandidateState, FilterPreferences

def get_base_state():
    return FilterCandidateState(
        is_verified=True,
        is_banned=False,
        is_under_review=False,
        has_profile=True,
        has_preferences=True,
        age=25,
        active_conversations=0,
        location="USA",
        timeline="1_YEAR",
        tradition="MODERN",
        wali="MODERATE",
        marital_status="NEVER_MARRIED",
        relocation_openness="NO"
    )

def get_base_prefs():
    return FilterPreferences(
        age_min=20,
        age_max=30,
        location_pref="ANY",
        timeline_pref="ANY",
        tradition_pref="ANY",
        wali_pref="ANY",
        marital_status_pref="ANY"
    )

def test_verified_users_pass():
    res = NISHardFilterEngine.evaluate(get_base_state(), get_base_prefs(), get_base_state(), get_base_prefs())
    assert res.passed is True
    assert res.status == "PASSED"

def test_unverified_fails():
    u_state = get_base_state()
    u_state.is_verified = False
    res = NISHardFilterEngine.evaluate(u_state, get_base_prefs(), get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "VERIFICATION" for f in res.failed_filters)

def test_banned_user_fails():
    c_state = get_base_state()
    c_state.is_banned = True
    res = NISHardFilterEngine.evaluate(get_base_state(), get_base_prefs(), c_state, get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "BANNED" for f in res.failed_filters)

def test_under_review_fails():
    c_state = get_base_state()
    c_state.is_under_review = True
    res = NISHardFilterEngine.evaluate(get_base_state(), get_base_prefs(), c_state, get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "UNDER_REVIEW" for f in res.failed_filters)

def test_incomplete_profile_fails():
    u_state = get_base_state()
    u_state.has_profile = False
    res = NISHardFilterEngine.evaluate(u_state, get_base_prefs(), get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "INCOMPLETE_PROFILE" for f in res.failed_filters)

def test_incomplete_preferences_fail():
    c_state = get_base_state()
    c_state.has_preferences = False
    res = NISHardFilterEngine.evaluate(get_base_state(), get_base_prefs(), c_state, get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "INCOMPLETE_PREFERENCES" for f in res.failed_filters)

def test_age_mismatch_fails():
    u_state = get_base_state()
    u_state.age = 40
    res = NISHardFilterEngine.evaluate(u_state, get_base_prefs(), get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "AGE" for f in res.failed_filters)

def test_location_mismatch_fails():
    u_prefs = get_base_prefs()
    u_prefs.location_pref = "UK"
    res = NISHardFilterEngine.evaluate(get_base_state(), u_prefs, get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "LOCATION" for f in res.failed_filters)

def test_nikah_timeline_mismatch_fails():
    u_prefs = get_base_prefs()
    u_prefs.timeline_pref = "IMMEDIATE"
    res = NISHardFilterEngine.evaluate(get_base_state(), u_prefs, get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "NIKAH_TIMELINE" for f in res.failed_filters)

def test_tradition_preference_mismatch_fails():
    u_prefs = get_base_prefs()
    u_prefs.tradition_pref = "TRADITIONAL"
    res = NISHardFilterEngine.evaluate(get_base_state(), u_prefs, get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "TRADITION" for f in res.failed_filters)

def test_wali_preference_mismatch_fails():
    u_prefs = get_base_prefs()
    u_prefs.wali_pref = "HIGH"
    res = NISHardFilterEngine.evaluate(get_base_state(), u_prefs, get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "WALI_INVOLVEMENT" for f in res.failed_filters)

def test_active_conversation_cap_blocks():
    u_state = get_base_state()
    u_state.active_conversations = 1
    res = NISHardFilterEngine.evaluate(u_state, get_base_prefs(), get_base_state(), get_base_prefs())
    assert res.passed is False
    assert any(f.filter == "ACTIVE_CONVERSATION_CAP" for f in res.failed_filters)
