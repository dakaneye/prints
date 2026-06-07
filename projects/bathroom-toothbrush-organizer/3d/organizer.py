"""Family bathroom organizer with a scalloped outer wall.

A rounded-rectangle prism whose perimeter is fluted with concave vertical
scallops (a ring of circles subtracted from the 2D profile, then extruded).
Two zones share the body:

  * Wet zone (left): three Ø16 brush bores in a back row and one toothpaste
    pocket up front, each with a Ø4 drain hole through the floor so water
    runs straight out the bottom onto the counter/tray below.
  * Dry zone (right end): a q-tip well with its own raised solid floor (no
    drain) so sheeting water can't reach it, capped by the separate
    qtip_lid.py lift-off lid.

Print orientation: upright, as it sits. Every feature is vertical or open at
the top — no bridges, no supports. See README.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Circle,
    Cylinder,
    Pos,
    RectangleRounded,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
WIDTH = 165.0  # X — footprint width
DEPTH = 70.0  # Y — footprint depth
HEIGHT = 80.0  # Z — overall height
CORNER_R = 18.0  # rounded-rect corner radius

SCALLOP_R = 4.0  # groove radius scooped into the perimeter; depth ≈ this
# Scallop centers are spaced ~2·SCALLOP_R along the perimeter so adjacent
# scoops meet at sharp vertical ridges (concave vertical scallops).

FLOOR = 4.0  # solid floor thickness under the wet pockets
DRAIN_D = 4.0  # drain-hole diameter through the floor

BRUSH_D = 16.0  # brush bore diameter (fits adult + kids' manual brushes)
BRUSH_Y = 14.0  # back row, +Y of center
BRUSH_X = (-55.0, -35.0, -15.0)  # three bores across the wet zone

TP_W = 50.0  # toothpaste pocket size (X)
TP_L = 26.0  # toothpaste pocket size (Y)
TP_X = -35.0  # toothpaste pocket center X
TP_Y = -16.0  # front row, -Y of center

QT_D = 42.0  # q-tip well diameter
QT_X = 55.0  # right end
QT_FLOOR = FLOOR + 3.0  # raised solid floor — keeps q-tips dry, no drain hole

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# Scalloped outer profile: subtract a ring of circles centered on the
# rounded-rect perimeter, then extrude once (2D boolean is far faster than 3D).
outline = RectangleRounded(WIDTH, DEPTH, CORNER_R)
perimeter = outline.wires()[0]
n_scallops = max(12, round(perimeter.length / (2 * SCALLOP_R)))
profile = outline
for i in range(n_scallops):
    p = perimeter @ (i / n_scallops)  # normalized point along the perimeter
    profile = profile - Pos(p.X, p.Y) * Circle(SCALLOP_R)
part = extrude(profile, amount=HEIGHT)

# Wet zone: three brush bores down to the floor, each with a floor drain hole.
for cx in BRUSH_X:
    part = part - Pos(cx, BRUSH_Y, FLOOR) * Cylinder(BRUSH_D / 2, HEIGHT - FLOOR, align=BOTTOM)
    part = part - Pos(cx, BRUSH_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Toothpaste pocket (front) with its own floor drain hole.
part = part - Pos(TP_X, TP_Y, FLOOR) * Box(TP_W, TP_L, HEIGHT - FLOOR, align=BOTTOM)
part = part - Pos(TP_X, TP_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Dry zone: q-tip well with a raised solid floor (no drain hole). Surrounding
# material forms the wall that isolates it from the wet zone.
part = part - Pos(QT_X, 0, QT_FLOOR) * Cylinder(QT_D / 2, HEIGHT - QT_FLOOR, align=BOTTOM)

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "organizer.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
