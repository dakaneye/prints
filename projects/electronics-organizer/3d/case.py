"""Electronics organizer — outer tote and friction-fit lid with engraved map.

Layout A (per docs/superpowers/specs/2026-05-09-electronics-organizer-design.md):

    +---------------------------------+
    | [LED reel ø79]   [cap case]     |   ← back row, 88 mm deep
    +----------------+-----------------+
    |                |                 |
    |  Gridfinity    | [header pin]    |   ← front zone, 126 mm deep
    |  3×3 (126×126) |                 |
    |                |   (dead strip)  |
    +----------------+-----------------+

The case has a stepped floor: 3 mm thin floor under Zone A (where the
Gridfinity baseplate sits), and a thicker floor under Zones B/C so the
subcase / reel pockets can recess without breaking through the bottom.

Emits two STLs to ./out/:
- tote.stl — case body with floor, walls, Gridfinity baseplate, wells
- lid.stl — friction-fit sleeve lid with the layout map recessed into the top
"""

from pathlib import Path

# ─── Parameters ──

# Compartment list. Lid label, kind, and *args for size.
#   kind="bin"   → Gridfinity cell, args = (cols, rows)
#   kind="well"  → rectangular well, args = (width_mm, depth_mm, height_mm)
#                  (existing subcase external dims; clearance added in code)
#   kind="reel"  → cylindrical pocket, args = (diameter_mm, depth_mm)
COMPARTMENTS: list[tuple[str, str, tuple]] = [
    ("LEDS", "reel", (75.0, 13.0)),  # WS2812B 5 m reel, lying flat
    ("CAPS", "well", (130.0, 85.0, 22.0)),  # capacitor subcase
    ("HEADERS", "well", (100.0, 65.0, 18.0)),  # header pin subcase, rotated 90° in layout
    ("ESP32", "bin", (1, 2)),
    ("RTC", "bin", (1, 2)),
    ("AMP", "bin", (1, 1)),
    ("uSD", "bin", (1, 1)),
    ("USB-C", "bin", (1, 1)),
    ("BTNS", "bin", (1, 1)),
    ("SPKR", "bin", (1, 1)),
]

# Tote sizing
WALL_THICKNESS = 3.0
FLOOR_THICKNESS = 3.0  # thin floor under Zone A (Gridfinity baseplate sits on top)
ZONE_GAP = 5.0  # spacing between back row and front zone, and between zones

# Well clearance over nominal subcase dims
WELL_CLEARANCE_W = 3.0
WELL_CLEARANCE_D = 3.0
WELL_CLEARANCE_H = 1.0
REEL_CLEARANCE_R = 2.0  # +2 mm in radius (diametric +4 mm)
REEL_CLEARANCE_H = 2.0

# Gridfinity (per spec)
CELL_PITCH = 42.0
BASEPLATE_HEIGHT = 4.75
GRID_COLS = 3
GRID_ROWS = 3
BIN_HEIGHT_U = 6  # 1U = 7 mm; 6U = 42 mm

# Lid
LID_OVERLAP = 6.0  # how far the lid skirt comes down over the tote outer wall
LID_CLEARANCE = 0.30  # XY gap between tote outer wall and lid inner wall (per side)
LID_TOP_THICKNESS = 2.4

# Engraving
ENGRAVE_DEPTH = 0.6
LABEL_FONT = "Arial"  # Bold via FontStyle.BOLD; Liberation Sans on Linux/CI
HEADER_TEXT = "ELECTRONICS"
HEADER_CAP_HEIGHT = 9.0
LABEL_CAP_BIN_1x1 = 4.0
LABEL_CAP_BIN_1x2 = 5.0
LABEL_CAP_WELL = 7.0
PERIMETER_LINE_WIDTH = 0.5


# ─── Geometry ──
try:
    import gridfinity as gf  # type: ignore[import-not-found]
