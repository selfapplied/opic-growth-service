# How the OPIC Field Grows

## Autopoietic Growth

The OPIC field now grows **autonomously** through pattern recognition and conceptual synthesis. The witness analyzes existing content to discover new conceptual organs without manual intervention.

### Autonomous Synthesis

The system:
1. **Analyzes** all tiddler content for patterns
2. **Extracts** frequently mentioned concepts
3. **Identifies** conceptual gaps
4. **Synthesizes** new layers from patterns
5. **Grows** the field automatically

### Manual Growth

You can still trigger growth manually by adding tiddlers (see below).

## What Triggers Growth?

The autopoietic witness detects new **conceptual organs** (layers) in two ways:

### 1. **New Tiddlers**
Add new `.tid` files to `tiddlers/` that contain:
- The word "opic" or "architecture" in the content
- Layer definitions (see formats below)

### 2. **Updated Tiddlers**
Modify existing tiddlers to add new layer definitions.

## Layer Definition Formats

The witness recognizes layers in two formats:

### Format 1: YAML Blocks
```tiddler
title: New Component

tags: architecture opic

```yaml
layers:
  - {name: "New Layer Name", color: "#777"}
```
```

### Format 2: Markdown Lists
```tiddler
!! Architecture Components

* **New Layer Name** – description
```

The witness extracts anything in `**bold**` from markdown lists.

## Example: Adding a New Layer

Let's add a new layer to demonstrate growth:

```bash
# Create a new tiddler
cat > tiddlers/New-Component.tid << 'EOF'
title: New Component

tags: architecture opic

type: text/vnd.tiddlywiki

!! Component Description

```yaml
layers:
  - {name: "Resonance Field", color: "#888"}
```

This component adds a new resonance layer to the field.
EOF
```

Then commit and push:
```bash
git add tiddlers/New-Component.tid
git commit -m "Add new resonance layer"
git push
```

On the next workflow run, the witness will:
1. Detect the new "Resonance Field" layer
2. Add it to the growth snapshot
3. Update the master SVG diagram
4. Generate new visualizations
5. Commit everything automatically

## Current Detection Logic

The witness scans all `.tid` files and:
- Checks if content contains "opic" or "architecture"
- Extracts YAML layer definitions
- Extracts markdown list items with `**bold**` names
- Deduplicates by layer name
- Records source tiddler for each layer

## Growth Metrics

When new layers are detected:
- **Delta:** Number of new layers since last snapshot
- **Growth Rate:** `delta / previous_count`
- **Total Layers:** Current count
- **New Layers:** List of newly detected organs

## Making It Grow

To trigger growth, you can:

1. **Add a new tiddler** with layer definitions
2. **Update existing tiddler** with new layers
3. **Use either format** (YAML or markdown)
4. **Commit and push** to repository
5. **Wait for next run** (or trigger manually)

The witness will discover and document the growth automatically.

