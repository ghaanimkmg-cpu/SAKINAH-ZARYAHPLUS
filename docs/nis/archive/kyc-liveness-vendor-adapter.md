# Sakinah KYC & Liveness Vendor Adapter

## Overview
This document outlines the foundation for integrating a real-world KYC and Liveness vendor (e.g., Onfido, SumSub) into the Sakinah NIS system, specifically matching Omar's requirements.

## Omar's KYC Requirements
- **Verification:** Users must verify their identity using a valid Government ID (Aadhaar, Passport, PAN, Voter ID).
- **Liveness:** A real-time selfie check must confirm the user is a live person.
- **Face Match:** The selfie must be algorithmically matched against the photo on the provided Government ID.

## Data Minimization & Privacy (Strict Rules)
To comply with the NIS architecture's extreme privacy stance:
1. **No Raw Aadhaar/ID Storage:** The backend NEVER stores raw document numbers or document images in the primary database.
2. **No Raw Selfie Storage:** The backend NEVER stores the user's liveness selfie.
3. **Restricted Fields:** The only fields persisted to `NISDemographicProfile` upon successful verification are:
   - `verified_identity_name`
   - `verified_age`
   - `verified_gender`
   - `is_kyc_verified`
4. **Candidate Privacy:** Verified ID details are for systemic trust and safety routing only. They are **never** exposed to candidates/matches.

## Development Sandbox Mode
Currently, the system uses a `SandboxKycVendorAdapter` when `APP_ENV=development`.
- The frontend calls `/sandbox/complete` endpoints to mock vendor success.
- This allows full pipeline testing without collecting real PII or burning real vendor credits.

## Production Pending Behavior
In production (`APP_ENV=production`), if `KYC_PROVIDER_API_KEY` is missing:
- Endpoints return `VENDOR_NOT_CONFIGURED`.
- The frontend will gracefully block the user with a pending badge, preventing unverified access to the considered few pipeline.
- The sandbox endpoints strictly throw an error in production, preventing bypassing.

## Human Review for Weak Matches
If the vendor returns a weak score for either liveness or face-match (e.g., `< 0.8` or `"WEAK"` status), the system does NOT auto-reject the user.
Instead, it flags the verification as `PENDING_REVIEW` and sets `human_review_required = True`, routing it to the NIS admin dashboard for manual inspection.

## Future Developers: Connecting the Real Vendor
1. Inside `backend/app/nis/services/kyc_vendor_adapter.py`, replace the stub logic in the production branches.
2. Call the real vendor's SDK via REST or their Python client.
3. Keep the webhook endpoints mapped to `process_callback` patterns.
4. Add vendor API keys to the `.env` production config.
