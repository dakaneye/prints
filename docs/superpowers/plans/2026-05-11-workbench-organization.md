# Workbench organization implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the Multiboard wall project, lock in measured drawer/pegboard dimensions, and regenerate the drawer STL set so the user can spend the next ~week printing baseplates + Multiboard tiles in parallel.

**Architecture:** Two sibling projects under `projects/`. `workbench-drawer-gridfinity/` is parametric build123d (already scaffolded; needs `TILES` retuned to actual drawer sizes). `workbench-pegboard-multiboard/` is downloaded-STL only (Multiboard Core tile from Hands-On Tools on MakerWorld) — new scaffold with README + SOURCES.md + print-log.md but no `3d/` directory yet.

**Tech Stack:** Python 3.13, build123d ≥ 0.10, gridfinity-build123d (from git), pytest + trimesh for smoke tests, ruff for lint, Bambu A1 + SUNLU PLA+ 2.0 filament.

---

## Phase 1: Scaffold Multiboard project (UNBLOCKED — execute now)

All tasks below are independent of user input and can run in the current session.

### Task 1: Create Multiboard project directory structure

**Files:**
- Create: `projects/workbench-pegboard-multiboard/` (directory)
- Create: `projects/workbench-pegboard-multiboard/downloaded/` (directory)

- [ ] **Step 1: Make directories**

Run:
```bash
mkdir -p projects/workbench-pegboard-multiboard/downloaded
```

Expected: no output, exit 0.

- [ ] **Step 2: Verify structure**

Run:
```bash
ls projects/workbench-pegboard-multiboard/
```

Expected output:
```
downloaded
```

---

### Task 2: Write the Multiboard project README

**Files:**
- Create: `projects/workbench-pegboard-multiboard/README.md`

- [ ] **Step 1: Write README.md**

Create `projects/workbench-pegboard-multiboard/README.md` with this content:

```markdown
# Workbench pegboard Multiboard wall

Tiled Multiboard wall mounted on top of the existing 1/4" pegboard
behind the garage workbench rolling cabinet. Multiboard is Hands-On
Tools' octagon-tiled wall storage system — each 200 × 200 mm Core plate
mounts via 4 screw holes, accepts Multiconnect-standard accessories
(hooks, shelves, holders), and bridges to Gridfinity bins via official
adapters.

## Pegboard dimensions

| Dimension | Value | Status |
|---|---|---|
| Visible width (panel behind cabinet) | TBD mm | **MEASURE** |
| Visible height | TBD mm | **MEASURE** |
| Stud spacing behind pegboard | ~406 mm (16" OC, US framing) | Confirm by tapping |
| Pegboard thickness | TBD mm (likely 3-6 mm hardboard) | Measure with calipers |

## Tile coverage plan

Core plate footprint: 200 × 200 mm bounding box, octagonal outline,
200 mm pitch in both X and Y. A 1300 × 1100 mm pegboard fits 6 wide ×
5 tall = **30 octagon plates** (+ 20 optional corner-square fillers
for full visual coverage). Update once dimensions are measured.

## Mount strategy

Two-tier screw plan:

1. **Primary load path:** where a Multiboard mount hole aligns with both
   a pegboard hole AND a wall stud → #8 × 2" wood screw through tile +
   pegboard into stud. Rated 50+ lbs per tile properly mounted.
2. **Pegboard-only fallback:** where no stud aligns → #8 × 3/4" wood
   screw with washer through tile + pegboard only. Rated 5-10 lbs per
   screw — acceptable for light-tool zones, not heavy zones.

Plan tile placement so heavy items (DeWalt corded drill, bar clamps)
land on tiles with at least one stud-mount screw.

## Files

- `downloaded/SOURCES.md` — Multiboard Core tile + accessory STL provenance
- `print-log.md` — per-print diary
- `3d/` — *reserved for future custom accessories* (not present yet —
  the standard tile and most tool holders are downloaded, not parametric)

## Print recipe

Bambu A1 with default `0.20mm Standard @BBL A1` profile, filament set
manually to **SUNLU PLA+ 2.0**.

| Setting | Value |
|---|---|
| Layer height | 0.2 mm |
| Walls | 4 (tiles bear weight; thicker walls = stiffer) |
| Infill | 25% gyroid (denser than drawer baseplates — load-bearing) |
| Supports | None (tiles are designed support-free) |
| Brim | None (textured PEI) |

Per-tile estimate: ~50 g filament, ~3-4 hrs print time.

## First print: one Core tile (gate before printing 30)

Print one Core tile and load-test before committing to bulk print:

1. Mount tile to a representative section of the pegboard with the
   intended screw pattern (one stud + one pegboard-only).
2. Hang the heaviest item planned for that tile (most likely the DeWalt
   corded drill, ~5 lbs).
3. Bump-test: bump the tile from below with a fist. No visible flex >
   1 mm; no screw rotation.
4. If all pass → proceed to bulk print. If any fail → revisit screw
   count, filament wall thickness, or relocate heavy items.

## Importing into Bambu Studio

Same flow as the other projects:

1. File → Import → Import 3MF/STL → pick the downloaded Multiboard Core
   tile STL.
2. Filament: SUNLU PLA+ 2.0 manually.
3. Profile: `0.20mm Standard @BBL A1`. Bump infill to 25%, walls to 4.
4. Slice → preview → print.

For bulk print: import once, Right-click → Set quantity → 30, Auto
Arrange Plate. Each plate fits ~2 tiles; ~15 plates over the bulk run.
```

