# Design: `misc-3d-printing-projects` + Wizard Figurine for Wallace (v1)

**Date:** 2026-04-21
**Author:** Sam (with Claude)
**Status:** Approved for implementation planning

## Purpose

Two nested goals:

1. **Establish `misc-3d-printing-projects`** — a public GitHub repo that holds small, one-off 3D printing projects. Hybrid model: each project folder can mix downloaded third-party STLs (for organic shapes like figurines) with parametric `build123d` scripts (for custom / personalized parts).

2. **First project: a wizard-themed figurine for Sam's nephew Wallace (age 8)** — a downloaded figurine paired with a custom build123d display base engraved with his name. First real print on Sam's newly-arrived Bambu Lab A1. The project is deliberately framed as a teaching moment — both for Wallace (how 3D printing works, how downloaded vs. coded parts coexist) and for Sam (first-time A1 workflow validation).

## Context

**Sam's hardware** (verified 2026-04-21 via OB1 capture):
- Bambu Lab A1, 256×256mm bed, no AMS (single-color per print unless manual filament swap)
- Filament on hand: SUNLU PLA+ 2.0 in Black, White, Grey, Oak Wood
- Slicer: Bambu Studio (macOS, Homebrew install)
- CAD: `build123d >= 0.10.0` + `ocp-vscode` for live preview

**Existing pattern** (in `~/dev/personal/word-clock-for-my-daughters/enclosure/3d/`):
- Per-directory `.venv/` (gitignored), `requirements.txt`, `*.py` generators, `out/*.stl` (gitignored), `build_all.py`, per-folder `README.md`
- Script convention: docstring → parameters (mm, cited in comments) → primitives + booleans + transforms → `export_stl()`
- Alignment convention: `(Align.CENTER, Align.CENTER, Align.MIN)` = bottom at Z=0, centered in XY

This spec **extends that convention one level up**: each project is a self-contained folder, each project's `3d/` subdirectory follows the word-clock pattern unchanged.

**Nephew context:** Wallace is 8, learning to read, new but enthusiastic fan of Harry Potter (likely book-1 level). Project-for Wallace is chosen over design-by-Wallace — Sam picks the scope, Wallace is the audience and occasional collaborator (e.g., picks the STL from a shortlist, watches print, regenerates the engraved base).

## Scope (v1)

### Repository: `~/dev/personal/misc-3d-printing-projects/`

Public GitHub repo. Top-level layout:

```
misc-3d-printing-projects/
├── README.md                   # What this repo is, index of projects, printer basics
├── CONTRIBUTING.md             # "Personal hobby repo. PRs not expected. Fork freely."
├── LICENSE                     # MIT
├── CODEOWNERS                  # * @dakaneye
├── conventions.md              # Project folder layout, filament catalog, naming rules
├── .gitignore                  # .venv/, out/*.stl, *.3mf, __pycache__, .DS_Store,
│                               # AND projects/*/downloaded/ (never commit third-party STLs)
├── .github/
│   ├── dependabot.yml          # pip + github-actions (covers both ecosystems)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       ├── ci.yml              # ruff check + ruff format --check (lint only)
│       └── codeql.yml          # Python CodeQL on push/PR + weekly
├── docs/
│   ├── 3d-printing-setup.md    # Shared A1 workflow, Bambu Studio, slicer defaults
│   └── superpowers/specs/      # Design docs (this file lives here)
├── shared/
│   └── 3d/                     # OPTIONAL shared build123d helpers
│       ├── requirements.txt
│       ├── build123d_helpers.py  # e.g., engrave_text(), chamfered_plaque()
│       └── README.md
└── projects/
    └── wizard-figurine-for-wallace/
        ├── README.md           # Public-facing description (IP-neutral)
        ├── downloaded/         # GITIGNORED. Third-party STLs live here locally only.
        │   └── SOURCES.md      # URL + author + license + download date per STL
        ├── 3d/
        │   ├── requirements.txt       # build123d>=0.10.0
        │   ├── base.py                # Parametric engraved display base
        │   ├── build_all.py           # Regenerates every *.py sibling
        │   └── out/                   # GITIGNORED
        └── print-log.md        # Per-print diary: success/fail/lessons
```

