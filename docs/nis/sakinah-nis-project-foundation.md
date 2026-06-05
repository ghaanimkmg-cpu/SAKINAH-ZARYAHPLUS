# Sakinah + NEXUS Intelligence System (NIS) Project Foundation

## 1. Definitions
- **Sakinah**: The user-facing matchmaking experience, built within the existing ZaryahPlus React/TypeScript frontend (`frontend/src/features/sakinah/`).
- **NEXUS Intelligence System (NIS)**: The backend intelligence system powering Sakinah, handling all logic, checks, and sensitive decisions.

## 2. Final Architecture
- **Frontend**: Existing ZaryahPlus React app.
- **Backend**: Python + FastAPI.
- **Database**: PostgreSQL.
- **Relationship**: Users interact with Sakinah, which makes API calls to the NIS backend. NIS serves as the absolute authority on all matchmaking decisions.

## 3. Strict Rules & Constraints
- **FastAPI + PostgreSQL Direction**: The backend must use FastAPI and PostgreSQL.
- **No Firebase Rule**: Firebase (Auth, Firestore, Admin SDK, Rules) is strictly prohibited for the new Sakinah/NIS system.
- **No Paid AI APIs Rule**: OpenAI, Claude, or any paid AI keys must not be used for v1.
- **Raya Scripted Rule**: Raya will be scripted/template-based for v1.
- **Visual Source of Truth**: The HTML file acts as the visual source of truth, dictating UI patterns (premium dark/gold design, Raya orb, Stepper, Rounded Cards). It must not resemble a generic dashboard or typical dating app.
- **Server-Authoritative Rule**: The frontend must never decide matchmaking outcomes. NIS decides eligibility, verification, safety, hard filter passes, compatibility, mutual interest, conversation unlocking, and human review flags.
- **No-Match Principle**: The system must prefer to return "NO_SUITABLE_MATCHES_RIGHT_NOW" over a weak or careless match. Certainty and safety are prioritized over volume.

## 4. Full Phase List
Phase 0: Project Foundation & Codebase Analysis
Phase 1: Sakinah Frontend Foundation
Phase 2: Sakinah Frontend Shared Components
Phase 3: Sakinah Frontend Core Pages
Phase 4: Sakinah Frontend Matchmaking Pages
Phase 5: Sakinah Frontend Flow Pages and Routing
Phase 6: FastAPI Backend Skeleton
Phase 7: PostgreSQL Setup, SQLAlchemy, and Alembic
Phase 8: Core NIS Database Models
Phase 9: Authentication / User Context Placeholder
Phase 10: KYC Sandbox and Eligibility Gate
Phase 11: User Signal Profile and Match Preferences
Phase 12: Hard Filter Engine
Phase 13: Rule-Based Compatibility Engine
Phase 14: Confidence Thresholds and No-Match Rule
Phase 15: Considered Few Generator
Phase 16: Scripted Raya Explanation Service
Phase 17: Mutual Interest and Silent Pass Gate
Phase 18: Matchflow State Machine
Phase 19: Structured Conversation Engine
Phase 20: Safety Flags, Reports, and Human Review
Phase 21: API Contract Finalization
Phase 22: Frontend + Backend Integration
Phase 23: Full End-to-End Testing
Phase 24: Deployment Readiness
Phase 25: Advanced NIS Upgrade Plan

## 5. Strict Execution Protocol
- **One Phase at a Time**: The project must be executed strictly phase-by-phase.
- **Stop After Each Phase**: After completing a phase, testing it, and documenting it, execution must halt to wait for explicit user approval before proceeding to the next phase.
