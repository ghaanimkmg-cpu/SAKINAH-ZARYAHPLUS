# Sakinah + NIS Final Report

## 1. What I Created
I created the full **Sakinah** matchmaking journey inside ZaryahPlus, along with its powerful backend brain called **NIS** (NEXUS Intelligence System).

**Sakinah** is the user-facing matchmaking journey. It guides users through an intentional process of defining their intentions (Niyyah), their values, and their private self-reflections (Mirror/Portrait) before they ever see a candidate.

**NIS** is the backend intelligence and safety layer behind it. It persists all profiles, readiness states, and matchflow data in a PostgreSQL database using SQLAlchemy. It enforces production authentication. It runs a KYC/Liveness sandbox adapter for secure identity verification. And it provides a transparent NIS proof report to demonstrate its decision-making.

## 2. What NIS Is
NIS stands for **NEXUS Intelligence System**.

NIS is the backend intelligence layer that decides whether a candidate is safe and suitable enough to be shown.

It is **not** a swipe system.
It is **not** random matching.
It is **not** a compatibility percentage system.
It is **not** a public scoring system.
It does **not** recommend marriage.

NIS is designed to prefer:
**No match**
over
**a wrong match.**

## 3. Why NIS Was Created
NIS was created because Sakinah should not behave like a dating app.

The system needs to protect users from:
- fake abundance
- random candidates
- unsafe profiles
- emotionally risky pairings
- weak compatibility
- unverified users
- photo-first decisions
- casual chat behavior

NIS was built to make Sakinah **character-first**, **safety-first**, and **backend-authoritative**.

## 4. How NIS Was Created
The build journey followed a strict, logic-first path:
- Foundation rules were defined first.
- Hard filters were created.
- Psychological pair dynamics were added.
- Confidence/no-match threshold was added.
- Considered-few generation was created.
- Privacy rules were enforced.
- Database persistence was added.
- Demographic/KYC-derived profile storage was added.
- Auth enforcement was added.
- KYC/liveness sandbox adapter was added.
- A proof report was created to demonstrate NIS behavior.

## 5. What NIS Checks Before Showing a Candidate

| NIS Layer | What It Checks | Why It Matters |
| --- | --- | --- |
| Eligibility / verification state | Is the user ID-verified and eligible? | Unverified users get blocked. |
| Demographics | Age, gender, location rules. | Age mismatch gets blocked. |
| Preferences | Non-negotiable dealbreakers. | Opposing dealbreakers get blocked. |
| Hard filters | Strict boundary rules. | Severe incompatibilities get blocked. |
| Psychological pair dynamics | Do their personalities create a healthy dynamic? | Angry + angry / weak repair pattern gets blocked. |
| Dangerous pair combinations | High risk emotional pairings. | Emotionally unstable pairings get blocked. |
| Confidence threshold | Is there enough data to make a safe match? | Insufficient data gets blocked. |
| Safety/report status | Has the user been flagged or banned? | Banned user gets blocked. |
| No-match rule | If nobody is suitable. | If nobody is suitable, NIS returns "no suitable matches right now". |
| Privacy protection | Ensures reflection data is never shared. | Protects user vulnerability. |

## 6. NIS Psychological Pair Dynamics
NIS does not match people only because they are similar.
It checks whether two personalities create calm, responsibility, repair, and long-term suitability.

**Dangerous combinations (Blocked):**
- high anger + high anger
- high conflict + weak repair
- emotionally unstable + emotionally unstable
- avoidant + emotionally needy
- weak boundaries + strong family pressure
- financial irresponsibility + financial irresponsibility
- not ready + not ready

**Healthy complementarity (Approved):**
- calm + expressive but repair-oriented
- structured + flexible
- emotionally steady + emotionally open
- financially careful + financially balanced

## 7. How NIS Can Be Proven
The human-readable proof page is available at:
`/sakinah/dev/proof-report`

The proof report gives NIS controlled demo candidates:
- **Strong Candidate** → shown
- **Banned Candidate** → blocked
- **Angry / weak repair candidate** → blocked
- **Age mismatch candidate** → blocked
- **Weak candidate** → blocked
- **Insufficient data candidate** → blocked

This proves NIS is not randomly displaying people. The backend is making the decision, and the frontend only displays the backend-approved result.

## 8. Technologies Used
- React + TypeScript
- Vite
- FastAPI
- SQLAlchemy
- Alembic
- Pytest
- PyJWT generic auth adapter
- Local development scripts
- No Firebase currently implemented

Firebase/Firestore can be added later by future developers if Omar confirms that architecture and provides credentials.

## 9. Frontend Pages Explained

