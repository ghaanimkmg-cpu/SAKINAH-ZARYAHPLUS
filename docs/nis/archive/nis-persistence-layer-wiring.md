# NIS Persistence Layer Wiring

As part of Phase K, the in-memory `_mock_` dictionaries across the NIS backend have been replaced with SQLAlchemy Database Operations.

## Summary of Changes

1. **New Schema Creation**: Added `NISNiyyahIntention`, `NISValuesProfile`, `NISMirrorReflection`, and `NISPrivatePortrait` to complete the missing signal area tables for Sakinah.
2. **Migrations**: `alembic revision --autogenerate` generated the migration for these tables and UUID corrections.
3. **Services DB Refactoring**:
   - `NISMatchPreferenceService`
   - `NISUserSignalProfileService`
   - `NISSafetyService`
   - `NISHumanReviewService`
   - `NISStructuredConversationService`
   - `NISMatchflowService`
   - `NISMutualInterestService`
4. **API Controller DI**: The `db: Session = Depends(get_db)` has been injected into all corresponding routes.

## Remaining Gaps / Next Steps
- `Safety` and `HumanReview` services now save to the Database, but their identity banning mechanism needs deeper integration into an authentication middleware.
- Full UUID mapping for system-generated mock users needs to be handled cautiously, as SQLAlchemy strictly validates UUID strings.
- **Architectural Difference Note**: Omar's Build Brief mentions using Firebase Auth and Firestore for data persistence. However, this implementation utilizes a FastAPI + SQLAlchemy/PostgreSQL stack. If Omar confirms that Firebase/Firestore is the final desired infrastructure, future developers will need to swap out the SQLAlchemy repository layer for Firestore collections, as the current DB models are strictly SQL-based.

## Skipped Test Recovery Plan (COMPLETED)
The previously skipped tests (`test_matchflow.py`, `test_mutual_interest.py`, `test_safety_human_review.py`, `test_structured_conversation.py`) have been fully rewritten in Phase K.1 to use the in-memory SQLite `db: Session` fixture instead of legacy dictionaries. All critical business logic pathways are now proven against the database layer.

## Demographic/KYC Persistence Gap (RESOLVED in Phase K.2)
- The `/api/v1/nis/considered-few` endpoint now fully uses the database for `NISDemographicProfile`.
- The static demographic defaults (like `age=25`) have been completely removed.
- Candidates lacking demographic data are correctly blocked from the matching pool.
- The `test_nis_demographics_gap.py` xfail test has been converted into full passing tests verifying this logic.