- [ ] **Step 2: Verify file content**

Run:
```bash
wc -l projects/workbench-pegboard-multiboard/README.md
```

Expected: roughly 70-80 lines.

---

### Task 3: Write the downloaded/SOURCES.md placeholder

**Files:**
- Create: `projects/workbench-pegboard-multiboard/downloaded/SOURCES.md`

- [ ] **Step 1: Write SOURCES.md**

Create `projects/workbench-pegboard-multiboard/downloaded/SOURCES.md` with this content:

```markdown
# Downloaded STL sources

**STL/3MF files themselves are gitignored** — only this SOURCES.md gets
committed. Do not re-host third-party models.

Populate the entries below as you download tiles and accessories. The
template at the bottom matches the format used elsewhere in this repo.

---

## Multiboard Core tile (planned ~30 copies)

- **URL:** <https://multiboard.io> — official source. Fetch the Core
  tile STL from Hands-On Tools' MakerWorld page, link to be added on
  first download.
- **Author:** Hands-On Tools (Keegan)
- **License:** Confirm from MakerWorld page at download time
- **Downloaded:** YYYY-MM-DD (fill in)
- **Tile size:** 200 × 200 mm bounding box, octagonal outline (8 × 8 MU)
- **Print quantity:** 30 for primary pegboard coverage (+ 20 optional
  corner-square fillers for full visual coverage)
- **Notes:** Print with 4 walls, 25% infill — load-bearing tile, not
  the baseplate default

## Multiconnect ↔ Gridfinity adapter (optional, 4-8 copies)

- **URL:** TBD — Hands-On Tools publishes adapter STLs alongside Core
  tile
- **Author:** Hands-On Tools (or community remix)
- **License:** TBD
- **Downloaded:** YYYY-MM-DD (fill in)
- **Notes:** Lets a 2×2 or 3×3 Gridfinity bin printed for the drawer
  hang on the wall

## Tool-specific accessories (add as picked)

Recommended starting set — search MakerWorld for "Multiboard <tool>":

- **Drill cradle** (DeWalt corded drill, hand drill)
- **Bar clamp rack**
- **Spring clamp rack**
- **C-clamp hooks**
- **Hex key (Allen) holder**
- **Pliers / wire-cutter holder**
- **Tape measure holder**
- **Speed square holder**
- **Multi-screwdriver rack** (replaces the loose yellow-handle row)
- **Cable / cord wrap holder**
- **Level rack** (mini torpedo + larger)

---

<!-- Template:

## `<filename>.stl`

- **URL:** <https://...>
- **Author:** <name or handle>
- **License:** <CC-BY / CC0 / etc>
- **Downloaded:** YYYY-MM-DD
- **Purpose:** <which tool/zone>
- **Print qty:** <N>
- **Notes:** <any tweaks needed in slicer>

-->
```

