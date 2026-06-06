# Developer Handover Checklist

This document is a formal handover checklist for developers continuing work on the Sakinah module and the broader ZaryahPlus NIS platform.

## 1. Local Development Environment
- [x] **Startup Script:** Use `start-dev.bat` to boot the application. The script will boot both the backend and frontend, and automatically open `http://localhost:5173/sakinah` in your browser.
- [x] **Frontend URL:** `http://localhost:5173/sakinah`
- [x] **Backend Health Check:** Verify the backend is running at `http://127.0.0.1:8000/health`.
- [x] **Proxy Configuration:** Vite proxy automatically forwards `/api` and `/health` requests to the local backend.
- [x] **Local Dev Fallbacks:** When the backend is unreachable or a production database is missing, the frontend will automatically switch to **Development Preview Mode** and display `DevFallbackBadge`s. Do not pretend this behavior is production.

## 2. Source Control Boundaries
- [x] **No Firebase Rule:** The project does strictly NOT use Firebase. Do not introduce Firebase libraries or dependencies.
- [x] **Excluded Files:** **Do not commit** the following:
  - `node_modules/`
  - `venv/`
  - `.env` files containing actual secrets
  - Hardcoded secrets
  - `logs/`
  - Temporary or scratch scripts

## 3. Sakinah Reference Journey Routes
The frontend implements the full premium dark-gold parity reference flow. The completed route progression is:
1. `/sakinah` (Entry)
2. `/sakinah/role`
3. `/sakinah/primer`
4. `/sakinah/kyc`
5. `/sakinah/liveness`
6. `/sakinah/home`
7. `/sakinah/niyyah`
8. `/sakinah/values`
9. `/sakinah/mirror`
10. `/sakinah/portrait`
11. `/sakinah/preferences`
12. `/sakinah/considered-few`
13. `/sakinah/candidate/:id`
14. `/sakinah/matchflow/:id`
15. `/sakinah/conversation/:id`
16. `/sakinah/decision/:id`

**Optional Support Routes:**
- `/sakinah/safety`
- `/sakinah/community`
- `/sakinah/vent`

## 4. Production Pending (Next Steps)
The following features are stubbed or mocked in the current parity build and must be wired up securely before a production launch:
- [ ] **Production JWT / User Mapping:** Connect the real user identity system to NIS. Currently, endpoints use hardcoded 'mock_target' or similar IDs.
- [ ] **PostgreSQL Live DB Wiring:** Transition the SQLite/in-memory stubs or missing columns to the live production schema on PostgreSQL.
- [ ] **Real KYC / Liveness Vendor:** Integrate the actual third-party vendor (e.g., Onfido, SumSub) for KYC and liveness checks to replace the visual placeholder screens.
- [ ] **Admin Role Enforcement:** Ensure that NIS backend routes fully enforce admin-only constraints where required via JWT scopes.
