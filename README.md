# ZaryahPlus Sakinah + NEXUS Intelligence System

Sakinah is the user-facing matchmaking feature inside ZaryahPlus.
NEXUS Intelligence System, NIS, is the backend intelligence system that powers eligibility, KYC, compatibility, match control, safety, and structured conversation.

## Architecture
- Existing ZaryahPlus React frontend
- Sakinah module inside `frontend/src/features/sakinah/`
- NIS backend using FastAPI
- PostgreSQL database
- SQLAlchemy + Alembic
- No Firebase for new Sakinah/NIS system

## Implemented Modules
- Sakinah frontend foundation
- Sakinah shared components
- Sakinah pages and routes
- FastAPI backend skeleton
- PostgreSQL + Alembic setup
- Core NIS database models
- Auth/user context placeholder
- KYC sandbox and eligibility gate
- User signal profile and preferences APIs
- Hard filter engine
- Rule-based compatibility engine
- Confidence thresholds and no-match rule
- Considered few generator
- Scripted Raya explanation service
- Mutual interest and silent pass gate
- Matchflow state machine
- Structured conversation engine
- Safety reports and human review
- API contract
- Frontend-backend integration
- Full test report

## Product Principles
- No swipe
- No infinite feed
- No public profile browsing
- No rejection notifications
- No who-liked-you
- No photos before approved gated stage
- No weak matches
- No fake abundance
- Prefer no match over wrong match
- Raya guides only and never decides
- Backend/NIS is server-authoritative

## Local Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
npm run build
```

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload
```

## Branch Note
This work is currently on `feature/sakinah-nis-full-build` and should not be merged to main without review.

## Status
Work in progress / deployment-ready review branch.