### Public-facing IP posture

Warner Bros owns the Harry Potter IP. Personal-use fan-prints from community-uploaded STLs are broadly tolerated in the 3D printing community but **not legally affirmative**. Mitigation strategy for this public repo:

- **Public-facing strings are generic.** Folder name `wizard-figurine-for-wallace/`. Public README calls it "a wizard-themed figurine." No "Harry Potter" in README, commit messages, or issue titles.
- **Internal design docs (this file, `print-log.md` entries, conversation history) can name the character freely** — specs are design history, not a public website.
- **Downloaded STLs never get committed.** `projects/*/downloaded/` is globally gitignored. `SOURCES.md` links out to the hosting site (MakerWorld / Printables / Thingiverse) without mirroring the bytes. This also respects those sites' license terms, which typically prohibit re-hosting.
- All original work (build123d scripts, docs, engraved base) is MIT-licensed.

### First project: Wizard figurine + engraved oak base

**Downloaded part:**
- A standing-pose wizard-boy figurine, ~100mm tall, single-piece, "no supports needed" or "minimal supports only" tagged
- Source: MakerWorld (Bambu-optimized community) or Printables. Selection criteria: ≥100 downloads, ≥4-star average, recent reviews confirming A1 success
- Stored locally in `projects/wizard-figurine-for-wallace/downloaded/` (gitignored)
- Provenance recorded in `downloaded/SOURCES.md`
- Filament: **Oak Wood PLA** (SUNLU PLA+ 2.0). Wood grain reads as a hand-carved toy rather than a blank print — the best unpainted aesthetic available from current stock.

**Parametric part (`projects/wizard-figurine-for-wallace/3d/base.py`):**
- Rectangular display plaque, approximately 90mm × 60mm × 10mm (final dims adjusted to the actual figurine footprint after the first figurine print)
- Top surface engraved "WALLACE" (front, raised or recessed letters)
- Second line below the name: print month and year, "APR 2026"
- Recessed footprint on the top surface matching the figurine's feet — so the figurine locates into the base without glue (v1)
- Chamfered edges for a finished feel
- Filament: **Oak Wood PLA** (same as figurine, for a unified look)
- Script follows the word-clock 3d/ convention: docstring → parameters (mm, sourced in comments) → primitives + booleans + transforms → `export_stl()`

**Assembly:**
- v1: no glue. Figurine sits in the base's footprint recess. Removable so Wallace can play with it.
- Fallback if the recess is too loose: a single dot of PLA-safe super glue, or a hidden M3 brass-insert + screw under the base.

### Teaching beats (to be captured in the project README)

Four deliberate "show Wallace" moments this project sets up. These belong in the project's README as "How to run this with Wallace" so future-Sam doesn't lose them:

1. **"The internet has amazing builders"** — browse MakerWorld together, point out the STL author's name and credits, download and open in Bambu Studio to see the model rotate.
2. **"But we can make our own too"** — open `base.py`, change the engraved text live (demo: "WALLACE" → "HARRY" → regen → back to "WALLACE"), show how the same file produces different STLs.
3. **"Watch the robot build it"** — start the figurine print together, watch the first 15 minutes, explain layer height, start Bambu Studio's time-lapse capture.
4. **"The reveal"** — pop figurine off the build plate, snap into the engraved base, hand to Wallace.

## Success criteria

1. Repo exists on GitHub as a public repository
2. `public-repo-setup` completion gate passes: no secrets in history, zero high/critical Dependabot or CodeQL alerts, all Actions pinned to SHAs, LICENSE + CONTRIBUTING + Dependabot + CI + CodeQL + CODEOWNERS + branch protection all in place
3. MIT license compatibility verified for `build123d` (Apache-2.0) and all transitive dependencies (manual one-time check, no ongoing license scanner)
4. Figurine prints cleanly on the A1 without catastrophic failure
5. `base.py` produces a plaque STL that prints cleanly, and the figurine's feet locate into its recess
6. "WALLACE" and "APR 2026" are legible from arm's length
7. Wallace recognizes the figurine without being told who it is
8. Sam makes at least one meaningful build123d change (e.g., regenerates with different engraved text) while Wallace is watching — the "we coded this" teaching beat lands in real life

