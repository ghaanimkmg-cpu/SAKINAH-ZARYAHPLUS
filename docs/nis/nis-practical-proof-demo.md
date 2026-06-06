# NIS Practical Proof & Demo Suite

## 1. What NIS Is
The **Network Intelligence System (NIS)** is the strictly server-authoritative matchmaking engine of Sakinah. It is a deterministic, highly secure pipeline built in Python/FastAPI that filters, evaluates, and curates candidates based on hard filters, safety risks, and deep psychological pair dynamics. It does not guess, it does not use simple "similarity scoring," and it operates entirely independent of the frontend.

## 2. What NIS Is Not
- NIS is **not** a traditional matching algorithm calculating arbitrary "compatibility percentages."
- NIS does **not** rely on Firebase, Firestore, or client-side evaluation.
- NIS does **not** use buzzwords like "soulmate" or "perfect match."
- NIS does **not** just match people who answer questions identically (e.g., angry + angry is blocked, not matched).

## 3. How to Prove NIS is Working
We have built a deterministic proof suite that operates independently of the frontend UI. By feeding 6 specific, controlled candidates through the pipeline, we can mathematically prove that the backend respects all business, safety, and psychological rules before returning candidates to the client.

## 4. Demo Candidates and Expected Outcomes
We use a mock user, `demo_user_ayman`, to evaluate 6 test candidates:

1. **`demo_candidate_strong`**
   - **Expected:** `SHOWN`
   - **Reason:** Passes all age, safety, and psychological checks. Exhibits healthy complementarity.
2. **`demo_candidate_banned`**
   - **Expected:** `BLOCKED`
   - **Reason:** Blocked by safety/ban rules. Identity banned.
3. **`demo_candidate_angry`**
   - **Expected:** `BLOCKED`
   - **Reason:** Blocked by psychological dynamics (high anger + weak repair patterns).
4. **`demo_candidate_age_mismatch`**
   - **Expected:** `BLOCKED`
   - **Reason:** Fails hard filters (age is outside user's preferences).
5. **`demo_candidate_weak`**
   - **Expected:** `BLOCKED`
   - **Reason:** Fails due to weak compatibility (avoidant, unready, volatile).
6. **`demo_candidate_insufficient`**
   - **Expected:** `BLOCKED`
   - **Reason:** Important core profile data is missing.

## 5. How to Run Backend Tests
Developers can cryptographically verify the algorithm by running the pytest suite:
```bash
cd backend
python -m pytest app/nis/tests/test_nis_demo_proof.py
```
This runs 12 specific assertions ensuring the route works, fails safely in production, exposes no private fields, and blocks all 5 unsafe candidates.

## 6. How to Call the Proof Endpoint
We have exposed a special, development-only API endpoint to retrieve the proof report in real-time.
- **Endpoint:** `GET /api/v1/nis/dev/proof-report`
- **Note:** This endpoint will return `403 Forbidden` if the server is run in `APP_ENV=production`.

## 7. How to Explain Results to Omar
When demonstrating this to Omar, emphasize that:
1. The frontend has absolutely no power. The UI only renders what the backend explicitly permits.
2. The backend proves its intelligence by intentionally filtering out the 5 bad candidates, returning only the single high-confidence match.
3. We are protecting user privacy by stripping out percentages, PII, and medical language entirely.

## 8. What is Currently Engine-Verified
- Hard filter exclusion (Age, location, etc.).
- Safety block exclusion (Banned/under-review users).
- Psychological dynamic filtering (Blocking dangerous combinations).
- Privacy protection (Stripping raw inputs before leaving the server).

## 9. What is Staging-Ready
- The frontend UI flow `/sakinah/considered-few` correctly ingests the API and gracefully handles both "candidates found" and "no suitable matches" states.
- The pipeline architecture in `NISConsideredFewService`.

## 10. What is Still Pending Before Live Launch
- The current `demo_candidate` lists inside the services are hardcoded for testing/proving the algorithm. Before live launch, these lists must be replaced with dynamic SQLAlchemy ORM queries against the PostgreSQL database.
- Raya preview text is currently a static placeholder and needs to be hooked up to the real `RayaScriptService`.

---

## Demo Script for Omar

**Step 1:** Run the backend and frontend. (Using `npm run dev` and `start.bat` or your local equivalents).
**Step 2:** Open backend health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) to prove the server is running.
**Step 3:** Open the human-readable proof report UI on the frontend: [http://localhost:5173/sakinah/dev/proof-report](http://localhost:5173/sakinah/dev/proof-report).
(Do NOT show the raw JSON `/api/v1/nis/dev/proof-report` to Omar as it is not easily readable).
**Step 4:** Show Omar the premium UI. Point out that the status is `PASSED`, and walk through the candidates. Show that out of 6 candidates, only `Strong Candidate` was allowed through. The others were systematically blocked by the backend pipeline for age, anger, bans, or weak compatibility. Read out the human-friendly reasons.
**Step 5:** Navigate to the Considered Few page: [http://localhost:5173/sakinah](http://localhost:5173/sakinah) -> Considered Few.
**Step 6:** Explain that the frontend only displays what the backend approved. The frontend is making no decisions, ensuring absolute safety and backend authority.
