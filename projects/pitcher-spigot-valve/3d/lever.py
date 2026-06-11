"""Lever for the pitcher spigot valve. PRINT IN PLA.

Rides in the body's yoke slot, pivots on a Ø3 pin through the yoke ears. The arm
reaches under the stem foot; the handle rests up-and-out. PULL the handle down
and the arm lifts the foot off the seat → pours. Release and the stopper's own
weight pushes the arm back down, returning the handle up → shuts. The handle
length gives the leverage to lift the stopper against the water above it.

Built at the assembled position (pivot matches valve_body PIVOT_X / PIVOT_Z).
Prints flat on its wide Y face — no supports.
"""

from pathlib import Path

from build123d import Align, Box, Cylinder, Pos, Rot, export_stl

# ─── Parameters (mm) — pivot matches valve_body.py ──
PIVOT_X = 24.0
PIVOT_Z = -23.0
HOLE_R = 1.7  # Ø3.4 — runs freely on the Ø3 pin
ARM_HALF_Y = 3.8  # fills the yoke slot (Y = ±4) with 0.2 mm clearance each side
FOOT_X = 14.0  # stem-foot axis (valve_body XC)
ARM_TOP_Z = -22.0  # arm top meets the foot bottom here at rest

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry (all plain boxes; each overlaps the boss so they fuse to one solid) ──
ARM_X0 = FOOT_X - 4.0  # arm reaches past the foot so the back wall sits behind it
boss = Pos(PIVOT_X, 0, PIVOT_Z) * Box(5.0, 2 * ARM_HALF_Y, 5.0)
# Arm from under the foot to into the boss (top surface = foot bottom).
arm = Pos((ARM_X0 + PIVOT_X + 0.5) / 2, 0, ARM_TOP_Z - 1) * Box(
    (PIVOT_X + 0.5) - ARM_X0, 2 * ARM_HALF_Y, 2
)
# Back wall (−X end of the arm): stops the foot sliding off toward the spout —
# the one direction it could escape. Y is pinned by the arm width + the yoke
# slot, +X by the arm body. Low enough to clear the spout on an over-pull.
CW = 1.3  # wall height above the arm top
cradle_back = Pos(ARM_X0 + 0.5, 0, ARM_TOP_Z - 1 + CW / 2) * Box(1.0, 2 * ARM_HALF_Y, 2 + CW)
# Handle: one bar tilted up-and-out, its lower end buried in the boss.
handle = Pos(PIVOT_X + 4, 0, PIVOT_Z + 4.5) * Rot(0, -40, 0) * Box(14, 2 * ARM_HALF_Y, 3.5)
# Paddle grip at the handle tip.
paddle = Pos(PIVOT_X + 9.2, 0, PIVOT_Z + 8.5) * Box(4.5, 2 * (ARM_HALF_Y + 1.5), 9)

lever = boss + arm + cradle_back + handle + paddle
# Pin hole all the way through the boss — centred on Y (a rotated align=BOTTOM
# cylinder would only drill halfway, leaving a blind hole).
pin_hole = Pos(PIVOT_X, 0, PIVOT_Z) * (Rot(90, 0, 0) * Cylinder(HOLE_R, 8))
lever -= pin_hole

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(lever, str(out_dir / "lever.stl"))
