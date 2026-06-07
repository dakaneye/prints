"""Lift-off lid for the organizer's oval q-tip well.

A plug-style cap: a flat oval disc that overhangs the well rim and rests on the
body's top face, with a short downward oval plug that slips into the well
(0.8 mm diametral clearance for a hand-fit). Keeps q-tips dry and clean.

Print orientation: cap face down on the bed, plug pointing up — no overhang,
no supports. The well radii here must track QT_RX / QT_RY in organizer.py.
"""

from pathlib import Path

from build123d import Ellipse, Pos, export_stl, extrude

# ─── Parameters (mm) ──
WELL_RX = 32.0  # must match QT_RX in organizer.py
WELL_RY = 23.0  # must match QT_RY in organizer.py
CLEARANCE = 0.8  # diametral gap so the plug hand-fits the well (0.4 per side)

CAP_OVERHANG = 3.0  # cap reach beyond the well, rests on the body top
CAP_THICK = 3.0  # cap disc thickness
PLUG_DEPTH = 6.0  # how far the plug reaches into the well

# ─── Geometry ──
cap = extrude(Ellipse(WELL_RX + CAP_OVERHANG, WELL_RY + CAP_OVERHANG), amount=CAP_THICK)
plug = Pos(0, 0, CAP_THICK) * extrude(
    Ellipse(WELL_RX - CLEARANCE / 2, WELL_RY - CLEARANCE / 2), amount=PLUG_DEPTH
)
part = cap + plug

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "qtip_lid.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
