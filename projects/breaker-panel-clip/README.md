# Breaker panel clip

Small spacer block that slips into the gap below the bottom edge of an
exterior breaker / meter access panel. The panel is a friction-fit door
(push in + slide up to close) that occasionally slips down out of friction
and swings open. The block fills the bottom gap so the panel can't slide
down — once it can't slide down, it can't swing open.

No fasteners (no screws / adhesive / magnets). The panel's own weight plus
floor friction holds the block in place; a pull tab on the front lets you
yank it out when you need to open the panel.

## Print recipe

| Filament | Print time | Plate density | Notes |
|---|---|---|---|
| SUNLU PLA+ 2.0 (any color) | ~8–12 min | 1 per plate | Flat on bed, no supports needed |

Bambu Studio: select "SUNLU PLA+ 2.0" profile manually.

## Geometry summary

- **Block**: 12 mm wide × 20 mm deep × 7.3 mm tall — fills the panel-bottom
  gap (measured at ~7.5 mm; print starts undersize for easy first fit and
  is dialed up if it rattles)
- **Pull tab**: 12 mm wide × 15 mm long × 3 mm thick, with a 5 mm finger
  hole — extends forward from the block, accessible outside the cabinet
- **Total footprint**: 12 × 35 × 7.3 mm

## Files

- `3d/block.py` — parametric build123d script
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Tweaking

All design parameters live at the top of `3d/block.py`. Common tweaks:

- Tighter / looser fit in the gap: edit `BLOCK_HEIGHT` (±0.2 mm)
- More / less depth into the cabinet: edit `BLOCK_DEPTH`
- Tab too short to grip easily: edit `TAB_LENGTH`
- Bigger / smaller finger hole: edit `TAB_HOLE_DIAM`

After editing, regenerate:

```bash
3d/.venv/bin/python 3d/block.py
```

Output goes to `3d/out/block.stl`.
