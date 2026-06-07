# Wowza coin keychain — design

**Date:** 2026-04-21 (v1), revised 2026-04-25 (v2)
**Status:** approved, implemented as `projects/wowza-keychain/3d/keychain.py`

## What it is

A small round 3D-printed coin with the word "Wowza" raised on the front
and a hole near the top edge for a split ring. Chelsea (teacher) hands
them out to students who score 100% on assignments.

V1 was 45 mm with a stacking rim. After printing one, Chelsea asked for
quarter-sized and no rim — v2 drops both. Coins no longer stack flush;
that requirement was waived in favour of a smaller, simpler shape.

## Origin

Originally a stamp idea from Notion. PLA+ stamps don't work (too rigid,
non-porous), and we have no TPU or silicone on hand, so we pivoted to a
keychain — a clean fit for what's already in the cabinet.

## Design decisions and the reasoning

### Use case — student rewards (B), not personal keychain or display piece
Drives: small, durable, batch-printable, generic ("Wowza" is the badge),
no per-student personalisation.

### Form factor — coin (round) with raised text on the face
The earlier exploration tried a cookie-cutter word silhouette with a
flange for the keyring. The user's wife clarified she wanted a coin
with raised print on it instead. Coin geometry is simpler, prints
support-free, and avoids the thin-feature fragility of a word silhouette.

### Font — Arial Rounded MT Bold, auto-sized
"Bold rounded" was the user's stated direction. `Arial Rounded MT Bold`
is the cleanest macOS option for that aesthetic. Text is auto-sized to
the available coin face from a `TEXT_MARGIN` parameter rather than
hard-coded — resizing the coin no longer requires re-tuning the font size.

### Stacking (v1 only — removed in v2)
v1 added a 2 mm wide, 1.5 mm tall rim around the perimeter so stacked
coins would rest rim-to-bottom with the text floating in the gap. After
printing one, Chelsea asked for the rim removed — accepting the loss of
flush stacking in exchange for a cleaner coin face.

### Hole — 5 mm, 5 mm from edge
Standard split-ring fit. Sits in the upper portion of the coin face;
text shifts down to clear it.

## Final geometry (v2)

| Parameter | Value | Notes |
|---|---|---|
| `COIN_DIAM` | 24.5 mm | US-quarter sized |
| `COIN_THICKNESS` | 4 mm | base disk |
| `TEXT_RAISE` | 1 mm | raised text height |
| `TEXT_MARGIN` | 2 mm | clearance from coin edge to text |
| `TEXT_Y_OFFSET` | -3.5 mm | shifts text into the lower half, clear of the hole |
| `HOLE_DIAM` | 5 mm | split-ring fit |
| `HOLE_FROM_EDGE` | 5 mm | hole centre to coin edge |
| Total height | 5 mm | |

(Back face is blank.)
