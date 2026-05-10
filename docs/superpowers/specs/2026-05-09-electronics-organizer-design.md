# Electronics organizer — design

**Date:** 2026-05-09
**Status:** approved (brainstormed), pending implementation
**Project location:** `projects/electronics-organizer/`
**Trigger:** word-clock Phase 2 BOM landing in bulk multipacks (3× ESP32, 5× DS3231, 4× speakers, 10× USB-C breakouts, 20× tact switches, plus 5 m WS2812B reel and existing capacitor / header-pin subcases). Need a labeled home for both the in-use parts and the carryover spares.

## What it is

A single portable parts-organizer case with a friction-fit lid. The lid's top face is engraved with a 1:1 layout map showing what's in each compartment underneath, so the case identifies its own contents at a glance when closed.

Three internal zones:

- **Zone A — Gridfinity grid** (3 × 3 = 9 cells): removable bins for small electronics — ESP32, RTC, amp, microSD breakout, USB-C breakout, tact switches, speakers
- **Zone B — LED reel pocket**: cylindrical well sized to the WS2812B 5 m spool
- **Zone C — subcase wells**: rectangular drop-in pockets sized to the existing capacitor and header-pin organizer cases

## Origin

Trigger was the Phase 2 word-clock parts arrival — most line items are multipacks where 1 unit goes onto the breadboard and 2-19 units go into a "where do I keep this?" pile. Shelving the bare bags was the path of least resistance and would have aged badly: a year from now, the user opens the bag and has no idea which IC is which without reading the silkscreen with a loupe. Labeled, fixed-location storage is the durable answer.

## Scope: what's in vs out

In:
- The 5m WS2812B reel
- Existing capacitor and header-pin subcase
- Small breakouts and ICs from the Phase 2 BOM (ESP32, DS3231, MAX98357A, microSD breakout, USB-C breakout, tact switches, speakers)

Out (lives elsewhere on the shelf):
- The fabricated PCB itself (one-off, no spares to organize)
- Resistors / jumper wire kit / alligator clips (already organized in their own kit packaging — no wins from re-organizing)
- Breadboard (too big and used in-place)
- USB-C cable and 5V charger (cable storage is its own problem)

This was a deliberate scope cut during brainstorming — the case is sized for the high-value, currently-disorganized parts, not "all electronics ever."

## Design decisions and the reasoning

### Form factor — single tackle-box case (B over A/C)

Considered: drawer-resident Gridfinity (already exists in `desk-drawer-gridfinity`), portable case with lid, open shelf rack, wall-mounted pegboard. Picked portable case because the parts move between storage and workbench during build sessions, and a closed case is dust-resistant for parts that may sit untouched for months.

### Single compartmented case, not a system of mini-boxes

Considered a tote of small individually-lidded boxes (one per part type). Rejected: more print time, more lids to lose, label ergonomics worse (you'd have to read each box's lid). One case with one labeled lid is faster to scan visually.

### Lid map (option C from brainstorm), not engraved bin walls or paper labels

Considered: engraved bin walls (recessed text per cell), paper-label slot per cell, lid map showing layout, hybrid. Picked lid map because:
- Re-labeling = reprint the lid only, not the tray (cheap and decoupled)
- Single piece of geometry holds all the labels — easier to layout, render, paint-fill
- When the case is closed and stacked, you can still tell what's in it without opening
- The Gridfinity bins are removable; lid map remains the single source of truth

Trade-off accepted: the map only stays accurate as long as bins are returned to their home cells. This is a "guidance, not contract" relationship.

### Friction-fit removable lid (option A from brainstorm)

Considered: friction-fit, print-in-place hinge, separate lid + living hinge tab, magnet-latched. Picked friction-fit for v1 because the whole point of putting labels on the lid is that the lid is a separately-printable object — friction-fit makes it cheap to iterate. User flagged the print-in-place hinge as a "better feel" idea worth revisiting in v2.

### Hybrid: custom outer tote + Gridfinity bins inside (search-first finding)

Prior-art research confirmed: no existing community design hits all four requirements at once (friction-fit lid + drop-in subcase wells + LED reel pocket + engraved lid map). But the small-bin-with-labels piece is well-trodden territory — the `moritzmhmk/gridfinity-build123d` library (already a dependency in `desk-drawer-gridfinity/`) provides `Bin`, `SubdividedCompartment`, and `with_label=True`.

Decision: hand-roll only the parts no library covers (outer tote, lid sleeve, LED reel pocket, subcase wells, engraved lid map), and pull bins from `gridfinity-build123d`. Bonus: bins are dimensionally compatible with the desk-drawer baseplate, so a "spare ESP32 bin" can move between drawer and case without modification.

