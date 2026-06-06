# Sakinah Development Preview Audit

## Overview
This document catalogs every route in the Sakinah pipeline that is currently running in **Development Preview Mode**, utilizing mock data, or pending backend/vendor integration. It identifies the production gaps that must be resolved before the feature is fully liveable.

## 1. Routes and Current Status

### Static / No Backend Required
These pages are static onboarding or purely informative. They are considered production-ready as they require no dynamic persistence.
- `/sakinah`
- `/sakinah/role`
- `/sakinah/primer`
- `/sakinah/community`

### Development Proof (Intentional)
- `/sakinah/dev/proof-report`
  - **Why preview exists:** Designed purely for internal QA of the NIS algorithm.
  - **Required Action:** Ensure this is strictly restricted in production environments via 403 blocks.

### Pending External Vendors
- `/sakinah/kyc`
  - **Preview Badge:** "Production KYC vendor pending. Safe sandbox mode."
  - **Missing:** Integration with the official third-party KYC provider.
- `/sakinah/liveness`
  - **Preview Badge:** "Production Liveness vendor pending. No real selfie collected."
  - **Missing:** Integration with the official third-party biometric liveness provider.

### Pending Database Persistence APIs
These routes are purely frontend placeholders. Their data is not saved to the backend yet.
- `/sakinah/home`
  - **Preview Badge:** "Development Preview Mode: No backend aggregation connected yet."
  - **Missing:** Dashboard aggregation API to pull matches, status, and pending actions.
- `/sakinah/niyyah`
  - **Preview Badge:** "Development Preview Mode: Persistence API pending."
  - **Missing:** Backend API to store Niyyah text and DB schema.
- `/sakinah/values`
  - **Preview Badge:** "Development Preview Mode: Persistence API pending."
  - **Missing:** Backend API to store Islamic value alignments.
- `/sakinah/mirror`
  - **Preview Badge:** "Development Preview Mode: Mirror API pending. No answers stored."
  - **Missing:** Backend API to store deep self-reflection answers.
- `/sakinah/portrait`
  - **Preview Badge:** "Development Preview Mode: Portrait API pending."
  - **Missing:** Backend API to store structured profile traits.
- `/sakinah/vent`
  - **Preview Badge:** "Development Preview Mode: Private frontend-only journaling."
  - **Missing:** If intended for cloud sync, a secure private journaling API. Otherwise, remains local.

### Backend-Backed (But Dependent on Fallbacks/Mocks)
These routes have functioning backend endpoints (`/api/v1/nis/...`) but currently rely on mock candidate data, test headers (`X-Test-User-Id`), or local fallback logic if the API fails.
- `/sakinah/eligibility`
  - **Current State:** API connected, uses `DevFallbackBadge` if offline.
- `/sakinah/profile`
  - **Current State:** API connected, uses `DevFallbackBadge` if offline.
- `/sakinah/preferences`
  - **Current State:** API connected, uses `DevFallbackBadge` if offline.
- `/sakinah/considered-few`
  - **Preview Badge:** "Development Preview Mode: Backend offline, using safe mock candidates."
  - **Current State:** API connected, but the backend itself generates hardcoded demo pool (`demo_user_ayman` logic).
- `/sakinah/candidate/:candidateId`
  - **Current State:** API connected. Frontend uses `mockCandidates` import to resolve candidate details if the backend fails.
- `/sakinah/matchflow/:matchflowId`
  - **Preview Badge:** "Development Preview Mode: Backend unreachable. Proceeding with CONVERSATION_OPEN state."
  - **Current State:** Has hardcoded routing logic (`navigate('/sakinah/conversation/mock_conversation_1')`).
- `/sakinah/conversation/:conversationId`
  - **Current State:** Hardcoded parameters (`sendConversationMessage('mock', ...)` and `navigate('/sakinah/decision/mock_matchflow_1')`).
- `/sakinah/decision/:matchflowId`
  - **Current State:** Hardcoded parameters (`submitDecision('mock', ...)`).
- `/sakinah/safety`
  - **Preview Badge:** "Development Preview Mode: Backend unreachable. Report mock processed securely."
  - **Current State:** Has hardcoded target logic (`submitReport('mock_target', ...)`).

## 2. Global Production Blockers

### A. Real Database Persistence
The entire NIS backend engine is currently operating using in-memory `mock_repositories`. No user profiles, preferences, candidate pools, or matchflows are saved to a PostgreSQL database.
- **Action:** Convert all mock repositories in the backend to SQLAlchemy repositories linked to the real `users`, `user_preferences`, and `matchflows` tables.

### B. JWT Authentication & Security
The frontend `sakinahApi.ts` injects a hardcoded `X-Test-User-Id: user_frontend_dev` header to bypass authentication.
- **Action:** Remove the test header injection and enforce standard JWT Bearer token authentication for all Sakinah API routes.

## 3. Recommended Next Build Phases

To safely transition Sakinah from Development Preview to Full Production, the following phases are recommended in order:

1. **Phase: Persistence Layer**
   - Design and apply SQLAlchemy models and migrations for NIS matching data.
   - Replace Python backend mock repositories with real DB CRUD operations.
2. **Phase: Complete Missing APIs**
   - Build backend endpoints for Niyyah, Values, Mirror, and Portrait.
   - Connect these to the frontend and remove "Persistence API pending" badges.
3. **Phase: Auth & Integrity Enforcement**
   - Replace `X-Test-User-Id` with strict JWT decoding.
   - Strip out all `mockCandidates` imports and fallback `mock_target` IDs from the React frontend.
   - Convert `DevFallbackBadge` into strict blocking error boundaries.
4. **Phase: External Integration**
   - Integrate the official real-world KYC and Liveness vendors.
5. **Phase: Aggregation & Polish**
   - Implement the `SakinahHomePage` dashboard backend logic to serve live matchflow states.
   - Remove all final `DevFallbackBadge` instances across the application.
