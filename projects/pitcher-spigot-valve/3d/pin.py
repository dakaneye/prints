"""Pivot pin for the lever. PRINT IN PLA (or use a 3 mm rod / filament offcut).

A plain Ø3 rod through the yoke ears + lever boss. Print it standing on end (it
is just a short cylinder) or lay several flat. Push-fit; a dab of friction holds
it — it carries almost no load.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

PIN_R = 1.5  # Ø3.0 — snug in the Ø3.2 yoke holes, free in the Ø3.4 lever hole
PIN_LEN = 15.0  # spans the yoke outer width (Y = ±7.5), flush at the far ear
HEAD_R = 2.5  # Ø5 head — can't pass through, so the pin can't fall out
HEAD_H = 1.5

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

pin = Cylinder(PIN_R, PIN_LEN, align=BOTTOM) + Cylinder(HEAD_R, HEAD_H, align=BOTTOM)

out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(pin, str(out_dir / "pin.stl"))
