from sqlalchemy.orm import Session
import uuid
from app.nis.schemas.readiness import ReadinessHomeResponse
from app.nis.services.niyyah_service import NISNiyyahService
from app.nis.services.values_service import NISValuesService
from app.nis.services.mirror_service import NISMirrorService
from app.nis.services.portrait_service import NISPortraitService
from app.nis.services.demographics_service import NISDemographicsService

class NISReadinessService:
    @staticmethod
    def get_readiness_home(db: Session, user_id: uuid.UUID) -> ReadinessHomeResponse:
        niyyah = NISNiyyahService.get_my_niyyah(db, user_id).is_complete
        values = NISValuesService.get_my_values(db, user_id).is_complete
        mirror = NISMirrorService.get_my_mirror(db, user_id).is_complete
        portrait = NISPortraitService.get_my_portrait(db, user_id).is_complete
        
        demographics = False
        try:
            demo_resp = NISDemographicsService.get_my_demographics(db, user_id)
            # Depending on how it's implemented, we just check if it exists and has basic data
            if demo_resp and hasattr(demo_resp, 'age') and demo_resp.age is not None:
                demographics = True
        except Exception:
            pass
            
        is_fully_ready = niyyah and values and mirror and portrait and demographics
        
        return ReadinessHomeResponse(
            niyyah_complete=niyyah,
            values_complete=values,
            mirror_complete=mirror,
            portrait_complete=portrait,
            demographics_complete=demographics,
            is_fully_ready=is_fully_ready
        )
