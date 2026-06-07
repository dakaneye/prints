"""Gridfinity baseplate tiles, sized to fit the Bambu A1's 256x256 mm bed.

The full drawer needs an 8x8 grid (336x336 mm of cells in a ~358x340 mm
drawer). The A1 can't print 8x8 in one piece, so this script emits one
STL per tile in TILES — the four tiles together form the 8x8 baseplate.

`gridfinity-build123d` only generates bin geometry, so the baseplate is
built here: a flat slab with `gf.Base(grid)` subtracted from it. The
subtracted shape is the exact bin-foot profile, so any standard
Gridfinity bin seats correctly.
"""

from pathlib import Path

# ─── Parameters ──
# Tiles to generate as (cols, rows, qty). One STL per (cols, rows); set qty
# in Bambu Studio (Right-click → Set quantity). Default 8x8 split: two 6x4
# tiles + two 2x4 tiles. The A1's 256 mm bed fits up to 6x6 in one print.
TILES: list[tuple[int, int, int]] = [
    (6, 4, 2),
    (2, 4, 2),
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
        "  python3.13 -m venv projects/desk-drawer-gridfinity/3d/.venv\n"
        "  projects/desk-drawer-gridfinity/3d/.venv/bin/pip install "
        "-r projects/desk-drawer-gridfinity/3d/requirements.txt"
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
