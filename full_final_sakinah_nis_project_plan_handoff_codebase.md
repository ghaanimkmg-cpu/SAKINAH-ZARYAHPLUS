# ZaryahPlus Sakinah + NEXUS Intelligence System (NIS)
## FULL FINAL PROJECT EXECUTION PLAN FOR ANTIGRAVITY

**Project:** ZaryahPlus  
**New Feature:** Sakinah Matchmaking  
**Backend Intelligence System:** NEXUS Intelligence System (NIS)  
**Frontend:** React / TypeScript inside existing ZaryahPlus app  
**Backend:** Python + FastAPI  
**Database:** PostgreSQL  
**Execution Tool:** Antigravity / VS Code Agent  
**Execution Style:** Strict phase-by-phase execution only  
**Visual Source of Truth:** `sakinah-dev-reference (1)(1).html`  
**Seriousness Level:** Production-grade, safety-first, no careless matching  

---

# CRITICAL CODEBASE RULE — MUST FOLLOW

This project must be performed inside the provided handoff codebase folder:

```text
sakinah-handoff/
```

Do not create a separate standalone app.

Do not create a new React project.

Do not create a new frontend outside the existing codebase.

The existing ZaryahPlus frontend inside the handoff folder must be used.

The Sakinah frontend must be created inside the same existing frontend structure:

```text
frontend/src/features/sakinah/
```

The backend must also be added inside the same handoff workspace, preferably as:

```text
backend/
```

or another clearly named backend folder if the existing codebase already has a backend convention.

The final result must be one integrated project folder where:

```text
Existing ZaryahPlus frontend
+ new Sakinah frontend module
+ new NIS FastAPI backend
+ PostgreSQL integration
```

work together.

Antigravity must first inspect the handoff codebase structure before creating files.

Antigravity must preserve the existing frontend architecture, routing style, design system, and shared components.

Antigravity must not break existing features.

Antigravity must not touch unrelated features unless routing/navigation integration requires it.

If routing/navigation files must be modified, Antigravity must explain exactly what was changed and why.

---


# 0. ABSOLUTE EXECUTION RULE — READ FIRST

Antigravity must execute this project **one phase at a time only**.

Antigravity must **never** build the whole project in one attempt.

For every phase:

1. Complete only the current phase.
2. Do not begin the next phase automatically.
3. Run all relevant tests/checks for the current phase.
4. Explain clearly:
   - what was created
   - what was modified
   - what was tested
   - what passed
   - what failed, if anything
   - what is pending
   - what assumptions were made
   - what risks remain
5. Stop after the explanation.
6. Ask the user for permission before moving to the next phase.

At the end of every phase, Antigravity must write:

```text
Phase completed and tested. I am stopping here. Please confirm if I should proceed to the next phase.
```

If any test fails, Antigravity must not proceed. It must explain the failure and wait for instruction.

---

# 1. What We Are Building

We are building a serious matchmaking feature inside ZaryahPlus.

There are two connected systems:

```text
Sakinah = user-facing matchmaking experience
NEXUS Intelligence System (NIS) = backend intelligence system powering Sakinah
```

Users interact with Sakinah.

Sakinah calls NIS APIs.

NIS controls all serious decisions.

NIS decides:

- whether a user is eligible
- whether KYC is verified
- whether a user is safe
- whether a candidate passes hard filters
- whether compatibility is strong enough
- whether a candidate can be shown
- whether mutual interest exists
- whether conversation can open
- which conversation topics are unlocked
- whether human review is required
- whether a user should be banned or blocked

The frontend must never decide these things.

---

# 2. Final Architecture

```text
ZaryahPlus Existing Frontend
React + TypeScript
│
└── frontend/src/features/sakinah/
    ├── Sakinah UI screens
    ├── Sakinah components
    ├── Sakinah frontend services
    ├── API calls to NIS backend
    └── Visual design from HTML reference
        ↓
NEXUS Intelligence System Backend
Python + FastAPI
        ↓
PostgreSQL Database
        ↓
KYC Sandbox / Matching / Safety / Human Review
```

---

# 3. Final Technical Direction

Use:

