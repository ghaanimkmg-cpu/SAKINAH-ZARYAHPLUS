import uuid
from sqlalchemy.orm import Session
from app.nis.schemas.mutual_interest import InterestActionResponse
from app.nis.models.matching import NISMatchInterest
from app.nis.enums.nis_enums import MatchInterestStatus

class NISMutualInterestService:
    @classmethod
    def record_interest(cls, db: Session, actor_id: str, candidate_id: str) -> InterestActionResponse:
        try:
            actor_uuid = uuid.UUID(actor_id)
            cand_uuid = uuid.UUID(candidate_id)
        except ValueError:
            actor_uuid = uuid.uuid4()
            cand_uuid = uuid.uuid4()
            
        existing = db.query(NISMatchInterest).filter_by(sender_id=actor_uuid, receiver_id=cand_uuid).first()
        if existing:
            if existing.status == MatchInterestStatus.PASSED:
                raise ValueError("Cannot express interest after passing.")
            existing.status = MatchInterestStatus.INTERESTED
        else:
            new_interest = NISMatchInterest(
                sender_id=actor_uuid,
                receiver_id=cand_uuid,
                status=MatchInterestStatus.INTERESTED
            )
            db.add(new_interest)
            
        db.commit()

        # Check mutual interest
        reciprocal = db.query(NISMatchInterest).filter_by(sender_id=cand_uuid, receiver_id=actor_uuid, status=MatchInterestStatus.INTERESTED).first()
        
        if reciprocal:
            return InterestActionResponse(
                status="MUTUAL_INTEREST",
                mutual_interest=True,
                message="Mutual interest has been found. The next step will be guided carefully."
            )
            
        return InterestActionResponse(
            status="INTEREST_RECORDED",
            mutual_interest=False,
            message="Your interest has been recorded privately."
        )

    @classmethod
    def record_pass(cls, db: Session, actor_id: str, candidate_id: str) -> InterestActionResponse:
        try:
            actor_uuid = uuid.UUID(actor_id)
            cand_uuid = uuid.UUID(candidate_id)
        except ValueError:
            actor_uuid = uuid.uuid4()
            cand_uuid = uuid.uuid4()
            
        existing = db.query(NISMatchInterest).filter_by(sender_id=actor_uuid, receiver_id=cand_uuid).first()
        if existing:
            existing.status = MatchInterestStatus.PASSED
        else:
            new_pass = NISMatchInterest(
                sender_id=actor_uuid,
                receiver_id=cand_uuid,
                status=MatchInterestStatus.PASSED
            )
            db.add(new_pass)
            
        db.commit()

        return InterestActionResponse(
            status="PASS_RECORDED",
            mutual_interest=False,
            message="This has been closed silently."
        )
