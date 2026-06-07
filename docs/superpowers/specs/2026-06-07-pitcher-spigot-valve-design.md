# Pitcher spigot valve — design

A printable replacement for a broken push-button spigot on a glass beverage
pitcher. The original is a spring-loaded push-button tap; this replacement
trades the button for a **quarter-turn plug valve** (stay-put lever), which is
reliably printable in PLA where a spring-return mechanism is not.

## Problem

The green plastic spigot body on a glass pitcher has failed. The original
assembly is a through-wall tap: a threaded barrel passes through a hole in the
pitcher wall, a rubber gasket and a (clear) nut clamp it in place, and a
push-button mechanism dispenses liquid out a downward spout.

Only the green body needs replacing. The rubber gasket is intact and will be
reused. The original clear nut's thread cannot be reliably reverse-engineered,
so a matched printed nut is produced instead.

A commercial replacement (e.g. Igloo 24009 push-button cooler spigot, ~5/8"
thread) exists and would outperform a printed valve, but the goal here is an
in-house printed part.

## Constraints

- **Wall is glass.** The clamp cannot be torqued — glass cracks under point
  load. Sealing must come from gasket compression, not clamping force.
  Tightening is finger-tight only; the nut spreads load with a wide flat face.
- **Material is PLA+ only** (SUNLU PLA+ 2.0, per repo filament catalog).
  Intermittent cold-water contact only. FDM layer lines can weep under standing
  pressure, so every real seal sits on a discrete gasket/taper face, never on a
  printed wall holding water across a layer seam.
- **Fixed hole.** The glass hole is 15.8 mm and cannot be re-drilled; the barrel
  must pass through it with clearance.

## Mechanism

Quarter-turn plug valve ("petcock"):

- A slightly **tapered plug** drops vertically into a matching tapered seat in
  the valve chamber.
- The plug has a horizontal **cross-bore**; a flat **lever paddle** sits on top.
- Lever aligned with the spout = cross-bore open = flow. Lever rotated 90° =
  bore blocked = closed. The plug stays where it is set (no spring).
- A **retainer** (printed clip/collar) holds the plug down so water pressure
  cannot lift it out.
- A thin smear of food-safe silicone grease on the plug taper makes it
  leak-tight and smooth to turn.

## Flow path

Pitcher interior → through-wall barrel bore (10 mm) → valve chamber → plug
cross-bore (~10 mm) → downward spout → cup. Pitcher sits at the counter edge so
the downward spout clears.

## Sealing

Two independent seals, both on forgiving faces:

1. **Wall seal.** The reused rubber gasket (OD 34 / ID 19 / 3 mm) compresses
   between the body flange and the outer glass face. It seals the annular gap
   around the barrel and cushions the glass from the printed flange.
2. **Valve seal.** The tapered plug seated in the tapered chamber seat, snugged
   by the retainer, plus silicone grease.

The printed nut bears on the inner glass face. With only one rubber gasket on
hand, the nut sits on bare glass — mitigated by a wide flat bearing face and
finger-tight assembly. An optional second rubber washer on the inside face would
add margin but is not required.

## Parameters

All dimensions in mm. `*` marks values expected to need a tuning pass.

| Parameter | Value | Source / reason |
|---|---|---|
| Glass hole Ø | 15.8 | measured |
| Barrel OD (thread major) | 15.3 | passes the 15.8 hole with clearance |
| Barrel bore (flow) | 10.0 | matches old inner-barrel bore |
| Glass thickness | ~3.0 (uncertain) | barrel thread length made generous (~16) so fit is not sensitive to this |
| Barrel thread length | ~16 | gasket (3) + glass (3) + nut engagement, with margin |
| Flange OD | 33 | ≤ gasket OD 34; inside the 20 mm flat radius around the hole |
| Gasket (reused) | OD 34 / ID 19 / 3 thick | sits under flange against glass |
| Chamber / outlet bore | ~14 | matches old stem outlet bore |
| Plug cross-bore | ~10 | flow ≈ barrel bore |
| Plug-to-seat clearance | TBD* | top-level parameter; dialed in on the fit prototype |
| Spout drop below hole | ≤ ~20 | within the 30 mm to base |
| Lever | ~30 long, flat paddle | quarter-turn, stay-put |
| Thread form | coarse printable (matched pair) | nut and barrel printed together so threads fit each other |

## Components and files

New project `projects/pitcher-spigot-valve/`, following repo conventions
(one part per `snake_case.py` script, three-section convention, `out/` output).

- `3d/body.py` — barrel + flange + valve chamber (tapered seat) + downward spout
- `3d/plug.py` — tapered plug + cross-bore + lever paddle
- `3d/nut.py` — clamp nut, matched thread, wide flat bearing face
- `3d/retainer.py` — clip/collar retaining the plug
- `3d/build_all.py` — regenerates every sibling script
- `tests/test_pitcher_spigot_valve.py` — smoke tests asserting each generator
  emits a non-trivial STL
- `README.md`, `print-log.md` per convention

Assembly clearances (plug-in-seat, barrel-clears-hole) are verified during the
build with the **cad-khana** wrapper, since a mating multi-part valve is where
interference bugs hide.

## Testing and validation

- **Smoke tests** (CI): each generator runs and produces a valid, non-trivial
  STL — catches build123d API drift and empty boolean results.
- **Assembly diagnostics** (cad-khana): plug seats in the chamber with the
  intended clearance; barrel OD clears the 15.8 hole; no part interferes.
- **Physical fit prototype:** print body + plug + nut, verify the plug turns and
  seats and the barrel passes the glass hole. Tune `plug-to-seat clearance`.
- **Leak test:** assemble with water and confirm no weeping at the wall seal or
  the valve in both open and closed positions before trusting it on the pitcher.

## Out of scope

- Replicating the original spring-loaded push-button action.
- Matching the original color or the original nut's thread.
- Reusing the original clear nut (a matched printed nut replaces it).
