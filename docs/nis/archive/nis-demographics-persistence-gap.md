# NIS Demographics Persistence Gap

## Overview
During Phase K, the psychological core (`UserSignalProfile` and `MatchPreference`) was successfully wired to the SQLAlchemy persistence layer. However, demographic data is currently handled by static defaults.

## Why Demographic Data is Required by HardFilterEngine
The `NISHardFilterEngine` is the gatekeeper of the matching system. It strictly enforces non-negotiable criteria before the psychological `NISCompatibilityEngine` runs. It requires a `FilterCandidateState` object, which depends on real demographic information to execute critical blocking rules (e.g. age mismatch, tradition incompatibility).

## Missing Fields
Currently, the following demographic and identity fields are missing from the persistence layer and are being hardcoded in `/api/v1/nis/considered-few`:
- `age`
- `gender`
- `location`
- `relocation_openness`
- `tradition`
- `marital_status`
- `wali`
- `timeline`

## Proposed Model
A new model, likely `NISDemographicProfile` or derived from the central KYC table, needs to be implemented.
**Required Schema fields:**
- `user_id` (UUID, Foreign Key)
- `age` (Integer)
- `gender` (Enum)
- `location` (String)
- `relocation_open` (Boolean/Enum)
- `tradition` (String/Enum)
- `marital_status` (Enum)
- `wali_preference` (Enum)
- `nikah_timeline` (Enum)
- `verified_identity_name` (String, from KYC)
- `verified_age` (Integer, from KYC)
- `verified_gender` (String/Enum, from KYC)

## Data Sources
1. **KYC Verification:** `verified_identity_name`, `verified_age`, `verified_gender` must be exclusively sourced and sealed by the vendor KYC process, not user input.
2. **User Preference/Intake:** `location`, `relocation_open`, `tradition`, `marital_status`, `wali_preference`, and `nikah_timeline` will be captured during the onboarding flow.

## Privacy Rules
The demographics pipeline must adhere to strict privacy rules:
- **Never expose raw Aadhaar**: Government ID numbers must never be saved in plaintext or transmitted to the frontend.
- **Never expose government ID documents**: Scanned document images remain in isolated secure storage.
- **Never expose selfie biometrics**: Liveness checks are for internal verification only.
- **Identity data is system-only**: `verified_identity_name` and exact age validation are strictly for internal trust systems and hard filters, not for display on public profiles unless explicitly governed by the product rules.

## Status Update (Phase K.2)
The `NISDemographicProfile` model has now been implemented. Static defaults (`age=25`, `location="Unknown"`, etc.) have been completely removed from the `NISConsideredFewService` production logic. The `FilterCandidateState` is now hydrated from real database values.

However, the external KYC vendor integration (Phase L) is still pending. The `verified_identity_name`, `verified_age`, and `verified_gender` fields exist in the database schema but are not yet populated by a real third-party service. Raw Aadhaar and liveness integrations remain pending for Phase L.
