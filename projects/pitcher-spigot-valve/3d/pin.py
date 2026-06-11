"""Pivot pin for the lever. PRINT IN PLA (or use a 3 mm rod / filament offcut).

A Ø3 rod through the yoke ears + lever boss, with a Ø5 head that seats in a
counterbore in the −Y ear: it can't fall out, yet sits FLUSH (head recessed,
shaft tip flush at the far ear) — no part sticks out. Push it in head-last from
the counterbore side. Print standing on end. It carries almost no load.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

PIN_R = 1.5  # Ø3.0 shaft — free in the Ø3.2 yoke holes / Ø3.4 lever hole
PIN_LEN = 15.0  # shaft spans the 15 mm yoke, flush at the far ear
HEAD_R = 2.5  # Ø5 head — seats flush in the ear's Ø5.2 counterbore, can't pass through
HEAD_H = 2.0

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

pin = Cylinder(PIN_R, PIN_LEN, align=BOTTOM) + Cylinder(HEAD_R, HEAD_H, align=BOTTOM)

out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(pin, str(out_dir / "pin.stl"))
