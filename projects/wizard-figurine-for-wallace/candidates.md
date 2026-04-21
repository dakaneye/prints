# STL candidates (pre-download research)

Research pass on 2026-04-21, before Wallace has picked. Listed in
preference order for an **unpainted Oak Wood PLA print on a Bambu A1**.

## Shortlist

### 1. Chibi figurine — MakerWorld #1013579

- **URL:** https://makerworld.com/en/models/1013579-chibi-harry-potter
- **Style:** chibi (oversized head, chunky body)
- **Claim (from search excerpt):** "single piece, nothing to assemble"
- **Why this is the top pick for v1:**
  - Chunky silhouette reads clearly without paint — big shapes (robe, wand,
    glasses, scar) translate well into oak-wood grain
  - Single-piece + no-assembly = lowest first-print risk
  - Most forgiving if the A1 calibration is imperfect on the first run
- **Unverified:** couldn't fetch download count / star rating via WebFetch
  (MakerWorld returned 403). Eyeball the page before downloading:
  - Boost count / downloads
  - Community-posted "makes" photos
  - Stated print time + support requirements

### 2. Mini figurine by Wekster — Printables #341976 ⭐ most-vetted

- **URL:** https://www.printables.com/model/341976-mini-harry-potter-single-and-multimaterial
- **Style:** more realistic proportions (not chibi)
- **Verified metrics (2026-04-21):** 2,917 downloads, 638 likes, 31 reviews
- **Matches setup:** has an explicit single-material variant — purpose-built
  for no-AMS printers. Use that one.
- **Tradeoff:** realistic detail may blur in wood PLA without paint —
  small face features (scar, glasses rims) won't read as crisp edges the
  way chibi proportions would.

### 3. Mini figurine by Layered Studio — MakerWorld #1124142

- **URL:** https://makerworld.com/en/models/1124142
- **Style:** "layered" — likely designed for color-zone filament swaps
  (AMS or manual pauses), but should print fine as single-color
- **Unverified:** couldn't fetch metrics; same eyeball-the-page caveat

## Criteria that drove the filter

- Standing pose, ~100mm tall
- Single-piece or explicitly "minimal supports"
- Community-verified (≥100 downloads / ≥4-star or MakerWorld boost signal)
- Silhouette reads without paint (since v1 is unpainted)
- Wallace is 8, new-but-growing fan — iconic protagonist pose beats obscure
  side character

## Rejected / parked for later

- **Articulated Toy (Printables #370384 by Entopop):** articulated is fun for
  an 8yo but it's multi-piece + TPU joints + glue + supports — too complex
  for a first print experience. Revisit after v1 succeeds if Wallace wants
  a "play-with-it" version.
- **Dobby / Dumbledore / Hagrid chibis:** iconic but book-2+ characters;
  Wallace is in book-1 territory. Park as v3 candidates.
- **Wand display stands:** lots of these on Printables, but those are
  complementary props — not the figurine itself.

## How Wallace picks

Show him **#1 and #2** side-by-side (not all three — keeps the choice
manageable for an 8yo). Ask which "feels more like Harry to him."

## What happens after the pick

1. Download the chosen STL → `downloaded/` (gitignored)
2. Record provenance in `downloaded/SOURCES.md` (URL, author, license, date)
3. Slice in Bambu Studio with Oak Wood PLA / SUNLU PLA+ 2.0 profile
4. Save `.3mf` project file to this folder and commit it
5. Print — refer to `print-log.md` for logging outcome

This file can be deleted or kept as history after v1 is printed.
