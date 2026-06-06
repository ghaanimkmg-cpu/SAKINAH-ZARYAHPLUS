from typing import Optional
from app.nis.schemas.user_signal_profile import UserSignalProfile

# In-memory mock store for test safety until DB wiring
_mock_profiles = {}

class NISUserSignalProfileService:
    @staticmethod
    async def get_profile(user_id: str) -> Optional[UserSignalProfile]:
        """
        Retrieves the user's signal profile. Returns default if none exists.
        """
        if user_id in _mock_profiles:
            return _mock_profiles[user_id]
            
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
    async def update_profile(user_id: str, profile: UserSignalProfile) -> UserSignalProfile:
        """
        Updates the user's signal profile.
        """
        _mock_profiles[user_id] = profile
        return profile
