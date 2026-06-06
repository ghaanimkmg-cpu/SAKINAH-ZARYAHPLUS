# Sakinah Considered Few Card UI Fix

## Issue Found
On `/sakinah/considered-few`, the candidates in the pool were rendering as plain, unstyled stacked text. The beautiful premium dark-gold cards with the interactive hover effect from the reference UI were completely missing. Similarly, the full `cand-card` layout on the Candidate screen was missing its premium styling.

## Root Cause
During the migration of the dev reference UI to React components in Phase E, several critical CSS classes for the matching flow were accidentally omitted from `sakinah.css`. Specifically, `.sk-pool-card`, `.pool-aura`, `.sk-active-banner`, and the entire `.sk-cand-card` suite of classes were never added to the stylesheet, causing the `className` bindings in `ConsideredFewList.tsx` and `CandidatePortraitCard.tsx` to fail silently and render as plain text.

## Files Changed
- `frontend/src/features/sakinah/styles/sakinah.css`: Added all missing CSS classes from the dev reference:
  - `.sk-pool-card` and `.pool-aura` for the Considered Few list rows.
  - `.sk-active-banner` for the pool intro text.
  - `.sk-cand-card`, `.cand-aura`, `.cand-name`, `.cand-meta`, `.sk-resonance`, and `.sk-no-face` for the candidate portrait screen.

## Desktop / Mobile Verification
- **Desktop (1440px, 1280px, 1024px):** Candidates now render as distinct, premium dark-gold bordered cards inside the `max-w-[800px]` central column. Hovering shifts the cards gently to the right with a gold border highlight, exactly matching the reference. The layout feels like a premium desktop web application without feeling cramped.
- **Mobile (430px, 390px):** Cards cleanly stack one per row, consuming the full available width with excellent touch targets. No horizontal overflow occurs.

## Product Rules Preserved
- No swipe UI or feed algorithms were introduced.
- Candidates remain curated and bounded.
- The "no face" and private signaling text remains explicitly stated.
- No public photo grid is visible.