```text
Frontend: Existing ZaryahPlus React app
Frontend feature location: frontend/src/features/sakinah/
Backend: Python + FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Migrations: Alembic
Testing: Pytest + frontend tests/checks
API Style: REST
KYC: Sandbox vendor first
AI: No paid AI APIs for v1
Raya: Scripted/template-based for v1
Matching: Server-authoritative NIS logic
```

---

# 4. Firebase Removal Rule

Firebase has been removed from the new Sakinah/NIS build plan.

Do not use:

```text
Firebase
Firestore
Firebase Auth
Firebase Admin SDK
Firebase config
Firestore collections
Firebase security rules
```

If the handoff codebase still contains old Firebase files, do not extend them for this new Sakinah/NIS system.

Use the existing frontend structure only.

The new backend must be:

```text
FastAPI + PostgreSQL
```

---

# 5. Visual Source of Truth

The Sakinah frontend must follow:

```text
sakinah-dev-reference (1)(1).html
```

This HTML file is the visual source of truth.

Antigravity must open and study the HTML file before building frontend screens.

The React implementation does not need to copy the HTML line-for-line, but it must recreate the same:

- premium dark/gold mood
- Raya orb / Raya presence
- character-first flow
- mobile-like focused journey
- calm transitions
- rounded cards
- gold accents
- considered few screen
- candidate portrait screen
- matchflow stepper
- structured conversation topic curriculum
- decision screen
- safety screen

The frontend must not look like a generic dashboard.

It must not look like a dating app.

---

# 6. Non-Negotiable Product Rules

The system must never:

1. Act like a dating app.
2. Create swipe behavior.
3. Create infinite feed behavior.
4. Create public profile browsing.
5. Show photos before the approved gated stage.
6. Send rejection notifications.
7. Show “who liked you.”
8. Fake match abundance.
9. Lower standards to fill the pool.
10. Show weak matches.
11. Expose raw Raya conversations.
12. Expose raw Barakah Lab entries.
13. Turn gratitude, worship, or community into public scores.
14. Let Raya decide marriage outcomes.
15. Let Raya recommend marriage.
16. Claim perfect compatibility.
17. Claim divine certainty.
18. Bypass safety checks.
19. Let the frontend write sensitive matchmaking data.
20. Let the frontend decide who is shown.
21. Open chat before mutual interest.
22. Show intimacy/closeness topic before nikah.
23. Store raw Aadhaar or raw government ID numbers.
24. Use real PII during development.
25. Use paid AI APIs for v1.
26. Use Firebase for the new Sakinah/NIS system.

---

# 7. NIS v1 Boundary

For v1:

```text
Raya is scripted/template-based.
No OpenAI, Claude, or paid AI keys are used.
NIS uses structured answers, preferences, KYC state, hard filters, rule-based compatibility, safety checks, and confidence thresholds.
Advanced AI-based user understanding is reserved for a later approved upgrade.
```

Do not implement advanced AI in v1.

Do not directly use Barakah Lab data in matching for v1 unless leadership explicitly approves it.

---

# 8. No-Match Principle

NIS must prefer:

```text
NO_SUITABLE_MATCHES_RIGHT_NOW
```

over a weak or careless match.

No match is not a failure.

It is part of the seriousness and safety of the system.

Suggested user-facing message:

```text
We do not have someone suitable enough to show right now.
We would rather wait than show the wrong person.
```

---

# 9. Complete Phase List

Execute in this order only:

```text
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
```

---

# PHASE 0 — PROJECT FOUNDATION & CODEBASE ANALYSIS

## Goal

Understand the handoff codebase, the HTML reference, and the final architecture before creating code.

This phase is analysis + documentation only.

## Tasks

1. Open the provided `sakinah-handoff/` codebase folder in VS Code / Antigravity. All work must happen inside this same handoff codebase.
2. Inspect the existing frontend structure.
3. Locate:
   - frontend source path
   - router file
   - navigation files
   - API helper pattern
   - shared components
   - theme/design files
   - auth/protected route pattern
4. Open and study:

```text
sakinah-dev-reference (1)(1).html
```

