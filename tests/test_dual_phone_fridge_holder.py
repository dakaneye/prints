"""Smoke + invariant tests for the dual phone fridge holder generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
PROJECT_3D = REPO_ROOT / "projects" / "dual-phone-fridge-holder" / "3d"

SCRIPT = PROJECT_3D / "holder.py"
STL = PROJECT_3D / "out" / "holder.stl"


def _run(script: Path, out_stl: Path) -> None:
    if out_stl.exists():
        out_stl.unlink()
    result = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{script.name} exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert out_stl.is_file(), f"Expected {out_stl} after running {script.name}"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_produces_valid_stl():
    _run(SCRIPT, STL)
    assert STL.stat().st_size > 50_000, (
        f"STL suspiciously small ({STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_geometry_invariants():
    if not STL.exists():
        _run(SCRIPT, STL)
    mesh = trimesh.load(str(STL))
    assert mesh.is_watertight, "Mesh is not watertight — would not slice cleanly"

    # Print pose: X = width, Y = depth, Z = height. Derived from parameters
    # in holder.py: plate 189.6 wide × 97.4 tall, plate + pocket depth 18.4.
    x, y, z = mesh.extents
    assert abs(x - 189.6) < 0.1, f"Width {x:.2f}, expected 189.6"
    assert abs(y - 18.4) < 0.1, f"Depth {y:.2f}, expected 18.4"
    assert abs(z - 97.4) < 0.1, f"Height {z:.2f}, expected 97.4"

    # Hollow sanity: pockets + magnet recesses must carve real volume out of
    # the bounding solid, but the part is far from empty either.
    bbox_volume = x * y * z
    assert 0.15 * bbox_volume < mesh.volume < 0.5 * bbox_volume, (
        f"Volume {mesh.volume:.0f} mm³ implausible — pockets may be missing"
    )

    # Both phone cavities exist: a section through each pocket's midplane
    # must show an interior gap at least POCKET_W wide and POCKET_D deep.
    for x_center in (-45.4, 45.4):
        section = mesh.section(plane_normal=[0, 0, 1], plane_origin=[x_center, 0, 55.0])
        assert section is not None, f"No material at z=55 near x={x_center}"

    # Magnet recesses: slicing just inside the back face yields 20 circle
    # loops plus the plate outline.
    back = mesh.section(plane_normal=[0, 1, 0], plane_origin=[0, 0.9, 0])
    loops = len(back.discrete)
    assert loops == 21, f"Expected 21 loops (outline + 20 recesses), got {loops}"
