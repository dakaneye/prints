"""Smoke test for the breaker-panel-clip block generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "projects" / "breaker-panel-clip" / "3d" / "block.py"
OUT_STL = SCRIPT.parent / "out" / "block.stl"


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
        f"block.py exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running block.py"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_script_produces_valid_stl():
    _run_generator()
    # 5 KB floor catches catastrophic regressions (empty STL, broken
    # boolean) without breaking on mesh-resolution changes. The part is
    # tiny — a few cm³ — so even a healthy STL is small.
    assert OUT_STL.stat().st_size > 5_000, (
        f"STL suspiciously small ({OUT_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_stl_geometry_invariants():
    if not OUT_STL.exists():
        _run_generator()

    mesh = trimesh.load(str(OUT_STL))
    assert mesh.is_watertight, "Block mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count} — "
        "geometry likely has disconnected pieces"
    )

    w, d, h = mesh.extents
    # Block is 12 wide × (20 + 15 tab) deep × 7.3 tall by default. Bounds
    # are loose enough to allow ±50 % parameter tweaks without breaking.
    assert 6 < w < 25, f"Width out of plausible range: {w:.1f} mm"
    assert 20 < d < 60, f"Depth (block + tab) out of plausible range: {d:.1f} mm"
    assert 4 < h < 12, f"Height out of plausible range: {h:.1f} mm"