5. Identify HTML visual patterns to recreate.
6. Create the project foundation document.

## Create File

```text
docs/nis/sakinah-nis-project-foundation.md
```

## Required Document Content

The document must define:

- Sakinah as the user-facing matchmaking feature
- NIS as the backend intelligence system
- FastAPI + PostgreSQL architecture
- no Firebase rule
- no paid AI API rule for v1
- Raya scripted/template-based rule for v1
- frontend visual source of truth
- backend-authoritative rule
- no-match principle
- full phase execution plan
- stop-after-each-phase rule

## Testing / Verification

Verify:

- foundation file exists
- HTML reference exists and was reviewed
- frontend paths were identified
- backend location decision is documented
- no Firebase rule is documented
- phase-by-phase rule is documented

## Report Required

After Phase 0, report:

1. Frontend root path found.
2. Router file found.
3. Navigation file found.
4. API helper pattern found.
5. Design/theme system found.
6. HTML reference reviewed.
7. Foundation file created.
8. Any risks or missing details.

## Stop Rule

Stop after Phase 0 and ask permission before Phase 1.

---

# PHASE 1 — SAKINAH FRONTEND FOUNDATION

## Goal

Create the Sakinah frontend module foundation inside the existing handoff frontend codebase. Do not create a separate React app.

Do not build all screens yet.

## Create Structure

```text
frontend/src/features/sakinah/
├── pages/
├── components/
├── hooks/
├── services/
├── types/
├── data/
├── styles/
└── index.ts
```

## Create Files

```text
frontend/src/features/sakinah/types/sakinah.types.ts
frontend/src/features/sakinah/data/mockSakinahData.ts
frontend/src/features/sakinah/styles/sakinahTheme.ts
frontend/src/features/sakinah/index.ts
```

## Required Types

Include types for:

- eligibility status
- candidate summary
- considered few response
- matchflow step
- conversation topic
- decision outcome
- safety report payload
- user signal profile payload
- match preference payload

## Design Tokens

Create theme tokens based on the HTML reference:

```text
dark background
panel dark
gold
soft gold
dim gold
ink
dim ink
green
rose
blue
rounded radius
soft shadows
```

## Mock Data Rules

Mock data is temporary only.

Mock data must not include:

- real people
- real photos
- compatibility percentages
- raw psychological labels
- raw Raya data
- raw Barakah Lab data
- marriage recommendation

## Testing

Test:

- folder exists
- types compile
- mock data imports
- design tokens import
- no route is broken
- no backend logic added

## Stop Rule

Stop after Phase 1 and ask permission before Phase 2.

---

# PHASE 2 — SAKINAH FRONTEND SHARED COMPONENTS

## Goal

Create reusable Sakinah UI components based on the HTML reference.

## Components

Create:

```text
SakinahShell.tsx
SakinahHeader.tsx
RayaOrb.tsx
RayaScriptCard.tsx
CandidatePortraitCard.tsx
ConsideredFewList.tsx
MatchStrengthPill.tsx
InterestActionPanel.tsx
MatchflowStepper.tsx
ConversationTopicList.tsx
ConversationMessageList.tsx
DecisionPanel.tsx
SafetyNotice.tsx
EmptyMatchState.tsx
```

## Visual Requirements

Components must match the HTML reference feel:

- premium dark background
- gold borders
- serif titles
- mono-style labels
- soft cards
- aura circles
- Raya orb
- calm spacing
- no dating-app visuals

## Component Rules

Components must not:

- calculate compatibility
- decide eligibility
- unlock chat
- unlock topics
- show rejection
- show photos early
- show raw private signals

## Testing

Test:

- components compile
- components accept typed props
- components render with mock data
- no backend dependency
- no swipe UI
- no photo-first UI

## Stop Rule

Stop after Phase 2 and ask permission before Phase 3.

---

# PHASE 3 — SAKINAH FRONTEND CORE PAGES

## Goal

Build the core onboarding and setup pages.

## Pages

Create:

```text
SakinahEntryPage.tsx
SakinahEligibilityPage.tsx
SakinahProfileSignalsPage.tsx
SakinahPreferencesPage.tsx
```

