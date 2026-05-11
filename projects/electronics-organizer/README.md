# Electronics organizer

> **v1 status: failed.** The v1 STLs were printed and don't fit the items
> they were designed for. See `print-log.md` for the post-mortem. Bins
> are usable for loose components; the tote + lid are not usable as-is.
> A v2 will likely pivot to a community-published Gridfinity case rather
> than another custom build123d pass.

A portable parts case for the word-clock Phase 2 BOM and its multipack
spares. Friction-fit lid with a layout map on top — the case identifies
its own contents at a glance when closed.

Three internal zones:

- **Zone A — Gridfinity 3×3 grid**: 9 removable bins for small breakouts
  and ICs (ESP32, RTC, amp, microSD breakout, USB-C breakout, tact
  switches, speakers). Bins are dimensionally compatible with the desk-
  drawer baseplate, so spares can move between drawer and case freely.
- **Zone B — LED reel pocket**: cylindrical well for the WS2812B 5 m spool.
- **Zone C — subcase wells**: two rectangular drop-in pockets sized to
  the existing capacitor and header-pin organizer cases.

Design doc: [`docs/superpowers/specs/2026-05-09-electronics-organizer-design.md`](../../docs/superpowers/specs/2026-05-09-electronics-organizer-design.md).

## What's inside (lid map)

```
                ELECTRONICS
   +-----------------------------+
   |   LEDS    |     CAPS        |   ← back row
   |   (reel)  |   (cap case)    |
   +-----------+--+--------------+
   | ESP32 | RTC| AMP |          |
   |       |    +-----+ HEADERS  |
   |       |    | uSD |          |
   |       |    +-----+ (header  |
   |       |    |     |   pin)   |
   +-------+----+ USB-C +--------+
   | (orientation triangle)      |
   +-----------------------------+
```

(Approximate; actual positions come from `case.py`.)

## Compartment list

| Compartment | Holds | Stash |
|---|---|---|
| 1×2 bin `ESP32` | ESP32 DevKit V1 | 3-pack |
| 1×2 bin `RTC` | DS3231 RTC modules | 5-pack spares |
| 1×1 bin `AMP` | MAX98357A amp | 2-pack |
| 1×1 bin `uSD` | microSD breakout + microSD card | 2-pack |
| 1×1 bin `USB-C` | USB-C breakout | 10-pack |
| 1×1 bin `BTNS` | Tact switches | 20-pack |
| 1×1 bin `SPKR` | 8 Ω 40 mm speakers | 4-pack stacked |
| Reel pocket `LEDS` | WS2812B 5 m reel | 1 |
| Well `CAPS` | Capacitor subcase | existing |
| Well `HEADERS` | Header pin subcase | existing |

## Print recipe

Bambu A1 with `0.20mm Standard @BBL A1` profile, **filament selected
manually** to "SUNLU PLA+ 2.0" (no RFID on the spool). Grey or white both
work — grey hides print lines better; white reads the engraving better
without paint-fill.

| Setting | Value |
|---|---|
| Layer height | 0.2 mm |
| Walls | 3 (tote + lid), 2 (bins) |
| Infill | 15% gyroid |
| Supports | None |
| Brim | None (textured PEI) |

A1 bed is 256 × 256 mm. Every part fits in one shot:

| STL | Footprint (mm) | Height | Volume | Print copies |
|---|---|---|---|---|
| `tote.stl` | 223 × 225 | 50 mm | ~540 cm³ | 1 |
| `lid.stl` | 230 × 232 | 8 mm | ~93 cm³ | 1 |
| `bin_1x1x6U.stl` | 41.5 × 41.5 | 45.6 mm | ~18 cm³ | 5 |
| `bin_1x2x6U.stl` | 41.5 × 83.5 | 45.6 mm | ~32 cm³ | 2 |

Total filament (mesh volumes; slicer will report less with infill):
~775 cm³ ≈ 960 g at 100% — expect 350–450 g actual at the recipe above.
Total print time ≈ 20–25 hours across all plates (tote alone is the
single longest print at ~12–15 h).

## Files

- `3d/case.py` — outer tote + lid generator (the meat)
- `3d/bins.py` — Gridfinity bin set for Zone A
- `3d/build_all.py` — regenerate every STL in `3d/`
- `3d/requirements.txt` — `build123d` + `gridfinity-build123d`
- `downloaded/SOURCES.md` — provenance for the gridfinity library
- `print-log.md` — per-print diary

