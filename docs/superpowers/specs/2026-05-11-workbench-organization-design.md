# Workbench organization — design

**Date:** 2026-05-11
**Status:** approved (brainstormed), pending implementation
**Project locations:** `projects/workbench-drawer-gridfinity/` (scaffolded), `projects/workbench-pegboard-multiboard/` (to scaffold)
**Trigger:** garage workbench is unusable in current state. Pegboard behind the rolling cabinet is half-utilized with bent-wire pegs that wobble; tools fall off when a clamp gets bumped. Drawers below are a layered pile of bit cases, hex keys, levels, and screw boxes with no fixed homes — every search means lifting three things off the top. Wants 60-70% of tools on the wall and the rest organized in fixed-location drawer bins, all built around popular 3D-printable systems so accessories are downloadable rather than hand-rolled.

## What it is

Two parallel projects that share a print queue:

- **Wall:** Multiboard (Hands-On Tools' octagon-tiled wall system, truncated square tiling pattern 4.8.8) mounted on top of the existing pegboard. 30 200×200 mm Core plates (octagonal outline in a 200 mm bounding box, 8 MU square units per plate) cover the visible pegboard area. Tool-specific accessories (drill cradle, clamp rack, hex-key holder, etc.) snap to the tiles via the Multiconnect standard, and Gridfinity-bin adapters bridge wall ↔ drawer storage for small parts.
- **Drawer:** Gridfinity baseplates + bins for the Craftsman rolling cabinet drawers. Mirrors the `desk-drawer-gridfinity` pattern (parametric build123d, `gridfinity-build123d` library) — one STL per unique tile size, one STL per unique bin, fits the Bambu A1's 256 mm bed.

The two systems share a base unit: a 1×1 Gridfinity bin printed today can sit in a drawer or, via a Multiboard-Gridfinity adapter, hang on the wall. That dimensional compatibility is the design's load-bearing decision.

## Scope: what's in vs out

In:
- The Craftsman 3-drawer rolling cabinet (top, middle, bottom drawers)
- The pegboard panel directly behind the cabinet (~3' × 4' visible area)
- The tools currently hanging on the pegboard (DeWalt corded drill, hand drill, bar/spring/C clamps, levels, squares, snips, pliers, screwdrivers loose on a rack, cable, brush, etc.)
- The tools currently in the drawers (bit cases, hex keys, tape measures, sockets, hole saws, screws, headlamp, etc.)

Out (lives elsewhere):
- The Bambu A1 + filament + 3D-print workstation (separate space, separate problem)
- The temp electronics workstation (image 2) — that's the active workspace, not the storage system
- The wall area above the pegboard / under the cabinets — pegboard expansion is a possible v2 but out of scope here
- Bench-top surface organization (peg-up only)

## Design decisions and the reasoning

### Wall system — Multiboard (chosen over HSW, Gridfinity-Wall, and pegboard-only)

Considered: keep the pegboard and just print 3D-pegboard hooks; cover the pegboard with a tiled system (Multiboard or HSW); a hybrid where Underware tiles clip into pegboard holes in specific zones; replace the pegboard entirely. User chose tiled system on top of pegboard.

Within tiled systems, Multiboard wins on three factors:

1. **Load capacity** — single tile rated 50+ lbs properly screwed into a stud. Easily handles the DeWalt corded drill (~5 lbs), bar clamps (1-2 lbs each), and dense small-tool zones.
2. **Accessory ecosystem** — by a wide margin the largest community library on MakerWorld/Printables. For most of the user's tools (drills, clamps, levels, screwdriver sets, tape measures), a tool-specific Multiboard holder already exists and is free to download.
3. **Gridfinity bridge** — Multiboard officially publishes Gridfinity-bin adapters, so a 2×2 bin printed for the drawer can mount on the wall without a second design. This is what makes "one bin design serves both places" real.

HSW was rejected for thinner ecosystem despite similar mechanical capability. Gridfinity-Wall (square tiles, just baseplates on the wall) was rejected because the 90°-only grid makes diverse-shape hooks (clamps, drills, levels) awkward — Multiboard's octagonal connection points let accessories mount in 45° increments around each Multipoint, which matters for ergonomic tool placement.

### Drawer system — Gridfinity, parametric, mirrors `desk-drawer-gridfinity`

This is a non-decision: Gridfinity is the de-facto standard for drawer organization in the 3D-print community, the user already has a working parametric build123d generator + tested print recipe in the sibling `desk-drawer-gridfinity` project, and Multiboard-Gridfinity adapters are what bridge to the wall. Any other choice would be deliberate self-sabotage. The workbench drawer project is a clean fork of the desk-drawer project with retuned `TILES` and `BINS` parameters once measurements are in hand.

### Mounting strategy — 3D-printed pegboard adapters (revised 2026-05-13)

Original spec called for screwing each tile through the pegboard, with a stud-mount primary load path. **Revised to use a 3D-printed adapter system** ([MakerWorld: Pegboard Mount for Multiboard](https://makerworld.com/en/models/519109-pegboard-mount-for-multiboard)) after discovering it covers the load case without drilling.

Mechanism: the adapter STLs snap into standard 1/4" pegboard holes and expose Multiboard MultiPoint nodes on their faces. Tiles snap onto the adapters; accessories snap onto the tiles. Load passes from accessory → tile → adapter → pegboard hole → pegboard's existing stud-screws → wall stud.

Adapter types and count for the 6 × 5 tile grid: 4 Single Peg (grid corners) + 8 Double Vertical (left/right edges) + 10 Double Horizontal (top/bottom edges) + 20 Quad Peg (interior 4-way intersections) = **42 adapters total**, ~267 g of filament, ~6-10 plates of small prints.

Why this beats the original screw plan:

1. **Reversible** — no drill holes in the pegboard, tile layout can be moved around as tool placement evolves
2. **Faster install** — snap-in clips replace ~120 individual screw drives
3. **Same load capacity for the actual workload** — heaviest item is the DeWalt corded drill (~5 lbs); 4 clips per tile at ~5 lbs each is ~20 lbs/tile, well above what any single tile carries
4. **Pegboard stays intact** — survives system changes (Multiboard has already been renamed once during this project; future-proofs against another)

Fallback retained: if a specific tile ends up overloaded (>20 lbs on a single tile, unlikely), drill a supplemental #8 × 2" wood screw through tile + adapter + pegboard into a stud at that location. Hybrid is fine.

Original rejection of "pegboard-clip mounts" was based on simple hooks rated ~5 lbs each — this adapter set uses 2-4 clips per adapter and aggregates across a tile, which is a different load profile than I'd evaluated.

### Multiboard parts — downloaded, not parametric (drawer parts stay parametric)

Multiboard's Core tile geometry is finicky (octagonal perimeter with 8 Multipoint mounting nodes, specific tolerances, the rear screw bosses). Hand-rolling a "Multiboard-compatible" tile in build123d risks tolerance drift that would silently break accessory compatibility — and the official Hands-On Tools tile is freely downloadable from multibuild.io and battle-tested by thousands of builds. The downside (downloaded STLs don't get committed per repo policy) is irrelevant because we don't need a parametric Multiboard generator — we need 30 identical official tiles.

`workbench-pegboard-multiboard/downloaded/SOURCES.md` records the MakerWorld URL, author, license, and download date per the repo's `downloaded/` convention. A `3d/` directory is reserved for *custom* future accessories that don't exist on MakerWorld (e.g., a 4Runner-rear-seat-button-style accessory specific to one of Sam's tools).

Drawer parts remain parametric because (a) the dimensions are drawer-specific and need re-tuning per project, and (b) the existing `gridfinity-build123d` library provides validated `Bin` and `Base` geometry that's known-compatible with the standard.

### Print queue — drawer baseplate first, then Multiboard test tile, then bulk

Sequencing is constrained by the single Bambu A1 (one print at a time) and the need to validate each component before committing to the bulk print. The order:

1. **Drawer baseplate 6×4** (already generated, ~3 hrs) — kicks off tonight. Confirms the Gridfinity bin-foot profile mates with a downloaded bin (any standard 1×1 or 2×2 bin from MakerWorld).
2. **Multiboard Core tile ×1** (download tonight, print after #1, ~3-4 hrs) — confirms the tile mounts cleanly to the pegboard, accepts a Multiconnect hook, and bears weight. **Gate:** load test before committing to 30 tiles.
3. **Full drawer baseplate set** (regenerate after measurements, ~12-20 hrs total over 2-3 prints) — fills each drawer.
4. **Full Multiboard wall** (~30 tiles, ~90 hrs total over ~5-7 days) — background printer, runs while user works on other things.
5. **Tool-specific accessories** (download per-tool from MakerWorld) — drill cradles, clamp racks, hex-key holders, etc. Print as accessory designs are picked.

Total estimated print time over the first week: ~110-120 hours (well within the user's "whole week to print" budget). Total filament: ~1.5-2 kg PLA+ — within the SUNLU PLA+ catalog already on hand.

### Project naming — split into two projects, not one umbrella

Considered a single `projects/workbench-organization/` umbrella project. Rejected because the existing repo pattern is one folder per coherent printable thing (`desk-drawer-gridfinity`, `electronics-organizer`), and the drawer + wall projects have genuinely different dependencies (parametric vs downloaded), different print recipes, and different update cadences. Two siblings (`workbench-drawer-gridfinity`, `workbench-pegboard-multiboard`) is the local idiom.

## Open questions to resolve before locking the full implementation

These don't block the first two prints but block bulk tile/baseplate generation:

1. **Drawer dimensions** — interior W × D × interior H for each of the three Craftsman drawers. User has measurements already; we'll walk through them after the first print kicks off.
2. **Pegboard dimensions** — full visible W × H of the pegboard panel behind the rolling cabinet, plus how the area above the cabinet relates (one continuous panel or a separate piece). Drives the tile count.
3. **Filament color** — drawer baseplates default to grey or black for visual cohesion with the drawer interior. Multiboard tiles probably black to match. User to confirm.
4. **Tool inventory + zoning** — easier as a 5-minute walkthrough after the first Multiboard tile is on the wall and the first baseplate is in a drawer. Don't try to pre-plan zoning in the abstract; let the physical first prints inform it.

## References

Wall system:
- [Multiboard official site](https://multiboard.io/) — Hands-On Tools' system docs
- Multiboard Core tile + Gridfinity adapter: download links in `projects/workbench-pegboard-multiboard/downloaded/SOURCES.md` once user fetches them

Drawer system:
- Existing `projects/desk-drawer-gridfinity/` — same library, same conventions, working reference
- [moritzmhmk/gridfinity-build123d](https://github.com/moritzmhmk/gridfinity-build123d) — parametric bin + base generator (already a project dependency)
- Repo conventions for parametric scripts: `conventions.md`, 3-section build123d template (Parameters / Geometry / Export)

Pegboard mounting reference:
- Existing pegboard already screwed into studs at ~16" OC — see image 1 of the original brainstorm conversation for the visible board.
