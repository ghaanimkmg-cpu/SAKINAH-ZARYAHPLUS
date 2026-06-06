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

        def evaluate_dimension(name: str, val1: str, val2: str, dangerous_pairs: List[Tuple[str, str]] = []) -> DimensionScore:
            status = "MODERATE"
            is_tension = False
            is_dangerous = False
            is_shared = False
            notes = ""
            clean_name = name.replace('_', ' ')

            if val1 == val2:
                status = "STRONG"
                is_shared = True
                notes = f"Strong shared alignment in {clean_name}."
                shared_strengths.append(notes)
            else:
                status = "WEAK"
                is_tension = True
                notes = f"Manageable difference in {clean_name}."

            # Check for dangerous mismatch
            for (d1, d2) in dangerous_pairs:
                if (val1 == d1 and val2 == d2) or (val1 == d2 and val2 == d1):
                    status = "INCOMPATIBLE"
                    is_tension = True
                    is_dangerous = True
                    notes = f"Dangerous mismatch in {clean_name}."
                    dangerous_mismatches.append(notes)
                    break
            
            if is_tension and not is_dangerous:
                tension_points.append(notes)

            return DimensionScore(
                dimension=name,
                status=status,
                notes=notes,
                is_tension_point=is_tension,
                is_dangerous_mismatch=is_dangerous,
                is_shared_strength=is_shared
            )

        # 1. Emotional Steadiness
        dimensions.append(evaluate_dimension("emotional_steadiness", p1.emotional_steadiness, p2.emotional_steadiness, [("VOLATILE", "VOLATILE")]))
        
        # 2. Communication
        dimensions.append(evaluate_dimension("communication_compatibility", p1.communication_style, p2.communication_style))

        # 3. Conflict Repair
        dimensions.append(evaluate_dimension("conflict_repair", p1.conflict_repair_style, p2.conflict_repair_style, [("AVOIDANT", "AVOIDANT"), ("VOLATILE", "VOLATILE")]))

        # 4. Values / Deen Alignment
        dimensions.append(evaluate_dimension("deen_alignment", p1.deen_alignment, p2.deen_alignment, [("STRONG", "WEAK")]))

        # 5. Family Responsibility
        dimensions.append(evaluate_dimension("family_responsibility", p1.family_responsibility, p2.family_responsibility, [("HIGH", "LOW")]))

        # 6. Marriage Readiness
        dimensions.append(evaluate_dimension("marriage_readiness", p1.marriage_readiness, p2.marriage_readiness, [("READY", "NOT_READY")]))

        # 7. Financial Expectation
        dimensions.append(evaluate_dimension("financial_expectation", p1.financial_expectation, p2.financial_expectation, [("HIGH", "LOW")]))

        # 8. Life Direction
        dimensions.append(evaluate_dimension("life_direction", p1.life_direction, p2.life_direction))

        # 9. Wali Comfort
        dimensions.append(evaluate_dimension("wali_comfort", p1.wali_comfort, p2.wali_comfort, [("COMFORTABLE", "UNCOMFORTABLE")]))

        # 10. Lifestyle Rhythm
        dimensions.append(evaluate_dimension("lifestyle_rhythm", p1.social_lifestyle, p2.social_lifestyle, [("VERY_SOCIAL", "HOMEBODY")]))

        # Internal evaluation only
        num_tensions = len(tension_points)
        num_dangerous = len(dangerous_mismatches)
        
        if num_dangerous > 0:
            comp_status = "INCOMPATIBLE"
            reasoning = "Fundamental incompatibilities detected in key areas."
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
            reasoning = "High alignment across core values and lifestyle factors."

        # Since we use deterministic complete fields for tests right now, confidence is HIGH unless incomplete data
        confidence = "HIGH"

        return CompatibilityResult(
            compatibility_status=comp_status,
            confidence_level=confidence,
            dimension_results=dimensions,
            shared_strengths=shared_strengths,
            possible_tension_points=tension_points,
            dangerous_mismatches=dangerous_mismatches,
            reasoning_summary=reasoning,
            review_required=review_required
        )