## Requirements

### Entry Page

Must include:

- Raya welcome
- calm introduction
- serious marriage tone
- no dating language
- gold CTA
- HTML reference visual style

### Eligibility Page

Displays backend/mocked status:

```text
NOT_STARTED
PENDING
VERIFIED
HUMAN_REVIEW_REQUIRED
REJECTED
BANNED
```

Frontend must not decide eligibility.

### Profile Signals Page

Collect structured user inputs.

Do not show psychological scores.

### Preferences Page

Collect match preferences and hard-filter inputs.

Use gentle language.

## Testing

Test:

- pages compile
- forms render
- mock service works
- no sensitive data in localStorage
- no dating/swipe language
- visual style matches HTML reference

## Stop Rule

Stop after Phase 3 and ask permission before Phase 4.

---

# PHASE 4 — SAKINAH FRONTEND MATCHMAKING PAGES

## Goal

Build pages for considered few and candidate portrait.

## Pages

Create:

```text
SakinahConsideredFewPage.tsx
SakinahCandidatePage.tsx
```

## Considered Few Page

Must:

- show only backend/mock returned candidates
- show max 3 to 5 candidates
- show honest empty state
- no infinite scroll
- no swipe
- no public search
- no photo-first display

## Candidate Page

Must:

- show aura instead of photo
- show shared strengths
- show Raya preview
- show honest edge
- show interest and silent pass actions
- show note that photo is hidden before gated stage

Must not:

- show real photo
- show public profile
- show raw private data
- show compatibility percentage
- recommend marriage

## Testing

Test:

- considered few renders
- empty state works
- candidate page renders
- interest button calls service
- pass button calls service
- pass is not shown as rejection
- no photos
- no swipe/search/feed

## Stop Rule

Stop after Phase 4 and ask permission before Phase 5.

---

# PHASE 5 — SAKINAH FRONTEND FLOW PAGES AND ROUTING

## Goal

Build remaining Sakinah pages and connect routing/navigation.

## Pages

Create:

```text
SakinahMatchflowPage.tsx
SakinahConversationPage.tsx
SakinahDecisionPage.tsx
SakinahSafetyPage.tsx
```

## Routes

Add routes similar to:

```text
/sakinah
/sakinah/eligibility
/sakinah/profile
/sakinah/preferences
/sakinah/considered-few
/sakinah/candidate/:candidateId
/sakinah/matchflow/:matchflowId
/sakinah/conversation/:conversationId
/sakinah/decision/:matchflowId
/sakinah/safety
```

Follow existing router style.

## Navigation

Add navigation entry if required.

Do not break existing features.

## Page Rules

### Matchflow

Display backend-controlled steps only.

### Conversation

Show topics:

```text
Parents & Family
Work
Friends
Habits
Self-image
Responsibility
Expectations
Finances
```

No intimacy/closeness topic before nikah.

### Decision

Options:

```text
PROCEED
PAUSE
CLOSE
```

No pressure.

No Raya recommendation.

### Safety

Include reporting and safety explanation.

## Testing

Test:

- routes work
- navigation works
- pages render
- locked topics appear locked
- no intimacy topic
- no chat opens by frontend alone
- report UI calls service
- no unrelated features broken

## Stop Rule

Stop after Phase 5 and ask permission before Phase 6.

---

# PHASE 6 — FASTAPI BACKEND SKELETON

## Goal

Create backend skeleton for NIS.

## Suggested Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── errors.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── health.py
│   │       └── nis/
│   ├── nis/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── enums/
│   │   └── tests/
│   └── tests/
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## Dependencies

Use:

```text
fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary or asyncpg
pydantic
pydantic-settings
python-dotenv
pytest
httpx
```

## Health Endpoint

Create:

```text
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "NIS Backend",
  "version": "v1"
}
```

## Testing

Test:

- app starts
- health endpoint works
- config loads
- no Firebase dependency added

## Stop Rule

Stop after Phase 6 and ask permission before Phase 7.

---

# PHASE 7 — POSTGRESQL SETUP, SQLALCHEMY, AND ALEMBIC

## Goal

