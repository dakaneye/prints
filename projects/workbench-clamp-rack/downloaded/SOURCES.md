# Downloaded sources

**Cloned repos and generated STLs are gitignored** — only this
SOURCES.md is committed. Do not re-host third-party code or models.

The clamp cradle is generated locally from the QuackWorks Vertical
Item Holder generator; the STL is never committed. See the project
README for the exact regenerate command and parameters.

---

## QuackWorks (Vertical Item Holder generator)

- **URL:** <https://github.com/AndyLevesque/QuackWorks>
- **Author:** Andy Levesque (with Multiboard/Multipoint by Jonathan
  at Keep Making; Multiconnect by @David D; Multiconnect v2 by
  @Dontic; Multipoint mount by @SnazzyGreenWarrior)
- **License:** Creative Commons Attribution-NonCommercial-ShareAlike
  4.0 (CC-BY-NC-SA 4.0). Multipoint mount portions per
  <https://www.multiboard.io/license>. Personal, non-commercial use
  only — consistent with this repo's posture.
- **Cloned:** 2026-05-17
- **Commit:** `61231295ea08c302eff32051769113c48cbda255`
  (2026-02-03)
- **File used:** `VerticalMountingSeries/VerticalItemHolder.scad`
- **Notes:** Generates a forward-facing item cradle with a
  configurable wall connector. Built with `Connection_Type="Multipoint"`
  (Multiboard's native protruding snap — mates a bare tile), not
  Multiconnect (which is a recessed slot needing a male rail).
  Parameters and the one-line regenerate command live in the project
  README. Output: `clamp_head_cradle_multipoint.stl`, printed twice
  (one cradle per clamp).

## BOSL2 (OpenSCAD library dependency)

- **URL:** <https://github.com/BelfrySCAD/BOSL2>
- **Author:** Belfry OpenSCAD (Revar Desmera et al.)
- **License:** BSD-2-Clause
- **Cloned:** 2026-05-17
- **Commit:** `881947c32a28fa68049b518dcc1e73202bfc2c7c`
  (2026-05-13, v2.0.741)
- **Notes:** Required by QuackWorks. Resolved via
  `OPENSCADPATH=projects/workbench-clamp-rack/downloaded` so
  `include <BOSL2/std.scad>` finds the cloned copy.

## Mounting hardware — obtain, do not commit

Official Multiboard parts. Download from the source, print locally;
bytes stay local (gitignored), like every other downloaded model
here. Mounts the cradle's Multipoint negative rail to the
`workbench-pegboard-multiboard` tiles. Qty: one of each per cradle →
**2 of each**.

### Heavy Weight-Bearing Hook Snap

- **URL:** <https://thangs.com/designer/MultiBuild/3d-model/Heavy%20Weight-Bearing%20Hook%20Snap-1311032>
  (also on the multibuild.io parts library)
- **Author:** MultiBuild / Multiboard (Keep Making)
- **License:** Multiboard Licence — confirm terms at the source
- **Notes:** Heavy-duty directional hook. One-direction load,
  inserted at an angle, arrow up. Only works with tiles offset from
  the wall. Pushes onto the cradle's Multipoint rail; secured by the
  Small Thread Multipoint below.

### Small Thread Multipoint

- **URL:** multibuild.io parts library — "Small Thread Multipoint"
  (companion screw piece for the Hook Snap)
- **Author:** MultiBuild / Multiboard (Keep Making)
- **License:** Multiboard Licence — confirm terms at the source
- **Notes:** The screw that secures the Hook Snap and threads into
  the tile point. Required companion to the Hook Snap. Do not
  substitute a generic T-bolt (reported to bend apart under load).
