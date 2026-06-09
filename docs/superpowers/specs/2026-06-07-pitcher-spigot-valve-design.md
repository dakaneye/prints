# Pitcher spigot valve — design

A printable replacement for a broken push-button spigot on a glass beverage
pitcher. The replacement is a **spring-loaded, lever-operated poppet valve** —
the same family as the original push tap: a spring holds a soft stopper shut on
a seat, and a lever lifts it to pour.

> This supersedes two earlier concepts recorded against this project: a
> quarter-turn plug valve and a flexing TPU diaphragm. Both were abandoned —
> the plug valve could not seal a printed taper reliably, and the diaphragm
> depended on flex behaviour that could not be predicted or printed. The lesson:
> every seal must be a *compressed soft face*, and shut-off needs a *positive
> closing force* (a spring), not gravity.

## Problem

The green plastic spigot body on a glass pitcher has failed. The original is a
through-wall tap: a threaded barrel passes through a hole in the pitcher wall, a
gasket and a nut clamp it, and a spring-loaded push-button dispenses out a
downward spout. Only the body needs replacing; the glass and hole are reused.

## Constraints

- **Wall is glass.** The clamp cannot be torqued — glass cracks under point load.
  Sealing comes from gasket compression, finger-tight only.
- **Fixed hole.** The glass hole is 15.8 mm; the barrel must pass through it.
- **Watertight body.** FDM layer lines weep under standing water. The body is
  printed in **PETG** (bonds between layers) with thick walls; PLA was the wrong
  material and leaked through the walls.
- **Every seal is a compressed soft face**, never a printed wall holding water
  across a layer seam, and never a flexing or tight-tolerance printed seal.

## Mechanism

Spring-loaded poppet, lever-actuated:

- Water enters the barrel into a vertical **chamber**. A solid **seat floor** at
  the chamber bottom has only a Ø6 **throat** to the downward **spout**.
- A soft TPU **stopper** (disc + stem) rests on the seat. A **compression spring**
  between the stopper and the press-in **cap** pushes it down — positively shut
  at any water level; water pressure adds to the seal.
- The **stem** runs down through the throat and out the spout to a **lever** that
  pivots in a yoke on the body. Pull the lever down → the arm pushes the stem up
  → the stopper lifts off the seat → flow around the stem, down the spout.
  Release → the spring shuts it.
- The stem lives in the spout, **dry whenever the valve is shut**, so there is no
  rod-through-water gland to leak. The only moving seal is the stopper on the
  seat.

## Sealing

Three compression seals, all forgiving soft faces:

1. **Glass mount.** Two TPU gaskets, one each side of the glass
   (flange · gasket · GLASS · gasket · nut), clamped finger-tight by the winged
   nut. Proven to seal.
2. **Valve seat.** The spring-pressed TPU stopper on the printed seat ring.
3. **Cap.** The TPU cap's flange squeezes the chamber rim; its plug grips by
   interference. A static seal — no stem passes through it.

## Parts

One part per `snake_case.py` script (three-section convention, `out/` output):

| Script | Part | Material |
|---|---|---|
| `valve_body.py` | barrel + flange + chamber + seat + spout + lever yoke (one piece) | PETG |
| `poppet.py` | stopper: disc + stem + spring post | TPU 95A |
| `cap.py` | press-in cap / spring abutment | TPU 95A |
| `lever.py` | pull-down lever (back wall traps the foot) | PLA |
| `nut.py` | winged clamp nut | PLA |
| `gasket.py` | glass seal (print two) | TPU 95A |
| `pin.py` | lever pivot pin (headed) | PLA |

Plus a sourced light compression spring (~Ø5–7.5 OD, 12–16 mm free, stainless).

## Key parameters (mm)

| Parameter | Value | Reason |
|---|---|---|
| Glass hole Ø | 15.8 | measured |
| Barrel OD (thread crest) | ~14.9 | passes the 15.8 hole |
| Feed bore | Ø8 | flow into the chamber |
| Chamber ID / wall | Ø12 / 3 | holds the stopper; PETG wall |
| Seat throat | Ø6 | the stopper (Ø9) seals over it |
| Spring post | Ø3 | centres the spring |
| Lever lift at full pull | ~4.6 mm | opens the throat |

## Construction notes

- The helix-swept thread, fused as a unit, makes OCC booleans fail silently. The
  body is built from **plain cylinders first** (which fuse reliably), with the
  thread ridge added last as a swept sliver — otherwise the body falls into loose
  pieces. Keep that order.
- Body prints **chamber-up**: the seat, cavity and spout are clean and
  support-free (a 45° cone self-supports the spout shoulder); supports land only
  on the external barrel. The side-printed barrel threads come out rough — chased
  clean by running the nut down.

## Verification

- **Smoke tests:** each generator emits a valid, non-trivial STL; the rigid parts
  are single watertight solids.
- **Assembly checks (build123d `&`):** the seat floor stops the stopper falling;
  it lifts free to pour; the lever lifts ~4.6 mm with zero body collision through
  the full swing; the spring post clears the cap at full open.
- **Physical:** body watertight chamber-up; spring shuts firmly full and
  near-empty; leak-test shut and pouring before trusting it on the pitcher.

## Out of scope

- Matching the original colour.
- A commercial replacement (the goal is an in-house printed part).
