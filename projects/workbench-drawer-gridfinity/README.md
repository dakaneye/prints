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
footprint and varying interior height (the top drawer is shallow for
small bits, the bottom drawer is deep for cases and chargers).

| Drawer | Width | Depth | Interior height | Cells (W × D) | Status |
|---|---|---|---|---|---|
| Top    | 580 mm (~22.8") | 410 mm (~16.1") | 50 mm (~2") | 13 × 9 | STLs ready |
| Middle | 565 mm (~22.2") | 410 mm | 70 mm (~2.75") | 13 × 9 | STLs ready |
| Bottom | 565 mm | 410 mm | 150 mm (~5.9") | 13 × 9 | STLs ready |

All three drawers share the same 13 × 9 cell grid (the 15 mm width difference
between top and middle/bottom is absorbed by the 4 mm clearance inset). Each
drawer is split into 6 tiles in a 3 × 2 layout (widths 5 + 4 + 4 cells,
heights 5 + 4 cells). Across all three drawers: 4 unique tile STLs, 18 tiles
to print total.

Bin height ceiling by drawer:
- Top (50 mm interior): max bin height 6U (42 mm) — leaves room for the
  stacking lip
- Middle (70 mm): max 9U (63 mm)
- Bottom (150 mm): max 18U (126 mm); 12U (84 mm) is the practical default

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

A1 bed is 256 × 256 mm. Single-piece tiles cap at ~6 × 6 cells. The
generator emits one STL per unique `(cols, rows)` in `TILES`.

## Files

- `3d/baseplate.py` — parametric baseplate tile generator (4 unique tile sizes, 18 tiles total across 3 drawers)
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
