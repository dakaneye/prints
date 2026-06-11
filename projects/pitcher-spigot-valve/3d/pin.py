"""Pivot pin for the lever. PRINT IN PLA (or use a 3 mm rod / filament offcut).

A plain Ø3 rod through the yoke ears + lever boss. Shorter than the 15 mm yoke
so it sits flush/recessed — it does not stick out — while still bridging both
ears. Snug in the Ø3.2 yoke holes, free in the Ø3.4 lever hole; a dab of glue on
one end makes it permanent if it works loose. Print standing on end, or lay
several flat. It carries almost no load.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

PIN_R = 1.5  # Ø3.0 — snug in the Ø3.2 yoke holes, free in the Ø3.4 lever hole
PIN_LEN = 12.5  # sits within the 15 mm yoke (recessed ~1.25 mm each end); no head

pin = Cylinder(PIN_R, PIN_LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))

out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(pin, str(out_dir / "pin.stl"))
