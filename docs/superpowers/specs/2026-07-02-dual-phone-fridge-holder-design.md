# Dual phone fridge holder — design

Date: 2026-07-02
Status: approved (verbal, in-session)

## What

A single-piece wall-pocket holder for two iPhone 16 Pros (with cases) that
mounts to the side of the refrigerator via press-fit neodymium magnets.
Concept inspired by MakerWorld model 1880128 ("Phone wall mount charging
holder") — that model is licensed no-derivatives, so this is an independent
parametric design in build123d, not a remix. No STL from the source model is
used or modified.

## Requirements

- Holds two cased iPhone 16 Pros side by side, portrait, screens out
- Magnet-mounts to a painted-steel fridge side; no adhesive, no screws
- Parking only — no charging-cable pass-through (solid pocket floors)
- Uses magnets on hand: 6 mm ⌀ × 2 mm neodymium discs (assorted-set grade,
  assume N35)
- Prints on the Bambu A1 in SUNLU PLA+ 2.0 grey, no supports

## Dimensions

Phone basis: iPhone 16 Pro nominal 149.6 × 71.5 × 8.25 mm; case estimated
(user opted out of caliper measurement) at ~75 × 11 mm.

| Feature | Value |
|---|---|
| Backplate | 189.6 × 107.4 × 3 mm, rounded corners r8 (width driven by two 82.8 mm pocket shells + 8 gap + 8 margins) |
| Pocket interior | 78 W × 13 D per phone (~3 / ~2 mm case clearance) |
| Pocket front-wall interior height | 65 mm above the floor's front lip |
| Pocket walls (front + sides) | 2.4 mm |
| Gap between pockets | 8 mm |
| Pocket floor | 45° wedge, ~3 mm thick, sloping down toward the backplate |
| Finger scoop | 30 mm wide notch in each front wall, rounded bottom |
| Magnet recesses | 20× (5 cols × 4 rows) on the back face, ⌀6.3 × 1.8 mm deep |

The 45° floor serves two purposes: it prints support-free in the standing
orientation, and it tips the phone bottom toward the backplate so the phone
leans into the fridge rather than out of the pocket.

Magnets sit ~0.2 mm proud of the back face (2 mm magnet in a 1.8 mm recess)
so the steel contact is magnet-on-fridge, not plastic-on-fridge. Press fit
plus a dab of CA glue per magnet.

## Holding-force budget [MED]

Load: 2× cased phone (~230 g each) + holder (~100 g) ≈ 560 g, in shear.
A 6×2 N35 disc pulls ~0.5–0.7 kg on bare steel; shear resistance ≈ 0.25 ×
pull ≈ 125–175 g per magnet, degraded some by fridge paint. 20 magnets ≈
2.5–3.5 kg shear capacity → ~5× margin. The grid spreads to the plate edges
so the torque from phones leaning in the pockets is resisted at the top row.
Verify empirically before trusting: mount empty → one phone → two phones.

## Print

- Standing, in-use orientation (as exported). No supports; no bridges; all
  overhangs ≤ 45° by construction.
- 5 mm brim — a 3 mm plate standing on edge is tip-prone.
- SUNLU PLA+ 2.0 grey (manual profile select), 0.20 mm layer, 4 walls
  (pocket lips take pry loads), 15% infill. ~100 g, ~3 h.

## Repo shape

- `projects/dual-phone-fridge-holder/3d/holder.py` — one part, three-section
  convention, exports `out/holder.stl` in print pose
- `build_all.py`, `requirements.txt` per convention
- `tests/test_dual_phone_fridge_holder.py` — smoke + invariants (watertight,
  extents, volume plausibility, magnet-recess volume removed)
- README with print recipe + orientation decision; print-log started

## Out of scope

- Charging cable slots (explicitly declined)
- Personalization / labels
- MagSafe alignment — the magnets face the fridge, not the phones
