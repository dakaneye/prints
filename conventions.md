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
from pathlib import Path

from build123d import Align, Box, export_stl  # explicit; whatever the part needs

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

## Print-readiness rules

These are CAD-side rules that prevent print failures we've actually hit.
Apply before exporting STLs.

### Labels: raised, not recessed

Any text or label on a part **must be raised relief**, not recessed
(engraved). Don't extrude a sketch with negative `amount` and subtract from
the part; extrude positive and add.

Reason: a recessed label on a top face forces the slicer to bridge across
each letter cavity at the recess-end Z height (typically 0.6 mm above the
bed when the engraved face is printed down). Bridges over 4-5 mm sag in
PLA — strands drop into the recess and obscure the text. Raised letters
print as the last feature on top of solid material, with no bridging,
clean letter edges, and shadow contrast that reads without paint-fill.

History: lid for `projects/electronics-organizer/` was first printed with
recessed labels — strands hung in the letter recesses and the `ELECTRONICS`
header and orientation triangle were unreadable. Reprinted with raised
labels, which fixed it.

Trade-off accepted: no Sharpie paint-fill (can't fill a raised feature).
Contrast comes from relief and shadow. Two-tone via mid-print filament
swap is still possible (manual swap at the raised-text Z height).

### Pre-print orientation review

Before handing STLs off to slicing, walk through orientation explicitly:

1. **Identify the print orientation** the slicer will use (or that you
   want it to use). Bambu Studio doesn't auto-orient on the A1 — what you
   import is what prints unless you rotate.
2. **Identify hanging structures** in that orientation — overhangs > 45°,
   bridges > 4 mm in PLA, ceilings over hollow cavities, undercuts.
3. **Pick one of three responses for each hanging structure**:
   - **Redesign the part** (preferred): flip orientation, split into
     multiple printable pieces, or change geometry (raised → recessed,
     fillet sharp corners) to remove the overhang.
   - **Accept supports**: tell the user explicitly that supports are
     needed, what kind (tree / normal / lightning), and where they'll
     contact the part. The user accepts the support-scar trade-off.
   - **Test bridge with a small sample**: print a 50×50 mm test piece
     first to validate that the bridge resolves cleanly on this filament.
4. **Document the decision** in the README's print recipe section so the
   next person (or future you) knows what supports / orientation matter.

History: the electronics-organizer lid would have been better caught at
orientation review — the strand failure was predictable from the recessed
labels at the bridge-edge Z. The fix is to redesign (raised labels), but
the second-line answer when redesign isn't an option is to use supports.

## IP / license posture

- Public-facing strings (README, folder names, commit messages, issue titles)
  are IP-neutral. Use generic descriptors ("wizard figurine") rather than
  copyrighted character names.
- Internal design docs (`docs/superpowers/specs/`, `print-log.md`) can name
  characters freely — these are design history, not a public-facing website.
- `projects/*/downloaded/` is globally gitignored. Third-party STLs are never
  committed. `SOURCES.md` links out to the hosting site without mirroring
  bytes.
