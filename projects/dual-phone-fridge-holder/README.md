# Dual phone fridge holder

One-piece wall pocket for two large phones (sized for cased iPhone 16 Pros)
that mounts to the side of the refrigerator with press-fit neodymium magnets.
Concept borrowed from the classic open-front wall-pocket phone holder;
independent parametric design in build123d.

- Backplate 189.6 × 97.4 × 3 mm, two pockets 78 × 13 mm interior, 45°
  wedge floors that tip the phones toward the fridge
- Back face: 5×4 grid of ⌀6.3 × 1.8 mm recesses for 6×2 mm neodymium discs
  — press fit + a dab of CA glue each; magnets sit ~0.2 mm proud so they
  contact the steel directly
- Parking only — no charging-cable slots

All dimensions are parameters in `3d/holder.py`. If a case doesn't fit,
bump `POCKET_W`/`POCKET_D`; if magnets fit loose/tight, adjust `MAGNET_FIT`
and regenerate.

## Assembly

Press a magnet into each of the 20 recesses with a drop of CA. Keep
polarity consistent (all same face out) so stacking order off the magnet
stack stays foolproof. Load-test on the fridge before trusting it:
empty → one phone → two phones.

## Print recipe

| Filament | Print time | Notes |
|---|---|---|
| SUNLU PLA+ 2.0 Grey (manual profile select) | ~3 h | 0.20 mm layer, 4 walls, 15% infill |

Orientation notes:

- STL exports in print pose: standing upright on the backplate's bottom
  edge, in-use orientation
- **Rotate 90° in the slicer so the 190 mm axis runs front-to-back (Y)**
  — the A1 bed only accelerates in Y, and that puts the shaking along the
  plate's stiff direction instead of its 3 mm-thin one
- **Use a 5 mm brim** — a 3 mm plate standing on edge is tip-prone
- No supports, no bridges — pocket floors are 45° wedges starting 2 mm
  above the bed (cross-section deepens to an L almost immediately), the
  finger-scoop notches open upward, magnet recesses are 6 mm side-wall
  holes
