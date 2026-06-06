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
