"""Smoke tests for the pitcher-spigot-valve generators.

Runs each part's generator and asserts it emits a non-trivial STL. The rigid
printed parts must be watertight single solids (loose pieces won't slice). The
soft seals (gasket, poppet, cap) just need to be valid, non-trivial meshes.
"""

import subprocess
import sys
from pathlib import Path

import pytest
import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT_DIR = REPO_ROOT / "projects" / "pitcher-spigot-valve" / "3d"


def _run(script_name: str) -> Path:
    script = SCRIPT_DIR / script_name
    out_stl = SCRIPT_DIR / "out" / f"{script.stem}.stl"
    if out_stl.exists():
        out_stl.unlink()
    result = subprocess.run(
        [sys.executable, str(script)], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"{script_name} exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert out_stl.is_file(), f"Expected {out_stl} after running {script_name}"
    return out_stl


# (script, min_bytes, must_be_one_watertight_solid)
PARTS = [
    ("valve_body.py", 100_000, True),
    ("poppet.py", 5_000, True),
    ("lever.py", 8_000, True),
    ("cap.py", 5_000, True),
    ("nut.py", 5_000, True),
    ("gasket.py", 5_000, True),
    ("pin.py", 2_000, True),
]


@pytest.mark.parametrize("script,min_bytes,watertight", PARTS)
def test_part_produces_valid_stl(script, min_bytes, watertight):
    out = _run(script)
    size = out.stat().st_size
    assert size > min_bytes, f"{script} STL suspiciously small ({size} bytes)"
    mesh = trimesh.load(str(out))
    if watertight:
        assert mesh.is_watertight, f"{script} mesh not watertight — would not slice cleanly"
        assert mesh.body_count == 1, (
            f"{script} should be one connected solid, got {mesh.body_count}"
        )


def test_body_within_size_budget():
    out = _run("valve_body.py")
    mesh = trimesh.load(str(out))
    assert max(mesh.extents) < 70, f"body unexpectedly large: {mesh.extents}"
