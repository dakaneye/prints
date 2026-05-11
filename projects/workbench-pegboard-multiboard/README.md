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
