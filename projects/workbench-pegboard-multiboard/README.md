# Workbench pegboard Multiboard wall

Tiled Multiboard wall mounted on top of the existing 1/4" pegboard
behind the garage workbench rolling cabinet. Multiboard is Hands-On
Tools' octagon-tiled wall storage system — each 200 × 200 mm Core
plate (octagonal outline inside a 200 mm square bounding box) mounts
via screws, accepts Multiconnect-standard accessories (hooks, shelves,
holders), and bridges to Gridfinity bins via official adapters. Tiles
combine in a truncated square tiling (4.8.8) — octagons edge-to-edge
with small square gaps at the 4-corner intersections (those gaps can
optionally be filled with separate square-filler tiles).

## Pegboard dimensions

| Dimension | Value | Status |
|---|---|---|
| Visible width (panel behind cabinet) | 1300 mm (~51") | Measured |
| Visible height | 1100 mm (~43") | Measured |
| Stud spacing behind pegboard | 406 mm (16" OC) | Standard US framing |
| Pegboard thickness | ~6 mm (1/4") | Standard hardboard |

## Tile coverage plan

Core plate footprint: 200 × 200 mm bounding box (octagonal outline),
200 mm pitch in both X and Y. Pegboard area is 1300 × 1100 mm. Tile fit:
6 tiles wide × 5 rows tall = **30 octagon plates** for primary coverage
(spans 1200 × 1000 mm with ~50–100 mm border slack). 20 optional
square-filler tiles can plug the 4-corner gaps if you want a fully
solid surface. See `downloaded/SOURCES.md` for the coverage math.

## Mount strategy

3D-printed pegboard adapters (no drilling). The
[Pegboard Mount for Multiboard](https://makerworld.com/en/models/519109-pegboard-mount-for-multiboard)
remix publishes 4 adapter types that snap into standard 1/4" pegboard
holes and provide MultiPoint nodes for Multiboard tiles to snap onto.
Load passes from accessory → tile → adapter → pegboard hole →
pegboard's existing stud-screws → wall.

The 4 adapter types and where each goes on a tile grid:

| Adapter | Where it installs | Count for 6 × 5 grid |
|---|---|---|
| **Single Peg** | Each of the 4 outer corners of the entire grid | 4 |
| **Double Vertical** | Left and right edges — joins 2 vertically-stacked tiles | 8 (4 per side) |
| **Double Horizontal** | Top and bottom edges — joins 2 side-by-side tiles | 10 (5 per edge) |
| **Quad Peg** | Interior 4-way intersections where 4 tiles meet | 20 (5 × 4) |
| **Total** | | **42 adapters** |

Total adapter filament: ~267 g (¼ of a spool). Print recipe: standard
0.20 mm A1 profile, 3 walls, 25 % infill, no supports. Each adapter
prints in 30-70 min; small enough to pack 6-10 per plate.

**Pegboard manufacturing variance:** the creator notes their pegboard
had a ¼" drift at column 16 that opened a small gap between tiles 2
and 3. For a 1300 mm wide installation (~51"), measure hole-to-hole
spacing in three places before locking the layout — cumulative drift
of 1 mm/foot can compound across 6 tiles. If drift is found, plan tile
placement so the gap falls between tiles you don't care about, or
shift adapter pegs to engage cleaner holes.

**Fallback for unexpectedly heavy zones:** if a single tile ends up
overloaded (>20 lbs of tools on one tile), you can drill a
supplemental #8 × 2" wood screw through tile + adapter + pegboard into
a stud at that location. Unlikely to be needed given typical
workbench loads (DeWalt corded drill ~5 lbs, bar clamps 1-2 lbs each).

## Files

- `downloaded/SOURCES.md` — Multiboard Core tile + accessory STL provenance
- `print-log.md` — per-print diary

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

Per-tile estimate: ~35 g filament, ~3 hrs print time (verified against
the actual `8x8 MU - MultiBoard Octagon Plate.stl` at 25% infill /
4 walls — STL is 71 cm³ raw volume).

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
