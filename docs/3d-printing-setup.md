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
