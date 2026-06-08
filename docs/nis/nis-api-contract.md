# NIS API Contract

This document outlines the API contracts for the Sakinah NIS backend, covering base URLs, auth, privacy rules, frontend integration notes, and endpoint-by-endpoint details.

## 1. API Base URL
- **Local Development:** `http://localhost:8000/api/v1`
- **Production:** (Pending final deployment URL)

## 2. Auth / User Context Requirement
Most endpoints require a valid user context. The backend uses a server-side dependency (`get_current_user`) to resolve the user.

## 3. Development Auth Behavior
During development, the `get_current_user` dependency looks for the `X-Test-User-Id` header to mock the authenticated user context.

## 4. Production Auth Pending Note
> [!WARNING]
> In production, the `get_current_user` dependency will be replaced by a strict JWT/Session verification system. The current header-based system is for development and testing only.

## 5. Admin Route Protection Warning
> [!WARNING]
> Admin routes currently use the standard placeholder auth for integration testing. Before production, these routes MUST be protected by a strict `is_admin_user` dependency.

## 6. Request/Response Examples
Requests generally accept JSON payloads. Responses will be JSON with standard HTTP status codes.

## 7. Error Format
Errors follow the standard FastAPI structure:
```json
{
  "detail": "Error message explanation"
}
```

## 8. Data Privacy Rules
The API must **never** expose:
- Raw Aadhaar numbers
- Raw government IDs
- Raw ID document images
- Raw selfie images
- Raw Raya conversations
- Raw Barakah Lab entries
- Worship score
- Gratitude score
- Spiritual rank
- Compatibility percentage
- Reporter identity to the reported user
- Rejection notifications
- Who-liked-you data

## 9. No Firebase Rule
> [!IMPORTANT]
> This system strictly uses standard backend endpoints. Firebase SDKs, Firestore, and Firebase Realtime Database are explicitly banned to protect algorithmic integrity and ensure backend server authority.

## 10. Frontend Integration Notes
> [!IMPORTANT]
> - Frontend **must not** calculate compatibility.
> - Frontend **must not** decide eligibility.
> - Frontend **must not** open chat by itself.
> - Frontend **must not** unlock conversation topics by itself.
> - Frontend **must not** create matchflow by itself.
> - Frontend **must not** display rejected/pass notifications.
> - Frontend **must not** show photos before the backend explicitly allows it.
> - **Backend/NIS is server-authoritative.**

---

## 11. Endpoint-by-Endpoint Contract

### Health
- **GET /health**
  - **Purpose:** Base app health check.
  - **Auth:** None
  - **Response:** `{"status": "ok"}`
- **GET /api/v1/health**
  - **Purpose:** API v1 health check.
  - **Auth:** None
  - **Response:** `{"status": "healthy", "version": "1.0.0"}`

### Auth / User Context
- **GET /api/v1/nis/auth/me**
  - **Purpose:** Retrieve the current authenticated user context.
  - **Auth:** Required
  - **Response:** `{"user_id": "user_123", "roles": ["USER"]}`

### KYC / Eligibility
- **POST /api/v1/nis/kyc/start**
  - **Purpose:** Initiate the KYC process.
  - **Auth:** Required
  - **Response:** `{"status": "PENDING"}`
- **POST /api/v1/nis/kyc/callback**
  - **Purpose:** Webhook callback for KYC status updates.
  - **Auth:** Webhook verification
  - **Response:** `{"status": "RECEIVED"}`
- **GET /api/v1/nis/eligibility/me**
  - **Purpose:** Check current eligibility state.
  - **Auth:** Required
  - **Response:** `{"is_eligible": true, "reasons": []}`

### Profile / Preferences
- **GET /api/v1/nis/profile/me**
  - **Purpose:** Retrieve the user's public/search profile data.
  - **Auth:** Required
  - **Response:** `{"bio": "...", "traits": []}`
- **PUT /api/v1/nis/profile/me**
  - **Purpose:** Update the user's profile.
  - **Auth:** Required
  - **Body:** `{"bio": "New bio"}`
  - **Response:** `{"status": "UPDATED"}`
- **GET /api/v1/nis/preferences/me**
  - **Purpose:** Retrieve the user's match preferences.
  - **Auth:** Required
  - **Response:** `{"age_min": 25, "age_max": 35}`
- **PUT /api/v1/nis/preferences/me**
  - **Purpose:** Update the user's match preferences.
  - **Auth:** Required
  - **Body:** `{"age_min": 26}`
  - **Response:** `{"status": "UPDATED"}`

### Readiness
- **GET /api/v1/nis/readiness/home**
  - **Purpose:** Aggregate the completion status of all readiness phases.
  - **Auth:** Required
  - **Response:** `{"niyyah_complete": true, "values_complete": true, "mirror_complete": false, "portrait_complete": false, "demographics_complete": true, "is_fully_ready": false}`

### Niyyah
- **GET /api/v1/nis/niyyah/me**
  - **Purpose:** Retrieve the user's Niyyah intention.
  - **Auth:** Required
  - **Response:** `{"intention_text": "...", "is_complete": true}`
- **PUT /api/v1/nis/niyyah/me**
  - **Purpose:** Save the user's Niyyah intention.
  - **Auth:** Required
  - **Body:** `{"intention_text": "..."}`

### Values
- **GET /api/v1/nis/values/me**
  - **Purpose:** Retrieve the user's Values data.
  - **Auth:** Required
  - **Response:** `{"values_data": {...}, "is_complete": true}`
