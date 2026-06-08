from sqlalchemy.orm import Session
import uuid
from app.nis.models.profiles import NISMirrorReflection
from app.nis.schemas.mirror import MirrorUpdateRequest, MirrorResponse

class NISMirrorService:
    @staticmethod
    def get_my_mirror(db: Session, user_id: uuid.UUID) -> MirrorResponse:
        mirror = db.query(NISMirrorReflection).filter_by(user_id=user_id).first()
        if not mirror:
            return MirrorResponse(reflection_data={}, is_complete=False)
        is_complete = bool(mirror.reflection_data and len(mirror.reflection_data) > 0)
        return MirrorResponse(reflection_data=mirror.reflection_data, is_complete=is_complete)

    @staticmethod
    def update_my_mirror(db: Session, user_id: uuid.UUID, request: MirrorUpdateRequest) -> MirrorResponse:
        mirror = db.query(NISMirrorReflection).filter_by(user_id=user_id).first()
        if not mirror:
            mirror = NISMirrorReflection(user_id=user_id, reflection_data=request.reflection_data)
            db.add(mirror)
        else:
            mirror.reflection_data = request.reflection_data
        db.commit()
        db.refresh(mirror)
        
        is_complete = bool(mirror.reflection_data and len(mirror.reflection_data) > 0)
        return MirrorResponse(reflection_data=mirror.reflection_data, is_complete=is_complete)
