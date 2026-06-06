from typing import Optional
from app.nis.schemas.match_preferences import MatchPreferences

# In-memory mock store for test safety until DB wiring
_mock_preferences = {}

class NISMatchPreferenceService:
    @staticmethod
    async def get_preferences(user_id: str) -> Optional[MatchPreferences]:
        """
        Retrieves the user's match preferences. Returns default if none exists.
        """
        if user_id in _mock_preferences:
            return _mock_preferences[user_id]
            
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
    async def update_preferences(user_id: str, preferences: MatchPreferences) -> MatchPreferences:
        """
        Updates the user's match preferences.
        """
        _mock_preferences[user_id] = preferences
        return preferences
