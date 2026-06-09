"""Printable wall gasket for the pitcher spigot valve.

PRINT IN TPU (95A) — PRINT TWO, one each side of the glass (flange · gasket ·
GLASS · gasket · nut). A flat sealing washer between the body flange and the
glass — an alternative to reusing the original rubber gasket. Print it FLAT:
the bed-side face comes out smooth and seals well against glass. 95A is firmer
than rubber, so clamp it well (that is why the nut is stiff PLA). Print solid
(100% infill / many walls) so water cannot weep through.

Sized for the body flange; ID clears the barrel, OD sits under the flange.

Print: TPU 95A, external spool, flat, solid infill, no supports.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

ID = 16.0  # clears the Ø15.3 barrel
OD = 30.0  # under the 33 mm flange
THK = 2.5

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
gasket = Cylinder(OD / 2, THK, align=BOTTOM) - Cylinder(ID / 2, THK, align=BOTTOM)

out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(gasket, str(out_dir / "gasket.stl"))
