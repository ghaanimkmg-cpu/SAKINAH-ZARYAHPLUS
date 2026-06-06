from app.nis.schemas.mutual_interest import InterestActionResponse

# Mock in-memory state for Phase 17 validation
_MOCK_ACTION_STORE = {}
_MOCK_CANDIDATE_STATUS = {}
_MOCK_USER_STATUS = {}

class NISMutualInterestService:
    @classmethod
    def record_interest(cls, actor_id: str, candidate_id: str) -> InterestActionResponse:
        # 1. Check if actor is eligible
        actor_status = _MOCK_USER_STATUS.get(actor_id, "VERIFIED")
        if actor_status in ["BANNED", "UNDER_REVIEW", "INELIGIBLE"]:
            raise ValueError(f"User is {actor_status} and cannot express interest.")

        # 2. Check if candidate is approved / high confidence
        cand_status = _MOCK_CANDIDATE_STATUS.get(candidate_id, "HIGH_CONFIDENCE_MATCH")
        if cand_status != "HIGH_CONFIDENCE_MATCH":
            raise ValueError("Candidate is not approved for matching.")

        # 3. Check existing action
        existing_action = _MOCK_ACTION_STORE.get((actor_id, candidate_id))
        
        if existing_action == "INTEREST":
            pass # Idempotent
        elif existing_action == "PASS":
            raise ValueError("Cannot express interest after passing.")
        else:
            _MOCK_ACTION_STORE[(actor_id, candidate_id)] = "INTEREST"
        
        # 4. Check mutual interest
        reciprocal_action = _MOCK_ACTION_STORE.get((candidate_id, actor_id))
        
        if reciprocal_action == "INTEREST":
            return InterestActionResponse(
                status="MUTUAL_INTEREST",
                mutual_interest=True,
                message="Mutual interest has been found. The next step will be guided carefully."
            )
            
        return InterestActionResponse(
            status="INTEREST_RECORDED",
            mutual_interest=False,
            message="Your interest has been recorded privately."
        )

    @classmethod
    def record_pass(cls, actor_id: str, candidate_id: str) -> InterestActionResponse:
        existing_action = _MOCK_ACTION_STORE.get((actor_id, candidate_id))
        
        if existing_action == "PASS":
            pass # Idempotent
        elif existing_action == "INTEREST":
            # Overwrite interest with pass
            _MOCK_ACTION_STORE[(actor_id, candidate_id)] = "PASS"
        else:
            _MOCK_ACTION_STORE[(actor_id, candidate_id)] = "PASS"

        return InterestActionResponse(
            status="PASS_RECORDED",
            mutual_interest=False,
            message="This has been closed silently."
        )
        
    @classmethod
    def clear_mock_state(cls):
        _MOCK_ACTION_STORE.clear()
        _MOCK_CANDIDATE_STATUS.clear()
        _MOCK_USER_STATUS.clear()
        
    @classmethod
    def seed_mock_state(cls, user_status: dict, candidate_status: dict):
        _MOCK_USER_STATUS.update(user_status)
        _MOCK_CANDIDATE_STATUS.update(candidate_status)
