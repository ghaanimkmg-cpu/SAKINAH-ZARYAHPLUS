from typing import Optional
from sqlalchemy.orm import Session
from app.nis.schemas.user_signal_profile import UserSignalProfile
from app.nis.models.profiles import NISUserSignalProfile
from app.nis.enums.nis_enums import SafetyRiskLevel, ConfidenceLevel

import uuid

def _float_to_str(val: Optional[float]) -> str:
    if val is None: return "UNKNOWN"
    if val >= 0.8: return "HIGH"
    if val <= 0.3: return "LOW"
    return "MODERATE"

def _str_to_float(val: str) -> float:
    if val == "HIGH": return 0.9
    if val == "LOW": return 0.2
    if val == "MODERATE": return 0.5
    return 0.5

class NISUserSignalProfileService:
    @staticmethod
    def get_profile(db: Session, user_id: str) -> Optional[UserSignalProfile]:
        """
        Retrieves the user's signal profile. Returns default if none exists.
        """
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            u_uuid = uuid.uuid4()
            
        record = db.query(NISUserSignalProfile).filter_by(user_id=u_uuid).first()
        if record:
            return UserSignalProfile(
                emotional_steadiness=_float_to_str(record.emotional_steadiness),
                communication_style=record.communication_style or "UNKNOWN",
                conflict_repair_style=record.conflict_repair_style or "UNKNOWN",
                family_responsibility=record.family_responsibility or "UNKNOWN",
                deen_alignment=record.deen_alignment or "UNKNOWN",
                marriage_readiness=_float_to_str(record.marriage_readiness),
                financial_expectation=record.financial_expectation or "UNKNOWN",
                wali_comfort=record.wali_comfort or "UNKNOWN",
                life_direction=record.life_direction or "UNKNOWN",
                self_awareness_level=_float_to_str(record.self_awareness_level),
                social_lifestyle=record.social_lifestyle or "UNKNOWN",
                safety_risk_level=record.safety_risk_level.name if record.safety_risk_level else "LOW",
                confidence_level=record.confidence_level.name if record.confidence_level else "LOW",
                missing_signal_areas=record.missing_signal_areas or [],
                review_required=record.review_required or False
            )
            
        # Return a safe empty/default profile if none exists
        return UserSignalProfile(
            emotional_steadiness="UNKNOWN",
            communication_style="UNKNOWN",
            conflict_repair_style="UNKNOWN",
            family_responsibility="UNKNOWN",
            deen_alignment="UNKNOWN",
            marriage_readiness="UNKNOWN",
            financial_expectation="UNKNOWN",
            wali_comfort="UNKNOWN",
            life_direction="UNKNOWN",
            self_awareness_level="UNKNOWN",
            social_lifestyle="UNKNOWN"
        )

    @staticmethod
    def update_profile(db: Session, user_id: str, profile: UserSignalProfile) -> UserSignalProfile:
        """
        Updates the user's signal profile.
        """
        try:
            u_uuid = uuid.UUID(user_id)
        except ValueError:
            u_uuid = uuid.uuid4()
            
        record = db.query(NISUserSignalProfile).filter_by(user_id=u_uuid).first()
        if not record:
            record = NISUserSignalProfile(user_id=u_uuid)
            db.add(record)
            
        record.emotional_steadiness = _str_to_float(profile.emotional_steadiness)
        record.communication_style = profile.communication_style
        record.conflict_repair_style = profile.conflict_repair_style
        record.family_responsibility = profile.family_responsibility
        record.deen_alignment = profile.deen_alignment
        record.marriage_readiness = _str_to_float(profile.marriage_readiness)
        record.financial_expectation = profile.financial_expectation
        record.wali_comfort = profile.wali_comfort
        record.life_direction = profile.life_direction
        record.self_awareness_level = _str_to_float(profile.self_awareness_level)
        record.social_lifestyle = profile.social_lifestyle
        record.missing_signal_areas = profile.missing_signal_areas
        record.review_required = profile.review_required
        
        try:
            record.safety_risk_level = SafetyRiskLevel[profile.safety_risk_level]
        except KeyError:
            record.safety_risk_level = SafetyRiskLevel.LOW
            
        try:
            record.confidence_level = ConfidenceLevel[profile.confidence_level]
        except KeyError:
            record.confidence_level = ConfidenceLevel.LOW
            
        db.commit()
        db.refresh(record)
        return profile
