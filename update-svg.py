#!/usr/bin/env python3
"""
Update SVG diagram in OPIC tiddler using discovered layers.
Reads layers from architecture tiddlers and regenerates the SVG.
"""

import sys
import re
from pathlib import Path

# Import functions from local modules
import importlib.util
spec = importlib.util.spec_from_file_location("generate_svg", Path(__file__).parent / "generate-svg.py")
generate_svg_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_svg_module)

spec2 = importlib.util.spec_from_file_location("discover_layers", Path(__file__).parent / "discover-layers.py")
discover_layers_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(discover_layers_module)

generate_architecture_svg = generate_svg_module.generate_architecture_svg
discover_layers = discover_layers_module.discover_layers

def update_tiddler_svg(tiddler_path, layers=None):
    """Update the SVG section in a tiddler file."""
    if layers is None:
        layers = discover_layers(str(Path(tiddler_path).parent))
    
    if not layers:
        print("No layers found. Using default layers.", file=sys.stderr)
        layers = [
            {"name": "ΣBody Ports", "color": "#333"},
            {"name": "ζ-Engine Kernel", "color": "#444"},
            {"name": "Φ-Ledger (Ethics + Consensus)", "color": "#555"},
            {"name": "ΣLink Bus (Network Resonance)", "color": "#666"},
        ]
    
    with open(tiddler_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Architecture Diagram section
    pattern = r'(!! Architecture Diagram\n\n)(<svg.*?</svg>)(\n\n!!)'
    
    new_svg = generate_architecture_svg(layers)
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, r'\1' + new_svg + r'\3', content, flags=re.DOTALL)
    else:
        # If pattern not found, try to insert after Architecture Diagram heading
        pattern2 = r'(!! Architecture Diagram\n\n)'
        if re.search(pattern2, content):
            content = re.sub(pattern2, r'\1' + new_svg + '\n\n', content)
        else:
            print("Warning: Could not find Architecture Diagram section", file=sys.stderr)
            return False
    
    with open(tiddler_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == '__main__':
    tiddler_path = sys.argv[1] if len(sys.argv) > 1 else 'OPIC-Field-Specification-1.0.tid'
    
    if update_tiddler_svg(tiddler_path):
        print(f"Updated SVG in {tiddler_path}")
    else:
        sys.exit(1)

