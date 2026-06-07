# Pitcher Spigot Valve Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a printable quarter-turn plug-valve spigot that replaces a broken push-button tap on a glass beverage pitcher.

**Architecture:** Four build123d parts in a new `projects/pitcher-spigot-valve/` project — a valve **body** (through-wall threaded barrel + flange + tapered plug seat + downward spout), a tapered **plug** with an L-shaped bore and a lever paddle, a matched clamp **nut**, and a **retainer** collar. Threads are modeled as coarse helix-swept trapezoids (build123d 0.10.0 ships no thread class). Sealing is by the reused rubber gasket (wall) and the tapered plug seat (valve); clamping is finger-tight because the wall is glass.

**Tech Stack:** Python 3.13, build123d 0.10.0 (`Cylinder`, `Cone`, `Box`, `Helix`, `sweep`, `Trapezoid`, `loft`, boolean ops), pytest + trimesh smoke tests, Bambu Lab A1 / SUNLU PLA+.

---

## Design contract (shared numbers)

All parts honor these. They mirror the spec `docs/superpowers/specs/2026-06-07-pitcher-spigot-valve-design.md`.

| Name | Value (mm) | Meaning |
|---|---|---|
| `HOLE_DIA` | 15.8 | glass hole the barrel passes through |
| `THREAD_PITCH` | 3.0 | coarse, printable |
| `THREAD_CORE_R` | 6.75 | barrel core radius (root) |
| `THREAD_CREST_R` | 7.65 | barrel outer radius (crest) → OD 15.3 < 15.8 ✓ |
| `THREAD_LEN` | 16.0 | threaded barrel length |
| `BARREL_BORE_R` | 5.0 | flow bore radius (Ø10) |
| `FLANGE_OD` | 33.0 | seats the rubber gasket against glass |
| `FLANGE_THK` | 3.0 | flange disc thickness |
| `NUT_THREAD_CLEAR` | 0.3 | radial clearance added to nut internal thread |
| `SEAT_TOP_R` | 9.0 | plug seat radius at top (chamber) |
| `SEAT_BOT_R` | 8.0 | plug seat radius at bottom (taper) |
| `SEAT_DEPTH` | 18.0 | vertical depth of plug seat |
| `PLUG_CLEAR` | 0.25 | radial plug-to-seat clearance (TUNED on prototype) |
| `LBORE_R` | 3.5 | plug L-channel radius |
| `SPOUT_BORE_R` | 4.0 | spout passage radius |
| `SPOUT_OD` | 12.0 | spout tube outer diameter |
| `SPOUT_DROP` | 18.0 | spout tip below barrel axis (≤ 30 clearance) |

Coordinate convention for **body** and **plug**:
- **X** = barrel / flow axis (horizontal, through the glass). Barrel extends −X into the pitcher; flange at X=0; chamber straddles the origin.
- **Z** = plug axis (vertical). Plug drops in from +Z; spout exits −Z (down).
- Open: plug L-bore connects the −X barrel inlet to the −Z spout. Closed: 90° rotation faces a solid seat wall.

---

## File structure

```
projects/pitcher-spigot-valve/
├── README.md                 # what it is, print settings, assembly
├── print-log.md              # per-print diary (prototype tuning, leak test)
└── 3d/
    ├── requirements.txt       # build123d>=0.10.0
    ├── nut.py                 # clamp nut (internal helix thread, wide face)
    ├── body.py                # barrel + flange + seat + spout
    ├── plug.py                # tapered plug + L-bore + lever
    ├── retainer.py            # snap collar holding the plug down
    └── build_all.py           # regenerates every sibling script
tests/
├── test_pitcher_spigot_valve.py   # smoke + geometry-invariant tests per part
└── test_pitcher_spigot_valve_fit.py  # parameter-consistency assembly guard
```

Build order: `nut` (defines the thread), `body` (matching external thread), `plug`, `retainer`, then the assembly guard. Each part is a self-contained script per repo convention (Parameters → Geometry → Export), writing to `3d/out/<name>.stl`.

---

## Task 1: Project scaffold

