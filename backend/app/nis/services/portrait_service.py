from sqlalchemy.orm import Session
import uuid
from app.nis.models.profiles import NISPrivatePortrait
from app.nis.schemas.portrait import PortraitUpdateRequest, PortraitResponse

class NISPortraitService:
    @staticmethod
    def get_my_portrait(db: Session, user_id: uuid.UUID) -> PortraitResponse:
        portrait = db.query(NISPrivatePortrait).filter_by(user_id=user_id).first()
        if not portrait:
            return PortraitResponse(portrait_data={}, is_complete=False)
        is_complete = bool(portrait.portrait_data and len(portrait.portrait_data) > 0)
        return PortraitResponse(portrait_data=portrait.portrait_data, is_complete=is_complete)

    @staticmethod
    def update_my_portrait(db: Session, user_id: uuid.UUID, request: PortraitUpdateRequest) -> PortraitResponse:
        portrait = db.query(NISPrivatePortrait).filter_by(user_id=user_id).first()
        if not portrait:
            portrait = NISPrivatePortrait(user_id=user_id, portrait_data=request.portrait_data)
            db.add(portrait)
        else:
            portrait.portrait_data = request.portrait_data
        db.commit()
        db.refresh(portrait)
        
        is_complete = bool(portrait.portrait_data and len(portrait.portrait_data) > 0)
        return PortraitResponse(portrait_data=portrait.portrait_data, is_complete=is_complete)
