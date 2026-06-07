"""Spacer block for the breaker panel bottom gap.

Sits on the cabinet floor and fills the ~7.5 mm gap below the panel's
bottom edge. Pull tab on the front extends out of the cabinet for one-
handed removal.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    export_stl,
)

# ─── Parameters (mm) ──
# Measured gap: ~7.5 mm. Start under by 0.2 mm so the block slides in cleanly
# for the first fit; bump up by 0.1 mm increments if it rattles.
BLOCK_HEIGHT = 7.3

# Panel front face is 17.6 mm wide. Block stays narrower so it has lateral
# clearance and can be placed off-centre if the bottom profile demands it.
BLOCK_WIDTH = 12.0

# Front-to-back depth into the cabinet. Less than the 30 mm thickest
# dimension of the box, so it doesn't poke through anything.
BLOCK_DEPTH = 20.0

# Pull tab extends forward (out of the cabinet face) for finger access.
TAB_WIDTH = 12.0
TAB_LENGTH = 15.0
TAB_THICKNESS = 3.0

# Finger hole near the tab's front edge — easier to grab than a flat tab.
TAB_HOLE_DIAM = 5.0
TAB_HOLE_INSET = 4.0  # centre of hole, measured from the tab's front edge


# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

block = Box(BLOCK_WIDTH, BLOCK_DEPTH, BLOCK_HEIGHT, align=BOTTOM)

# Tab back face flush with block's front face (Y = BLOCK_DEPTH / 2).
tab = Pos(0, BLOCK_DEPTH / 2, 0) * Box(
    TAB_WIDTH,
    TAB_LENGTH,
    TAB_THICKNESS,
    align=(Align.CENTER, Align.MIN, Align.MIN),
)

# Cylinder over-tall on both ends so the boolean cut leaves no thin film.
hole_y = BLOCK_DEPTH / 2 + TAB_LENGTH - TAB_HOLE_INSET
hole = Pos(0, hole_y, -1) * Cylinder(
    radius=TAB_HOLE_DIAM / 2,
    height=TAB_THICKNESS + 2,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

part = (block + tab) - hole


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "block.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
