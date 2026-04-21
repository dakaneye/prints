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
python3.13 -m venv .venv   # build123d caps at Python 3.13 — don't use 3.14+
.venv/bin/pip install --upgrade pip -r requirements.txt
```

**Python version note:** `build123d >=0.10.0` requires Python `>=3.10,<3.14`.
Homebrew's default `python3` on this Mac is currently 3.14, which pip will
refuse. Use `python3.13` explicitly (available via Nix / pyenv / uv). If
`which python3.13` fails, install one — e.g., `brew install python@3.13` or
`uv python install 3.13`.

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

Lint + tests run in CI via `dakaneye/hookshot`'s `python-ci.yml` reusable
workflow. The caller in `.github/workflows/ci.yml` is generated
automatically by the `~/dev/personal/.github` sync engine.

**Tests** live under `tests/` at the repo root. They run each project's
generator script and assert it produces a valid, non-trivial STL — catching
build123d API drift, import breakage, and geometry regressions. To run
locally:

```bash
# From repo root
python3.13 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

The root `.venv` is separate from the per-project `3d/.venv` — the root one
holds `build123d + pytest` for running tests; the project one holds just
`build123d` for authoring parts. Both are gitignored.
