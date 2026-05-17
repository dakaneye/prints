# Clamp Jaw Pad Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a pure-parametric `clamp-jaw-pad` project that generates an STL for a slide-on C-channel pad replacing the worn pad on a parallel bar clamp jaw.

**Architecture:** Boolean build123d script (outer stadium prism − channel pocket − mouth window), matching the existing `breaker-panel-clip` pattern. Pure-parametric, no `downloaded/`. Smoke + geometry-invariant test mirrors `tests/test_breaker_panel_clip.py`.

**Tech Stack:** build123d ≥0.10.0 (Python 3.13 venv), pytest, trimesh.

Spec: `docs/superpowers/specs/2026-05-17-clamp-jaw-pad-design.md`.

---

### Task 1: Scaffold the project structure

**Files:**
- Create: `projects/clamp-jaw-pad/3d/requirements.txt`
- Create: `projects/clamp-jaw-pad/3d/out/.gitkeep` (placeholder; `out/` is gitignored, dir must exist for generator)

- [ ] **Step 1: Create directories and requirements**

```bash
mkdir -p projects/clamp-jaw-pad/3d/out
printf 'build123d>=0.10.0\n' > projects/clamp-jaw-pad/3d/requirements.txt
```

- [ ] **Step 2: Verify structure**

Run: `ls -R projects/clamp-jaw-pad`
Expected: `3d/` containing `requirements.txt` and `out/`.

---

### Task 2: Smoke + geometry-invariant test (TDD — write first, must fail)

**Files:**
- Test: `tests/test_clamp_jaw_pad.py`

- [ ] **Step 1: Write the failing test**

```python
"""Smoke test for the clamp-jaw-pad generator."""

import subprocess
import sys
from pathlib import Path

import trimesh

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "projects" / "clamp-jaw-pad" / "3d" / "pad.py"
OUT_STL = SCRIPT.parent / "out" / "pad.stl"


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
        f"pad.py exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert OUT_STL.is_file(), f"Expected {OUT_STL} after running pad.py"


def test_script_exists():
    assert SCRIPT.is_file(), f"Missing generator: {SCRIPT}"


def test_script_produces_valid_stl():
    _run_generator()
    assert OUT_STL.stat().st_size > 5_000, (
        f"STL suspiciously small ({OUT_STL.stat().st_size} bytes) — geometry may be broken"
    )


def test_stl_geometry_invariants():
    if not OUT_STL.exists():
        _run_generator()

    mesh = trimesh.load(str(OUT_STL))
    assert mesh.is_watertight, "Pad mesh is not watertight — would not slice cleanly"
    assert mesh.body_count == 1, (
        f"Expected one connected body, got {mesh.body_count} — "
        "geometry likely has disconnected pieces"
    )

    # Nominal outer bounds 38.67 (X) x 27 (Y) x 10 (Z). Bounds loose
    # enough for ±50 % parameter tweaks without breaking.
    x, y, z = sorted(mesh.extents)
    assert 5 < x < 16, f"Smallest extent (thickness) out of range: {x:.1f} mm"
    assert 14 < y < 41, f"Mid extent (width) out of range: {y:.1f} mm"
    assert 20 < z < 58, f"Largest extent (length) out of range: {z:.1f} mm"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_clamp_jaw_pad.py -v`
Expected: FAIL — `test_script_exists` fails (generator does not exist yet).

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_clamp_jaw_pad.py
git commit -m "test(clamp-jaw-pad): add smoke + geometry-invariant test"
```

---

### Task 3: The generator script (make the test pass)

**Files:**
- Create: `projects/clamp-jaw-pad/3d/pad.py`

- [ ] **Step 1: Write the generator**

```python
"""Slide-on pad for a parallel bar clamp jaw.

Caps the flat steel jaw so metal never touches the workpiece. The jaw
slides in axially through the open mouth and bottoms out against the
solid closed end. The cross-section is a C: a back wall, two side
walls, and two asymmetric lips that curl over the channel and retain
the pad on the jaw's front face. The two short ends are stadium-rounded.

Print orientation: stand on the closed end (slide axis vertical) — no
bridges, no supports. See README.
"""

from pathlib import Path

from build123d import Align, Box, Pos, RectangleRounded, export_stl, extrude

# ─── Parameters (mm) ──
# Measured from the worn original; it currently fits the jaw, so it is
# treated as ground truth.
OUTER_LENGTH = 38.67   # slide axis: closed end → mouth
OUTER_WIDTH = 27.0     # across the lips
OUTER_THICKNESS = 10.0  # back-to-front: BACK_WALL + CHANNEL_HEIGHT + LIP_THICKNESS

CHANNEL_WIDTH = 21.0   # jaw plate width
CHANNEL_HEIGHT = 4.0   # slot the jaw sits in (jaw thickness)

