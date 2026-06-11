"""Lever for the pitcher spigot valve. PRINT IN PLA.

Rides in the body's yoke slot, pivots on a Ø3 pin through the yoke ears. The arm
reaches under the stem foot; the handle rests up-and-out. PULL the handle down
and the arm lifts the foot off the seat → pours. Release and the stopper's own
weight pushes the arm back down, returning the handle up → shuts. The handle
length gives the leverage to lift the stopper against the water above it.

The handle is shaped like a beverage-tap lever: a narrow neck off the pivot
(slot-width, so it clears the yoke ears) flaring into a wide scooped paddle.

Built at the assembled position (pivot matches valve_body PIVOT_X / PIVOT_Z).
Print on its side (a wide Y face on the bed); the shallow scoop trough may want
light support, which peels off the grip face cleanly.
"""

from pathlib import Path

from build123d import Align, Box, Cylinder, Plane, Pos, Rectangle, Rot, export_stl, loft

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
# ── Scooped paddle handle, shaped like a beverage-tap lever ──
# A narrow NECK comes off the pivot at slot width (so it clears the yoke ears),
# then flares into a wide scooped head once it has risen above the ears.
PADDLE_LEN = 34.0
NECK_X = 15.0  # stays slot-width until here (clears the ears), then flares
TILT = 44.0  # angle up-and-out from horizontal
PADDLE_T = 6.0
SCOOP_R = 12.0
FLOOR_T = 1.8  # trough floor left under the scoop
HALF_NECK = ARM_HALF_Y  # 3.8 — fits the yoke slot
HALF_TIP = 8.0  # half-width at the flared tip


def _xsec(half_w):
    return Plane.YZ * Rectangle(2 * half_w, PADDLE_T, align=(Align.CENTER, Align.MIN))


# Loft: slot-width neck (two sections) then flare to the wide head.
_slab = loft(
    [
        _xsec(HALF_NECK),
        Pos(NECK_X, 0, 0) * _xsec(HALF_NECK),
        Pos(PADDLE_LEN, 0, 0) * _xsec(HALF_TIP),
    ]
)
# Scoop a trough into the flared head only (cylinder along the length).
_scoop = Pos((NECK_X + PADDLE_LEN) / 2, 0, FLOOR_T + SCOOP_R) * (
    Rot(0, 90, 0) * Cylinder(SCOOP_R, PADDLE_LEN - NECK_X)
)
_paddle = _slab - _scoop
# Tilt up-and-out and bury the back in the boss.
handle = Pos(PIVOT_X, 0, PIVOT_Z) * Rot(0, -TILT, 0) * Pos(-3, 0, 0) * _paddle

lever = boss + arm + cradle_back + handle
# Pin hole all the way through the boss — centred on Y (a rotated align=BOTTOM
# cylinder would only drill halfway, leaving a blind hole). Long enough to clear
# the paddle stem that overlaps the boss.
pin_hole = Pos(PIVOT_X, 0, PIVOT_Z) * (Rot(90, 0, 0) * Cylinder(HOLE_R, 11))
lever -= pin_hole

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(lever, str(out_dir / "lever.stl"))
