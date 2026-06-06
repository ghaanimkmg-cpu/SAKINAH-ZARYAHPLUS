from app.nis.schemas.hard_filters import HardFilterResult, FailedFilter
from dataclasses import dataclass

@dataclass
class FilterCandidateState:
    is_verified: bool
    is_banned: bool
    is_under_review: bool
    has_profile: bool
    has_preferences: bool
    age: int
    active_conversations: int
    location: str
    timeline: str
    tradition: str
    wali: str
    marital_status: str
    relocation_openness: str = "NO"

@dataclass
class FilterPreferences:
    age_min: int
    age_max: int
    location_pref: str
    timeline_pref: str
    tradition_pref: str
    wali_pref: str
    marital_status_pref: str

class NISHardFilterEngine:
    # Default safe value
    ACTIVE_CONVERSATION_CAP = 1

    @classmethod
    def evaluate(
        cls, 
        user_state: FilterCandidateState, 
        user_prefs: FilterPreferences,
        candidate_state: FilterCandidateState,
        candidate_prefs: FilterPreferences,
        are_already_active: bool = False,
        is_blocked_or_reported: bool = False
    ) -> HardFilterResult:
        failed_filters = []

        if not user_state.is_verified or not candidate_state.is_verified:
            failed_filters.append(FailedFilter(filter="VERIFICATION", reason="One or both users are unverified"))

        if user_state.is_banned or candidate_state.is_banned:
            failed_filters.append(FailedFilter(filter="BANNED", reason="One or both users are banned"))

        if user_state.is_under_review or candidate_state.is_under_review:
            failed_filters.append(FailedFilter(filter="UNDER_REVIEW", reason="One or both users are under human review"))

        if not user_state.has_profile or not candidate_state.has_profile:
            failed_filters.append(FailedFilter(filter="INCOMPLETE_PROFILE", reason="Missing signal profile"))
            
        if not user_state.has_preferences or not candidate_state.has_preferences:
            failed_filters.append(FailedFilter(filter="INCOMPLETE_PREFERENCES", reason="Missing match preferences"))

        if candidate_state.age < user_prefs.age_min or candidate_state.age > user_prefs.age_max:
            failed_filters.append(FailedFilter(filter="AGE", reason="Candidate age out of user bounds"))
        if user_state.age < candidate_prefs.age_min or user_state.age > candidate_prefs.age_max:
            failed_filters.append(FailedFilter(filter="AGE", reason="User age out of candidate bounds"))

        if user_prefs.location_pref != "ANY" and user_prefs.location_pref != candidate_state.location:
            if candidate_state.relocation_openness != "OPEN":
                failed_filters.append(FailedFilter(filter="LOCATION", reason="Location mismatch and relocation not open"))
        if candidate_prefs.location_pref != "ANY" and candidate_prefs.location_pref != user_state.location:
            if user_state.relocation_openness != "OPEN":
                failed_filters.append(FailedFilter(filter="LOCATION", reason="Location mismatch and relocation not open"))

        if user_prefs.timeline_pref != "ANY" and user_prefs.timeline_pref != candidate_state.timeline:
            failed_filters.append(FailedFilter(filter="NIKAH_TIMELINE", reason="Timeline mismatch"))
        if candidate_prefs.timeline_pref != "ANY" and candidate_prefs.timeline_pref != user_state.timeline:
             failed_filters.append(FailedFilter(filter="NIKAH_TIMELINE", reason="Timeline mismatch"))

        if user_prefs.tradition_pref != "ANY" and user_prefs.tradition_pref != candidate_state.tradition:
            failed_filters.append(FailedFilter(filter="TRADITION", reason="Tradition mismatch"))
        if candidate_prefs.tradition_pref != "ANY" and candidate_prefs.tradition_pref != user_state.tradition:
            failed_filters.append(FailedFilter(filter="TRADITION", reason="Tradition mismatch"))

        if user_prefs.wali_pref != "ANY" and user_prefs.wali_pref != candidate_state.wali:
            failed_filters.append(FailedFilter(filter="WALI_INVOLVEMENT", reason="Wali preference mismatch"))
        if candidate_prefs.wali_pref != "ANY" and candidate_prefs.wali_pref != user_state.wali:
            failed_filters.append(FailedFilter(filter="WALI_INVOLVEMENT", reason="Wali preference mismatch"))

        if user_prefs.marital_status_pref != "ANY" and user_prefs.marital_status_pref != candidate_state.marital_status:
             failed_filters.append(FailedFilter(filter="MARITAL_STATUS", reason="Marital status mismatch"))
        if candidate_prefs.marital_status_pref != "ANY" and candidate_prefs.marital_status_pref != user_state.marital_status:
             failed_filters.append(FailedFilter(filter="MARITAL_STATUS", reason="Marital status mismatch"))

        if is_blocked_or_reported:
             failed_filters.append(FailedFilter(filter="BLOCKED_REPORTED", reason="Blocked or reported relationship exists"))

        if user_state.active_conversations >= cls.ACTIVE_CONVERSATION_CAP:
             failed_filters.append(FailedFilter(filter="ACTIVE_CONVERSATION_CAP", reason="User reached conversation cap"))
        if candidate_state.active_conversations >= cls.ACTIVE_CONVERSATION_CAP:
             failed_filters.append(FailedFilter(filter="ACTIVE_CONVERSATION_CAP", reason="Candidate reached conversation cap"))

        if are_already_active:
             failed_filters.append(FailedFilter(filter="ALREADY_ACTIVE", reason="Candidate is already active with user"))

        if failed_filters:
            return HardFilterResult(
                passed=False,
                status="HARD_REJECT",
                failed_filters=failed_filters
            )
        
        return HardFilterResult(
            passed=True,
            status="PASSED",
            failed_filters=[]
        )
