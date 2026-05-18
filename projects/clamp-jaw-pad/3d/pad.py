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
OUTER_WIDTH = 26.0  # across the lips (= CHANNEL_WIDTH + 2 × 2.5 wrap)
OUTER_THICKNESS = 11.5  # back-to-front: BACK_WALL + CHANNEL_HEIGHT + LIP_THICKNESS

CHANNEL_WIDTH = 21.0  # jaw plate width
CHANNEL_HEIGHT = 4.0  # slot the jaw sits in (jaw thickness)

BACK_WALL = 3.5  # solid plate between channel floor and workpiece face
LIP_THICKNESS = 4.0  # Z thickness of each retaining lip
LIP_OVERHANG_A = 2.0  # +Y lip inward reach over the channel
LIP_OVERHANG_B = 3.7  # -Y lip inward reach over the channel
MOUTH_OVERSHOOT = 2.0  # pocket extends past the +X mouth so it opens cleanly

# The pocket's closed end is a semicircle concentric with the outer D.
# Concentric circles give a constant solid wall everywhere around the
# back and along the sides: (OUTER_WIDTH - CHANNEL_WIDTH) / 2 = 2.5 mm.
# This is what fills the back corners that a rectangular pocket left open.
WRAP_WALL = (OUTER_WIDTH - CHANNEL_WIDTH) / 2

# Added to channel width AND height for slide fit. 0.0 = reproduce as
# measured (tightest PLA grip). Bump up if it will not slide on.
FIT_CLEARANCE = 0.0

# ─── Geometry ──
# X = slide axis, Y = across, Z = back→front. The outer body is centered
# in XY at the origin (RectangleRounded centers there) and extruded from
# Z=0 (back wall) to Z=OUTER_THICKNESS (front). Closed D end at X = -L/2,
# open mouth at X = +L/2.

# Outer body: a stadium prism. RectangleRounded with radius = half the
# width rounds the two short (X) ends to true semicircles. Radius nudged
# 0.001 under W/2 so build123d keeps the straight long edges instead of
# degenerating to an ellipse.
body = extrude(
    RectangleRounded(OUTER_LENGTH, OUTER_WIDTH, OUTER_WIDTH / 2 - 0.001),
    amount=OUTER_THICKNESS,
)

# Centre of the outer D arc, and where the straight side walls begin.
d_center_x = -OUTER_LENGTH / 2 + OUTER_WIDTH / 2

# Channel pocket: a stadium whose closed end is a semicircle concentric
# with the outer D (constant WRAP_WALL all around the back), floored by
# BACK_WALL, ceiled by the lips. Sized so its open end overshoots the
# +X mouth by MOUTH_OVERSHOOT, leaving a clean opening with no thin film.
pocket_w = CHANNEL_WIDTH + FIT_CLEARANCE
pocket_h = CHANNEL_HEIGHT + FIT_CLEARANCE
pocket_r = pocket_w / 2
# Distance from the closed arc centre to the far (mouth) extreme.
pocket_reach = OUTER_LENGTH / 2 + MOUTH_OVERSHOOT - d_center_x
pocket_len = pocket_reach + pocket_r
pocket_cx = d_center_x + pocket_len / 2 - pocket_r
pocket = Pos(pocket_cx, 0, BACK_WALL) * extrude(
    RectangleRounded(pocket_len, pocket_w, pocket_r - 0.001),
    amount=pocket_h,
)

# Mouth window: removes the +Z face between the lips so the jaw's front
# is exposed and only the two Y-edge lips remain. It starts at the
# straight section (d_center_x), so the rounded D end keeps a solid
# front cap like the original. Offset in Y so the +Y lip reads
# LIP_OVERHANG_A and the -Y lip reads LIP_OVERHANG_B.
window_w = CHANNEL_WIDTH - LIP_OVERHANG_A - LIP_OVERHANG_B
window_center_y = (LIP_OVERHANG_B - LIP_OVERHANG_A) / 2
window_len = OUTER_LENGTH / 2 + MOUTH_OVERSHOOT - d_center_x
window = Pos(
    d_center_x,
    window_center_y,
    OUTER_THICKNESS - LIP_THICKNESS,
) * Box(
    window_len,
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
