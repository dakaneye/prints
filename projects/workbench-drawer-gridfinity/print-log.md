# Print log — workbench drawer Gridfinity

One entry per print attempt. Include: date, what was printed, filament,
slicer settings, duration, outcome, lessons.

---

## Inventory (current — as of 2026-05-25)

Standard recipe across all prints: SUNLU PLA+ 2.0 white, profile
`0.20mm Standard @BBL A1`, 3 walls / 15% gyroid / no supports / no
brim.

### Printed

| Part | Have | Needed | Notes |
|---|---|---|---|
| `baseplate_3x5.stl` | 2 | 4 | top drawer back band (2 per compartment × 2 compartments) |
| `baseplate_6x4.stl` | 2 | 2 | top drawer front band ✓ complete |
| `baseplate_5x5.stl` | 3 | 2 | middle + bottom back-left corner; +1 spare |
| `baseplate_5x4.stl` | 9 | 6 | middle + bottom front-left + 4×5 rotated; +3 spare |
| `baseplate_4x4.stl` | 6 | 4 | middle + bottom 4×4 positions; +2 spare |

### Still to print

| Part | Qty | Purpose |
|---|---|---|
| `baseplate_3x5.stl` | **2** | finish top drawer back band (have 2/4) |
| `spacer_left_25x205.stl` | **2** | top drawer LEFT compartment side slack (~25 mm) |
| `spacer_right_45x205.stl` | **2** | top drawer RIGHT compartment side slack (~45 mm) |
| middle/bottom spacers | TBD | pending caliper measurement of front + right slack |

**Total still to print: 6 known + middle/bottom spacers TBD.**

---

## History

### 2026-05-25 — top drawer 3×5 (partial)

- **What:** `baseplate_3x5.stl` × 2 (of 4 needed)
- **Filament:** SUNLU PLA+ 2.0 white
- **Slicer:** `0.20mm Standard @BBL A1`, standard recipe
- **Outcome:** success — replacement for the failed 6×5 design
- **Lessons:** `3x5` (126 × 210 mm) prints reliably; well clear of A1's
  edge exclusion zone. 2 more to go for the full set.

### 2026-05 — 6×5 attempt: spaghetti failure

- **What:** `baseplate_6x5.stl` (251.5 × 209.5 mm), overnight print
- **Outcome:** failure. Mid-print corner lift → adhesion lost → spaghetti.
- **Diagnosis:** A1's nominal 256 × 256 bed has edge exclusion zones
  for the probe and carriage. 251.5 mm in the long axis sits right at
  the bed-flatness boundary; the corner detached from the build plate
  partway through.
- **Decision:** abandon 6×5 on A1. Split the top-drawer back band
  width-wise into two 3×5 tiles. `baseplate.py` TILES updated and
  README per-drawer placement map updated accordingly.

### ~2026-05 — backlog (logged retroactively, dates approximate)

Counts taken from physical inventory on 2026-05-25; per-print dates
not preserved.

- **3× `baseplate_5x5.stl`** — middle/bottom drawer back-left tiles
  (design needs 2; 1 spare)
- **9× `baseplate_5x4.stl`** — middle/bottom drawer left-front + rotated
  4×5 positions (design needs 6; 3 spare)
- **2× `baseplate_6x4.stl`** — top drawer fronts, both compartments
  (design needs 2; complete)
- **6× `baseplate_4x4.stl`** — middle/bottom drawer 4×4 positions
  (design needs 4; 2 spare)

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
