# Wizard figurine for Wallace

A wizard-themed figurine with a personalized engraved oak display base —
built for my 8-year-old nephew as his introduction to 3D printing.

## What's in this folder

- `downloaded/` (LOCAL ONLY — gitignored) — the downloaded figurine STL
- `downloaded/SOURCES.md` — provenance: URL, author, license, date per STL
- `3d/base.py` — parametric engraved display base (Python / build123d)
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Print recipe

| Part | Filament | Print time | Notes |
|---|---|---|---|
| Figurine (downloaded) | Oak Wood PLA | ~5–7h | ~100mm tall; minimal supports |
| Display base (`base.py`) | Oak Wood PLA | ~1–2h | Engraved name + print date |

Slicer: Bambu Studio, "SUNLU PLA+ 2.0" profile manually selected.

## Assembly

V1: figurine's feet sit into a recessed footprint in the base — no glue.
Fallback: single dot of PLA-safe super glue, or hidden M3 insert + screw.

## How to run this with Wallace

Four deliberate teaching beats — don't skip them:

1. **"The internet has amazing builders"** — browse MakerWorld together,
   look at the STL author's profile, credit them by name. Someone *made*
   this.
2. **"But we can make our own too"** — open `3d/base.py`, change the
   engraved text live (demo: change the name → regenerate → look at the
   new STL → change back). Same file, different part.
3. **"Watch the robot build it"** — start the figurine print together,
   watch the first 15 minutes, explain layer height ("each line is
   thinner than a hair"), start Bambu Studio's time-lapse capture.
4. **"The reveal"** — pop the figurine off the plate, snap into the
   base, hand it over. Set expectations if unpainted: "this is the
   wooden version — we'll paint it together next time."

## Version history

- **v1 (this print):** unpainted, oak-wood figurine + engraved oak base
- **v2 (future):** paint session (Army Painter Speedpaint kit)
- **v3+ (future):** additional poses / companion figures
