# Downloaded STL sources

**STL/3MF files themselves are gitignored** — only this SOURCES.md gets
committed. Do not re-host third-party models.

Populate the entries below as you download tiles and accessories. The
template at the bottom matches the format used elsewhere in this repo.

---

## Multiboard Core tile

- **URL:** <https://multibuild.io/parts>
- **Author:** Hands-On Tools (Keegan)
- **License:** Confirm from the source page at download time
- **Downloaded:** 2026-05-11
- **Tile size:** 200 mm flat-to-flat hex
- **Print quantity:** 36 (full pegboard coverage — see math below)
- **Notes:** 4 walls, 25% infill, no supports, no brim. Note: official
  site has been renamed (originally Multiboard.io → now Multibuild.io);
  the system name "Multiboard" is retained in this doc for consistency
  with the rest of the project.

### Pegboard coverage math

- Pegboard visible: 1300 × 1100 mm
- Tile flat-to-flat: 200 mm
- Honeycomb stagger row pitch: ~173 mm (200 × √3/2)
- Tiles per row: floor(1300 / 200) = 6
- Rows: floor(1100 / 173) = 6
- Total tiles: 6 × 6 = 36

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
- **Tile size or bin size:** <e.g., 200 mm hex / 2x2x6U>
- **Print qty:** <N>
- **Notes:** <any tweaks needed in slicer>

-->
