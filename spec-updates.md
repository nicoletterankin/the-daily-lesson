# Spec updates needed — Kelly-as-wallpaper correction

*Pre-RTX. Planning only. No build changes yet.*

---

## The correction (restated crisply)

**Wrong (what I had in `ux.md` and what reads ambiguously in product-spec §1):** Kelly in a small framed window, Modal canvas as a separate plane beneath/beside her, User controls in front. Kelly can shrink, reposition, become a badge.

**Right (the actual product):** Kelly is the **full-bleed 16:9 wallpaper, always.** She never shrinks, never slides, never becomes a badge, never stacks below or beside anything. The screen is her frame. Think interactive YouTube Live Stream / Zoom call with the most advanced digital human ever built — she fills the viewport, you make eye contact with her continuously, and *everything else floats on top of her as HUD elements*.

**The three planes, corrected:**

| Plane | What it is | Coverage rule |
|---|---|---|
| **Kelly (back, full-bleed)** | 16:9 streamed video wallpaper. Always present, always centered, always at full viewport. | 100% of viewport, always. |
| **Modal (middle, HUD overlays)** | Apps, widgets, diagrams, timelines, sliders. Float on top of Kelly. Draggable, dismissible. | **Never full-screen. Never occlude Kelly's face/eyes.** |
| **User (front, controls)** | Mic, scrubber, track picker. | Floats above modals. Edge-anchored, minimal footprint. |

The product is *not* "Kelly on a slide deck" or "Kelly inside a Zoom tile next to a whiteboard." It's "Kelly as a window into a teacher you're talking to, with manipulable artifacts hovering between you."

---

## What changes in `01-product-spec.md`

### §1 — The medium / three planes (rewrite required)

Current text reads as if Kelly, Modal, and User are equal-weight planes layered like a triptych. Rewrite to make explicit:

- Kelly is the **wallpaper**. Full-bleed 16:9, never resized, never repositioned.
- Modal elements are **HUD overlays** — like sticky notes, Loom comment bubbles, or floating browser-extension widgets — that appear on top of Kelly without covering her face.
- The "shared modal plane between her and the user" phrasing in current spec §1 is misleading. Better framing: "a HUD layer of manipulable widgets that float in front of Kelly, on the same surface the user touches."

### §2 — Quality bars (add a new bar)

Add **Bar F — Eye contact never broken.**

- Operationalization: in any frame of any lesson, Kelly's eyes must be visible to the user. No overlay element ever occludes the eye region of the rendered Kelly frame.
- Test method: automated — render 10 random frames per lesson with all worst-case overlay states (max widgets, longest text, mid-drag), assert eye-region pixels are not occluded.
- Combined with existing Bar B (liveness/interactivity) but distinct: B is about Kelly's responsiveness; F is about the user never losing her face.

This is a hard constraint on all overlay design. It bounds Studio creators too.

### §3 — Kelly plane (back) — streaming runtime (reframe)

Rewrite to lead with: "Kelly's video stream fills the entire viewport at 16:9, always. There is no compositing layer behind her, no fallback static image position. The MuseTalk → kelly_avatar plugin renders one full-bleed video track per session for the entire lesson duration."

Implications already true in current spec, just need to be made explicit:
- 5090 is rendering full viewport-resolution Kelly continuously, not a thumbnail.
- WebRTC track is sized to viewport, not to a small frame.
- No "picture-in-picture" behavior, ever.

### §4 — Modal plane (middle) — choreographed diorama (significant reframe)

Current spec calls this a "choreographed diorama" — language that suggests a full canvas/scene. Replace with:

> The Modal plane is a **HUD layer of floating widgets** — diagrams, equations, timelines, maps, sliders, cards — that appear on top of Kelly when relevant, animate in/out with her speech, and respond to touch. Widgets are bounded boxes (max ~40% of viewport area each, max ~60% combined coverage). The user can drag, resize within a clamp, dismiss, or tap-to-expand. Widgets never occlude Kelly's face region.

