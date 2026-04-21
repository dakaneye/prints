# `misc-3d-printing-projects` Repo + Wizard Figurine (Wallace) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a public GitHub repo for Sam's miscellaneous 3D printing projects and scaffold the first project — an unpainted wizard-themed figurine with a custom engraved oak display base for his 8-year-old nephew Wallace.

**Architecture:** Hybrid repo: each project folder pairs downloaded third-party STLs (gitignored, never committed) with parametric `build123d` scripts (original work, MIT-licensed). Public-facing strings are IP-neutral; internal design docs name the character freely. Repo starts private, flips public after the completion gate passes.

**Tech Stack:** Python 3.11+, `build123d >= 0.10.0`, `ruff` for linting, GitHub Actions (all pinned to full commit SHAs), CodeQL, Dependabot, Bambu Studio slicer, Bambu Lab A1 printer, SUNLU PLA+ 2.0 filament.

**Reference spec:** `docs/superpowers/specs/2026-04-21-harry-figurine-for-wallace-design.md`

---

## Phases

1. **Repo foundation** (tasks 1–7) — LICENSE, README, gitignore, conventions, pyproject.toml
2. **GitHub Actions + Dependabot** (tasks 8–12) — CI (ruff), CodeQL, Dependabot, issue templates
3. **First project scaffold** (tasks 13–18) — project folder, README, SOURCES.md template, base.py, build_all.py
4. **Local verification** (tasks 19–20) — ruff passes, base.py produces a valid STL
5. **GitHub repo creation + flip to public** (tasks 21–25) — create private, push, verify completion gate, flip public
6. **Physical execution checklist** (tasks 26–32) — Sam-driven printer onboarding, STL selection with Wallace, print, assemble, deliver

---

## Phase 1: Repo foundation

### Task 1: Create `.gitignore`

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Create `.gitignore` with the exact content below**

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
!**/sources/**/*.stl  # future escape hatch if we ever check in an authored STL
*.3mf

# Third-party downloaded models — NEVER commit these (IP + license compliance)
projects/*/downloaded/

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

- [ ] **Step 2: Verify `.gitignore` rules work**

Run: `cd ~/dev/personal/misc-3d-printing-projects && mkdir -p projects/test/downloaded && touch projects/test/downloaded/fake.stl && git status`
Expected: `projects/test/downloaded/fake.stl` does NOT appear in git status output.
Cleanup: `rm -rf projects/test`

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add gitignore"
```

---

### Task 2: Create `LICENSE` (MIT)

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Create MIT `LICENSE` with exact content below**

```
MIT License

Copyright (c) 2026 Sam Dacanay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Commit**

```bash
git add LICENSE
git commit -m "chore: add MIT license"
```

---

### Task 3: Create `CODEOWNERS`

**Files:**
- Create: `CODEOWNERS`

- [ ] **Step 1: Create top-level `CODEOWNERS`**

```
* @dakaneye
```

- [ ] **Step 2: Commit**

```bash
git add CODEOWNERS
git commit -m "chore: add codeowners"
```

---

### Task 4: Create `CONTRIBUTING.md`

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Create `CONTRIBUTING.md`**

```markdown
# Contributing

This is a personal hobby repository for Sam's miscellaneous 3D printing projects.
PRs are not expected — feel free to fork, adapt, and enjoy.

If you find a bug in one of the `build123d` scripts or a documentation issue,
issues are welcome. See the issue templates under `.github/ISSUE_TEMPLATE/`.

## Project structure

- `projects/<name>/downloaded/` — third-party STLs are pulled here locally only
  and are **never committed** (see `.gitignore`). Provenance lives in
  `downloaded/SOURCES.md`.
- `projects/<name>/3d/` — parametric `build123d` scripts that generate STLs
  for custom parts. Each follows the per-directory convention: `.venv/`,
  `requirements.txt`, `*.py`, `out/` (gitignored).

## License

MIT, applies to original code + docs only. Downloaded STLs retain their
original licenses per `SOURCES.md`.
```

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add contributing guide"
```

---

### Task 5: Create `pyproject.toml` (ruff config)

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
# build123d uses `from build123d import *` heavily — tolerate star imports
# in scripts under projects/*/3d/ and shared/3d/
select = ["E", "F", "W", "I"]
ignore = ["F403", "F405"]  # star imports + undefined from star

