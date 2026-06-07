"""Two-clamp head-up holder, Pliers-Holder-style two-loop Multiboard mount.

The holder body is a rectangular prism (36 × 25 × 75) with two
side-by-side pockets, a front slit to slide each clamp in, and a
bottom slot per pocket for the bar to hang through.

Two loop tabs attach to the back face (wall side) and protrude
ABOVE the prism's top edge — same arrangement as the Pliers Holder.
Each tab: 40 mm wide × 38 mm tall × 2 mm thick, flat bottom merged
with the prism's back-top edge, rounded top with a Ø23 mm screw
hole and a Ø30 × 1 mm counterbore.

Loop pitch 50 mm centre-to-centre = 2 × the 25 mm Multipoint pitch.
Mass hangs directly below the screws → pure shear load.

PART = "coupon": one isolated loop tab (~25 min print) for screw fit.
PART = "holder": the full two-clamp holder.

Axes: X horizontal along wall, Y out from wall (Y=0 = wall face),
Z vertical (Z=0 = bottom of holder).
"""

from pathlib import Path

from build123d import Axis, Box, Cylinder, Pos, export_stl

# ─── Parameters ──  (all mm)
PART = "holder"  # "coupon" | "holder"

LOOP_OD = 40.0  # rounded-end diameter
LOOP_ID = 23.0  # screw clearance hole (measured from a printed Pliers Holder)
LOOP_THICK = 2.0  # flat against the wall
CBORE_OD = 30.0  # counterbore on outer face (screw head / connector flange)
CBORE_DEPTH = 1.0
TAB_TOTAL_H = 38.0  # total tab height = stem 18 + semicircle 20
LOOP_PITCH_X = 50.0  # 2 × Multipoint pitch

# Clamp head, measured (head-up vertical):
HEAD_LONG = 85.0
HEAD_WIDE = 27.0
HEAD_THICK = 18.0
BAR_W, BAR_T = 19.5, 6.3

CAPTURE_H = 72.0
POCKET_X = HEAD_WIDE + 3.0
POCKET_Y = HEAD_THICK + 2.0
WALL = 3.0
BASE = 3.0
DIVIDER = 3.0
FRONT_LIP = 10.0
BAR_SLOT_W = BAR_W + 1.5

CRADLE_INNER_X = POCKET_X * 2 + DIVIDER
CRADLE_OUTER_X = CRADLE_INNER_X + 2 * WALL  # 69
CRADLE_OUTER_Y = LOOP_THICK + POCKET_Y + WALL  # 25 — full prism depth incl. back face
CRADLE_OUTER_Z = CAPTURE_H + BASE  # 75

STEM_H = TAB_TOTAL_H - LOOP_OD / 2  # 18


# ─── Geometry ──
def loop_tab(x_offset: float, z_base: float):
    """Vertical tab: flat-bottom stem + semicircle top with screw hole
    and counterbore. Bottom at Z=z_base, centred at X=x_offset, in the
    wall-facing plane (Y = 0 to LOOP_THICK)."""
    stem = Pos(x_offset, LOOP_THICK / 2, z_base + STEM_H / 2) * Box(LOOP_OD, LOOP_THICK, STEM_H)
    disc = Pos(x_offset, LOOP_THICK / 2, z_base + STEM_H) * Cylinder(
        radius=LOOP_OD / 2, height=LOOP_THICK
    ).rotate(Axis.X, 90)
    lower_clip = Pos(x_offset, LOOP_THICK / 2, z_base + STEM_H - LOOP_OD / 4) * Box(
        LOOP_OD + 0.2, LOOP_THICK + 0.2, LOOP_OD / 2
    )
    half_disc = disc - lower_clip
    bore = Pos(x_offset, LOOP_THICK / 2, z_base + STEM_H) * Cylinder(
        radius=LOOP_ID / 2, height=LOOP_THICK + 2
    ).rotate(Axis.X, 90)
    cbore = Pos(x_offset, LOOP_THICK - CBORE_DEPTH / 2, z_base + STEM_H) * Cylinder(
        radius=CBORE_OD / 2, height=CBORE_DEPTH
    ).rotate(Axis.X, 90)
    return (stem + half_disc) - bore - cbore


def holder():
    """Rectangular prism cradle (with pockets + bar slots + front slits)
    plus two loop tabs protruding above the back-top edge."""
    prism = Pos(0, CRADLE_OUTER_Y / 2, CRADLE_OUTER_Z / 2) * Box(
        CRADLE_OUTER_X, CRADLE_OUTER_Y, CRADLE_OUTER_Z
    )
    body = prism
    # back wall thickness inside the prism = LOOP_THICK + WALL = 5 mm
    pocket_y_centre = LOOP_THICK + WALL + POCKET_Y / 2
    for sx in (-(POCKET_X + DIVIDER) / 2, (POCKET_X + DIVIDER) / 2):
        # interior pocket
        body = body - Pos(sx, pocket_y_centre, BASE + CAPTURE_H / 2) * Box(
            POCKET_X, POCKET_Y, CAPTURE_H
        )
        # front slit (above the retaining lip)
        body = body - Pos(
            sx,
            LOOP_THICK + WALL + POCKET_Y + WALL / 2,  # cuts through the front wall
            BASE + FRONT_LIP + (CAPTURE_H - FRONT_LIP) / 2,
        ) * Box(POCKET_X, WALL + 2, CAPTURE_H - FRONT_LIP)
        # bottom bar slot (bar hangs through here)
        body = body - Pos(sx, LOOP_THICK + WALL - 0.5, 0) * Box(BAR_SLOT_W, WALL + 4, BASE * 2 + 1)
    # loops above
    body = body + loop_tab(-LOOP_PITCH_X / 2, CRADLE_OUTER_Z)
    body = body + loop_tab(LOOP_PITCH_X / 2, CRADLE_OUTER_Z)
    return body


if PART == "coupon":
    part = loop_tab(0, 0)
else:
    part = holder()

# ─── Export ──
out = Path(__file__).parent / "out"
out.mkdir(exist_ok=True)
name = "loop_fit_coupon" if PART == "coupon" else "clamp_loop_holder"
export_stl(part, str(out / f"{name}.stl"))
print(f"exported {name}.stl  bbox={part.bounding_box().size}  volume={part.volume:.0f}mm^3")
