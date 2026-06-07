# Pitcher spigot valve

A printable quarter-turn plug-valve replacement for a broken push-button
spigot on a glass beverage pitcher. Reuses the original rubber gasket;
everything else is printed.

## Parts (in `3d/`)

- `body.py` — through-wall threaded barrel, gasket flange, tapered plug
  seat, downward spout
- `plug.py` — tapered plug with an L-shaped bore and a lever paddle
- `nut.py` — clamp nut (matched thread, wide bearing face)
- `retainer.py` — press-fit collar that holds the plug down

## Mount (glass wall — handle gently)

Outside → inside: body flange · **rubber gasket** · glass · nut.
Finger-tight only. The gasket seals; clamping force does not. Do not
torque a nut against glass.

## Print settings

- SUNLU PLA+ 2.0 (manual filament profile in Bambu Studio)
- ≥4 perimeters on body and plug so water does not weep through layer lines
- Body: barrel pointing up, spout supported. Plug: lever up.
- Food-safe silicone grease on the plug taper before assembly.

First print is a fit prototype — tune `PLUG_CLEAR` in `plug.py` until the
plug turns smoothly and seats. Leak-test with water before use.
