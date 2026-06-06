# Sakinah NIS Deployment Readiness

This document outlines the deployment readiness state of the ZaryahPlus Sakinah + NEXUS Intelligence System (NIS) backend and frontend components.

## 1. Environment Variables

> [!CAUTION]
> Ensure all variables are correctly populated before deploying. Never check secrets into source control.

**Backend (`.env`)**
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+psycopg://user:password@host/db`)
- `ENVIRONMENT`: `development`, `staging`, or `production`
- `CORS_ORIGINS`: Comma-separated list of allowed frontend origins

## 2. Backend Setup
1. Use Python 3.10+
2. Install dependencies: `pip install -r requirements.txt`
3. Start the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 3. Frontend Setup
1. Install dependencies: `npm install`
2. Configure `VITE_API_URL` to point to the backend domain.
3. Build for production: `npm run build`
4. Serve the `dist/` directory via Nginx/CDN.

## 4. PostgreSQL Setup & Alembic Migrations
- Ensure a PostgreSQL 14+ instance is running.
- Execute migrations against the production database: `alembic upgrade head`
- Ensure the database user has schema creation privileges during initial deployment.

## 5. Build and Testing Commands

**Frontend**
```bash
cd frontend
npm run build
```

**Backend**
```bash
cd backend
python -m pytest
```

## 6. Pre-Deployment Checklist

- [ ] Execute `pytest` ensuring 100% pass rate.
- [ ] Run `npm run build` and ensure no TypeScript errors exist.
- [ ] Ensure database backups are scheduled.
- [ ] Verify `CORS_ORIGINS` strictly matches the production domain.
- [ ] **Auth / JWT Verification Pending Note:** Ensure the development-only `X-Test-User-Id` header is removed, and a robust JWT decoding dependency replaces `get_current_user`.
- [ ] **Admin Role Enforcement Pending Note:** The admin route protection currently utilizes standard auth. It MUST be swapped to require an explicit `is_admin_user` dependency.
- [ ] **KYC Production Vendor Pending Note:** The KYC system currently uses a stub mechanism. A production vendor integration (e.g., Veriff/Onfido) must be attached to the callback mechanism.

## 7. Architectural Rules

> [!IMPORTANT]
> **No Firebase Rule:** Sakinah and NIS explicitly ban the usage of Firebase Realtime Database, Firestore, and standard Firebase client listeners. All data flows exclusively through standard REST endpoints in the FastAPI backend to ensure algorithmic integrity.

## 8. Rollback Notes
- If an Alembic migration introduces instability: `alembic downgrade -1`
- Always take a database snapshot prior to `alembic upgrade head`.

## 9. Remaining Risks Before Production
1. **Auth Context:** Real tokens need to be configured.
2. **Production Vendor Integration:** Webhooks from the KYC provider need to correctly target the callback route.
3. **Database Scale:** The caching mechanism for candidate generation might need optimization under heavy load (currently relies on basic database queries).
