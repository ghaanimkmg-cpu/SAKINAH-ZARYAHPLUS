from app.nis.schemas.raya_explanations import RayaScriptInputs, RayaExplanationResult

class NISRayaScriptService:
    FORBIDDEN_PHRASES = [
        "you should marry",
        "perfect match",
        "allah chose",
        "guaranteed",
        "you should proceed",
        "do not miss this",
        "soulmate",
        "definitely right"
    ]

    @classmethod
    def generate_explanation(cls, inputs: RayaScriptInputs) -> RayaExplanationResult:
        if inputs.no_match_status or inputs.final_status == "NO_SUITABLE_MATCHES_RIGHT_NOW":
            return RayaExplanationResult(
                title="Nothing suitable enough right now",
                preview="We do not have someone suitable enough to show right now.",
                explanation="It is better to wait than to show the wrong person. Your process can continue when stronger alignment appears.",
                tone="PROTECTIVE",
                decision_boundary="Raya does not decide outcomes."
            )

        if inputs.review_required or inputs.confidence_level == "MODERATE" or inputs.compatibility_status == "MODERATE_COMPATIBILITY":
            return RayaExplanationResult(
                title="A point for consideration",
                preview="There may be a thoughtful point to discuss.",
                explanation="This is only an invitation to reflect, not a conclusion. Take your time; the decision remains yours.",
                tone="CAUTIOUS",
                decision_boundary="Raya does not decide outcomes. The decision remains with you."
            )

        if inputs.shared_strengths and not inputs.possible_tension_points:
            strengths_str = " and ".join(inputs.shared_strengths[:2])
            preview = f"You both seem to value {strengths_str}." if strengths_str else "You share foundational values."
            explanation = "This may be worth exploring gently. Take your time; the decision remains yours."
            
            return RayaExplanationResult(
                title="A gentle point of alignment",
                preview=preview,
                explanation=explanation,
                tone="GENTLE",
                decision_boundary="Raya does not decide outcomes. The decision remains with you."
            )

        if inputs.possible_tension_points:
            strengths_str = " and ".join(inputs.shared_strengths[:1])
            tensions_str = " and ".join(inputs.possible_tension_points[:1])
            preview_pt1 = f"You both seem to value {strengths_str}. " if strengths_str else ""
            preview = f"{preview_pt1}However, there may be a thoughtful point to discuss regarding {tensions_str}."
            explanation = "This may be worth exploring gently. Take your time; the decision remains yours."
            
            return RayaExplanationResult(
                title="Alignment with points to reflect on",
                preview=preview,
                explanation=explanation,
                tone="BALANCED",
                decision_boundary="Raya does not decide outcomes. The decision remains with you."
            )

        # Default fallback
        return RayaExplanationResult(
            title="A gentle suggestion",
            preview="You share foundational values.",
            explanation="This may be worth exploring gently. Take your time; the decision remains yours.",
            tone="GENTLE",
            decision_boundary="Raya does not decide outcomes. The decision remains with you."
        )
