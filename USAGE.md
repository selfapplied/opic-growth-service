# OPIC Whitepaper Automation Usage

## Quick Start

### Manual SVG Generation (Cursor Prompt)

1. Open `opic-svg-generator.prompt` in Cursor
2. Provide layer definitions in YAML format
3. Cursor generates SVG and updates tiddler

### Automatic Layer Discovery

The system can automatically discover layers from multiple tiddlers:

```bash
# Discover layers from all architecture tiddlers
python3 discover-layers.py

# Update SVG in main tiddler automatically
python3 update-svg.py OPIC-Field-Specification-1.0.tid
```

### Enhanced Cursor Prompt (Auto-Discovery)

Use `opic-svg-generator-auto.prompt` for automatic discovery:

1. Cursor scans all `.tid` files
2. Extracts layers from YAML blocks
3. Generates unified diagram
4. Updates tiddler automatically

## Adding Layers to Tiddlers

Include YAML blocks in any architecture-tagged tiddler:

```tiddler
title: Architecture Component X

tags: architecture opic

type: text/vnd.tiddlywiki

!! Component Description

```yaml
layers:
  - {name: "New Layer", color: "#777"}
```

Content here...
```

The discovery tool will find and aggregate these automatically.

## Workflow Options

### Option 1: Manual (Cursor Prompt)
- Use `opic-svg-generator.prompt`
- Provide layers explicitly
- Full control over diagram

### Option 2: Semi-Automatic (Scripts)
- Add YAML blocks to tiddlers
- Run `discover-layers.py` → `update-svg.py`
- Batch updates

### Option 3: Full Auto (Enhanced Prompt)
- Use `opic-svg-generator-auto.prompt`
- Cursor handles discovery + generation
- Single-step workflow

## Integration

All tools maintain the **self-deflating** property:
- Pure text output
- No external dependencies
- Reproducible diagrams
- TiddlyWiki-ready