[tool.ruff.format]
quote-style = "double"
```

- [ ] **Step 2: Verify ruff config is valid**

Requires ruff installed locally. If not present: `pip install --user ruff` or use `pipx install ruff`.

Run: `cd ~/dev/personal/misc-3d-printing-projects && ruff check .`
Expected: PASS (no Python files yet, exit 0).

Run: `ruff format --check .`
Expected: PASS (no Python files yet, exit 0).

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add ruff config"
```

---

### Task 6: Create top-level `README.md`

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

```markdown
# misc-3d-printing-projects

Small, one-off 3D printing projects for Sam's Bambu Lab A1.

Each project is self-contained under `projects/<name>/`. Some projects are pure
downloads from the 3D-printing community (MakerWorld, Printables, Thingiverse);
some are pure `build123d` parametric scripts I've written; most are hybrids —
a downloaded model paired with a custom accent part I coded.

## Repository layout

```
misc-3d-printing-projects/
├── docs/
│   ├── 3d-printing-setup.md    # Bambu A1 + Bambu Studio workflow notes
│   └── superpowers/            # Project design docs + plans
├── projects/
│   └── <project-name>/
│       ├── README.md           # What this project is
│       ├── downloaded/         # Third-party STLs (LOCAL ONLY — gitignored)
│       │   └── SOURCES.md      # URL + author + license + download date
│       ├── 3d/                 # build123d scripts for parametric parts
│       └── print-log.md        # Per-print diary
└── conventions.md              # Folder layout + filament catalog + naming
```

## Projects

| Project | Status | Description |
|---|---|---|
| `wizard-figurine-for-wallace` | in progress | A wizard-themed figurine with a personalized engraved oak display base |

## Printer + filament

See `docs/3d-printing-setup.md`.

## License

MIT — see `LICENSE`. Applies to my original code and docs. Downloaded STLs
retain their original licenses and are never committed to this repo.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add top-level readme"
```

---

### Task 7: Create `conventions.md`

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

- Project folders: `kebab-case`, descriptive, IP-neutral (no copyrighted character
  names in public-facing strings)
- `build123d` scripts: `snake_case.py`, one part per file
- STL output: generator writes to `out/<same_name_as_script>.stl`

## Filament catalog (on hand as of 2026-04-21)

| Filament | Brand | Notes |
|---|---|---|
| Black | SUNLU PLA+ 2.0 | General purpose |
| White | SUNLU PLA+ 2.0 | Best for painting; prime canvas |
| Grey | SUNLU PLA+ 2.0 | Neutral, hides print lines |
| Oak Wood | SUNLU PLA+ 2.0 | Wood-filled; prints with visible grain, good unpainted |

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
# `align=(CENTER, CENTER, MIN)` = bottom of shape at Z=0, centered in XY.
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
  committed. `SOURCES.md` links out to the hosting site without mirroring bytes.
```

- [ ] **Step 2: Commit**

```bash
git add conventions.md
git commit -m "docs: add conventions"
```

---

## Phase 2: GitHub Actions + Dependabot

### Task 8: Create `.github/dependabot.yml`

**Files:**
- Create: `.github/dependabot.yml`

- [ ] **Step 1: Create `.github/dependabot.yml`**

```yaml
version: 2
updates:
  # Python dependencies for each project's build123d scripts.
  # Listed individually because Dependabot needs an exact directory per entry.
  - package-ecosystem: "pip"
    directory: "/projects/wizard-figurine-for-wallace/3d"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3

  # GitHub Actions — the commonly-missed ecosystem.
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3
```

- [ ] **Step 2: Commit**

```bash
git add .github/dependabot.yml
git commit -m "ci: configure dependabot for pip and actions"
```

---

### Task 9: Create issue templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/feature_request.md`

