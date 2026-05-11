"""Generic empty Gridfinity bins for the workbench drawers.

Mirrors `desk-drawer-gridfinity/3d/bins.py`. Empty starter set — drawer
inventory will drive `BINS` once dimensions are confirmed and items are
mapped to cells.

For purpose-shaped inserts (socket trays, bit-holder slots, hex-key
cradles), download from MakerWorld and log in `downloaded/SOURCES.md`
instead — the community designs are better-tuned to specific tools.

One STL per unique (cols, rows, height_U). Set print quantity in Bambu
Studio (Right-click → Set quantity → N) to match the BINS table.
"""

from pathlib import Path

# ─── Parameters ──
# (cols, rows, height_U, qty) where 1U = 7 mm. Empty until drawer
# inventory is mapped. Example shapes that tool drawers commonly want:
#   (1, 1, 3, 4),   # tape measure / pocket items
#   (2, 1, 6, 2),   # small driver / level
#   (2, 2, 6, 2),   # bit case / socket box
#   (3, 2, 4, 2),   # bit strips lying flat
BINS: list[tuple[int, int, int, int]] = []

UNIT_MM = 7.0  # Gridfinity height unit


# ─── Geometry ──
try:
    import gridfinity as gf  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "gridfinity-build123d not installed. Set up the per-project venv:\n"
        "  python3.13 -m venv projects/workbench-drawer-gridfinity/3d/.venv\n"
        "  projects/workbench-drawer-gridfinity/3d/.venv/bin/pip install "
        "-r projects/workbench-drawer-gridfinity/3d/requirements.txt"
    ) from exc

from build123d import export_stl  # noqa: E402


def make_bin(cols: int, rows: int, height_u: int):
    """A blank Gridfinity bin: foot + walls + stacking lip + one open cavity."""
    grid = [[True] * cols for _ in range(rows)]
    return gf.Bin(grid=grid, height=height_u * UNIT_MM)


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

if not BINS:
    print("No bins configured — populate BINS once drawer inventory is mapped.")

for cols, rows, height_u, qty in BINS:
    part = make_bin(cols, rows, height_u)
    out_path = out_dir / f"bin_{cols}x{rows}x{height_u}U.stl"
    export_stl(part, str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"Wrote {out_path.name} ({size_kb} KB) — print {qty} copies")