Add to §4:
- **Widget budget per moment.** At most N widgets visible simultaneously (recommend N=3 for sanity; let Studio go to 5 with a warning).
- **Face-region no-fly zone.** Define a rectangular region around Kelly's rendered face that overlays cannot enter. The runtime knows where her face is (we're driving the lipsync — we have the keypoints). Widget layout engine respects the box.
- **Layout engine.** Widgets snap to four corner regions (TL, TR, BL, BR) and a chin-bar (centered, bottom, below face). Default is BL or BR. Center is forbidden.

### §5 — User plane (front) — controls and inputs (small change)

Change one line: User-plane elements (mic, scrubber, track chip) are edge-anchored and float above all modal widgets. They are subject to the same face-region no-fly zone. The bottom timeline already lives below the face naturally.

### §6 — The Studio — creator recording mode (significant implications)

Reframe Studio canvas:
- The creator's recorded avatar is **also full-bleed 16:9 wallpaper** in their published lesson.
- Studio's authoring view shows the creator's avatar full-bleed in the right column (preview-mode), with the four-primitive bar (⊕ Generate / ⇪ Import / ▦ Compose / ✎ Refine) floating on top of the avatar as a HUD bar.
- The script column (left) is the only non-overlay UI in Studio. It can be collapsed to give the creator full-bleed preview at any moment.
- Same Bar F applies to creator-published lessons. Studio's layout engine enforces the no-fly zone for creators too — they can't accidentally publish a lesson where their own face is covered.

### §10 — Domains (no change, keep as-is)

### §12 — Build sequence (no change to phases, but)

Phase 2 (Modal plane and aids, weeks 8-12) was already scoped to build the diorama. The work is the same; the framing is different. Same components, but:
- Phase 2 deliverable is now "HUD overlay layout engine + face-region no-fly zone enforcement" rather than "modal canvas with embedded Kelly window."
- This is a *clarification*, not a scope change. The plumbing is the same.

### §14 — Kelly source video capture (one clarification)

Five pose channels (neutral, left, right, down, lean_in) are still correct, but add: "captured at 16:9, framed for full-viewport rendering. Source resolution must support full-bleed playback at 1080p minimum, 4K preferred." This was implicit; make it explicit.

---

## What changes in `02-financial-model.md`

**Nothing material.** Kelly being full-bleed vs. windowed is a layout decision, not a cost structure decision. The runtime is already rendering the full viewport. ~$0 marginal cost is unaffected.

One small note worth adding to the model's notes section: "Full-bleed always-on Kelly means viewport-resolution streaming continuously per session; this is already accounted for in the 5090's per-session capacity estimate."

---

## What changes in `03-strategic-narrative.md`

One paragraph in "The product we will launch" benefits from a sharper framing:

**Current:** "Curious Kelly — an interactive AI teacher streaming today's lesson live over WebRTC. […] Kelly's body and gaze choreograph to interactive visual aids on a shared modal plane between her and the user."

**Proposed:** "Curious Kelly — an interactive AI teacher streaming today's lesson live over WebRTC. The screen is her. Full-bleed, 16:9, the most advanced digital human ever shipped — closer to a YouTube Live Stream with a teacher who can see what you're doing than to a video player with a chat sidebar. Diagrams, timelines, and interactive aids float on top of her as HUD widgets without ever breaking eye contact. The user can speak, interrupt, ask questions; Kelly's gaze and gestures choreograph to the widgets she's pointing at."

This is a sharpening, not a strategy change. The moat is identical.

---

## What changes in `04-operations-log.md`

Add to "Recent decisions log":

> **2026-05-07 — UX model clarified: Kelly is the wallpaper, not a windowed plane.** Kelly renders full-bleed 16:9 always; modal elements are HUD overlays that never cover her face. Bar F (eye contact never broken) added to product spec §2. No build-sequence change; clarification only.

Add to "Open decisions awaiting founder action":

