#!/usr/bin/env python3
"""
Update SVG diagram in OPIC tiddler using discovered layers.
Cloud-ready version for GitHub Actions.
"""

import sys
import re
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]

# Import generate_svg from parent directory or local
def load_generate_svg():
    """Load SVG generator function."""
    # Try local first
    local_svg = REPO_DIR / "scripts" / "generate_svg.py"
    if local_svg.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("generate_svg", local_svg)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.generate_architecture_svg
    
    # Fallback to inline
    def generate_architecture_svg(layers=None, width=420, height=260, layer_height=40, layer_gap=15):
        if layers is None:
            layers = [
                {"name": "ΣBody Ports", "color": "#333"},
                {"name": "ζ-Engine Kernel", "color": "#444"},
                {"name": "Φ-Ledger (Ethics + Consensus)", "color": "#555"},
                {"name": "ΣLink Bus (Network Resonance)", "color": "#666"},
            ]
        
        center_x = width // 2
        start_y = 15
        
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
        svg.append('  <style>')
        svg.append('    .lbl{font:10px sans-serif;fill:#fff;text-anchor:middle}')
        svg.append('    .box{rx:10;ry:10;stroke:#222;stroke-width:1.2;fill:#333}')
        svg.append('  </style>')
        
        y = start_y
        base_width = 200
        width_step = 40
        
        for i, layer in enumerate(layers):
            layer_width = base_width + (i * width_step)
            x = center_x - layer_width // 2
            fill = layer.get("color") or layer.get("fill", "#333")
            svg.append(f'  <rect x="{x}" y="{y}" width="{layer_width}" height="{layer_height}" class="box" fill="{fill}"/>')
            text_y = y + layer_height // 2 + 5
            svg.append(f'  <text x="{center_x}" y="{text_y}" class="lbl">{layer["name"]}</text>')
            y += layer_height + layer_gap
        
        arrow_y = y
        arrow_end_y = min(arrow_y + 25, height - 10)
        svg.append(f'  <path d="M{center_x} {arrow_y}v{arrow_end_y - arrow_y}" stroke="#777" stroke-width="2" marker-end="url(#arrow)"/>')
        svg.append('  <defs>')
        svg.append('    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">')
        svg.append('      <path d="M 0 0 L 10 5 L 0 10 z" fill="#777"/>')
        svg.append('    </marker>')
        svg.append('  </defs>')
        label_y = min(arrow_end_y + 5, height - 5)
        svg.append(f'  <text x="{center_x}" y="{label_y}" font-size="9" fill="#aaa" text-anchor="middle">Reversible Flow (> < =)</text>')
        svg.append('</svg>')
        
        return '\n'.join(svg)
    
    return generate_architecture_svg

def load_layers_from_growth():
    """Load layers from today's growth snapshot."""
    import yaml
    from datetime import date
    
    growth_file = REPO_DIR / "growth" / f"{date.today().isoformat()}.yaml"
    if growth_file.exists():
        data = yaml.safe_load(growth_file.read_text())
        return data.get('layers', [])
    return None

def update_tiddler_svg(tiddler_path, layers=None):
    """Update the SVG section in a tiddler file."""
    generate_svg = load_generate_svg()
    
    if layers is None:
        layers = load_layers_from_growth()
    
    if not layers:
        print("No layers found. Using default layers.", file=sys.stderr)
        layers = [
            {"name": "ΣBody Ports", "color": "#333"},
            {"name": "ζ-Engine Kernel", "color": "#444"},
            {"name": "Φ-Ledger (Ethics + Consensus)", "color": "#555"},
            {"name": "ΣLink Bus (Network Resonance)", "color": "#666"},
        ]
    
    tiddler_file = Path(tiddler_path)
    if not tiddler_file.is_absolute():
        tiddler_file = REPO_DIR / tiddler_path
    
    with open(tiddler_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Architecture Diagram section
    pattern = r'(!! Architecture Diagram\n\n)(<svg.*?</svg>)(\n\n!!)'
    
    new_svg = generate_svg(layers)
    
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
    
    with open(tiddler_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == '__main__':
    tiddler_path = sys.argv[1] if len(sys.argv) > 1 else 'tiddlers/OPIC-Field-Specification-1.0.tid'
    
    if update_tiddler_svg(tiddler_path):
        print(f"Updated SVG in {tiddler_path}")
    else:
        sys.exit(1)

