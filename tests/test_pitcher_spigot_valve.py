"""Smoke + geometry tests for the pitcher-spigot-valve generators."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT_DIR = REPO_ROOT / "projects" / "pitcher-spigot-valve" / "3d"


def _run(script_name: str) -> Path:
    script = SCRIPT_DIR / script_name
    out_stl = SCRIPT_DIR / "out" / f"{script.stem}.stl"
    if out_stl.exists():
        out_stl.unlink()
    result = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{script_name} exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert out_stl.is_file(), f"Expected {out_stl} after running {script_name}"
    return out_stl


def test_nut_produces_valid_stl():
    out = _run("nut.py")
    assert out.stat().st_size > 5_000, f"nut STL suspiciously small ({out.stat().st_size} bytes)"
    mesh = trimesh.load(str(out))
    assert mesh.is_watertight, "nut mesh not watertight — would not slice cleanly"


def test_body_produces_valid_stl():
    out = _run("body.py")
    assert out.stat().st_size > 20_000, f"body STL suspiciously small ({out.stat().st_size} bytes)"
    mesh = trimesh.load(str(out))
    assert mesh.is_watertight, "body mesh not watertight — would not slice cleanly"
    assert mesh.body_count == 1, f"body should be one connected solid, got {mesh.body_count}"
    assert max(mesh.extents) < 70, f"body unexpectedly large: {mesh.extents}"


def test_plug_produces_valid_stl():
    out = _run("plug.py")
    assert out.stat().st_size > 10_000, f"plug STL suspiciously small ({out.stat().st_size} bytes)"
    mesh = trimesh.load(str(out))
    assert mesh.body_count == 1, f"plug should be one connected solid, got {mesh.body_count}"


def test_retainer_produces_valid_stl():
    out = _run("retainer.py")
    assert out.stat().st_size > 3_000, (
        f"retainer STL suspiciously small ({out.stat().st_size} bytes)"
    )
    mesh = trimesh.load(str(out))
    assert mesh.is_watertight, "retainer mesh not watertight"
