"""Smoke test for the clamp-jaw-pad generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "projects" / "clamp-jaw-pad" / "3d" / "pad.py"
OUT_STL = SCRIPT.parent / "out" / "pad.stl"


def _run_generator() -> None:
    if OUT_STL.exists():
        OUT_STL.unlink()
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"pad.py exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running pad.py"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_script_produces_valid_stl():
    _run_generator()
    assert OUT_STL.stat().st_size > 5_000, (
        f"STL suspiciously small ({OUT_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_stl_geometry_invariants():
    if not OUT_STL.exists():
        _run_generator()

    mesh = trimesh.load(str(OUT_STL))
    assert mesh.is_watertight, "Pad mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count} — "
        "geometry likely has disconnected pieces"
    )

    # Nominal outer bounds 38.67 (X) x 27 (Y) x 10 (Z). Bounds loose
    # enough for ±50 % parameter tweaks without breaking.
    x, y, z = sorted(mesh.extents)
    assert 5 < x < 16, f"Smallest extent (thickness) out of range: {x:.1f} mm"
    assert 14 < y < 41, f"Mid extent (width) out of range: {y:.1f} mm"
    assert 20 < z < 58, f"Largest extent (length) out of range: {z:.1f} mm"
