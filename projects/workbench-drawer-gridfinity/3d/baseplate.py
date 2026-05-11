"""Gridfinity baseplate tiles for the workbench rolling-cabinet drawers.

Mirrors `desk-drawer-gridfinity/3d/baseplate.py` — emits one STL per
tile in TILES. Drawer dimensions are still TBD, so the default is a
single 6 x 4 tile: the largest single tile that fits the Bambu A1's
256 mm bed comfortably, and a fit-check before committing to a full
drawer's worth of plates.

`gridfinity-build123d` only generates bin geometry, so the baseplate is
built here: a flat slab with `gf.Base(grid)` subtracted from it. The
subtracted shape is the exact bin-foot profile, so any standard
Gridfinity bin seats correctly.
"""

from pathlib import Path

# ─── Parameters ──
# Tiles to generate as (cols, rows, qty). One STL per (cols, rows); set qty
# in Bambu Studio (Right-click → Set quantity). All three Craftsman
# drawers share the same 13x9 cell grid (interior ~565-580 W × 410 D mm
# with 4 mm clearance). Per-drawer layout: 13 cols = 5+4+4, 9 rows = 5+4,
# giving 6 tiles per drawer in 4 unique sizes. Across 3 drawers:
TILES: list[tuple[int, int, int]] = [
    (5, 5, 3),  # top-left corner of each drawer
    (5, 4, 3),  # bottom-left corner of each drawer
    (4, 5, 6),  # top middle + top right of each drawer
    (4, 4, 6),  # bottom middle + bottom right of each drawer
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
