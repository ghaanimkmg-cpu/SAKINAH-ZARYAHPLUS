# Sakinah NIS: Omar Demo Script

This script is designed to be a simple, human walkthrough of the Sakinah Network of Intentional Singles (NIS) for Omar. 

## Step 1: Open Sakinah Frontend
**Action:** Open the browser and navigate to `http://localhost:5173/sakinah`.
**Talking Point:** "Omar, this is the entry point to Sakinah. Notice the premium, intentional design that separates it from standard swiping apps. We are setting a serious tone from the very first click."

## Step 2: Show the Full Journey
**Action:** Click through the onboarding, navigating through Niyyah, Values, Mirror, and Portrait.
**Talking Point:** "Before anyone sees a single candidate, they must prove their readiness. They define their intentions, align their values, and privately reflect. None of this sensitive reflection data is shared with matches—it's strictly to ensure they are psychologically prepared for Nikah."

## Step 3: Open the NIS Proof Page
**Action:** Navigate to `http://localhost:5173/sakinah/dev/proof-report`.
**Talking Point:** "You asked for proof that the algorithm actually protects our users. This dashboard runs live scenarios through our backend engine in real-time to prove the safety rules work."

## Step 4: Explain the Proof Results
**Action:** Point to the different test results on the proof page.
**Talking Point:** 
- "Here, we injected a highly compatible, safe candidate. The system allowed them through."
- "Next, we injected a user who was previously banned. The engine caught the identity hash and permanently blocked them from the pool."
- "We then injected a user who scored high on anger and low on repair attempts during their readiness phase. The system blocked them to protect our users from emotional harm."
- "We tested an age mismatch beyond our strict thresholds, and they were blocked."
- "Finally, we tested candidates who gave weak, low-effort answers. The engine recognized their lack of seriousness and filtered them out."

## Step 5: Show KYC / Liveness Pages
**Action:** Navigate to `http://localhost:5173/sakinah/kyc` and then `/sakinah/liveness`.
**Talking Point:** 
- "To keep out fakes, we built a strict identity verification flow. Right now, it is running in 'Sandbox Mode', meaning the code is fully wired, but it's not burning real money on vendor APIs yet."
- "Once you approve, we just plug in the real Onfido/SumSub credentials."
- "Most importantly, we respect user privacy. **We do not store raw Aadhaar numbers, government IDs, or their selfies in our database.** We only extract the verified name, age, and gender, and then immediately discard the sensitive files."

## Step 6: Honest Production Gaps
**Action:** Return to the home screen.
**Talking Point:** "To take this live to the public, there are three remaining steps:
1. We need the real paid API keys for the KYC vendor.
2. We need to swap our generic authentication with the live Firebase Admin tokens.
3. We need to wire up push notifications so people know when they get a match.
Everything else—the database, the algorithm, the safety checks—is built and fully functional."
