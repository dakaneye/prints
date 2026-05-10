"""Generic empty Gridfinity bins for the electronics organizer.

Single open cavity per bin — Zone A of the case is sized for these. If a
purpose-shaped insert is wanted later (e.g., a cradle for the speakers, or
divided slots for tact switches), download a community design into
`downloaded/` and log it in SOURCES.md.

One STL per unique (cols, rows, height_U). Set print quantity in Bambu
Studio (Right-click → Set quantity → N) per the BINS table.
"""

from pathlib import Path

# ─── Parameters ──
# (cols, rows, height_U, qty) — keep aligned with the COMPARTMENTS list in
# case.py. Two unique bin sizes cover the Phase 2 word-clock BOM:
#   1x1x6U: AMP, µSD, USB-C, BTNS, SPKR (5 bins)
#   1x2x6U: ESP32, RTC          (2 bins)
BINS: list[tuple[int, int, int, int]] = [
    (1, 1, 6, 5),
    (1, 2, 6, 2),
]

UNIT_MM = 7.0  # Gridfinity height unit


# ─── Geometry ──
try:
    import gridfinity as gf  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "gridfinity-build123d not installed. Set up the per-project venv:\n"
        "  python3.13 -m venv projects/electronics-organizer/3d/.venv\n"
        "  GIT_CONFIG_GLOBAL=/dev/null projects/electronics-organizer/3d/.venv/bin/pip install "
        "-r projects/electronics-organizer/3d/requirements.txt"
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
