"""Smoke + invariant tests for the bathroom toothbrush organizer generators."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
PROJECT_3D = REPO_ROOT / "projects" / "bathroom-toothbrush-organizer" / "3d"

BODY_SCRIPT = PROJECT_3D / "organizer.py"
BODY_STL = PROJECT_3D / "out" / "organizer.stl"

LID_SCRIPT = PROJECT_3D / "qtip_lid.py"
LID_STL = PROJECT_3D / "out" / "qtip_lid.stl"


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


def test_body_script_exists():
    assert BODY_SCRIPT.is_file(), f"Missing generator: {BODY_SCRIPT}"


def test_body_produces_valid_stl():
    _run(BODY_SCRIPT, BODY_STL)
    assert BODY_STL.stat().st_size > 50_000, (
        f"Body STL suspiciously small ({BODY_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_body_geometry_invariants():
    if not BODY_STL.exists():
        _run(BODY_SCRIPT, BODY_STL)
    mesh = trimesh.load(str(BODY_STL))
    assert mesh.is_watertight, "Body mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, f"Expected one connected body, got {mesh.body_count}"
    # Nominal outer bounds 188 (X) x 70 (Y) x 80 (Z); reeding adds ~0.5 mm of
    # crest to the X/Y extents. Sorted: depth < height < width.
    depth, height, width = sorted(mesh.extents)
    assert 60 < depth < 78, f"Depth extent out of range: {depth:.1f} mm"
    assert 75 < height < 85, f"Height extent out of range: {height:.1f} mm"
    assert 180 < width < 200, f"Width extent out of range: {width:.1f} mm"


def test_lid_script_exists():
    assert LID_SCRIPT.is_file(), f"Missing generator: {LID_SCRIPT}"


def test_lid_produces_valid_stl():
    _run(LID_SCRIPT, LID_STL)
    assert LID_STL.stat().st_size > 5_000, (
        f"Lid STL suspiciously small ({LID_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_lid_geometry_invariants():
    if not LID_STL.exists():
        _run(LID_SCRIPT, LID_STL)
    mesh = trimesh.load(str(LID_STL))
    assert mesh.is_watertight, "Lid mesh is not watertight"
    assert mesh.body_count == 1, f"Expected one connected body, got {mesh.body_count}"
    # Oval cap 70 (X) x 52 (Y), total height 9 mm. Sorted: height < short < long.
    height, short_axis, long_axis = sorted(mesh.extents)
    assert 7 < height < 12, f"Lid height out of range: {height:.1f} mm"
    assert 46 < short_axis < 58, f"Lid short axis out of range: {short_axis:.1f} mm"
    assert 62 < long_axis < 74, f"Lid long axis out of range: {long_axis:.1f} mm"
