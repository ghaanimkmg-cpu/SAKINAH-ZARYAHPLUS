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
- The `ConsideredFew` service still uses mock data generation for demo purposes, as requested.
- `Safety` and `HumanReview` services now save to the Database, but their identity banning mechanism needs deeper integration into an authentication middleware.
- Full UUID mapping for system-generated mock users needs to be handled cautiously, as SQLAlchemy strictly validates UUID strings.
