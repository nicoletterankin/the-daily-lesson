# HELD Pet Deck — QR Print Files: Where Everything Is

*Lesson of the Day, PBC · held.press · verified 2026-07-21*

This document is the single findable answer to "where are the pet deck QR print files?"
for any operator, human or AI. Machine-readable version: [`pet-deck-qr-manifest.json`](./pet-deck-qr-manifest.json).

## TL;DR

**All 104 pet deck print files (52 fronts + 52 backs) are already in R2** and were
machine-verified end-to-end on 2026-07-21. Nothing is missing. The old
"COLLIDING TILES" flag in `state/shortcodes.json` is stale — the backs now in R2
carry regenerated, collision-free QR codes.

## Where the files live

| What | Location |
|---|---|
| R2 bucket | `heldpress` (Cloudflare) |
| Public CDN | `https://media.held.press/cards/` (alt: `https://pub-f7e3656e37ec4b4baa2758013c88f0cc.r2.dev/cards/`) |
| Naming | `pet-{suit}{n}-front.jpg` and `pet-{suit}{n}-back.jpg` · suit ∈ ground, feel, remember, tend · n ∈ 1–13 |
| Example | `https://media.held.press/cards/pet-ground1-back.jpg` |
| QR payload on each back | `https://held.press/p/p{suit-letter}{n}` (letters: g/f/r/t) |
| Shortcode registry | `state/shortcodes.json` in the `heldpress` bucket (canonical); repo copy: [`shortcodes.json`](./shortcodes.json) |

## Verification results (2026-07-21, this repo's `verify` run)

Per HELD values line #5 — machine-verify every printed QR at 100% and 50% scale
before print files ship:

- **52/52 QR codes decode correctly** with zbar at **both 100% and 50% scale**,
  each to its exact expected shortlink `https://held.press/p/p{g|f|r|t}{n}`.
  No collisions, no wrong payloads.
- **52/52 shortlinks** return 302 to the correct room `https://held.press/pet/{suit}/{n}/`.
- **52/52 room pages** return HTTP 200.
- **104/104 image files** present in R2 (zero missing in full census).
- SHA-256 checksums for every file are in the manifest JSON — compare before
  sending anything to a printer to be sure you have the verified bytes.

Note: OpenCV's built-in `QRCodeDetector` fails 11 of the backs at 50% scale;
zbar (the reference decoder, and what real phone scanners exceed) reads all 52
cleanly. Use zbar for gate checks.

## What is still open

1. **Physical proof scan.** `printed` is still `false` in the registry. The QR
   gate covers digital verification; a physical scan of printed proofs
   (like grief's g8/r6 note) remains a Nicolette-side step before/after press.
2. **Registry sync.** The canonical `state/shortcodes.json` in R2 still says
   `"COLLIDING TILES — regenerate backs against /p/p* before print"`. That is
   stale. The corrected registry is committed here as `shortcodes.json`; the
   next `held-kelly-batch` run (which holds the R2 keys) should push it:
   follow the lock ritual (take lock → **fetch state tarball first** → work →
   push → release), replace `shortcodes.json` in state, and
   `r2_put(shortcodes.json, 'state/shortcodes.json')`. This session had no R2
   write credentials (they live with the scheduled tasks), so the R2-side
   registry was not modified.

## How to re-verify (any AI, any session, no credentials needed)

```bash
# census + download (all public reads)
for suit in ground feel remember tend; do for n in $(seq 1 13); do
  curl -sfO "https://media.held.press/cards/pet-$suit$n-back.jpg"; done; done
# decode with zbar at 100% and 50%, compare to https://held.press/p/p{g,f,r,t}{n}
# full script: see verify_qr.py in this directory
python3 verify_qr.py .
```

## Related context

- Operations manual: `held-press` skill → `references/HELD-OPERATIONS.md`
- Print gates: `references/DECK-PRESS.md`
- Grief deck QR status: verified, printed (g8, r6 awaiting physical scan)
- SOUL deck: shortcodes reserved under `/p/s…`, suits TBD