Set up PostgreSQL connection, SQLAlchemy base, and Alembic migrations.

## Tasks

1. Configure database session.
2. Configure Alembic.
3. Create base model mixins.
4. Confirm PostgreSQL connection.
5. Create test database setup if needed.

## Testing

Test:

- database connection works
- Alembic runs
- base model imports
- no Firebase dependency exists

## Stop Rule

Stop after Phase 7 and ask permission before Phase 8.

---

# PHASE 8 — CORE NIS DATABASE MODELS

## Goal

Create all core NIS models and migrations.

## Tables

Create:

```text
nis_users
nis_kyc_verifications
nis_match_preferences
nis_user_signal_profiles
nis_compatibility_evaluations
nis_considered_pools
nis_match_interests
nis_matchflows
nis_structured_conversations
nis_conversation_messages
nis_safety_flags
nis_reports
nis_human_reviews
nis_identity_bans
nis_audit_logs
```

## Sensitive Data Rules

KYC must never store:

```text
raw Aadhaar
raw government ID number
raw ID document
```

Signal profile must never store:

```text
raw Raya conversations
raw Barakah Lab entries
```

## Testing

Test:

- all models import
- migrations create tables
- sensitive prohibited fields do not exist
- relationships work
- enums are valid

## Stop Rule

Stop after Phase 8 and ask permission before Phase 9.

---

# PHASE 9 — AUTHENTICATION / USER CONTEXT PLACEHOLDER

## Goal

Create backend user-context handling for development and future production auth.

Firebase must not be used.

## Tasks

1. Create auth dependency placeholder.
2. Support development-mode test user context.
3. Protect sensitive endpoints.
4. Document production auth integration as pending if not provided.

## Rules

- no fake insecure production auth
- dev test user allowed only in dev mode
- protected endpoints require user context

## Testing

Test:

- protected endpoint rejects missing auth
- dev mode can inject test user
- non-dev mode does not allow test bypass
- user context includes user_id

## Stop Rule

Stop after Phase 9 and ask permission before Phase 10.

---

# PHASE 10 — KYC SANDBOX AND ELIGIBILITY GATE

## Goal

Build KYC sandbox integration and eligibility gate.

## Services

Create:

```text
NISKYCService
NISEligibilityService
```

## APIs

```text
POST /api/v1/nis/kyc/start
POST /api/v1/nis/kyc/callback
GET /api/v1/nis/eligibility/me
```

## KYC Rules

- sandbox vendor only in development
- no real PII in development
- store only name, age, gender, provider reference, identity hash, status
- never store raw Aadhaar
- never expose identity to matches
- low liveness/face-match confidence goes to human review
- low confidence is not automatic hard reject
- banned identity cannot return

## Testing

Test:

- unverified user not matchable
- sandbox verification marks verified
- minimal data stored
- raw ID not stored
- low confidence creates review
- banned identity blocks eligibility
- eligibility API returns safe status only

## Stop Rule

Stop after Phase 10 and ask permission before Phase 11.

---

# PHASE 11 — USER SIGNAL PROFILE AND MATCH PREFERENCES

## Goal

Create structured user data required for matching.

## APIs

```text
GET /api/v1/nis/profile/me
PUT /api/v1/nis/profile/me
GET /api/v1/nis/preferences/me
PUT /api/v1/nis/preferences/me
```

## Rules

- no raw Raya conversations
- no raw Barakah Lab entries
- no public scores
- no compatibility percentage
- backend validates everything

## Testing

Test:

- create/update profile
- create/update preferences
- invalid values rejected
- private fields not exposed
- raw prohibited text not stored
- only authenticated user updates own data

## Stop Rule

Stop after Phase 11 and ask permission before Phase 12.

---

# PHASE 12 — HARD FILTER ENGINE

## Goal

Build server-side hard filters.

## Filters

Implement:

- both users verified
- neither banned
- neither under review
- profile complete
- preferences complete
- age compatibility
- location/relocation compatibility
- nikah timeline compatibility
- tradition compatibility
- wali preference compatibility
- marital status compatibility
- blocked/reported relationship
- active conversation cap
- candidate not already active with user

