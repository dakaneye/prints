# Bathroom toothbrush organizer

A scalloped-wall family bathroom organizer. Holds 3 manual toothbrushes
(1 adult + 2 kids) and a toothpaste tube in an open, draining wet zone, with
a walled-off, covered q-tip cubby that stays dry. Pure parametric (build123d),
with a concave vertically-scalloped outer wall. Design history:
`docs/superpowers/specs/2026-06-07-bathroom-toothbrush-organizer-design.md`.

## Parts

| Part | Script | Output |
|---|---|---|
| Body | `3d/organizer.py` | `out/organizer.stl` |
| Q-tip lid | `3d/qtip_lid.py` | `out/qtip_lid.stl` |

## Dimensions

- Body: 165 W × 70 D × 80 H mm, 18 mm corner radius
- Brush bores: 3 × Ø16 mm, back row, Ø4 floor drain each
- Toothpaste pocket: 50 × 26 mm, front, Ø4 floor drain
- Q-tip well: Ø42 mm, raised solid floor (no drain)
- Lid: Ø48 mm × 9 mm, plug-fit (0.8 mm clearance)

## Regenerate

```bash
projects/bathroom-toothbrush-organizer/3d/.venv/bin/python projects/bathroom-toothbrush-organizer/3d/build_all.py
```

## Print recipe

- Filament: SUNLU PLA+ 2.0 Oak Wood (select profile manually — no RFID)
- Orientation: body upright as it sits; lid cap-face down, plug up
- Supports: none — every feature is vertical or open at the top
- Settings: 0.2 mm layers, ~15% gyroid infill, 3 walls (keeps the scallop
  grooves strong where they cut into the wall)
- Drainage: the wet zone drains straight through the floor holes onto the
  counter/tray below — there are deliberately no standoff feet (they would
  force a first-layer bridge). A separate nesting drip tray is a possible
  follow-on if lift-off is wanted.