- [ ] **Step 1: Create `.github/ISSUE_TEMPLATE/bug_report.md`**

```markdown
---
name: Bug report
about: Something in a build123d script or CI broke
title: "[bug] "
labels: bug
---

**What broke:**

**What you were trying to do:**

**Project / script affected:**

**Steps to reproduce:**

**Expected vs actual:**
```

- [ ] **Step 2: Create `.github/ISSUE_TEMPLATE/feature_request.md`**

```markdown
---
name: Feature request
about: Suggest a new project or script
title: "[idea] "
labels: enhancement
---

**What the project / part would do:**

**Why it's interesting:**

**Rough size estimate (print time, complexity):**
```

- [ ] **Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/
git commit -m "ci: add bug + feature issue templates"
```

---

### Task 10: Fetch current SHAs for GitHub Actions

**Files:** none (this is a lookup step)

All Actions must be pinned to full commit SHAs per the public-repo-setup skill. Fetch current SHAs now so the workflows use up-to-date pins.

- [ ] **Step 1: Fetch actions/checkout SHA**

Run: `gh api repos/actions/checkout/commits/v4 --jq '.sha'`
Record the SHA in your scratchpad (40 chars, starts with a hex prefix).

- [ ] **Step 2: Fetch actions/setup-python SHA**

Run: `gh api repos/actions/setup-python/commits/v5 --jq '.sha'`
Record the SHA.

- [ ] **Step 3: Fetch github/codeql-action SHA**

Run: `gh api repos/github/codeql-action/commits/v3 --jq '.sha'`
Record the SHA. (Both `init` and `analyze` use the same repo, same SHA.)

- [ ] **Step 4: No commit — SHAs get baked into the workflow files in Tasks 11–12.**

---

### Task 11: Create `.github/workflows/ci.yml` (ruff lint)

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create `ci.yml` with actual SHAs from Task 10**

Replace `<CHECKOUT_SHA>` and `<SETUP_PYTHON_SHA>` with the SHAs fetched in Task 10.

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: Ruff lint + format check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<CHECKOUT_SHA>  # v4

      - uses: actions/setup-python@<SETUP_PYTHON_SHA>  # v5
        with:
          python-version: "3.11"

      - name: Install ruff
        run: pip install ruff

      - name: ruff check
        run: ruff check .

      - name: ruff format check
        run: ruff format --check .
```

- [ ] **Step 2: Verify YAML syntax locally**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
Expected: no output, exit 0.

(Fallback if PyYAML not installed: `python3 -c "import yaml" 2>&1` → if ImportError, install with `pip install --user pyyaml` or skip this step; CI will validate on push anyway.)

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add ruff lint workflow"
```

---

### Task 12: Create `.github/workflows/codeql.yml`

**Files:**
- Create: `.github/workflows/codeql.yml`

- [ ] **Step 1: Create `codeql.yml` with actual SHAs from Task 10**

Replace `<CHECKOUT_SHA>` and `<CODEQL_SHA>` with the SHAs fetched in Task 10.

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 12 * * 1"  # Mondays at 12:00 UTC

jobs:
  analyze:
    name: Analyze Python
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@<CHECKOUT_SHA>  # v4

      - uses: github/codeql-action/init@<CODEQL_SHA>  # v3
        with:
          languages: python

      - uses: github/codeql-action/analyze@<CODEQL_SHA>  # v3
```

- [ ] **Step 2: Verify YAML syntax**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/codeql.yml'))"`
Expected: no output, exit 0.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/codeql.yml
git commit -m "ci: add codeql workflow"
```

---

## Phase 3: First project scaffold

### Task 13: Create `docs/3d-printing-setup.md`

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

**Bambu Studio** installed at `/Applications/BambuStudio.app` (macOS, Homebrew install).

Import STLs via `File → Import → Import 3MF/STL`, or drag-drop into the plater.
`File → Open Project` only accepts `.3mf` slicer project bundles, not raw STL.

## Filament profiles

Filament catalog: see `conventions.md`.

SUNLU PLA+ 2.0 has no RFID — manually select **"SUNLU PLA+ 2.0"** profile in
Bambu Studio.

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
project's `.venv`. Gives you live 3D preview of build123d parts without
re-exporting STL each time.

## Related

- Detailed Bambu Studio + A1 onboarding walkthrough:
  `~/dev/personal/word-clock-for-my-daughters/docs/hardware/3d-printing-setup.md`
  (private repo, same author).
```

