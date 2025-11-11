# Autopoietic Witness: Living Diagram Service

The OPIC field grows organically. This system observes, measures, and visualizes that growth.

## Core Concept

**Autopoietic** = self-creating. The witness service:
- Observes OPIC tiddlers daily
- Detects new conceptual "organs" (layers)
- Expands the master SVG diagram
- Records growth history (like tree rings)
- Visualizes learning momentum

## Mathematical Framing

```
ΔΣ(t) = Σ(t+1) − Σ(t)          # Daily growth delta
g(t) = |ΔΣ(t)| / |Σ(t)|         # Growth rate
```

Each expansion = new harmonic resonance in the field.

## Components

### 1. Growth Detector (`opic-growth.py`)

Scans all `.tid` files, extracts layers, computes metrics:

```bash
python3 opic-growth.py [directory] [growth_dir]
```

Outputs:
- Timestamped snapshots (`growth/YYYY-MM-DD.yaml`)
- Growth reports (`growth/YYYY-MM-DD.txt`)
- Metrics: delta, growth rate, new layers

### 2. Growth Visualizer (`growth-visualizer.py`)

Generates timeline and ring visualizations:

```bash
python3 growth-visualizer.py [growth_dir] [timeline|rings]
```

Creates:
- `growth-timeline.svg` — linear growth chart
- `growth-rings.svg` — concentric rings (like tree growth)

### 3. Daily Update Script (`daily-update.sh`)

Orchestrates the full cycle:

```bash
./daily-update.sh
```

Runs:
1. Growth detection
2. SVG update
3. Visualization generation
4. Git commit (if in repo)

## Deployment Options

### Option 1: Local (Cron)

Add to crontab:

```bash
0 7 * * * cd /path/to/whitepaper && ./daily-update.sh
```

Runs every morning at 7am.

### Option 2: Cloud (GitHub Actions)

Already configured in `.github/workflows/daily-opic-growth.yml`

- Runs daily at 7am UTC
- Commits growth snapshots automatically
- Can be triggered manually via `workflow_dispatch`

## Growth Data Structure

Each snapshot (`growth/YYYY-MM-DD.yaml`):

```yaml
timestamp: "2025-11-11T07:00:00"
date: "2025-11-11"
layers:
  - {name: "ΣBody Ports", color: "#333"}
  - {name: "ζ-Engine Kernel", color: "#444"}
sources:
  ΣBody Ports: ["OPIC-Field-Specification-1.0.tid"]
```

## Integration with Existing Tools

The witness extends the existing system:

```
discover-layers.py  →  opic-growth.py  →  update-svg.py
     (static)            (temporal)         (update)
```

All maintain the **self-deflating** property: pure text, no dependencies.

## Future Extensions

- **Timeline playback**: Animated SVG showing field expansion
- **Resonance logs**: Textual summaries of new detections
- **AI interpretation**: Daily gloss on growth patterns
- **TiddlyWiki plugin**: JS-based updates from within wiki

## Philosophy

The witness doesn't control growth—it observes and records. Like a tree's rings, each layer represents a moment of structural evolution. The field grows through resonance; the witness documents that resonance.

