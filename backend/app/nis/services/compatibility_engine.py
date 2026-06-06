from app.nis.schemas.compatibility import CompatibilityResult, DimensionScore
from app.nis.schemas.user_signal_profile import UserSignalProfile
from typing import List, Tuple

class NISCompatibilityEngine:
    @classmethod
    def evaluate(cls, p1: UserSignalProfile, p2: UserSignalProfile) -> CompatibilityResult:
        dimensions: List[DimensionScore] = []
        tension_points: List[str] = []
        dangerous_mismatches: List[str] = []
        shared_strengths: List[str] = []
        review_required = False

        # Check Insufficient Data
        if "UNKNOWN" in [p1.emotional_steadiness, p2.emotional_steadiness, p1.deen_alignment, p2.deen_alignment]:
            return CompatibilityResult(
                compatibility_status="INSUFFICIENT_DATA",
                confidence_level="UNKNOWN",
                dimension_results=[],
                shared_strengths=[],
                possible_tension_points=["Insufficient data to calculate compatibility."],
                dangerous_mismatches=[],
                reasoning_summary="Not enough data to form a reliable compatibility assessment.",
                review_required=True
            )

        # Helper to safely check pairs
        def has_pair(val1, val2, target1, target2):
            return (val1 == target1 and val2 == target2) or (val1 == target2 and val2 == target1)

        def add_danger(msg: str):
            dangerous_mismatches.append(msg)
            nonlocal review_required
            review_required = True

        def add_tension(msg: str):
            tension_points.append(msg)

        def add_strength(msg: str):
            shared_strengths.append(msg)

        # ---------------------------------------------------------
        # DANGEROUS COMBINATIONS (Hard Blocks / Review Required)
        # ---------------------------------------------------------
        
        # High anger + high anger
        if p1.anger_intensity == "HIGH" and p2.anger_intensity == "HIGH":
            add_danger("Mutual high anger intensity may create unsafe conflict pressure.")

        # High conflict intensity + low repair ability
        if has_pair(p1.anger_intensity, p2.anger_intensity, "HIGH", "MODERATE") or p1.anger_intensity == "HIGH" or p2.anger_intensity == "HIGH":
            if p1.conflict_repair_style in ["AVOIDANT", "DEFENSIVE"] or p2.conflict_repair_style in ["AVOIDANT", "DEFENSIVE"]:
                if (p1.anger_intensity == "HIGH" and p2.conflict_repair_style in ["AVOIDANT", "DEFENSIVE"]) or \
                   (p2.anger_intensity == "HIGH" and p1.conflict_repair_style in ["AVOIDANT", "DEFENSIVE"]):
                    add_danger("High intensity combined with weak repair pattern.")

        # Low emotional regulation + low emotional regulation
        if p1.emotional_steadiness == "VOLATILE" and p2.emotional_steadiness == "VOLATILE":
            add_danger("Mutual volatility may escalate safely.")

        # Avoidant + avoidant
        if p1.attachment_needs == "AVOIDANT" and p2.attachment_needs == "AVOIDANT":
            add_danger("May lead to profound emotional disconnect.")

        # Emotionally needy + emotionally unavailable
        if has_pair(p1.attachment_needs, p2.attachment_needs, "ANXIOUS", "AVOIDANT"):
            add_danger("Anxious-avoidant loop risk.")

        # Highly dominant + highly dominant
        if p1.ego_humility == "DOMINANT" and p2.ego_humility == "DOMINANT":
            add_danger("Clashing egos may create power struggles.")

        # Controlling + conflict avoidance
        if has_pair(p1.ego_humility, p2.ego_humility, "CONTROLLING", "BALANCED"):
            if p1.ego_humility == "CONTROLLING" and p2.conflict_repair_style == "AVOIDANT":
                add_danger("Risk of unhealthy power dynamic.")
            if p2.ego_humility == "CONTROLLING" and p1.conflict_repair_style == "AVOIDANT":
                add_danger("Risk of unhealthy power dynamic.")

        # Financially irresponsible + financially irresponsible
        if p1.financial_responsibility == "IRRESPONSIBLE" and p2.financial_responsibility == "IRRESPONSIBLE":
            add_danger("Mutual financial carelessness poses severe stability risk.")

        # Not-ready + not-ready
        if p1.marriage_readiness == "NOT_READY" and p2.marriage_readiness == "NOT_READY":
            add_danger("Neither party is ready for marital responsibilities.")

        # Weak boundaries + high family pressure
        if has_pair(p1.boundary_respect, p2.boundary_respect, "WEAK", "RESPECTFUL"):
            pass
        if (p1.boundary_respect == "WEAK" and p2.family_responsibility == "HIGH_PRESSURE") or \
           (p2.boundary_respect == "WEAK" and p1.family_responsibility == "HIGH_PRESSURE"):
            add_danger("Weak boundaries unable to handle high family pressure safely.")

        # Impulsive + impulsive
        if p1.stability_risk == "IMPULSIVE" and p2.stability_risk == "IMPULSIVE":
            add_danger("Mutual impulsivity creates long-term instability.")

        # Low accountability + low accountability
        if p1.conflict_repair_style == "DEFENSIVE" and p2.conflict_repair_style == "DEFENSIVE":
            add_danger("Mutual lack of accountability blocks repair.")

        # ---------------------------------------------------------
        # HEALTHY COMPLEMENTARITY (Strengths)
        # ---------------------------------------------------------

        # Calm/stable + expressive but repair-oriented
        if has_pair(p1.emotional_steadiness, p2.emotional_steadiness, "STEADY", "EXPRESSIVE"):
            if p1.conflict_repair_style == "PROACTIVE" and p2.conflict_repair_style == "PROACTIVE":
                add_strength("Healthy balance of steady calm and expressive communication, grounded in repair.")

        # Structured + flexible
        if has_pair(p1.social_lifestyle, p2.social_lifestyle, "STRUCTURED", "FLEXIBLE"):
            add_strength("Complementary lifestyle rhythm (structured meets flexible).")

        # Emotionally steady + emotionally open
        if has_pair(p1.emotional_steadiness, p2.attachment_needs, "STEADY", "OPEN") or \
           has_pair(p2.emotional_steadiness, p1.attachment_needs, "STEADY", "OPEN"):
            add_strength("Strong emotional foundation combining steadiness with openness.")

        # Financially careful + financially balanced
        if has_pair(p1.financial_responsibility, p2.financial_responsibility, "CAREFUL", "BALANCED"):
            add_strength("Complementary and healthy financial responsibility.")

        # Family-responsible + family-responsible
        if p1.family_responsibility == "HIGH" and p2.family_responsibility == "HIGH":
            add_strength("Deeply shared value for family responsibility and care.")

        # Assertive but respectful + gentle but communicative
        if has_pair(p1.ego_humility, p2.communication_style, "ASSERTIVE", "GENTLE") or \
           has_pair(p2.ego_humility, p1.communication_style, "ASSERTIVE", "GENTLE"):
            if p1.boundary_respect == "RESPECTFUL" and p2.boundary_respect == "RESPECTFUL":
                add_strength("Complementary communication styles (assertive meets gentle).")

        # ---------------------------------------------------------
        # STANDARD TENSIONS & LEGACY DANGEROUS PAIRS
        # ---------------------------------------------------------
        
        legacy_dangerous = [
            (p1.deen_alignment, p2.deen_alignment, "STRONG", "WEAK", "deen_alignment"),
            (p1.family_responsibility, p2.family_responsibility, "HIGH", "LOW", "family_responsibility"),
            (p1.marriage_readiness, p2.marriage_readiness, "READY", "NOT_READY", "marriage_readiness"),
            (p1.financial_expectation, p2.financial_expectation, "HIGH", "LOW", "financial_expectation"),
            (p1.wali_comfort, p2.wali_comfort, "COMFORTABLE", "UNCOMFORTABLE", "wali_comfort"),
            (p1.social_lifestyle, p2.social_lifestyle, "VERY_SOCIAL", "HOMEBODY", "social_lifestyle"),
            (p1.conflict_repair_style, p2.conflict_repair_style, "AVOIDANT", "AVOIDANT", "conflict_repair_style"),
            (p1.conflict_repair_style, p2.conflict_repair_style, "VOLATILE", "VOLATILE", "conflict_repair_style")
        ]

        for val1, val2, t1, t2, name in legacy_dangerous:
            if has_pair(val1, val2, t1, t2):
                add_danger(f"Dangerous mismatch in {name.replace('_', ' ')}.")

        # Generic tensions for any difference across the 13 dimensions
        all_dims = [
            ("emotional_steadiness", p1.emotional_steadiness, p2.emotional_steadiness),
            ("anger_intensity", p1.anger_intensity, p2.anger_intensity),
            ("conflict_repair_style", p1.conflict_repair_style, p2.conflict_repair_style),
            ("communication_style", p1.communication_style, p2.communication_style),
            ("attachment_needs", p1.attachment_needs, p2.attachment_needs),
            ("ego_humility", p1.ego_humility, p2.ego_humility),
            ("family_responsibility", p1.family_responsibility, p2.family_responsibility),
            ("financial_responsibility", p1.financial_responsibility, p2.financial_responsibility),
            ("financial_expectation", p1.financial_expectation, p2.financial_expectation),
            ("marriage_readiness", p1.marriage_readiness, p2.marriage_readiness),
            ("social_lifestyle", p1.social_lifestyle, p2.social_lifestyle),
            ("deen_alignment", p1.deen_alignment, p2.deen_alignment),
            ("boundary_respect", p1.boundary_respect, p2.boundary_respect),
            ("stability_risk", p1.stability_risk, p2.stability_risk),
            ("wali_comfort", p1.wali_comfort, p2.wali_comfort),
            ("life_direction", p1.life_direction, p2.life_direction)
        ]

        for name, val1, val2 in all_dims:
            # Check if this exact difference wasn't already flagged as a dangerous mismatch
            is_already_dangerous = False
            for d in dangerous_mismatches:
                if name.replace('_', ' ') in d:
                    is_already_dangerous = True
                    break
            
            if val1 != val2 and not is_already_dangerous:
                add_tension(f"Manageable difference in {name.replace('_', ' ')}.")

        # ---------------------------------------------------------
        # SCORING & FINAL STATUS
        # ---------------------------------------------------------

        num_tensions = len(tension_points)
        num_dangerous = len(dangerous_mismatches)
        
        if num_dangerous > 0:
            comp_status = "INCOMPATIBLE"
            reasoning = "Fundamental incompatibilities or unsafe dynamics detected."
            review_required = True
        elif num_tensions >= 4:
            comp_status = "WEAK_COMPATIBILITY"
            reasoning = "Multiple tension points identified. Proceed with caution."
            review_required = True
        elif num_tensions >= 2:
            comp_status = "MODERATE_COMPATIBILITY"
            reasoning = "Generally aligned but with some manageable differences to navigate."
        else:
            comp_status = "STRONG_COMPATIBILITY"
            reasoning = "High psychological and values alignment."

        confidence = "HIGH" if comp_status in ["STRONG_COMPATIBILITY", "MODERATE_COMPATIBILITY"] else "LOW"

        return CompatibilityResult(
            compatibility_status=comp_status,
            confidence_level=confidence,
            dimension_results=[],  # Simplified in Phase I to focus on aggregated dynamics
            shared_strengths=shared_strengths,
            possible_tension_points=tension_points,
            dangerous_mismatches=dangerous_mismatches,
            reasoning_summary=reasoning,
            review_required=review_required
        )
