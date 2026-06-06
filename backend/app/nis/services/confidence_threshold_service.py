from typing import List, Union
from app.nis.schemas.confidence_thresholds import CandidateConfidenceResult, NoMatchResult
from app.nis.schemas.hard_filters import HardFilterResult
from app.nis.schemas.compatibility import CompatibilityResult
from dataclasses import dataclass

@dataclass
class CandidateInputs:
    candidate_user_id: str
    hard_filter_result: HardFilterResult
    compatibility_result: CompatibilityResult
    safety_risk_level: str
    profile_data_complete: bool
    preference_data_complete: bool

class NISConfidenceThresholdService:
    @staticmethod
    def evaluate_candidate(inputs: CandidateInputs) -> CandidateConfidenceResult:
        reasons = []
        blocked_reasons = []

        # 1. Check Data Completeness
        if not inputs.profile_data_complete or not inputs.preference_data_complete:
            blocked_reasons.append("Important signal data is missing")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="INSUFFICIENT_DATA",
                confidence_level="UNKNOWN",
                can_show_candidate=False,
                requires_human_review=True,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )
        
        # 2. Check Safety
        if inputs.safety_risk_level == "HIGH":
            blocked_reasons.append("Safety risk is high")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="SAFETY_REJECT",
                confidence_level="UNKNOWN",
                can_show_candidate=False,
                requires_human_review=True,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )
        reasons.append("Safety risk is low")

        # 3. Check Hard Filters
        if not inputs.hard_filter_result.passed:
            blocked_reasons.append("Hard filters failed")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="HARD_REJECT",
                confidence_level="UNKNOWN",
                can_show_candidate=False,
                requires_human_review=False,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )
        reasons.append("Hard filters passed")

        # 4. Check Compatibility
        comp = inputs.compatibility_result
        if comp.compatibility_status == "INSUFFICIENT_DATA":
             blocked_reasons.append("Compatibility data is insufficient")
             return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="INSUFFICIENT_DATA",
                confidence_level="UNKNOWN",
                can_show_candidate=False,
                requires_human_review=True,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )

        if comp.compatibility_status == "INCOMPATIBLE" or comp.review_required or len(comp.dangerous_mismatches) > 0:
            blocked_reasons.append("Dangerous pair dynamics or review required")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="HARD_REJECT" if comp.compatibility_status == "INCOMPATIBLE" else "MODERATE_CONFIDENCE_REVIEW",
                confidence_level="UNKNOWN",
                can_show_candidate=False,
                requires_human_review=True,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )

        if comp.compatibility_status == "WEAK_COMPATIBILITY":
            blocked_reasons.append("Compatibility is weak")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="LOW_CONFIDENCE_DO_NOT_SHOW",
                confidence_level="LOW",
                can_show_candidate=False,
                requires_human_review=False,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )

        if comp.compatibility_status == "MODERATE_COMPATIBILITY":
            reasons.append("Compatibility is moderate but needs checks")
            return CandidateConfidenceResult(
                candidate_user_id=inputs.candidate_user_id,
                final_status="MODERATE_CONFIDENCE_REVIEW",
                confidence_level="MODERATE",
                can_show_candidate=False,
                requires_human_review=True,
                reasons=reasons,
                blocked_reasons=blocked_reasons
            )

        # 5. Passed everything -> STRONG_COMPATIBILITY
        reasons.append("Compatibility is strong")
        reasons.append("Sufficient profile data exists")
        return CandidateConfidenceResult(
            candidate_user_id=inputs.candidate_user_id,
            final_status="HIGH_CONFIDENCE_MATCH",
            confidence_level="HIGH",
            can_show_candidate=True,
            requires_human_review=False,
            reasons=reasons,
            blocked_reasons=blocked_reasons
        )

    @staticmethod
    def evaluate_pool(candidates: List[CandidateInputs]) -> Union[CandidateConfidenceResult, NoMatchResult]:
        evaluated = []
        for candidate in candidates:
            res = NISConfidenceThresholdService.evaluate_candidate(candidate)
            if res.can_show_candidate:
                return res
            evaluated.append(res)
            
        return NoMatchResult(candidates=evaluated)
