from app.nis.schemas.kyc import KYCStartResponse, KYCCallbackPayload, KYCStatusResponse
from app.nis.enums.nis_enums import VerificationStatus

class NISKYCService:
    @staticmethod
    async def start_kyc_flow(user_id: str) -> KYCStartResponse:
        """
        Starts the KYC sandbox flow. No real PII in development.
        """
        return KYCStartResponse(
            status="PENDING",
            provider="sandbox",
            message="KYC sandbox flow started."
        )

    @staticmethod
    async def process_callback(payload: KYCCallbackPayload, user_id: str) -> KYCStatusResponse:
        """
        Processes sandbox payload.
        Low liveness/face-match score (< 0.8) must create human review requirement, not hard reject.
        """
        human_review = False
        review_reason = None
        status = VerificationStatus.VERIFIED

        if not payload.verification_passed:
            status = VerificationStatus.REJECTED
        elif payload.liveness_score < 0.8 or payload.face_match_score < 0.8:
            status = VerificationStatus.HUMAN_REVIEW_REQUIRED
            human_review = True
            reasons = []
            if payload.liveness_score < 0.8:
                reasons.append("Low liveness score")
            if payload.face_match_score < 0.8:
                reasons.append("Low face match score")
            review_reason = " | ".join(reasons)

        # In a real implementation with DB session, we would create/update NISKycVerification and NISUser here.
        # Minimal verification data is stored. No raw Aadhaar or selfie image is handled.

        return KYCStatusResponse(
            verification_status=status,
            human_review_required=human_review,
            review_reason=review_reason,
            message="KYC callback processed successfully."
        )
