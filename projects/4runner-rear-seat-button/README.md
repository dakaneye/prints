# 4Runner rear seat release button

Replacement for the small button that releases the rear seatbacks (the
fold-down button on the seat shoulder) on a 5th-gen Toyota 4Runner
(2010–2018). OEM part `72661-35010`. Pure download from Thingiverse — no
custom CAD on this one.

See `downloaded/SOURCES.md` for the URL, author, and license.

## Variants in the download

Two STLs:

- `Button_Domed.stl` — original release. Slight dome on top; closest
  visual match to the OEM button.
- `Button_Not_Domed_Top.stl` — flat-top revision. Easier to print
  cleanly, but doesn't match the OEM dome.

If only one button is missing, print **Domed** so it matches the OEM
button still installed on the other seat. If both are gone, either is
fine — just print two of the same.

A Fusion 360 source (`ButtonFusionPlans.f3d`) is also bundled if the fit
needs tweaking.

## Print recipe

| Filament | Print time | Notes |
|---|---|---|
| SUNLU PLA+ 2.0 grey | ~30 min (est) | Closest match to the OEM dark-grey interior trim. |

**Orientation: dome down on the bed, open cavity facing up.** No
supports needed in this orientation:

- Dome face goes against the build plate → mirror-smooth finish on the
  visible side.
- The cavity is open-topped → no ceiling to bridge, no internal
  supports.
- Outer walls flare ~5–10° from vertical going up → within unsupported
  overhang range.

Add a **brim** — the dome's small contact patch needs help adhering.

Author notes the fit is "not perfect" — light sanding may be needed if
it doesn't seat cleanly on the post in the seat trim.

## Files

- `downloaded/` (LOCAL ONLY — gitignored) — the two STLs + Fusion source
- `downloaded/SOURCES.md` — provenance and license
- `print-log.md` — per-print diary
