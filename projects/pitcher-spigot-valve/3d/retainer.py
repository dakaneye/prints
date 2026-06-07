"""Retainer collar for the pitcher spigot valve.

A press-fit ring that drops over the plug neck and grips the chamber's
outer wall, holding the plug down against water pressure while still
letting it turn. Replace with a threaded cap if it lifts in testing.

Print orientation: flat, no supports.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

# ─── Parameters (mm) — match body.py chamber and plug.py neck ──
SEAT_TOP_R = 9.0
SEAT_WALL = 3.0
CHAMBER_OUTER_R = SEAT_TOP_R + SEAT_WALL  # = 12.0, body chamber OD/2

GRIP_CLEAR = 0.15  # press-fit interference onto chamber wall
COLLAR_HEIGHT = 6.0
COLLAR_WALL = 3.0
# Clears the plug neck (NECK_R 5.25) but is smaller than the plug top
# shoulder (~8.75) so the collar caps and retains the plug.
NECK_CLEAR_R = 5.8

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
outer = Cylinder(CHAMBER_OUTER_R + COLLAR_WALL, COLLAR_HEIGHT, align=BOTTOM)
grip_bore = Cylinder(CHAMBER_OUTER_R - GRIP_CLEAR, COLLAR_HEIGHT - COLLAR_WALL, align=BOTTOM)
neck_bore = Cylinder(NECK_CLEAR_R, COLLAR_HEIGHT, align=BOTTOM)

retainer = outer - grip_bore - neck_bore

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(retainer, str(out_dir / "retainer.stl"))
