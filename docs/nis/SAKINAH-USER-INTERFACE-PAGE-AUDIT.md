# Sakinah User Interface Page Audit

## 1. What Omar Requested
Omar requested a new "User Interface Page" to act as a profile completion flow. The requested sections were:
1. Basic identity
2. Marriage intention
3. Faith / maslak / practice
4. Family and wali
5. Lifestyle and responsibility
6. Communication and conflict
7. Spouse preferences
8. Boundaries and safety
9. Review and submit

## 2. What Already Exists
The vast majority of these sections already exist natively within the Sakinah Journey, backed by NIS APIs and persistence layers:
- **Basic identity**: Handled by the `/sakinah/kyc` and Demographics backend layer.
- **Marriage intention**: Handled by `/sakinah/niyyah`.
- **Faith / maslak / practice**: Handled by `/sakinah/values`.
- **Family / Lifestyle / Communication**: Handled dynamically through the 9 dimensions in `/sakinah/mirror`.
- **Spouse preferences**: Handled by `/sakinah/preferences` (age, relocation).

## 3. What Should Not Be Duplicated
We must **not** duplicate Niyyah, Values, Mirror, Portrait, or Preferences. Creating a monolithic "User Interface Page" that asks these questions again would break the UX, fracture the database schema, and violate the principle of the structured, phased Sakinah journey.

## 4. Recommended Final Structure
**Option D: Do not create a new page; improve existing pages/flow only.**

The existing `/sakinah/home` page already serves as a profile completion dashboard and guided intake hub. Instead of a separate "User Interface Page", we should just add the missing data points to the existing Journey. 

## 5. Missing Questions Only
The only genuinely missing pieces of information that were in the proposal but are absent from the current flow:

**Family and wali:**
- Wali Name
- Wali Relation (Father, Brother, Uncle, etc.)
- Wali Contact Information
- Desired Wali involvement level (e.g., handles all chats, supervises only, steps in later)

**Boundaries and safety (Preferences expansion):**
- Hard Dealbreakers (e.g., Smoking, willing to have kids, previous marriages)

**Review confirmation:**
- A final "Review and Submit" summary step before entering the "Considered Few" matching pool.

## 6. Backend/API Impact
If we add the missing questions to the existing flow:

**Wali Details:**
- **Backend model**: Missing. Needs `nis_wali_details` table or columns in `nis_users`.
- **Feed NIS**: Yes. Wali involvement style is a matching factor.
- **Privacy**: Private. Only shared with a match when conversation begins.

**Boundaries (Dealbreakers):**
- **Backend model**: Partially exists in `nis_preferences`, but needs new columns for smoking, kids, etc.
- **Feed NIS**: Yes, as hard filters.
- **Privacy**: Private. Filter-only.

**Review Summary:**
- **Backend model**: No new fields needed. Just a frontend aggregate view.

## 7. Final Recommendation
Do **not** build a separate "User Interface Page". 
Instead, add a "Wali & Boundaries" phase to the existing journey (perhaps as an extension of `/sakinah/preferences`), and a final "Review Profile" step before unlocking the `/sakinah/considered-few` pool. This keeps the architecture clean and prevents duplicate data entry.
