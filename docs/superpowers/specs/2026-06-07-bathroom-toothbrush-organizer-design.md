# Bathroom toothbrush organizer — design

**Date:** 2026-06-07
**Status:** approved (brainstormed), pending implementation
**Project location:** `projects/bathroom-toothbrush-organizer/`
**Trigger:** wife liked a MakerWorld bathroom organizer / toothbrush holder
(model 1192955) but wants the scalloped exterior wall of a MakerWorld q-tip
holder (model 2074092). Rather than mod third-party STLs, rebuild parametrically:
a family toothbrush holder with the scalloped wall styled in, plus a q-tip stash.

## What it is

A single scalloped-wall organizer (oak wood PLA+) for a family bathroom counter.
Holds the household's manual toothbrushes and toothpaste in an open, draining wet
zone, with a walled-off, covered q-tip cubby that stays dry. Two printed pieces:
the body and a lift-off lid for the q-tip cubby.

The two source models are **not** copied byte-for-byte (MakerWorld blocks
automated fetch, and the repo's IP posture keeps third-party bytes local-only).
The toothbrush-holder layout is reconstructed from the functional requirements
gathered in brainstorming; the scalloped wall is the borrowed styling idea.

## Contents it holds (settled in brainstorming)

- **3 manual toothbrushes** — 1 adult + 2 kids. The adult uses an electric that
  lives on its own charger, so no electric well is included.
- **Toothpaste** — one shared pocket sized for a full tube; the kids' travel-size
  tube sits in the same pocket. No dedicated travel-tube slot.
- **Q-tips** — their own covered, dry compartment.

## Form

- **Footprint:** rounded-rectangle, **165 W × 70 D mm**, ~18 mm corner radius.
  "Medium" size per brainstorming. Fits the A1's 256 mm bed, prints in one piece.
- **Height:** ~80 mm.
- **Outer wall:** **concave vertical scallops** — grooves scooped into the wall,
  running floor-to-rim, with sharp-ish ridges between. This is the borrowed look.
- **Two zones split by a solid full-height divider wall:**
  - **Wet zone** (left, ~110 mm): 3 brush bores + toothpaste pocket, drains
    through the floor.
  - **Dry zone** (right, ~50 mm): q-tip cubby with its own raised solid floor and
    a lift-off lid.

## Internal layout & dimensions

**Wet zone:**

- **3 brush bores**, Ø16 mm, in a row across the back. Ø16 lets a manual brush
  drop in and rest by its wider thumb-rest/head; fits both adult and kids' brushes.
  Each bore stops ~6 mm above the floor with a **Ø4 mm drain hole** through the
  floor at its bottom.
- **Toothpaste pocket** at the front: rounded rectangle ~50 × 26 mm, open top,
  with a Ø4 mm drain hole. One shared pocket for whatever tube is in rotation.

**Dry zone:**

- **Q-tip cubby:** ~Ø42 mm round well, interior ~70 mm deep. Q-tips (~75 mm)
  stand upright with tops just proud of the rim; the lid covers them.
- **Solid floor raised ~3 mm** above the wet floor, no drain hole — stays dry even
  if water sheets across.
- **Raised rim lip** around the well for the lid to register on.

**Lid:**

- Lift-off cap (not hinged). A disc with a short downward skirt that slips over the
  rim lip, ~0.4 mm clearance. Printed flat-top-down, no supports.

## Drainage / standing

Flat bottom with vertical drain holes — water runs straight through onto the
counter/tray below (the chosen drainage approach). **No standoff feet in v1:**
feet or a recessed base would force a wide first-layer bridge across the bottom.
If lifting it off the counter is wanted after a test print, the clean follow-on is
a separate scalloped drip tray it nests into — not bottom feet.

## Design decisions and reasoning

### Parametric rebuild, not an STL mod (chosen in brainstorming)

Considered: hybrid graft of scallops onto a downloaded toothbrush-holder STL vs.
full parametric rebuild. Picked rebuild because the scallop *is* the outer wall —
core geometry, not a boltable add-on feature — so grafting buys nothing over
modeling it, and rebuild keeps zero third-party bytes in the repo (IP posture)
while staying fully editable.

### Q-tip cubby on the end, walled off and covered

Toothbrushes drip; q-tips must stay dry. Putting the cubby on one **end** keeps the
wet/dry divider short and the q-tips farthest from the dripping brushes. The cubby
gets its own raised solid floor (no drain hole) and a lift-off lid so neither
sheeting water nor bathroom splashes reach the q-tips.

### Vertical bores, no raised deck (printability-driven)

The classic "holes in a raised top deck" toothbrush holder bridges across the
cavity opening — a >4 mm PLA bridge the repo's print-readiness rules call out.
Instead the brush sockets are **vertical bores** in a mostly-solid (infill-filled)
body: every hole is a vertical feature that prints clean upright with no support,
and the body is modeled as outer shell minus pockets so the slicer fills it with
~15% infill (light and fast).

### Lift-off lid, not a print-in-place hinge

Simpler and reliable for v1, and prints flat-top-down with no supports. A hinged
flip-top is a possible v2 feel upgrade.

## Scope: what's in vs out

In:

- 3 manual brush bores, 1 toothpaste pocket, 1 covered q-tip cubby
- Scalloped (concave vertical) outer wall
- Floor drain holes for the wet zone

Out (deliberate cuts):

- Electric toothbrush well (electric lives on its charger)
- Standoff feet / integrated drip tray (deferred to a possible separate tray)
- Dedicated travel-tube slot (shared toothpaste pocket covers it)
- Hinged lid (lift-off for v1)

## Print recipe

- **Orientation:** body upright (as it sits), lid flat-top-down.
- **Overhangs/bridges:** none — every feature is vertical or open at the top.
- **Supports:** none for either piece.
- **Filament:** Oak Wood PLA+ (manual profile select — no RFID).
- **Settings:** 0.2 mm layers, ~15% gyroid infill, 3 walls so the scallop grooves
  stay strong where they cut into the wall.

## Files (matches repo parametric pattern)

```
projects/bathroom-toothbrush-organizer/
├── README.md
├── print-log.md
└── 3d/
    ├── requirements.txt
    ├── organizer.py     # body
    ├── qtip_lid.py      # lift-off lid
    └── build_all.py
```

Plus smoke tests `tests/test_bathroom_toothbrush_organizer.py` covering both
generators (run the script, assert a non-trivial STL), matching the existing
`tests/` pattern.

## Open assumptions to verify against the real models

- Layout of the source toothbrush holder is reconstructed from requirements, not
  copied — confirm the brush/toothpaste arrangement reads right once printed.
- "Concave vertical scallops" approximates the q-tip holder's wall; groove count,
  depth, and ridge sharpness are tunable parameters once a screenshot or a test
  print is available.
- Ø16 brush bores and the shared toothpaste pocket sizing assume standard manual
  brushes — verify with a caliper on the actual brushes before committing the size.