## Testing

Test each filter.

Also test:

- failed hard filter never reaches compatibility engine
- failure does not notify candidate
- frontend cannot bypass filters

## Stop Rule

Stop after Phase 12 and ask permission before Phase 13.

---

# PHASE 13 — RULE-BASED COMPATIBILITY ENGINE

## Goal

Create explainable v1 compatibility engine.

No paid AI calls.

## Dimensions

Evaluate:

- values alignment
- emotional steadiness compatibility
- communication compatibility
- conflict repair compatibility
- family responsibility alignment
- deen/tradition expectation alignment
- marriage readiness
- financial expectation fit
- life direction fit
- wali/family compatibility
- lifestyle rhythm
- possible tension points

## Testing

Test:

- strong pair
- weak pair
- incompatible pair
- insufficient data
- manageable difference
- dangerous mismatch
- no output recommends marriage
- no raw private data exposed

## Stop Rule

Stop after Phase 13 and ask permission before Phase 14.

---

# PHASE 14 — CONFIDENCE THRESHOLDS AND NO-MATCH RULE

## Goal

Prevent weak matches from being shown.

## Final Statuses

```text
HIGH_CONFIDENCE_MATCH
MODERATE_CONFIDENCE_REVIEW
LOW_CONFIDENCE_DO_NOT_SHOW
INSUFFICIENT_DATA
HARD_REJECT
SAFETY_REJECT
NO_SUITABLE_MATCHES_RIGHT_NOW
```

Only `HIGH_CONFIDENCE_MATCH` can be shown automatically.

## Testing

Test:

- high confidence shown
- low confidence blocked
- insufficient data blocked
- hard reject blocked
- safety reject blocked
- no suitable matches returned
- threshold not lowered to fill pool

## Stop Rule

Stop after Phase 14 and ask permission before Phase 15.

---

# PHASE 15 — CONSIDERED FEW GENERATOR

## Goal

Generate small curated candidate pool.

## API

```text
GET /api/v1/nis/considered-few
```

## Rules

- show 3 to 5 candidates where possible
- show fewer if fewer are suitable
- show none if none qualify
- no swipe
- no feed
- no public search
- no photo-first display
- no who-liked-you
- no raw private signals
- no photos

## Testing

Test:

- only approved candidates returned
- max 5
- weak candidates excluded
- empty state works
- no photos
- no raw data
- auth required

## Stop Rule

Stop after Phase 15 and ask permission before Phase 16.

---

# PHASE 16 — SCRIPTED RAYA EXPLANATION SERVICE

## Goal

Create safe template-based Raya explanations.

No paid AI calls.

## Allowed Language

Raya may say:

- “You both seem to value...”
- “This may be worth exploring gently...”
- “Take your time.”
- “The decision remains yours.”

## Forbidden Language

Raya must never say:

- “You should marry this person.”
- “This is your perfect match.”
- “Allah chose this person for you.”
- “You are guaranteed to be compatible.”
- “You should proceed.”
- “Do not miss this chance.”

## Testing

Test:

- explanation generated from shared strengths
- tension note generated gently
- forbidden phrase blocked
- no marriage recommendation
- no raw data exposed
- safe fallback exists

## Stop Rule

Stop after Phase 16 and ask permission before Phase 17.

---

# PHASE 17 — MUTUAL INTEREST AND SILENT PASS GATE

## Goal

Build private interest and silent pass.

## APIs

```text
POST /api/v1/nis/candidates/{candidate_id}/interest
POST /api/v1/nis/candidates/{candidate_id}/pass
```

## Rules

- interest is private
- pass is silent
- no rejection notification
- no who-liked-you
- one-sided interest does not open chat
- mutual interest creates matchflow
- no blank chat box

## Testing

Test:

- interest stored privately
- pass stored privately
- pass does not notify candidate
- one-sided interest does not open chat
- mutual yes creates matchflow
- duplicate action handled safely

## Stop Rule

Stop after Phase 17 and ask permission before Phase 18.

---

# PHASE 18 — MATCHFLOW STATE MACHINE

## Goal

Create server-side matchflow state machine.

