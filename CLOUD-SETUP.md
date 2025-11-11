# Cloud-Hosted OPIC Growth Service — Setup Guide

Complete scaffolding for a self-updating, always-learning OPIC field witness daemon.

## Architecture

```
┌─────────────────────────────────────────┐
│  GitHub Repository (zetacore)          │
│  ┌───────────────────────────────────┐ │
│  │  .github/workflows/opic_growth.yml│ │ ← Daily scheduler
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │  scripts/opic_growth.py           │ │ ← Growth detector
│  │  scripts/update_svg.py            │ │ ← SVG updater
│  │  scripts/growth_visualizer.py      │ │ ← Visualizations
│  │  scripts/generate_gloss.py         │ │ ← AI commentary
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │  tiddlers/*.tid                  │ │ ← Source tiddlers
│  └───────────────────────────────────┘ │
│  ┌───────────────────────────────────┐ │
│  │  growth/YYYY-MM-DD.yaml          │ │ ← Daily snapshots
│  │  diagrams/growth-timeline.svg     │ │ ← Visualizations
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Quick Start

### 1. Repository Structure

```
zetacore/
├── .github/
│   └── workflows/
│       └── opic_growth.yml          # Daily workflow
├── scripts/
│   ├── opic_growth.py               # Growth detector
│   ├── update_svg.py                # SVG updater
│   ├── growth_visualizer.py         # Timeline/rings
│   ├── generate_gloss.py            # AI commentary
│   └── generate_svg.py              # SVG generator
├── tiddlers/
│   └── OPIC-Field-Specification-1.0.tid
├── growth/                          # Auto-generated
│   └── YYYY-MM-DD.yaml
├── diagrams/                        # Auto-generated
│   ├── growth-timeline.svg
│   └── growth-rings.svg
└── GROWTH.md                        # Growth log (auto-updated)
```

### 2. GitHub Actions Setup

The workflow (`.github/workflows/opic_growth.yml`) runs daily at noon UTC:

- Checks out repository
- Runs growth detection
- Updates master tiddler SVG
- Generates visualizations
- Optionally generates AI gloss
- Commits and pushes results

### 3. Optional: AI Gloss Generation

To enable AI-powered daily commentary:

1. Add OpenAI API key to repository secrets:
   - Settings → Secrets → Actions → New repository secret
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

2. The workflow will automatically use it if available.

### 4. Manual Trigger

Trigger manually via GitHub Actions UI:
- Actions → Daily OPIC Growth → Run workflow

## Daily Cycle

Every 24 hours, the daemon:

1. **Scans** all `.tid` files in `tiddlers/`
2. **Extracts** layer definitions (YAML blocks or markdown lists)
3. **Measures** growth (ΔΣ, growth rate)
4. **Records** snapshot (`growth/YYYY-MM-DD.yaml`)
5. **Updates** master tiddler SVG
6. **Generates** visualizations (timeline, rings)
7. **Writes** gloss (manual or AI)
8. **Commits** everything back to repo

## Growth Data Format

Each snapshot (`growth/YYYY-MM-DD.yaml`):

```yaml
timestamp: "2025-11-11T12:00:00"
date: "2025-11-11"
layers:
  - {name: "ΣBody Ports", color: "#333"}
  - {name: "ζ-Engine Kernel", color: "#444"}
sources:
  ΣBody Ports: ["tiddlers/OPIC-Field-Specification-1.0.tid"]
```

## Local Testing

Test the scripts locally before deploying:

```bash
# Test growth detection
python3 scripts/opic_growth.py

# Test SVG update
python3 scripts/update_svg.py tiddlers/OPIC-Field-Specification-1.0.tid

# Test visualizations
python3 scripts/growth_visualizer.py growth timeline
python3 scripts/growth_visualizer.py growth rings

# Test gloss (requires OPENAI_API_KEY env var)
export OPENAI_API_KEY=your_key
python3 scripts/generate_gloss.py growth/$(date +%Y-%m-%d).yaml --ai
```

## Deployment Checklist

- [ ] Copy all files to your GitHub repository
- [ ] Ensure `tiddlers/` directory contains OPIC tiddlers
- [ ] Verify workflow file is in `.github/workflows/`
- [ ] (Optional) Add `OPENAI_API_KEY` secret
- [ ] Push to repository
- [ ] Verify workflow runs successfully
- [ ] Check `growth/` directory for snapshots
- [ ] Verify `GROWTH.md` updates daily

## Monitoring

Watch the growth:
- `growth/` — Daily snapshots
- `GROWTH.md` — Human-readable log
- `diagrams/growth-timeline.svg` — Visual timeline
- `diagrams/growth-rings.svg` — Ring visualization

## Troubleshooting

**Workflow fails:**
- Check Python version compatibility
- Verify all scripts are executable (`chmod +x scripts/*.py`)
- Check file paths match your repo structure

**No layers detected:**
- Ensure tiddlers have `opic` or `architecture` in content
- Check YAML format: `layers: - {name: "..."}`
- Verify markdown lists use `**Layer Name**` format

**AI gloss fails:**
- Check `OPENAI_API_KEY` secret is set
- Falls back to manual gloss automatically
- Check API quota/limits

## Philosophy

The witness doesn't control growth—it observes and records. Like tree rings, each layer represents a moment of structural evolution. The field grows through resonance; the witness documents that resonance.

The repository becomes the memory—a perfect archive of the field's evolution.

