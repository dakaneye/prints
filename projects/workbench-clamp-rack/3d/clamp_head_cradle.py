"""Shallow vertical cradle for a light bar clamp, screw-mounted to a
Multiboard tile.

Load-smart orientation: the fixed-jaw head sits in a shallow pocket
held flat against the wall; the head's long (~85 mm) dimension runs
vertically; the bar exits the bottom and hangs straight down right at
the tile face. Clamp mass stays within ~20 mm of the tile, so the
mount sees mostly shear (straight down the tile), not a pull-out
moment.

Mount is screw-primary: the official Locking Bolt threads through and
carries the load (a screw resists the hanging moment; a snap channel
does not). A shallow, deliberately loose hex recess registers the
official connector (object_6 of the Angled Drill Holder 3mf) for
anti-rotation only — so exact socket precision is not load-critical.

PART = "coupon": back plate + hex socket + bolt bore only (~20 min)
to test-fit your PRINTED Hook Snap + Locking Bolt before the cradle.
PART = "cradle": the full part.

Axes: X along the wall, Y out from the wall (Y=0 = tile face),
Z vertical (Z=0 = bottom).
"""

from pathlib import Path

from build123d import (
    Axis,
    Box,
    Cylinder,
    Plane,
    Polygon,
    Pos,
    export_stl,
    extrude,
    offset,
)

# ─── Parameters ──  (all mm)
PART = "cradle"  # "coupon" | "cradle"

# Clamp head, measured (generic light bar clamp, ~834 g). In this
# orientation: long dim vertical, mid dim across the wall, thin dim
# out from the wall.
HEAD_LONG = 85.0  # jaw/head long dimension -> vertical, along wall (Z)
HEAD_WIDE = 27.0  # head across -> horizontal, along wall (X)
HEAD_THICK = 18.0  # head thickness -> out from wall (Y standoff)
BAR_W, BAR_T = 19.5, 6.3

CAPTURE_H = 78.0  # how much of HEAD_LONG the pocket grips (<= HEAD_LONG)
SIDE_CLR = 1.5  # per-side clearance around the head
WALL = 3.0
BASE = 3.0
FRONT_LIP = 10.0  # low front lip height so the head can't fall forward
BAR_SLOT_W = BAR_W + 1.5

POCKET_W = HEAD_WIDE + 2 * SIDE_CLR  # 30.0  (X interior)
POCKET_Y = HEAD_THICK + SIDE_CLR  # 19.5  (Y interior, standoff)
BACK_W = POCKET_W + 2 * WALL  # 36.0
BACK_H = CAPTURE_H + BASE  # 81.0

# Official Multipoint connector outline (object_6 convex hull,
# centered, (x, z) mm) — registration only, intentionally loose:
SOCKET_OUTLINE = [
    (-8.82, -1.59),
    (-7.50, -2.74),
    (-7.47, -2.76),
    (4.18, -7.53),
    (7.48, -7.53),
    (7.98, -7.30),
    (7.98, -6.37),
    (7.98, 8.46),
    (7.48, 8.70),
    (4.18, 8.70),
    (-6.60, 3.95),
    (-8.07, 3.25),
    (-8.82, 2.76),
]
SOCKET_THICK = 4.5
SOCKET_CLEARANCE = 0.6  # generous: screw carries load, hex only registers
SOCKET_DEPTH = SOCKET_THICK + 0.5
BOLT_BORE_D = 5.0  # clearance for the Locking Bolt shaft — verify on coupon
BACK_T = SOCKET_DEPTH + 3.0  # socket recess + solid behind
MOUNT_FROM_TOP = 18.0  # socket centre below the top: mass hangs below the screw


def place(shape, *, x=None, y=None, z=None, cx=None, cz=None):
    """Translate by bounding box so there are no orientation guesses."""
    bb = shape.bounding_box()
    dx = dy = dz = 0.0
    if cx is not None:
        dx = cx - (bb.min.X + bb.max.X) / 2
    if x is not None:
        dx = x - bb.min.X
    if y is not None:
        dy = y - bb.min.Y
    if z is not None:
        dz = z - bb.min.Z
    if cz is not None:
        dz = cz - (bb.min.Z + bb.max.Z) / 2
    return Pos(dx, dy, dz) * shape


# ─── Geometry ──
def socket_cutter(cx, cz):
    """object_6 outline + clearance, extruded SOCKET_DEPTH inward from
    the tile face (Y=0)."""
    prof = offset(Polygon(*SOCKET_OUTLINE), amount=SOCKET_CLEARANCE)
    prism = extrude(Plane.XZ * prof, amount=SOCKET_DEPTH)
    prism = place(prism, cx=cx, cz=cz)
    return place(prism, y=0.0)


if PART == "coupon":
    W, H = 40.0, 40.0
    part = place(Box(W, BACK_T, H), cx=0.0, y=0.0, z=0.0)
    sx, sz = 0.0, H / 2.0
else:
    # back plate (flat to tile)
    part = place(Box(BACK_W, BACK_T, BACK_H), cx=0.0, y=0.0, z=0.0)
    # shallow cradle: outer block forward of the back plate, hollowed
    outer = place(Box(BACK_W, POCKET_Y + WALL, BACK_H), cx=0.0, y=BACK_T, z=0.0)
    part = part + outer
    cavity = place(Box(POCKET_W, POCKET_Y, CAPTURE_H), cx=0.0, y=BACK_T + WALL, z=BASE)
    part = part - cavity
    # open the front above the low retaining lip
    front_win = place(
        Box(POCKET_W, WALL + 2, CAPTURE_H - FRONT_LIP),
        cx=0.0,
        y=BACK_T + WALL + POCKET_Y - 1,
        z=BASE + FRONT_LIP,
    )
    part = part - front_win
    # bottom bar slot, kept against the wall so the bar hangs flush
    slot = place(Box(BAR_SLOT_W, WALL + 4, BASE + 2), cx=0.0, y=BACK_T + WALL - 1, z=-1.0)
    part = part - slot
    sx, sz = 0.0, BACK_H - MOUNT_FROM_TOP

# screw-primary mount: hex registration recess + bolt bore
part = part - socket_cutter(sx, sz)
bore = Cylinder(radius=BOLT_BORE_D / 2, height=BACK_T + 2).rotate(Axis.X, 90)
part = part - place(bore, cx=sx, y=-1.0, cz=sz)

# ─── Export ──
out = Path(__file__).parent / "out"
out.mkdir(exist_ok=True)
name = "socket_fit_coupon" if PART == "coupon" else "clamp_head_cradle"
export_stl(part, str(out / f"{name}.stl"))
print(f"exported {name}.stl  bbox={part.bounding_box().size}  volume={part.volume:.0f}mm^3")
