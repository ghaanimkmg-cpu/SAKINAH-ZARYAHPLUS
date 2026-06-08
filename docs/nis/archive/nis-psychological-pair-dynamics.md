# NIS Psychological Pair Dynamics

## Overview
NIS is explicitly not a simple similarity matcher. Similarity is not always compatibility (e.g. `angry + angry = dangerous`, not matched). The NIS Compatibility Engine evaluates serious psychological pair dynamics to determine healthy complementarity and detect dangerous opposition or compounding risks.

## Dimensions Evaluated
The engine evaluates 13 core dimensions:
1. Emotional regulation (`emotional_steadiness`)
2. Anger / conflict intensity (`anger_intensity`)
3. Conflict repair ability (`conflict_repair_style`)
4. Communication style (`communication_style`)
5. Attachment / space needs (`attachment_needs`)
6. Ego / humility (`ego_humility`)
7. Family responsibility (`family_responsibility`)
8. Financial responsibility (`financial_responsibility`)
9. Financial expectation (`financial_expectation`)
10. Marriage readiness (`marriage_readiness`)
11. Lifestyle rhythm (`social_lifestyle`)
12. Religious/value seriousness (`deen_alignment`)
13. Boundary respect (`boundary_respect`)

## Dangerous Pair Dynamics Detected
The engine actively blocks combinations that create unsafe environments or predictable failure loops.
Examples of detected risks:
- **Mutual High Anger:** High anger intensity + High anger intensity → "May create unsafe conflict pressure."
- **High Conflict + Low Repair:** High anger paired with avoidant/defensive repair styles → "High intensity combined with weak repair pattern."
- **Mutual Volatility:** Volatile + Volatile → "Mutual volatility may escalate safely."
- **Mutual Avoidance:** Avoidant + Avoidant attachment → "May lead to profound emotional disconnect."
- **Anxious-Avoidant Loop:** Emotionally needy (Anxious) + Emotionally unavailable (Avoidant) → "Anxious-avoidant loop risk."
- **Power Struggles:** Dominant + Dominant or Controlling + Avoidant → "Risk of unhealthy power dynamic."
- **Mutual Irresponsibility:** Financially irresponsible + Financially irresponsible → "Mutual financial carelessness poses severe stability risk."
- **Mutual Unreadiness:** Not-ready + Not-ready → "Neither party is ready for marital responsibilities."
- **Pressure vs Boundaries:** Weak boundaries + High family pressure → "Weak boundaries unable to handle high family pressure safely."

*When dangerous dynamics are found, the engine overrides any shared value alignment. The match is assigned `INCOMPATIBLE` or `REVIEW_REQUIRED` and the `NISConfidenceThresholdService` strictly blocks it from being shown.*

## Healthy Complementarity
The engine recognizes that differences can be strengths if they balance each other healthily. These generate `shared_strengths` without creating tension points.
- **Calm + Expressive:** Steady emotional regulation + Expressive communication (grounded in proactive repair).
- **Structured + Flexible:** Complementary social lifestyles.
- **Steady + Open:** Emotionally steady foundation combined with open attachment.
- **Careful + Balanced:** Complementary financial responsibility.

## The "No Match" Rule
NIS firmly prefers showing *no match* over a *wrong match*. 
- A pair with dangerous emotional dynamics must not be shown just because their deen/tradition values match perfectly.
- If all available candidates trigger dangerous dynamics or weak compatibility, the system returns `NO_SUITABLE_MATCHES_RIGHT_NOW`. The frontend gracefully handles this rather than substituting fake candidates.

## Human Review Trigger
If the algorithm detects multiple manageable tension points or complex dynamics (e.g., moderate compatibility with flagged risks), it marks `review_required = True`. The `NISConfidenceThresholdService` will intercept the candidate and prevent them from being shown until human review clears the flag.

## Privacy and Output Boundaries
The engine strictly enforces privacy and psychological safety:
- **No Diagnostics:** It never uses medical or clinical diagnostic labels. Safe language is used (e.g. "requires human review", "may create conflict pressure").
- **No Destiny Language:** It never outputs phrases like "perfect match", "soulmate", "Allah chose this", or "you should marry".
- **No Percentages:** Raw compatibility percentages or scores are never calculated or exposed to the user.
- **No Raw Data Leakage:** Internal private signals (like worship score, raw Barakah entries, swipe logs) are never serialized in the response.

## Developer Verification
Developers can verify the algorithm behavior by:
1. Running the exhaustive unit tests in `backend/app/nis/tests/test_psychological_pair_dynamics.py` which simulate pairwise profile interactions.
2. Observing the output of `NISCompatibilityEngine.evaluate(p1, p2)`. The resulting `CompatibilityResult` clearly enumerates `dangerous_mismatches` and `shared_strengths`.
