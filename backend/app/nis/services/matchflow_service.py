from typing import Dict, Set, FrozenSet
import uuid
from app.nis.schemas.matchflow import MatchflowResponse, MatchflowStep

_MOCK_MATCHFLOW_DB: Dict[str, dict] = {}
_MOCK_MUTUAL_INTERESTS: Set[FrozenSet[str]] = set()

class NISMatchflowService:
    VALID_STEPS = [
        "PROFILES_COMPLETE",
        "COMPATIBILITY_IDENTIFIED",
        "MUTUAL_INTEREST",
        "STRUCTURED_OPENING",
        "WALI_INVITABLE",
        "SUPERVISED_DEPTH",
        "DECISION"
    ]

    @classmethod
    def create_matchflow(cls, user_a: str, user_b: str) -> str:
        # Matchflow can only be created after mutual interest
        pair = frozenset([user_a, user_b])
        if pair not in _MOCK_MUTUAL_INTERESTS:
            raise ValueError("Matchflow can only be created after mutual interest is established.")
            
        mf_id = f"mf_{uuid.uuid4().hex[:8]}"
        _MOCK_MATCHFLOW_DB[mf_id] = {
            "users": pair,
            "current_step": "MUTUAL_INTEREST"
        }
        return mf_id

    @classmethod
    def get_matchflow(cls, matchflow_id: str, user_id: str) -> MatchflowResponse:
        mf = _MOCK_MATCHFLOW_DB.get(matchflow_id)
        if not mf:
            raise ValueError("Matchflow not found.")
            
        if user_id not in mf["users"]:
            raise ValueError("Unauthorized access to matchflow.")

        current_step = mf["current_step"]
        
        steps_out = []
        current_idx = cls.VALID_STEPS.index(current_step)
        
        for idx, step_name in enumerate(cls.VALID_STEPS):
            if idx < current_idx:
                status = "DONE"
            elif idx == current_idx:
                status = "CURRENT"
            else:
                status = "LOCKED"
                
            steps_out.append(MatchflowStep(step=step_name, status=status))

        # Chat is NOT open in this phase.
        chat_open = False
        message = "Mutual interest has been found. The next step will be opened carefully."

        return MatchflowResponse(
            matchflow_id=matchflow_id,
            current_step=current_step,
            steps=steps_out,
            chat_open=chat_open,
            message=message
        )

    @classmethod
    def transition_step(cls, matchflow_id: str, new_step: str):
        mf = _MOCK_MATCHFLOW_DB.get(matchflow_id)
        if not mf:
            raise ValueError("Matchflow not found.")
            
        if new_step not in cls.VALID_STEPS:
            raise ValueError(f"Invalid transition step: {new_step}")

        current_idx = cls.VALID_STEPS.index(mf["current_step"])
        new_idx = cls.VALID_STEPS.index(new_step)

        if new_idx != current_idx + 1:
            raise ValueError("Invalid state transition sequence.")

        mf["current_step"] = new_step

    @classmethod
    def clear_mock_state(cls):
        _MOCK_MATCHFLOW_DB.clear()
        _MOCK_MUTUAL_INTERESTS.clear()

    @classmethod
    def seed_mutual_interest(cls, user_a: str, user_b: str):
        _MOCK_MUTUAL_INTERESTS.add(frozenset([user_a, user_b]))
