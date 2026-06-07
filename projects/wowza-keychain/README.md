# Wowza keychain

Quarter-sized coin keychain with raised "Wowza" text on the front — for
Chelsea to hand out to students who score 100% on assignments.

## Print recipe

| Filament | Print time (one) | Plate density | Notes |
|---|---|---|---|
| SUNLU PLA+ 2.0 (any color) | ~12–18 min | 12+ per plate | Flat on bed, no supports needed |

Bambu Studio: select "SUNLU PLA+ 2.0" profile manually.

## Geometry summary

- **Coin**: 24.5 mm diameter × 4 mm thick (US-quarter sized)
- **Text**: "Wowza" raised 1 mm, in `Arial Rounded MT Bold`, auto-sized
  to leave 2 mm horizontal clearance inside the coin edge
- **Hole**: 5 mm diameter, 5 mm from the top edge — fits a standard split ring
- **Total height**: 5 mm

## Files

- `3d/keychain.py` — parametric build123d script
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Tweaking

All design parameters live at the top of `3d/keychain.py`. Common tweaks:

- Change the word: edit `WORD`
- Bigger / smaller coin: edit `COIN_DIAM`, text auto-rescales
- More breathing room: increase `TEXT_MARGIN`
- Thinner / thicker disk: edit `COIN_THICKNESS`

After editing, regenerate:

```bash
3d/.venv/bin/python 3d/keychain.py
```

Output goes to `3d/out/keychain.stl`.

## Background

See [`../../docs/superpowers/specs/2026-04-21-wowza-coin-keychain-design.md`](../../docs/superpowers/specs/2026-04-21-wowza-coin-keychain-design.md)
for the design that produced this.