BACK_WALL = 2.0        # solid plate behind the channel
LIP_THICKNESS = 4.0    # Z thickness of each retaining lip
LIP_OVERHANG_A = 2.0   # +Y lip inward reach over the channel
LIP_OVERHANG_B = 3.7   # -Y lip inward reach over the channel
SIDE_WALL = 2.5        # each Y-edge wall
CLOSED_END_WALL = 2.5  # solid stop at the D end

# Added to channel width AND height for slide fit. 0.0 = reproduce as
# measured (tightest PLA grip). Bump up if it will not slide on.
FIT_CLEARANCE = 0.0

# ─── Geometry ──
# X = slide axis, Y = across, Z = back→front. The outer body is centered
# in XY at the origin (RectangleRounded centers there) and extruded from
# Z=0 (back wall) to Z=OUTER_THICKNESS (front). Closed end at X = -L/2,
# open mouth at X = +L/2.

# Outer body: a stadium prism. RectangleRounded with radius = half the
# width rounds the two short (X) ends to true semicircles — no fragile
# edge filtering. Radius nudged 0.001 under W/2 so build123d keeps the
# straight long edges instead of degenerating to an ellipse.
profile = RectangleRounded(OUTER_LENGTH, OUTER_WIDTH, OUTER_WIDTH / 2 - 0.001)
body = extrude(profile, amount=OUTER_THICKNESS)

# Channel pocket: open at the +X mouth, stops CLOSED_END_WALL short of
# the -X closed end, floored by BACK_WALL, ceiled by the lips. Over-long
# in +X by 1 mm so the boolean leaves a clean open mouth (no thin film).
pocket_w = CHANNEL_WIDTH + FIT_CLEARANCE
pocket_h = CHANNEL_HEIGHT + FIT_CLEARANCE
pocket_len = OUTER_LENGTH - CLOSED_END_WALL + 1.0
pocket = Pos(-OUTER_LENGTH / 2 + CLOSED_END_WALL, 0, BACK_WALL) * Box(
    pocket_len,
    pocket_w,
    pocket_h,
    align=(Align.MIN, Align.CENTER, Align.MIN),
)

# Mouth window: removes the +Z face between the lips so the jaw's front
# face is exposed and only the two Y-edge lips remain. Offset in Y so
# the +Y lip reads LIP_OVERHANG_A and the -Y lip reads LIP_OVERHANG_B.
window_w = CHANNEL_WIDTH - LIP_OVERHANG_A - LIP_OVERHANG_B
window_center_y = (LIP_OVERHANG_B - LIP_OVERHANG_A) / 2
window = Pos(
    -OUTER_LENGTH / 2 + CLOSED_END_WALL,
    window_center_y,
    OUTER_THICKNESS - LIP_THICKNESS,
) * Box(
    pocket_len,
    window_w,
    LIP_THICKNESS + 1.0,  # over-tall in +Z so the cut breaks the surface
    align=(Align.MIN, Align.CENTER, Align.MIN),
)

part = body - pocket - window

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "pad.stl"
export_stl(part, str(out_path))
print(f"Wrote {out_path}")
```

- [ ] **Step 2: Set up the project venv and regenerate manually**

Run:
```bash
cd projects/clamp-jaw-pad/3d && python3.13 -m venv .venv && .venv/bin/pip install -q -r requirements.txt && .venv/bin/python pad.py && cd -
```
Expected: `Wrote .../out/pad.stl`, exit 0.

If build123d raises (e.g. `extrude`/`RectangleRounded` import or
signature differs in the installed version), fix the API call in
`pad.py` to the installed build123d's equivalent and re-run until it
writes the STL. Do not change dimensions to work around a CAD error.

- [ ] **Step 3: Run the test suite against it**

Run: `.venv/bin/pytest tests/test_clamp_jaw_pad.py -v`
Expected: all three tests PASS.

- [ ] **Step 4: Lint**

Run: `ruff check projects/clamp-jaw-pad && ruff format --check projects/clamp-jaw-pad`
Expected: no errors. If `ruff format --check` reports the file, run `ruff format projects/clamp-jaw-pad` and re-run the suite.

- [ ] **Step 5: Commit**

```bash
git add projects/clamp-jaw-pad/3d/pad.py projects/clamp-jaw-pad/3d/requirements.txt
git commit -m "feat(clamp-jaw-pad): add slide-on jaw pad generator"
```

---

### Task 4: build_all.py regenerator

**Files:**
- Create: `projects/clamp-jaw-pad/3d/build_all.py`

- [ ] **Step 1: Copy the standard regenerator**

```bash
cp projects/breaker-panel-clip/3d/build_all.py projects/clamp-jaw-pad/3d/build_all.py
```

- [ ] **Step 2: Verify it regenerates the part**

Run: `projects/clamp-jaw-pad/3d/.venv/bin/python projects/clamp-jaw-pad/3d/build_all.py`
Expected: `All 1 script(s) regenerated successfully.`

- [ ] **Step 3: Commit**

```bash
git add projects/clamp-jaw-pad/3d/build_all.py
git commit -m "build(clamp-jaw-pad): add build_all regenerator"
```

---

### Task 5: README and print-log

**Files:**
- Create: `projects/clamp-jaw-pad/README.md`
- Create: `projects/clamp-jaw-pad/print-log.md`

- [ ] **Step 1: Write README.md**

```markdown
# Clamp jaw pad