## Matchflow Steps

```text
PROFILES_COMPLETE
COMPATIBILITY_IDENTIFIED
MUTUAL_INTEREST
STRUCTURED_OPENING
WALI_INVITABLE
SUPERVISED_DEPTH
DECISION
```

## API

```text
GET /api/v1/nis/matchflows/{matchflow_id}
```

## Rules

- matchflow exists only after mutual yes
- frontend cannot create matchflow directly
- state transitions backend-controlled
- invalid transitions rejected
- audit important transitions

## Testing

Test:

- mutual yes creates matchflow
- invalid transition rejected
- frontend cannot force state
- current step returned safely
- no raw private data exposed

## Stop Rule

Stop after Phase 18 and ask permission before Phase 19.

---

# PHASE 19 — STRUCTURED CONVERSATION ENGINE

## Goal

Create guided topic-by-topic conversation.

## APIs

```text
GET /api/v1/nis/conversations/{conversation_id}
POST /api/v1/nis/conversations/{conversation_id}/messages
```

## Topics

```text
Parents & Family
Work
Friends
Habits
Self-image
Responsibility
Expectations
Finances
```

## Rules

- conversation starts only after mutual yes
- no blank free chat at beginning
- Raya frames first exchange
- topics unlock one by one
- wali can be present
- wali cannot decide for seeker
- contact info leakage detected
- intimacy/closeness locked until after nikah

## Testing

Test:

- chat blocked before mutual yes
- first topic opens after mutual yes
- topics unlock in order
- locked topic cannot be skipped
- intimacy topic blocked
- contact info detected
- wali present state works
- messages tied to topic

## Stop Rule

Stop after Phase 19 and ask permission before Phase 20.

---

# PHASE 20 — SAFETY FLAGS, REPORTS, AND HUMAN REVIEW

## Goal

Build safety and human review system.

## APIs

```text
POST /api/v1/nis/reports
GET /api/v1/nis/admin/reviews
POST /api/v1/nis/admin/reviews/{review_id}/decision
```

## Safety Flag Types

```text
CONTACT_LEAK_ATTEMPT
AGGRESSIVE_LANGUAGE
MANIPULATION_RISK
BOUNDARY_PRESSURE
SUSPICIOUS_IDENTITY
REPEATED_REPORTS
MASS_INTEREST_BEHAVIOR
OFF_PLATFORM_PRESSURE
PHOTO_LEAK_RISK
```

## Review Actions

```text
NO_ACTION
WARN_USER
LIMIT_ACCOUNT
PAUSE_MATCHMAKING
PERMANENT_BAN
ESCALATE_TO_SCHOLAR_COUNSELLOR
```

## Testing

Test:

- report creates record
- high severity creates review
- review decision stored
- banned user blocked
- identity ban checked
- safety reject prevents matching
- under-review user blocked
- contact leak creates flag

## Stop Rule

Stop after Phase 20 and ask permission before Phase 21.

---

# PHASE 21 — API CONTRACT FINALIZATION

## Goal

Finalize API contracts for frontend integration.

## Required API List

Document and verify:

```text
GET /api/v1/nis/eligibility/me
GET /api/v1/nis/profile/me
PUT /api/v1/nis/profile/me
GET /api/v1/nis/preferences/me
PUT /api/v1/nis/preferences/me
GET /api/v1/nis/considered-few
GET /api/v1/nis/candidates/{candidate_id}
POST /api/v1/nis/candidates/{candidate_id}/interest
POST /api/v1/nis/candidates/{candidate_id}/pass
GET /api/v1/nis/matchflows/{matchflow_id}
GET /api/v1/nis/conversations/{conversation_id}
POST /api/v1/nis/conversations/{conversation_id}/messages
POST /api/v1/nis/matchflows/{matchflow_id}/decision
POST /api/v1/nis/reports
```

## Create Documentation

Create:

```text
docs/nis/nis-api-contract.md
```

Include request/response examples.

## Testing

Test:

- OpenAPI docs load
- all endpoints listed
- sample responses match frontend types
- no raw private data in responses
- errors are consistent

## Stop Rule

