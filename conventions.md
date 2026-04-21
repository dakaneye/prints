# Conventions

## Folder layout per project

```
projects/<kebab-case-name>/
├── README.md          # What this project is, print settings, photos
├── downloaded/        # GITIGNORED — third-party STLs pulled locally only
│   └── SOURCES.md     # URL + author + license + download date, one per STL
├── 3d/                # Optional — build123d scripts for parametric parts
│   ├── requirements.txt
│   ├── *.py           # One script per part
│   ├── build_all.py   # Regenerates every sibling *.py
│   └── out/           # GITIGNORED — generated STLs go here
└── print-log.md       # Per-print diary (success/fail/lessons/photos)
```

## Naming

- Project folders: `kebab-case`, descriptive, IP-neutral (no copyrighted
  character names in public-facing strings)
- `build123d` scripts: `snake_case.py`, one part per file
- STL output: generator writes to `out/<same_name_as_script>.stl`

## Filament catalog (on hand as of 2026-04-21)

| Filament | Brand | Notes |
|---|---|---|
| Black | SUNLU PLA+ 2.0 | General purpose |
| White | SUNLU PLA+ 2.0 | Best for painting; prime canvas |
| Grey | SUNLU PLA+ 2.0 | Neutral, hides print lines |
| Oak Wood | SUNLU PLA+ 2.0 | Wood-filled; visible grain, good unpainted |

Bambu Studio filament profile: select **"SUNLU PLA+ 2.0"** manually (no RFID
auto-detect on third-party spools).

## `build123d` script convention

Every script in any `3d/` directory follows these three sections:

```python
"""Explain the part in plain English."""
from build123d import *
from pathlib import Path

# ─── Parameters ──
# All dimensions in mm. Source of numbers in comments.
WIDTH = 90.0

# ─── Geometry ──
# Primitive shapes combined with +, -, &.
# align=(CENTER, CENTER, MIN) = bottom of shape at Z=0, centered in XY.
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
part = Box(WIDTH, 60, 10, align=BOTTOM)

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(part, str(out_dir / "part.stl"))
```

## IP / license posture

- Public-facing strings (README, folder names, commit messages, issue titles)
  are IP-neutral. Use generic descriptors ("wizard figurine") rather than
  copyrighted character names.
- Internal design docs (`docs/superpowers/specs/`, `print-log.md`) can name
  characters freely — these are design history, not a public-facing website.
- `projects/*/downloaded/` is globally gitignored. Third-party STLs are never
  committed. `SOURCES.md` links out to the hosting site without mirroring
  bytes.
