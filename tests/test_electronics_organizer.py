"""Smoke tests for the electronics organizer project.

Runs `build_all.py` (which executes every part script in 3d/) and validates
the produced STLs. Generators depend on `gridfinity-build123d`, which only
lives in the per-project venv. When the lib is missing in the running
interpreter, scripts exit 1 with install instructions — the test verifies
that contract and skips the heavier checks so CI stays green.
"""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
PROJECT_3D = REPO_ROOT / "projects" / "electronics-organizer" / "3d"
BUILD_ALL = PROJECT_3D / "build_all.py"
OUT_DIR = PROJECT_3D / "out"
CASE_SCRIPT = PROJECT_3D / "case.py"
BINS_SCRIPT = PROJECT_3D / "bins.py"


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
    assert CASE_SCRIPT.is_file(), f"Missing case.py: {CASE_SCRIPT}"
    assert BINS_SCRIPT.is_file(), f"Missing bins.py: {BINS_SCRIPT}"


def test_scripts_exit_cleanly_when_lib_missing():
    if _gridfinity_lib_available():
        return  # Other tests cover the success path.
    for script in (CASE_SCRIPT, BINS_SCRIPT):
        result = subprocess.run(
            [sys.executable, str(script)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1, (
            f"{script.name}: expected exit 1 when gridfinity lib missing, got {result.returncode}"
        )
        assert "gridfinity-build123d not installed" in result.stderr, (
            f"{script.name}: expected install hint on stderr, got:\n{result.stderr}"
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
    # Expect at least: tote.stl, lid.stl, plus one bin per unique size
    # (1x1 + 1x2 = 2 bin STLs minimum). Floor at 4.
    assert len(stls) >= 4, (
        f"Expected at least 4 STLs (tote, lid, ≥2 bins), got {len(stls)}: {[s.name for s in stls]}"
    )

    names = {s.name for s in stls}
    assert "tote.stl" in names, f"Missing tote.stl in {names}"
    assert "lid.stl" in names, f"Missing lid.stl in {names}"

    for stl in stls:
        # Even small bins are >50 KB; smaller = empty / broken boolean.
        assert stl.stat().st_size > 50_000, (
            f"STL suspiciously small ({stl.stat().st_size} bytes): {stl.name}"
        )

        mesh = trimesh.load(str(stl))
        assert mesh.is_watertight, f"{stl.name} is not watertight"
        assert mesh.body_count == 1, f"{stl.name} has {mesh.body_count} disconnected bodies"

        w, d, h = mesh.extents
        # Bins: 42-180 mm wide, 5-50 mm tall.
        # Tote / lid: ~220 mm × ~225 mm footprint, up to ~50 mm tall.
        assert 40 < w < 260, f"{stl.name} width out of range: {w:.1f} mm"
        assert 40 < d < 260, f"{stl.name} depth out of range: {d:.1f} mm"
        assert 3 < h < 60, f"{stl.name} height out of range: {h:.1f} mm"


def test_tote_and_lid_have_matching_footprint():
    """Lid sleeves over the tote — XY footprint should match within tolerance."""
    if not _gridfinity_lib_available():
        return

    tote_stl = OUT_DIR / "tote.stl"
    lid_stl = OUT_DIR / "lid.stl"
    if not tote_stl.exists() or not lid_stl.exists():
        _run_build_all()

    tote = trimesh.load(str(tote_stl))
    lid = trimesh.load(str(lid_stl))

    tote_w, tote_d, _ = tote.extents
    lid_w, lid_d, _ = lid.extents

    # Lid overlaps the tote externally — should be ~2*wall_thickness wider.
    # Tolerance: lid is 5–10 mm wider/deeper than the tote.
    w_diff = lid_w - tote_w
    d_diff = lid_d - tote_d
    assert 4 < w_diff < 12, (
        f"Lid width ({lid_w:.1f}) vs tote width ({tote_w:.1f}): "
        f"diff {w_diff:.1f} mm — expected 4–12 mm overlap"
    )
    assert 4 < d_diff < 12, (
        f"Lid depth ({lid_d:.1f}) vs tote depth ({tote_d:.1f}): "
        f"diff {d_diff:.1f} mm — expected 4–12 mm overlap"
    )
