from typing import Dict, Any, Optional
from app.core.config import settings
from app.nis.schemas.kyc import KycSandboxPayload, LivenessSandboxPayload

class SandboxKycVendorAdapter:
    """
    KYC / Liveness adapter interface.
    This acts as a placeholder for the real vendor integration (e.g. Onfido, SumSub)
    required by Omar's brief.
    """

    @staticmethod
    def start_kyc_session(user_id: str) -> Dict[str, Any]:
        if settings.APP_ENV != "development":
            # Production requires real vendor configuration
            if not settings.KYC_PROVIDER_API_KEY:
                return {"status": "VENDOR_NOT_CONFIGURED", "message": "Production vendor pending."}
            # ... call real vendor ...
            return {"status": "ERROR", "message": "Real vendor not fully implemented."}
            
        return {
            "status": "SANDBOX_READY",
            "session_id": f"sandbox_kyc_{user_id}",
            "message": "Development Sandbox KYC session started"
        }

    @staticmethod
    def submit_government_id_sandbox(user_id: str, payload: KycSandboxPayload) -> Dict[str, Any]:
        if settings.APP_ENV != "development":
            raise ValueError("Sandbox completion not allowed in production")
            
        return {
            "status": "VERIFIED",
            "verified_name": payload.verified_name,
            "verified_age": payload.verified_age,
            "verified_gender": payload.verified_gender
        }

    @staticmethod
    def start_liveness_session(user_id: str) -> Dict[str, Any]:
        if settings.APP_ENV != "development":
            if not settings.KYC_PROVIDER_API_KEY:
                return {"status": "VENDOR_NOT_CONFIGURED", "message": "Production vendor pending."}
            return {"status": "ERROR", "message": "Real vendor not fully implemented."}

        return {
            "status": "SANDBOX_READY",
            "session_id": f"sandbox_liveness_{user_id}",
            "message": "Development Sandbox Liveness session started"
        }

    @staticmethod
    def process_liveness_callback(user_id: str, payload: LivenessSandboxPayload) -> Dict[str, Any]:
        if settings.APP_ENV != "development":
            raise ValueError("Sandbox completion not allowed in production")

        human_review = False
        if payload.face_match_status == "WEAK" or payload.liveness_status == "WEAK":
            human_review = True

        return {
            "status": "VERIFIED" if not human_review else "PENDING_REVIEW",
            "liveness_status": payload.liveness_status,
            "face_match_status": payload.face_match_status,
            "human_review_required": human_review
        }

    @staticmethod
    def get_verification_status(user_id: str) -> Dict[str, Any]:
        if settings.APP_ENV != "development":
            if not settings.KYC_PROVIDER_API_KEY:
                return {"status": "VENDOR_NOT_CONFIGURED"}
        return {"status": "PENDING"}