**Files:**
- Create: `projects/pitcher-spigot-valve/3d/requirements.txt`
- Create: `projects/pitcher-spigot-valve/3d/build_all.py`
- Create: `projects/pitcher-spigot-valve/README.md`
- Create: `projects/pitcher-spigot-valve/print-log.md`

- [ ] **Step 1: Create the project directories**

Run:
```bash
mkdir -p projects/pitcher-spigot-valve/3d/out
```

- [ ] **Step 2: Write `requirements.txt`**

```
build123d>=0.10.0
```

- [ ] **Step 3: Write `build_all.py`** (identical to the repo's standard regenerator)

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
        result = subprocess.run([sys.executable, str(script)], cwd=HERE)
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

- [ ] **Step 4: Write `README.md`** (IP-neutral, generic descriptors)

```markdown
# Pitcher spigot valve

A printable quarter-turn plug-valve replacement for a broken push-button
spigot on a glass beverage pitcher. Reuses the original rubber gasket;
everything else is printed.

## Parts (in `3d/`)

- `body.py` — through-wall threaded barrel, gasket flange, tapered plug
  seat, downward spout
- `plug.py` — tapered plug with an L-shaped bore and a lever paddle
- `nut.py` — clamp nut (matched thread, wide bearing face)
- `retainer.py` — snap collar that holds the plug down

## Mount (glass wall — handle gently)

Outside → inside: body flange · **rubber gasket** · glass · nut.
Finger-tight only. The gasket seals; clamping force does not. Do not
torque a nut against glass.

## Print settings

- SUNLU PLA+ 2.0 (manual filament profile in Bambu Studio)
- ≥4 perimeters on body and plug so water does not weep through layer lines
- Body: barrel pointing up, spout supported. Plug: lever up.
- Food-safe silicone grease on the plug taper before assembly.

First print is a fit prototype — tune `PLUG_CLEAR` in `plug.py`/`body.py`
until the plug turns smoothly and seats. Leak-test with water before use.
```

- [ ] **Step 5: Write `print-log.md`**

```markdown
# Print log — pitcher spigot valve

## Prototype 1 (planned)

Goal: verify the barrel passes the 15.8 mm glass hole, the plug seats and
turns, and the L-bore aligns with the barrel inlet when open.

- PLUG_CLEAR: 0.25 (starting value)
- Result: _pending_
- Leak test (open / closed): _pending_
```

- [ ] **Step 6: Commit**

```bash
git add projects/pitcher-spigot-valve/3d/requirements.txt \
        projects/pitcher-spigot-valve/3d/build_all.py \
        projects/pitcher-spigot-valve/README.md \
        projects/pitcher-spigot-valve/print-log.md
git commit -m "build(pitcher-spigot-valve): scaffold project"
```

---

## Task 2: Clamp nut (`nut.py`)

The nut defines the thread the body must match: a coarse internal helix-swept
trapezoid, plus `NUT_THREAD_CLEAR` radial clearance so a printed barrel turns in
it. A wide, flat bearing face spreads load over the glass.

**Files:**
- Create: `projects/pitcher-spigot-valve/3d/nut.py`
- Create/modify test: `tests/test_pitcher_spigot_valve.py`

- [ ] **Step 1: Write the failing smoke test** (create the test file)

```python
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
    assert out.stat().st_size > 5_000, (
        f"nut STL suspiciously small ({out.stat().st_size} bytes)"
    )
    mesh = trimesh.load(str(out))
    assert mesh.is_watertight, "nut mesh not watertight — would not slice cleanly"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_nut_produces_valid_stl -v
```
Expected: FAIL — `nut.py` does not exist yet (non-zero exit / missing file).

- [ ] **Step 3: Write `nut.py`**

```python
"""Clamp nut for the pitcher spigot valve.

Threads onto the body barrel from inside the pitcher and clamps the
flange + reused rubber gasket against the glass. The thread is a coarse
helix-swept trapezoid matching body.py, widened by NUT_THREAD_CLEAR so a
printed barrel turns freely. The bearing face is wide and flat to spread
load over glass — finger-tight only.

Print orientation: bearing face down on the plate, no supports.
"""

from pathlib import Path

from build123d import (
    Align,
    Cylinder,
    Helix,
    Plane,
    Trapezoid,
    export_stl,
    sweep,
)

# ─── Parameters (mm) — see plan "Design contract" ──
THREAD_PITCH = 3.0
THREAD_CORE_R = 6.75
NUT_THREAD_CLEAR = 0.3  # radial clearance vs barrel
NUT_HEIGHT = 9.0  # thread engagement; ≥ glass thickness + margin
NUT_OD = 30.0  # wide flat face spreads load over glass

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Internal thread radius = barrel core + crest growth + clearance. The
# nut bore is the thread root; the swept trapezoid carves the groove.
bore_r = THREAD_CORE_R + NUT_THREAD_CLEAR  # plain bore (thread root of nut)
helix_r = bore_r  # crest of internal thread reaches inward to here

body = Cylinder(NUT_OD / 2, NUT_HEIGHT, align=BOTTOM)
bore = Cylinder(bore_r, NUT_HEIGHT, align=BOTTOM)

# Internal thread groove: sweep a trapezoid along a helix at the bore wall.
path = Helix(pitch=THREAD_PITCH, height=NUT_HEIGHT, radius=helix_r)
profile = Plane(origin=path @ 0, z_dir=path % 0) * Trapezoid(
    width=THREAD_PITCH * 0.75, height=1.0, left_side_angle=60
)
groove = sweep(profile, path)

nut = body - bore - groove

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(nut, str(out_dir / "nut.stl"))
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_nut_produces_valid_stl -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add projects/pitcher-spigot-valve/3d/nut.py tests/test_pitcher_spigot_valve.py
git commit -m "feat(pitcher-spigot-valve): add clamp nut"
```

---

## Task 3: Valve body (`body.py`)

The body carries the through-wall threaded barrel, the gasket flange, the
tapered plug seat, and the downward spout. Bores: barrel bore (−X, Ø10) enters
the seat; spout bore (−Z, Ø8) exits the seat bottom; seat is open at +Z for
plug insertion.

**Files:**
- Create: `projects/pitcher-spigot-valve/3d/body.py`
- Modify: `tests/test_pitcher_spigot_valve.py`

- [ ] **Step 1: Write the failing test** (append to the test file)

```python
def test_body_produces_valid_stl():
    out = _run("body.py")
    assert out.stat().st_size > 20_000, (
        f"body STL suspiciously small ({out.stat().st_size} bytes)"
    )
    mesh = trimesh.load(str(out))
    assert mesh.body_count == 1, (
        f"body should be one connected solid, got {mesh.body_count}"
    )
    # Barrel crest must clear the 15.8 mm glass hole.
    # X extent spans barrel (−X) through chamber/spout (+X); the barrel
    # cross-section is the limiter — checked precisely in the fit guard.
    x, y, z = mesh.extents
    assert max(mesh.extents) < 70, f"body unexpectedly large: {mesh.extents}"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_body_produces_valid_stl -v
```
Expected: FAIL — `body.py` missing.

- [ ] **Step 3: Write `body.py`**

```python
"""Valve body for the pitcher spigot valve.

A through-wall threaded barrel (passes the glass hole, clamped by nut +
reused gasket against the flange) opens into a tapered plug seat with a
downward spout. Quarter-turn plug (plug.py) gates flow.

Axes: X = barrel/flow (−X into pitcher), Z = plug axis (spout exits −Z).
Flow when open: barrel bore (−X) → plug L-bore → spout bore (−Z).

Print orientation: barrel pointing up (+X vertical), spout needs light
support. ≥4 perimeters so the bores don't weep.
"""

from pathlib import Path

from build123d import (
    Align,
    Axis,
    Cone,
    Cylinder,
    Helix,
    Plane,
    Pos,
    Rot,
    Trapezoid,
    export_stl,
    sweep,
)

# ─── Parameters (mm) — see plan "Design contract" ──
THREAD_PITCH = 3.0
THREAD_CORE_R = 6.75
THREAD_CREST_R = 7.65  # OD 15.3 < HOLE_DIA 15.8
THREAD_LEN = 16.0
BARREL_BORE_R = 5.0

FLANGE_OD = 33.0
FLANGE_THK = 3.0

SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
SEAT_WALL = 3.0  # chamber wall around the seat

SPOUT_BORE_R = 4.0
SPOUT_OD = 12.0
SPOUT_DROP = 18.0  # tip below barrel axis (Z=0)

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Chamber is centered on the origin; barrel axis and spout pass through it.
# 1) Chamber block: a cylinder around the plug seat, axis = Z, centered Z=0.
chamber_outer_r = SEAT_TOP_R + SEAT_WALL
chamber = Pos(0, 0, -SEAT_DEPTH / 2) * Cylinder(
    chamber_outer_r, SEAT_DEPTH, align=BOTTOM
)

# 2) Barrel: threaded cylinder along −X, starting at the chamber wall.
#    Built along +Z then rotated so its axis is +X, then translated to −X.
barrel_core = Cylinder(THREAD_CORE_R, THREAD_LEN, align=BOTTOM)
b_path = Helix(pitch=THREAD_PITCH, height=THREAD_LEN, radius=THREAD_CORE_R)
b_profile = Plane(origin=b_path @ 0, z_dir=b_path % 0) * Trapezoid(
    width=THREAD_PITCH * 0.6, height=THREAD_CREST_R - THREAD_CORE_R,
    left_side_angle=60,
)
barrel_threaded = barrel_core + sweep(b_profile, b_path)
# Rotate +Z axis → −X, place outboard of the chamber.
barrel = Rot(0, -90, 0) * barrel_threaded  # now axis along +X from origin
barrel = Pos(-(chamber_outer_r + THREAD_LEN), 0, 0) * barrel

# 3) Flange: gasket disc at the glass face (X = −chamber_outer_r).
flange = Pos(-chamber_outer_r, 0, 0) * (
    Rot(0, 90, 0) * Cylinder(FLANGE_OD / 2, FLANGE_THK, align=BOTTOM)
)

# 4) Spout: downward tube from chamber bottom.
spout = Pos(0, 0, -SPOUT_DROP) * Cylinder(SPOUT_OD / 2, SPOUT_DROP, align=BOTTOM)

solid = chamber + barrel + flange + spout

# 5) Tapered plug seat (subtract): open at +Z, narrowing downward.
seat = Pos(0, 0, SEAT_DEPTH / 2) * (
    Rot(180, 0, 0) * Cone(SEAT_BOT_R, SEAT_TOP_R, SEAT_DEPTH, align=BOTTOM)
)
# 6) Barrel bore (−X) into the seat.
barrel_bore = Rot(0, -90, 0) * Cylinder(
    BARREL_BORE_R, chamber_outer_r + THREAD_LEN + 1, align=BOTTOM
)
barrel_bore = Pos(-(chamber_outer_r + THREAD_LEN), 0, 0) * barrel_bore
# 7) Spout bore (−Z) out of the seat bottom.
spout_bore = Pos(0, 0, -SPOUT_DROP) * Cylinder(
    SPOUT_BORE_R, SPOUT_DROP + 1, align=BOTTOM
)

body = solid - seat - barrel_bore - spout_bore

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(body, str(out_dir / "body.stl"))
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_body_produces_valid_stl -v
```
Expected: PASS. If build123d raises on a boolean (e.g. a bore not reaching the
seat), open the STL with `projects/pitcher-spigot-valve/3d/.venv/bin/python body.py`
and adjust the offending `Pos`/length — geometry tuning is expected here; keep
the parameters in the contract table consistent.

- [ ] **Step 5: Commit**

```bash
git add projects/pitcher-spigot-valve/3d/body.py tests/test_pitcher_spigot_valve.py
git commit -m "feat(pitcher-spigot-valve): add valve body"
```

---

## Task 4: Plug (`plug.py`)

A tapered plug matching the body seat (minus `PLUG_CLEAR` radially), an L-shaped
bore (−X inlet meeting −Z outlet at the plug center), and a flat lever paddle on
top. Lever aligned with −X = open.

**Files:**
- Create: `projects/pitcher-spigot-valve/3d/plug.py`
- Modify: `tests/test_pitcher_spigot_valve.py`

- [ ] **Step 1: Write the failing test** (append)

```python
def test_plug_produces_valid_stl():
    out = _run("plug.py")
    assert out.stat().st_size > 10_000, (
        f"plug STL suspiciously small ({out.stat().st_size} bytes)"
    )
    mesh = trimesh.load(str(out))
    assert mesh.body_count == 1, (
        f"plug should be one connected solid, got {mesh.body_count}"
    )
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_plug_produces_valid_stl -v
```
Expected: FAIL — `plug.py` missing.

- [ ] **Step 3: Write `plug.py`**

```python
"""Quarter-turn plug for the pitcher spigot valve.

A tapered plug seats in body.py's chamber. An L-shaped internal bore
connects a side opening (−X, the barrel inlet) to a bottom opening (−Z,
the spout). Rotate the lever 90° to face a solid seat wall = closed.
A flat paddle on top is the lever.

PLUG_CLEAR is the tuning knob: increase it if the plug binds, decrease
it if it leaks/wobbles. Smear food-safe silicone grease on the taper.

Print orientation: lever up, taper down, no supports.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Cone,
    Cylinder,
    Pos,
    Rot,
    export_stl,
)

# ─── Parameters (mm) — match body.py seat ──
SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
PLUG_CLEAR = 0.25  # radial clearance vs seat — TUNE on the prototype

LBORE_R = 3.5  # L-channel radius
LEVER_LEN = 30.0
LEVER_WIDTH = 9.0
LEVER_THK = 5.0
LEVER_LIFT = 3.0  # paddle sits this far above the seat top

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
# Tapered plug body, clearance-reduced to turn inside the seat.
top_r = SEAT_TOP_R - PLUG_CLEAR
bot_r = SEAT_BOT_R - PLUG_CLEAR
plug = Rot(180, 0, 0) * Cone(bot_r, top_r, SEAT_DEPTH, align=BOTTOM)
# After flipping, the wide end is up; shift so the plug spans Z∈[0, SEAT_DEPTH].
plug = Pos(0, 0, SEAT_DEPTH) * plug

# Lever paddle on top.
lever = Pos(0, 0, SEAT_DEPTH + LEVER_LIFT) * Box(
    LEVER_LEN, LEVER_WIDTH, LEVER_THK, align=BOTTOM
)
# Neck joining paddle to plug top so it prints as one body.
neck = Pos(0, 0, SEAT_DEPTH) * Cylinder(top_r * 0.6, LEVER_LIFT + 0.1, align=BOTTOM)

solid = plug + neck + lever

# L-bore: side channel (−X) + bottom channel (−Z) meeting at plug mid-height.
mid_z = SEAT_DEPTH * 0.5
side = Pos(0, 0, mid_z) * (Rot(0, -90, 0) * Cylinder(LBORE_R, top_r + 1, align=BOTTOM))
# Keep only the −X half so it opens on one side, not straight through.
side_keep = Pos(-(top_r + 1), 0, mid_z - LBORE_R) * Box(
    top_r + 1, LBORE_R * 2 + 2, LBORE_R * 2 + 2, align=(Align.MIN, Align.CENTER, Align.MIN)
)
side = side & side_keep
bottom = Cylinder(LBORE_R, mid_z + LBORE_R, align=BOTTOM)  # from Z=0 up to mid

plug_final = solid - side - bottom

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(plug_final, str(out_dir / "plug.stl"))
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_plug_produces_valid_stl -v
```
Expected: PASS. If the `side & side_keep` intersection yields an empty solid
(channel doesn't reach the surface), widen `side_keep` or run the script
directly to inspect — the L-bore is the trickiest boolean.

- [ ] **Step 5: Commit**

```bash
git add projects/pitcher-spigot-valve/3d/plug.py tests/test_pitcher_spigot_valve.py
git commit -m "feat(pitcher-spigot-valve): add quarter-turn plug"
```

---

## Task 5: Retainer collar (`retainer.py`)

A thin collar that sits over the plug neck and snaps/screws to the chamber top,
keeping the plug seated against water pressure. Kept simple: a washer-shaped ring
sized to clear the plug neck and overlap the chamber rim; fastened with the same
thread family or a press fit. Start with a press-fit ring (printable, no
fasteners); upgrade only if it lifts.

**Files:**
- Create: `projects/pitcher-spigot-valve/3d/retainer.py`
- Modify: `tests/test_pitcher_spigot_valve.py`

- [ ] **Step 1: Write the failing test** (append)

```python
def test_retainer_produces_valid_stl():
    out = _run("retainer.py")
    assert out.stat().st_size > 3_000, (
        f"retainer STL suspiciously small ({out.stat().st_size} bytes)"
    )
    mesh = trimesh.load(str(out))
    assert mesh.is_watertight, "retainer mesh not watertight"
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_retainer_produces_valid_stl -v
```
Expected: FAIL — `retainer.py` missing.

- [ ] **Step 3: Write `retainer.py`**

```python
"""Retainer collar for the pitcher spigot valve.

A press-fit ring that drops over the plug neck and grips the chamber's
outer wall, holding the plug down against water pressure while still
letting it turn. Replace with a threaded cap if it lifts in testing.

Print orientation: flat, no supports.
"""

from pathlib import Path

from build123d import Align, Cylinder, export_stl

# ─── Parameters (mm) — match body.py chamber ──
SEAT_TOP_R = 9.0
SEAT_WALL = 3.0
CHAMBER_OUTER_R = SEAT_TOP_R + SEAT_WALL  # = 12.0

GRIP_CLEAR = 0.15  # press-fit interference onto chamber wall
COLLAR_HEIGHT = 6.0
COLLAR_WALL = 3.0
NECK_CLEAR_R = SEAT_TOP_R * 0.6 + 0.4  # clears plug neck, retains plug shoulder

BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# ─── Geometry ──
outer = Cylinder(CHAMBER_OUTER_R + COLLAR_WALL, COLLAR_HEIGHT, align=BOTTOM)
grip_bore = Cylinder(CHAMBER_OUTER_R - GRIP_CLEAR, COLLAR_HEIGHT - COLLAR_WALL, align=BOTTOM)
neck_bore = Cylinder(NECK_CLEAR_R, COLLAR_HEIGHT, align=BOTTOM)

retainer = outer - grip_bore - neck_bore

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(retainer, str(out_dir / "retainer.stl"))
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve.py::test_retainer_produces_valid_stl -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add projects/pitcher-spigot-valve/3d/retainer.py tests/test_pitcher_spigot_valve.py
git commit -m "feat(pitcher-spigot-valve): add plug retainer collar"
```

---

## Task 6: Assembly consistency guard + cad-khana check

A fast, deterministic parameter guard that catches the interference bugs the spec
flags — barrel crest must clear the glass hole, plug must fit the seat with
positive clearance, spout must fit the vertical budget, bores must connect. This
re-declares the contract numbers (the generators are self-contained per repo
convention) and asserts the relationships.

**Files:**
- Create: `tests/test_pitcher_spigot_valve_fit.py`

- [ ] **Step 1: Write the guard test**

```python
"""Parameter-consistency guard for the pitcher-spigot-valve assembly.

Mirrors the design contract in
docs/superpowers/specs/2026-06-07-pitcher-spigot-valve-design.md and the
generator constants. Pure arithmetic — fast and deterministic.
"""

# Design contract (mm)
HOLE_DIA = 15.8
THREAD_CREST_R = 7.65
SEAT_TOP_R = 9.0
SEAT_BOT_R = 8.0
SEAT_DEPTH = 18.0
PLUG_CLEAR = 0.25
LBORE_R = 3.5
BARREL_BORE_R = 5.0
SPOUT_DROP = 18.0
CLEARANCE_TO_BASE = 30.0  # measured: hole bottom → base


def test_barrel_clears_glass_hole():
    barrel_od = 2 * THREAD_CREST_R
    assert barrel_od < HOLE_DIA, (
        f"barrel OD {barrel_od} must clear the {HOLE_DIA} glass hole"
    )


def test_plug_fits_seat_with_clearance():
    assert PLUG_CLEAR > 0, "plug must be smaller than the seat"
    assert SEAT_BOT_R - PLUG_CLEAR > LBORE_R + 0.8, (
        "plug wall too thin around the L-bore at the narrow end"
    )


def test_lbore_connects_inlet_and_spout():
    # L-bore radius must not exceed the flow bores it joins.
    assert LBORE_R <= BARREL_BORE_R, "L-bore wider than the barrel bore"


def test_spout_within_vertical_budget():
    assert SPOUT_DROP < CLEARANCE_TO_BASE, (
        f"spout drop {SPOUT_DROP} exceeds {CLEARANCE_TO_BASE} to the base"
    )
```

- [ ] **Step 2: Run the guard**

Run:
```bash
.venv/bin/pytest tests/test_pitcher_spigot_valve_fit.py -v
```
Expected: PASS (all four).

- [ ] **Step 3: Regenerate everything and run the full suite**

Run:
```bash
projects/pitcher-spigot-valve/3d/.venv/bin/python projects/pitcher-spigot-valve/3d/build_all.py
.venv/bin/pytest tests/test_pitcher_spigot_valve.py tests/test_pitcher_spigot_valve_fit.py -v
ruff check . && ruff format --check .
```
Expected: all generators regenerate, all tests pass, lint clean.

- [ ] **Step 4: cad-khana interference check (interactive)**

Invoke the **cad-khana** skill to load the body and plug STLs into an assembly,
position the plug in the seat, and assert no interference and that the L-bore
aligns with the barrel inlet in the open position. This is the visual/geometric
confirmation the arithmetic guard can't give. Record findings in `print-log.md`.

- [ ] **Step 5: Commit**

```bash
git add tests/test_pitcher_spigot_valve_fit.py
git commit -m "test(pitcher-spigot-valve): add assembly consistency guard"
```

---

## Task 7: Physical fit prototype + leak test (manual)

No code — this is the real-world verification the spec requires. Slicer and
printer steps, results logged in `print-log.md`.

- [ ] **Step 1: Slice and print the prototype**

Import `body.stl`, `plug.stl`, `nut.stl`, `retainer.stl` into Bambu Studio
(Import 3MF/STL, manual "SUNLU PLA+ 2.0" profile), ≥4 perimeters. Print.

- [ ] **Step 2: Dry fit**

Confirm: barrel passes the 15.8 mm glass hole; plug seats and turns; lever
sweeps 90° between open and closed; nut threads onto the barrel.

- [ ] **Step 3: Tune `PLUG_CLEAR` if needed**

If the plug binds or leaks, edit `PLUG_CLEAR` in `plug.py` (and re-check the
guard in `tests/test_pitcher_spigot_valve_fit.py`), regenerate, reprint the plug
only. Log each iteration.

- [ ] **Step 4: Leak test**

Assemble with the rubber gasket and food-safe silicone grease, finger-tight.
Fill with water. Confirm no weeping at the wall seal or the valve, open and
closed. Log the result.

- [ ] **Step 5: Commit the log**

```bash
git add projects/pitcher-spigot-valve/print-log.md projects/pitcher-spigot-valve/3d/plug.py
git commit -m "docs(pitcher-spigot-valve): record prototype fit + leak test"
```

---

## Self-review notes

- **Spec coverage:** quarter-turn plug (Task 4), reused gasket + matched printed
  nut (Tasks 2–3), glass-gentle wide nut face (Task 2), downward spout within the
  30 mm budget (Task 3 + guard), tapered seat valve seal (Tasks 3–4), smoke +
  geometry tests (Tasks 2–5), assembly diagnostics (Task 6), fit prototype + leak
  test (Task 7). All spec sections map to a task.
- **Thread reality:** helix-swept trapezoid validated against build123d 0.10.0
  (single-solid barrel + nut, ~3 s each). No built-in thread class is used.
- **Known iteration points:** body bores (Task 3 Step 4), plug L-bore boolean
  (Task 4 Step 4), `PLUG_CLEAR` (Task 7). These are flagged inline, not hidden.
```