- **Resolve: max widget coverage of viewport.** Recommendation: 40% per widget, 60% combined.
- **Resolve: face-region no-fly zone geometry.** Recommendation: bounding box from forehead to chin, ear-to-ear, padded 10%.
- **Resolve: portrait/mobile policy.** Recommendation: letterbox to 16:9 (black bars top/bottom) so Kelly's framing is preserved across devices. Alternative: portrait-cropped Kelly is a different production stream — costly and adds a second pose-capture session. Letterbox wins on cost and simplicity.

---

## What I had wrong in `ux.md` (now fixed in this branch)

Specifically wrong:
1. **Screen 2 (Active lesson)** — I drew Kelly as a small framed video at the top with the Modal canvas as a large box beneath her. Should be: Kelly fills the entire viewport, Modal widgets float on top in a corner.
2. **Screen 3 (Interrupt)** — I had Modal "dim 30% and stay visible" while Kelly listens. The dim is fine but Kelly was framed; she should be full-bleed and her listening is conveyed by gaze alone.
3. **Screen 5 (Reflection)** — I had "Modal fades to background" and "Kelly centered, full attention." That was halfway right (Kelly always centered, sure) but wrong in implying Kelly *moved* to be centered. She was already there. The change is: Modal widgets dismiss; the reflection prompt appears as a single chin-bar overlay; Kelly looks at the user.
4. **Screen 6 (End state)** — I drew an empty page with "Close the tab" / "Tomorrow →" buttons. Wrong — Kelly is still there as wallpaper, saying goodbye. The two buttons are overlays.
5. **Open question #2 (mobile)** — I asked "does Kelly stack below Kelly, or shrink to a corner badge?" Both options are wrong by this correction. Right answer: letterbox to 16:9.
6. **Studio canonical view** — I drew a "preview window" with avatar in a small frame and a four-primitive bar in a separate panel. Should be: full-bleed creator avatar with the bar floating on top as an HUD strip, plus collapsible script column on the left.

`ux.md` will be corrected in a follow-up commit.

---

## New open questions (none of these blocks the build, but lock before Phase 2)

1. **Max modal widget coverage** — 40%/60% recommended. Founder confirm or override.
2. **Face-region no-fly zone geometry** — recommend ear-to-ear forehead-to-chin + 10% padding. The runtime already has Kelly's face keypoints from MuseTalk; trivial to compute.
3. **Portrait/mobile policy** — letterbox recommended. Cheaper, preserves framing, no second capture session.
4. **Widget snap regions** — TL / TR / BL / BR / chin-bar. Center forbidden. Confirm these five are the universe.
5. **Maximum simultaneous widgets** — recommend 3 default, 5 max for Studio creators with a warning UI.
6. **Reflection prompt rendering** — chin-bar overlay (text appears below Kelly's face), Kelly looks at the user as she asks. Confirm this is the canonical reflection treatment.
7. **End state rendering** — Kelly still full-bleed, saying "That's the lesson," with two overlay buttons (Close the tab / Tomorrow →) as a chin-bar pair. Confirm.
8. **Track picker overlay placement** — top-right corner (TR snap region), single chip. Confirm.
9. **Calendar dots placement** — top-edge centered, narrow strip, 5 dots. Confirm or alternate.
10. **First arrival (t = 0 to 3s)** — what's on screen before Kelly's first frame arrives? Recommend: black with the date and lesson title in the chin-bar position, so the visual frame is the same shape as the lesson and Kelly fades in without geometric jolt.

---

## TL;DR

Three sentences:

1. Kelly is the entire screen, always. Full-bleed 16:9, never shrinks, never moves, never becomes a badge.
2. Modals are HUD widgets that float on top — they never cover her face, never go full-screen, and dismiss when not in use.
3. Spec §1, §2, §3, §4, §6, and §14 need updates per above; financial model and strategy doc need a single sharpening line each; ops log gets a decision entry and three new open decisions; my `ux.md` needs the screens redrawn (will follow in next commit).
