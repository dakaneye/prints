"""Slide-on pad for a parallel bar clamp jaw.

Caps the flat steel jaw so metal never touches the workpiece. The jaw
slides in axially through the open mouth and bottoms out against the
solid closed end. The cross-section is a C: a back wall, two side
walls, and two asymmetric lips that curl over the channel and retain
the pad on the jaw's front face. The two short ends are stadium-rounded.

Print orientation: stand on the closed end (slide axis vertical) — no
bridges, no supports. See README.
"""

from pathlib import Path

from build123d import Align, Box, Pos, RectangleRounded, export_stl, extrude

# ─── Parameters (mm) ──
# Measured from the worn original; it currently fits the jaw, so it is
# treated as ground truth.
OUTER_LENGTH = 38.67  # slide axis: closed end → mouth
OUTER_WIDTH = 27.0  # across the lips
OUTER_THICKNESS = 10.0  # back-to-front: BACK_WALL + CHANNEL_HEIGHT + LIP_THICKNESS

CHANNEL_WIDTH = 21.0  # jaw plate width
CHANNEL_HEIGHT = 4.0  # slot the jaw sits in (jaw thickness)

BACK_WALL = 2.0  # solid plate behind the channel
LIP_THICKNESS = 4.0  # Z thickness of each retaining lip
LIP_OVERHANG_A = 2.0  # +Y lip inward reach over the channel
LIP_OVERHANG_B = 3.7  # -Y lip inward reach over the channel
SIDE_WALL = 2.5  # each Y-edge wall
CLOSED_END_WALL = 2.5  # solid stop at the D end

# Added to channel width AND height for slide fit. 0.0 = reproduce as
# measured (tightest PLA grip). Bump up if it will not slide on.
FIT_CLEARANCE = 0.0

# ─── Geometry ──
# X = slide axis, Y = across, Z = back→front. The outer body is centered
# in XY at the origin (RectangleRounded centers there) and extruded from
# Z=0 (back wall) to Z=OUTER_THICKNESS (front). Closed end at X = -L/2,
# open mouth at X = +L/2.

# Outer body: a stadium prism. RectangleRounded with radius = half the
# width rounds the two short (X) ends to true semicircles — no fragile
# edge filtering. Radius nudged 0.001 under W/2 so build123d keeps the
# straight long edges instead of degenerating to an ellipse.
profile = RectangleRounded(OUTER_LENGTH, OUTER_WIDTH, OUTER_WIDTH / 2 - 0.001)
body = extrude(profile, amount=OUTER_THICKNESS)

# Channel pocket: open at the +X mouth, stops CLOSED_END_WALL short of
# the -X closed end, floored by BACK_WALL, ceiled by the lips. Over-long
# in +X by 1 mm so the boolean leaves a clean open mouth (no thin film).
pocket_w = CHANNEL_WIDTH + FIT_CLEARANCE
pocket_h = CHANNEL_HEIGHT + FIT_CLEARANCE
pocket_len = OUTER_LENGTH - CLOSED_END_WALL + 1.0
pocket = Pos(-OUTER_LENGTH / 2 + CLOSED_END_WALL, 0, BACK_WALL) * Box(
    pocket_len,
    pocket_w,
    pocket_h,
    align=(Align.MIN, Align.CENTER, Align.MIN),
)

# Mouth window: removes the +Z face between the lips so the jaw's front
# face is exposed and only the two Y-edge lips remain. Offset in Y so
# the +Y lip reads LIP_OVERHANG_A and the -Y lip reads LIP_OVERHANG_B.
window_w = CHANNEL_WIDTH - LIP_OVERHANG_A - LIP_OVERHANG_B
window_center_y = (LIP_OVERHANG_B - LIP_OVERHANG_A) / 2
window = Pos(
    -OUTER_LENGTH / 2 + CLOSED_END_WALL,
    window_center_y,
    OUTER_THICKNESS - LIP_THICKNESS,
) * Box(
    pocket_len,
    window_w,
    LIP_THICKNESS + 1.0,  # over-tall in +Z so the cut breaks the surface
    align=(Align.MIN, Align.CENTER, Align.MIN),
)

part = body - pocket - window

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "pad.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