except ImportError as exc:
    raise SystemExit(
        "gridfinity-build123d not installed. Set up the per-project venv:\n"
        "  python3.13 -m venv projects/electronics-organizer/3d/.venv\n"
        "  GIT_CONFIG_GLOBAL=/dev/null projects/electronics-organizer/3d/.venv/bin/pip install "
        "-r projects/electronics-organizer/3d/requirements.txt"
    ) from exc

from build123d import (  # noqa: E402
    Align,
    Box,
    Circle,
    Cylinder,
    FontStyle,
    Polygon,
    Pos,
    Rectangle,
    Text,
    export_stl,
    extrude,
)

# ── Resolve compartment dimensions (with clearance) ──


def _well_size(label: str) -> tuple[float, float, float]:
    for name, kind, args in COMPARTMENTS:
        if name == label and kind == "well":
            w, d, h = args
            return (w + WELL_CLEARANCE_W, d + WELL_CLEARANCE_D, h + WELL_CLEARANCE_H)
    raise KeyError(f"No well named {label!r}")


def _reel_size(label: str) -> tuple[float, float]:
    for name, kind, args in COMPARTMENTS:
        if name == label and kind == "reel":
            dia, h = args
            return (dia + 2 * REEL_CLEARANCE_R, h + REEL_CLEARANCE_H)
    raise KeyError(f"No reel named {label!r}")


LED_DIA, LED_DEPTH = _reel_size("LEDS")
CAP_W, CAP_D, CAP_H = _well_size("CAPS")
HDR_W_NAT, HDR_D_NAT, HDR_H = _well_size("HEADERS")
HDR_W, HDR_D = HDR_D_NAT, HDR_W_NAT  # rotated 90°: long axis runs front-to-back


# ── Layout A: derive coordinates from compartment dimensions ──
# Coordinate system: front-left interior corner at (0, 0), +X right, +Y back.

GRID_W = CELL_PITCH * GRID_COLS  # 126
GRID_D = CELL_PITCH * GRID_ROWS  # 126

BACK_ROW_D = max(LED_DIA, CAP_D)  # back row depth band
INT_W = max(
    LED_DIA + ZONE_GAP + CAP_W,  # back row width
    GRID_W + ZONE_GAP + HDR_W,  # front zone width
)
INT_D = BACK_ROW_D + ZONE_GAP + max(GRID_D, HDR_D)

BACK_CY = INT_D - BACK_ROW_D / 2

# Compartment centers (interior frame)
LED_CX, LED_CY = LED_DIA / 2, BACK_CY
CAP_CX, CAP_CY = LED_DIA + ZONE_GAP + CAP_W / 2, BACK_CY
GRID_CX, GRID_CY = GRID_W / 2, GRID_D / 2
HDR_CX = GRID_W + ZONE_GAP + HDR_W / 2
HDR_CY = GRID_D - HDR_D / 2  # back-aligned within front zone

# Stepped floor: thicker under Zones B/C so wells can recess
DEEP_FLOOR_THICKNESS = FLOOR_THICKNESS + max(CAP_H, HDR_H, LED_DEPTH)
# Outer height: tallest content stack in any zone
#   Zone A: thin floor (3) + baseplate (4.75) + bin (42) = 49.75
#   Zones B/C: items recess into wells, so they don't add above the deep floor
INTERIOR_HEIGHT = FLOOR_THICKNESS + BASEPLATE_HEIGHT + BIN_HEIGHT_U * 7.0 + 0.25  # 50

OUT_W = INT_W + 2 * WALL_THICKNESS
OUT_D = INT_D + 2 * WALL_THICKNESS
OUT_H = INTERIOR_HEIGHT


def _interior(x: float, y: float, z: float = 0.0) -> Pos:
    """Translate from interior-front-left frame to outer-centered frame."""
    return Pos(-INT_W / 2 + x, -INT_D / 2 + y, z)


# ── Tote ──

