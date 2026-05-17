# Clamp jaw pad

Slide-on replacement pad for the head of a parallel bar clamp. It caps
the flat steel jaw so the metal never marks the workpiece. The jaw
slides in through the open mouth and bottoms out against the solid
closed (D) end; two asymmetric lips curl over the channel and hold the
pad on the jaw's front face.

Pure-parametric — generated from `3d/pad.py`, no downloaded STL.

## Print recipe

| Filament | Orientation | Supports | Notes |
|---|---|---|---|
| SUNLU PLA+ 2.0 (any color) | Stand on the closed (D) end, slide axis vertical | None | Channel prints vertically — no bridge over the mouth window |

Bambu Studio: select "SUNLU PLA+ 2.0" profile manually. The D-end
footprint is small (27 × 10 mm) — add a brim if the first layer lifts.

**Grip caveat:** the original is a compliant plastic that grips by
flex. PLA+ is rigid and will not flex the same way. The channel is
reproduced as-measured (`FIT_CLEARANCE = 0.0`) for the tightest grip
PLA can give. After a test fit: if it will not slide on, raise
`FIT_CLEARANCE` in 0.2 mm steps; if it slides on but won't stay,
record it in `print-log.md` (a flexible-filament reprint is the real
fix, out of scope here).

## Geometry summary

- Outer body: 38.67 mm (slide) × 27 mm (across) × 10 mm (thick),
  stadium-rounded short ends
- Channel: 21 mm wide × 4 mm tall slot, ~36.2 mm deep
- Lips: 4 mm thick, overhang 2.0 mm (one edge) / 3.7 mm (other)
- Walls: 2.5 mm sides, 2.0 mm back, 2.5 mm closed end

## Files

- `3d/pad.py` — parametric build123d script
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Tweaking

All parameters live at the top of `3d/pad.py`. Common tweaks:

- Won't slide on / too tight: raise `FIT_CLEARANCE` (±0.2 mm)
- Different jaw width or thickness: edit `CHANNEL_WIDTH` / `CHANNEL_HEIGHT`
- Lip grip too weak/strong: edit `LIP_OVERHANG_A` / `LIP_OVERHANG_B`

After editing, regenerate:

```bash
3d/.venv/bin/python 3d/pad.py
```

Output goes to `3d/out/pad.stl`.
