"""Valve body for the pitcher spigot valve.

A through-wall threaded barrel (passes the glass hole, clamped by nut +
reused gasket against the flange) opens into a tapered plug seat with a
downward spout. Quarter-turn plug (plug.py) gates flow.

Axes: X = barrel/flow (−X into pitcher), Z = plug axis (spout exits −Z).
Flow when open: barrel bore (−X) → plug L-bore → spout bore (−Z).

Print orientation: barrel pointing up (+X vertical), spout needs light
support. >=4 perimeters so the bores don't weep.
"""

from pathlib import Path

from build123d import (
    Align,
    Cone,
    Cylinder,
    Helix,
    Plane,
    Pos,
    Rot,
    Trapezoid,
    export_stl,
    sweep,
)

# ─── Parameters (mm) ──
THREAD_PITCH = 3.0
THREAD_CORE_R = 6.75
THREAD_CREST_R = 7.65  # OD 15.3 < HOLE_DIA 15.8
THREAD_LEN = 16.0
BARREL_BORE_R = 5.0

FLANGE_OD = 33.0
FLANGE_THK = 3.0

SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
SEAT_WALL = 3.0  # chamber wall around the seat

SPOUT_BORE_R = 4.0
SPOUT_OD = 12.0
SPOUT_DROP = 18.0  # tip below barrel axis (Z=0)

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Chamber is centered on the origin; barrel axis and spout pass through it.
# 1) Chamber block: a cylinder around the plug seat, axis = Z, centered Z=0.
chamber_outer_r = SEAT_TOP_R + SEAT_WALL
chamber = Pos(0, 0, -SEAT_DEPTH / 2) * Cylinder(chamber_outer_r, SEAT_DEPTH, align=BOTTOM)

# 2) Barrel: threaded cylinder along −X, starting at the chamber wall.
#    Built along +Z then rotated so its axis is +X, then translated to −X.
barrel_core = Cylinder(THREAD_CORE_R, THREAD_LEN, align=BOTTOM)
b_path = Helix(pitch=THREAD_PITCH, height=THREAD_LEN, radius=THREAD_CORE_R)
b_profile = Plane(origin=b_path @ 0, z_dir=b_path % 0) * Trapezoid(
    width=THREAD_PITCH * 0.6,
    height=THREAD_CREST_R - THREAD_CORE_R,
    left_side_angle=60,
)
barrel_threaded = barrel_core + sweep(b_profile, b_path)
# Rot(0,-90,0) sends the +Z-built barrel to span X=[-THREAD_LEN, 0]; its
# inner end sits at the origin. Shift it −X so it protrudes outboard of the
# chamber wall (surface at X=−chamber_outer_r) while keeping a 2 mm overlap
# into the chamber for a solid weld.
BARREL_OVERLAP = 2.0
barrel_shift = -(chamber_outer_r - BARREL_OVERLAP)
barrel = Rot(0, -90, 0) * barrel_threaded
barrel = Pos(barrel_shift, 0, 0) * barrel

# 3) Flange: gasket disc at the glass face. Started 1 mm proud of the
#    chamber surface (−chamber_outer_r) so its inner thickness overlaps the
#    chamber body rather than sharing a tangent plane with it (a coincident
#    face there leaves the export non-watertight).
FLANGE_OVERLAP = 1.0
flange = Pos(-(chamber_outer_r + FLANGE_OVERLAP), 0, 0) * (
    Rot(0, 90, 0) * Cylinder(FLANGE_OD / 2, FLANGE_THK + FLANGE_OVERLAP, align=BOTTOM)
)

# 4) Spout: downward tube from chamber bottom.
spout = Pos(0, 0, -SPOUT_DROP) * Cylinder(SPOUT_OD / 2, SPOUT_DROP, align=BOTTOM)

# 4b) Neck: a frustum welding the chamber floor to the spout. The tapered
#     seat bottom (radius SEAT_BOT_R) is wider than the spout tube, so a
#     funnel from just outside the seat bottom down to the spout OD gives a
#     solid connection and channels flow from the seat into the spout bore.
chamber_floor_z = -SEAT_DEPTH / 2
NECK_H = 8.0
NECK_OVERLAP = 3.0  # neck top rises above the chamber floor to weld solidly
neck_top_r = SEAT_TOP_R + 2.0  # wider than the seat at every overlap Z
# Cone narrow end (SPOUT_OD/2) at the bottom, wide end (neck_top_r) at the
# top; the wide top rises NECK_OVERLAP above the chamber floor. Because the
# neck radius exceeds the seat radius all the way through the chamber-floor
# cut plane, a solid ring outside the seat cavity welds the spout to the
# chamber and funnels flow into the spout bore.
neck_top_z = chamber_floor_z + NECK_OVERLAP
neck = Pos(0, 0, neck_top_z - NECK_H) * Cone(SPOUT_OD / 2, neck_top_r, NECK_H, align=BOTTOM)

solid = chamber + barrel + flange + neck + spout

# 5) Tapered plug seat (subtract): open at +Z, narrowing downward — wide
#    SEAT_TOP_R at the top opening (+Z) tapering to SEAT_BOT_R at the floor
#    (−Z) so a top-dropped plug wedges and seals.
seat = Pos(0, 0, -SEAT_DEPTH / 2) * Cone(SEAT_BOT_R, SEAT_TOP_R, SEAT_DEPTH, align=BOTTOM)
# 6) Barrel bore (−X) into the seat. Runs from past the barrel tip through
#    the chamber wall and 1 mm past the seat axis so the flow path opens
#    into the seat cavity.
barrel_bore_len = chamber_outer_r + THREAD_LEN + 1
barrel_bore = Rot(0, -90, 0) * Cylinder(BARREL_BORE_R, barrel_bore_len, align=BOTTOM)
barrel_bore = Pos(1, 0, 0) * barrel_bore
# 7) Spout bore (−Z) out of the seat bottom.
spout_bore = Pos(0, 0, -SPOUT_DROP) * Cylinder(SPOUT_BORE_R, SPOUT_DROP + 1, align=BOTTOM)

body = solid - seat - barrel_bore - spout_bore

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(body, str(out_dir / "body.stl"))
