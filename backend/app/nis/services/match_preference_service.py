from typing import Optional
from sqlalchemy.orm import Session
from app.nis.schemas.match_preferences import MatchPreferences
from app.nis.models.preferences import NISMatchPreference

import uuid

class NISMatchPreferenceService:
    @staticmethod
    def get_preferences(db: Session, user_id: str) -> Optional[MatchPreferences]:
        """
        Retrieves the user's match preferences. Returns default if none exists.
        """
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            u_uuid = uuid.uuid4()
            
        record = db.query(NISMatchPreference).filter_by(user_id=u_uuid).first()
        if record:
            return MatchPreferences(
                age_range_min=record.age_range_min or 18,
                age_range_max=record.age_range_max or 99,
                location_preference=record.location_preference or "ANY",
                relocation_openness=str(record.relocation_openness) if record.relocation_openness is not None else "ANY",
                nikah_timeline=record.nikah_timeline or "UNKNOWN",
                tradition_preference=record.tradition_preference or "ANY",
                wali_involvement_preference=record.wali_involvement_preference or "ANY",
                marital_status_preference=record.marital_status_preference or "ANY",
                financial_expectation_preference=record.financial_expectation_preference or "ANY"
            )
            
        # Return safe default
        return MatchPreferences(
            age_range_min=18,
            age_range_max=99,
            location_preference="ANY",
            relocation_openness="ANY",
            nikah_timeline="UNKNOWN",
            tradition_preference="ANY",
            wali_involvement_preference="ANY",
            marital_status_preference="ANY",
            financial_expectation_preference="ANY"
        )

    @staticmethod
    def update_preferences(db: Session, user_id: str, preferences: MatchPreferences) -> MatchPreferences:
        """
        Updates the user's match preferences.
        """
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            u_uuid = uuid.uuid4()
            
        record = db.query(NISMatchPreference).filter_by(user_id=u_uuid).first()
        if not record:
            record = NISMatchPreference(user_id=u_uuid)
            db.add(record)
        
        record.age_range_min = preferences.age_range_min
        record.age_range_max = preferences.age_range_max
        record.location_preference = preferences.location_preference
        record.relocation_openness = preferences.relocation_openness.lower() == "true" if preferences.relocation_openness not in ("ANY", "UNKNOWN") else None
        record.nikah_timeline = preferences.nikah_timeline
        record.tradition_preference = preferences.tradition_preference
        record.wali_involvement_preference = preferences.wali_involvement_preference
        record.marital_status_preference = preferences.marital_status_preference
        record.financial_expectation_preference = preferences.financial_expectation_preference
        
        db.commit()
        db.refresh(record)
        
        return preferences