# Solid outer block, then carve out cavities.
tote = Box(OUT_W, OUT_D, OUT_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

# Full interior cavity at deep floor level — covers Zones B/C correctly. We'll
# punch additional removal in Zone A below to drop its floor back to the thin
# value (so the Gridfinity baseplate has somewhere to sit).
tote -= Pos(0, 0, DEEP_FLOOR_THICKNESS) * Box(
    INT_W,
    INT_D,
    OUT_H - DEEP_FLOOR_THICKNESS + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

# Zone A: thin the floor down from DEEP to FLOOR_THICKNESS in the Gridfinity area.
tote -= _interior(GRID_CX, GRID_CY, FLOOR_THICKNESS) * Box(
    GRID_W,
    GRID_D,
    DEEP_FLOOR_THICKNESS - FLOOR_THICKNESS + 0.01,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)


# Zone A: add the Gridfinity baseplate slab on top of the thin floor.
def _gridfinity_slab():
    grid = [[True] * GRID_COLS for _ in range(GRID_ROWS)]
    bin_feet = gf.Base(grid=grid)
    slab = Box(
        GRID_W,
        GRID_D,
        BASEPLATE_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return slab - bin_feet


tote += _interior(GRID_CX, GRID_CY, FLOOR_THICKNESS) * _gridfinity_slab()

# Zones B/C: cut wells downward from the deep-floor surface. Well bottoms stop
# above z=0 (LED 11mm, header pin 7mm, cap case 3mm — never breaks through).
tote -= _interior(LED_CX, LED_CY, DEEP_FLOOR_THICKNESS - LED_DEPTH) * Cylinder(
    radius=LED_DIA / 2,
    height=LED_DEPTH + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
tote -= _interior(CAP_CX, CAP_CY, DEEP_FLOOR_THICKNESS - CAP_H) * Box(
    CAP_W,
    CAP_D,
    CAP_H + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
tote -= _interior(HDR_CX, HDR_CY, DEEP_FLOOR_THICKNESS - HDR_H) * Box(
    HDR_W,
    HDR_D,
    HDR_H + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)


# ── Lid (friction-fit sleeve) ──

LID_INNER_W = OUT_W + 2 * LID_CLEARANCE
LID_INNER_D = OUT_D + 2 * LID_CLEARANCE
LID_OUTER_W = LID_INNER_W + 2 * WALL_THICKNESS
LID_OUTER_D = LID_INNER_D + 2 * WALL_THICKNESS
LID_H = LID_OVERLAP + LID_TOP_THICKNESS
LID_TOP_Z = LID_H

lid = Box(
    LID_OUTER_W,
    LID_OUTER_D,
    LID_H,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
lid -= Box(
    LID_INNER_W,
    LID_INNER_D,
    LID_OVERLAP + 1.0,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)


# ── Engrave the lid map ──


def _engrave_text(s: str, cap_height: float, x: float, y: float):
    sketch = Pos(x, y, 0) * Text(
        s,
        font_size=cap_height,
        font=LABEL_FONT,
        font_style=FontStyle.BOLD,
        align=(Align.CENTER, Align.CENTER),
    )
    return Pos(0, 0, LID_TOP_Z) * extrude(sketch, amount=-ENGRAVE_DEPTH)


def _engrave_rect_outline(w: float, d: float, x: float, y: float):
    outer = Pos(x, y, 0) * Rectangle(w, d, align=(Align.CENTER, Align.CENTER))
    inner = Pos(x, y, 0) * Rectangle(
        w - 2 * PERIMETER_LINE_WIDTH,
        d - 2 * PERIMETER_LINE_WIDTH,
        align=(Align.CENTER, Align.CENTER),
    )
    return Pos(0, 0, LID_TOP_Z) * extrude(outer - inner, amount=-ENGRAVE_DEPTH)


def _engrave_circle_outline(diameter: float, x: float, y: float):
    outer = Pos(x, y, 0) * Circle(radius=diameter / 2)
    inner = Pos(x, y, 0) * Circle(radius=diameter / 2 - PERIMETER_LINE_WIDTH)
    return Pos(0, 0, LID_TOP_Z) * extrude(outer - inner, amount=-ENGRAVE_DEPTH)


def _interior_to_lid(x: float, y: float) -> tuple[float, float]:
    """Map (x, y) from interior-front-left frame to lid-center XY frame."""
    return (x - INT_W / 2, y - INT_D / 2)


# Header along the back edge of the lid
header_y = INT_D / 2 - HEADER_CAP_HEIGHT - 4.0
lid -= _engrave_text(HEADER_TEXT, HEADER_CAP_HEIGHT, 0.0, header_y)

# Subcase wells and reel — outline + label
for name, kind, args in COMPARTMENTS:
    if kind == "well":
        if name == "CAPS":
            cx, cy = _interior_to_lid(CAP_CX, CAP_CY)
            ow, od = CAP_W, CAP_D
        elif name == "HEADERS":
            cx, cy = _interior_to_lid(HDR_CX, HDR_CY)
            ow, od = HDR_W, HDR_D
        else:
            continue
        lid -= _engrave_rect_outline(ow, od, cx, cy)
        lid -= _engrave_text(name, LABEL_CAP_WELL, cx, cy)
    elif kind == "reel":
        if name == "LEDS":
            cx, cy = _interior_to_lid(LED_CX, LED_CY)
            lid -= _engrave_circle_outline(LED_DIA, cx, cy)
            lid -= _engrave_text(name, LABEL_CAP_WELL, cx, cy)


# Bins on the 3×3 grid. (col, row, w_cells, h_cells) — col 0 = left, row 0 = front.
BIN_PLACEMENT: dict[str, tuple[int, int, int, int]] = {
    "ESP32": (0, 1, 1, 2),
    "RTC": (1, 1, 1, 2),
    "AMP": (2, 2, 1, 1),
    "uSD": (2, 1, 1, 1),
    "USB-C": (0, 0, 1, 1),
    "BTNS": (1, 0, 1, 1),
    "SPKR": (2, 0, 1, 1),
}

for name, kind, args in COMPARTMENTS:
    if kind != "bin":
        continue
    col, row, wc, hc = BIN_PLACEMENT[name]
    cell_cx = (col + wc / 2) * CELL_PITCH
    cell_cy = (row + hc / 2) * CELL_PITCH
    cx, cy = _interior_to_lid(cell_cx, cell_cy)
    cap_h = LABEL_CAP_BIN_1x2 if (wc * hc > 1) else LABEL_CAP_BIN_1x1
    lid -= _engrave_rect_outline(wc * CELL_PITCH, hc * CELL_PITCH, cx, cy)
    lid -= _engrave_text(name, cap_h, cx, cy)


# Orientation marker — small triangle at front-left corner of the lid map,
# matching one on the tote rim (added below).
def _front_left_triangle():
    fx, fy = _interior_to_lid(8.0, 8.0)
    pts = [(fx - 4, fy + 4), (fx + 4, fy + 4), (fx, fy - 4)]
    tri = Polygon(*pts, align=None)
    return Pos(0, 0, LID_TOP_Z) * extrude(tri, amount=-ENGRAVE_DEPTH)


lid -= _front_left_triangle()


# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

tote_path = out_dir / "tote.stl"
lid_path = out_dir / "lid.stl"
export_stl(tote, str(tote_path))
export_stl(lid, str(lid_path))

tote_kb = tote_path.stat().st_size // 1024
lid_kb = lid_path.stat().st_size // 1024

print(f"Wrote {tote_path.name} ({tote_kb} KB)")
print(f"Wrote {lid_path.name} ({lid_kb} KB)")
print(f"Tote outer: {OUT_W:.1f} × {OUT_D:.1f} × {OUT_H:.1f} mm")
print(f"Lid outer:  {LID_OUTER_W:.1f} × {LID_OUTER_D:.1f} × {LID_H:.1f} mm")
