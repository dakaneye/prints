"""Lift-off lid for the organizer's q-tip well.

A plug-style cap: a flat disc that overhangs the well rim and rests on the
body's top face, with a short downward plug that slips into the Ø42 well
(0.8 mm diametral clearance for a hand-fit). Keeps q-tips dry and clean.

Print orientation: cap face down on the bed, plug pointing up — no overhang,
no supports. Diameters here must track QT_D in organizer.py.
"""

from pathlib import Path

from build123d import Align, Cylinder, Pos, export_stl

# ─── Parameters (mm) ──
WELL_D = 42.0  # must match QT_D in organizer.py
CLEARANCE = 0.8  # diametral gap so the plug hand-fits the well

CAP_OVERHANG = 3.0  # cap radius beyond the well, rests on the body top
CAP_THICK = 3.0  # cap disc thickness
PLUG_DEPTH = 6.0  # how far the plug reaches into the well

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

cap = Pos(0, 0, 0) * Cylinder(WELL_D / 2 + CAP_OVERHANG, CAP_THICK, align=BOTTOM)
plug = Pos(0, 0, CAP_THICK) * Cylinder((WELL_D - CLEARANCE) / 2, PLUG_DEPTH, align=BOTTOM)
part = cap + plug

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "qtip_lid.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