- [ ] **Step 2: Commit**

```bash
git add docs/3d-printing-setup.md
git commit -m "docs: add 3d printing setup guide"
```

---

### Task 14: Create project folder skeleton

**Files:**
- Create: `projects/wizard-figurine-for-wallace/README.md`
- Create: `projects/wizard-figurine-for-wallace/print-log.md`

- [ ] **Step 1: Create the project folder**

Run: `mkdir -p ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d`

- [ ] **Step 2: Create `projects/wizard-figurine-for-wallace/README.md`** (IP-neutral, with teaching beats)

```markdown
# Wizard figurine for Wallace

A wizard-themed figurine with a personalized engraved oak display base —
built for Sam's 8-year-old nephew as his introduction to 3D printing.

## What's in this folder

- `downloaded/` (LOCAL ONLY — gitignored) — the downloaded figurine STL
- `downloaded/SOURCES.md` — provenance: URL, author, license, date for each STL
- `3d/base.py` — parametric engraved display base (Python / build123d)
- `3d/build_all.py` — regenerates every STL in `3d/`
- `print-log.md` — per-print diary

## Print recipe

| Part | Filament | Print time | Notes |
|---|---|---|---|
| Figurine (downloaded) | Oak Wood PLA | ~5–7h | ~100mm tall; minimal supports only |
| Display base (`base.py`) | Oak Wood PLA | ~1–2h | Engraved with "WALLACE" + print date |

Slicer: Bambu Studio, "SUNLU PLA+ 2.0" profile manually selected.

## Assembly

V1: figurine's feet sit into a recessed footprint in the base — no glue.
Fallback: single dot of PLA-safe super glue, or hidden M3 insert + screw.

## How to run this with Wallace

Four deliberate teaching beats — don't skip them:

1. **"The internet has amazing builders"** — browse MakerWorld together, look
   at the STL author's profile, credit them by name. Someone *made* this.
2. **"But we can make our own too"** — open `3d/base.py`, change the engraved
   text live (demo: change "WALLACE" → "HARRY" → regenerate → look at the
   new STL → change back to "WALLACE"). Same file, different part.
3. **"Watch the robot build it"** — start the figurine print together, watch
   the first 15 minutes, explain layer height ("each line is thinner than a
   hair"), start Bambu Studio's time-lapse capture.
4. **"The reveal"** — pop the figurine off the plate, snap into the base,
   hand to Wallace. Set expectations if unpainted: "this is the wooden
   version — we'll paint it together next time."

## Version history

- **v1 (this print):** unpainted, oak-wood figurine + engraved oak base
- **v2 (future):** paint session with Wallace (Army Painter Speedpaint kit)
- **v3+ (future):** additional poses / companion figures once v1 lands
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

### Task 15: Create `downloaded/SOURCES.md` template

**Files:**
- Create: `projects/wizard-figurine-for-wallace/downloaded/.gitkeep`
- Create: `projects/wizard-figurine-for-wallace/downloaded/SOURCES.md`

**Important:** `downloaded/` is gitignored per `.gitignore` (`projects/*/downloaded/`). The rules must be amended to still track `.gitkeep` and `SOURCES.md` so the folder + its provenance template exist in the repo.

- [ ] **Step 1: Amend `.gitignore` to allow `.gitkeep` and `SOURCES.md` inside `downloaded/`**

Edit `.gitignore`. Find the line `projects/*/downloaded/` and replace the "Third-party downloaded models" block with:

```gitignore
# Third-party downloaded models — NEVER commit STL/3MF/step bytes (IP + license compliance)
projects/*/downloaded/*
# ...except the provenance placeholder + SOURCES index, which track the folder's existence
!projects/*/downloaded/.gitkeep
!projects/*/downloaded/SOURCES.md
```

- [ ] **Step 2: Create the `.gitkeep` placeholder**

Run: `touch projects/wizard-figurine-for-wallace/downloaded/.gitkeep`

- [ ] **Step 3: Create `SOURCES.md`**

```markdown
# Downloaded STL sources

One entry per downloaded file. Fill in when a file is added to this folder.

**STL/3MF/step files themselves are gitignored** — only this SOURCES.md gets
committed. Do not re-host third-party models.

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

- [ ] **Step 4: Verify gitignore still excludes STL bytes but allows tracking files**

Run the following from the repo root:

```bash
touch projects/wizard-figurine-for-wallace/downloaded/fake.stl
git status --porcelain projects/wizard-figurine-for-wallace/downloaded/
```

Expected output: only `SOURCES.md` and `.gitkeep` appear; `fake.stl` is absent (silently ignored).

Cleanup: `rm projects/wizard-figurine-for-wallace/downloaded/fake.stl`

- [ ] **Step 5: Commit**

```bash
git add .gitignore projects/wizard-figurine-for-wallace/downloaded/.gitkeep projects/wizard-figurine-for-wallace/downloaded/SOURCES.md
git commit -m "feat: add sources template for downloaded stls"
```

---

### Task 16: Create `3d/requirements.txt`

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

### Task 17: Write `3d/base.py` (parametric engraved base)

**Files:**
- Create: `projects/wizard-figurine-for-wallace/3d/base.py`

- [ ] **Step 1: Create `.venv` and install `build123d`**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

Expected: `build123d` installs along with OpenCascade native deps. Takes ~2-3 min on first run.

- [ ] **Step 2: Write `base.py`**

```python
"""Display base for the wizard figurine.

A rectangular oak plaque with the recipient's name + print date engraved on
the top surface and a shallow recess that locates the figurine's feet.

FIGURINE_FOOT_WIDTH / FIGURINE_FOOT_DEPTH below are placeholders — after
printing the figurine, measure its feet with calipers and update these.
See Task 30 of the implementation plan.
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
# Plaque outer dimensions. Sized to give a ~100mm figurine a "stand" feel.
BASE_WIDTH = 90.0
BASE_DEPTH = 60.0
BASE_HEIGHT = 10.0

# Recipient name + date (engraved on top surface, front half)
RECIPIENT_NAME = "WALLACE"
PRINT_DATE = "APR 2026"

# Engraving depth — readable at arm's length, shallow enough to not weaken
# the plaque's top layer.
ENGRAVE_DEPTH = 1.2

NAME_FONT_SIZE = 10.0
DATE_FONT_SIZE = 5.0

# Recessed footprint for figurine's feet — PLACEHOLDER values.
# After the figurine prints, measure its base and update these (+ 0.4mm
# print tolerance per dimension).
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

**Note on the build123d API:** `Text` + `extrude` usage here matches the algebra-mode pattern documented in build123d 0.10+. If `base.py` fails on first run with an import or signature error, consult https://build123d.readthedocs.io/ for the exact current API — `Text` may need a `font=` argument on some systems, and `extrude` may require a sketch/plane context depending on version. Expect 0–2 iterations on the first run.

- [ ] **Step 3: Run it**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
.venv/bin/python base.py
```

Expected:
- Prints `Wrote .../out/base.stl`
- `out/base.stl` exists
- `out/base.stl` size > 1 KB

- [ ] **Step 4: Verify the STL is valid**

Run: `ls -la projects/wizard-figurine-for-wallace/3d/out/base.stl`
Expected: file exists with nonzero size. For visual check, open the STL in Bambu Studio (optional — not required for plan completion, but catches most bugs): the plaque should have "WALLACE" + date engraved on the top, a shallow rectangular recess in the back half, and chamfered top edges.

- [ ] **Step 5: Commit**

```bash
git add projects/wizard-figurine-for-wallace/3d/base.py
git commit -m "feat: parametric engraved display base"
```

---

### Task 18: Write `3d/build_all.py`

**Files:**
- Create: `projects/wizard-figurine-for-wallace/3d/build_all.py`

- [ ] **Step 1: Create `build_all.py`**

```python
"""Regenerate every STL in this directory by running every sibling *.py file.

Excludes itself (build_all.py). Output goes to each script's local out/.
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

- [ ] **Step 2: Run it**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
.venv/bin/python build_all.py
```

Expected:
- Prints `=== base.py ===`
- Prints `Wrote .../out/base.stl`
- Prints `All 1 script(s) regenerated successfully.`
- Exit 0

- [ ] **Step 3: Commit**

```bash
git add projects/wizard-figurine-for-wallace/3d/build_all.py
git commit -m "feat: add build_all.py for wizard project"
```

---

## Phase 4: Local verification

### Task 19: Run ruff locally (must pass before CI sees it)

**Files:** none

- [ ] **Step 1: Run ruff check**

```bash
cd ~/dev/personal/misc-3d-printing-projects
ruff check .
```

Expected: exit 0, no complaints.

If ruff flags issues, fix them in the offending file, re-run, and amend the appropriate earlier commit OR add a `fix: ruff cleanup` commit. Do not proceed until ruff passes.

- [ ] **Step 2: Run ruff format check**

```bash
ruff format --check .
```

Expected: exit 0. If it complains, run `ruff format .`, inspect the diff, and commit the formatting fixes as `style: ruff format`.

- [ ] **Step 3: Confirm git status is clean**

Run: `git status`
Expected: "nothing to commit, working tree clean"

---

### Task 20: Run `build_all.py` from scratch on a fresh venv

**Files:** none

Validates the setup instructions in `docs/3d-printing-setup.md` actually work.

- [ ] **Step 1: Remove the existing venv and regenerated STL**

```bash
cd ~/dev/personal/misc-3d-printing-projects/projects/wizard-figurine-for-wallace/3d
rm -rf .venv out
```

- [ ] **Step 2: Follow the documented setup from zero**

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python build_all.py
```

Expected:
- `build123d` installs cleanly
- `base.py` runs, writes `out/base.stl`
- `build_all.py` reports success, exits 0

- [ ] **Step 3: Confirm `out/base.stl` is NOT staged**

Run: `git status`
Expected: clean working tree. `out/` is gitignored; `.venv/` is gitignored.

---

## Phase 5: GitHub repo creation + flip to public

### Task 21: Create the GitHub repo (PRIVATE to start)

**Files:** none

Creating private first lets us verify the completion gate before exposing anything.

- [ ] **Step 1: Create the repo as private, push existing commits**

```bash
cd ~/dev/personal/misc-3d-printing-projects
gh repo create misc-3d-printing-projects --private --source=. --remote=origin --description "Miscellaneous 3D printing projects — Bambu Lab A1 + build123d"
git push -u origin main
```

Expected:
- Repo created under Sam's account
- `main` branch pushed with all commits from Tasks 1–18
- CI workflow (Task 11) + CodeQL (Task 12) both start running on the push event

- [ ] **Step 2: Verify the push landed**

Run: `gh repo view --web`
Expected: browser opens to the repo page showing the README and the commit history. Note the URL for later reference.

---

### Task 22: Verify CI and CodeQL pass

**Files:** none

- [ ] **Step 1: Wait for workflow runs to complete**

Run: `gh run list --limit 5`
Expected: two runs listed — "CI" and "CodeQL" — both eventually in `completed` state with `success` conclusion.

If either is still `in_progress`, wait a minute and re-run.

- [ ] **Step 2: Inspect failure if either run fails**

If CI failed, run: `gh run view --log-failed`
Common failure: ruff complaint on something local ruff didn't catch (very rare; both should use the same version). Fix, push, wait for re-run.

If CodeQL failed and it's not a syntax issue: CodeQL occasionally flags benign Python patterns. Read the alert, decide if it's a real issue or a suppression candidate. Do not proceed to Task 25 until both runs are green.

---

### Task 23: Enable Dependabot + security features

**Files:** none

- [ ] **Step 1: Enable Dependabot alerts and security updates**

```bash
gh api -X PATCH "repos/:owner/misc-3d-printing-projects" \
  -f security_and_analysis='{"advanced_security":{"status":"enabled"},"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"},"dependabot_security_updates":{"status":"enabled"}}'
```

Note: `advanced_security` is only available on public repos (and GHE with an Advanced Security license). If this API call fails with `"advanced_security is only available on public or enterprise repositories"`, omit that sub-object and re-run with just `secret_scanning` + `secret_scanning_push_protection` + `dependabot_security_updates`. Advanced Security enables automatically once we flip to public in Task 25.

- [ ] **Step 2: Verify Dependabot picked up our config**

Run: `gh api "repos/:owner/misc-3d-printing-projects/dependabot/alerts"`
Expected: empty array `[]` (no known vulnerabilities in our deps yet — ✓ clean).

---

### Task 24: Set branch protection on `main`

**Files:** none

- [ ] **Step 1: Enable required status checks and review before merge**

```bash
gh api -X PUT "repos/:owner/misc-3d-printing-projects/branches/main/protection" \
  -f required_status_checks='{"strict":true,"contexts":["Ruff lint + format check","Analyze Python"]}' \
  -f enforce_admins=false \
  -f required_pull_request_reviews='{"required_approving_review_count":0,"dismiss_stale_reviews":true}' \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

Rationale: `required_approving_review_count=0` because Sam is the sole maintainer — requiring self-approval is friction without benefit. The important gates are: CI must pass, no force pushes, no deletions.

- [ ] **Step 2: Verify the protection took effect**

Run: `gh api "repos/:owner/misc-3d-printing-projects/branches/main/protection" --jq '.required_status_checks.contexts'`
Expected: `["Ruff lint + format check", "Analyze Python"]`

- [ ] **Step 3: Run `gitleaks` over the repo's full history**

Install if needed: `brew install gitleaks`

Run: `gitleaks detect --source . --verbose`
Expected: `no leaks found`. If any leak is reported, STOP — do not proceed to Task 25. Rewrite history to remove the leak and rotate the secret.

---

### Task 25: Flip repo to public

**Files:** none

All security gates passed. Flip to public.

- [ ] **Step 1: Run the completion gate checklist manually**

Confirm every item is green before flipping:

- CI green on latest main commit: `gh run list --workflow=ci.yml --limit 1`
- CodeQL green on latest main commit: `gh run list --workflow=codeql.yml --limit 1`
- Dependabot alerts = 0: `gh api "repos/:owner/misc-3d-printing-projects/dependabot/alerts" --jq 'length'`
- CodeQL alerts = 0: `gh api "repos/:owner/misc-3d-printing-projects/code-scanning/alerts?severity=high,critical" --jq 'length'` (may error if scanning hasn't run yet on a private repo without Advanced Security — OK to proceed if previous checks all green)
- Gitleaks clean: Task 24 Step 3
- All Actions pinned to SHAs: `grep -r "uses:" .github/workflows/ | grep -v "@[a-f0-9]\{40\}"` should return nothing (except a mandatory blank line / comment).

If any check fails, fix before flipping.

- [ ] **Step 2: Flip to public**

```bash
gh repo edit --visibility public --accept-visibility-change-consequences
```

Expected: repo is now public. Re-run `gh repo view --web` to verify.

- [ ] **Step 3: Re-verify Advanced Security is now enabled**

Run: `gh api "repos/:owner/misc-3d-printing-projects" --jq '.security_and_analysis'`
Expected: `advanced_security.status == "enabled"`. Re-run Task 23 Step 1 if not.

---

## Phase 6: Physical execution checklist (human-driven)

The agent stops here. The following tasks are for Sam to execute in the physical world with Wallace. Each step updates the repo afterward.

### Task 26: Bambu A1 onboarding

- [ ] Unbox A1, follow Bambu's in-box QR-code setup
- [ ] Run the built-in bed leveling + vibration calibration
- [ ] Connect to local wifi, link to Bambu Handy app + Bambu account
- [ ] Successfully complete the default first-print tutorial (usually a small benchy)
- [ ] Log the first-print experience in `print-log.md` under a dated entry

### Task 27: Oak Wood PLA calibration cube

Validates the SUNLU PLA+ 2.0 wood profile before committing to a longer print.

- [ ] Load Oak Wood PLA on the spool holder
- [ ] In Bambu Studio, open the built-in 20mm calibration cube (or download from Printables)
- [ ] Select "SUNLU PLA+ 2.0" filament profile manually
- [ ] Start with default temperature; adjust if layers look stringy or under-extruded
- [ ] Print; expect ~20 min
- [ ] Log temperature + flow adjustments + outcome in `print-log.md`
- [ ] Commit the print-log update: `git commit -m "docs(print-log): oak-pla calibration cube"`

### Task 28: Pick the figurine with Wallace

- [ ] Browse MakerWorld / Printables for standing-pose wizard figurines, ~100mm tall, single-piece, "minimal supports" tag, ≥100 downloads, ≥4 stars
- [ ] Shortlist 3–4. Show Wallace only the shortlist — he picks the final one.
- [ ] Credit the creator explicitly when showing Wallace: "this is X's design"
- [ ] Download STL to `projects/wizard-figurine-for-wallace/downloaded/`
- [ ] Update `downloaded/SOURCES.md` with URL, author, license, today's date
- [ ] Commit: `git commit -m "docs(sources): add figurine provenance"`

### Task 29: Print the figurine

- [ ] Import the downloaded STL into Bambu Studio
- [ ] Orient for minimal supports; slice with the SUNLU PLA+ 2.0 Oak Wood profile
- [ ] Save the `.3mf` project file to `projects/wizard-figurine-for-wallace/<name>.3mf` (this IS committed — it's the slicer project, not a raw STL from a third party)
- [ ] Print. Have Wallace watch the first 15 min. Enable time-lapse.
- [ ] When done, remove, inspect, photograph
- [ ] Log outcome in `print-log.md`. Commit: `git commit -m "docs(print-log): figurine print results"`

### Task 30: Measure figurine, update `base.py`, regenerate

- [ ] With calipers (or a ruler if that's what you have), measure the figurine's foot footprint: width × depth
- [ ] Edit `projects/wizard-figurine-for-wallace/3d/base.py`:
  - `FIGURINE_FOOT_WIDTH` = measured width + 0.4mm (print tolerance)
  - `FIGURINE_FOOT_DEPTH` = measured depth + 0.4mm
- [ ] Regenerate: `.venv/bin/python base.py`
- [ ] Open the new STL in Bambu Studio, visually confirm the recess looks right
- [ ] Commit: `git commit -m "fix(base): dial in figurine footprint dimensions"`

### Task 31: Print the engraved base

- [ ] Slice `out/base.stl` in Bambu Studio with Oak Wood PLA profile
- [ ] Save `.3mf` project file to `projects/wizard-figurine-for-wallace/base.3mf`; commit it
- [ ] Print. Takes ~1–2h
- [ ] Remove, inspect engraving legibility, dry-fit the figurine in the recess
- [ ] If the figurine is too loose, apply a small dot of PLA-safe super glue
- [ ] If too tight: measure again, add 0.2mm more tolerance, regenerate, reprint base (not figurine)
- [ ] Log in `print-log.md`. Commit.

### Task 32: Reveal + hand off to Wallace

- [ ] Snap figurine into base
- [ ] Photograph final result
- [ ] Add a photo (or a `photo-placeholder.md` noting one needs to be added) to `projects/wizard-figurine-for-wallace/README.md`
- [ ] Deliver to Wallace. Run through the four teaching beats from the project README ("The internet has amazing builders," "But we can make our own too," "Watch the robot build it," "The reveal")
- [ ] Log Wallace's reaction in `print-log.md` — the real success criterion
- [ ] Final commit: `git commit -m "docs(print-log): wallace reveal"`

**Project v1 complete.** v2 (paint session) gets its own spec + plan when Sam is ready.
