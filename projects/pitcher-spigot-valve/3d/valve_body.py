"""Valve body for the pitcher spigot — one piece. PRINT IN PETG.

The through-glass barrel (clamped by nut + 2 gaskets against the glass — the
proven seal) feeds a vertical chamber. A solid seat floor at the chamber bottom
has only a Ø6 throat; a TPU stopper (poppet.py) rests on that floor and seals
the throat by gravity + water pressure = SHUT. Its stem runs down the DRY spout
to a lever (lever.py) that pushes it up to pour; release and it drops back.

The only moving seal is the stopper on the seat (soft-on-hard compression). The
stem lives in the spout, dry whenever the valve is shut, so there is no
rod-through-water gap to weep — that was the diaphragm's failure.

The chamber top opens for dropping the stopper in; a cap closes it later.

Construction note: the helix-swept thread, fused as a unit, makes OCC booleans
fail silently — so the body is built from PLAIN cylinders first (these fuse
reliably), and the thread ridge is added last as a swept sliver embedded in the
barrel surface. Keep it that way or the body falls into loose pieces.

Axes: X = flow (barrel −X into pitcher), Z = vertical (chamber +Z, spout −Z).
Print: PETG, chamber up; >=4 perimeters so the walls hold water.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
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
# Through-glass barrel + flange (proven glass mount; pairs with nut.py / gasket.py).
BARREL_CORE_R = 6.75  # nut threads on this; crest stays < 15.8 glass hole
BARREL_PITCH = 3.0
BARREL_LEN = 16.0
THREAD_DEPTH = 1.4  # ridge radial size → crest ≈ 7.45 (OD 14.9 < 15.8)
BORE_R = 4.0  # Ø8 feed bore
FLANGE_OD = 33.0
FLANGE_THK = 3.0
Z_IN = 7.0  # barrel/bore axis height (above the seat)

# Vertical chamber (holds the stopper) + seat + spout.
CH_IR = 6.0  # chamber inner radius (stopper Ø9 drops in)
CH_WALL = 3.0  # PETG wall
CH_OR = CH_IR + CH_WALL  # 9
CH_TOP = 18.0  # chamber top (cap seats here)
SEAT_HOLE_R = 3.0  # Ø6 throat (smaller than the Ø9 disc)
FLOOR_T = 2.5  # solid seat floor: a ring the disc seals on
SPOUT_LEN = 16.0
SPOUT_OR = 7.0
SPOUT_IR = 5.0  # Ø10 bore below the floor, around the Ø3.5 stem
XC = 14.0  # chamber/spout axis X (clear of the flange)

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
BARREL_X0 = -BARREL_LEN  # −16, barrel tip inside the pitcher
STUB_LEN = XC - BARREL_X0  # plain barrel-core + neck, one cylinder to the chamber

# ─── Geometry: structural pieces, all PLAIN cylinders (fuse reliably) ──
# Barrel-core + neck as a single cylinder along X at Z_IN, from the pitcher tip
# to the chamber axis. Deep overlap with the chamber ties them together.
stub = Pos(BARREL_X0, 0, Z_IN) * (Rot(0, 90, 0) * Cylinder(BARREL_CORE_R, STUB_LEN, align=BOTTOM))
flange = Pos(0, 0, Z_IN) * (Rot(0, 90, 0) * Cylinder(FLANGE_OD / 2, FLANGE_THK, align=BOTTOM))
chamber = Pos(XC, 0, 0) * Cylinder(CH_OR, CH_TOP, align=BOTTOM)
spout = Pos(XC, 0, -SPOUT_LEN) * Cylinder(SPOUT_OR, SPOUT_LEN + CH_WALL, align=BOTTOM)
# 45° cone from chamber OD down to spout OD: printed chamber-up, this shoulder
# self-supports (no support material) instead of being a flat downward overhang.
CONE_H = CH_OR - SPOUT_OR  # 2 → 45°
spout_cone = Pos(XC, 0, -CONE_H) * Cone(SPOUT_OR, CH_OR, CONE_H, align=BOTTOM)

# Lever yoke: a slotted bracket on the +X/under side of the spout. Two ears
# straddle the stem foot; the lever rides in the slot and pivots on a pin
# through PIVOT. Exported so lever.py shares the pivot location.
PIVOT_X = XC + 10.0  # 24
PIVOT_Z = -23.0
PIN_R = 1.6  # Ø3.2 pin clearance hole
CB_R = 2.6  # Ø5.2 counterbore — the pin head seats flush in the −Y ear
CB_DEPTH = 2.1
# Ears 3.5 mm thick (Y 4..7.5), with >2 mm of plastic all round the pin hole:
# the block runs Z=−27..−14 (4 mm below the hole at −23) and X=17..28 (so the
# Ø5.2 head counterbore at X=24 still keeps ~1.4 mm wall to the +X edge).
yoke_block = Pos(22.5, 0, -20.5) * Box(11, 15, 13)  # X17..28 Y-7.5..7.5 Z-27..-14
yoke_slot = Pos(19.5, 0, -22.25) * Box(19, 8, 11.5)  # lever slot, open bottom; leaves two ears
yoke = yoke_block - yoke_slot
struct = chamber + spout + spout_cone + stub + flange + yoke

# External barrel thread: a helical ridge embedded in the stub surface over the
# pitcher-side length (X = −16..0). Added to the already-fused plain solid.
_tpath = Helix(pitch=BARREL_PITCH, height=BARREL_LEN, radius=BARREL_CORE_R)
ridge = Pos(BARREL_X0, 0, Z_IN) * (
    Rot(0, 90, 0)
    * sweep(
        Plane(origin=_tpath @ 0, z_dir=_tpath % 0)
        * Trapezoid(width=BARREL_PITCH * 0.7, height=THREAD_DEPTH, left_side_angle=60),
        _tpath,
    )
)
solid = struct + ridge

# ─── Bores (subtract) ──
cavity = Pos(XC, 0, 0) * Cylinder(CH_IR, CH_TOP + 1, align=BOTTOM)  # chamber; floor at Z=0
# Spout bore (Ø10) below the seat floor only — floor stays solid.
spout_bore = Pos(XC, 0, -SPOUT_LEN) * Cylinder(SPOUT_IR, SPOUT_LEN - FLOOR_T + 0.5, align=BOTTOM)
# Seat throat: Ø6 hole through the solid floor, cavity (Z=0) → spout bore.
seat_hole = Pos(XC, 0, -FLOOR_T) * Cylinder(SEAT_HOLE_R, FLOOR_T + 0.5, align=BOTTOM)
# Feed bore: Ø8 along −X at Z_IN, pitcher → chamber cavity.
feed = Pos(BARREL_X0 - 1, 0, Z_IN) * (Rot(0, 90, 0) * Cylinder(BORE_R, STUB_LEN + 1, align=BOTTOM))

# Pivot pin hole through BOTH yoke ears (centred on Y so it passes all the way
# through — a rotated align=BOTTOM cylinder would only drill one side).
pivot_hole = Pos(PIVOT_X, 0, PIVOT_Z) * (Rot(90, 0, 0) * Cylinder(PIN_R, 18))
# Open the slot up through the yoke web (centre only) over the +X half so the
# lever's neck can rise out — the ears still tie to the spout via the web at
# X<21, which is untouched.
handle_clear = Pos(24.0, 0, -14.75) * Box(8.0, 2 * 4.0, 5.0)
# Counterbore in the −Y ear so the pin head sits flush (retained, not proud).
counterbore = Pos(PIVOT_X, -6.5, PIVOT_Z) * (Rot(90, 0, 0) * Cylinder(CB_R, CB_DEPTH))

body = solid - cavity - spout_bore - seat_hole - feed - pivot_hole - handle_clear - counterbore

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(body, str(out_dir / "valve_body.stl"))