- **PUT /api/v1/nis/values/me**
  - **Purpose:** Save the user's Values data.
  - **Auth:** Required
  - **Body:** `{"values_data": {...}}`

### Mirror
- **GET /api/v1/nis/mirror/me**
  - **Purpose:** Retrieve the user's private Mirror reflections.
  - **Auth:** Required
  - **Response:** `{"reflection_data": {...}, "is_complete": true}`
  - **Privacy:** Must remain private-only. Must not be exposed to candidates.
- **PUT /api/v1/nis/mirror/me**
  - **Purpose:** Save the user's private Mirror reflections.
  - **Auth:** Required
  - **Body:** `{"reflection_data": {...}}`

### Portrait
- **GET /api/v1/nis/portrait/me**
  - **Purpose:** Retrieve the user's derived Portrait data.
  - **Auth:** Required
  - **Response:** `{"portrait_data": {...}, "is_complete": true}`
  - **Privacy:** Must remain user-only. Must not be exposed to matches.
- **PUT /api/v1/nis/portrait/me**
  - **Purpose:** Save the user's Portrait data.
  - **Auth:** Required
  - **Body:** `{"portrait_data": {...}}`

### Considered Few
- **GET /api/v1/nis/considered-few**
  - **Purpose:** Retrieve the curated list of candidates considered highly compatible.
  - **Auth:** Required
  - **Response:** `{"status": "FOUND", "candidates": [...]}`
  - **Privacy:** Frontend must not try to recalculate or second-guess this list.

### Candidate / Interest
- **GET /api/v1/nis/candidates/{candidate_id}**
  - **Purpose:** Retrieve minimal safe profile details of a candidate.
  - **Auth:** Required
  - **Response:** `{"candidate_id": "...", "display_name": "...", "shared_strengths": [...]}`
  - **Privacy:** Must NOT expose raw private signals, raw Raya/Barakah data, compatibility percentages, or photos before gated stages.
- **POST /api/v1/nis/candidates/{candidate_id}/interest**
  - **Purpose:** Express private interest in a candidate.
  - **Auth:** Required
  - **Response:** `{"status": "INTEREST_RECORDED"}`
- **POST /api/v1/nis/candidates/{candidate_id}/pass**
  - **Purpose:** Pass on a candidate privately.
  - **Auth:** Required
  - **Response:** `{"status": "PASS_RECORDED"}`

### Matchflow
- **GET /api/v1/nis/matchflows/{matchflow_id}**
  - **Purpose:** Get the current state and step of a matchflow.
  - **Auth:** Required
  - **Response:** `{"matchflow_id": "mf_123", "current_step": "MUTUAL_INTEREST", "steps": [...]}`
- **POST /api/v1/nis/matchflows/{matchflow_id}/decision**
  - **Purpose:** Submit a user's decision (e.g., PROCEED, PAUSE, CLOSE).
  - **Auth:** Required
  - **Body:** `{"outcome": "PROCEED"}`
  - **Response:** `{"status": "DECISION_RECORDED", "outcome": "PROCEED"}`
  - **Privacy:** Must not pressure the user and must not allow Raya to recommend an outcome.

### Conversation
- **GET /api/v1/nis/conversations/{conversation_id}**
  - **Purpose:** Load the conversation topics and allowed messages.
  - **Auth:** Required
  - **Response:** `{"current_topic": "PARENTS_AND_FAMILY", "topics": [...], "messages": []}`
- **POST /api/v1/nis/conversations/{conversation_id}/messages**
  - **Purpose:** Post a message to the current topic.
  - **Auth:** Required
  - **Body:** `{"topic": "PARENTS_AND_FAMILY", "content": "Hello."}`
  - **Response:** `{"accepted": true, "contact_leak_detected": false}`

### Reports / Safety
- **POST /api/v1/nis/reports**
  - **Purpose:** Submit a safety report against a user.
  - **Auth:** Required
  - **Body:** `{"reported_user_id": "user_xyz", "flag_type": "AGGRESSIVE_LANGUAGE", "severity": "LOW"}`
  - **Response:** `{"report_id": "rep_123", "safety_flag_created": true, "human_review_required": false}`
  - **Privacy:** Reporter identity is explicitly scrubbed.

### Admin / Human Review
- **GET /api/v1/nis/admin/reviews**
  - **Purpose:** List reviews pending admin decision.
  - **Auth:** Required (Admin level pending)
  - **Response:** `[{"review_id": "rev_1", "user_id": "user_bad"}]`
- **POST /api/v1/nis/admin/reviews/{review_id}/decision**
  - **Purpose:** Submit a moderation decision.
  - **Auth:** Required (Admin level pending)
  - **Body:** `{"decision": "PERMANENT_BAN"}`
  - **Response:** `{"status": "RESOLVED", "decision": "PERMANENT_BAN"}`

---

## 12. Development Only

### Practical Proof Demo Verification
- **GET /api/v1/nis/dev/proof-report**
  - **Purpose:** Returns a practical, deterministic proof report showing exactly which candidates pass or fail the NIS pipeline, and why. Used for stakeholder demos.
  - **Auth:** Disabled/Blocked outside of `development` environment. Production requests return 403 Forbidden.
  - **Response:**
    ```json
    {
      "current_user": "demo_user_ayman",
      "nis_passed": true,
      "results": [
        {
          "candidate_id": "demo_candidate_strong",
          "expected": "SHOWN",
          "actual": "SHOWN",
          "reason": "Passed all checks."
        }
      ]
    }
    ```
  - **Privacy:** No private raw data, selfies, Aadhaar info, compatibility percentages, or Barakah text is ever exposed. No Firebase logic is used.