## Unverified assumptions (flag in implementation, verify on first print)

- **[MED]** Oak Wood PLA optimal temperature / flow rate on the A1. SUNLU PLA+ 2.0 profile exists in Bambu Studio but wood-filled flow behavior isn't yet verified. Mitigation: run auto-calibration + a small wood-PLA calibration cube (~20mm, ~20 min) before the figurine print.
- **[MED]** Bed adhesion on a brand-new A1 textured PEI plate. No prior baseline. Mitigation: follow Bambu's first-print onboarding exactly, use glue stick if the calibration cube lifts.
- **[LOW]** Wood-filament nozzle wear on the A1's stock hardened steel nozzle. A1 ships with a hardened steel nozzle so wood PLA should be fine indefinitely, but worth logging wear observations in `print-log.md`.
- **[LOW]** The specific STL we'll download. Not yet chosen. Selection will happen during implementation, filtered through the criteria in the "Downloaded part" section above.

## Out of scope (v1)

**Deferred to v2 or later:**
- Painting. Buy a starter kit (Army Painter Speedpaint or Citadel Contrast, ~$25) and do a separate painting afternoon with Wallace.
- Alternate poses: wizard-on-broomstick, companion-figure trio (bushy-haired friend + red-haired friend). Unlock after v1 succeeds.
- AMS Lite accessory purchase (~$250). Skip unless a future project has a structural multi-color use case.
- Additional projects in `projects/ideas.md`: Hogwarts-letter display plaque, wand stand, house-crest wall mount.

**Not doing in this repo, ever:**
- Selling prints. Personal and gift use only.
- Print-farm logistics, spool inventory, business automation. This is a hobby repo.
- Printer firmware or network automation. Bambu's first-party software already covers this.

**Deliberately light, not missing:**
- No unit tests for `build123d` scripts. "Does `python base.py` produce a valid STL that looks right in the viewer?" is the test. A formal unit test for an engraved plaque is over-engineering.
- No per-project slicer-settings automation. Save the final `.3mf` project file in the project folder and commit it. No need to script Bambu Studio.

## Risks

1. **First print fails.** Mitigation: run printer calibration + a small wood-PLA calibration cube before the figurine. Log any failures in `print-log.md` for future reference.
2. **Downloaded STL is low-quality.** Mitigation: pick by download count + recent reviews + "no supports needed" tag, not just screenshots. Preview in Bambu Studio before committing to the print.
3. **Base recess dimensions wrong.** Mitigation: first iteration of `base.py` uses placeholder footprint dimensions; after the figurine prints, measure its feet and regenerate. Expect 1-2 iterations.
4. **IP exposure.** Mitigated above: public-facing strings generic, downloaded STLs gitignored.
5. **Sam ships v1 unpainted and Wallace is underwhelmed.** Mitigation: set expectations explicitly before the reveal ("this is the wooden version — we're going to paint it together next time").

## Ecosystem-specific notes

- Python-only repo. No JS/Go/containers.
- `build123d` is Apache-2.0, MIT-compatible. No other direct runtime deps expected beyond build123d's own transitive set (OpenCascade via ocp-vscode, which is Apache-2.0 / LGPL-2.1 at worst — LGPL is compatible for dynamic linking, which this is).
- CI: `ruff check` + `ruff format --check` only. No STL smoke-test — installing `build123d` in CI pulls in heavy native deps (OpenCascade) for marginal value on a hobby repo. Sam runs scripts locally before committing; CI's job is catching syntax and formatting issues.
- CodeQL: Python analysis, push + PR + weekly cron.
- Dependabot: `pip` ecosystem (pointed at each project's `requirements.txt` and `shared/3d/requirements.txt`) + `github-actions` ecosystem.

## Related work

- `~/dev/personal/word-clock-for-my-daughters/enclosure/3d/` — the canonical build123d-per-project pattern this spec extends
- `~/dev/personal/word-clock-for-my-daughters/docs/hardware/3d-printing-setup.md` (referenced from within that project) — Bambu Studio + A1 onboarding notes, should be linked from `misc-3d-printing-projects/docs/3d-printing-setup.md`
