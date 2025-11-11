#!/usr/bin/env python3
"""
Generate SVG architecture diagram for OPIC Field Specification.
Cloud-ready standalone version.
"""

def generate_architecture_svg(layers=None, width=420, height=260, layer_height=40, layer_gap=15):
    """Generate SVG diagram from layer metadata."""
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

if __name__ == '__main__':
    print(generate_architecture_svg())

