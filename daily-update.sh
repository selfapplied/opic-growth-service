#!/bin/bash
# Daily autopoietic witness: runs growth detection and updates master tiddler

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run growth detection
python3 opic-growth.py . growth

# Update master tiddler SVG
python3 update-svg.py OPIC-Field-Specification-1.0.tid

# Generate growth visualizations
python3 growth-visualizer.py growth timeline
python3 growth-visualizer.py growth rings

# Commit if in git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    git add growth/ OPIC-Field-Specification-1.0.tid
    git commit -m "daily opic expansion: $(date +%Y-%m-%d)" || true
fi

echo "Daily update complete: $(date)"

