"""Gridfinity baseplate tiles for the workbench rolling-cabinet drawers.

Mirrors `desk-drawer-gridfinity/3d/baseplate.py` — emits one STL per
unique tile in TILES. The three Craftsman cabinet drawers do NOT share
a layout:

- Top drawer has a FIXED divider 11" (~279 mm) from the left wall,
  splitting it into two ~6 x 9 cell compartments. Each compartment
  splits into a 6x5 + 6x4 tile pair (9 rows won't fit the A1 bed).
  Top drawer total: 2x 6x5 + 2x 6x4.
- Middle + bottom drawers are continuous 13 x 9 grids (interior
  ~565 W x 410 D mm). Each splits 5+4+4 cols x 5+4 rows into
  1x 5x5 + 1x 5x4 + 2x 4x5 + 2x 4x4 (5x4 and 4x5 are the same STL
  rotated 90 degrees).

16 tiles total across the three drawers. Largest tile (6x5) is
251.5 mm — near the A1's 256 mm bed limit but proven (the sibling
desk-drawer-gridfinity project prints 6-wide tiles successfully).

`gridfinity-build123d` only generates bin geometry, so the baseplate is
built here: a flat slab with `gf.Base(grid)` subtracted from it. The
subtracted shape is the exact bin-foot profile, so any standard
Gridfinity bin seats correctly.

`gridfinity-build123d` only generates bin geometry, so the baseplate is
built here: a flat slab with `gf.Base(grid)` subtracted from it. The
subtracted shape is the exact bin-foot profile, so any standard
Gridfinity bin seats correctly.
"""

from pathlib import Path

# ─── Parameters ──
# Tiles to generate as (cols, rows, qty). One STL per (cols, rows); set qty
# in Bambu Studio (Right-click → Set quantity). qty is total copies across
# all three drawers. Top drawer is divider-split (two 6x9 compartments);
# middle + bottom are continuous 13x9. 4x5 positions use the 5x4 STL
# rotated 90 degrees, so 5x4 qty covers both orientations.
TILES: list[tuple[int, int, int]] = [
    (3, 5, 4),  # top drawer — back band split (6x5 too big for A1 bed edge zones);
    # 2 tiles side-by-side per compartment × 2 compartments
    (6, 4, 2),  # top drawer — front band, one per compartment
    (5, 5, 2),  # middle + bottom — left corner, 5-deep band
    (5, 4, 6),  # middle + bottom — left corner 4-deep + middle/right 5-deep (rotated)
    (4, 4, 4),  # middle + bottom — middle/right, 4-deep band
]

# Cell pitch and slab thickness are fixed by the Gridfinity spec — match
# what gf.Base produces (bin foot = 4.75 mm tall, 41.5 mm cell footprint).
CELL_PITCH = 42.0
SLAB_HEIGHT = 4.75
SLAB_INSET = 0.5  # 0.25 mm of air around each tile edge so tiles don't bind.


# ─── Geometry ──
# gridfinity-build123d isn't in the repo .venv (only build123d is), so the
# import is gated. Set up the per-project venv per README to author parts.
try:
    import gridfinity as gf  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "gridfinity-build123d not installed. Set up the per-project venv:\n"
        "  python3.13 -m venv projects/workbench-drawer-gridfinity/3d/.venv\n"
        "  projects/workbench-drawer-gridfinity/3d/.venv/bin/pip install "
        "-r projects/workbench-drawer-gridfinity/3d/requirements.txt"
    ) from exc

from build123d import Align, Box, export_stl  # noqa: E402


def make_baseplate(cols: int, rows: int):
    """A flat slab with bin-foot profiles subtracted from the top face."""
    grid = [[True] * cols for _ in range(rows)]
    bin_feet = gf.Base(grid=grid)  # extends from z=0 to z=SLAB_HEIGHT, centered in XY

    slab_w = CELL_PITCH * cols - SLAB_INSET
    slab_d = CELL_PITCH * rows - SLAB_INSET
    slab = Box(
        slab_w,
        slab_d,
        SLAB_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return slab - bin_feet


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

for cols, rows, qty in TILES:
    plate = make_baseplate(cols, rows)
    out_path = out_dir / f"baseplate_{cols}x{rows}.stl"
    export_stl(plate, str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"Wrote {out_path.name} ({size_kb} KB) — print {qty} copies")
