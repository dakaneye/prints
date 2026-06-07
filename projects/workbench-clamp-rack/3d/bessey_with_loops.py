"""Combine the Bessey F-clamp holder STL (untouched) with two Pliers-Holder-style
Multipoint loops attached at the back-top edge.

No modification to the Bessey STL — the loops are generated separately in
build123d, positioned in the Bessey's native coordinate space, then both
meshes are concatenated into a single STL. Slicers treat the result as one
print job; the loops touch the holder along their bottom edge, so the print
fuses them.

Bessey STL bbox (measured): X=[435.45, 519.45], Y=[128.25, 249.25],
Z=[0, 30]. The back face (sparse, mostly flat = wall side) is X=min=435.45;
the top in wall-mount orientation is Z=max=30; above the holder = +Z.
"""

from pathlib import Path

import trimesh
from build123d import Axis, Box, Cylinder, Pos, export_stl

# ─── Parameters ──  (all mm)
BESSEY_STL = Path("/Users/samueldacanay/Downloads/Old+bessey+F+clamp_stls/obj_2_Part 1.stl")

# Bessey-STL native bbox:
BESSEY_X_BACK = 435.45  # X=min face = back (wall side)
BESSEY_Z_TOP = 30.0  # Z=max = top (when wall-mounted)
BESSEY_Y_MID = (128.25 + 249.25) / 2  # 188.75

# Loop dimensions (copied from Pliers Holder loops):
LOOP_OD = 40.0
LOOP_ID = 23.0  # measured from a printed Pliers Holder
LOOP_THICK = 2.0  # flat against the wall
CBORE_OD = 30.0
CBORE_DEPTH = 1.0
TAB_TOTAL_H = 38.0
STEM_H = TAB_TOTAL_H - LOOP_OD / 2  # 18
LOOP_PITCH_Y = 50.0  # 2 × Multipoint pitch (loops spaced along Y axis)


def loop_tab(y_centre: float):
    """One loop tab in Bessey native coords. The tab lies flat against
    the back wall (X = BESSEY_X_BACK plane), extends 2 mm into the
    holder direction (+X), 38 mm tall in +Z above the holder top, 40
    mm wide in Y centred at y_centre. Screw hole + counterbore axis
    along X (the bolt enters from the user side at X = BACK + LOOP_THICK,
    threads into the wall behind at X = BACK)."""
    # Stem: low Z region of the tab
    stem = Pos(
        BESSEY_X_BACK + LOOP_THICK / 2,
        y_centre,
        BESSEY_Z_TOP + STEM_H / 2,
    ) * Box(LOOP_THICK, LOOP_OD, STEM_H)
    # Rounded top: full disc, then clip lower half
    disc = Pos(
        BESSEY_X_BACK + LOOP_THICK / 2,
        y_centre,
        BESSEY_Z_TOP + STEM_H,
    ) * Cylinder(radius=LOOP_OD / 2, height=LOOP_THICK).rotate(Axis.Y, 90)
    lower_clip = Pos(
        BESSEY_X_BACK + LOOP_THICK / 2,
        y_centre,
        BESSEY_Z_TOP + STEM_H - LOOP_OD / 4,
    ) * Box(LOOP_THICK + 0.2, LOOP_OD + 0.2, LOOP_OD / 2)
    half_disc = disc - lower_clip
    # Bore (Ø23 through, axis along X)
    bore = Pos(
        BESSEY_X_BACK + LOOP_THICK / 2,
        y_centre,
        BESSEY_Z_TOP + STEM_H,
    ) * Cylinder(radius=LOOP_ID / 2, height=LOOP_THICK + 2).rotate(Axis.Y, 90)
    # Counterbore on the user-facing side (X = BACK + LOOP_THICK)
    cbore = Pos(
        BESSEY_X_BACK + LOOP_THICK - CBORE_DEPTH / 2,
        y_centre,
        BESSEY_Z_TOP + STEM_H,
    ) * Cylinder(radius=CBORE_OD / 2, height=CBORE_DEPTH).rotate(Axis.Y, 90)
    return (stem + half_disc) - bore - cbore


# ─── Generate each loop separately, then concatenate everything ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
loop1_stl = out_dir / "_loop1.stl"
loop2_stl = out_dir / "_loop2.stl"
export_stl(loop_tab(BESSEY_Y_MID - LOOP_PITCH_Y / 2), str(loop1_stl))
export_stl(loop_tab(BESSEY_Y_MID + LOOP_PITCH_Y / 2), str(loop2_stl))

bessey_mesh = trimesh.load(BESSEY_STL)
loops_mesh = trimesh.util.concatenate([trimesh.load(loop1_stl), trimesh.load(loop2_stl)])
combined = trimesh.util.concatenate([bessey_mesh, loops_mesh])

combined_stl = out_dir / "bessey_with_loops.stl"
combined.export(combined_stl)
print(
    f"bessey + loops -> {combined_stl}\n"
    f"  bessey verts={len(bessey_mesh.vertices)}  "
    f"bbox={bessey_mesh.bounds[1] - bessey_mesh.bounds[0]}\n"
    f"  loops verts={len(loops_mesh.vertices)}    "
    f"bbox={loops_mesh.bounds[1] - loops_mesh.bounds[0]}\n"
    f"  combined verts={len(combined.vertices)}  "
    f"bbox={combined.bounds[1] - combined.bounds[0]}"
)
