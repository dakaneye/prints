# Desk drawer Gridfinity organizer

Custom-fit Gridfinity baseplate + downloaded bins for the top desk drawer.
Gridfinity is Zack Freedman's modular grid storage system — every bin and
baseplate is sized in 42 × 42 mm cells with 7 mm height units (1U = 7 mm).

## Drawer

| Dimension | Value | Status |
|---|---|---|
| Width  | 358 mm | **MEASURE TO CONFIRM** — guessed from "35.8" |
| Depth  | 340 mm | **MEASURE TO CONFIRM** — guessed from "34" |
| Interior height | TBD | **MEASURE** — drives max bin height (3U=21 mm, 6U=42 mm, 9U=63 mm, 12U=84 mm) |

8 × 8 cells fits with ~22 mm width slack and ~4 mm depth slack. Slack goes
to the back as an empty filler strip (or a custom 0.5×8 baseplate later).

## Items being organized

From the photo as of 2026-05-02:

- Guitar strap (rolled, leather) — bulky, deep bin
- Wood guitar pick case + round pick dish
- Guitar capo
- Grip strength trainers (3, stacked)
- Checkbook
- Felix Gray glasses case (~165 × 60 mm)
- Pens + markers (Sharpies, dry-erase)
- Business cards
- Pocket notebook (Martindale's)
- Duct-taped deck of playing cards
- Keys

## Zone layout (proposed)

Group items by use, not by shape — keeps related stuff together when the
drawer is opened.

| Zone | Cells | Contents |
|---|---|---|
| Guitar (front-left) | 4 × 4 | Strap (3×3 deep bin), pick case (1×1), pick dish (1×1), capo (1×2) |
| Office (front-right) | 4 × 2 | Pens (1×2 vertical), markers (1×2 vertical), business cards (1×2), notebook (1×2) |
| Personal (back-left) | 4 × 2 | Glasses case (4×2 long bin) |
| Misc (back-right) | 4 × 4 | Checkbook (4×2), grip trainers (2×2 deep), playing cards (1×2), keys (1×2) |

Adjust as you print and try things. Bin sizes are downloaded individually
(see `downloaded/SOURCES.md`); only the baseplate is custom.

## Print recipe

Bambu A1 with default `0.20mm Standard @BBL A1` profile, filament set
manually to **SUNLU PLA+ 2.0** (white or grey both work — grey hides
print lines better in a drawer).

| Setting | Value |
|---|---|
| Layer height | 0.2 mm |
| Walls | 3 (baseplate), 2 (bins) |
| Infill | 15% gyroid |
| Supports | None |
| Brim | None (textured PEI) |

A1 bed is 256 × 256 mm. An 8×8 baseplate doesn't fit in one shot — the
generator splits it into A1-printable tiles. Default split: **two 6×4 +
two 2×4** tiles (two unique STLs, print 2 copies of each).

Actual STL bounds (verified from generated STLs):

| STL | Footprint | Height | Volume | Print copies |
|---|---|---|---|---|
| `baseplate_6x4.stl` | 251.5 × 167.5 mm | 4.75 mm | 35 cm³ | 2 |
| `baseplate_2x4.stl` | 83.5 × 167.5 mm | 4.75 mm | 12 cm³ | 2 |
| `bin_1x2x6U.stl` | 41.5 × 83.5 mm | 45.6 mm | 32 cm³ | 2 |
| `bin_2x2x6U.stl` | 83.5 × 83.5 mm | 45.6 mm | 58 cm³ | 2 |
| `bin_2x2x9U.stl` | 83.5 × 83.5 mm | 66.6 mm | 64 cm³ | 2 |
| `bin_4x2x6U.stl` | 167.5 × 83.5 mm | 45.6 mm | 108 cm³ | 2 |
| `bin_3x3x12U.stl` | 125.5 × 125.5 mm | 87.6 mm | 140 cm³ | 1 |

Bin volumes are walls + floor only (the cavity is air). Total filament for
the full set: ~620 cm³ (~770 g of PLA+) at 15% infill.

> Bin heights = `7 × U + 3.6 mm` (the 3.6 mm is the stacking lip — only
> consumes Z when bins aren't stacked).

## Files

- `3d/baseplate.py` — parametric baseplate tile generator
- `3d/bins.py` — generic empty bins (starter set; specialized inserts come from `downloaded/`)
- `3d/build_all.py` — regenerates every part script
- `3d/requirements.txt` — `build123d` + `gridfinity-build123d`
- `downloaded/SOURCES.md` — purpose-built bins pulled from MakerWorld / Printables
- `print-log.md` — per-print diary

## Setup (per-project venv)

```bash
python3.13 -m venv 3d/.venv
# The library is installed from a git URL. If you have a global
# url.git@github.com:.insteadof rewrite (SSH+YubiKey), bypass it for
# this command:
GIT_CONFIG_GLOBAL=/dev/null 3d/.venv/bin/pip install -r 3d/requirements.txt

3d/.venv/bin/python 3d/baseplate.py        # baseplate tiles
3d/.venv/bin/python 3d/bins.py             # bin starter set
3d/.venv/bin/python 3d/build_all.py        # everything
```

Generated STLs land in `3d/out/`:

- `baseplate_<cols>x<rows>.stl` — one per unique tile size
- `bin_<cols>x<rows>x<height>U.stl` — one per unique bin size

Print quantities are printed by each script — match them in Bambu Studio
via Right-click → Set quantity.

## Importing into Bambu Studio

The A1 doesn't auto-orient like the X1. For each STL:

1. **File → Import → Import 3MF/STL** (drag-drop also works). `Open
   Project` only handles `.3mf` bundles, so don't use it.
2. Filament: select **"SUNLU PLA+ 2.0"** manually (no RFID on the spool).
3. Profile: `0.20mm Standard @BBL A1`. No brim needed on the textured PEI plate.
4. Lay it flat on the bed (the script exports with the cell openings
   already pointing up — no rotation needed).
5. Right-click the part → **Set quantity → 2** (per the table above), then
   **Auto Arrange Plate**. Each 6×4 takes a full plate alone; the two
   2×4s should fit together on one plate.
6. Slice → preview to confirm bin pockets aren't bridged shut → Print.

Suggested sequence: **2×4 first** as a single test print (~1 hr) — let
you verify a downloaded bin actually seats before committing to the
larger 6×4 prints (~3 hrs each).

## Tweaking the parts

**Baseplate tiles** — edit `3d/baseplate.py`:

- `TILES` — list of `(cols, rows, qty)`. Default `[(6, 4, 2), (2, 4, 2)]`.
  Add a row for any additional tile size; one STL per unique `(cols, rows)`.
- `CELL_PITCH`, `SLAB_HEIGHT`, `SLAB_INSET` — Gridfinity spec constants.
  Don't touch unless you know what you're doing — bin compatibility breaks.

**Bins** — edit `3d/bins.py`:

- `BINS` — list of `(cols, rows, height_U, qty)` where 1U = 7 mm. Add or
  remove rows as the layout evolves.

The current bin generator produces blank bins (single open cavity, no
dividers). For purpose-shaped inserts (drilled pen pockets, glasses
cradles, guitar pick organizers), use community designs from MakerWorld
and log in `downloaded/SOURCES.md` — that ecosystem is far better-tuned
than anything you'd hand-roll.

The baseplate generator produces the "Light" profile — no magnet holes,
no screw holes. Most desk-drawer use cases want this. For magnet
anchoring, you'd swap to kennetek's OpenSCAD generator or extend
`baseplate.py` to subtract magnet pockets after the bin-foot subtract.
