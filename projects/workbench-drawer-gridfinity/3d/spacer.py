"""Flat spacer strips for top drawer perimeter slack.

The top drawer's two compartments are each tiled with a 6 × 9 grid of
42 mm cells (252 × 378 mm of baseplate), inside compartments that are
~279 mm (left of divider) × ~296 mm (right of divider) wide and
410 mm deep. That leaves a strip of empty space along the outer edge
of each compartment:

  - LEFT compartment: ~25 mm wide × 410 mm deep, against the left wall
  - RIGHT compartment: ~45 mm wide × 410 mm deep, against the right wall

These spacers fill that slack so the printed tiles don't slide
sideways in the drawer. They're flat slabs at the same 4.75 mm height
as a Gridfinity baseplate, so the drawer floor stays level with the
tile slab — useful if a long item rests across the spacer + tile.

Each side strip is split into two halves so it fits A1's safe build
area (each half ≈ 205 mm long; A1's effective edge-safe zone is
~250 mm). Adjust SPACERS below if your drawer measures differently;
the README's "27/44 mm" is calculated from interior width minus the
6 × 42 mm tile footprint and may be off by a few mm vs the actual
drawer due to wall radii and divider thickness.
"""

from pathlib import Path

from build123d import Box, export_stl

# ─── Parameters ──  (all mm)
SLAB_HEIGHT = 4.75  # match Gridfinity baseplate slab height
DRAWER_DEPTH = 410.0
PIECE_LEN = DRAWER_DEPTH / 2  # 205 mm — safely inside A1's edge-safe zone

# (label, width_mm, qty_per_side)
# qty 2 = the strip is split into two halves to fit A1; print both
# halves to span the full 410 mm drawer depth.
SPACERS: list[tuple[str, float, int]] = [
    ("left", 25.0, 2),  # ~25 mm slack on the left edge of the LEFT compartment
    ("right", 45.0, 2),  # ~45 mm slack on the right edge of the RIGHT compartment
]

# ─── Geometry & Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

for label, width, qty in SPACERS:
    slab = Box(width, PIECE_LEN, SLAB_HEIGHT)
    name = f"spacer_{label}_{int(width)}x{int(PIECE_LEN)}.stl"
    export_stl(slab, str(out_dir / name))
    print(
        f"Wrote {name} ({width:.0f} × {PIECE_LEN:.0f} × {SLAB_HEIGHT} mm) "
        f"— print {qty} copies (covers full {DRAWER_DEPTH:.0f} mm drawer depth)"
    )
