# Clamp Jaw Pad — Design

Date: 2026-05-17
Status: Approved (design); spec under user review

## What this is

A replacement slide-on pad for the head of a parallel bar clamp. The pad
caps the flat metal jaw so the steel never touches the workpiece. The
original is a slightly compliant red plastic part that has worn / split;
this reproduces its geometry as a parametric build123d part for the
Bambu Lab A1 in SUNLU PLA+.

Pure-parametric project. No third-party STL, no `downloaded/`.

## Function and topology

Slide-on **end cap** with a C cross-section:

- One short end is a **solid closed wall** (the rounded "D"); the metal
  jaw bottoms out against it.
- The opposite short end is an **open mouth**; the flat jaw slides in
  along the slide axis.
- The cross-section perpendicular to the slide axis is a **C**: a back
  wall (spine) + two side walls + two lips that curl inward over the
  channel. The lips retain the pad on the jaw's front face so it does
  not fall off.
- The lips are **asymmetric**: one overhangs 2.0 mm, the other 3.7 mm
  (reproduced as measured).
- The two short ends of the outer body are **stadium-rounded**, not
  square.

## Coordinate system

- **X** — slide axis (`OUTER_LENGTH`, 38.67 mm). Closed wall at the X
  minimum, open mouth at the X maximum.
- **Y** — across (`OUTER_WIDTH`, 27.0 mm). Lips sit at the Y extremes
  and overhang inward.
- **Z** — back-to-front (`OUTER_THICKNESS`, 10.0 mm). Back wall at Z
  minimum; channel opens toward +Z; lips cap the +Z side.

## Parameters (mm)

| Param | Value | Meaning |
|---|---|---|
| `OUTER_LENGTH` | 38.67 | Slide axis, closed end → mouth |
| `OUTER_WIDTH` | 26.0 | Across the lips (= `CHANNEL_WIDTH` + 2 × 2.5 wrap) |
| `OUTER_THICKNESS` | 11.5 | Back wall 3.5 + channel 4 + lip 4 |
| `CHANNEL_WIDTH` | 21.0 | Jaw plate width |
| `CHANNEL_HEIGHT` | 4.0 | Slot the jaw sits in (jaw thickness) |
| `BACK_WALL` | 3.5 | Solid plate between channel floor and workpiece face |
| `LIP_THICKNESS` | 4.0 | Z thickness of each retaining lip |
| `LIP_OVERHANG_A` | 2.0 | One lip's inward reach over the channel |
| `LIP_OVERHANG_B` | 3.7 | Other lip's inward reach |
| `MOUTH_OVERSHOOT` | 2.0 | Pocket extends past the +X mouth for a clean opening |
| `WRAP_WALL` | 2.5 | Derived `(OUTER_WIDTH − CHANNEL_WIDTH) / 2`; constant solid wall around the D and along the sides |
| `FIT_CLEARANCE` | 0.0 | Added to channel W/H for slide fit; tune after test print |

Derived: the mouth opening between lips ≈ `CHANNEL_WIDTH` −
`LIP_OVERHANG_A` − `LIP_OVERHANG_B` ≈ 15.3 mm. The jaw cavity runs
under a solid front cap at the D end and opens to the front (between
the lips) from the straight section to the mouth.

## Geometry construction (boolean method)

Matches the existing `projects/breaker-panel-clip/3d/block.py` style.

1. **Outer body**: a stadium-footprint prism — `OUTER_LENGTH` ×
   `OUTER_WIDTH` × `OUTER_THICKNESS`, short (X) ends rounded to
   `OUTER_WIDTH / 2` via `RectangleRounded` extruded in Z.
2. **Channel pocket**: a *stadium* `(CHANNEL_WIDTH + FIT_CLEARANCE)`
   wide × `(CHANNEL_HEIGHT + FIT_CLEARANCE)` tall, subtracted. Its
   closed end is a semicircle **concentric with the outer D**, leaving
   a constant `WRAP_WALL` of solid all the way around the back — this
   fills the back corners a rectangular pocket would breach. Floored by
   `BACK_WALL`; sized so the open end overshoots the +X mouth by
   `MOUTH_OVERSHOOT`.
3. **Mouth window**: subtract the central opening on the +Z face
   between the two lips (width = channel − overhangs), starting at the
   straight section (the D-arc centre) so the rounded D end keeps a
   solid front cap like the original, running out past the mouth.

Asymmetry handled by offsetting the window in Y so one lip reads 2.0 mm
and the other 3.7 mm.

**Iteration note (2026-05-18):** the first render used a rectangular
pocket; the rounded outer D tapers narrower than the 21 mm pocket near
the back, so the pocket breached the shell and the back corners were
hollow. Fixed by making the pocket a stadium with a closed end
concentric to the outer D (constant `WRAP_WALL`).

**Iteration note (2026-05-18, fit review):** D/side wrap of 3.0 mm read
too thick and the 2.0 mm contact plate too thin under clamp load.
`OUTER_WIDTH` 27→26 (wrap → 2.5 mm, matching the original
21-channel/2.5-wall measurement); `BACK_WALL` 2.0→3.5 and
`OUTER_THICKNESS` 10→11.5 (extra material added on the contact side
only — channel and lip positions unchanged, still fits the jaw).

## Print orientation review (conventions §Print-readiness)

- **Chosen orientation**: stand the part on its **closed D end** —
  slide axis (X) vertical. The channel runs vertically; lips become
  vertical walls. **No bridges, no overhangs >45°, no supports.**
- Rejected: back-wall-down — the mouth window becomes a ~15 mm PLA
  bridge (sags badly) or needs interior supports that scar the
  jaw-contact surface.
- Bed adhesion: the 27 × 10 mm D-end footprint is small but adequate on
  the A1; a brim is acceptable if the first layer lifts.
- Documented in the project README print recipe.

## Material caveat

The original grips by friction/flex of a compliant plastic. PLA+ is
rigid and will not flex the same way. Reproducing the channel at
`FIT_CLEARANCE = 0.0` gives the tightest grip PLA can provide. After the
first test print, tune `FIT_CLEARANCE` up if it won't slide on, or note
in `print-log.md` if grip is insufficient. TPU is out of scope (only
SUNLU PLA+ black/white/grey/oak on hand).

## Deliverables

```
projects/clamp-jaw-pad/
├── README.md            # what it is, print recipe, grip caveat
├── 3d/
│   ├── requirements.txt # build123d
│   ├── pad.py           # the generator (Parameters / Geometry / Export)
│   └── build_all.py     # standard regenerator (copied pattern)
└── print-log.md         # per-print diary, starts empty
tests/test_clamp_jaw_pad.py   # smoke + geometry-invariant test
```

## Testing

Follow `tests/test_breaker_panel_clip.py`:

- `test_script_exists` — generator file present.
- `test_script_produces_valid_stl` — runs `pad.py`, asserts exit 0 and
  a non-trivial STL (> 5 KB).
- `test_stl_geometry_invariants` — `trimesh` load: watertight, single
  body, bounding box within ±50 % of the nominal
  38.67 × 27 × 10 mm so a regression (empty boolean, runaway dimension)
  fails loudly.

## Out of scope

- TPU / flexible-filament reprint.
- Modeling the clamp body beyond the jaw it caps.
- Multiple sizes / a parametric family for other clamps (single fit).