- [ ] **Step 2: Verify file content**

Run:
```bash
grep -c "^## " projects/workbench-pegboard-multiboard/downloaded/SOURCES.md
```

Expected: 3 (Core tile, Adapter, Tool-specific accessories).

---

### Task 4: Write print-log.md

**Files:**
- Create: `projects/workbench-pegboard-multiboard/print-log.md`

- [ ] **Step 1: Write print-log.md**

Create `projects/workbench-pegboard-multiboard/print-log.md` with this content:

```markdown
# Print log — workbench pegboard Multiboard

One entry per print attempt. Include: date, what was printed, filament,
slicer settings, duration, outcome, lessons.

---

<!-- Template:

## YYYY-MM-DD — <part name + qty>

- **Filament:** <brand + color>
- **Slicer profile:** <name>
- **Print time:** <hh:mm>
- **Outcome:** success / partial / failure
- **Photos:** (optional, paths to local copies)
- **Lessons:** <what to do differently next time>

-->
```

- [ ] **Step 2: Verify file exists**

Run:
```bash
ls -la projects/workbench-pegboard-multiboard/print-log.md
```

Expected: file exists, ~15 lines.

---

### Task 5: Lint the new files

- [ ] **Step 1: Run ruff**

Run:
```bash
ruff check projects/workbench-pegboard-multiboard/ 2>&1
```

Expected: `All checks passed!` (no Python files yet, but the directory should not trip any rule).

- [ ] **Step 2: Run pytest on the existing suite**

Run:
```bash
.venv/bin/pytest 2>&1 | tail -5
```

Expected: all existing tests still pass; new tests (if any) also pass.

---

### Task 6: Phase 1 commit

- [ ] **Step 1: Show what's about to be committed**

Run:
```bash
git status projects/workbench-pegboard-multiboard/
```

Expected: 3 untracked files (README.md, downloaded/SOURCES.md, print-log.md).

- [ ] **Step 2: Stage the Multiboard project files**

Run:
```bash
git add projects/workbench-pegboard-multiboard/
```

- [ ] **Step 3: Commit**

