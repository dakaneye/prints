"""Quarter-turn plug for the pitcher spigot valve.

A tapered plug seats in body.py's chamber (seat centered at Z=0, spanning
Z=[-SEAT_DEPTH/2, +SEAT_DEPTH/2], wide SEAT_TOP_R at the +Z opening
tapering to SEAT_BOT_R at the -Z floor). An L-shaped internal bore connects
a side opening (-X, the barrel inlet at Z=0) to a bottom opening (-Z, the
spout). Rotate the lever 90 deg to face a solid seat wall = closed. A flat
paddle on top is the lever.

PLUG_CLEAR is the tuning knob: increase if it binds, decrease if it
leaks/wobbles. Smear food-safe silicone grease on the taper.

Print orientation: lever up, taper down, no supports.
"""

from pathlib import Path

from build123d import Align, Box, Cone, Cylinder, Pos, Rot, export_stl

# ─── Parameters (mm) — match body.py seat frame ──
SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
PLUG_CLEAR = 0.25  # radial clearance vs seat — TUNE on the prototype

# L-channel radius. Ø7, below the spec's nominal Ø10: a wider bore would
# thin the plug wall at the narrow seat end below the fit guard's
# SEAT_BOT_R − PLUG_CLEAR > LBORE_R + 0.8 rule. Trades some flow for wall.
LBORE_R = 3.5
LEVER_LEN = 30.0
LEVER_WIDTH = 9.0
LEVER_THK = 5.0
# Paddle must sweep ABOVE the body's gasket flange (a 33 mm disc standing at
# the −X face, top edge near Z=16.5) so the lever clears it in the open
# position where it points at the flange. Flange top is at SEAT_DEPTH/2 + 7.5;
# lift the paddle just above that.
LEVER_LIFT = 9.0  # paddle this far above the seat top → bottom at Z=18 > flange
NECK_R = 5.25  # joins paddle to plug top as one body

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
TOP_Z = SEAT_DEPTH / 2  # +9 — seat opening
BOT_Z = -SEAT_DEPTH / 2  # -9 — seat floor

# ─── Geometry ──
# Tapered plug, clearance-reduced, narrowing downward to match the seat.
top_r = SEAT_TOP_R - PLUG_CLEAR
bot_r = SEAT_BOT_R - PLUG_CLEAR
plug = Pos(0, 0, BOT_Z) * Cone(bot_r, top_r, SEAT_DEPTH, align=BOTTOM)

# Lever paddle + neck above the seat opening.
neck = Pos(0, 0, TOP_Z) * Cylinder(NECK_R, LEVER_LIFT + 0.1, align=BOTTOM)
lever = Pos(0, 0, TOP_Z + LEVER_LIFT) * Box(LEVER_LEN, LEVER_WIDTH, LEVER_THK, align=BOTTOM)
solid = plug + neck + lever

# L-bore: side channel (-X, blind half) at Z=0 meeting a vertical channel
# (-Z) from the plug bottom up to centre. Liquid: barrel inlet -> side
# channel -> centre -> down -> plug bottom -> spout.
side = Rot(0, -90, 0) * Cylinder(LBORE_R, top_r + 1, align=BOTTOM)
bottom = Pos(0, 0, BOT_Z) * Cylinder(LBORE_R, SEAT_DEPTH / 2 + LBORE_R, align=BOTTOM)

plug_final = solid - side - bottom

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(plug_final, str(out_dir / "plug.stl"))
