# Pitcher spigot valve

A printable replacement for a broken push-button spigot on a glass beverage
pitcher. It is a **spring-loaded, lever-operated poppet valve**: a spring holds
a soft stopper shut on a seat; pull the lever down to lift it off and pour,
release and the spring snaps it closed. Mounts through the existing 15.8 mm
glass hole, clamped by a printed nut and TPU gaskets.

## Parts (in `3d/`)

| Script | Part | Material | Qty |
|---|---|---|---|
| `valve_body.py` | through-glass barrel + chamber + seat + spout + lever yoke (one piece) | PETG | 1 |
| `poppet.py` | stopper — sealing disc + stem + spring post | TPU 95A | 1 |
| `cap.py` | press-in chamber cap / spring abutment | TPU 95A | 1 |
| `lever.py` | pull-down lever | PLA | 1 |
| `nut.py` | winged clamp nut | PLA | 1 |
| `gasket.py` | glass seal — **print two** | TPU 95A | 2 |
| `pin.py` | lever pivot pin (or a 3 mm rod) | PLA | 1 |

**Also needed (not printed):** a light compression spring, ~Ø5–7.5 OD, ID > 3.5,
12–16 mm free length, solid length < 4 mm. Stainless if you have it — it sits in
the drink.

## How it works

Water enters the barrel and fills the chamber. A spring (reacting against the
cap) presses the TPU stopper down onto a seat ring, sealing a Ø6 throat — firmly
shut whether the pitcher is full or nearly empty; water pressure only adds to
the seal. Pull the lever down and its arm pushes the stem up, lifting the stopper
off the seat; water flows around the stem, down the spout, out. Release and the
spring shuts it.

The stem lives in the spout, which is **dry whenever the valve is shut**, so
there is no rod-through-water gap to weep. The only moving seal is the soft
stopper on the seat — compression, the same principle as the glass gaskets.

## Mount (glass wall — handle gently)

Inside the pitcher ← → outside: **nut · gasket · GLASS · gasket · flange · valve.**
Finger-tight only — the gaskets seal, clamping force does not. Never torque a nut
against glass.

## Assembly

1. Drop the **stopper** into the chamber (stem down the spout).
2. Drop the **spring** over the post on top of the stopper.
3. Press the **cap** in — it compresses the spring and holds everything shut.
4. Set the **lever** in the yoke slot, push the **pin** through.
5. Mount through the glass: flange · gasket · GLASS · gasket · nut.

## Print settings

- **Body in PETG** — it bonds between layers far better than PLA, so the walls
  actually hold water. PLA parts are SUNLU PLA+ 2.0; soft parts are SUNLU TPU 95A
  (external spool, not the AMS).
- **Body chamber-up.** The seat, cavity and spout print clean and support-free; a
  45° cone self-supports the spout shoulder. Supports land only on the external
  barrel and peel off — run the nut down the barrel a couple of times to chase
  the side-printed threads.
- ≥4 perimeters on the body so the walls hold water. Food-safe epoxy brushed down
  the wet path is cheap insurance.
- Gaskets / poppet / cap: TPU 95A, printed flat, solid infill.

Leak-test with water — shut and pouring — before trusting it on the pitcher.

## Renders

See `renders/`: `valve_mechanism.png` (shut vs. pouring), `valve_connections.png`
(how the pin, lever and stopper engage), `valve_print_pose.png` (orientation +
where supports land).
