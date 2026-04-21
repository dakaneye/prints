"""Smoke test for the wizard figurine display base generator.

Running base.py should exit 0 and write a non-trivial STL file. This catches
build123d API drift, import breakage, and obvious geometry regressions
(e.g., a subtraction that leaves no remaining solid).
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BASE_SCRIPT = REPO_ROOT / "projects" / "wizard-figurine-for-wallace" / "3d" / "base.py"
OUT_STL = BASE_SCRIPT.parent / "out" / "base.stl"


def test_base_script_exists():
    assert BASE_SCRIPT.is_file(), f"Missing generator: {BASE_SCRIPT}"


def test_base_produces_valid_stl():
    if OUT_STL.exists():
        OUT_STL.unlink()

    result = subprocess.run(
        [sys.executable, str(BASE_SCRIPT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"base.py exited {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running base.py"

    # 90x60x10mm plaque with engravings + recess — empirical output is ~1.5MB.
    # Floor at 10KB catches catastrophic regressions (empty STL, broken boolean)
    # without being tight enough to break on mesh-resolution changes.
    size = OUT_STL.stat().st_size
    assert size > 10_000, f"STL suspiciously small ({size} bytes) — geometry may be broken"