| Route | Page Purpose | What Frontend Does | Backend/API Used | Storage | Status |
| --- | --- | --- | --- | --- | --- |
| `/sakinah` | Landing Page | Explains intentionality | None | None | Complete |
| `/sakinah/role` | Select Role | Chooses candidate or guardian | None | Local | Complete |
| `/sakinah/primer` | Introduction | Explains strict rules | None | Local | Complete |
| `/sakinah/kyc` | Identity Verification | Triggers vendor sandbox | `/api/v1/nis/kyc/*` | DB via API | Sandbox Complete |
| `/sakinah/liveness` | Face Match | Triggers liveness sandbox | `/api/v1/nis/liveness/*` | DB via API | Sandbox Complete |
| `/sakinah/home` | Readiness Dashboard | Shows preparation progress | `/api/v1/nis/readiness/home` | DB via API | Complete |
| `/sakinah/niyyah` | Intentions | Captures intentions | `/api/v1/nis/niyyah/me` | DB via API | Complete |
| `/sakinah/values` | Values Assessment | Captures core values | `/api/v1/nis/values/me` | DB via API | Complete |
| `/sakinah/mirror` | Self-Reflection | Captures private reflection | `/api/v1/nis/mirror/me` | DB via API | Complete |
| `/sakinah/portrait` | Final Self-Summary | Captures personal portrait | `/api/v1/nis/portrait/me` | DB via API | Complete |
| `/sakinah/preferences` | Match Criteria | Sets hard dealbreakers | `/api/v1/nis/preferences/me` | DB via API | Complete |
| `/sakinah/considered-few` | Candidate Pool | Displays approved candidates | `/api/v1/nis/considered-few` | DB via API | Complete |
| `/sakinah/candidate/:id` | Candidate Detail | Shows specific candidate | `/api/v1/nis/candidates/{id}` | DB via API | Complete |
| `/sakinah/matchflow/:id` | Active Match | Manages matching state | `/api/v1/nis/matchflows/{id}` | DB via API | Complete |
| `/sakinah/conversation/:id` | Structured Chat | Facilitates guided chat | `/api/v1/nis/conversations/{id}` | DB via API | Complete |
| `/sakinah/decision/:id` | Outcome | Handles proceed/pause/close | `/api/v1/nis/matchflows/{id}/decision` | DB via API | Complete |
| `/sakinah/safety` | Reporting | Files a safety report | `/api/v1/nis/reports` | DB via API | Complete |
| `/sakinah/community` | Guardian Network | Guardian support interface | Mock API | Local | Complete |
| `/sakinah/vent` | Emotional Support | Support outlet | Mock API | Local | Complete |
| `/sakinah/dev/proof-report` | NIS Proof | Runs live demo scenarios | `/api/v1/nis/dev/proof-report` | DB via API | Complete |

## 10. Backend/API Explained

| Backend Area | What It Does | Storage | Status |
| --- | --- | --- | --- |
| Auth | Enforces JWT security | DB | Complete |
| Profile | Manages demographic signals | DB | Complete |
| Preferences | Manages match criteria | DB | Complete |
| Demographics | Manages verified age/gender | DB | Complete |
| Niyyah | Saves user intentions | DB | Complete |
| Values | Saves core values | DB | Complete |
| Mirror | Saves private reflection | DB | Complete |
| Portrait | Saves personal portrait | DB | Complete |
| Considered Few | Generates the safe match pool | DB | Complete |
| Candidate Actions | Records pass/interest signals | DB | Complete |
| Matchflow | Runs the state machine | DB | Complete |
| Conversation | Saves chat messages | DB | Complete |
| Decision | Processes final match outcomes | DB | Complete |
| Safety Reports | Captures user flags | DB | Complete |
| Human Review/Admin | Flags users for admin review | DB | Complete |
| KYC | Integrates ID verification vendor | DB | Sandbox Complete |
| Liveness | Integrates face-match vendor | DB | Sandbox Complete |
| NIS Proof Report | Runs the engine for demo | None | Complete |

## 11. Database / Storage Explanation
- SQLAlchemy models were created.
- Alembic migrations were added.
- Profile, preferences, demographics, readiness, matchflow, conversation, safety, and human review are database-backed.
- The dev proof endpoint uses controlled demo fixtures only.
- Raw Aadhaar, raw government ID, and raw selfie are **not** stored.
- KYC/liveness stores only safe minimal fields (verified name, age, gender).

## 12. Why Some Pages Are Still Sandbox / Preview
KYC and Liveness cannot be fully production-live without real vendor credentials.

**Reasons:**
- Government ID verification needs an external vendor.
- Liveness / face-match needs an external vendor.
- Production API keys are not available yet.
- Real identity data must not be used in development.
- The app must not fake verification.

**What is already done:**
- Adapter foundation created.
- Sandbox flow works.
- Backend controls verification state.
- Weak liveness goes to human review.
- Raw Aadhaar/selfie not stored.

## 13. What Is Fully Working Now
- Frontend full journey
- Backend APIs
- Database persistence
- Auth enforcement
- NIS matching logic
- NIS proof page
- Readiness pages backend-backed
- Considered-few DB-backed
- Safety/human review flow
- KYC/liveness sandbox foundation
- Production build passes
- Backend tests pass

## 14. What Is Not Yet Final Production
- Real KYC/liveness vendor credentials
- Live vendor SDK/API wiring
- Firebase Admin token validation if Omar requires Firebase
- Production deployment environment
- Production users
- Push notifications if required

## 15. Final Status
- **Demo-ready: Yes** (Fully runnable on `localhost` with mocked data/vendor endpoints).
- **Staging-ready: Yes** (Ready for a live test environment to review frontend UX).
- **Production-ready: Not yet** (Requires live vendor credentials and actual production integrations).

## 16. What Future Developers Should Do Next
1. Add real KYC/liveness vendor credentials.
2. Replace sandbox adapter with real vendor API implementation.
3. Decide Firebase/Firestore vs current SQLAlchemy/PostgreSQL direction.
4. If Firebase is required, add Firebase Admin token verification.
5. Deploy to staging.
6. Run UAT.
7. Security review.
8. Then production deployment.

## 17. Rules Developers Must Not Break
- no swipe
- no feed
- no public profiles
- no photo-first matching
- no compatibility percentage
- no spiritual score
- no rejection notification
- no intimacy before nikah
- Raya never decides marriage outcome
- frontend never decides matches
- raw identity data never exposed
- no fake abundance
- no random candidate padding
