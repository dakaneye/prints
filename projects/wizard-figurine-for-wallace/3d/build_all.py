"""Regenerate every STL in this directory.

Runs every sibling *.py (excluding build_all.py itself). Output goes to
each script's local out/ directory.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ME = Path(__file__).name


def main() -> int:
    scripts = sorted(p for p in HERE.glob("*.py") if p.name != ME)
    if not scripts:
        print("No part scripts found.")
        return 0

    failures: list[str] = []
    for script in scripts:
        print(f"\n=== {script.name} ===")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=HERE,
        )
        if result.returncode != 0:
            failures.append(script.name)

    if failures:
        print(f"\nFAILED: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(scripts)} script(s) regenerated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
