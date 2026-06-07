# Bathroom toothbrush organizer

A reeded-wall family bathroom organizer. Holds 3 manual toothbrushes
(1 adult + 2 kids) and a toothpaste tube in an open, draining wet zone, with
a walled-off, covered q-tip cubby that stays dry. Pure parametric (build123d),
with a smooth vertically-reeded outer wall. Built as a thin-walled hollow shell
(mostly empty inside) so it prints fast and light. Design history:
`docs/superpowers/specs/2026-06-07-bathroom-toothbrush-organizer-design.md`.

## Parts

| Part | Script | Output |
|---|---|---|
| Body | `3d/organizer.py` | `out/organizer.stl` |
| Q-tip lid | `3d/qtip_lid.py` | `out/qtip_lid.stl` |

## Dimensions

- Body: 188 W × 70 D × 80 H mm, 18 mm corner radius
- Outer wall: smooth vertical reeding, ~7.5 mm flute pitch, ~0.55 mm deep,
  bounded by a smooth 6 mm base band and 5 mm top rim (flush with flute crests)
- Construction: hollow shell, 3 mm outer wall + floor, 2.4 mm socket walls
  (~285 cm³ of material vs ~680 cm³ if printed solid)
- Brush sockets: 3 × Ø18 mm, back row, Ø4 floor drain each
- Toothpaste pocket: 56 × 30 mm, front, Ø4 floor drain
- Q-tip well: 64 × 46 mm oval (long axis left-right), center-right, raised solid floor (no drain)
- Lid: 70 × 52 mm oval × 9 mm, plug-fit (0.8 mm clearance)

## Regenerate

```bash
projects/bathroom-toothbrush-organizer/3d/.venv/bin/python projects/bathroom-toothbrush-organizer/3d/build_all.py
```

## Print recipe

- Filament: SUNLU PLA+ 2.0 Oak Wood (select profile manually — no RFID)
- Orientation: body upright as it sits; lid cap-face down, plug up
- Supports: none — every feature is vertical or open at the top
- Settings: 0.2 mm layers, 3 walls. The body is a hollow shell, so infill
  barely applies — keep it low (≤10%); wall count carries the strength.
- Drainage: the wet zone drains straight through the floor holes onto the
  counter/tray below — there are deliberately no standoff feet (they would
  force a first-layer bridge). A separate nesting drip tray is a possible
  follow-on if lift-off is wanted.
