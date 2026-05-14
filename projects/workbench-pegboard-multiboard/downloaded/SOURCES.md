# Downloaded STL sources

**STL/3MF files themselves are gitignored** — only this SOURCES.md gets
committed. Do not re-host third-party models.

Populate the entries below as you download tiles and accessories. The
template at the bottom matches the format used elsewhere in this repo.

---

## `8x8 MU - MultiBoard Octagon Plate.stl`

- **URL:** <https://multibuild.io/parts>
- **Author:** Hands-On Tools (Keegan)
- **License:** Confirm from the source page at download time
- **Downloaded:** 2026-05-11
- **Tile size:** 8 × 8 Multiboard Units = 200 × 200 mm bounding box,
  octagonal outline, 6.2 mm thick
- **Print quantity:** 30 (full pegboard coverage — see math below)
- **Notes:** 4 walls, 25% infill, no supports, no brim. ~35 g per tile
  at these settings. Note: official site has been renamed (originally
  Multiboard.io → now Multibuild.io); the system name "Multiboard"
  is retained in this doc for consistency with the rest of the project.

### Pegboard coverage math

Multiboard tiles are octagonal (not hex). Edge-to-edge they form a
truncated square tiling (4.8.8): octagons in a regular grid, with
small square gaps at the 4-corner intersections.

- Pegboard visible: 1300 × 1100 mm
- Octagon plate: 200 × 200 mm bounding box, 200 mm pitch
- Tiles per row: floor(1300 / 200) = 6
- Rows: floor(1100 / 200) = 5
- Total octagons: 6 × 5 = 30 (covers 1200 × 1000 mm with ~50-100 mm
  border slack on each axis)
- Corner-square fillers (optional, separate STL not yet downloaded):
  (6−1) × (5−1) = 20 small square tiles to fill the corner gaps if
  full visual coverage is desired. Without them, pegboard shows
  through the corner gaps — most common look.

## `MultiboardPeg-3` Pegboard-mount adapter set (4 STLs, 42 total prints)

- **URL:** <https://makerworld.com/en/models/519109-pegboard-mount-for-multiboard>
- **Author:** Remix of "Pegboard Click" (see MakerWorld page for original
  attribution + license terms)
- **License:** Confirm from MakerWorld page
- **Downloaded:** 2026-05-13
- **Purpose:** Mount Multiboard Core plates onto the existing pegboard
  via snap-in clips — no drilling required, fully reversible
- **Print qty for the 6 × 5 grid:** 42 total (see breakdown below)
- **Notes:** Print recipe is the standard A1 0.20 mm profile, 3 walls,
  25 % infill, no supports. ~30-70 min per part. Total filament
  ~267 g across all 42 adapters.

Adapter geometry (validated against the downloaded STLs):

| Part | Bbox (mm) | Filament @ 25 % | Where it installs | Qty |
|---|---|---|---|---|
| `obj_1_Single Peg.stl` | 25 × 37 × 31 | 2.7 g | 4 grid corners | 4 |
| `obj_2_Double Peg - Vertical` | 25 × 62 × 31 | 4.7 g | Left/right edges (joins 2 vertically-stacked tiles) | 8 |
| `obj_4_Double Peg - Horizontal` | 25 × 37 × 57 | 4.6 g | Top/bottom edges (joins 2 side-by-side tiles) | 10 |
| `obj_3_Quad Peg.stl` | 25 × 62 × 57 | 8.6 g | Interior 4-way intersections | 20 |

`obj_5`–`obj_8` are duplicate geometry from the model's "all-on-one-plate"
test layout — same files as `obj_1`–`obj_4`, just renamed for the test
bundle.

**Pegboard variance caveat:** the creator reports a ¼" drift at
column 16 of their pegboard caused a gap between tiles 2-3. Measure
hole-to-hole spacing in 2-3 places before locking the layout — over
1300 mm width, cumulative drift of ~1 mm/ft can stack into a visible
seam.

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
- **Purpose:** <which tool / zone>
- **Tile size or bin size:** <e.g., 8x8 MU octagon / 2x2x6U>
- **Print qty:** <N>
- **Notes:** <any tweaks needed in slicer>

-->
