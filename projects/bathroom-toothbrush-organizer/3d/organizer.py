"""Family bathroom organizer with a smoothly-reeded outer wall.

A thin-walled hollow shell — not a solid block — so it prints fast and uses
little filament. The outer wall is fluted with fine vertical reeding (each
perimeter point displaced by a sine of its arc length, then extruded), bounded
by a smooth base band and top rim. The interior is mostly empty: a thin wet/dry
divider splits it into two compartments, and the functional features stand in
them as thin-walled sockets:

  * Wet zone (left): three Ø18 brush sockets in a back row and one toothpaste
    pocket up front, each a thin tube with a Ø4 drain hole through the floor so
    water runs straight out the bottom onto the counter/tray below.
  * Dry zone (right): a wide oval q-tip well with its own raised solid floor
    (no drain) so sheeting water can't reach it, capped by the separate
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

# Smooth, un-reeded rim bands top and bottom — the flutes live between them.
RIM_BOTTOM = 6.0  # smooth base band height
RIM_TOP = 5.0  # smooth top rim band height

WALL = 3.0  # outer-shell and wet/dry divider wall thickness
SOCK_WALL = 2.4  # wall thickness of the brush sockets / toothpaste / oval well
FLOOR = 3.0  # thin floor under the open interior and the pockets
DRAIN_D = 4.0  # drain-hole diameter through the floor
DIVIDER_X = 10.0  # X of the wet/dry divider wall

BRUSH_D = 18.0  # brush socket bore (fits adult + kids' manual brushes)
BRUSH_Y = 14.0  # back row, +Y of center
BRUSH_X = (-66.0, -43.0, -20.0)  # three sockets across the wet zone

TP_W = 56.0  # toothpaste pocket size (X)
TP_L = 30.0  # toothpaste pocket size (Y)
TP_X = -49.0  # toothpaste pocket center X
TP_Y = -15.0  # front row, -Y of center

QT_RX = 32.0  # q-tip well ellipse radius in X (well is 64 wide)
QT_RY = 23.0  # q-tip well ellipse radius in Y (well is 46 deep); long axis L-R
QT_X = 50.0  # center-right (pulled in from the end for a more balanced layout)
QT_FLOOR = FLOOR + 3.0  # raised solid floor — keeps q-tips dry, no drain hole

# Extra drains in the open wet-compartment floor (stray drips outside the
# sockets). Coordinates verified clear of the sockets and toothpaste pocket.
WET_DRAINS = ((-5.0, 14.0), (-5.0, -15.0))

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
FEAT_H = HEIGHT - FLOOR - RIM_TOP  # height of interior walls/sockets/divider


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


# Solid outer body: reeded prism plus smooth base/top rim bands. The rim outline
# is the nominal rect offset out by the flute amplitude, so it sits flush with
# the flute crests and fills the valleys within each band.
part = extrude(_reeded_profile(), amount=HEIGHT)
rim = RectangleRounded(WIDTH + 2 * FLUTE_DEPTH, DEPTH + 2 * FLUTE_DEPTH, CORNER_R + FLUTE_DEPTH)
part = part + extrude(rim, amount=RIM_BOTTOM)
part = part + Pos(0, 0, HEIGHT - RIM_TOP) * extrude(rim, amount=RIM_TOP)

# Hollow it out: remove an inner cavity inset by WALL (measured from the flute
# valleys) from the floor up to the open top. This leaves a thin reeded shell.
inner = RectangleRounded(
    WIDTH - 2 * (WALL + FLUTE_DEPTH),
    DEPTH - 2 * (WALL + FLUTE_DEPTH),
    max(2.0, CORNER_R - WALL),
)
inner_depth = DEPTH - 2 * (WALL + FLUTE_DEPTH)
part = part - Pos(0, 0, FLOOR) * extrude(inner, amount=HEIGHT - FLOOR)

# Wet/dry divider wall, floor to just under the top rim, spanning the cavity.
part = part + Pos(DIVIDER_X, 0, FLOOR) * Box(WALL, inner_depth, FEAT_H, align=BOTTOM)

# Add the thin-walled feature posts standing in the hollow, then bore them out.
for cx in BRUSH_X:
    part = part + Pos(cx, BRUSH_Y, FLOOR) * Cylinder(BRUSH_D / 2 + SOCK_WALL, FEAT_H, align=BOTTOM)
part = part + Pos(TP_X, TP_Y, FLOOR) * Box(
    TP_W + 2 * SOCK_WALL, TP_L + 2 * SOCK_WALL, FEAT_H, align=BOTTOM
)
part = part + Pos(QT_X, 0, FLOOR) * extrude(
    Ellipse(QT_RX + SOCK_WALL, QT_RY + SOCK_WALL), amount=FEAT_H
)

# Brush bores (over-tall so they open through the top rim) + floor drains.
for cx in BRUSH_X:
    part = part - Pos(cx, BRUSH_Y, FLOOR) * Cylinder(BRUSH_D / 2, HEIGHT, align=BOTTOM)
    part = part - Pos(cx, BRUSH_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Toothpaste pocket + floor drain.
part = part - Pos(TP_X, TP_Y, FLOOR) * Box(TP_W, TP_L, HEIGHT, align=BOTTOM)
part = part - Pos(TP_X, TP_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Oval q-tip well, bored from its raised floor (no drain — stays dry).
part = part - Pos(QT_X, 0, QT_FLOOR) * extrude(Ellipse(QT_RX, QT_RY), amount=HEIGHT)

# Extra drains in the open wet-compartment floor.
for dx, dy in WET_DRAINS:
    part = part - Pos(dx, dy, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "organizer.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
