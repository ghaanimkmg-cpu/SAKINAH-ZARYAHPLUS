from app.nis.schemas.kyc import EligibilityResponse
from app.nis.enums.nis_enums import EligibilityStatus

class NISEligibilityService:
    @staticmethod
    async def check_eligibility(user_id: str, is_banned: bool = False, kyc_status: str = "VERIFIED") -> EligibilityResponse:
        """
        Determines user eligibility. Unverified or banned users are not matchable.
        """
        if is_banned:
            return EligibilityResponse(
                eligibility_status=EligibilityStatus.BANNED,
                can_enter_matching=False,
                requires_human_review=False,
                message="User is banned and cannot enter matching."
            )

        if kyc_status == "HUMAN_REVIEW_REQUIRED":
            return EligibilityResponse(
                eligibility_status=EligibilityStatus.HUMAN_REVIEW_REQUIRED,
                can_enter_matching=False,
                requires_human_review=True,
                message="Your profile is under human review."
            )

        if kyc_status != "VERIFIED":
            return EligibilityResponse(
                eligibility_status=EligibilityStatus.PENDING,
                can_enter_matching=False,
                requires_human_review=False,
                message="You must complete KYC verification to enter matching."
            )

        return EligibilityResponse(
            eligibility_status=EligibilityStatus.VERIFIED,
            can_enter_matching=True,
            requires_human_review=False,
            message="You are eligible to continue."
        )
