# Bathroom Toothbrush Organizer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a parametric scalloped-wall family bathroom organizer (3 manual-brush bores + toothpaste pocket draining through the floor, plus a covered dry q-tip cubby with a lift-off lid).

**Architecture:** Two build123d generators under `projects/bathroom-toothbrush-organizer/3d/`. `organizer.py` builds the body: a rounded-rectangle prism whose perimeter is scalloped by subtracting a ring of vertical circles (concave vertical scallops), then bored with brush/toothpaste pockets (with floor drain holes) and a raised-floor q-tip well. `qtip_lid.py` builds a plug-style lift-off lid for the well. Both export to `out/` and are covered by one smoke/invariant test in `tests/`.

**Tech Stack:** Python 3.13, build123d 0.10.0, trimesh (mesh invariants), pytest. All code validated against the repo `.venv` during planning.

---

## File Structure

```
projects/bathroom-toothbrush-organizer/
├── README.md                 # what it is, print recipe, dimensions
├── print-log.md              # per-print diary (starts empty/first-entry)
└── 3d/
    ├── requirements.txt      # build123d only (per-project authoring venv)
    ├── organizer.py          # body generator → out/organizer.stl
    ├── qtip_lid.py           # lid generator → out/qtip_lid.stl
    └── build_all.py          # runs both siblings
tests/
└── test_bathroom_toothbrush_organizer.py   # smoke + invariants for both parts
```

Conventions this follows (from `conventions.md`): three-section script layout (Parameters / Geometry / Export), output to sibling `out/<script_name>.stl`, IP-neutral naming, raised-relief rule (N/A — no labels here), pre-print orientation review (documented in README). No `downloaded/` dir — this is pure parametric, zero third-party bytes.

---

## Task 1: Project scaffolding

**Files:**
- Create: `projects/bathroom-toothbrush-organizer/3d/requirements.txt`
- Create: `projects/bathroom-toothbrush-organizer/3d/build_all.py`

- [ ] **Step 1: Create the project directories**

Run:
```bash
mkdir -p projects/bathroom-toothbrush-organizer/3d
```

- [ ] **Step 2: Write `requirements.txt`**

Create `projects/bathroom-toothbrush-organizer/3d/requirements.txt`:
```
build123d>=0.10.0
```

