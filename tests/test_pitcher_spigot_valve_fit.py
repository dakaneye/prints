"""Assembly guards for the pitcher-spigot-valve.

Two layers:

1. Parameter-consistency arithmetic (fast, deterministic) mirroring the design
   contract in docs/superpowers/specs/2026-06-07-pitcher-spigot-valve-design.md.
2. A geometric interference check that reconstructs the body and plug (same
   coordinate frame) and asserts the plug does not collide with the body in any
   rotational position. This catches cross-part collisions the per-part smoke
   tests cannot — e.g. the lever sweeping into the gasket flange.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT_DIR = REPO_ROOT / "projects" / "pitcher-spigot-valve" / "3d"

# ─── Design contract (mm) ──
HOLE_DIA = 15.8
THREAD_CREST_R = 7.65
SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
PLUG_CLEAR = 0.25
LBORE_R = 3.5
BARREL_BORE_R = 5.0
SPOUT_DROP = 18.0
CLEARANCE_TO_BASE = 30.0  # measured: hole bottom → base


# ─── Parameter-consistency arithmetic ──
def test_barrel_clears_glass_hole():
    barrel_od = 2 * THREAD_CREST_R
    assert barrel_od < HOLE_DIA, f"barrel OD {barrel_od} must clear the {HOLE_DIA} glass hole"


def test_plug_fits_seat_with_clearance():
    assert PLUG_CLEAR > 0, "plug must be smaller than the seat"
    assert SEAT_BOT_R - PLUG_CLEAR > LBORE_R + 0.8, (
        "plug wall too thin around the L-bore at the narrow end"
    )


def test_lbore_connects_inlet_and_spout():
    assert LBORE_R <= BARREL_BORE_R, "L-bore wider than the barrel bore"


def test_spout_within_vertical_budget():
    assert SPOUT_DROP < CLEARANCE_TO_BASE, (
        f"spout drop {SPOUT_DROP} exceeds {CLEARANCE_TO_BASE} to the base"
    )


# ─── Geometric interference check ──
def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _overlap_volume(part_a, part_b):
    """Solid intersection volume; build123d returns None for an empty result."""
    inter = part_a & part_b
    return 0.0 if inter is None else inter.volume


def test_plug_does_not_interfere_with_body():
    """Plug must seat and turn without colliding with body material, both
    open (lever toward flange) and closed (lever 90°)."""
    from build123d import Rot

    body = _load("body").body
    plug = _load("plug").plug_final

    for angle in (0, 45, 90):
        vol = _overlap_volume(Rot(0, 0, angle) * plug, body)
        assert vol < 1.0, (
            f"plug collides with body at {angle}° (overlap {vol:.2f} mm^3) — "
            "check lever/flange clearance and plug-seat taper"
        )
