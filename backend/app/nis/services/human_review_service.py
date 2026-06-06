import uuid
from typing import Dict
from app.nis.schemas.human_review import ReviewDecisionRequest, ReviewDecisionResponse

_MOCK_REVIEWS_DB: Dict[str, dict] = {}
_MOCK_USER_STATES: Dict[str, str] = {}
_MOCK_IDENTITY_BANS: set = set()

class NISHumanReviewService:
    VALID_ACTIONS = [
        "NO_ACTION",
        "WARN_USER",
        "LIMIT_ACCOUNT",
        "PAUSE_MATCHMAKING",
        "PERMANENT_BAN",
        "ESCALATE_TO_SCHOLAR_COUNSELLOR"
    ]

    @classmethod
    def create_review(cls, flag_id: str, user_id: str, severity: str) -> str:
        rev_id = f"rev_{uuid.uuid4().hex[:8]}"
        _MOCK_REVIEWS_DB[rev_id] = {
            "flag_id": flag_id,
            "user_id": user_id,
            "severity": severity,
            "status": "PENDING"
        }
        _MOCK_USER_STATES[user_id] = "UNDER_REVIEW"
        return rev_id

    @classmethod
    def submit_decision(cls, review_id: str, request: ReviewDecisionRequest, admin_id: str) -> ReviewDecisionResponse:
        rev = _MOCK_REVIEWS_DB.get(review_id)
        if not rev:
            raise ValueError("Review not found.")
            
        if request.decision not in cls.VALID_ACTIONS:
            raise ValueError("Invalid review decision.")

        rev["decision"] = request.decision
        rev["status"] = "RESOLVED"
        rev["admin_id"] = admin_id
        rev["notes"] = request.notes

        user_id = rev["user_id"]

        if request.decision == "PERMANENT_BAN":
            _MOCK_USER_STATES[user_id] = "BANNED"
            _MOCK_IDENTITY_BANS.add(user_id)
        elif request.decision == "PAUSE_MATCHMAKING":
            _MOCK_USER_STATES[user_id] = "PAUSED"
        elif request.decision in ["NO_ACTION", "WARN_USER"]:
            _MOCK_USER_STATES[user_id] = "VERIFIED"
        elif request.decision == "LIMIT_ACCOUNT":
            _MOCK_USER_STATES[user_id] = "LIMITED"
            
        return ReviewDecisionResponse(
            review_id=review_id,
            decision=request.decision,
            status="RESOLVED",
            message="Review decision recorded."
        )
        
    @classmethod
    def get_user_status(cls, user_id: str) -> str:
        if user_id in _MOCK_IDENTITY_BANS:
            return "BANNED"
        return _MOCK_USER_STATES.get(user_id, "VERIFIED")

    @classmethod
    def check_matchmaking_eligibility(cls, user_id: str) -> bool:
        status = cls.get_user_status(user_id)
        return status not in ["BANNED", "UNDER_REVIEW", "PAUSED"]

    @classmethod
    def clear_mock_state(cls):
        _MOCK_REVIEWS_DB.clear()
        _MOCK_USER_STATES.clear()
        _MOCK_IDENTITY_BANS.clear()