## Setup (per-project venv)

```bash
python3.13 -m venv 3d/.venv
# gridfinity-build123d installs from a git URL. If you have a global
# url.git@github.com:.insteadof rewrite (SSH+YubiKey), bypass it for
# this command:
GIT_CONFIG_GLOBAL=/dev/null 3d/.venv/bin/pip install -r 3d/requirements.txt

3d/.venv/bin/python 3d/case.py        # tote + lid
3d/.venv/bin/python 3d/bins.py        # bin starter set
3d/.venv/bin/python 3d/build_all.py   # everything
```

Generated STLs land in `3d/out/`. Both directories are gitignored.

## Importing into Bambu Studio

For each STL:

1. **File → Import → Import 3MF/STL** (drag-drop also works). `Open
   Project` only handles `.3mf` bundles, so don't use it.
2. Filament: select **"SUNLU PLA+ 2.0"** manually.
3. Profile: `0.20mm Standard @BBL A1`. No brim needed on textured PEI.
4. Lay it flat — the script exports with the right side up.
5. For bins, set quantity per the table (Right-click → Set quantity → N).
6. Slice → preview to confirm the engraving comes out as recessed text
   and the wells aren't bridged shut → Print.

Suggested print sequence:

1. **Bins first** (~30 min each, low risk) — verify Gridfinity geometry
   prints cleanly on this machine before committing to the bigger parts.
2. **Lid second** — confirms the engraved labels are legible and lets you
   tune contrast (see below) before printing the tote.
3. **Tote last** — the long print, after the rest is validated.

## Lid label contrast

The lid labels are **raised 0.6 mm** relief, not recessed (see
`conventions.md` — recessed text bridges poorly in PLA). Contrast comes
from shadow and surface relief; readability is good in indirect light.

If you want higher contrast:

- **Two-tone via filament swap:** in Bambu Studio, add a manual
  filament-change `M600` at the layer where the raised text begins
  (lid top face = 8.0 mm from bed). Print body in grey, swap to white
  for the raised-label layers (top 0.6 mm). ~5 min interruption mid-print.

(Sharpie paint-fill doesn't work on raised features — it was an option for
the earlier recessed design but doesn't apply here.)

## Tweaking

All parameters live at the top of the relevant script.

**`3d/case.py`** — outer tote + lid:

- `COMPARTMENTS` — list of `(label, kind, args)`. Add/remove rows to
  reshape the layout. Three kinds:
  - `"bin"` — Gridfinity cell. Args `(cols, rows)`. Cell goes into Zone A.
  - `"well"` — rectangular drop-in well. Args `(width, depth, height)` in
    mm — these are the SUBCASE EXTERNAL dims; clearance is added in code.
  - `"reel"` — cylindrical pocket. Args `(diameter, depth)` in mm — reel
    external dims; clearance added in code.
- `LID_CLEARANCE` (default `0.30`) — XY gap between tote outer wall and
  lid inner wall. Tuning knob if first print is too tight (increase to
  `0.35`) or too loose (decrease to `0.25`).
- `ENGRAVE_DEPTH` (default `0.6` mm) — deeper engraving reads better but
  weakens the lid roof; don't exceed `LID_TOP_THICKNESS - 1.0`.
- `LABEL_FONT` (default `"Arial"`) — falls back gracefully if the font
  isn't present (build123d will pick a default sans-serif).

After editing, regenerate:

```bash
3d/.venv/bin/python 3d/case.py
```

**`3d/bins.py`** — bin set:

- `BINS` — list of `(cols, rows, height_U, qty)` where 1U = 7 mm. Add or
  remove rows when changing the case layout.

The current bins are blank (single open cavity, no internal dividers).
For purpose-shaped inserts (speaker cradle, divided tact-switch slots),
download a community bin from MakerWorld / Printables and log it in
`downloaded/SOURCES.md`. Bin sizes match `gridfinity-build123d` defaults
(1×1 = 41.5 × 41.5 mm, 1×2 = 41.5 × 83.5 mm).

## v2 candidates

Documented in the design spec, deferred for v1:

- Print-in-place hinge for the lid (better ergonomics, but PLA hinges
  fatigue in this size range)
- Two-tone lid via mid-print filament swap
- Repurposing the dead strip below the header-pin well as a labeled
  "MISC" cubby
