# Workbench drawer Gridfinity organizer

Custom-fit Gridfinity baseplates + bins for the Craftsman rolling toolbox
under the garage workbench pegboard. Same parametric setup as
`desk-drawer-gridfinity` — just retuned for tool storage instead of
office bits.

Gridfinity is Zack Freedman's modular grid storage system — every bin
and baseplate is sized in 42 × 42 mm cells with 7 mm height units
(1U = 7 mm).

## Drawers

The Craftsman cabinet has three drawers of identical width / depth
footprint and varying interior height. The **top drawer has a fixed
divider 11" (~279 mm) from the left wall** — it cannot be removed, so
that drawer is laid out as two independent compartments. Middle and
bottom drawers are open (no divider) and use a continuous grid.

| Drawer | Width | Depth | Interior height | Layout | Status |
|---|---|---|---|---|---|
| Top    | 580 mm (~22.8") | 410 mm (~16.1") | 50 mm (~2") | 2 × (6 × 9) compartments (fixed divider @ 279 mm) | STLs ready |
| Middle | 565 mm (~22.2") | 410 mm | 70 mm (~2.75") | 13 × 9 continuous | STLs ready |
| Bottom | 565 mm | 410 mm | 150 mm (~5.9") | 13 × 9 continuous | STLs ready |

**Top drawer (divider-split):** each compartment is ~6 × 9 cells. A 6 × 9
won't print as one tile (9 rows = 378 mm > A1 bed), so each compartment
splits depth-wise into a **back 5-deep band + front 4-deep band**. The
back 5-deep band is further split width-wise into two **3 × 5** tiles
because a single 6 × 5 (251.5 × 209.5 mm) sits right at the A1's edge
exclusion zone and fails mid-print (confirmed by an overnight spaghetti).
Per compartment: 2× 3×5 (back) + 1× 6×4 (front). Top drawer total:
**4× 3×5 + 2× 6×4**. Width slack: ~27 mm in the left compartment,
~44 mm in the right — see the filler note below.

**Middle + bottom drawers (continuous):** 13 × 9 grid, split 5+4+4 cols ×
5+4 rows into 1× 5×5 + 1× 5×4 + 2× 4×5 + 2× 4×4 per drawer (5×4 and 4×5
are the same STL rotated 90°).

**18 tiles + 4 spacers total** across the three drawers: 4× 3×5,
2× 6×4, 2× 5×5, 6× 5×4 (covers the 4×5 positions rotated), 4× 4×4;
plus 2× `spacer_left` + 2× `spacer_right` (top drawer only).

Bin height ceiling by drawer:
- Top (50 mm interior): max bin height 6U (42 mm) — leaves room for the
  stacking lip
- Middle (70 mm): max 9U (63 mm)
- Bottom (150 mm): max 18U (126 mm); 12U (84 mm) is the practical default

## Per-drawer tile placement

Looking down into each open drawer. Keep "front" vs "back" consistent
across drawers so bins stay interchangeable (Gridfinity is symmetric, so
which depth band is front is arbitrary — just pick one and keep it).

### Top drawer — fixed divider at ~279 mm from left

Two independent compartments, each 6 × 9 cells. Back band is split
width-wise into two 3×5 tiles (A1 bed edge zones reject a single 6×5);
front band is one 6×4:

```
        LEFT compartment        │ divider │      RIGHT compartment
        (~279 mm, 6 cols)       │ (fixed) │      (~296 mm, 6 cols)
      ┌─────────┬──────────┐    │         │    ┌─────────┬──────────┐
back  │  3 × 5  │   3 × 5  │    │         │    │  3 × 5  │   3 × 5  │
      ├─────────┴──────────┤    │         │    ├─────────┴──────────┤
front │       6 × 4        │    │         │    │       6 × 4        │
      └────────────────────┘    │         │    └────────────────────┘
   ~25 mm width slack on the         ~45 mm width slack on the
   left edge of this compartment     right edge of this compartment
   (filled by spacer_left)            (filled by spacer_right)
```

Top drawer = 4× `baseplate_3x5.stl` + 2× `baseplate_6x4.stl`
+ 2× `spacer_left_25x205.stl` + 2× `spacer_right_45x205.stl`.

The spacers are flat 4.75 mm slabs that fill the perimeter slack so
the tiles don't slide sideways in the drawer. Each side strip is
split into two halves (~205 mm each) because the full 410 mm drawer
depth exceeds A1's edge-safe build area. See `3d/spacer.py` to tune
widths if your drawer measures differently.

### Middle + bottom drawers — continuous 13 × 9

13 cols = 5+4+4, 9 rows = 5+4. The two `4×5` positions use the
`baseplate_5x4.stl` STL rotated 90°.

```
            cols 0–4      cols 5–8     cols 9–12
            (5 wide)      (4 wide)     (4 wide)
          ┌────────────┬────────────┬────────────┐
back      │            │            │            │
(rows0–4, │    5×5     │    4×5     │    4×5     │
 5 deep)  │            │            │            │
          ├────────────┼────────────┼────────────┤
front     │    5×4     │    4×4     │    4×4     │
(rows5–8, │            │            │            │
 4 deep)  │            │            │            │
          └────────────┴────────────┴────────────┘
```

Each of the middle and bottom drawers =
1× `baseplate_5x5.stl` + 1× `baseplate_5x4.stl` +
2× `baseplate_5x4.stl` (rotated 90° for the 4×5 slots) +
2× `baseplate_4x4.stl`.

Push tiles into the back-left corner; perimeter slack
(~19–34 mm width, ~32 mm depth) pools on the front + right. Optional
filler strips can take up that slack — a filler generator will be
added to `3d/` once the actual gaps are measured.

## Items being organized (rough)

From the drawer photos as of 2026-05-11:

- Drill driver bit cases (DeWalt yellow, Craftsman black)
- Bit holders / driver bit strips (loose + on red bit bars)
- Hex key (Allen) sets — multiple
- Tape measures (3+)
- Stud finder
- Multi-blade utility knives
- Levels (mini torpedo + larger)
- Drywall + cement board screw boxes
- Thread seal tape rolls
- Step drill bits
- Sockets (loose + on rails)
- Headlamp
- Hole saws
- Small parts organizers (multiple)
- Tinned copper wire box
- Various screws/anchors in plastic cases

Zone layout will be drafted once drawer dimensions are locked in and the
first print confirms fit.

## Print recipe

Bambu A1 with default `0.20mm Standard @BBL A1` profile, filament set
manually to **SUNLU PLA+ 2.0, white** (matches the Multiboard wall
filament — single-color across both systems).

| Setting | Value |
|---|---|
| Layer height | 0.2 mm |
| Walls | 3 (baseplate), 2 (bins) |
| Infill | 15% gyroid |
| Supports | None |
| Brim | None (textured PEI) |

A1 bed is 256 × 256 mm nominally, but the edge exclusion zones (probe
+ carriage limits) reject tiles larger than ~5×5 cells in practice —
a 6×5 (251.5 × 209.5 mm) failed mid-print with corner-lift / spaghetti.
The generator emits one STL per unique `(cols, rows)` in `TILES`.

## Files

- `3d/baseplate.py` — parametric baseplate tile generator (5 unique tile sizes, 18 tiles total across 3 drawers)
- `3d/spacer.py` — flat perimeter spacers for top drawer (2 widths, 4 pieces)
- `3d/bins.py` — generic empty bins (starter set empty until inventory is set)
- `3d/build_all.py` — regenerates every part script
- `3d/requirements.txt` — `build123d` + `gridfinity-build123d`
- `downloaded/SOURCES.md` — purpose-built bins pulled from MakerWorld / Printables
- `print-log.md` — per-print diary

## Setup (per-project venv)

```bash
python3.13 -m venv 3d/.venv
GIT_CONFIG_GLOBAL=/dev/null 3d/.venv/bin/pip install -r 3d/requirements.txt

3d/.venv/bin/python 3d/baseplate.py        # baseplate tiles
3d/.venv/bin/python 3d/bins.py             # bin starter set (empty until populated)
3d/.venv/bin/python 3d/build_all.py        # everything
```

Generated STLs land in `3d/out/`.

## Importing into Bambu Studio

Same flow as `desk-drawer-gridfinity` — see that README for the full
walkthrough. Short version:

1. **File → Import → Import 3MF/STL** (drag-drop works too).
2. Filament: **"SUNLU PLA+ 2.0"** manually.
3. Profile: `0.20mm Standard @BBL A1`. No brim.
4. Lay flat — script exports cell openings up.
5. Slice → preview → print.

## Tweaking the parts

**Baseplate tiles** — edit `3d/baseplate.py`:

- `TILES` — list of `(cols, rows, qty)`. Each unique `(cols, rows)`
  becomes one STL; `qty` is the total copies to print across all
  drawers. Edit when adding/removing drawers or changing layout.
- `CELL_PITCH`, `SLAB_HEIGHT`, `SLAB_INSET` — Gridfinity spec constants.
  Leave alone — bin compatibility breaks if these drift.

**Bins** — edit `3d/bins.py`:

- `BINS` — list of `(cols, rows, height_U, qty)` where 1U = 7 mm.
  Empty until drawer inventory is mapped to cells.

The baseplate generator produces the "Light" profile — no magnet holes,
no screw holes. Tool drawers don't need magnet anchoring; the weight of
the bin contents and the drawer walls hold everything in place.
