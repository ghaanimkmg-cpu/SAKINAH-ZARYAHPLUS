# Sakinah Dev Reference Pixel-Quality Parity Audit

This document tracks the UI and product flow parity between the source of truth (`sakinah-dev-reference.html`) and the current React implementation in `frontend/src/features/sakinah/`.

*Note: A foundation/theming commit has already occurred to align base fonts, global colors, and shared components (Commit `d696b38 feat: Phase 1 Sakinah Foundation and Theming parity`). The following audit reflects the state after Phase 1.*

## Parity Gap Analysis

| Reference screen | Current React route | Status | Gap | Required action |
|---|---|---|---|---|
| 1. Raya welcome | `/sakinah` (`SakinahEntryPage`) | Partially matched | Needs full styling parity with the breathing orb and fade-in UI. | Needs visual upgrade |
| 2. Role selection | `/sakinah/eligibility` (`SakinahEligibilityPage`) | Partially matched | Currently a basic form. Needs to be the Seeker vs Wali fork. | Needs visual upgrade |
| 3. Before we begin / expectation primer | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 4. KYC verification | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 5. Liveness verification | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 6. Sakinah home / journey overview | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 7. Niyyah / intention | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 8. Values / maslak | `/sakinah/profile` (`SakinahProfileSignalsPage`) | Partially matched | Exists as a basic form but does not match the comfort spectrum / design. | Needs visual upgrade |
| 9. Mirror reflections | `/sakinah/preferences` (`SakinahPreferencesPage`) | Partially matched | Exists as a form but misses the 9-dimension gratitude mechanic. | Needs visual upgrade |
| 10. Private portrait | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 11. Considered few | `/sakinah/pool` (`SakinahConsideredFewPage`) | Partially matched | List exists but lacks the staggered card animations and empty state. | Needs visual upgrade |
| 12. Candidate resonance | `/sakinah/candidate/:id` (`SakinahCandidatePage`) | Partially matched | Exists but lacks the "Character first" resonance dot animations. | Needs visual upgrade |
| 13. Matchflow | `/sakinah/matchflow/:id` (`SakinahMatchflowPage`) | Partially matched | Stage rail and structured opening UI exists but needs design polish. | Needs visual upgrade |
| 14. Structured conversation | `/sakinah/conversation/:id` (`SakinahConversationPage`) | Partially matched | Exists but lacks the 8-topic progressive unlock polish and timer notes. | Needs visual upgrade |
| 15. Decision | `/sakinah/decision/:id` (`SakinahDecisionPage`) | Partially matched | Exists but requires exit cards and visual parity. | Needs visual upgrade |
| 16. Safety | `/sakinah/safety` (`SakinahSafetyPage`) | Partially matched | Exists but needs the watermark/lock UI and visual parity. | Needs visual upgrade |
| 17. Community | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |
| 18. Vent Box / support | *None* | Missing | Does not exist in React flow. | Build missing screen and wire into flow |

## Global Overlays
- **Raya Floating FAB & Bottom Sheet:** Missing. The global presence of Raya at the bottom right corner does not exist in the React shell. Needs to be implemented globally across the Sakinah flow.