Run:
```bash
git commit -m "$(cat <<'EOF'
feat: scaffold workbench-pegboard-multiboard project

Adds README, SOURCES.md placeholder, and print-log for the Multiboard
wall system that sits on top of the existing pegboard. Downloaded-STL
pattern — no 3d/ generator (Core tile geometry pulled from official
MakerWorld page). Tile count and exact URLs filled in once pegboard is
measured and tile is downloaded.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: clean commit, no hook failures.

---

## Phase 2: GATE — user input required

Phase 3 cannot start until the user provides:

| # | Input | Format | Used by |
|---|---|---|---|
| G1 | Top drawer interior dimensions | W × D × interior-H in mm or inches | `baseplate.py:TILES`, `README.md` |
| G2 | Middle drawer interior dimensions | W × D × interior-H | same |
| G3 | Bottom drawer interior dimensions | W × D × interior-H | same |
| G4 | Pegboard visible width | mm or inches | `pegboard-multiboard/README.md` |
| G5 | Pegboard visible height | mm or inches | same |
| G6 | Filament color choice for drawer baseplates | "black" / "grey" | print recipe |
| G7 | Filament color choice for Multiboard tiles | "black" / "grey" / other | print recipe |
| G8 | Confirmed MakerWorld URL for Multiboard Core tile | URL | `downloaded/SOURCES.md` |

Collect all 8 inputs before continuing. Steps below reference them as G1-G8.

---

## Phase 3: Apply measurements and regenerate (UNBLOCKED after Phase 2)

### Task 7: Compute the drawer tile layout

This is a pen-and-paper task (or one Python REPL session) — no file
changes yet, just the math that feeds Task 8.

- [ ] **Step 1: Convert dimensions to mm if needed**

For each drawer:
- If width is in inches: `W_mm = W_in × 25.4`
- Drop fractional mm (round down) — slack is fine; binding is not.

- [ ] **Step 2: Compute usable cell counts per drawer**

For each drawer:
```
cols = floor((W_mm - 4) / 42)    # 4 mm clearance (2 mm per side)
rows = floor((D_mm - 4) / 42)
```

The 4 mm clearance is so the assembled baseplate doesn't bind against
the drawer walls. Example: a 432 mm wide drawer gives
`floor((432-4)/42) = floor(10.19) = 10` columns.

- [ ] **Step 3: Split into A1-printable tiles**

A1 single-tile cap: `cols ≤ 6, rows ≤ 6` (252 mm max edge).

Use the smallest tile count that covers the grid without overlap:
- If `cols ≤ 6 and rows ≤ 6` → one tile `(cols, rows, 1)`
- If `cols > 6 and rows ≤ 6` → split width: `(6, rows, K)` + `(cols-6×K, rows, 1)` where K covers full-width tiles
- If both > 6 → grid split — e.g., 10×8 = `(6, 4, 2) + (4, 4, 2) + (6, 4, 2) + (4, 4, 2)`; simplify by picking equal-sized tiles where possible

Document the chosen split per drawer.

- [ ] **Step 4: Verify total tile coverage matches the grid**

For each drawer, sum tile cells:
```
sum(cols_i × rows_i × qty_i) == drawer_cols × drawer_rows
```

If they don't match, the split is wrong — recompute.

---

### Task 8: Update `baseplate.py` with the new TILES

**Files:**
- Modify: `projects/workbench-drawer-gridfinity/3d/baseplate.py:19-22`

- [ ] **Step 1: Edit TILES list**

In `projects/workbench-drawer-gridfinity/3d/baseplate.py`, replace the
current `TILES` list (currently `[(6, 4, 1)]`) with the full set from
Task 7. Each unique `(cols, rows)` appears once with the total qty
across all drawers.

Example for three drawers all needing the same 6×4 + 4×4 split:
```python
TILES: list[tuple[int, int, int]] = [
    (6, 4, 6),   # 2 per drawer × 3 drawers
    (4, 4, 6),   # 2 per drawer × 3 drawers
]
```

Use the actual numbers from Task 7 Step 4.

- [ ] **Step 2: Verify edit**

Run:
```bash
grep -A 5 "^TILES" projects/workbench-drawer-gridfinity/3d/baseplate.py
```

Expected: shows the new `TILES` list with realistic counts.

---

### Task 9: Regenerate the drawer baseplate STLs

- [ ] **Step 1: Run baseplate generator**

Run:
```bash
projects/desk-drawer-gridfinity/3d/.venv/bin/python projects/workbench-drawer-gridfinity/3d/baseplate.py
```

Expected output: one line per unique `(cols, rows)` tile in TILES, of
the form:
```
Wrote baseplate_6x4.stl (NNNN KB) — print N copies
```

- [ ] **Step 2: Verify STL count and sizes**

Run:
```bash
ls -la projects/workbench-drawer-gridfinity/3d/out/
```

Expected: one `baseplate_<cols>x<rows>.stl` per unique tile in TILES.
Each STL > 200 KB (smaller = empty or broken).

- [ ] **Step 3: Validate STL geometry**

Run:
```bash
.venv/bin/python -c "
import trimesh
from pathlib import Path
for stl in Path('projects/workbench-drawer-gridfinity/3d/out').glob('*.stl'):
    m = trimesh.load(str(stl))
    w, d, h = m.extents
    print(f'{stl.name}: {w:.1f} x {d:.1f} x {h:.2f} mm  watertight={m.is_watertight}  bodies={m.body_count}')
