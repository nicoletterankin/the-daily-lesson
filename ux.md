# Curious Kelly — UX Design

*Design for kellyai.com/learn and kellyai.com/studio. Anchored in the three-plane architecture from product-spec §1: Kelly (back), Modal (middle), User (front).*

---

## Design principles (the constraints all screens obey)

1. **3-second rule.** From URL hit to Kelly's first word: ≤3s. No splash, no signup gate, no cookie banner. Anyone, anywhere, on day 1.
2. **One concept per screen.** No tabs. No nav. The lesson IS the page.
3. **Gaze, not chrome.** Kelly looks at what matters. The user follows her eyes, not a UI label.
4. **Touch the thing she's teaching.** The Modal plane is manipulable, not decorative. If you can see it, you can grab it.
5. **No streaks. No notifications. No leaderboards.** The reward for finishing is closing the tab.
6. **Close-the-tab as a feature.** End state explicitly invites you to leave. We don't farm session length.

---

## Screen 1 — Arrival (t = 0 to 3s)

```
┌──────────────────────────────────────────────────────────────┐
│  kellyai.com/learn                                           │
│                                                              │
│                                                              │
│                                                              │
│                                                              │
│                  ◯  ◯  ◯  ◯  ◯                              │
│             (calendar dots, today highlighted)               │
│                                                              │
│                                                              │
│                  Day 127 · The bottleneck                    │
│                                                              │
│                                                              │
│                  Kelly is arriving…                          │
│                                                              │
│                                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- No login. No track picker yet (default = Learn; user can switch later).
- Calendar dots are the only navigation: 5 visible, today is filled.
- Title is set, never animated. Lesson is not a surprise — it's an appointment.
- "Kelly is arriving…" is replaced by Kelly's video frame as soon as the WebRTC handshake completes. If it takes >3s, this text becomes the only failure surface (see Failure modes).

---

## Screen 2 — Active lesson (the canonical view)

This is where 95% of the session lives. Three planes, composed front-to-back.

```
┌──────────────────────────────────────────────────────────────┐
│  Day 127 · The bottleneck                          ⌄ Learn  │  ← thin top bar (only chrome)
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                  ╭───────────────────╮                       │
│                  │                   │                       │
│                  │      KELLY        │   ← KELLY plane       │
│                  │   (live stream)   │     (back)            │
│                  │                   │                       │
│                  ╰───────────────────╯                       │
│                                                              │
│         ┌──────────────────────────────────────┐            │
│         │                                      │            │
│         │   words ─────► sentences ─────► ...  │   ← MODAL  │
│         │           ↑                          │     plane  │
│         │     (Kelly's gaze lands here)        │     (mid)  │
│         │                                      │            │
│         │   [tap any node to expand]           │            │
│         └──────────────────────────────────────┘            │
│                                                              │
│  ●━━━━━━━━━━━━━○─────────  3:42 / 7:00          🎙️  ⏸     │  ← USER plane
└──────────────────────────────────────────────────────────────┘
```

### What each plane does

| Plane | Role | Interaction |
|---|---|---|
| **Kelly (back)** | Live AI teacher, streaming MuseTalk-rendered video. Gaze, gesture, posture. | Read-only. She talks; you listen or interrupt. |
| **Modal (middle)** | The diorama. Diagrams, equations, timelines, maps, sliders. | **Touch, drag, scrub, tap to expand.** Choreographed to Kelly's words. |
| **User (front)** | Timeline, mic, pause. Nothing else. | Tap mic to interrupt. Drag scrubber to revisit. |

### Why Kelly is small and centered, not full-bleed

Full-bleed avatar = TV mode = passive. The lesson is a conversation around an artifact. The artifact (Modal plane) gets the visual weight; Kelly is the teacher pointing at it. Kelly's frame hovers above-and-behind so her gaze can credibly land on the diagram beneath her.

---

## Screen 3 — User interrupts (mic active)

```
┌──────────────────────────────────────────────────────────────┐
│  Day 127 · The bottleneck                          ⌄ Learn  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                  ╭───────────────────╮                       │
│                  │      KELLY        │                       │
│                  │  (paused, eyes    │   ← Kelly visibly     │
│                  │   on the user)    │     stops, listens    │
│                  ╰───────────────────╯                       │
│                                                              │
│         ┌──────────────────────────────────────┐            │
│         │   words ─────► sentences ─────► ...  │  ← Modal    │
│         │   (dimmed 30%, frozen)               │    holds    │
│         └──────────────────────────────────────┘            │
│                                                              │
│       ╔══════════════════════════════════════╗              │
│       ║  ▓▓▓▓▓░░░  "wait, what does recovery ║              │
│       ║              from error mean?"        ║              │
│       ╚══════════════════════════════════════╝              │
│                                                              │
│  ●━━━━━━━━━━━━━○─────────  3:42 / 7:00         🔴  ⏸       │
└──────────────────────────────────────────────────────────────┘
```

- Tap mic → Kelly's lipsync freezes within ~150ms, eyes shift to user (gaze cue: "I'm listening").
- Live transcript appears in the user-plane band. This is the only time live text appears on screen.
- Modal dims but stays visible — the user might be pointing at it ("this node here, what does it mean?").
- On end-of-utterance, Kelly resumes from a Q-handling state, not from where she paused. The lesson timeline holds.

---

## Screen 4 — User touches the Modal

```
┌──────────────────────────────────────────────────────────────┐
│         ┌──────────────────────────────────────┐            │
│         │                                      │            │
│         │   words ─────► [SENTENCES] ─────► ..│            │
│         │                  ▲                   │            │
│         │              ┏━━━┻━━━━━━━━━┓         │            │
│         │              ┃ a string of  ┃        │            │
│         │              ┃ words with   ┃        │            │
│         │              ┃ a verb       ┃        │            │
│         │              ┗━━━━━━━━━━━━━━┛        │            │
│         │              (expanded on tap)       │            │
│         └──────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────┘
```

- Tap a node → it expands in place. No modal dialog, no overlay. The diagram IS the substrate.
- Kelly notices (the runtime emits a `modal_touch` event) and her next sentence acknowledges it: "right — sentences. that's where most learners think fluency lives. it doesn't."
- Drag the timeline scrubber on the Modal plane → Kelly silences, the diorama rewinds, you can replay any 10-second beat. Release scrubber → Kelly resumes.

---

## Screen 5 — Reflection prompt (the close)

Around minute 6:30, Kelly steps out of the canvas and asks the one question.

```
┌──────────────────────────────────────────────────────────────┐
│  Day 127 · The bottleneck                          ⌄ Learn  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                                                              │
│                  ╭───────────────────╮                       │
│                  │      KELLY        │                       │
│                  │ (centered, full   │  ← Modal plane fades  │
│                  │   attention)      │    to background      │
│                  ╰───────────────────╯                       │
│                                                              │
│                                                              │
│        "What's one error you'll let yourself                 │
│         make in your target language today?"                 │
│                                                              │
│         ┌──────────────────────────────────────┐            │
│         │  type, or hold mic to speak…         │            │
│         └──────────────────────────────────────┘            │
│                                                              │
│  ●━━━━━━━━━━━━━━━━━━━━━━━━━●  6:42 / 7:00                  │
└──────────────────────────────────────────────────────────────┘
```

- Modal fades to ~10% opacity. The question gets the room.
- Answer is private to the user. Stored locally by default. Only shared with Kelly's session for in-context follow-up.
- Skipping is a first-class action (`skip` button, no penalty, no reminder). The reflection is offered, not enforced.

---

## Screen 6 — End state (the explicit goodbye)

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                                                              │
│                                                              │
│                   That's the lesson.                         │
│                                                              │
│              You're done for today.                          │
│                                                              │
│                                                              │
│         ┌──────────────────────┐  ┌────────────────┐        │
│         │  Close the tab       │  │  Tomorrow →    │        │
│         └──────────────────────┘  └────────────────┘        │
│                                                              │
│         (Day 128 unlocks at midnight your time)              │
│                                                              │
│                                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- "Close the tab" is a real button. Tap it, the page closes (or attempts to via `window.close()`; if blocked, navigates to `about:blank`).
- "Tomorrow →" is *disabled* until midnight local. We don't let users binge ahead.
- No "share your streak." No "you've learned 12 days in a row!" No notification opt-in.
- This screen is the product's most heretical surface. It's the one that proves the rest.

---

## Screen 7 — Track picker (the only nav surface)

Tapping the `⌄ Learn` chip in the top bar reveals:

```
                       ┌─────────────────────────────┐
                       │                             │
                       │   ◉ Learn                   │
                       │     The 365 most important  │
                       │     things to know          │
                       │                             │
                       │   ◯ Grow                    │
                       │     AI fluency for          │
                       │     the next decade         │
                       │                             │
                       │   ─────────────────────     │
                       │                             │
                       │   Language: English ⌄       │
                       │   25 available              │
                       │                             │
                       └─────────────────────────────┘
```

- Two tracks. That's it. Future tracks slot in here without redesign.
- Language switch re-routes the WebRTC session to a track-language Kelly. No translation overlay; the lesson is taught natively in 25 languages.
- Pinned to top-right because it's the only persistent affordance.

---

# The Studio — kellyai.com/studio

The creator surface. One canvas. Four primitives. No mode-switching.

## Studio canonical view

```
┌──────────────────────────────────────────────────────────────────┐
│  ◀ My Lessons    "The bottleneck"        [Preview]  [Publish]   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐  ┌────────────────────────────────────────────┐ │
│  │            │  │                                            │ │
│  │  SCRIPT    │  │              UNIFIED CANVAS                │ │
│  │            │  │                                            │ │
│  │  Hook      │  │     ╭─────────────╮                        │ │
│  │  ─────     │  │     │   YOU       │                        │ │
│  │  Most…     │  │     │  (avatar)   │                        │ │
│  │  ▍         │  │     ╰─────────────╯                        │ │
│  │            │  │                                            │ │
│  │  Story     │  │     ┌────────────────────────┐            │ │
│  │  ─────     │  │     │ words → sentences → … │            │ │
│  │  In ling…  │  │     │       (Modal aid)      │            │ │
│  │            │  │     └────────────────────────┘            │ │
│  │  Wonder    │  │                                            │ │
│  │  ──────    │  │  ┌─────────────────────────────────────┐  │ │
│  │  What if…  │  │  │  ⊕ Generate  ⇪ Import  ▦ Compose  ✎ │  │ │
│  │            │  │  │                              Refine │  │ │
│  │  Action    │  │  └─────────────────────────────────────┘  │ │
│  │  ──────    │  │       (four primitives, always visible)   │ │
│  │  Today,…   │  │                                            │ │
│  │            │  │                                            │ │
│  └────────────┘  └────────────────────────────────────────────┘ │
│                                                                  │
│  ●━━━━━━━━━●━━━━━●━━━━━━━●━━━━━━━ 0:00 ──────── 7:00            │
│   Hook    Story  Wonder  Action  Wisdom    (timeline)            │
└──────────────────────────────────────────────────────────────────┘
```

### The four primitives

| Primitive | What it does | When you reach for it |
|---|---|---|
| **⊕ Generate** | Cloud diffusion (~$0.001/image) creates a new aid from a text prompt. | "I need a diagram of the water cycle." |
| **⇪ Import** | Drop in an SVG, image, video, or URL. Snaps to the canvas grid. | "I already have a diagram from class." |
| **▦ Compose** | Drag-arrange existing nodes. Connect with arrows. Group, layer, animate. | "I want this node to appear when I say 'sentences'." |
| **✎ Refine** | Edit any aid in place: text, color, position, motion. | "Make that arrow bolder." |

These four are always visible at the bottom of the canvas. No mode toggle. Tap a primitive, the canvas accepts that kind of input. Tap another, the canvas accepts that kind. Switching is instant.

### Script ↔ Canvas binding

The left column is the lesson script — five sections (Hook, Story, Wonder, Action, Wisdom), the same shape as every Daily Lesson. The script is *time*, the canvas is *space*. Drag a Modal aid onto a script section → it appears when the avatar speaks that section. Drag it onto the timeline directly → finer control, frame-level.

### Avatar capture (one time, ever)

First time in Studio:

```
┌──────────────────────────────────────────────────────────────┐
│   Record your avatar                                          │
│                                                               │
│   We need 5 short clips. Same lighting, same wardrobe,        │
│   one session. Total: ~3 minutes.                             │
│                                                               │
│       ╭──────────╮ ╭──────────╮ ╭──────────╮                 │
│       │ neutral  │ │   left   │ │  right   │                 │
│       │   ▓▓▓    │ │          │ │          │                 │
│       ╰──────────╯ ╰──────────╯ ╰──────────╯                 │
│       ╭──────────╮ ╭──────────╮                              │
│       │   down   │ │ lean in  │                              │
│       │          │ │          │                              │
│       ╰──────────╯ ╰──────────╯                              │
│                                                               │
│   [Start recording]              Already done? [Re-capture]   │
└──────────────────────────────────────────────────────────────┘
```

Five pose channels (neutral, left, right, down, lean_in) — exactly what the product spec §14 specifies for Kelly herself. Same bar applies to creators: validated at 100% on a large screen, three-place backup.

After capture, you never see this screen again unless you tap "Re-capture."

### Publish

```
┌──────────────────────────────────────────────────────────────┐
│   Publish "The bottleneck"                                    │
│                                                               │
│   URL:  yourname.kellyai.com/the-bottleneck                   │
│        (or use a custom domain — paid tier)                   │
│                                                               │
│   ☑ Free tier: 1 published lesson, watermarked                │
│   ☐ Paid ($29/mo): unlimited, no watermark, custom domain     │
│                                                               │
│                                          [ Publish ]          │
└──────────────────────────────────────────────────────────────┘
```

One lesson free, watermarked, forever. Paid unlocks unlimited + custom domain. Same shape as the financial model — break-even at 3 paying creators.

---

## Failure modes (where the design has to hold)

| Failure | What the user sees |
|---|---|
| **Kelly takes >3s to arrive** | "Kelly is arriving…" persists. After 8s: "Kelly is having a slow morning. [Retry] or [Read the lesson]" — fallback to a static text/diagram version of today's lesson, same five sections. |
| **WebRTC blocked by network** | Same fallback to static lesson. The daily lesson is never gated on streaming. |
| **User has no mic permission** | Mic button shows `🚫`. Touching it offers a typed-input field. Lesson works without voice. |
| **Local model fails Bar C (soul)** | Per Runbook D: Kelly falls back to a tighter, more scripted persona. The lesson still ships. |
| **User's language not yet covered** | Track picker shows the 25 supported languages plus "Help us translate" for the rest. |

---

## What this design is NOT

- Not a Zoom call with an AI. Kelly is not a face on a tile.
- Not a slide deck. The Modal plane is not slides advancing — it's a single living diorama.
- Not a chatbot. Voice and text are interrupts to a structured lesson, not the lesson itself.
- Not a course platform. There is no syllabus, no module tree, no "next up." Today's lesson is the unit.
- Not gamified. No XP, no streaks, no badges, no notifications, no email. Ever.

---

## Open design questions (flag for founder)

1. **Calendar dots in top bar — show how many?** 5 feels right (3 past, today, 1 ahead-but-locked). 7 feels noisy. Validate with first 5 outside viewers (per ops-log Bar E).
2. **Modal plane on mobile** — does it stack below Kelly, or does Kelly shrink to a corner badge? Six-device matrix test in week 12 (Bar D).
3. **Studio's four primitives — order on the bar.** Generate-first reads as "AI tool." Compose-first reads as "design tool." Recommendation: Compose-first, because the primitive that gets used most often per session belongs leftmost.
4. **End state's "Close the tab" — does it actually close the tab?** Browser security may block `window.close()` on tabs the user didn't open via script. Fallback: navigate to `about:blank` with the same copy.