- [ ] **Step 3: Write `build_all.py`** (verbatim copy of the repo's standard regenerator)

Create `projects/bathroom-toothbrush-organizer/3d/build_all.py`:
```python
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
```

- [ ] **Step 4: Commit**

```bash
git add projects/bathroom-toothbrush-organizer/3d/requirements.txt projects/bathroom-toothbrush-organizer/3d/build_all.py
git commit -m "build(bathroom-organizer): scaffold project and build_all"
```

---

## Task 2: Organizer body generator (TDD)

**Files:**
- Test: `tests/test_bathroom_toothbrush_organizer.py`
- Create: `projects/bathroom-toothbrush-organizer/3d/organizer.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_bathroom_toothbrush_organizer.py`:
```python
"""Smoke + invariant tests for the bathroom toothbrush organizer generators."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
PROJECT_3D = REPO_ROOT / "projects" / "bathroom-toothbrush-organizer" / "3d"

BODY_SCRIPT = PROJECT_3D / "organizer.py"
BODY_STL = PROJECT_3D / "out" / "organizer.stl"

LID_SCRIPT = PROJECT_3D / "qtip_lid.py"
LID_STL = PROJECT_3D / "out" / "qtip_lid.stl"


def _run(script: Path, out_stl: Path) -> None:
    if out_stl.exists():
        out_stl.unlink()
    result = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{script.name} exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert out_stl.is_file(), f"Expected {out_stl} after running {script.name}"


def test_body_script_exists():
    assert BODY_SCRIPT.is_file(), f"Missing generator: {BODY_SCRIPT}"


def test_body_produces_valid_stl():
    _run(BODY_SCRIPT, BODY_STL)
    assert BODY_STL.stat().st_size > 50_000, (
        f"Body STL suspiciously small ({BODY_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_body_geometry_invariants():
    if not BODY_STL.exists():
        _run(BODY_SCRIPT, BODY_STL)
    mesh = trimesh.load(str(BODY_STL))
    assert mesh.is_watertight, "Body mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count}"
    )
    # Nominal outer bounds 165 (X) x 70 (Y) x 80 (Z); scallops trim X/Y a few mm.
    x, y, z = sorted(mesh.extents)
    assert 60 < x < 75, f"Depth extent out of range: {x:.1f} mm"
    assert 75 < y < 85, f"Height extent out of range: {y:.1f} mm"
    assert 155 < z < 170, f"Width extent out of range: {z:.1f} mm"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/pytest tests/test_bathroom_toothbrush_organizer.py::test_body_script_exists -v`
Expected: FAIL — `Missing generator: .../organizer.py`.

- [ ] **Step 3: Write the body generator**

Create `projects/bathroom-toothbrush-organizer/3d/organizer.py`:
```python
"""Family bathroom organizer with a scalloped outer wall.

A rounded-rectangle prism whose perimeter is fluted with concave vertical
scallops (a ring of circles subtracted from the 2D profile, then extruded).
Two zones share the body:

  * Wet zone (left): three Ø16 brush bores in a back row and one toothpaste
    pocket up front, each with a Ø4 drain hole through the floor so water
    runs straight out the bottom onto the counter/tray below.
  * Dry zone (right end): a q-tip well with its own raised solid floor (no
    drain) so sheeting water can't reach it, capped by the separate
    qtip_lid.py lift-off lid.

Print orientation: upright, as it sits. Every feature is vertical or open at
the top — no bridges, no supports. See README.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Circle,
    Cylinder,
    Pos,
    RectangleRounded,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
WIDTH = 165.0  # X — footprint width
DEPTH = 70.0  # Y — footprint depth
HEIGHT = 80.0  # Z — overall height
CORNER_R = 18.0  # rounded-rect corner radius

SCALLOP_R = 4.0  # groove radius scooped into the perimeter; depth ≈ this
# Scallop centers are spaced ~2·SCALLOP_R along the perimeter so adjacent
# scoops meet at sharp vertical ridges (concave vertical scallops).

FLOOR = 4.0  # solid floor thickness under the wet pockets
DRAIN_D = 4.0  # drain-hole diameter through the floor

BRUSH_D = 16.0  # brush bore diameter (fits adult + kids' manual brushes)
BRUSH_Y = 14.0  # back row, +Y of center
BRUSH_X = (-55.0, -35.0, -15.0)  # three bores across the wet zone

TP_W = 50.0  # toothpaste pocket size (X)
TP_L = 26.0  # toothpaste pocket size (Y)
TP_X = -35.0
TP_Y = -16.0  # front row, -Y of center

QT_D = 42.0  # q-tip well diameter
QT_X = 55.0  # right end
QT_FLOOR = FLOOR + 3.0  # raised solid floor — keeps q-tips dry, no drain hole

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# Scalloped outer profile: subtract a ring of circles centered on the
# rounded-rect perimeter, then extrude once (2D boolean is far faster than 3D).
outline = RectangleRounded(WIDTH, DEPTH, CORNER_R)
perimeter = outline.wires()[0]
n_scallops = max(12, round(perimeter.length / (2 * SCALLOP_R)))
profile = outline
for i in range(n_scallops):
    p = perimeter @ (i / n_scallops)  # normalized point along the perimeter
    profile = profile - Pos(p.X, p.Y) * Circle(SCALLOP_R)
part = extrude(profile, amount=HEIGHT)

# Wet zone: three brush bores down to the floor, each with a floor drain hole.
for cx in BRUSH_X:
    part = part - Pos(cx, BRUSH_Y, FLOOR) * Cylinder(
        BRUSH_D / 2, HEIGHT - FLOOR, align=BOTTOM
    )
    part = part - Pos(cx, BRUSH_Y, 0) * Cylinder(
        DRAIN_D / 2, FLOOR + 1, align=BOTTOM
    )

# Toothpaste pocket (front) with its own floor drain hole.
part = part - Pos(TP_X, TP_Y, FLOOR) * Box(
    TP_W, TP_L, HEIGHT - FLOOR, align=BOTTOM
)
part = part - Pos(TP_X, TP_Y, 0) * Cylinder(DRAIN_D / 2, FLOOR + 1, align=BOTTOM)

# Dry zone: q-tip well with a raised solid floor (no drain hole). Surrounding
# material forms the wall that isolates it from the wet zone.
part = part - Pos(QT_X, 0, QT_FLOOR) * Cylinder(
    QT_D / 2, HEIGHT - QT_FLOOR, align=BOTTOM
)

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "organizer.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/pytest tests/test_bathroom_toothbrush_organizer.py -k body -v`
Expected: 3 passed (`test_body_script_exists`, `test_body_produces_valid_stl`, `test_body_geometry_invariants`).

- [ ] **Step 5: Commit**

```bash
git add tests/test_bathroom_toothbrush_organizer.py projects/bathroom-toothbrush-organizer/3d/organizer.py
git commit -m "feat(bathroom-organizer): add scalloped body generator"
```

---

## Task 3: Q-tip lid generator (TDD)

**Files:**
- Modify: `tests/test_bathroom_toothbrush_organizer.py` (append lid tests)
- Create: `projects/bathroom-toothbrush-organizer/3d/qtip_lid.py`

- [ ] **Step 1: Write the failing tests** — append to `tests/test_bathroom_toothbrush_organizer.py`:
```python
def test_lid_script_exists():
    assert LID_SCRIPT.is_file(), f"Missing generator: {LID_SCRIPT}"


def test_lid_produces_valid_stl():
    _run(LID_SCRIPT, LID_STL)
    assert LID_STL.stat().st_size > 5_000, (
        f"Lid STL suspiciously small ({LID_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_lid_geometry_invariants():
    if not LID_STL.exists():
        _run(LID_SCRIPT, LID_STL)
    mesh = trimesh.load(str(LID_STL))
    assert mesh.is_watertight, "Lid mesh is not watertight"
    assert mesh.body_count == 1, f"Expected one connected body, got {mesh.body_count}"
    # Cap Ø48, plug Ø~41, total height 9 mm. Smallest extent is the height.
    h, d1, d2 = sorted(mesh.extents)
    assert 7 < h < 12, f"Lid height out of range: {h:.1f} mm"
    assert 44 < d1 < 52, f"Lid diameter out of range: {d1:.1f} mm"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `.venv/bin/pytest tests/test_bathroom_toothbrush_organizer.py::test_lid_script_exists -v`
Expected: FAIL — `Missing generator: .../qtip_lid.py`.

- [ ] **Step 3: Write the lid generator**

Create `projects/bathroom-toothbrush-organizer/3d/qtip_lid.py`:
```python
"""Lift-off lid for the organizer's q-tip well.

A plug-style cap: a flat disc that overhangs the well rim and rests on the
body's top face, with a short downward plug that slips into the Ø42 well
(0.8 mm diametral clearance for a hand-fit). Keeps q-tips dry and clean.

Print orientation: cap face down on the bed, plug pointing up — no overhang,
no supports. Diameters here must track QT_D in organizer.py.
"""

from pathlib import Path

from build123d import Align, Cylinder, Pos, export_stl

# ─── Parameters (mm) ──
WELL_D = 42.0  # must match QT_D in organizer.py
CLEARANCE = 0.8  # diametral gap so the plug hand-fits the well

CAP_OVERHANG = 3.0  # cap radius beyond the well, rests on the body top
CAP_THICK = 3.0  # cap disc thickness
PLUG_DEPTH = 6.0  # how far the plug reaches into the well

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

cap = Pos(0, 0, 0) * Cylinder(
    WELL_D / 2 + CAP_OVERHANG, CAP_THICK, align=BOTTOM
)
plug = Pos(0, 0, CAP_THICK) * Cylinder(
    (WELL_D - CLEARANCE) / 2, PLUG_DEPTH, align=BOTTOM
)
part = cap + plug

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "qtip_lid.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
```

- [ ] **Step 4: Run the full test file to verify all pass**

Run: `.venv/bin/pytest tests/test_bathroom_toothbrush_organizer.py -v`
Expected: 6 passed (3 body + 3 lid).

- [ ] **Step 5: Commit**

```bash
git add tests/test_bathroom_toothbrush_organizer.py projects/bathroom-toothbrush-organizer/3d/qtip_lid.py
git commit -m "feat(bathroom-organizer): add q-tip well lift-off lid"
```

---

## Task 4: README, print-log, and full verification

**Files:**
- Create: `projects/bathroom-toothbrush-organizer/README.md`
- Create: `projects/bathroom-toothbrush-organizer/print-log.md`

- [ ] **Step 1: Write the README**

Create `projects/bathroom-toothbrush-organizer/README.md`:
```markdown
# Bathroom toothbrush organizer

A scalloped-wall family bathroom organizer. Holds 3 manual toothbrushes
(1 adult + 2 kids) and a toothpaste tube in an open, draining wet zone, with
a walled-off, covered q-tip cubby that stays dry. Pure parametric (build123d);
the scalloped wall is styled after a q-tip holder the design borrows its look
from. Design history: `docs/superpowers/specs/2026-06-07-bathroom-toothbrush-organizer-design.md`.

## Parts

| Part | Script | Output |
|---|---|---|
| Body | `3d/organizer.py` | `out/organizer.stl` |
| Q-tip lid | `3d/qtip_lid.py` | `out/qtip_lid.stl` |

## Dimensions

- Body: 165 W × 70 D × 80 H mm, 18 mm corner radius
- Brush bores: 3 × Ø16 mm, back row, Ø4 floor drain each
- Toothpaste pocket: 50 × 26 mm, front, Ø4 floor drain
- Q-tip well: Ø42 mm, raised solid floor (no drain)
- Lid: Ø48 mm × 9 mm, plug-fit (0.8 mm clearance)

## Regenerate

```bash
projects/bathroom-toothbrush-organizer/3d/.venv/bin/python projects/bathroom-toothbrush-organizer/3d/build_all.py
```

## Print recipe

- Filament: SUNLU PLA+ 2.0 Oak Wood (select profile manually — no RFID)
- Orientation: body upright as it sits; lid cap-face down, plug up
- Supports: none — every feature is vertical or open at the top
- Settings: 0.2 mm layers, ~15% gyroid infill, 3 walls (keeps the scallop
  grooves strong where they cut into the wall)
- Drainage: the wet zone drains straight through the floor holes onto the
  counter/tray below — there are deliberately no standoff feet (they would
  force a first-layer bridge). A separate nesting drip tray is a possible
  follow-on if lift-off is wanted.
```

- [ ] **Step 2: Write the print-log first entry**

Create `projects/bathroom-toothbrush-organizer/print-log.md`:
```markdown
# Print log — bathroom toothbrush organizer

## Pending first print

- Parts generated, not yet printed.
- Verify before printing: caliper the actual manual brushes against the Ø16
  bores, and confirm the concave vertical scallop look matches the q-tip
  holder it's styled after (groove count/depth tunable via `SCALLOP_R`).
```

- [ ] **Step 3: Regenerate both STLs via build_all and confirm output**

Run:
```bash
.venv/bin/python projects/bathroom-toothbrush-organizer/3d/build_all.py
```
Expected: `All 2 script(s) regenerated successfully.` and two files in `3d/out/`.

- [ ] **Step 4: Run the full test suite**

Run: `.venv/bin/pytest tests/test_bathroom_toothbrush_organizer.py -v`
Expected: 6 passed.

- [ ] **Step 5: Run the linters (matches CI)**

Run: `ruff check projects/bathroom-toothbrush-organizer tests/test_bathroom_toothbrush_organizer.py && ruff format --check projects/bathroom-toothbrush-organizer tests/test_bathroom_toothbrush_organizer.py`
Expected: no errors. (If `ruff format --check` reports a diff, run `ruff format <paths>` and re-stage.)

- [ ] **Step 6: Commit**

```bash
git add projects/bathroom-toothbrush-organizer/README.md projects/bathroom-toothbrush-organizer/print-log.md
git commit -m "docs(bathroom-organizer): add README and print-log"
```

---

## Self-Review notes

- **Spec coverage:** scalloped wall (Task 2 profile loop), 3 brush bores + drains (Task 2), toothpaste pocket + drain (Task 2), dry raised-floor q-tip well (Task 2), lift-off lid (Task 3), no standoff feet / counter-drain (documented Task 4 README), oak filament + upright/no-support recipe (Task 4), smoke tests both parts (Tasks 2–3). All covered.
- **Deviation from spec wording:** spec said "raised rim lip" for lid registration; implemented as a plug-style lid (cap rests on body top, plug enters the well). Functionally equivalent, simpler, prints without supports. Noted here intentionally.
- **Type/name consistency:** `WELL_D` in `qtip_lid.py` must equal `QT_D` in `organizer.py` (both 42.0) — flagged in both files' comments.
- **Validation:** body and lid scripts were run in the repo `.venv` (build123d 0.10.0) during planning — both export watertight, single-body STLs (body 164.5×69.5×80; lid Ø48×9).
```