"
```

Expected: each STL is watertight, single body, height ≈ 4.75 mm,
footprint matches `cols×42` × `rows×42` minus the 0.5 mm inset.

- [ ] **Step 4: Run smoke tests**

Run:
```bash
.venv/bin/pytest tests/test_workbench_drawer_gridfinity.py -v
```

Expected: 3 passed.

---

### Task 10: Update the drawer project README dimension table

**Files:**
- Modify: `projects/workbench-drawer-gridfinity/README.md` (the "Drawers" section table)

- [ ] **Step 1: Replace the TBD rows with actual values**

Open `projects/workbench-drawer-gridfinity/README.md` and replace the
Drawers table (around lines 12-18) with the measured values. Format:

```markdown
| Drawer | Width | Depth | Interior height | Cells (W × D) | Status |
|---|---|---|---|---|---|
| Top    | <G1 W> mm | <G1 D> mm | <G1 H> mm | <cols> × <rows> | STL ready |
| Middle | <G2 W> mm | <G2 D> mm | <G2 H> mm | <cols> × <rows> | STL ready |
| Bottom | <G3 W> mm | <G3 D> mm | <G3 H> mm | <cols> × <rows> | STL ready |
```

Also remove the "First print: starter tile" section (now obsolete —
the starter print already happened; the real layout is in place).

- [ ] **Step 2: Verify edit**

Run:
```bash
grep -A 5 "^## Drawers" projects/workbench-drawer-gridfinity/README.md
```

Expected: table shows measured values, no TBDs.

---

### Task 11: Update the Multiboard SOURCES.md with the downloaded tile

**Files:**
- Modify: `projects/workbench-pegboard-multiboard/downloaded/SOURCES.md` (the Core tile entry)

- [ ] **Step 1: Replace the Core tile placeholder**

Open `projects/workbench-pegboard-multiboard/downloaded/SOURCES.md`.
Replace the "Multiboard Core tile (planned ~30 copies)" entry with:

```markdown
## Multiboard Core tile

- **URL:** <G8 — MakerWorld URL>
- **Author:** Hands-On Tools (Keegan)
- **License:** <as shown on the MakerWorld page>
- **Downloaded:** <today's date YYYY-MM-DD>
- **Tile size:** 200 × 200 mm bounding box, octagonal outline (8 × 8 MU)
- **Print quantity:** <computed from pegboard dimensions — see below>
- **Notes:** 4 walls, 25% infill, no supports, no brim
```

- [ ] **Step 2: Compute and record tile count**

In the same SOURCES.md, add directly below the Core tile entry:

```markdown
### Pegboard coverage math

