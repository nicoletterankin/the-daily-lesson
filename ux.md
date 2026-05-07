# Curious Kelly — UX Design

*Design for kellyai.com/learn and kellyai.com/studio. Corrected 2026-05-07 to match Kelly-as-wallpaper architecture (see `spec-updates.md`).*

---

## The architectural commitment

**Kelly is the screen.** Full-bleed 16:9 streamed video wallpaper, always. She never shrinks, never moves, never becomes a badge, never stacks. Think interactive YouTube Live Stream / Zoom call with the most advanced digital human — she fills the viewport for the entire lesson, you make eye contact with her continuously.

Everything else — diagrams, controls, the timeline, the reflection prompt, even the goodbye — floats on top of her as **HUD overlays**. Overlays are bounded, edge-anchored, and **never cover her face**. The runtime knows where her face is (we're driving the lipsync; we have the keypoints) and enforces a face-region no-fly zone for every overlay.

The three planes are not three windows side-by-side. They're three depths of one frame:

| Depth | What it is | Coverage |
|---|---|---|
| **Kelly (back, wallpaper)** | 16:9 streamed video. Always full-bleed. | 100% of viewport, always. |
| **Modal (middle, HUD widgets)** | Diagrams, sliders, timelines, cards. Float over Kelly. Snap to corner regions. | Per-widget ~40% max; combined ~60% max. Never the face. |
| **User (front, controls)** | Mic, scrubber, track chip, calendar dots. Edge-anchored. | Minimal footprint. |

---

## Design principles

1. **3-second rule.** URL hit to Kelly's first word ≤ 3s. No splash, no signup, no cookie banner.
2. **Eye contact never broken.** Kelly's eyes are visible in every frame of every lesson. This is product-spec Bar F.
3. **One concept per session.** No tabs, no nav, no module tree. Today's lesson is the unit.
4. **Touch the thing she's teaching.** Modal widgets are manipulable, not decorative. Drag, scrub, tap-to-expand.
5. **No streaks, notifications, leaderboards.** Ever.
6. **Close-the-tab is a feature.** The end state explicitly invites you to leave.
7. **Widgets snap; they don't free-float.** Five legal positions: top-left, top-right, bottom-left, bottom-right, chin-bar (centered, below face). Center is forbidden.

---

## Screen 1 — Arrival (t = 0 to 3s)

The first frame is the same shape as the lesson, so Kelly's arrival doesn't jolt the geometry.

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─○─○─○─○                                          ⌄ Learn EN  │  ← user-plane chrome
│   ↑                                                              │     (calendar dots TL,
│  (calendar dots, today highlighted)                              │      track chip TR)
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│              [black, fading to Kelly's first frame]              │
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Day 127 · The bottleneck                                  │ │  ← chin-bar overlay
│  │  Kelly is arriving…                                        │ │     (will dismiss when
│  └────────────────────────────────────────────────────────────┘ │      Kelly speaks)
└──────────────────────────────────────────────────────────────────┘
```

- The viewport is 16:9. On non-16:9 displays (most laptops, all phones in portrait), letterbox to 16:9 with black bars. Kelly's framing is preserved across every device.
- Calendar dots (top-left), track chip (top-right), title/status (chin-bar) are already in their final positions. When Kelly's video appears, the chrome stays put.
- "Kelly is arriving…" lives in the chin-bar and is replaced by silence (and Kelly's gaze) once she's live.

---

## Screen 2 — Active lesson (the canonical view)

This is where ~95% of the session lives. **Kelly is everywhere. Modal widgets float on top of her, snapped to corner regions and chin-bar. Her face is never covered.**

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─○─○─○─○                                          ⌄ Learn EN  │
│                                                                  │
│                  ┌──────────────────────────┐                    │
│                  │  words → sentences → …   │  ← Modal widget,   │
│                  │  [tap any node]          │     TR snap        │
│                  └──────────────────────────┘                    │
│                                                                  │
│                                                                  │
│                       KELLY (full-bleed)                         │
│                                                                  │
│                ╔═══════════════════════════╗                     │
│                ║   ←   FACE NO-FLY ZONE  → ║   ← runtime-enforced │
│                ║   (no overlay enters)     ║     bounds (invisible │
│                ╚═══════════════════════════╝     to the user)    │
│                                                                  │
│                                                                  │
│  ┌────────────┐                                                  │
│  │ Recovery   │                                                  │
│  │ from error │  ← Modal widget, BL snap                         │
│  │ (counter)  │     (only ~25% of viewport)                      │
│  └────────────┘                                                  │
│                                                                  │
│  ●━━━━━━━━━━○──────────────  3:42 / 7:00          🎙️  ⏸        │  ← user-plane,
└──────────────────────────────────────────────────────────────────┘     chin-bar
```

### What you see
- Kelly is the wallpaper. She is making eye contact with you.
- A diagram widget ("words → sentences → …") snapped to TR. Kelly's gaze flicks to it as she introduces it; her gesture points to its general direction.
- A counter widget ("Recovery from error") snapped to BL — appears later in the lesson, once she introduces the concept.
- Bottom edge: timeline scrubber + mic + pause. The timeline lives below the face naturally — no risk of occlusion.
- Top edge: calendar dots and track chip stay where they were on arrival.

### What you don't see
- The face no-fly zone is invisible. The layout engine just refuses to place any widget inside it. If a widget would land there, it slides to the nearest legal snap point.
- Widgets don't free-float. They snap. This bounds creator chaos in Studio and learner cognitive load.

### Widget budget
Default: max 3 simultaneous widgets. Studio allows up to 5 with a warning. More than 5 would force overlap and increase no-fly-zone risk.

---

## Screen 3 — User interrupts (mic active)

Tap mic. **Kelly stays full-bleed.** Her lipsync freezes within ~150ms; her eyes shift to lock onto you (gaze cue: "I'm listening"). Modal widgets dim to ~30% but stay visible — you might be pointing at one. Live transcript appears in a chin-bar overlay.

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─○─○─○─○                                          ⌄ Learn EN  │
│                                                                  │
│                  ┌──────────────────────────┐                    │
│                  │  words → sentences → …   │  ← dimmed 30%      │
│                  └──────────────────────────┘                    │
│                                                                  │
│                                                                  │
│                       KELLY (listening,                          │
│                        eyes on user)                             │
│                                                                  │
│                                                                  │
│                                                                  │
│  ┌────────────┐                                                  │
│  │ Recovery   │  ← dimmed 30%                                    │
│  │ from error │                                                  │
│  └────────────┘                                                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ▓▓▓▓▓▓░░  "wait, what does recovery from error mean?"     │ │  ← chin-bar:
│  └────────────────────────────────────────────────────────────┘ │     live transcript
│  ●━━━━━━━━━━○──────────────  3:42 / 7:00         🔴  ⏸          │
└──────────────────────────────────────────────────────────────────┘
```

- Live transcript is the only place text-from-user appears on screen.
- On end-of-utterance, Kelly's mouth re-engages from a Q-handling state. The lesson timeline holds (the scrubber doesn't advance during the interrupt).

---

## Screen 4 — User touches a widget

Tap a node in the diagram widget → it expands **inside the widget's snap region.** No modal dialog, no full-screen takeover, no occlusion of Kelly.

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─○─○─○─○                                          ⌄ Learn EN  │
│                                                                  │
│              ┌──────────────────────────────────┐                │
│              │  words → [SENTENCES] → …          │                │
│              │             ▲                     │  ← widget      │
│              │       ┏━━━━━┻━━━━━━━┓             │     expanded   │
│              │       ┃ a string of  ┃            │     in place,  │
│              │       ┃ words with a ┃            │     bounded    │
│              │       ┃ verb         ┃            │     within     │
│              │       ┗━━━━━━━━━━━━━━┛            │     ~40%       │
│              └──────────────────────────────────┘                │
│                                                                  │
│                       KELLY (acknowledging:                      │
│                        "right — sentences.")                     │
│                                                                  │
│                                                                  │
│  ●━━━━━━━━━━○──────────────  3:42 / 7:00          🎙️  ⏸        │
└──────────────────────────────────────────────────────────────────┘
```

- Tap-to-expand happens **within the widget's bounding box.** If the expansion would breach the no-fly zone or exceed 40% of the viewport, the widget pops to a larger but still-bounded box on the same edge.
- The runtime emits `modal_touch` with the node's identity. Kelly's next sentence acknowledges it ("right — sentences.").
- Drag the timeline scrubber → Kelly silences, widgets rewind their state with the lesson, you can replay any 10-second beat. Release → Kelly resumes.

---

## Screen 5 — Reflection prompt (the close)

Around minute 6:30, Kelly steps out of the canvas and asks the one question. **She is still full-bleed and looking at you.** Modal widgets dismiss. The prompt appears as a chin-bar overlay.

```
┌──────────────────────────────────────────────────────────────────┐
│  ●─○─○─○─○                                          ⌄ Learn EN  │
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│                       KELLY (looking at you,                     │
│                        asking the question)                      │
│                                                                  │
│                                                                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  "What's one error you'll let yourself                     │ │
│  │   make in your target language today?"                     │ │  ← chin-bar
│  │                                                            │ │     (prompt)
│  │  [ type, or hold mic to speak ]            [ skip ]        │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ●━━━━━━━━━━━━━━━━━━━━━━━━━●  6:42 / 7:00                       │
└──────────────────────────────────────────────────────────────────┘
```

- Modal widgets dismiss (slide off-edge in their snap direction). Kelly does not move; the screen just gets quieter.
- Kelly's gaze is locked on the user — the question is a person asking, not a form prompt.
- Skip is first-class. Tap skip → straight to end state. No penalty, no reminder, no "are you sure?"
- Answer is private to the user. Stored locally by default. Only shared with Kelly's session for in-context follow-up.

---

## Screen 6 — End state (the goodbye)

**Kelly is still on screen.** She says "that's the lesson" out loud. The two affordances appear as overlay buttons.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                                  │
│                                                                  │
│                                                                  │
│                       KELLY (smiling, saying                     │
│                        "that's the lesson —                      │
│                         you're done for today.")                 │
│                                                                  │
│                                                                  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  That's the lesson. You're done for today.                 │ │  ← chin-bar copy
│  │                                                            │ │
│  │  [ Close the tab ]              [ Tomorrow → ]             │ │
│  │                                                            │ │
│  │  Day 128 unlocks at midnight your time.                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

- "Close the tab" is a real button. `window.close()` first; on browsers that block it, navigate to `about:blank` with the same copy still visible briefly.
- "Tomorrow →" is *disabled* until midnight local. We don't let users binge ahead.
- Kelly fades out only after the user takes one of the two actions. The default is silence and her presence — we don't push.
- No "share your streak." No "you've learned 12 days in a row." No notification opt-in. Ever.

---

## Screen 7 — Track picker

Tapping the `⌄ Learn` chip in the top-right. Single floating overlay; **Kelly stays full-bleed behind it.**

```
                                          ┌─────────────────────────────┐
                                          │  ◉ Learn                    │
                                          │    The 365 most important   │
                                          │    things to know           │
                                          │                             │
                                          │  ◯ Grow                     │
                                          │    AI fluency for the       │
                                          │    next decade              │
                                          │                             │
                                          │  ─────────────────────────  │
                                          │                             │
                                          │  Language: English ⌄        │
                                          │  25 available               │
                                          └─────────────────────────────┘
```

- Snaps to TR. ~30% of viewport. Doesn't enter the face no-fly zone (TR snap region is above-and-right of the face by definition).
- Language switch re-routes the WebRTC session to a track-language Kelly. No translation overlay; the lesson is taught natively.

---

# The Studio — kellyai.com/studio

The creator authoring surface. **The creator's avatar is full-bleed in the preview**, exactly like Kelly is in `/learn`. Same Bar F applies — Studio's layout engine refuses to place a widget over the creator's face.

## Studio canonical view

```
┌──────────────────────────────────────────────────────────────────┐
│  ◀ My Lessons    "The bottleneck"        [ Preview ] [ Publish ] │
├──────────────────┬───────────────────────────────────────────────┤
│                  │                                               │
│  SCRIPT          │              CREATOR'S AVATAR                 │
│  (collapsible)   │              (full-bleed preview)             │
│                  │                                               │
│  Hook            │      ┌──────────────────────┐                 │
│  ─────           │      │ words → sentences    │ ← widget        │
│  Most people…    │      └──────────────────────┘   (TR snap)     │
│                  │                                               │
│  Story           │                                               │
│  ─────           │                                               │
│  In linguistics… │              [creator's face]                 │
│                  │              (no-fly zone)                    │
│  Wonder          │                                               │
│  ──────          │                                               │
│  What if…        │                                               │
│                  │                                               │
│  Action          │                                               │
│  ──────          │                                               │
│  Today…          │  ┌─────────────────────────────────────────┐ │
│                  │  │  ⊕ Generate  ⇪ Import  ▦ Compose  ✎ Refine│  ← floating
│  Wisdom          │  └─────────────────────────────────────────┘ │     primitive bar
│  ──────          │       (HUD over the avatar, chin-bar zone)    │
│  Fluency is…     │                                               │
│                  │  ●━━●━━●━━●━━●─────────  0:00 ── 7:00          │
│                  │   Hk Sy Wn Ac Wi  (timeline, lesson sections)  │
└──────────────────┴───────────────────────────────────────────────┘
```

### What's true here
- **The avatar fills the right column** (preview pane). When the creator collapses the script column, the avatar fills the entire viewport — exactly the published-lesson view.
- The four primitives (⊕ Generate / ⇪ Import / ▦ Compose / ✎ Refine) live as a floating HUD bar in the chin-bar zone. Always visible. No mode switch.
- Widgets the creator places snap to the same five regions (TL/TR/BL/BR/chin-bar). The layout engine prevents face occlusion automatically — the creator can't accidentally publish a lesson where their own face is covered.
- Script column is the *only* non-overlay UI in Studio. Collapse it for full-bleed preview at any time.

### Avatar capture (one time, ever)

```
┌──────────────────────────────────────────────────────────────────┐
│   Record your avatar                                              │
│                                                                   │
│   We need 5 short clips. Same lighting, same wardrobe,            │
│   one session. Total: ~3 minutes. Frame yourself 16:9.            │
│                                                                   │
│       ╭──────────╮ ╭──────────╮ ╭──────────╮                     │
│       │ neutral  │ │   left   │ │  right   │                     │
│       │   ▓▓▓    │ │          │ │          │                     │
│       ╰──────────╯ ╰──────────╯ ╰──────────╯                     │
│       ╭──────────╮ ╭──────────╮                                  │
│       │   down   │ │ lean in  │                                  │
│       ╰──────────╯ ╰──────────╯                                  │
│                                                                   │
│   [ Start recording ]            Already done? [ Re-capture ]     │
└──────────────────────────────────────────────────────────────────┘
```

Same five pose channels as Kelly herself (product-spec §14): neutral, left, right, down, lean_in. Captured at 16:9, 1080p minimum, 4K preferred. Validated at 100% on a large screen.

### Publish

```
┌──────────────────────────────────────────────────────────────────┐
│   Publish "The bottleneck"                                        │
│                                                                   │
│   URL:  yourname.kellyai.com/the-bottleneck                       │
│         (or use a custom domain — paid tier)                      │
│                                                                   │
│   ☑ Free tier: 1 published lesson, watermarked                    │
│   ☐ Paid ($29/mo): unlimited, no watermark, custom domain         │
│                                                                   │
│   Bar F check: face never occluded ✓                              │
│   Widget budget: 3 used, 5 max ✓                                  │
│   Total runtime: 6:54 (within 5–8 min target) ✓                   │
│                                                                   │
│                                          [ Publish ]              │
└──────────────────────────────────────────────────────────────────┘
```

Pre-publish checks include the layout engine's Bar F verification — automatic, not manual.

---

## Failure modes

| Failure | What the user sees |
|---|---|
| **Kelly takes >3s to arrive** | Chin-bar copy persists: "Kelly is arriving…". After 8s: "Kelly is having a slow morning. [Retry] · [Read the lesson]" — fallback to a static text/diagram version. The daily lesson is never gated on streaming. |
| **WebRTC blocked by network** | Same fallback. |
| **No mic permission** | Mic button shows `🚫`. Tapping it offers a typed-input field. Lesson works without voice. |
| **Local model fails Bar C (soul)** | Per Runbook D: Kelly falls back to a tighter, more scripted persona. Lesson still ships. |
| **Language not yet covered** | Track picker shows the 25 supported languages plus "Help us translate." |
| **Display is portrait/non-16:9** | Letterbox to 16:9 with black bars top/bottom. Kelly's framing preserved across devices. No portrait-cropped Kelly stream — see `spec-updates.md` open question #3. |

---

## What this design is NOT

- Not a Zoom call with Kelly in a tile and a whiteboard next to her.
- Not a video player with a chat sidebar.
- Not a slide deck with Kelly inset in a corner badge.
- Not a chatbot. Voice and text are interrupts to a structured lesson, not the lesson itself.
- Not a course platform. No syllabus, no module tree, no "next up." Today's lesson is the unit.
- Not gamified. No XP, no streaks, no badges, no notifications, no email. Ever.

---

## Open design questions (flag for founder, see `spec-updates.md` for full list)

1. **Max widget coverage** — recommend 40% per widget, 60% combined.
2. **Face no-fly zone geometry** — recommend ear-to-ear, forehead-to-chin, +10% padding.
3. **Portrait/mobile** — letterbox to 16:9 (recommended) vs. portrait-cropped Kelly (more cost, separate capture session).
4. **Widget snap regions** — TL, TR, BL, BR, chin-bar. Center forbidden. Confirm these five.
5. **Max simultaneous widgets** — 3 default, 5 max for Studio. Confirm.
6. **Calendar dots** — top-left, 5 dots. Confirm or alternate.
7. **First-arrival pre-Kelly frame** — black with chin-bar title (recommended), so the geometry of arrival matches the geometry of the lesson.
