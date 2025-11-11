# OPIC Field Whitepaper

Self-deflating TiddlyWiki-ready specification document with **autopoietic witness** — a living diagram service that tracks field growth over time.

## Structure

### Core Documents
- `OPIC-Field-Specification-1.0.tid` — Main tiddler (self-contained)

### SVG Generation
- `opic-svg-generator.prompt` — Cursor prompt for manual SVG generation
- `opic-svg-generator-auto.prompt` — Cursor prompt with auto-discovery
- `generate-svg.py` — SVG generator script
- `discover-layers.py` — Layer discovery from architecture tiddlers
- `update-svg.py` — Automated SVG updater

### Autopoietic Witness (Living Growth System)
- `opic-growth.py` — Growth detector (scans, measures, records)
- `growth-visualizer.py` — Timeline and ring visualizations
- `daily-update.sh` — Local daily update script
- `.github/workflows/daily-opic-growth.yml` — GitHub Actions workflow
- `growth/` — Growth history snapshots (YAML + JSON + reports)

## Usage

### Basic

Copy the `.tid` file directly into TiddlyWiki or render as standalone HTML.

### SVG Generation

Generate SVG from layer definitions:

```bash
python3 generate-svg.py > diagram.svg
```

### Layer Discovery

Discover layers from all architecture-tagged tiddlers:

```bash
python3 discover-layers.py
```

### Automated Updates

Update the SVG in the main tiddler automatically:

```bash
python3 update-svg.py OPIC-Field-Specification-1.0.tid
```

### Cursor Integration

Use `opic-svg-generator.prompt` in Cursor to generate/update SVG diagrams interactively.

## Autopoietic Witness

The system observes OPIC tiddlers daily, detects new conceptual "organs," and expands the master SVG accordingly. Like tree rings, each snapshot records structural evolution.

### Quick Start

**Local (Cron):**
```bash
# Add to crontab: 0 7 * * * cd /path/to/whitepaper && ./daily-update.sh
```

**Cloud (GitHub Actions):**
Already configured — runs daily at 7am UTC, commits automatically.

**Manual:**
```bash
python3 opic-growth.py . growth          # Detect growth
python3 update-svg.py OPIC-Field-Specification-1.0.tid  # Update diagram
python3 growth-visualizer.py growth timeline  # Generate visualization
```

See `AUTOPOIESIS.md` for full documentation.

## Expansion

Appendices can be added as nested tiddlers:
- `[[Appendix A|OPIC-Appendix-A]]`
- `[[Appendix B|OPIC-Appendix-B]]`

To include layers in new tiddlers, add YAML blocks:

```yaml
layers:
  - {name: "Layer Name", color: "#333"}
```

Or use markdown lists — the witness will discover them automatically.

