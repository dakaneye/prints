"""Display base for the wizard figurine.

A rectangular oak plaque with the recipient's name + print date engraved on
the top surface and a shallow recess that locates the figurine's feet.

FIGURINE_FOOT_WIDTH / FIGURINE_FOOT_DEPTH below are placeholders — after
printing the figurine, measure its feet with calipers and update these.
See Task 20 of the implementation plan.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Pos,
    Text,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
# Plaque outer dimensions. Sized for a ~100mm figurine.
BASE_WIDTH = 90.0
BASE_DEPTH = 60.0
BASE_HEIGHT = 10.0

# Recipient name + date (engraved on top surface, front half)
RECIPIENT_NAME = "WALLACE"
PRINT_DATE = "APR 2026"

# Engraving depth — readable at arm's length, shallow enough not to weaken
# the plaque's top layer.
ENGRAVE_DEPTH = 1.2

NAME_FONT_SIZE = 10.0
DATE_FONT_SIZE = 5.0

# Recessed footprint for figurine's feet — PLACEHOLDER values.
# After the figurine prints, measure its base and update these
# (+ ~0.4mm print tolerance per dimension).
FIGURINE_FOOT_WIDTH = 30.0
FIGURINE_FOOT_DEPTH = 20.0
FOOT_RECESS_DEPTH = 2.0

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# Main plaque
plaque = Box(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT, align=BOTTOM)

# Name engraving — front half of the plaque (negative Y)
name_text = Text(RECIPIENT_NAME, font_size=NAME_FONT_SIZE)
name_3d = extrude(name_text, amount=ENGRAVE_DEPTH)
name_3d = Pos(0, -BASE_DEPTH * 0.25, BASE_HEIGHT - ENGRAVE_DEPTH) * name_3d

# Date engraving — below the name
date_text = Text(PRINT_DATE, font_size=DATE_FONT_SIZE)
date_3d = extrude(date_text, amount=ENGRAVE_DEPTH)
date_3d = Pos(0, -BASE_DEPTH * 0.40, BASE_HEIGHT - ENGRAVE_DEPTH) * date_3d

plaque = plaque - name_3d - date_3d

# Figurine foot recess — back half of the plaque (positive Y)
foot_recess = Box(
    FIGURINE_FOOT_WIDTH,
    FIGURINE_FOOT_DEPTH,
    FOOT_RECESS_DEPTH,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
foot_recess = Pos(0, BASE_DEPTH * 0.15, BASE_HEIGHT - FOOT_RECESS_DEPTH) * foot_recess
plaque = plaque - foot_recess

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(plaque, str(out_dir / "base.stl"))

print(f"Wrote {out_dir / 'base.stl'}")
