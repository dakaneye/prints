# Print log — electronics organizer

## v1 (2026-05-09) — failed; do not reprint as-is

The v1 design (commit `7efa285`, lid fix in `84973f8`) shipped six STLs
that did not solve the stated problem. Documenting every failure mode so
the next pass (or a published-print substitute) starts from a real
baseline.

| Failure | Root cause |
|---|---|
| **Lid**: recessed labels printed with strands hanging in the letter recesses, illegible | Recessed text bridges poorly in PLA when the engraved face prints down. Fix codified in `conventions.md` (raised labels only). Lid STL was regenerated with raised text post-print. |
| **Capacitor well**: subcase doesn't fit | Well sized to 130×85×22 mm "quick" estimate + 3 mm clearance. Actual subcase is bigger; no caliper measurement taken at design time. |
| **Header-pin well**: subcase doesn't fit | Same root cause as capacitor well — sized to estimate, not measurement. |
| **LED reel pocket**: reel doesn't fit | Sized to 75 mm ø estimate + 4 mm clearance. Actual reel is bigger. Same root cause: no caliper measurement. |
| **Bins**: don't hold the multipack quantities advertised in README | 1×1 internal volume (~57 cm³) was sized for loose components, not for components in their original anti-static packaging / strip holders / bags. The 10-pack of USB-C breakouts and the 20-pack of tact switches don't fit with their packaging. |
| **Lid friction-fit**: not right | `LID_CLEARANCE` (0.30 mm/side) was a guess. Either too tight or too loose on this filament/printer combo. Not characterized against a test piece before the full lid print. |

**Root cause across all failures**: designed against estimated dimensions
("quick" measurements + assumed clearances), not against caliper
measurements of the actual items being stored. No fit-test print before
committing to a 12-hour tote print. This is an avoidable category of
failure; the rule going forward (per `conventions.md` print-readiness
section) is: real measurements, fit-test print for any uncertain dim,
before any large print.

**Status**: keeping the v1 STLs printed (tote + bins) as-is for the bins
to be useful (they accept correctly-sized loose components even if the
multipack packaging won't fit). Lid v1 print is scrap; reprint from the
raised-label STL when ready.

**v2 strategy (not started)**: pivot to community designs. The
gridfinity-build123d bins remain valid (well-tested upstream). The tote
+ lid combination is the part where a published design (e.g., the
Gridfinity-compatible cases found during search-first research) is more
likely to work first-try than another custom pass.

## Future print entries

| Date | Part | Filament | Params changed | Outcome |
|---|---|---|---|---|
| | | | | |
