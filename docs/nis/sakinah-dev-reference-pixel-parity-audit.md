# Sakinah Dev Reference Pixel-Quality Parity Audit

This document tracks the UI and product flow parity between the source of truth (`sakinah-dev-reference.html`) and the current React implementation in `frontend/src/features/sakinah/`. It also establishes the full-stack backend alignment to ensure the React frontend remains a thin UI layer over the authoritative NIS backend.

*Note: A foundation/theming commit has already occurred to align base fonts, global colors, and shared components (Commit `d696b38 feat: Phase 1 Sakinah Foundation and Theming parity`). The following audit reflects the state after Phase 1.*

## Parity Gap & Full-Stack Analysis

| Reference screen | Current React route | Frontend status | Backend/API status | Data stored? | Gap | Required action |
|---|---|---|---|---|---|---|
| 1. Raya welcome | `/sakinah` | Partially matched | Frontend-only acceptable | No | Needs full styling parity with the breathing orb and fade-in UI. | Needs visual upgrade |
| 2. Role selection | `/sakinah/eligibility` | Partially matched | Frontend-only acceptable | Session-only (Seeker vs Wali). If role must persist later, new API needed. | Currently a basic form. Needs to be the Seeker vs Wali fork. | Needs visual upgrade |
| 3. Before we begin / primer | *None* | Missing | Frontend-only acceptable | No | Does not exist in React flow. | Build missing screen and wire into flow |
| 4. KYC verification | *None* | Missing | Existing API available / Production vendor pending | Yes (via vendor) | Does not exist in React flow. | Build missing screen and wire into flow |
| 5. Liveness verification | *None* | Missing | Development preview only / Production vendor pending | Yes (via vendor) | Does not exist in React flow. | Build missing screen and wire into flow |
| 6. Sakinah home | *None* | Missing | Existing API available | Aggregated | Does not exist in React flow. May need aggregation API later. | Build missing screen and wire into flow |
| 7. Niyyah / intention | *None* | Missing | New API needed | Yes (Derived/Profile) | Does not exist in React flow. Must map safely into profile signals. | Build missing screen and wire into flow |
| 8. Values / maslak | `/sakinah/profile` | Partially matched | New API needed | Yes (Derived/Profile) | Exists as a basic form but does not match the comfort spectrum / design. Must map safely into profile/preferences. | Needs visual upgrade |
| 9. Mirror reflections | `/sakinah/preferences`| Partially matched | New API needed | Yes (Derived/Private signals only. No raw public exposure) | Exists as a form but misses the 9-dimension gratitude mechanic. | Needs visual upgrade |
| 10. Private portrait | *None* | Missing | New API needed | Derived from profile/mirror. User-only. | Does not exist in React flow. | Build missing screen and wire into flow |
| 11. Considered few | `/sakinah/pool` | Partially matched | Existing API available | Yes | List exists but lacks the staggered card animations and empty state. | Needs visual upgrade |
| 12. Candidate resonance | `/sakinah/candidate/:id`| Partially matched | Existing API available | Candidate detail | Exists but lacks the "Character first" resonance dot animations. May need richer backend-safe explanation fields later. | Needs visual upgrade |
| 13. Matchflow | `/sakinah/matchflow/:id`| Partially matched | Existing API available | State machine | Stage rail and structured opening UI exists but needs design polish. | Needs visual upgrade |
| 14. Structured conversation| `/sakinah/conversation/:id`| Partially matched| Existing API available | Yes | Exists but lacks the 8-topic progressive unlock polish and timer notes. | Needs visual upgrade |
| 15. Decision | `/sakinah/decision/:id`| Partially matched | Existing API available | State machine | Exists but requires exit cards and visual parity. | Needs visual upgrade |
| 16. Safety | `/sakinah/safety` | Partially matched | Existing API available | Reports | Exists but needs the watermark/lock UI and visual parity. | Needs visual upgrade |
| 17. Community | *None* | Missing | New API needed | Optional | Does not exist in React flow. New API needed only if interactive. Must not feed matching in v1. | Build missing screen and wire into flow |
| 18. Vent Box / support | *None* | Missing | New API needed | Private | Does not exist in React flow. New API needed only if interactive. Must remain private and must not feed matching in v1. | Build missing screen and wire into flow |
| Global Raya FAB / bottom sheet | *None* | Missing | Frontend UI acceptable | N/A | Does not exist in the React shell. Any personalized guidance must use scripted Raya service or safe backend source later. | Build missing component and wire into global layout |

## Full-Stack Integration Rules
1. If an existing backend API already supports a screen, the React page must use it.
2. If backend support is missing, do not fake it silently.
3. Missing backend support must be documented as a gap.
4. If required for the current flow, create minimal safe backend routes/services/schemas in the correct future phase.
5. Backend/NIS remains server-authoritative.
6. Frontend remains display/action layer only.
7. Development preview fallback is allowed only for local demo and must be clearly marked.
8. Development preview must not pretend to be production.

## Rules for Future Backend Additions
If a future phase needs new backend APIs, they must:
- use FastAPI
- live under `backend/app/api/v1/nis/`
- use schemas under `backend/app/nis/schemas/`
- use services under `backend/app/nis/services/`
- include tests
- update `docs/nis/nis-api-contract.md`
- update relevant handover docs
- run backend pytest
- avoid Firebase

New backend work must NOT:
- use raw Raya conversations
- use raw Barakah Lab entries
- create worship score
- create gratitude score
- create compatibility percentage
- recommend marriage
- claim perfect match
- expose private data
- expose raw government ID
- expose raw selfie
- expose raw Aadhaar
- create public spiritual ranking

## Frontend Boundaries
Frontend must NOT:
- calculate compatibility
- decide real eligibility
- decide KYC success for production
- create real matchflow for production
- unlock real chat for production
- store sensitive private signals locally as source of truth
- show compatibility percentage
- show rejection notifications
- show who-liked-you
- expose raw private data
- pretend dev preview data is production data

## Before Each Future Phase
Before building each future phase, Antigravity must report whether the phase is:
- frontend-only
- frontend + existing API
- frontend + new backend API needed
- development-preview only
- production vendor pending

If the phase requires new backend APIs, Antigravity must pause and clearly state:
- what API is needed
- why it is needed
- what data it stores
- what privacy constraints apply
- what tests will be added
