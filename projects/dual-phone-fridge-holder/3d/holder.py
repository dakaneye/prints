"""Dual phone wall pocket that magnet-mounts to the side of a refrigerator.

One backplate with two open-front pockets, sized for two cased iPhone 16
Pros side by side in portrait. The back face has a 5×4 grid of shallow
recesses for 6×2 mm neodymium disc magnets, press-fit + CA glue, sitting
~0.2 mm proud so the magnets contact the fridge steel directly.

Each pocket floor is a 45° wedge sloping down toward the backplate: it
prints support-free in the standing orientation and tips the phone toward
the fridge instead of out of the pocket. Each front wall has a rounded
finger scoop for grabbing the phone.

Print orientation: as exported — standing upright on the backplate's bottom
edge, in-use pose. No supports, no bridges; use a 5 mm brim (3 mm plate on
edge is tip-prone).
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Cylinder,
    Plane,
    Polygon,
    Pos,
    RectangleRounded,
    Rot,
    export_stl,
    extrude,
)

# ─── Parameters ──
# All dimensions in mm.

# iPhone 16 Pro nominal 71.5 × 8.25; case estimated ~75 × 11 (no calipers).
POCKET_W = 78.0  # interior width per phone, ~3 mm case clearance
POCKET_D = 13.0  # interior depth, ~2 mm case clearance
POCKET_H = 65.0  # front-wall interior height above the floor's front lip
WALL_T = 2.4  # pocket front + side wall thickness
FLOOR_T = 3.0  # vertical thickness of the 45° wedge floor
POCKET_GAP = 8.0  # gap between the two pockets

PLATE_T = 3.0  # backplate thickness
PLATE_MARGIN_X = 8.0  # backplate border beyond the pocket outer walls
PLATE_CORNER_R = 8.0
POCKET_Z0 = 2.0  # lowest point of the pocket wedge above the plate bottom;
# kept near the bed so the print's cross-section deepens to an L-shape
# almost immediately — a bare 3 mm standing wall is the wobbly failure mode

SCOOP_W = 30.0  # finger scoop width in each front wall
SCOOP_DEPTH = 22.0  # scoop depth down from the wall top

# 6×2 mm neodymium discs (assorted-set grade). Recess is shallower than the
# magnet so it sits ~0.2 mm proud and contacts the fridge steel directly.
MAGNET_D = 6.0
MAGNET_FIT = 0.3  # diametral press-fit allowance for hole shrink
MAGNET_RECESS = 1.8
MAGNET_COLS = 5
MAGNET_ROWS = 4
MAGNET_EDGE = 15.0  # grid inset from the backplate edges

POCKET_OUTER_W = POCKET_W + 2 * WALL_T
PLATE_W = 2 * POCKET_OUTER_W + POCKET_GAP + 2 * PLATE_MARGIN_X
PLATE_H = POCKET_Z0 + FLOOR_T + (POCKET_D + WALL_T) + POCKET_H + 12.0

# ─── Geometry ──
# Modeled in print pose: plate bottom edge on Z=0, backplate spanning
# Y ∈ [0, PLATE_T], pockets extending toward +Y (away from the fridge).

plate = extrude(
    Plane.XZ * RectangleRounded(PLATE_W, PLATE_H, PLATE_CORNER_R),
    amount=-PLATE_T,
)
plate = Pos(0, 0, PLATE_H / 2) * plate

# Pocket side profile in the YZ plane, extruded across X. The underside
# rises at 45° from the backplate to the front wall; the cavity floor is
# the same slope lifted by FLOOR_T, so the phone slides back and leans in.
OUTER_D = POCKET_D + WALL_T  # pocket depth beyond the plate, incl. front wall
Z_LIP = POCKET_Z0 + FLOOR_T + POCKET_D  # cavity floor's front (highest) point
Z_TOP = Z_LIP + POCKET_H  # top of the pocket walls


def pocket(x_center: float):
    """One pocket solid (walls + floor, cavity removed) at x_center."""
    outer_profile = Polygon(
        (PLATE_T, POCKET_Z0),
        (PLATE_T + OUTER_D, POCKET_Z0 + OUTER_D),
        (PLATE_T + OUTER_D, Z_TOP),
        (PLATE_T, Z_TOP),
        align=None,
    )
    outer = extrude(Plane.YZ * outer_profile, amount=POCKET_OUTER_W / 2, both=True)
    cavity_profile = Polygon(
        (PLATE_T, POCKET_Z0 + FLOOR_T),
        (PLATE_T + POCKET_D, Z_LIP),
        (PLATE_T + POCKET_D, Z_TOP + 5),
        (PLATE_T, Z_TOP + 5),
        align=None,
    )
    cavity = extrude(Plane.YZ * cavity_profile, amount=POCKET_W / 2, both=True)
    scoop = Pos(0, PLATE_T + POCKET_D + WALL_T / 2, Z_TOP) * Box(
        SCOOP_W, WALL_T + 2, 2 * SCOOP_DEPTH, align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    scoop_round = (
        Pos(0, PLATE_T + POCKET_D + WALL_T / 2, Z_TOP - SCOOP_DEPTH)
        * Rot(90, 0, 0)
        * Cylinder(SCOOP_W / 2, WALL_T + 2, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    )
    return Pos(x_center, 0, 0) * (outer - cavity - scoop - scoop_round)


x_off = (POCKET_OUTER_W + POCKET_GAP) / 2
part = plate + pocket(-x_off) + pocket(x_off)

# Magnet recesses: shallow cylinders cut into the back face (Y=0 side).
xs = [
    -(PLATE_W / 2 - MAGNET_EDGE) + i * (PLATE_W - 2 * MAGNET_EDGE) / (MAGNET_COLS - 1)
    for i in range(MAGNET_COLS)
]
zs = [MAGNET_EDGE + j * (PLATE_H - 2 * MAGNET_EDGE) / (MAGNET_ROWS - 1) for j in range(MAGNET_ROWS)]
for x in xs:
    for z in zs:
        recess = (
            Pos(x, MAGNET_RECESS / 2 - 0.01, z)
            * Rot(90, 0, 0)
            * Cylinder(
                (MAGNET_D + MAGNET_FIT) / 2,
                MAGNET_RECESS + 0.02,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            )
        )
        part = part - recess

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(part, str(out_dir / "holder.stl"))
print(f"Exported {out_dir / 'holder.stl'}")
