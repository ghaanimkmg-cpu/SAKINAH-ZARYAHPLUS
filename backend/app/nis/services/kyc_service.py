from app.nis.schemas.kyc import KYCStartResponse, KYCStatusResponse, KycSandboxPayload, LivenessStartResponse, LivenessStatusResponse, LivenessSandboxPayload
from app.nis.services.kyc_vendor_adapter import SandboxKycVendorAdapter

class NISKYCService:
    @staticmethod
    async def start_kyc_flow(user_id: str) -> KYCStartResponse:
        res = SandboxKycVendorAdapter.start_kyc_session(user_id)
        return KYCStartResponse(
            status=res["status"],
            session_id=res.get("session_id"),
            message=res.get("message", "")
        )

    @staticmethod
    async def get_kyc_status(user_id: str) -> KYCStatusResponse:
        res = SandboxKycVendorAdapter.get_verification_status(user_id)
        return KYCStatusResponse(
            status=res["status"],
            verification_level=res.get("verification_level"),
            human_review_required=res.get("human_review_required", False),
            failure_reason=res.get("failure_reason")
        )

    @staticmethod
    async def process_kyc_sandbox(payload: KycSandboxPayload, user_id: str) -> KYCStatusResponse:
        res = SandboxKycVendorAdapter.submit_government_id_sandbox(user_id, payload)
        # Here we would update NISDemographicProfile
        # e.g. verified_identity_name = payload.verified_name
        return KYCStatusResponse(
            status=res["status"],
            verification_level="FULL",
            human_review_required=False
        )

    @staticmethod
    async def start_liveness_flow(user_id: str) -> LivenessStartResponse:
        res = SandboxKycVendorAdapter.start_liveness_session(user_id)
        return LivenessStartResponse(
            status=res["status"],
            session_id=res.get("session_id"),
            message=res.get("message", "")
        )

    @staticmethod
    async def get_liveness_status(user_id: str) -> LivenessStatusResponse:
        res = SandboxKycVendorAdapter.get_verification_status(user_id)
        return LivenessStatusResponse(
            status=res["status"],
            liveness_status=res.get("liveness_status"),
            face_match_status=res.get("face_match_status"),
            human_review_required=res.get("human_review_required", False)
        )

    @staticmethod
    async def process_liveness_sandbox(payload: LivenessSandboxPayload, user_id: str) -> LivenessStatusResponse:
        res = SandboxKycVendorAdapter.process_liveness_callback(user_id, payload)
        return LivenessStatusResponse(
            status=res["status"],
            liveness_status=res.get("liveness_status"),
            face_match_status=res.get("face_match_status"),
            human_review_required=res.get("human_review_required", False)
        )