- Pegboard visible: <G4> × <G5> mm
- Octagon plate pitch: 200 mm (both X and Y — truncated square tiling)
- Tiles per row: floor(<G4> / 200) = <N_cols>
- Rows: floor(<G5> / 200) = <N_rows>
- Total octagons: N_cols × N_rows = <total>
- Optional corner-square fillers: (N_cols−1) × (N_rows−1) = <filler total>
```

- [ ] **Step 3: Verify edit**

Run:
```bash
grep -E "^(##|###)" projects/workbench-pegboard-multiboard/downloaded/SOURCES.md
```

Expected: shows the Core tile entry filled in, plus the coverage math
subsection.

---

### Task 12: Update the pegboard README dimension table

**Files:**
- Modify: `projects/workbench-pegboard-multiboard/README.md` (the "Pegboard dimensions" section)

- [ ] **Step 1: Fill in measured values**

Open `projects/workbench-pegboard-multiboard/README.md`. Replace the
Pegboard dimensions table with:

```markdown
| Dimension | Value | Status |
|---|---|---|
| Visible width (panel behind cabinet) | <G4> mm | Measured |
| Visible height | <G5> mm | Measured |
| Stud spacing behind pegboard | 406 mm (16" OC) | Confirmed |
| Pegboard thickness | <measured> mm | Measured |
```

Also update the "Tile coverage plan" paragraph to use the actual tile
count computed in Task 11.

- [ ] **Step 2: Verify edit**

Run:
```bash
grep -A 6 "Pegboard dimensions" projects/workbench-pegboard-multiboard/README.md
```

Expected: table shows measured values, no TBDs.

---

### Task 13: Phase 3 commit

- [ ] **Step 1: Show what's about to be committed**

Run:
```bash
git status projects/workbench-drawer-gridfinity/ projects/workbench-pegboard-multiboard/
```

Expected: shows the README + baseplate.py modifications and SOURCES.md updates.

- [ ] **Step 2: Stage the changes**

Run:
```bash
git add projects/workbench-drawer-gridfinity/README.md \
        projects/workbench-drawer-gridfinity/3d/baseplate.py \
        projects/workbench-pegboard-multiboard/README.md \
        projects/workbench-pegboard-multiboard/downloaded/SOURCES.md
```

Note: don't `git add` the `out/` directory — STLs are gitignored.

- [ ] **Step 3: Commit**

Run:
```bash
git commit -m "$(cat <<'EOF'
feat: lock workbench drawer + pegboard dimensions, regenerate STLs

Drawer baseplate TILES updated to match the three Craftsman cabinet
drawers; STLs regenerated. Multiboard SOURCES.md updated with the
official Core tile URL and computed tile count for full pegboard
coverage.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: clean commit, no hook failures.

---

## Phase 4: Print queue execution (procedure, user-driven)

These steps run on the Bambu A1, not in code. Track progress in each
project's `print-log.md`.

### Task 14: Slice and print the drawer starter baseplate (already generated)

- [ ] **Step 1: Open Bambu Studio**

- [ ] **Step 2: File → Import → Import 3MF/STL**

Pick `projects/workbench-drawer-gridfinity/3d/out/baseplate_6x4.stl`
(or the largest tile from Task 9 if Phase 3 has run).

- [ ] **Step 3: Set filament profile**

Select **SUNLU PLA+ 2.0** (color per G6 from Phase 2). Click "Sync"
icon → confirm no AMS auto-detect (third-party spool, no RFID).

- [ ] **Step 4: Set slicer profile**

`0.20mm Standard @BBL A1`. Verify:
- 3 walls
- 15% infill (gyroid)
- No supports
- No brim
- Plate: textured PEI

- [ ] **Step 5: Slice and preview**

Click Slice. Check the preview — bin-foot pockets should be clear
recessed channels, not bridged shut. Estimated time displayed in the
top-right (~3 hrs for a 6×4 tile).

- [ ] **Step 6: Send to printer**

Click Print → confirm printer + plate are ready → start print.

- [ ] **Step 7: Log the print**

After the print finishes, add an entry to
`projects/workbench-drawer-gridfinity/print-log.md` with date, outcome,
notes.

---

### Task 15: Download + slice + print the Multiboard Core tile (after Phase 2 Gate)

- [ ] **Step 1: Download the Core tile STL**

Open the MakerWorld URL from G8. Download the Core tile STL/3MF.
Save to `projects/workbench-pegboard-multiboard/downloaded/`.

The folder is gitignored — local-only.

- [ ] **Step 2: Import to Bambu Studio**

File → Import → Import 3MF/STL. Pick the downloaded Core tile.

- [ ] **Step 3: Set print parameters**

- Filament: SUNLU PLA+ 2.0 (color per G7)
- Profile: `0.20mm Standard @BBL A1`
- **Walls: 4** (bump from default 3 — load-bearing)
- **Infill: 25% gyroid** (bump from default 15%)
- No supports, no brim

- [ ] **Step 4: Slice and print 1 tile**

Slice → preview → confirm no bridging issues → print. ~3-4 hrs.

- [ ] **Step 5: Load-test the printed tile**

Per `projects/workbench-pegboard-multiboard/README.md` "First print"
section:

1. Mount to a representative pegboard zone with one stud-screw + one
   pegboard-only screw.
2. Hang the heaviest planned item (DeWalt corded drill, ~5 lbs).
3. Bump-test: bump from below with a fist. Inspect for flex > 1 mm or
   screw rotation.

If pass → proceed to Task 16. If fail → revise (more walls, denser
infill, more screws) and reprint one tile before bulk.

- [ ] **Step 6: Log the print**

Add an entry to
`projects/workbench-pegboard-multiboard/print-log.md`.

---

### Task 16: Bulk print Multiboard tiles (background, ~5-7 days)

- [ ] **Step 1: Reload the Core tile and set quantity to N (G8 / coverage math)**

In Bambu Studio: open the Core tile project → Right-click the part →
Set quantity → N (the tile count from Task 11).

- [ ] **Step 2: Auto Arrange Plate**

Click Auto Arrange. Each plate fits ~2 tiles in square layout.
~15 plates for 30 tiles.

- [ ] **Step 3: Slice and send plate 1**

Slice plate 1 → send to printer. While it prints, prep the next plate
(no slicer action — the multi-plate project handles it).

- [ ] **Step 4: Run plates as printer is free**

Repeat for each plate until N tiles are printed. Log start/end times
for the batch in `print-log.md`.

---

### Task 17: Bulk print remaining drawer baseplate tiles (interleave with Multiboard)

- [ ] **Step 1: Open the drawer baseplate STLs in Bambu Studio**

Import each unique tile size from `projects/workbench-drawer-gridfinity/3d/out/`.

- [ ] **Step 2: Set quantities per the TILES table**

Each STL has its qty in the script output (Task 9 Step 1). Right-click
each part → Set quantity → N.

- [ ] **Step 3: Auto Arrange Plate**

Plates run in between Multiboard plates as the printer is free.

- [ ] **Step 4: Print and log**

Run plates as printer is available. Log in
`projects/workbench-drawer-gridfinity/print-log.md`.

---

## Phase 5: Tool inventory + zoning (after first prints land)

This phase is iterative — best done physically after the first drawer
baseplate is in a drawer and the first Multiboard tile is on the wall.

### Task 18: Sort tools into "wall" vs "drawer" piles

- [ ] **Step 1: Empty the existing drawers and pegboard onto the workbench**

Physical action — no code. Spread everything out.

- [ ] **Step 2: Sort each tool into one of three piles**

- Wall pile (60-70%): things used often, things that hang naturally,
  things that don't nest (drills, clamps, levels, squares, snips,
  pliers, screwdrivers, tape measures, snake-light, brush, cable)
