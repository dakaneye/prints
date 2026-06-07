"""Multiboard back-adapter for a community Bessey F-style bar clamp holder.

The holder (MakerWorld 952436) is a wall-mount comb that already grips
F-clamps; its back is a thin (~2 mm) wall — too thin to bolt against.
This adapter is a separate plate that matches the holder's back
footprint (84 × 121 mm), carries the screw-primary Multipoint mount,
and is glued to the holder back. The holder mesh is never modified.

Load: distributed across **4 Multipoint screw mounts** in a 2 × 2 grid
at 50 mm spacing (= 2 × the 25 mm Multipoint pitch — engages 4 tile
points, not one). For ~0.8 kg per clamp × 2 clamps = ~1.6 kg shared
across 4 screw mounts, load per mount is ~0.4 kg in shear. The
Locking Bolts carry the moment; the hex recesses register the
official connectors for anti-rotation only and are deliberately loose
(0.6 mm/side) so any mesh-measurement imprecision is forgiven.

PART = "coupon": one puck (~25 min print) — test-fit your printed
Hook Snap + Locking Bolt before printing the full plate.
PART = "plate": the 84 × 121 × 8 mm back-adapter with 4 mount pucks.

Axes: X horizontal along holder back (84 mm), Z vertical along
holder back (121 mm), Y out from the wall (the adapter thickness).
Y = 0 is the wall-facing face (with the hex socket recesses);
Y = +ADAPTER_T is the holder-side face (glued to holder back).
"""

from pathlib import Path

from build123d import (
    Axis,
    Box,
    Cylinder,
    Plane,
    Polygon,
    Pos,
    export_stl,
    extrude,
    offset,
)

# ─── Parameters ──  (all mm)
PART = "plate"  # "coupon" | "plate"

# Holder back footprint (measured from the supplied STL):
PLATE_W = 84.0  # X along wall
PLATE_H = 121.0  # Z vertical along wall
ADAPTER_T = 8.0  # Y — adapter thickness (gives bolts solid material)

# Multipoint mount grid (2 × 2 at 50 mm = 2 × the 25 mm Multipoint pitch)
MOUNT_PITCH_X = 50.0
MOUNT_PITCH_Z = 50.0

# Screw-primary Multipoint mount — same geometry as clamp_head_cradle.py
SOCKET_OUTLINE = [
    (-8.82, -1.59),
    (-7.50, -2.74),
    (-7.47, -2.76),
    (4.18, -7.53),
    (7.48, -7.53),
    (7.98, -7.30),
    (7.98, -6.37),
    (7.98, 8.46),
    (7.48, 8.70),
    (4.18, 8.70),
    (-6.60, 3.95),
    (-8.07, 3.25),
    (-8.82, 2.76),
]
SOCKET_THICK = 4.5
SOCKET_CLEARANCE = 0.6  # generous — screw holds, hex anti-rotates
SOCKET_DEPTH = SOCKET_THICK + 0.5  # 5.0
BOLT_BORE_D = 5.0  # clearance for Locking Bolt — verify on coupon


def place(shape, *, x=None, y=None, z=None, cx=None, cz=None):
    bb = shape.bounding_box()
    dx = dy = dz = 0.0
    if cx is not None:
        dx = cx - (bb.min.X + bb.max.X) / 2
    if x is not None:
        dx = x - bb.min.X
    if y is not None:
        dy = y - bb.min.Y
    if z is not None:
        dz = z - bb.min.Z
    if cz is not None:
        dz = cz - (bb.min.Z + bb.max.Z) / 2
    return Pos(dx, dy, dz) * shape


def mount_at(part, cx, cz):
    """Cut a hex socket (wall-facing) and a clearance bolt bore at (cx,cz)."""
    prof = offset(Polygon(*SOCKET_OUTLINE), amount=SOCKET_CLEARANCE)
    prism = extrude(Plane.XZ * prof, amount=SOCKET_DEPTH)
    prism = place(prism, cx=cx, cz=cz)
    prism = place(prism, y=0.0)  # recess opens at Y=0 (wall face)
    part = part - prism
    bore = Cylinder(radius=BOLT_BORE_D / 2, height=ADAPTER_T + 2).rotate(Axis.X, 90)
    bore = place(bore, cx=cx, y=-1.0, cz=cz)
    return part - bore


# ─── Geometry ──
if PART == "coupon":
    W, H = 40.0, 40.0
    part = place(Box(W, ADAPTER_T, H), cx=0.0, y=0.0, z=0.0)
    part = mount_at(part, 0.0, H / 2)
else:
    part = place(Box(PLATE_W, ADAPTER_T, PLATE_H), cx=0.0, y=0.0, z=0.0)
    # 2 × 2 grid centred on the plate
    for sx in (-MOUNT_PITCH_X / 2, MOUNT_PITCH_X / 2):
        for sz in (PLATE_H / 2 - MOUNT_PITCH_Z / 2, PLATE_H / 2 + MOUNT_PITCH_Z / 2):
            part = mount_at(part, sx, sz)

# ─── Export ──
out = Path(__file__).parent / "out"
out.mkdir(exist_ok=True)
name = "bessey_adapter_coupon" if PART == "coupon" else "bessey_multiboard_adapter"
export_stl(part, str(out / f"{name}.stl"))
print(f"exported {name}.stl  bbox={part.bounding_box().size}  volume={part.volume:.0f}mm^3")
