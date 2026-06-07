"""Wowza keychain — coin with raised text on the front, hole for split ring."""

from pathlib import Path

from build123d import (
    Align,
    Cylinder,
    Pos,
    Text,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
WORD = "WOWZA"
FONT = "Arial Rounded MT Bold"

COIN_DIAM = 24.5  # US-quarter sized
COIN_THICKNESS = 2.0  # half-thickness for a thinner, more coin-like feel

# Rim around the edge — the stacking surface. Coins rest rim-to-bottom
# when stacked, so RIM_HEIGHT must exceed TEXT_RAISE (enforced below).
RIM_WIDTH = 1.2
RIM_HEIGHT = 1.5

TEXT_RAISE = 1.0  # raised text height — readable + printable
TEXT_MARGIN = 2.5  # clearance from rim's inner edge to text
TEXT_Y_OFFSET = -2.0  # shift text down to leave room for the hole at the top

HOLE_DIAM = 5.0  # threads any standard split ring (wire ø 1–2 mm)
HOLE_FROM_EDGE = 5.0


# ─── Geometry ──
if RIM_HEIGHT <= TEXT_RAISE:
    raise ValueError(
        f"RIM_HEIGHT ({RIM_HEIGHT}) must exceed TEXT_RAISE ({TEXT_RAISE}) "
        "or stacked coins won't sit flush."
    )

coin = Cylinder(
    radius=COIN_DIAM / 2,
    height=COIN_THICKNESS,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

rim_outer = Cylinder(
    radius=COIN_DIAM / 2,
    height=RIM_HEIGHT,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
rim_inner = Cylinder(
    radius=COIN_DIAM / 2 - RIM_WIDTH,
    height=RIM_HEIGHT,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
rim = Pos(0, 0, COIN_THICKNESS) * (rim_outer - rim_inner)

# Text auto-sized to fit inside the depressed inner face. Resize COIN_DIAM
# or RIM_WIDTH and the text scales with it; no hand-tuning needed.
sample = Text(WORD, font_size=10.0, font=FONT)
sample_bb = sample.bounding_box()
text_font_size = 10.0 * (
    (COIN_DIAM - 2 * RIM_WIDTH - 2 * TEXT_MARGIN) / (sample_bb.max.X - sample_bb.min.X)
)

text_sketch = Text(WORD, font_size=text_font_size, font=FONT)
tbb = text_sketch.bounding_box()
# Text origin isn't its visual centre; recentre on (0, 0) before placing.
text_centered = (
    Pos(
        -(tbb.min.X + tbb.max.X) / 2,
        -(tbb.min.Y + tbb.max.Y) / 2,
    )
    * text_sketch
)
text_3d = Pos(0, TEXT_Y_OFFSET, COIN_THICKNESS) * extrude(text_centered, amount=TEXT_RAISE)

hole = Pos(0, (COIN_DIAM / 2) - HOLE_FROM_EDGE, 0) * Cylinder(
    radius=HOLE_DIAM / 2,
    height=COIN_THICKNESS + RIM_HEIGHT + 2,  # over-tall for a clean boolean
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

keychain = (coin + rim + text_3d) - hole


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "keychain.stl"
export_stl(keychain, str(out_path))
print(f"Wrote {out_path}")