References reviewed (and rejected for not matching all four requirements):
- [Pred's Gridfinity Storage Box](https://www.printables.com/model/543553-gridfinity-storage-box-by-pred-now-parametric) — hinged + label slots, F3D source only
- [Modern Gridfinity Case](https://www.printables.com/model/894202-modern-gridfinity-case) — hinged + label slots, no engraved map
- [Gridfinity Rugged Case Light R3](https://makerworld.com/en/models/463249-gridfinity-rugged-case-light-r3-150-sizes) — same pattern
- [Cullenect Swappable Labels](https://makerworld.com/en/models/446624-cullenect-swappable-labels-for-gridfinity-and-more) — solves bin labeling, not lid mapping

### Layout A (recommended), not B (tile-split, 16 cells) or C (drop header-pin case)

Three layouts considered:
- **A:** 3 × 3 Gridfinity grid + LED reel + cap case + header pin case. Footprint ~220 × 225 mm, fits the A1 bed in one shot. Small (~50 × 30 mm) dead space below the header-pin well.
- **B:** 4 × 4 Gridfinity (16 cells, 7 spare) + all subcases. Footprint ~290 × 260 mm — exceeds the 256 mm A1 bed, requires tile-split with dovetail keying.
- **C:** Same as A but drops the header-pin well to fit the bed cleanly.

Picked A. B is over-built — most of those 7 spare cells would print empty, and tile-split is a real cost (longer print, joint line, lid also splits). C drops a thing the user explicitly wanted in. A hits every spec and prints in one shot.

### Recessed-only engraving with optional Sharpie paint-fill

Bambu A1 has no AMS for this user, and they're committed to single-filament SUNLU PLA+ 2.0. Three contrast options considered:
- Recessed-only (default): readable in indirect light
- Sharpie paint-fill: ~2 minutes per lid, high contrast, no print interruption — recommended for v1
- Filament swap mid-print at the engraving Z height: true two-tone, ~5 min interruption — documented in README as v2 recipe

## Final geometry (v1)

### Tote

| Parameter | Value | Notes |
|---|---|---|
| `OUTER_FOOTPRINT` | ~220 × 225 mm | Auto-derived from compartment list + layout |
| `WALL_THICKNESS` | 3.0 mm | 3 perimeters at 0.4 mm nozzle |
| `FLOOR_THICKNESS` | 3.0 mm | Strong, flat |
| `INTERIOR_HEIGHT` | 45 mm | Driven by tallest content: 6U bins (42 mm) + 3 mm headroom. Cap subcase (23 mm), LED reel (15 mm), header pin (19 mm) all sit well below the bin tops. |

### Zones

| Zone | Compartment | Size (interior) | Clearance |
|---|---|---|---|
| A | Gridfinity 3 × 3 | 126 × 126 mm | per Gridfinity spec (4.75 mm baseplate inset) |
| B | LED reel (`reel`) | ø 79 mm × 15 mm deep | +4 mm dia, +2 mm depth over reel |
| C | Capacitor case (`well`) | 133 × 88 × 23 mm deep | +3 mm W&D, +1 mm H |
| C | Header pin case (`well`) | 103 × 68 × 19 mm deep | +3 mm W&D, +1 mm H |

### Lid

| Parameter | Value | Notes |
|---|---|---|
| `LID_OVERLAP` | 6 mm | Sleeves outside the tote |
| `LID_CLEARANCE` | 0.30 mm per side | Tuning knob if too tight or too loose on first print |
| `ENGRAVE_DEPTH` | 0.6 mm | Deep enough for Sharpie paint-fill |
| `LABEL_FONT` | Liberation Sans Bold | Build123d default; bundled font, CI-safe |
| Header text | "ELECTRONICS" | ~10 mm cap height across top edge |

### Compartment list (and lid labels)

| Bin / well | Label on lid | Holds | Stash size |
|---|---|---|---|
| 1×2 bin | `ESP32` | ESP32 DevKit V1 | 3-pack |
| 1×2 bin | `RTC` | DS3231 RTC modules | 5-pack spares |
| 1×1 bin | `AMP` | MAX98357A amp | 2-pack |
| 1×1 bin | `µSD` | microSD breakout + microSD card | 2-pack |
| 1×1 bin | `USB-C` | USB-C breakout | 10-pack |
| 1×1 bin | `BTNS` | Tact switches | 20-pack |
| 1×1 bin | `SPKR` | 8Ω 40 mm speakers | 4-pack stacked (~28 mm) |
| Reel pocket | `LEDS` | WS2812B 5 m reel | 1 |
| Well | `CAPS` | Capacitor subcase | 1 (existing) |
| Well | `HEADERS` | Header pin subcase | 1 (existing) |

## Architecture

### Files

```
projects/electronics-organizer/
├── 3d/
│   ├── case.py            # outer tote + lid, engraved map
│   ├── bins.py            # bin set for Zone A (mirrors desk-drawer-gridfinity/3d/bins.py)
│   ├── build_all.py       # runs case.py + bins.py
│   ├── requirements.txt   # build123d + gridfinity-build123d
│   └── out/               # gitignored — emitted STLs
├── downloaded/
│   └── SOURCES.md         # link out to gridfinity-build123d, license note
├── README.md              # print recipe + tweaking guide
└── print-log.md           # per-print diary
tests/test_electronics_organizer.py  # smoke tests for case.py and bins.py
```

### Script structure (`case.py`, three-section convention)

```python
# === Parameters ===
COMPARTMENTS = [
    ("LEDS",    "reel", 75, 15),
    ("CAPS",    "well", 130, 85, 22),
    ("HEADERS", "well", 100, 65, 18),
    ("ESP32",   "bin",  1, 2),
    ("RTC",     "bin",  1, 2),
    ("AMP",     "bin",  1, 1),
    ("µSD",     "bin",  1, 1),
    ("USB-C",   "bin",  1, 1),
    ("BTNS",    "bin",  1, 1),
    ("SPKR",    "bin",  1, 1),
]
LAYOUT = "A"  # A | B | C — Section 3 of brainstorm doc

WALL_THICKNESS, FLOOR_THICKNESS = 3.0, 3.0
LID_OVERLAP, LID_CLEARANCE = 6.0, 0.30
WELL_CLEARANCE_W, WELL_CLEARANCE_H = 3.0, 1.0
ENGRAVE_DEPTH, LABEL_FONT = 0.6, "Liberation Sans Bold"
LABEL_CAP_HEIGHT_BIN_1x1 = 4.0
LABEL_CAP_HEIGHT_BIN_1x2 = 5.0
LABEL_CAP_HEIGHT_WELL    = 7.0
HEADER_TEXT = "ELECTRONICS"
TILE_SPLIT_THRESHOLD = 250.0

# === Geometry ===
# 1. Compute zone bounding boxes from COMPARTMENTS + LAYOUT.
# 2. Tote: outer wall + floor; cut Gridfinity baseplate (Zone A),
#    LED reel pocket (Zone B), subcase wells (Zone C).
# 3. Lid: closed-top sleeve at outer-wall + clearance; engrave header,
#    per-cell labels, perimeter outlines, orientation triangle.
# 4. Tile-split if footprint exceeds threshold (not expected for Layout A).

# === Export ===
# Write tote.stl, lid.stl to ./out/.
```

### Bins (`bins.py`)

Mirrors `desk-drawer-gridfinity/3d/bins.py` — enumerates unique `(cols, rows, height_U)` tuples from `COMPARTMENTS` and emits one STL per unique combo. Default bin height: 6U (42 mm) — fits the speaker stack, shallow enough that contents are visible at a glance.

### Tests (`tests/test_electronics_organizer.py`)

Same shape as `tests/test_wowza_keychain.py`:
- `test_case_script_produces_valid_stls` — runs `case.py` as a subprocess, asserts `tote.stl` > 50 KB and `lid.stl` > 30 KB. If tile-split is triggered, asserts the additional tile STLs.
- `test_bins_script_produces_valid_stls` — runs `bins.py`, asserts at least one STL per unique bin size.

## Print recipe

| Setting | Value | Notes |
|---|---|---|
| Filament | SUNLU PLA+ 2.0 | manual selection in Bambu Studio (no RFID) |
| Profile | `0.20mm Standard @BBL A1` | |
| Layer | 0.2 mm | |
| Walls | 3 (tote), 2 (lid, bins) | |
| Infill | 15% gyroid | |
| Supports | None | LED reel pocket and subcase wells are open-top; Gridfinity baseplate prints support-free with the cell openings up |
| Brim | None | Textured PEI |

Per-piece print quantities:
- `tote.stl` × 1
- `lid.stl` × 1
- Bins: 2× (1×2) + 5× (1×1) per the compartment list — 7 STLs, total volume comparable to the desk-drawer bin set (~150 cm³)

Optional contrast pass on the lid:
- **Sharpie:** print, run a black/silver Sharpie over the recessed engraving, wipe excess from the surface with a paper towel
- **Two-tone (v2):** in Bambu Studio, add a manual filament-change M600 at the lid's engraving Z height (top 0.6 mm); print body in grey, swap to white for the engraving layer

## Open questions / v2 candidates

1. **Print-in-place hinge** — user flagged option B from the lid-attachment question as a "better feel" idea. Worth a v2 if friction-fit lid feels too disposable.
2. **Two-tone engraving via filament swap** — documented in README, not implemented in v1.
3. **Header-pin well dead space** — Layout A leaves ~50 × 30 mm of dead space below the header-pin well. Could become a labeled "MISC" cubby in v1 (cheap to add) or repurposed in v2.
4. **Stacking** — case is one-off in v1. If the user prints a sibling case (other domains, other projects), the lid skirts could be designed to stack rim-on-rim. Not in v1.

## Anti-goals (explicitly out of scope)

- A general "every-electronics" organizer with empty bins for stuff not yet owned (YAGNI; reprint when needed)
- AMS / multi-material print (user runs single-filament SUNLU PLA+ 2.0)
- Re-labelable paper inserts (chose engraved lid map instead — different ergonomics)
- Stackable / lockable case for transport (not a transport problem; it's a desk-to-shelf problem)
