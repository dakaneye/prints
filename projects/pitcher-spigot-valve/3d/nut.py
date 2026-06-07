"""Clamp nut for the pitcher spigot valve.

Threads onto the body barrel from inside the pitcher and clamps the
flange + reused rubber gasket against the glass. The thread is a coarse
helix-swept trapezoid matching body.py, widened by NUT_THREAD_CLEAR so a
printed barrel turns freely. The bearing face is wide and flat to spread
load over glass — finger-tight only.

Print orientation: bearing face down on the plate, no supports.
"""

from pathlib import Path

from build123d import (
    Align,
    Cylinder,
    Helix,
    Plane,
    Trapezoid,
    export_stl,
    sweep,
)

# ─── Parameters (mm) ──
THREAD_PITCH = 3.0
THREAD_CORE_R = 6.75
NUT_THREAD_CLEAR = 0.3  # radial clearance vs barrel
NUT_HEIGHT = 9.0  # thread engagement; >= glass thickness + margin
NUT_OD = 30.0  # wide flat face spreads load over glass

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Internal thread radius = barrel core + clearance. The nut bore is the
# thread root; the swept trapezoid carves the groove.
bore_r = THREAD_CORE_R + NUT_THREAD_CLEAR

body = Cylinder(NUT_OD / 2, NUT_HEIGHT, align=BOTTOM)
bore = Cylinder(bore_r, NUT_HEIGHT, align=BOTTOM)

path = Helix(pitch=THREAD_PITCH, height=NUT_HEIGHT, radius=bore_r)
profile = Plane(origin=path @ 0, z_dir=path % 0) * Trapezoid(
    width=THREAD_PITCH * 0.75, height=1.0, left_side_angle=60
)
groove = sweep(profile, path)

nut = body - bore - groove

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(nut, str(out_dir / "nut.stl"))
