"""Generic empty Gridfinity bins — starter set for the desk drawer.

These are blank bins with default compartments (single open cavity, no
dividers). For purpose-shaped inserts (pen holders with drilled pockets,
glasses cradles, guitar pick organizers), download from MakerWorld and
log in `downloaded/SOURCES.md` instead — the community designs are
better-tuned to specific items.

One STL per unique (cols, rows, height_U). Set print quantity in Bambu
Studio (Right-click → Set quantity → N) to match the BINS table.
"""

from pathlib import Path

# ─── Parameters ──
# (cols, rows, height_U, qty) where 1U = 7 mm. Edit to suit the layout.
BINS: list[tuple[int, int, int, int]] = [
    (1, 2, 6, 2),  # pens / markers (vertical)
    (2, 2, 6, 2),  # cards / keys / general purpose
    (2, 2, 9, 2),  # grip trainers stacked, playing cards deck
    (4, 2, 6, 2),  # glasses case, checkbook
    (3, 3, 12, 1),  # rolled guitar strap
]

UNIT_MM = 7.0  # Gridfinity height unit


# ─── Geometry ──
try:
    import gridfinity as gf  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "gridfinity-build123d not installed. Set up the per-project venv:\n"
        "  python3.13 -m venv projects/desk-drawer-gridfinity/3d/.venv\n"
        "  projects/desk-drawer-gridfinity/3d/.venv/bin/pip install "
        "-r projects/desk-drawer-gridfinity/3d/requirements.txt"
    ) from exc

from build123d import export_stl  # noqa: E402


def make_bin(cols: int, rows: int, height_u: int):
    """A blank Gridfinity bin: foot + walls + stacking lip + one open cavity."""
    grid = [[True] * cols for _ in range(rows)]
    return gf.Bin(grid=grid, height=height_u * UNIT_MM)


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

for cols, rows, height_u, qty in BINS:
    part = make_bin(cols, rows, height_u)
    out_path = out_dir / f"bin_{cols}x{rows}x{height_u}U.stl"
    export_stl(part, str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"Wrote {out_path.name} ({size_kb} KB) — print {qty} copies")
