from sqlalchemy.orm import Session
import uuid
from app.nis.models.profiles import NISValuesProfile
from app.nis.schemas.values import ValuesUpdateRequest, ValuesResponse

class NISValuesService:
    @staticmethod
    def get_my_values(db: Session, user_id: uuid.UUID) -> ValuesResponse:
        vp = db.query(NISValuesProfile).filter_by(user_id=user_id).first()
        if not vp:
            return ValuesResponse(values_data={}, is_complete=False)
        is_complete = bool(vp.values_data and len(vp.values_data) > 0)
        return ValuesResponse(values_data=vp.values_data, is_complete=is_complete)

    @staticmethod
    def update_my_values(db: Session, user_id: uuid.UUID, request: ValuesUpdateRequest) -> ValuesResponse:
        vp = db.query(NISValuesProfile).filter_by(user_id=user_id).first()
        if not vp:
            vp = NISValuesProfile(user_id=user_id, values_data=request.values_data)
            db.add(vp)
        else:
            vp.values_data = request.values_data
        db.commit()
        db.refresh(vp)
        
        is_complete = bool(vp.values_data and len(vp.values_data) > 0)
        return ValuesResponse(values_data=vp.values_data, is_complete=is_complete)
