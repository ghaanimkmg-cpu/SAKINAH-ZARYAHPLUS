# Sakinah Responsive Web Layout Correction

## Issue Found
During the dev reference implementation, the visual layout from the standalone `sakinah-dev-reference.html` file was copied verbatim. This reference file was designed to *demonstrate* the mobile application flow on a desktop monitor, so it explicitly wrapped the content in a fixed-size mobile simulator frame (complete with hardware notch, status bar, and phone screen border). When ported into the React app via `SakinahJourneyFrame` and `SakinahShell`, it forced the entire web application to render as a tiny phone simulator in the middle of a user's large desktop monitor, rather than acting like a responsive web app.

## Why the Phone Frame was Wrong
ZaryahPlus is a full-stack responsive web application with its own topbar and sidebar. The reference file's phone frame was a design artifact for presentation, not the intended target layout for desktop users. A production web application should take advantage of available desktop space with proper responsive containers, rather than arbitrarily restricting users to a 392px width on a 1440px monitor.

## Desktop Layout Correction
Both `SakinahJourneyFrame.tsx` and `SakinahShell.tsx` were rewritten to act as proper responsive web containers:
1. Removed `w-[392px]` constraints, notch overlays, and status bar mocks.
2. Implemented `max-w-6xl` (`1152px`) wrapper for the journey frame to allow left/right rails to breathe alongside the main content.
3. Implemented a `max-w-[700px]` to `max-w-[800px]` constraint specifically for the central content column on large screens, ensuring forms and text lines remain readable and comfortable, without being awkwardly narrow.
4. Preserved the premium dark-gold background gradients, outer shadows, and rounded borders on desktop to maintain the premium feel.

## Mobile Layout Behavior
Mobile styling remains structurally similar to the reference:
1. Flex containers shift seamlessly to full viewport width at `sm` breakpoint and below.
2. Horizontal padding and vertical margins tighten to maximize screen real estate (`px-[22px]`).
3. Single column layout gracefully stacking the content, without any horizontal scroll issues.

## Testing Parameters
**Routes Tested on Desktop & Mobile:**
- `/sakinah` (Entry/Role/Primer/KYC/Liveness)
- `/sakinah/home`
- `/sakinah/niyyah` & `/values` & `/mirror` & `/portrait`
- `/sakinah/preferences` & `/considered-few` & `/candidate/:id`
- `/sakinah/matchflow/:id` & `/conversation/:id` & `/decision/:id`
- `/sakinah/safety` & `/community` & `/vent`

**Widths Tested:**
- Desktop: `1440px`, `1280px`, `1024px`
- Mobile: `768px`, `430px`, `390px`

## Remaining UI Risks
None identified. The premium quality typography, pacing, and color palette have been fully maintained while completely removing the jarring phone-frame styling on PC displays. The flow behaves naturally as a modern web app.
