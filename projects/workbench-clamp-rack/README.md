# Workbench clamp rack

Head-up holders for two light bar/F-style clamps on the garage
Multiboard wall. Each clamp hangs with its bar perpendicular to the
ground: the fixed-jaw head sits in a forward-facing cradle, the bar
drops through a slot in the bottom and hangs straight down, the
sliding jaw dangles below.

Generated, not hand-authored. The cradle is one part from Andy
Levesque's QuackWorks **Vertical Item Holder** OpenSCAD generator,
built with a **Multipoint slot** back that takes an official
Multiboard screw-down connector (see Mount). We only supply
parameters. Print the one cradle **twice**; mount each wherever the
spacing suits you — the tiled wall sets clamp spacing, not the part.

See `downloaded/SOURCES.md` for generator provenance and license.

## Measured clamp (generic light bar clamp, no brand markings)

| Dimension | Value | How used |
|---|---|---|
| Bar width | 19.5 mm | Bottom slot the bar hangs through |
| Bar thickness | 6.3 mm | Bottom slot depth |
| Bar length | 555 mm (~22") | Dangle below the cradle — needs clear drop |
| Fixed-jaw reach/depth | 85 mm | Cradle depth out from the wall |
| Head height | 27 mm | Cradle internal height (vertical capture) |
| Head thickness | 18 mm | Cradle internal width (along the wall) |
| Weight (each) | ~834 g (837 / 831) | 2 clamps ≈ 1.67 kg / 3.7 lb total |

**Assumption to verify against the test print:** an earlier
measurement gave a "head width" of 110 mm. The cradle is sized from
the three explicit numbers above (reach 85 / height 27 / thickness
18), not the 110 mm. If the fixed-jaw casting is actually ~110 mm in
the dimension that has to enter the pocket, the cradle is undersized —
catch this on the single test print before printing the second.

## Mount

The cradle back is a **Multipoint slot** (the recessed channel — this
is correct and intentional, not a missing feature). It does not
mount to the tile directly. Mounting is a three-piece stack:

```
cradle (Multipoint slot)  ◄─  official Multiboard screw-down
                              connector (slides into the slot)
                                      │ screw
                                      ▼
                              Multiboard Core tile point
```

The heavy-duty mount is a two-part official Multiboard kit (see
`downloaded/SOURCES.md`):

1. **Heavy Weight-Bearing Hook Snap** — pushes onto the cradle's
   Multipoint negative rail. Directional: holds load in one
   direction, inserted at an angle, arrow pointing **up** (a hung
   clamp is pure downward load, so this is the correct orientation).
2. **Small Thread Multipoint** — the screw piece that secures the
   snap and threads into the tile point. This is the screw; it comes
   from this part, not the cradle. Use this, not a generic T-bolt
   (reported to bend apart under load).

One of each per cradle → two of each for this project.

**Constraint:** Heavy Hook Snaps only work with tiles **offset from
the wall** (the angled insert needs clearance behind the tile). The
`workbench-pegboard-multiboard` tiles are standoff-mounted on the
pegboard adapters, so this should hold — but confirm the standoff
depth clears the angled insert on the test mount.

Generated with `Connection_Type="Multipoint"` so the slot matches
the official Multipoint connector. The QuackWorks Multipoint slot is
built to the same Keep Making spec the official connector targets;
the single-cradle test gate below is the physical proof.

Load per cradle ≈ 0.83 kg plus a forward-tipping moment from the
~90 mm pocket depth (≈ 0.4 N·m). A single screw-down connector into a
tile point is the heavy-duty Multiboard mount and is well within range
for this — far stronger than the tool-free snap. The deep forward
pocket on one connector point is still the weakest aspect; the load
gate proves it before the second print.

## Regenerate the STL

Canonical path — **nix CLI OpenSCAD** (no `.app`, no Gatekeeper). This
is what produced the committed-as-provenance STL. From the repo root:

```bash
mkdir -p projects/workbench-clamp-rack/downloaded/out
OPENSCADPATH="projects/workbench-clamp-rack/downloaded" \
nix run --extra-experimental-features 'nix-command flakes' nixpkgs#openscad -- \
  -o projects/workbench-clamp-rack/downloaded/out/clamp_head_cradle_multipoint.stl \
  -D 'Connection_Type="Multipoint"' \
  -D 'internalWidth=22' -D 'internalDepth=90' -D 'internalHeight=30' \
  -D 'wallThickness=3' -D 'baseThickness=3' \
  -D 'frontCutout=true' -D 'frontUpperCapture=0' \
  -D 'frontLowerCapture=8' -D 'frontLateralCapture=3' \
  -D 'cordCutout=true' -D 'cordCutoutDiameter=21' \
  -D 'cordCutoutDepthOffset=-33' \
  "projects/workbench-clamp-rack/downloaded/QuackWorks/VerticalMountingSeries/VerticalItemHolder.scad"
```

`Connection_Type="Multipoint"` is the load-bearing choice — it puts a
protruding snap on the back that mates a bare Multiboard tile.
`multiConnectVersion`/`onRampEnabled` are Multiconnect-only and do not
apply here.

nixpkgs#openscad is 2021.01 but renders this generator + BOSL2
v2.0.741 cleanly (verified: Multipoint variant is a watertight body,
182 facets, with the connector protruding ~2.5 mm past the backer).

GUI alternative: install the notarized snapshot
(`brew install --cask openscad@snapshot`; if Gatekeeper still blocks,
`xattr -dr com.apple.quarantine "$(ls -d /Applications/OpenSCAD*.app | head -1)"`),
open `VerticalItemHolder.scad`, set the same values in the Customizer
(the `-D` names match the Customizer variables).

### Parameter rationale

| Param | Value | Basis |
|---|---|---|
| `internalWidth` | 22 | max(head thickness 18, bar 19.5) + clearance |
| `internalDepth` | 90 | jaw reach 85 + 5 clearance |
| `internalHeight` | 30 | head height 27 + clearance |
| `cordCutoutDiameter` | 21 | bar 19.5 + 1.5 — the slot the bar hangs through |
| `cordCutoutDepthOffset` | −33 | slot pushed to the rear so the bar hangs near the wall, cutting the tip moment |
| `frontLowerCapture` | 8 | retains the bottom front so the clamp can't swing out |
| `frontUpperCapture` | 0 | open top — drop the clamp straight in |

`-D` names are verified against the script; the exact printed fit is
unverified until the test print.

## Print recipe

Bambu A1, `0.20mm Standard @BBL A1`, filament set manually to
**SUNLU PLA+ 2.0**.

| Setting | Value |
|---|---|
| Layer height | 0.2 mm |
| Walls | 4 (bears a forward moment) |
| Infill | 25% gyroid |
| Supports | None — front-open, designed support-free |
| Brim | None (textured PEI) |

## Test gate — print ONE before the second

1. Print one cradle. Snap it onto a representative Multiboard tile.
2. Drop a clamp in head-up. Confirm the head seats fully, the bar
   hangs free through the bottom slot, and nothing fouls.
3. Bump it from below with a fist — no snap release, no >1 mm flex.
4. Confirm ~22" of clear drop below the mount point so the bar tip
   doesn't hit the cabinet.
5. All pass → print the second cradle. Any fail → adjust the
   parameter that's wrong (likely `internalWidth`/`internalDepth` if
   the 110 mm assumption bites) and re-render.

## Files

- `downloaded/SOURCES.md` — generator + BOSL2 provenance and license
- `print-log.md` — per-print diary

`downloaded/` (the cloned generator, BOSL2, and `out/*.stl`) is
gitignored — provenance only, never the bytes, same as every other
project here.
