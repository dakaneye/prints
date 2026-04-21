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
