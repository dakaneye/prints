"""Smoke test for the Wowza coin keychain generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "projects" / "wowza-keychain" / "3d" / "keychain.py"
OUT_STL = SCRIPT.parent / "out" / "keychain.stl"


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
        f"keychain.py exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running keychain.py"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_script_produces_valid_stl():
    _run_generator()
    # Empirical output is ~1 MB. 50 KB floor catches catastrophic regressions
    # (empty STL, broken boolean) without breaking on mesh-resolution changes.
    assert OUT_STL.stat().st_size > 50_000, (
        f"STL suspiciously small ({OUT_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_stl_geometry_invariants():
    if not OUT_STL.exists():
        _run_generator()

    mesh = trimesh.load(str(OUT_STL))
    assert mesh.is_watertight, "Keychain mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count} — "
        "geometry likely has disconnected pieces"
    )

    w, d, h = mesh.extents
    # Bounds cover both v1 (45 mm) and v2 (24.5 mm quarter-sized) layouts.
    assert 20 < w < 80, f"Width out of plausible range: {w:.1f} mm"
    assert 20 < d < 80, f"Depth out of plausible range: {d:.1f} mm"
    assert 3 < h < 10, f"Height out of plausible range: {h:.1f} mm"
