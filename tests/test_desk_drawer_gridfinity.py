"""Smoke test for the desk-drawer Gridfinity project.

Runs `build_all.py` (which executes every part script in 3d/) and
validates the produced STLs. The generators depend on
`gridfinity-build123d`, which only lives in the per-project venv. When
the lib is missing in the running interpreter, build_all.py exits 1 with
install instructions — this test verifies that contract and skips the
heavier checks so CI stays green.
"""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
PROJECT_3D = REPO_ROOT / "projects" / "desk-drawer-gridfinity" / "3d"
BUILD_ALL = PROJECT_3D / "build_all.py"
OUT_DIR = PROJECT_3D / "out"
ANY_SCRIPT = PROJECT_3D / "baseplate.py"  # both scripts share the same import gate


def _gridfinity_lib_available() -> bool:
    result = subprocess.run(
        [sys.executable, "-c", "import gridfinity"],
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def _run_build_all() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(BUILD_ALL)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_build_all_exists():
    assert BUILD_ALL.is_file(), f"Missing build_all.py: {BUILD_ALL}"
    assert ANY_SCRIPT.is_file(), f"Missing baseplate.py: {ANY_SCRIPT}"


def test_scripts_exit_cleanly_when_lib_missing():
    if _gridfinity_lib_available():
        return  # Other tests cover the success path.
    result = subprocess.run(
        [sys.executable, str(ANY_SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        f"Expected exit 1 when gridfinity lib missing, got {result.returncode}"
    )
    assert "gridfinity-build123d not installed" in result.stderr, (
        f"Expected install hint on stderr, got:\n{result.stderr}"
    )


def test_build_all_produces_valid_stls():
    if not _gridfinity_lib_available():
        return  # Covered by the lib-missing test above.

    for stl in OUT_DIR.glob("*.stl"):
        stl.unlink()

    result = _run_build_all()
    assert result.returncode == 0, (
        f"build_all.py exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    stls = sorted(OUT_DIR.glob("*.stl"))
    assert len(stls) >= 2, f"Expected at least 2 STLs (baseplate + bin), got {len(stls)}"

    for stl in stls:
        # Even small bins/baseplates are >50 KB; smaller = empty / broken boolean.
        assert stl.stat().st_size > 50_000, (
            f"STL suspiciously small ({stl.stat().st_size} bytes): {stl.name}"
        )

        mesh = trimesh.load(str(stl))
        assert mesh.is_watertight, f"{stl.name} is not watertight"
        assert mesh.body_count == 1, f"{stl.name} has {mesh.body_count} disconnected bodies"

        w, d, h = mesh.extents
        # Footprint: smallest 1x1 cell ~42 mm; largest 6x4 baseplate ~252 mm.
        # Height: baseplate ~5 mm; tallest bin (12U) ~88 mm.
        assert 40 < w < 340, f"{stl.name} width out of range: {w:.1f} mm"
        assert 40 < d < 340, f"{stl.name} depth out of range: {d:.1f} mm"
        assert 3 < h < 100, f"{stl.name} height out of range: {h:.1f} mm"
