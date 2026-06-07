from sqlalchemy.orm import Session
from app.nis.models.demographics import NISDemographicProfile
from typing import Optional
import uuid

class NISDemographicsService:
    @classmethod
    def get_demographics(cls, db: Session, user_id: str) -> Optional[NISDemographicProfile]:
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            return None
        return db.query(NISDemographicProfile).filter_by(user_id=u_uuid).first()
        
    @classmethod
    def is_demographics_complete(cls, profile: Optional[NISDemographicProfile]) -> bool:
        if not profile:
            return False
        # Phase K.2 simple completeness check
        required_fields = [
            profile.age,
            profile.gender,
            profile.location,
            profile.tradition,
            profile.marital_status
        ]
        return all(f is not None for f in required_fields)