Stop after Phase 21 and ask permission before Phase 22.

---

# PHASE 22 — FRONTEND + BACKEND INTEGRATION

## Goal

Connect the Sakinah frontend to the real NIS backend.

## Tasks

1. Review frontend service file.
2. Confirm endpoint names match.
3. Confirm response shapes match.
4. Replace mock calls with real NIS API calls.
5. Fix backend CORS if needed.
6. Ensure user context works in development.
7. Keep frontend decision-free.

## Rules

Do not move sensitive logic into frontend.

Do not create fake production candidates.

Do not rewrite UI unnecessarily.

## Testing

Test:

- frontend calls backend health
- frontend calls eligibility
- frontend loads considered few
- frontend submits interest/pass
- frontend loads matchflow
- frontend loads conversation
- frontend submits report
- errors display safely

## Stop Rule

Stop after Phase 22 and ask permission before Phase 23.

---

# PHASE 23 — FULL END-TO-END TESTING

## Goal

Run full project testing.

## Must-Pass Tests

1. unverified user cannot match
2. banned user cannot match
3. under-review user cannot match
4. hard filters block bad candidates
5. compatibility engine rejects weak pairs
6. confidence threshold blocks weak matches
7. no suitable matches state works
8. considered few max 5
9. no photos before gated stage
10. no rejection notification
11. chat blocked before mutual yes
12. topics unlock one by one
13. intimacy topic blocked before nikah
14. contact info leakage detected
15. report creates human review
16. Raya does not recommend outcome
17. frontend cannot bypass backend
18. no Firebase dependency exists
19. PostgreSQL migrations pass
20. FastAPI deployment config exists
21. frontend matches HTML visual reference
22. no raw private data appears in UI/API

## Create Test Report

Create:

```text
docs/nis/sakinah-nis-test-report.md
```

## Stop Rule

Stop after Phase 23 and ask permission before Phase 24.

---

# PHASE 24 — DEPLOYMENT READINESS

## Goal

Prepare system for deployment.

## Checklist

Verify:

- environment variables documented
- production secrets not committed
- PostgreSQL connection documented
- Alembic migrations ready
- CORS configured
- KYC sandbox/production switch documented
- logging configured
- error handling configured
- health endpoint ready
- OpenAPI docs ready
- rollback plan documented
- README updated
- no Firebase dependency exists
- frontend build works
- backend tests pass

## Create Deployment Docs

Create:

```text
docs/nis/sakinah-nis-deployment-readiness.md
```

## Stop Rule

Stop after Phase 24.

Do not deploy unless user explicitly gives permission.

---

# PHASE 25 — ADVANCED NIS UPGRADE PLAN

## Goal

Document the future path from NIS v1 to advanced NIS.

Do not implement advanced intelligence unless approved.

## Create File

```text
docs/nis/nis-advanced-upgrade-plan.md
```

## Future Possibilities

- deeper Raya-derived understanding
- long-term behavior patterns
- richer psychological profiles
- advanced compatibility modelling
- Barakah Lab-derived private character signals, only if approved
- improved human review intelligence
- learning from outcomes without exposing private data

## Conditions Before Advanced Upgrade

Do not implement until:

- v1 is stable
- safety is proven
- privacy is approved
- consent model is approved
- leadership approves Raya-derived signal usage
- leadership approves Barakah Lab signal usage
- no AI usage conflict exists
- legal/privacy review is complete

## Important Boundary

Barakah Lab must never become:

- public score
- spiritual ranking
- riya engine
- badge system
- popularity mechanism

If used later, it must only create private derived signals with consent.

## Stop Rule

Stop after Phase 25.

Do not implement advanced intelligence without leadership approval.

---

# FINAL REMINDER TO ANTIGRAVITY

Start with **Phase 0 only**.

Do not execute multiple phases.

Do not rush.

After each phase:

```text
complete → test → explain → stop → ask permission
```

This project is serious.

No shortcuts.

No fake matching.

No frontend-controlled decisions.

No weak matches.

No Firebase.

FastAPI + PostgreSQL only.

Sakinah must look like the HTML reference.

NIS must protect the seriousness of matchmaking.