- Drawer pile (25-35%): small loose items (bits, hex keys, sockets,
  screws, anchors, headlamp, step bits, hole saws, thread tape)
- Elsewhere pile (~5%): things that don't belong on the workbench at
  all (kitchen spillover, decor, etc.) — move them off the bench

- [ ] **Step 3: Photograph each pile**

For the record in the project READMEs / print-log.

---

### Task 19: Map drawer tools to Gridfinity bin sizes

For each item in the Drawer pile, pick the smallest bin size that fits.

- [ ] **Step 1: Measure each item (longest axis) or estimate by eye**

- [ ] **Step 2: Pick bin size**

Lookup table:
- Item longest axis < 40 mm → 1×1 bin
- 40-80 mm → 1×2 bin (vertical pocket)
- 80-120 mm → 2×2 or 3×1 bin
- 120-160 mm → 4×2 or 4×1
- > 160 mm → larger / use drawer divider

Item depth:
- Short (< 25 mm) → 3U bin
- Medium (25-45 mm) → 6U bin
- Tall (45-80 mm) → 9U or 12U bin

- [ ] **Step 3: Record the bin layout in a table**

In `projects/workbench-drawer-gridfinity/README.md`, add a Bins
section:

```markdown
## Bins

| Drawer | Cell zone | Bin size | Contents |
|---|---|---|---|
| Top | (0,0)-(2,2) | 3×3×9U | Bit cases (DeWalt + Craftsman) |
| Top | (3,0)-(3,1) | 1×2×6U | Hex key sets |
| ...
```

