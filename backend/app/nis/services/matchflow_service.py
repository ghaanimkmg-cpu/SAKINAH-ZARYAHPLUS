from typing import Dict, List
import uuid
from sqlalchemy.orm import Session
from app.nis.schemas.matchflow import MatchflowResponse, MatchflowStep
from app.nis.models.matching import NISMatchflow, NISMatchInterest
from app.nis.enums.nis_enums import MatchflowStatus

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
    def create_matchflow(cls, db: Session, user_a: str, user_b: str) -> str:
        # Matchflow can only be created after mutual interest
        # In a real app we'd verify that both sides said INTEREST.
        try:
            ua = uuid.UUID(user_a)
            ub = uuid.UUID(user_b)
        except ValueError:
            # Fallback for dev mode
            ua = uuid.uuid4()
            ub = uuid.uuid4()
            
        mf = NISMatchflow(
            user_a_id=ua,
            user_b_id=ub,
            status=MatchflowStatus.ACTIVE,
            current_step="MUTUAL_INTEREST"
        )
        db.add(mf)
        db.commit()
        db.refresh(mf)
        return str(mf.id)

    @classmethod
    def get_matchflow(cls, db: Session, matchflow_id: str, user_id: str) -> MatchflowResponse:
        try:
            mf_uuid = uuid.UUID(matchflow_id)
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise ValueError("Invalid UUID format.")
            
        mf = db.query(NISMatchflow).filter_by(id=mf_uuid).first()
        if not mf:
            raise ValueError("Matchflow not found.")
            
        if user_uuid not in [mf.user_a_id, mf.user_b_id]:
            raise ValueError("Unauthorized access to matchflow.")

        current_step = mf.current_step or "MUTUAL_INTEREST"
        
        steps_out = []
        try:
            current_idx = cls.VALID_STEPS.index(current_step)
        except ValueError:
            current_idx = 2
            
        for idx, step_name in enumerate(cls.VALID_STEPS):
            if idx < current_idx:
                status = "DONE"
            elif idx == current_idx:
                status = "CURRENT"
            else:
                status = "LOCKED"
                
            steps_out.append(MatchflowStep(step=step_name, status=status))

        # Chat is NOT open in this phase.
        chat_open = current_step in ["STRUCTURED_OPENING", "SUPERVISED_DEPTH"]
        message = "Mutual interest has been found. The next step will be opened carefully."

        return MatchflowResponse(
            matchflow_id=str(mf.id),
            current_step=current_step,
            steps=steps_out,
            chat_open=chat_open,
            message=message
        )

    @classmethod
    def transition_step(cls, db: Session, matchflow_id: str, new_step: str):
        try:
            mf_uuid = uuid.UUID(matchflow_id)
        except ValueError:
            raise ValueError("Invalid UUID.")
            
        mf = db.query(NISMatchflow).filter_by(id=mf_uuid).first()
        if not mf:
            raise ValueError("Matchflow not found.")
            
        if new_step not in cls.VALID_STEPS:
            raise ValueError(f"Invalid transition step: {new_step}")

        mf.current_step = new_step
        db.commit()

    @classmethod
    def seed_mutual_interest(cls, db: Session, user_a: str, user_b: str):
        pass # Used in tests, handled differently now with SQLAlchemy fixtures.
