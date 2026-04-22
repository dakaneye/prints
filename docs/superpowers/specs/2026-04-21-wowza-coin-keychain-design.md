# Wowza coin keychain — design

**Date:** 2026-04-21
**Status:** approved, implemented as `projects/wowza-keychain/3d/keychain.py`

## What it is

A small round 3D-printed coin with the word "Wowza" raised on the front
and a hole near the top edge for a split ring. Chelsea (teacher) hands
them out to students who score 100% on assignments. Students who earn
multiple should be able to **stack** them flush, since collecting is part
of the appeal.

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

### Stacking — rim taller than the raised text
Raised text + flat bottom = wobbly stacks. Resolved by adding a
`RIM_WIDTH = 2.0`, `RIM_HEIGHT = 1.5` ring around the perimeter. Stacked
coins rest rim-to-bottom; the text floats in the 0.3 mm gap between coin A's
top face and coin B's bottom. The script raises `ValueError` if anyone tweaks
the parameters such that `RIM_HEIGHT <= TEXT_RAISE`, so stackability can't
silently break.

### Hole — 5 mm, 5 mm from edge, in the depressed inner area
Standard split-ring fit. Located in the depressed face, not through the
rim, so the coin's silhouette stays clean.

## Final geometry

| Parameter | Value | Notes |
|---|---|---|
| `COIN_DIAM` | 45 mm | silver-dollar size |
| `COIN_THICKNESS` | 4 mm | base disk |
| `RIM_WIDTH` | 2 mm | radial width of the rim ring |
| `RIM_HEIGHT` | 1.5 mm | rim above coin face — must exceed text raise |
| `TEXT_RAISE` | 1.2 mm | raised text height |
| `TEXT_MARGIN` | 4 mm | clearance from rim's inner edge to text |
| `HOLE_DIAM` | 5 mm | split-ring fit |
| `HOLE_FROM_EDGE` | 5 mm | hole centre to coin edge |
| Total height | 5.5 mm | |

(Back face is blank in v1.)