Slide-on replacement pad for the head of a parallel bar clamp. It caps
the flat steel jaw so the metal never marks the workpiece. The jaw
slides in through the open mouth and bottoms out against the solid
closed (D) end; two asymmetric lips curl over the channel and hold the
pad on the jaw's front face.

Pure-parametric — generated from `3d/pad.py`, no downloaded STL.

## Print recipe

| Filament | Orientation | Supports | Notes |
|---|---|---|---|
| SUNLU PLA+ 2.0 (any color) | Stand on the closed (D) end, slide axis vertical | None | Channel prints vertically — no bridge over the mouth window |

Bambu Studio: select "SUNLU PLA+ 2.0" profile manually. The D-end
footprint is small (27 × 10 mm) — add a brim if the first layer lifts.

**Grip caveat:** the original is a compliant plastic that grips by
flex. PLA+ is rigid and will not flex the same way. The channel is
reproduced as-measured (`FIT_CLEARANCE = 0.0`) for the tightest grip
PLA can give. After a test fit: if it will not slide on, raise
`FIT_CLEARANCE` in 0.2 mm steps; if it slides on but won't stay,
record it in `print-log.md` (a flexible-filament reprint is the real
fix, out of scope here).

## Geometry summary

- Outer body: 38.67 mm (slide) × 27 mm (across) × 10 mm (thick),
  stadium-rounded short ends
- Channel: 21 mm wide × 4 mm tall slot, ~36.2 mm deep
- Lips: 4 mm thick, overhang 2.0 mm (one edge) / 3.7 mm (other)
- Walls: 2.5 mm sides, 2.0 mm back, 2.5 mm closed end

## Files

- `3d/pad.py` — parametric build123d script
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Tweaking

All parameters live at the top of `3d/pad.py`. Common tweaks:

- Won't slide on / too tight: raise `FIT_CLEARANCE` (±0.2 mm)
- Different jaw width or thickness: edit `CHANNEL_WIDTH` / `CHANNEL_HEIGHT`
- Lip grip too weak/strong: edit `LIP_OVERHANG_A` / `LIP_OVERHANG_B`

After editing, regenerate:

```bash
3d/.venv/bin/python 3d/pad.py
```

Output goes to `3d/out/pad.stl`.
```

- [ ] **Step 2: Write print-log.md**

```markdown
# Print log — clamp jaw pad

| Date | Filament | Params changed | Outcome |
|---|---|---|---|
| | | | |
```

- [ ] **Step 3: Commit**

```bash
git add projects/clamp-jaw-pad/README.md projects/clamp-jaw-pad/print-log.md
git commit -m "docs(clamp-jaw-pad): add README and print-log"
```

---

### Task 6: Full-suite verification

- [ ] **Step 1: Run the entire test suite**

Run: `.venv/bin/pytest -q`
Expected: all tests pass, including the three new `test_clamp_jaw_pad` tests. No regressions in other projects.

- [ ] **Step 2: Repo-wide lint (matches CI)**

Run: `ruff check . && ruff format --check .`
Expected: no errors.

- [ ] **Step 3: Confirm no third-party bytes / out artifacts staged**

Run: `git status --porcelain projects/clamp-jaw-pad`
Expected: clean (the `out/` STL and any `.venv` are gitignored; nothing untracked except expected source files already committed).

---

## Self-Review

- **Spec coverage:** topology, coordinate system, all 13 parameters, boolean construction (body/pocket/window), print-orientation rationale, material caveat, deliverables (project dir, pad.py, build_all.py, requirements.txt, README, print-log, test), testing strategy — each maps to Tasks 1–6. No spec gaps.
- **Placeholders:** none — full code/commands in every step. The outer body uses `RectangleRounded` + `extrude` (no fragile edge filtering); Task 3 Step 2 covers adapting the API call if the installed build123d version differs.
- **Type consistency:** STL path `projects/clamp-jaw-pad/3d/out/pad.stl` and `OUT_STL`/`SCRIPT` constants consistent between test and generator; parameter names identical between spec table, generator, and README.
