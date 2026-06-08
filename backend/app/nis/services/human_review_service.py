import uuid
from typing import Dict, List
from sqlalchemy.orm import Session
from app.nis.schemas.human_review import ReviewDecisionRequest, ReviewDecisionResponse
from app.nis.models.safety import NISHumanReview, NISIdentityBan
from app.nis.enums.nis_enums import HumanReviewStatus, HumanReviewDecision

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
    def create_review(cls, db: Session, flag_id: str, user_id: str, severity: str) -> str:
        # We don't link to a real KYC yet. We just create a pending review.
        rev = NISHumanReview(
            user_id=uuid.UUID(user_id),
            status=HumanReviewStatus.PENDING
        )
        db.add(rev)
        db.commit()
        db.refresh(rev)
        
        # We also need a way to track the user state. Since this is an audit only,
        # we will use the identity bans table for BANNED, but for others we'd need
        # a user table status column. For now, we mock the state or fetch it.
        return str(rev.id)

    @classmethod
    def submit_decision(cls, db: Session, review_id: str, request: ReviewDecisionRequest, admin_id: str) -> ReviewDecisionResponse:
        try:
            rev_uuid = uuid.UUID(review_id)
        except ValueError:
            raise ValueError("Review not found.")
            
        rev = db.query(NISHumanReview).filter_by(id=rev_uuid).first()
        if not rev:
            raise ValueError("Review not found.")
            
        if request.decision not in cls.VALID_ACTIONS:
            raise ValueError("Invalid review decision.")

        try:
            decision_enum = HumanReviewDecision[request.decision]
        except KeyError:
            decision_enum = HumanReviewDecision.NO_ACTION

        rev.status = HumanReviewStatus.COMPLETED
        rev.decision = decision_enum
        rev.reviewer_notes = request.notes
        db.commit()

        # Assuming user_id could be tracked, but schema doesn't link user directly in HumanReview
        # It links via KYC or Report.
        # If ban, we add to IdentityBan and update user
        if request.decision == "PERMANENT_BAN":
            ban = NISIdentityBan(identity_hash=str(uuid.uuid4().hex), reason=request.notes or "Banned via review")
            db.add(ban)
            from app.nis.models.user import NISUser
            u = db.query(NISUser).filter_by(id=rev.user_id).first()
            if u:
                u.eligibility_status = "BANNED"
            db.commit()
            
        return ReviewDecisionResponse(
            review_id=review_id,
            decision=request.decision,
            status="RESOLVED",
            message="Review decision recorded."
        )
        
    @classmethod
    def get_user_status(cls, db: Session, user_id: str) -> str:
        from app.nis.models.user import NISUser
        u = db.query(NISUser).filter_by(id=uuid.UUID(user_id)).first()
        if u:
            return u.eligibility_status.name if hasattr(u.eligibility_status, 'name') else str(u.eligibility_status)
        return "VERIFIED"

    @classmethod
    def check_matchmaking_eligibility(cls, db: Session, user_id: str) -> bool:
        status = cls.get_user_status(db, user_id)
        return status not in ["BANNED", "UNDER_REVIEW", "PAUSED", "NOT_STARTED"]

    @classmethod
    def list_reviews(cls, db: Session) -> List[dict]:
        reviews = db.query(NISHumanReview).all()
        result = []
        for rev in reviews:
            result.append({
                "review_id": str(rev.id),
                "user_id": str(rev.user_id),
                "severity": "HIGH",
                "status": rev.status.name if rev.status else "PENDING",
                "flag_id": "unknown",
                "decision": rev.decision.name if rev.decision else None
            })
        return result
