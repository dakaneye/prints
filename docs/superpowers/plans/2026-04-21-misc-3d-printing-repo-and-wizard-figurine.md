# `misc-3d-printing-projects` Repo + Wizard Figurine (Wallace) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a public GitHub repo for Sam's miscellaneous 3D printing projects and scaffold the first project — an unpainted wizard-themed figurine with a custom engraved oak display base for his 8-year-old nephew Wallace.

**Architecture:** Hybrid repo — each project folder pairs downloaded third-party STLs (gitignored, never committed) with parametric `build123d` scripts (original work). The repo lives under `dakaneye/` and is automatically picked up by the `~/dev/personal/.github` sync engine, which provides all community health files, CI callers (via `dakaneye/hookshot`), CodeQL, vuln scanning, Dependabot, and branch protection. This plan only scaffolds repo-specific code + docs.

**Tech Stack:** Python 3.11+, `build123d >= 0.10.0`, `ruff` for linting (run in CI by hookshot's `python-ci.yml`), Bambu Studio slicer, Bambu Lab A1 printer, SUNLU PLA+ 2.0 filament.

**Reference spec:** `docs/superpowers/specs/2026-04-21-harry-figurine-for-wallace-design.md`

**Reference infra (already in place, NOT modified by this plan):**
- `~/dev/personal/.github` — sync engine (targets `dakaneye/*` public repos)
- `~/dev/personal/hookshot` — reusable workflows (`python-ci.yml`, `codeql.yml`, etc.)
- `~/dev/personal/release-pilot` — release orchestration (not used here, no package published)

---

## What sync provides automatically (we do NOT hand-write these)

After the repo is pushed public, `~/dev/personal/.github`'s `sync-settings.yml` workflow will open a PR adding:

- **Enforced** (overwritten every sync): `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/*`
- **Dynamic** (regenerated per-repo from ecosystem detection): `.github/workflows/ci.yml` (calls `dakaneye/hookshot/.github/workflows/python-ci.yml@<sha>`), `.github/dependabot.yml`
- **Seed-only** (created once, repo can customize later): `.github/workflows/codeql.yml`, `.github/workflows/scan.yml`, `.github/workflows/dependabot-auto-merge.yml`
- **Branch protection** (applied via API): `repo-sync-baseline` ruleset — linear history, required signatures, 1 approving review, status checks auto-detected from ci.yml
- **Repo settings** (applied via API): merge methods (squash + rebase), delete-branch-on-merge, vulnerability alerts, has_issues

Sync detects this repo as **Python** via `pyproject.toml` (Task 2). The sync engine picks up public `dakaneye/*` repos automatically — no `settings.yml` change is needed.

---

## Phases

1. **Repo-specific scaffolding** (tasks 1–5) — `.gitignore`, `pyproject.toml`, `README.md`, `conventions.md`, `docs/3d-printing-setup.md`
2. **First project scaffold** (tasks 6–9) — project README + print-log, `downloaded/SOURCES.md`, `3d/` with base.py + build_all.py
3. **Local verification** (tasks 10–11) — ruff passes, fresh-venv smoke test
4. **Publish + sync** (tasks 12–15) — create public repo, push, trigger sync, merge sync PR
5. **Physical execution checklist** (tasks 16–22) — Sam-driven: calibrate, pick STL with Wallace, print, measure, print base, assemble, deliver

---

## Phase 1: Repo-specific scaffolding

### Task 1: Create `.gitignore`

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Create `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.Python
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# build123d / 3D output
out/
*.stl
*.3mf.backup

# Third-party downloaded models — NEVER commit STL/3MF bytes (IP + license compliance)
projects/*/downloaded/*
# ...except the provenance placeholder + SOURCES index
!projects/*/downloaded/.gitkeep
!projects/*/downloaded/SOURCES.md

# macOS
.DS_Store

# IDE
.idea/
.vscode/
*.swp
*.swo

# Secrets
.env
.env.local
*.key
*.pem
```

- [ ] **Step 2: Verify the `downloaded/` ignore rule works as intended**

Run from the repo root:
```bash
mkdir -p projects/_test/downloaded
touch projects/_test/downloaded/fake.stl projects/_test/downloaded/SOURCES.md
git status --porcelain projects/_test/downloaded/
```
Expected: `SOURCES.md` appears as untracked; `fake.stl` does not.

Cleanup: `rm -rf projects/_test`

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add gitignore"
```

---

### Task 2: Create `pyproject.toml` (ecosystem marker + ruff config)

**Files:**
- Create: `pyproject.toml`

This file serves double duty: it's the ecosystem marker that tells the sync engine to generate a Python CI caller (`python-ci.yml`), and it holds the `ruff` config that hookshot's CI will use to lint.

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "misc-3d-printing-projects"
version = "0.0.0"
description = "Miscellaneous 3D printing projects — Bambu Lab A1 + build123d"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
target-version = "py311"
# Exclude gitignored build artifacts + venvs; ruff won't see them anyway but
# being explicit helps if someone runs it against a dirty tree.
extend-exclude = [".venv", "out", "projects/*/downloaded"]

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
# build123d is used as `from build123d import *` in scripts — the star-import
# warnings (F403, F405) are noise for that pattern.
ignore = ["F403", "F405"]

[tool.ruff.format]
quote-style = "double"
```

- [ ] **Step 2: Verify ruff accepts the config**

If ruff isn't installed locally:
```bash
pip install --user ruff  # or: pipx install ruff / brew install ruff
```

Run:
```bash
ruff check .
ruff format --check .
```

Expected: both exit 0 (no Python files yet).

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add pyproject with ruff config"
```

---

### Task 3: Create top-level `README.md`

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

```markdown
# misc-3d-printing-projects

Small, one-off 3D printing projects for my Bambu Lab A1.

Each project is self-contained under `projects/<name>/`. Some are pure
downloads from the community (MakerWorld, Printables, Thingiverse); some are
pure `build123d` parametric scripts I've written; most are hybrids — a
downloaded model paired with a custom accent part I coded.

## Repository layout

```
misc-3d-printing-projects/
├── docs/
│   ├── 3d-printing-setup.md    # Bambu A1 + Bambu Studio workflow
│   └── superpowers/            # Design docs + implementation plans
├── projects/
│   └── <project-name>/
│       ├── README.md           # What this project is
│       ├── downloaded/         # Third-party STLs (LOCAL ONLY — gitignored)
│       │   └── SOURCES.md      # URL + author + license + date, per STL
│       ├── 3d/                 # build123d scripts for parametric parts
│       └── print-log.md        # Per-print diary
├── conventions.md              # Folder layout + filament catalog + naming
└── pyproject.toml              # Ruff config (CI uses this)
```

## Projects

| Project | Status | Description |
|---|---|---|
| `wizard-figurine-for-wallace` | in progress | Wizard-themed figurine with a personalized engraved oak display base |

## Printer + filament

See `docs/3d-printing-setup.md`.

## License

MIT — applies to my original code and docs. Downloaded STLs retain their
original licenses per each project's `downloaded/SOURCES.md`.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add top-level readme"
```

---

### Task 4: Create `conventions.md`

**Files:**
- Create: `conventions.md`

- [ ] **Step 1: Create `conventions.md`**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add conventions.md
git commit -m "docs: add conventions"
```

---

### Task 5: Create `docs/3d-printing-setup.md`

**Files:**
- Create: `docs/3d-printing-setup.md`

- [ ] **Step 1: Create `docs/3d-printing-setup.md`**

```markdown
# 3D printing setup — Bambu Lab A1

## Hardware

- Printer: Bambu Lab A1 (no AMS), 256×256mm bed
- Nozzle: stock 0.4mm hardened steel (wood-filled PLA safe)
- Build plate: textured PEI

## Slicer

**Bambu Studio** installed at `/Applications/BambuStudio.app` (macOS,
Homebrew install).

Import STLs via `File → Import → Import 3MF/STL`, or drag-drop into the
plater. `File → Open Project` only accepts `.3mf` slicer project bundles,
not raw STL.

## Filament profiles

Filament catalog: see `../conventions.md`.

SUNLU PLA+ 2.0 has no RFID — manually select **"SUNLU PLA+ 2.0"** profile
in Bambu Studio.

## Authoring workflow (build123d)

Each project's `3d/` directory is self-contained:

```bash
cd projects/<project>/3d
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -r requirements.txt
```

(`.venv/` is gitignored — it's ~500 MB of cached OpenCascade CAD geometry,
rebuild locally on demand.)

Regenerate one STL:
```bash
projects/<project>/3d/.venv/bin/python projects/<project>/3d/<script>.py
```

Regenerate every STL in a project:
```bash
projects/<project>/3d/.venv/bin/python projects/<project>/3d/build_all.py
```

## VS Code integration

Install the **OCP CAD Viewer** extension + `pip install ocp-vscode` in the
project's `.venv`. Gives live 3D preview of build123d parts without
re-exporting STL each time.

## CI

Lint runs in CI via `dakaneye/hookshot`'s `python-ci.yml` reusable workflow.
The caller in `.github/workflows/ci.yml` is generated automatically by the
`~/dev/personal/.github` sync engine. There are no unit tests for
`build123d` scripts — the check is "does `python base.py` produce a valid
STL in the viewer?", done locally.
```

- [ ] **Step 2: Commit**

```bash
git add docs/3d-printing-setup.md
git commit -m "docs: add 3d printing setup guide"
```

---

## Phase 2: First project scaffold

### Task 6: Create project folder with README + print-log

**Files:**
- Create: `projects/wizard-figurine-for-wallace/README.md`
- Create: `projects/wizard-figurine-for-wallace/print-log.md`

- [ ] **Step 1: Create the project folder**

```bash
mkdir -p ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
```

- [ ] **Step 2: Create `projects/wizard-figurine-for-wallace/README.md`** (IP-neutral, with teaching beats)

```markdown
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
```

- [ ] **Step 3: Create `projects/wizard-figurine-for-wallace/print-log.md`**

```markdown
# Print log — wizard figurine for Wallace

One entry per print attempt. Include: date, what was printed, filament,
slicer settings, duration, outcome, lessons.

---

<!-- Template:

## YYYY-MM-DD — <part name>

- **Filament:** <brand + color>
- **Slicer profile:** <name>
- **Print time:** <hh:mm>
- **Outcome:** success / partial / failure
- **Photos:** (optional, paths to local copies)
- **Lessons:** <what to do differently next time>

-->
```

- [ ] **Step 4: Commit**

```bash
git add projects/wizard-figurine-for-wallace/README.md projects/wizard-figurine-for-wallace/print-log.md
git commit -m "feat: scaffold wizard figurine project"
```

---

### Task 7: Create `downloaded/SOURCES.md` + `.gitkeep`

**Files:**
- Create: `projects/wizard-figurine-for-wallace/downloaded/.gitkeep`
- Create: `projects/wizard-figurine-for-wallace/downloaded/SOURCES.md`

The `.gitignore` from Task 1 already has the carve-out for `.gitkeep` and `SOURCES.md` inside `downloaded/`.

- [ ] **Step 1: Create the placeholder + SOURCES template**

```bash
touch projects/wizard-figurine-for-wallace/downloaded/.gitkeep
```

Then write `projects/wizard-figurine-for-wallace/downloaded/SOURCES.md`:

```markdown
# Downloaded STL sources

One entry per downloaded file. Fill in when a file is added to this folder.

**STL/3MF/step files themselves are gitignored** — only this SOURCES.md
gets committed. Do not re-host third-party models.

---

<!-- Template:

## `<filename>.stl`

- **URL:** <https link to MakerWorld / Printables / Thingiverse page>
- **Author:** <author's display name>
- **License:** <e.g., CC-BY-SA-4.0, MIT, Standard Digital File License>
- **Downloaded:** YYYY-MM-DD
- **Notes:** <scale adjustments, orientation, support settings, etc.>

-->
```

- [ ] **Step 2: Verify the ignore rules still work**

```bash
touch projects/wizard-figurine-for-wallace/downloaded/fake.stl
git status --porcelain projects/wizard-figurine-for-wallace/downloaded/
```
Expected: `.gitkeep` and `SOURCES.md` show as untracked; `fake.stl` is absent from the list.

Cleanup: `rm projects/wizard-figurine-for-wallace/downloaded/fake.stl`

- [ ] **Step 3: Commit**

```bash
git add projects/wizard-figurine-for-wallace/downloaded/.gitkeep projects/wizard-figurine-for-wallace/downloaded/SOURCES.md
git commit -m "feat: add sources template for downloaded stls"
```

---

### Task 8: Create `3d/requirements.txt`

**Files:**
- Create: `projects/wizard-figurine-for-wallace/3d/requirements.txt`

- [ ] **Step 1: Create `requirements.txt`**

```
build123d>=0.10.0
```

- [ ] **Step 2: Commit**

```bash
git add projects/wizard-figurine-for-wallace/3d/requirements.txt
git commit -m "feat: add build123d requirements"
```

---

### Task 9: Write `3d/base.py` + `3d/build_all.py`

**Files:**
- Create: `projects/wizard-figurine-for-wallace/3d/base.py`
- Create: `projects/wizard-figurine-for-wallace/3d/build_all.py`

- [ ] **Step 1: Set up the `.venv` and install build123d**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

Takes ~2-3 minutes on first run (OpenCascade native deps).

- [ ] **Step 2: Write `base.py`**

```python
"""Display base for the wizard figurine.

A rectangular oak plaque with the recipient's name + print date engraved on
the top surface and a shallow recess that locates the figurine's feet.

FIGURINE_FOOT_WIDTH / FIGURINE_FOOT_DEPTH below are placeholders — after
printing the figurine, measure its feet with calipers and update these.
See Task 20 of the implementation plan.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Pos,
    Text,
    export_stl,
    extrude,
)

# ─── Parameters (mm) ──
# Plaque outer dimensions. Sized for a ~100mm figurine.
BASE_WIDTH = 90.0
BASE_DEPTH = 60.0
BASE_HEIGHT = 10.0

# Recipient name + date (engraved on top surface, front half)
RECIPIENT_NAME = "WALLACE"
PRINT_DATE = "APR 2026"

# Engraving depth — readable at arm's length, shallow enough not to weaken
# the plaque's top layer.
ENGRAVE_DEPTH = 1.2

NAME_FONT_SIZE = 10.0
DATE_FONT_SIZE = 5.0

# Recessed footprint for figurine's feet — PLACEHOLDER values.
# After the figurine prints, measure its base and update these
# (+ ~0.4mm print tolerance per dimension).
FIGURINE_FOOT_WIDTH = 30.0
FIGURINE_FOOT_DEPTH = 20.0
FOOT_RECESS_DEPTH = 2.0

# ─── Geometry ──
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)

# Main plaque
plaque = Box(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT, align=BOTTOM)

# Name engraving — front half of the plaque (negative Y)
name_text = Text(RECIPIENT_NAME, font_size=NAME_FONT_SIZE)
name_3d = extrude(name_text, amount=ENGRAVE_DEPTH)
name_3d = Pos(0, -BASE_DEPTH * 0.25, BASE_HEIGHT - ENGRAVE_DEPTH) * name_3d

# Date engraving — below the name
date_text = Text(PRINT_DATE, font_size=DATE_FONT_SIZE)
date_3d = extrude(date_text, amount=ENGRAVE_DEPTH)
date_3d = Pos(0, -BASE_DEPTH * 0.40, BASE_HEIGHT - ENGRAVE_DEPTH) * date_3d

plaque = plaque - name_3d - date_3d

# Figurine foot recess — back half of the plaque (positive Y)
foot_recess = Box(
    FIGURINE_FOOT_WIDTH,
    FIGURINE_FOOT_DEPTH,
    FOOT_RECESS_DEPTH,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
foot_recess = Pos(0, BASE_DEPTH * 0.15, BASE_HEIGHT - FOOT_RECESS_DEPTH) * foot_recess
plaque = plaque - foot_recess

# ─── Export ──
out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)
export_stl(plaque, str(out_dir / "base.stl"))

print(f"Wrote {out_dir / 'base.stl'}")
```

**Note on the build123d API:** if `base.py` fails on first run with an import
or signature error, consult https://build123d.readthedocs.io/ — `Text` may
need a `font=` argument on some systems, and `extrude` may require a
sketch/plane context depending on version. Expect 0–2 iterations first run.

- [ ] **Step 3: Run `base.py`**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
.venv/bin/python base.py
```

Expected:
- Prints `Wrote .../out/base.stl`
- `out/base.stl` exists, > 1 KB

- [ ] **Step 4: Write `build_all.py`**

```python
"""Regenerate every STL in this directory.

Runs every sibling *.py (excluding build_all.py itself). Output goes to
each script's local out/ directory.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ME = Path(__file__).name


def main() -> int:
    scripts = sorted(p for p in HERE.glob("*.py") if p.name != ME)
    if not scripts:
        print("No part scripts found.")
        return 0

    failures: list[str] = []
    for script in scripts:
        print(f"\n=== {script.name} ===")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=HERE,
        )
        if result.returncode != 0:
            failures.append(script.name)

    if failures:
        print(f"\nFAILED: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(scripts)} script(s) regenerated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run `build_all.py`**

```bash
.venv/bin/python build_all.py
```

Expected:
- Prints `=== base.py ===`
- Prints `Wrote .../out/base.stl`
- Prints `All 1 script(s) regenerated successfully.`
- Exit 0

- [ ] **Step 6: Commit**

```bash
git add projects/wizard-figurine-for-wallace/3d/base.py projects/wizard-figurine-for-wallace/3d/build_all.py
git commit -m "feat: parametric engraved base + build_all"
```

---

## Phase 3: Local verification

### Task 10: Run ruff locally (mirrors what hookshot CI will do)

**Files:** none

- [ ] **Step 1: Run ruff check**

```bash
cd ~/dev/personal/misc-3d-printing-projects
ruff check .
```
Expected: exit 0. If it complains, fix and add a `style: ruff cleanup` commit.

- [ ] **Step 2: Run ruff format check**

```bash
ruff format --check .
```
Expected: exit 0. If it complains, run `ruff format .`, inspect, and commit
as `style: ruff format`.

- [ ] **Step 3: Confirm clean tree**

```bash
git status
```
Expected: "nothing to commit, working tree clean"

---

### Task 11: Fresh-venv smoke test

**Files:** none — validates that the setup steps in `docs/3d-printing-setup.md` actually work.

- [ ] **Step 1: Nuke the venv + out dir**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
rm -rf .venv out
```

- [ ] **Step 2: Rebuild per the documented steps**

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_all.py
```

Expected: build123d installs cleanly, base.py runs, STL written, exit 0.

- [ ] **Step 3: Confirm `out/` is still gitignored**

```bash
git status
```
Expected: clean — `out/` and `.venv/` both gitignored.

---

## Phase 4: Publish + sync

### Task 12: Create public GitHub repo + push

**Files:** none

- [ ] **Step 1: Run `gitleaks` one last time on the full history**

```bash
cd ~/dev/personal/misc-3d-printing-projects
gitleaks detect --source . --verbose
```
Expected: `no leaks found`. If any leak is flagged, **stop** — do not push.
Rewrite history to remove the leak and rotate the secret.

- [ ] **Step 2: Create the repo under `dakaneye/` and push**

```bash
gh repo create misc-3d-printing-projects \
  --public \
  --source=. \
  --remote=origin \
  --description "Miscellaneous 3D printing projects — Bambu Lab A1 + build123d"
git push -u origin main
```

Expected:
- Repo created at `dakaneye/misc-3d-printing-projects`, public
- `main` branch pushed with all local commits

- [ ] **Step 3: Verify on GitHub**

```bash
gh repo view --web
```
Expected: browser opens to the public repo page with README visible.

At this moment the repo has NO CI, NO issue templates, NO LICENSE/CONTRIBUTING/etc. — sync will add all of those in Task 13.

---

### Task 13: Trigger the sync engine

**Files:** none

- [ ] **Step 1: Dispatch the sync-settings workflow manually**

(Normally sync runs weekly Monday 8am UTC. We don't want to wait.)

```bash
gh workflow run sync-settings.yml --repo dakaneye/.github
```

- [ ] **Step 2: Watch it run**

```bash
gh run watch --repo dakaneye/.github
```

Expected: workflow completes successfully. It will:
- Detect `misc-3d-printing-projects` as Python (pyproject.toml present)
- Apply `repo-sync-baseline` ruleset via API
- Open a PR against `dakaneye/misc-3d-printing-projects` titled something like "repo-sync: update baseline files" adding community health files + CI caller + Dependabot config + seed workflows

- [ ] **Step 3: Verify the sync PR exists**

```bash
gh pr list --repo dakaneye/misc-3d-printing-projects
```

Expected: one open PR from the sync bot on branch `repo-sync/settings`.

---

### Task 14: Review + merge the sync PR

**Files:** none

- [ ] **Step 1: Inspect what sync is adding**

```bash
gh pr view --repo dakaneye/misc-3d-printing-projects --web
```
Expected: PR adds `.github/ISSUE_TEMPLATE/*`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE` (MIT), `.github/workflows/ci.yml` (hookshot caller for `python-ci.yml`), `.github/dependabot.yml`, `.github/workflows/codeql.yml`, `.github/workflows/scan.yml`, `.github/workflows/dependabot-auto-merge.yml`.

Nothing this plan wrote should conflict — I avoided writing everything in
the enforced/dynamic list.

- [ ] **Step 2: Wait for PR checks to complete**

```bash
gh pr checks --repo dakaneye/misc-3d-printing-projects --watch
```
Expected: CI (python-ci via hookshot) runs on the PR and passes. The newly-added ci.yml runs ruff check + format check on the PR's merged state.

- [ ] **Step 3: Merge the PR**

```bash
gh pr merge --repo dakaneye/misc-3d-printing-projects --squash --delete-branch
```

- [ ] **Step 4: Pull merged changes locally**

```bash
cd ~/dev/personal/misc-3d-printing-projects
git pull --rebase origin main
```

Expected: your local main now has LICENSE, CONTRIBUTING, etc. + `.github/` workflows/config.

---

### Task 15: Verify completion gate

**Files:** none

Sanity-check that the public repo is in the "ready" state per `public-repo-setup` Principle 5.

- [ ] **Step 1: CI green on main**

```bash
gh run list --repo dakaneye/misc-3d-printing-projects --workflow=ci.yml --limit 1
```
Expected: most recent run `conclusion: success`.

- [ ] **Step 2: CodeQL green on main**

```bash
gh run list --repo dakaneye/misc-3d-printing-projects --workflow=codeql.yml --limit 1
```
Expected: most recent run `conclusion: success` (or in-progress; it's triggered by push so may still be running).

- [ ] **Step 3: Dependabot alerts = 0**

```bash
gh api "repos/dakaneye/misc-3d-printing-projects/dependabot/alerts" --jq 'length'
```
Expected: `0`.

- [ ] **Step 4: All Actions in `.github/workflows/*.yml` pinned**

```bash
grep -r "uses:" .github/workflows/ | grep -v "@[a-f0-9]\{40\}" | grep -v "dakaneye/hookshot"
```
Expected: empty (nothing unpinned except `dakaneye/hookshot/...@v1` which is pinned inside hookshot's tag).

- [ ] **Step 5: Branch protection ruleset exists**

```bash
gh api "repos/dakaneye/misc-3d-printing-projects/rulesets" --jq '.[].name'
```
Expected: output includes `repo-sync-baseline`.

If all five checks pass, the repo is public-ready. Report the completion
gate as a checked markdown list to the user.

---

## Phase 5: Physical execution checklist (human-driven)

The agent stops here. These tasks are for Sam to execute in the physical
world, with Wallace where noted.

### Task 16: Bambu A1 onboarding

- [ ] Unbox A1, follow Bambu's in-box QR-code setup
- [ ] Run the built-in bed leveling + vibration calibration
- [ ] Connect to local wifi, link to Bambu Handy app + Bambu account
- [ ] Complete the default first-print tutorial (usually a small benchy)
- [ ] Log the first-print experience in `print-log.md` under a dated entry

### Task 17: Oak Wood PLA calibration cube

- [ ] Load Oak Wood PLA on the spool holder
- [ ] Open the built-in 20mm calibration cube in Bambu Studio (or download one from Printables)
- [ ] Select "SUNLU PLA+ 2.0" filament profile manually
- [ ] Start with default temperature; adjust if layers look stringy or under-extruded
- [ ] Print; expect ~20 min
- [ ] Log temperature + flow adjustments + outcome in `print-log.md`
- [ ] Commit: `git commit -m "docs(print-log): oak-pla calibration cube"`

### Task 18: Pick the figurine with Wallace

- [ ] Browse MakerWorld / Printables for standing-pose wizard figurines, ~100mm tall, single-piece, "minimal supports" tag, ≥100 downloads, ≥4 stars
- [ ] Shortlist 3–4. Show Wallace only the shortlist — he picks the final one.
- [ ] Credit the creator explicitly when showing Wallace: "this is X's design"
- [ ] Download STL to `projects/wizard-figurine-for-wallace/downloaded/`
- [ ] Update `downloaded/SOURCES.md` with URL, author, license, today's date
- [ ] Commit: `git commit -m "docs(sources): add figurine provenance"`

### Task 19: Print the figurine

- [ ] Import the downloaded STL into Bambu Studio
- [ ] Orient for minimal supports; slice with the SUNLU PLA+ 2.0 Oak Wood profile
- [ ] Save the `.3mf` project file to `projects/wizard-figurine-for-wallace/<name>.3mf`. This IS committed (it's the slicer project, not a third-party raw STL)
- [ ] Print. Have Wallace watch the first 15 min. Enable time-lapse.
- [ ] When done, remove, inspect, photograph
- [ ] Log outcome in `print-log.md`. Commit: `git commit -m "docs(print-log): figurine print results"`

### Task 20: Measure figurine, update `base.py`, regenerate

- [ ] With calipers (or a ruler), measure the figurine's foot footprint: width × depth
- [ ] Edit `projects/wizard-figurine-for-wallace/3d/base.py`:
  - `FIGURINE_FOOT_WIDTH` = measured width + 0.4mm (print tolerance)
  - `FIGURINE_FOOT_DEPTH` = measured depth + 0.4mm
- [ ] Regenerate: `.venv/bin/python base.py`
- [ ] Open the new STL in Bambu Studio, visually confirm the recess
- [ ] Commit: `git commit -m "fix(base): dial in figurine footprint"`

### Task 21: Print the engraved base

- [ ] Slice `out/base.stl` in Bambu Studio with Oak Wood PLA profile
- [ ] Save the `.3mf` project file to `projects/wizard-figurine-for-wallace/base.3mf`; commit it
- [ ] Print. ~1–2h
- [ ] Remove, inspect engraving legibility, dry-fit the figurine in the recess
- [ ] If loose, apply a small dot of PLA-safe super glue
- [ ] If tight: add 0.2mm more tolerance, regenerate, reprint base (not figurine)
- [ ] Log in `print-log.md`. Commit.

### Task 22: Reveal + hand off to Wallace

- [ ] Snap figurine into base
- [ ] Photograph final result
- [ ] Add photo to `projects/wizard-figurine-for-wallace/README.md`
- [ ] Deliver to Wallace. Run through the four teaching beats
- [ ] Log Wallace's reaction in `print-log.md` — the real success criterion
- [ ] Final commit: `git commit -m "docs(print-log): wallace reveal"`

**Project v1 complete.** v2 (paint session) gets its own spec + plan when Sam is ready.
