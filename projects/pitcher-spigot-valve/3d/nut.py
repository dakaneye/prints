"""Clamp nut for the pitcher spigot valve.

PRINT IN PLA (stiff — it must clamp the gasket hard; do NOT print in TPU, it
would squish instead of clamping). Threads onto the body barrel from inside
the pitcher and tightens the flange + gaskets against the glass. Three wings
give finger purchase to hand-tighten; the wide flat face spreads load over the
glass. Finger-tight only. Print >=5 perimeters / high infill for strong threads.

Print: bearing face down, no supports.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Cylinder,
    Helix,
    Plane,
    Pos,
    Rot,
    Trapezoid,
    export_stl,
    sweep,
)

# ─── Parameters (mm) — thread matches valve_body.py barrel ──
THREAD_CORE_R = 6.75
THREAD_PITCH = 3.0
NUT_THREAD_CLEAR = 0.3
NUT_HEIGHT = 6.0  # thin; ~2 turns of engagement
NUT_OD = 26.0  # wide flat face spreads load over glass

WINGS = 3
WING_LEN = 9.0  # how far each wing reaches past the nut OD
WING_W = 6.0  # wing thickness (finger grip)

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
bore_r = THREAD_CORE_R + NUT_THREAD_CLEAR
body = Cylinder(NUT_OD / 2, NUT_HEIGHT, align=BOTTOM)
bore = Cylinder(bore_r, NUT_HEIGHT, align=BOTTOM)
path = Helix(pitch=THREAD_PITCH, height=NUT_HEIGHT, radius=bore_r)
profile = Plane(origin=path @ 0, z_dir=path % 0) * Trapezoid(
    width=THREAD_PITCH * 0.75, height=1.0, left_side_angle=60
)
nut = body - bore - sweep(profile, path)


def _wing():
    # A bar reaching out from the nut OD, with a rounded tip, full nut height.
    bar = Pos(NUT_OD / 2 + WING_LEN / 2 - 2, 0, NUT_HEIGHT / 2) * Box(WING_LEN, WING_W, NUT_HEIGHT)
    tip = Pos(NUT_OD / 2 + WING_LEN - 2, 0, 0) * Cylinder(WING_W / 2, NUT_HEIGHT, align=BOTTOM)
    return bar + tip


for i in range(WINGS):
    nut += Rot(0, 0, 360 * i / WINGS) * _wing()

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(nut, str(out_dir / "nut.stl"))
