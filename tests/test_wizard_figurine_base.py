"""Smoke test for the wizard figurine display base generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "projects" / "wizard-figurine-for-wallace" / "3d" / "base.py"
OUT_STL = SCRIPT.parent / "out" / "base.stl"


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
        f"base.py exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running base.py"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_script_produces_valid_stl():
    _run_generator()
    # 90×60×10 mm plaque + engravings + recess — empirical ~1.5 MB. 10 KB
    # floor catches catastrophic regressions (empty STL, broken boolean).
    assert OUT_STL.stat().st_size > 10_000, (
        f"STL suspiciously small ({OUT_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_stl_geometry_invariants():
    if not OUT_STL.exists():
        _run_generator()

    mesh = trimesh.load(str(OUT_STL))
    assert mesh.is_watertight, "Base mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count} — "
        "engravings or recess may have separated the solid"
    )

    w, d, h = mesh.extents
    # Plaque is 90×60×10 mm — allow ±20 mm tolerance for parameter tweaks.
    assert 70 < w < 110, f"Width out of plausible range: {w:.1f} mm"
    assert 40 < d < 80, f"Depth out of plausible range: {d:.1f} mm"
    assert 8 < h < 15, f"Height out of plausible range: {h:.1f} mm"
