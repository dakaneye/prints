"""Chamber cap for the pitcher spigot valve. PRINT IN TPU 95A.

A press-in bung that closes the chamber top after the stopper + spring drop in.
Its flat underside is the spring's TOP abutment — the spring reacts against the
cap and pushes the stopper down onto the seat. Seals two ways, both compression
(the only kind that's held): the flange underside squeezes down on the chamber
rim, and the plug grips the cavity wall by interference. No stem passes through
it, so it is a static seal — far easier than the moving one at the seat. Pull it
out to service the stopper.

The chamber pressure is only the pitcher's head (~0.03 bar), so press-fit
friction far exceeds the force trying to push it out.

Built at the assembled position (cavity axis XC, chamber top Z=18). Prints flat
(flange on the bed), no supports.
"""

from pathlib import Path

from build123d import Align, Cylinder, Pos, export_stl

# ─── Parameters (mm) — match valve_body.py chamber top ──
XC = 14.0
CHAMBER_TOP = 18.0
CAVITY_R = 6.0  # = valve_body CH_IR

PLUG_R = CAVITY_R + 0.2  # 6.2 — interference in the Ø12 cavity (TPU squishes to seal/grip)
PLUG_DEPTH = 5.0
TIP_CHAMFER = 1.0  # eased lead-in so it starts straight
FLANGE_R = 8.0  # overhangs the cavity onto the rim (R6..R9) → compression seal
FLANGE_H = 3.0
SPRING_POCKET_R = 4.0  # captures the spring top OD (use a spring Ø5–7.5 OD)
SPRING_POCKET_DEPTH = 3.0

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Plug down into the cavity (Z = 13..18), with a chamfered lead-in at the bottom.
plug = Pos(XC, 0, CHAMBER_TOP - PLUG_DEPTH) * Cylinder(PLUG_R, PLUG_DEPTH, align=BOTTOM)
lead_in = Pos(XC, 0, CHAMBER_TOP - PLUG_DEPTH - TIP_CHAMFER) * Cylinder(
    PLUG_R - TIP_CHAMFER, TIP_CHAMFER, align=BOTTOM
)
# Flange sitting on the rim (Z = 18..21), the squeezed face that seals.
flange = Pos(XC, 0, CHAMBER_TOP) * Cylinder(FLANGE_R, FLANGE_H, align=BOTTOM)

# Spring pocket bored up into the underside — captures the spring top so it
# can't buckle or wander (the stopper post centres the bottom).
spring_pocket = Pos(XC, 0, CHAMBER_TOP - PLUG_DEPTH - TIP_CHAMFER) * Cylinder(
    SPRING_POCKET_R, SPRING_POCKET_DEPTH, align=BOTTOM
)

cap = plug + lead_in + flange - spring_pocket

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(cap, str(out_dir / "cap.stl"))
