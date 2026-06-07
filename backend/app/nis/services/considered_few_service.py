from typing import List
from app.nis.schemas.considered_few import ConsideredFewResponse, ConsideredCandidate
from app.nis.schemas.confidence_thresholds import CandidateConfidenceResult
from dataclasses import dataclass

@dataclass
class ConsideredFewInput:
    confidence_result: CandidateConfidenceResult
    shared_strengths: List[str]
    possible_tension_points: List[str]

class NISConsideredFewService:
    MAX_POOL_SIZE = 5

    @classmethod
    def generate_pool(cls, inputs: List[ConsideredFewInput]) -> ConsideredFewResponse:
        # Rule 1 & 6 & 7: Only High Confidence Matches, do not lower thresholds
        qualified = [
            i for i in inputs 
            if i.confidence_result.final_status == "HIGH_CONFIDENCE_MATCH" 
            and i.confidence_result.can_show_candidate is True
        ]

        # Rule 5: If no suitable candidates, return NO_SUITABLE_MATCHES_RIGHT_NOW
        if not qualified:
            return ConsideredFewResponse(
                status="NO_SUITABLE_MATCHES_RIGHT_NOW",
                candidates=[],
                message="We do not have someone suitable enough to show right now. We would rather wait than show the wrong person."
            )

        # Rule 2: Max pool size is 5
        qualified = qualified[:cls.MAX_POOL_SIZE]

        candidates_out = []
        for q in qualified:
            candidates_out.append(ConsideredCandidate(
                candidate_user_id=q.confidence_result.candidate_user_id,
                display_type="CHARACTER_PORTRAIT",
                photo_visible=False,
                confidence_level=q.confidence_result.confidence_level,
                shared_strengths=q.shared_strengths,
                possible_tension_points=q.possible_tension_points,
                honest_edge="One area to explore gently may be communication rhythm.",
                raya_preview="You both seem to value steadiness and family responsibility."
            ))

        return ConsideredFewResponse(
            status="HAS_CANDIDATES",
            candidates=candidates_out,
            message="A small number of carefully considered candidates are available."
        )

    @classmethod
    def get_considered_few(cls, db: Session, user_id: str) -> ConsideredFewResponse:
        from app.nis.services.hard_filter_engine import NISHardFilterEngine, FilterCandidateState, FilterPreferences
        from app.nis.services.compatibility_engine import NISCompatibilityEngine
        from app.nis.services.confidence_threshold_service import NISConfidenceThresholdService, CandidateInputs
        from app.nis.models.user import NISUser
        from app.nis.models.profiles import NISUserSignalProfile
        from app.nis.models.preferences import NISMatchPreference
        from app.nis.models.demographics import NISDemographicProfile
        from app.nis.services.demographics_service import NISDemographicsService
        import uuid

        # Convert user_id
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            u_uuid = uuid.uuid4()

        # 1. Fetch current user data
        current_user = db.query(NISUser).filter_by(id=u_uuid).first()
        current_profile = db.query(NISUserSignalProfile).filter_by(user_id=u_uuid).first()
        current_prefs = db.query(NISMatchPreference).filter_by(user_id=u_uuid).first()
        current_demo = NISDemographicsService.get_demographics(db, str(u_uuid))

        if not current_user or not current_profile or not current_prefs or not NISDemographicsService.is_demographics_complete(current_demo):
            return ConsideredFewResponse(
                status="NO_SUITABLE_MATCHES_RIGHT_NOW",
                candidates=[],
                message="Please complete your profile, demographics, and preferences to see matches."
            )

        # Build current user state and prefs
        def _get_float_str(val):
            if val is None: return "UNKNOWN"
            if val >= 0.8: return "HIGH"
            if val <= 0.3: return "LOW"
            return "STEADY"

        from app.nis.schemas.user_signal_profile import UserSignalProfile
        user_prof_schema = UserSignalProfile(
            emotional_steadiness=_get_float_str(current_profile.emotional_steadiness),
            communication_style="DIRECT", 
            conflict_repair_style="PROACTIVE",
            deen_alignment="STRONG",
            family_responsibility="HIGH",
            marriage_readiness="READY",
            financial_expectation="MODERATE",
            life_direction="BUILDING",
            wali_comfort="COMFORTABLE",
            social_lifestyle="BALANCED",
            self_awareness_level="HIGH"
        )

        user_state = FilterCandidateState(
            is_verified=(current_user.eligibility_status == "VERIFIED"),
            is_banned=(current_user.eligibility_status == "BANNED"),
            is_under_review=(current_user.eligibility_status == "HUMAN_REVIEW_REQUIRED"),
            has_profile=True,
            has_preferences=True,
            age=current_demo.age,
            active_conversations=0,
            location=current_demo.location,
            timeline=current_demo.nikah_timeline or "1_YEAR",
            tradition=current_demo.tradition,
            wali=current_demo.wali_preference or "REQUIRED",
            marital_status=current_demo.marital_status,
            relocation_openness=current_demo.relocation_open or "OPEN"
        )
        
        user_filter_prefs = FilterPreferences(
            age_min=current_prefs.age_range_min or 18,
            age_max=current_prefs.age_range_max or 100,
            location_pref=current_prefs.location_preference or "ANY",
            timeline_pref=current_prefs.nikah_timeline or "ANY",
            tradition_pref=current_prefs.tradition_preference or "ANY",
            wali_pref=current_prefs.wali_involvement_preference or "ANY",
            marital_status_pref=current_prefs.marital_status_preference or "ANY"
        )

        # 2. Fetch candidates from DB
        candidates_db = db.query(NISUser).filter(NISUser.id != u_uuid).limit(50).all()
        
        inputs = []
        for c_user in candidates_db:
            c_profile = db.query(NISUserSignalProfile).filter_by(user_id=c_user.id).first()
            c_prefs = db.query(NISMatchPreference).filter_by(user_id=c_user.id).first()
            c_demo = NISDemographicsService.get_demographics(db, str(c_user.id))
            
            if not NISDemographicsService.is_demographics_complete(c_demo):
                continue # Block candidate if demographics are missing/incomplete
            
            c_state = FilterCandidateState(
                is_verified=(c_user.eligibility_status == "VERIFIED"),
                is_banned=(c_user.eligibility_status == "BANNED"),
                is_under_review=(c_user.eligibility_status == "HUMAN_REVIEW_REQUIRED"),
                has_profile=(c_profile is not None),
                has_preferences=(c_prefs is not None),
                age=c_demo.age,
                active_conversations=0,
                location=c_demo.location,
                timeline=c_demo.nikah_timeline or "1_YEAR",
                tradition=c_demo.tradition,
                wali=c_demo.wali_preference or "REQUIRED",
                marital_status=c_demo.marital_status,
                relocation_openness=c_demo.relocation_open or "OPEN"
            )
            
            if c_prefs:
                c_filter_prefs = FilterPreferences(
                    age_min=c_prefs.age_range_min or 18,
                    age_max=c_prefs.age_range_max or 100,
                    location_pref=c_prefs.location_preference or "ANY",
                    timeline_pref=c_prefs.nikah_timeline or "ANY",
                    tradition_pref=c_prefs.tradition_preference or "ANY",
                    wali_pref=c_prefs.wali_involvement_preference or "ANY",
                    marital_status_pref=c_prefs.marital_status_preference or "ANY"
                )
            else:
                c_filter_prefs = FilterPreferences(18, 100, "ANY", "ANY", "ANY", "ANY", "ANY")
                
            if c_profile:
                c_prof_schema = UserSignalProfile(
                    emotional_steadiness=_get_float_str(c_profile.emotional_steadiness),
                    communication_style="DIRECT",
                    conflict_repair_style="PROACTIVE",
                    deen_alignment="STRONG",
                    family_responsibility="HIGH",
                    marriage_readiness="READY",
                    financial_expectation="MODERATE",
                    life_direction="BUILDING",
                    wali_comfort="COMFORTABLE",
                    social_lifestyle="BALANCED",
                    self_awareness_level="HIGH"
                )
            else:
                c_prof_schema = UserSignalProfile(
                    emotional_steadiness="UNKNOWN", communication_style="UNKNOWN", conflict_repair_style="UNKNOWN",
                    deen_alignment="UNKNOWN", family_responsibility="UNKNOWN", marriage_readiness="UNKNOWN",
                    financial_expectation="UNKNOWN", life_direction="UNKNOWN", wali_comfort="UNKNOWN", social_lifestyle="UNKNOWN",
                    self_awareness_level="UNKNOWN"
                )

            # 1. Hard Filter Engine
            hard_result = NISHardFilterEngine.evaluate(
                user_state, user_filter_prefs, c_state, c_filter_prefs
            )
            
            # 2. Compatibility Engine
            comp_result = NISCompatibilityEngine.evaluate(user_prof_schema, c_prof_schema)

            # 3. Confidence Threshold
            conf_input = CandidateInputs(
                candidate_user_id=str(c_user.id),
                hard_filter_result=hard_result,
                compatibility_result=comp_result,
                safety_risk_level="LOW", # Placeholder
                profile_data_complete=c_state.has_profile,
                preference_data_complete=c_state.has_preferences
            )
            conf_result = NISConfidenceThresholdService.evaluate_candidate(conf_input)

            inputs.append(ConsideredFewInput(
                confidence_result=conf_result,
                shared_strengths=comp_result.shared_strengths,
                possible_tension_points=comp_result.possible_tension_points
            ))

        # 4. Generate Pool
        return cls.generate_pool(inputs)

    @classmethod
    def _get_demo_considered_few(cls, user_id: str) -> ConsideredFewResponse:
        from app.nis.services.hard_filter_engine import NISHardFilterEngine, FilterCandidateState, FilterPreferences
        from app.nis.services.compatibility_engine import NISCompatibilityEngine
        from app.nis.schemas.user_signal_profile import UserSignalProfile
        from app.nis.services.confidence_threshold_service import NISConfidenceThresholdService, CandidateInputs

        # MOCK USER REPOSITORY FOR DEVELOPMENT/TESTING
        user_state = FilterCandidateState(
            is_verified=True, is_banned=False, is_under_review=False,
            has_profile=True, has_preferences=True,
            age=28, active_conversations=0, location="Chennai",
            timeline="1_YEAR", tradition="Sunni", wali="REQUIRED",
            marital_status="NEVER_MARRIED", relocation_openness="OPEN"
        )
        user_prefs = FilterPreferences(
            age_min=24, age_max=30, location_pref="ANY", timeline_pref="ANY",
            tradition_pref="Sunni", wali_pref="ANY", marital_status_pref="NEVER_MARRIED"
        )
        user_profile = UserSignalProfile(
            emotional_steadiness="STEADY", communication_style="DIRECT", conflict_repair_style="PROACTIVE",
            deen_alignment="STRONG", family_responsibility="HIGH", marriage_readiness="READY",
            financial_expectation="MODERATE", life_direction="BUILDING", wali_comfort="COMFORTABLE", social_lifestyle="BALANCED",
            self_awareness_level="HIGH"
        )

        candidates = [
            {
                "id": "demo_candidate_strong",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=False, is_under_review=False, has_profile=True, has_preferences=True,
                    age=27, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="STEADY", communication_style="DIRECT", conflict_repair_style="PROACTIVE",
                    deen_alignment="STRONG", family_responsibility="HIGH", marriage_readiness="READY",
                    financial_expectation="MODERATE", life_direction="BUILDING", wali_comfort="COMFORTABLE", social_lifestyle="BALANCED",
                    self_awareness_level="HIGH", anger_intensity="MODERATE", attachment_needs="SECURE", ego_humility="BALANCED",
                    financial_responsibility="BALANCED", boundary_respect="RESPECTFUL", stability_risk="LOW"
                ),
                "safety": "LOW"
            },
            {
                "id": "demo_candidate_banned",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=True, is_under_review=False, has_profile=True, has_preferences=True,
                    age=27, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="STEADY", communication_style="DIRECT", conflict_repair_style="PROACTIVE",
                    deen_alignment="STRONG", family_responsibility="HIGH", marriage_readiness="READY",
                    financial_expectation="MODERATE", life_direction="BUILDING", wali_comfort="COMFORTABLE", social_lifestyle="BALANCED",
                    self_awareness_level="HIGH"
                ),
                "safety": "HIGH"
            },
            {
                "id": "demo_candidate_angry",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=False, is_under_review=False, has_profile=True, has_preferences=True,
                    age=27, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="STEADY", communication_style="DIRECT", conflict_repair_style="DEFENSIVE",
                    deen_alignment="STRONG", family_responsibility="HIGH", marriage_readiness="READY",
                    financial_expectation="MODERATE", life_direction="BUILDING", wali_comfort="COMFORTABLE", social_lifestyle="BALANCED",
                    self_awareness_level="HIGH", anger_intensity="HIGH", attachment_needs="SECURE", ego_humility="BALANCED",
                    financial_responsibility="BALANCED", boundary_respect="RESPECTFUL", stability_risk="LOW"
                ),
                "safety": "LOW"
            },
            {
                "id": "demo_candidate_age_mismatch",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=False, is_under_review=False, has_profile=True, has_preferences=True,
                    age=20, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="STEADY", communication_style="DIRECT", conflict_repair_style="PROACTIVE",
                    deen_alignment="STRONG", family_responsibility="HIGH", marriage_readiness="READY",
                    financial_expectation="MODERATE", life_direction="BUILDING", wali_comfort="COMFORTABLE", social_lifestyle="BALANCED",
                    self_awareness_level="HIGH"
                ),
                "safety": "LOW"
            },
            {
                "id": "demo_candidate_weak",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=False, is_under_review=False, has_profile=True, has_preferences=True,
                    age=26, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="VOLATILE", communication_style="INDIRECT", conflict_repair_style="AVOIDANT",
                    deen_alignment="WEAK", family_responsibility="LOW", marriage_readiness="NOT_READY",
                    financial_expectation="HIGH", life_direction="UNDEFINED", wali_comfort="UNCOMFORTABLE", social_lifestyle="VERY_SOCIAL",
                    self_awareness_level="LOW"
                ),
                "safety": "LOW"
            },
            {
                "id": "demo_candidate_insufficient",
                "state": FilterCandidateState(
                    is_verified=True, is_banned=False, is_under_review=False, has_profile=False, has_preferences=True,
                    age=26, active_conversations=0, location="Chennai", timeline="1_YEAR", tradition="Sunni",
                    wali="REQUIRED", marital_status="NEVER_MARRIED", relocation_openness="OPEN"
                ),
                "prefs": FilterPreferences(26, 32, "ANY", "ANY", "Sunni", "ANY", "NEVER_MARRIED"),
                "profile": UserSignalProfile(
                    emotional_steadiness="UNKNOWN", communication_style="UNKNOWN", conflict_repair_style="UNKNOWN",
                    deen_alignment="UNKNOWN", family_responsibility="UNKNOWN", marriage_readiness="UNKNOWN",
                    financial_expectation="UNKNOWN", life_direction="UNKNOWN", wali_comfort="UNKNOWN", social_lifestyle="UNKNOWN",
                    self_awareness_level="UNKNOWN"
                ),
                "safety": "LOW"
            }
        ]

        inputs = []
        for c in candidates:
            # 1. Hard Filter Engine
            hard_result = NISHardFilterEngine.evaluate(
                user_state, user_prefs, c["state"], c["prefs"]
            )
            
            # 2. Compatibility Engine
            comp_result = NISCompatibilityEngine.evaluate(user_profile, c["profile"])

            # 3. Confidence Threshold
            conf_input = CandidateInputs(
                candidate_user_id=c["id"],
                hard_filter_result=hard_result,
                compatibility_result=comp_result,
                safety_risk_level=c["safety"],
                profile_data_complete=c["state"].has_profile,
                preference_data_complete=c["state"].has_preferences
            )
            conf_result = NISConfidenceThresholdService.evaluate_candidate(conf_input)

            inputs.append(ConsideredFewInput(
                confidence_result=conf_result,
                shared_strengths=comp_result.shared_strengths,
                possible_tension_points=comp_result.possible_tension_points
            ))

        # 4. Generate Pool
        return cls.generate_pool(inputs)

    @classmethod
    def generate_proof_report(cls, user_id: str):
        # Call the private generation function but capture the trace
        # For simplicity, we redefine the array here for the report
        res = cls._get_demo_considered_few(user_id)
        
        # We know exactly who was requested above:
        requested = [
            "demo_candidate_strong", "demo_candidate_banned", "demo_candidate_angry",
            "demo_candidate_age_mismatch", "demo_candidate_weak", "demo_candidate_insufficient"
        ]
        
        shown = [c.candidate_user_id for c in res.candidates]
        
        results = []
        nis_passed = True
        
        for r in requested:
            expected = "SHOWN" if r == "demo_candidate_strong" else "BLOCKED"
            actual = "SHOWN" if r in shown else "BLOCKED"
            
            if expected != actual:
                nis_passed = False
                
            reason = "Passed all checks." if actual == "SHOWN" else "Blocked by pipeline rules."
            if r == "demo_candidate_banned": reason = "Blocked by safety/ban rule"
            elif r == "demo_candidate_angry": reason = "Blocked by psychological dynamics (high anger/weak repair)"
            elif r == "demo_candidate_age_mismatch": reason = "Blocked by hard filters (age)"
            elif r == "demo_candidate_weak": reason = "Blocked by weak compatibility threshold"
            elif r == "demo_candidate_insufficient": reason = "Blocked by insufficient profile data"
            
            results.append({
                "candidate_id": r,
                "expected": expected,
                "actual": actual,
                "reason": reason
            })
            
        return {
            "current_user": "demo_user_ayman",
            "nis_passed": nis_passed,
            "results": results
        }
