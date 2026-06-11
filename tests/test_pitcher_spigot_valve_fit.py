"""Assembly guards for the pitcher-spigot-valve (lever-poppet design).

The PETG body feeds a chamber; a TPU stopper rests on a solid seat floor and
seals a Ø6 throat. Importing each generator regenerates its STL, then these
checks assert, in the shared coordinate frame:
  - the body is ONE watertight solid (no loose pieces; holds water),
  - the barrel clears the glass hole,
  - the stopper rests on the seat with no collision,
  - the solid floor stops it falling through the spout,
  - it lifts clear to pour.
"""

import importlib.util
import sys
from pathlib import Path

import trimesh
from build123d import Pos

REPO_ROOT = Path(__file__).parent.parent
SCRIPT_DIR = REPO_ROOT / "projects" / "pitcher-spigot-valve" / "3d"
HOLE_DIA = 15.8


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _overlap_volume(part_a, part_b):
    """Solid intersection volume; build123d returns None/empty for no overlap."""
    inter = part_a & part_b
    return 0.0 if inter is None or len(inter.solids()) == 0 else inter.volume


def test_body_is_one_watertight_solid():
    body = _load("valve_body").body
    assert len(body.solids()) == 1, "body must be a single solid — loose pieces won't print"
    mesh = trimesh.load(str(SCRIPT_DIR / "out" / "valve_body.stl"), force="mesh")
    assert mesh.is_watertight, "body mesh must be watertight (it holds water)"
    assert mesh.body_count == 1, "body mesh must be one connected piece"


def test_barrel_clears_glass_hole():
    vb = _load("valve_body")
    barrel_od = 2 * (vb.BARREL_CORE_R + vb.THREAD_DEPTH / 2)
    assert barrel_od < HOLE_DIA, f"barrel OD {barrel_od:.1f} must clear the {HOLE_DIA} glass hole"


def test_stopper_seats_seals_and_opens():
    body = _load("valve_body").body
    poppet = _load("poppet").poppet
    assert _overlap_volume(body, poppet) < 1.0, "stopper must rest on the seat without colliding"
    assert _overlap_volume(body, Pos(0, 0, -1) * poppet) > 5.0, (
        "solid seat floor must stop the stopper dropping through the throat"
    )
    assert _overlap_volume(body, Pos(0, 0, 5) * poppet) < 1.0, "stopper must lift clear to pour"


def test_pin_passes_through_both_ears_and_lever():
    """The pivot holes must go ALL the way through both yoke ears and the lever
    boss. (A rotated `align=BOTTOM` cylinder silently drills only one side —
    this guards that regression: a pin shaft must clear with no interference.)"""
    from build123d import Cylinder, Rot

    vb = _load("valve_body")
    body, lever = vb.body, _load("lever").lever
    shaft = Pos(vb.PIVOT_X, 0, vb.PIVOT_Z) * (Rot(90, 0, 0) * Cylinder(1.5, 16))
    assert _overlap_volume(shaft, body) < 0.5, "pin must clear a through-hole in BOTH yoke ears"
    assert _overlap_volume(shaft, lever) < 0.5, "pin must clear a through-hole in the lever boss"
