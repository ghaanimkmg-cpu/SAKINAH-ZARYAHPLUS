from sqlalchemy.orm import Session
import uuid
from app.nis.models.profiles import NISNiyyahIntention
from app.nis.schemas.niyyah import NiyyahUpdateRequest, NiyyahResponse

class NISNiyyahService:
    @staticmethod
    def get_my_niyyah(db: Session, user_id: uuid.UUID) -> NiyyahResponse:
        niyyah = db.query(NISNiyyahIntention).filter_by(user_id=user_id).first()
        if not niyyah:
            return NiyyahResponse(intention_text=None, is_complete=False)
        is_complete = bool(niyyah.intention_text and len(niyyah.intention_text.strip()) > 0)
        return NiyyahResponse(intention_text=niyyah.intention_text, is_complete=is_complete)

    @staticmethod
    def update_my_niyyah(db: Session, user_id: uuid.UUID, request: NiyyahUpdateRequest) -> NiyyahResponse:
        niyyah = db.query(NISNiyyahIntention).filter_by(user_id=user_id).first()
        if not niyyah:
            niyyah = NISNiyyahIntention(user_id=user_id, intention_text=request.intention_text)
            db.add(niyyah)
        else:
            niyyah.intention_text = request.intention_text
        db.commit()
        db.refresh(niyyah)
        
        is_complete = bool(niyyah.intention_text and len(niyyah.intention_text.strip()) > 0)
        return NiyyahResponse(intention_text=niyyah.intention_text, is_complete=is_complete)
