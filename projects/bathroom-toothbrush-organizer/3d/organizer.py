"""Family bathroom organizer with a smoothly-reeded outer wall.

A rounded-rectangle prism whose perimeter is fluted with fine vertical
reeding: each point on the perimeter is displaced radially by a sine wave of
the arc-length, then the resulting smooth wavy outline is extruded. This gives
soft rounded ridges and grooves that ride cleanly around the corners — no
sharp cusps, no corner spikes. Two zones share the body:

  * Wet zone (left): three Ø16 brush bores in a back row and one toothpaste
    pocket up front, each with a Ø4 drain hole through the floor so water
    runs straight out the bottom onto the counter/tray below.
  * Dry zone (right end): a wide oval q-tip well with its own raised solid
    floor (no drain) so sheeting water can't reach it, capped by the separate
    qtip_lid.py lift-off lid.

Print orientation: upright, as it sits. Every feature is vertical or open at
the top — no bridges, no supports. See README.
"""

import math
from pathlib import Path

from build123d import (
    Align,
    Box,
    Cylinder,
    Ellipse,
    Polygon,
    Pos,
    RectangleRounded,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
WIDTH = 188.0  # X — footprint width (wide enough for the oval q-tip well)
DEPTH = 70.0  # Y — footprint depth
HEIGHT = 80.0  # Z — overall height
CORNER_R = 18.0  # rounded-rect corner radius

# Vertical reeding: wide pitch, shallow depth. FLUTE_PITCH is the crest-to-crest
# spacing measured along the perimeter; FLUTE_DEPTH is the radial amplitude
# (ridges stand +DEPTH proud, grooves cut -DEPTH in). PERIMETER_SAMPLES sets how
# finely the wavy outline is polygonized — high enough to read as a smooth curve.
FLUTE_PITCH = 7.5
FLUTE_DEPTH = 0.55
PERIMETER_SAMPLES = 900

FLOOR = 4.0  # solid floor thickness under the wet pockets
DRAIN_D = 4.0  # drain-hole diameter through the floor

BRUSH_D = 16.0  # brush bore diameter (fits adult + kids' manual brushes)
BRUSH_Y = 14.0  # back row, +Y of center
BRUSH_X = (-65.0, -43.0, -21.0)  # three bores across the wet zone

TP_W = 50.0  # toothpaste pocket size (X)
TP_L = 26.0  # toothpaste pocket size (Y)
TP_X = -50.0  # toothpaste pocket center X
TP_Y = -16.0  # front row, -Y of center

QT_RX = 28.0  # q-tip well ellipse radius in X (well is 56 wide)
QT_RY = 21.0  # q-tip well ellipse radius in Y (well is 42 deep); long axis L-R
QT_X = 58.0  # right end
QT_FLOOR = FLOOR + 3.0  # raised solid floor — keeps q-tips dry, no drain hole

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)


def _reeded_profile():
    """Rounded-rect outline displaced into smooth vertical reeding.

    Walks the perimeter at PERIMETER_SAMPLES points, pushing each point along
    the perpendicular by a sine of its arc-length position. The flute count is
    chosen so a whole number of periods fits the loop, which makes the wave
    close seamlessly back on itself at the start point.
    """
    outline = RectangleRounded(WIDTH, DEPTH, CORNER_R)
    wire = outline.wires()[0]

    base = []
    normals = []
    for i in range(PERIMETER_SAMPLES):
        t = i / PERIMETER_SAMPLES
        point = wire @ t
        tangent = wire % t
        base.append((point.X, point.Y))
        normals.append((tangent.Y, -tangent.X))  # perpendicular to the tangent

    # Cumulative arc length so the flute pitch is uniform in real space,
    # independent of how the parameter t is distributed across edges.
    arc = [0.0]
    for i in range(1, PERIMETER_SAMPLES):
        x0, y0 = base[i - 1]
        x1, y1 = base[i]
        arc.append(arc[-1] + math.hypot(x1 - x0, y1 - y0))
    total = arc[-1] + math.hypot(base[0][0] - base[-1][0], base[0][1] - base[-1][1])

    n_flutes = max(8, round(total / FLUTE_PITCH))
    pts = []
    for i in range(PERIMETER_SAMPLES):
        x, y = base[i]
        nx, ny = normals[i]
        disp = FLUTE_DEPTH * math.sin(2 * math.pi * n_flutes * arc[i] / total)
        pts.append((x + nx * disp, y + ny * disp))
    return Polygon(*pts)


part = extrude(_reeded_profile(), amount=HEIGHT)

# Wet zone: three brush bores down to the floor, each with a floor drain hole.
for cx in BRUSH_X:
    part = part - Pos(cx, BRUSH_Y, FLOOR) * Cylinder(BRUSH_D / 2, HEIGHT - FLOOR, align=BOTTOM)
    part = part - Pos(cx, BRUSH_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Toothpaste pocket (front) with its own floor drain hole.
part = part - Pos(TP_X, TP_Y, FLOOR) * Box(TP_W, TP_L, HEIGHT - FLOOR, align=BOTTOM)
part = part - Pos(TP_X, TP_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Dry zone: oval q-tip well with a raised solid floor (no drain hole).
# Surrounding material forms the wall that isolates it from the wet zone.
part = part - Pos(QT_X, 0, QT_FLOOR) * extrude(Ellipse(QT_RX, QT_RY), amount=HEIGHT - QT_FLOOR)

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "organizer.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