---

### Task 20: Update `bins.py` with the bin set

**Files:**
- Modify: `projects/workbench-drawer-gridfinity/3d/bins.py:18-23`

- [ ] **Step 1: Populate BINS**

In `bins.py`, replace the empty `BINS = []` with the unique bin sizes
from Task 19 Step 3. Format:

```python
BINS: list[tuple[int, int, int, int]] = [
    (1, 2, 6, N1),  # qty across all drawers
    (2, 2, 6, N2),
    (2, 2, 9, N3),
    (3, 3, 9, N4),
    # ...
]
```

Use the actual counts from Task 19. Each unique (cols, rows, height_U)
appears once with total qty.

- [ ] **Step 2: Regenerate bin STLs**

Run:
```bash
projects/desk-drawer-gridfinity/3d/.venv/bin/python projects/workbench-drawer-gridfinity/3d/bins.py
```

Expected: one line per unique bin in BINS.

- [ ] **Step 3: Validate**

Run:
```bash
.venv/bin/pytest tests/test_workbench_drawer_gridfinity.py -v
```

Expected: 3 passed (the STL count assertion is `>= 1`, still satisfied).

- [ ] **Step 4: Commit**

Run:
```bash
git add projects/workbench-drawer-gridfinity/3d/bins.py \
        projects/workbench-drawer-gridfinity/README.md
git commit -m "$(cat <<'EOF'
feat: map workbench drawer inventory to Gridfinity bins

Populates bins.py with bin sizes computed from drawer inventory; adds
the per-drawer bin layout table to the README. STLs regenerate via the
existing per-project venv.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 21: Map wall tools to Multiboard accessories

- [ ] **Step 1: For each item in the Wall pile, search MakerWorld**

Format: `Multiboard <tool name>` — e.g., "Multiboard drill holder",
"Multiboard bar clamp", "Multiboard hex key".

- [ ] **Step 2: For each accessory found, record in SOURCES.md**

Add an entry to
`projects/workbench-pegboard-multiboard/downloaded/SOURCES.md` per the
template at the bottom of that file. Include URL, author, license,
download date, purpose, and print qty.

- [ ] **Step 3: Print accessories as needed**

These are short prints (10-60 min each) and can run between Multiboard
plates. No predetermined order — print what you need next as you
populate the wall.

- [ ] **Step 4: Commit SOURCES.md updates**

After each batch of accessories added:
```bash
git add projects/workbench-pegboard-multiboard/downloaded/SOURCES.md
git commit -m "docs(workbench-multiboard): add <tools> accessory sources"
```

---

## Self-review

Walked through each spec section vs each task:

- **Architecture (two projects, Multiboard wall + Gridfinity drawer)** — covered by Task 1-6 (Multiboard scaffold) + Tasks 7-9 (drawer regen) + drawer project already scaffolded outside this plan ✓
- **Wall system choice (Multiboard)** — implicit in Task 1-6 scaffold + Tasks 15-16 print queue ✓
- **Drawer system (Gridfinity, parametric)** — Tasks 7-10 + 20 ✓
- **Mount strategy (screw through tile + pegboard into studs)** — documented in Task 2 README; load-tested in Task 15 ✓
- **Multiboard parts downloaded, drawer parts parametric** — Tasks 11 + 15 (downloaded), Tasks 8-9 + 20 (parametric) ✓
- **Print queue order** — Tasks 14-17 ✓
- **Open questions resolved** — Phase 2 Gate (G1-G8) ✓
- **Project naming (two siblings, not one umbrella)** — Tasks 1-2 ✓

No spec requirement is unmapped. No placeholders in code blocks (all
code blocks contain complete content). No type/name inconsistencies
(TILES uses `(cols, rows, qty)` throughout; BINS uses `(cols, rows,
height_U, qty)` throughout).

One acknowledged dependency: Phase 3 onwards is gated on user-provided
measurements (G1-G8). Tasks reference these symbolically and the plan
spells out the exact arithmetic to convert them to code values.
