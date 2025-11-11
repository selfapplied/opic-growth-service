#!/usr/bin/env python3
"""
Generate growth timeline visualization from historical snapshots.
Creates animated or sequential SVG showing field expansion over time.
"""

import json
import sys
import yaml
from pathlib import Path
from datetime import datetime

def load_all_snapshots(growth_dir='growth'):
    """Load all historical snapshots."""
    snapshots = []
    for snapshot_file in sorted(Path(growth_dir).glob('*.yaml')):
        try:
            data = yaml.safe_load(snapshot_file.read_text())
            snapshots.append({
                'date': data.get('date', snapshot_file.stem),
                'layers': data.get('layers', []),
                'count': len(data.get('layers', []))
            })
        except Exception as e:
            print(f"Warning: {snapshot_file}: {e}", file=sys.stderr)
    return snapshots

def generate_timeline_svg(snapshots, width=800, height=400):
    """Generate SVG timeline showing growth over time."""
    if not snapshots:
        return '<svg xmlns="http://www.w3.org/2000/svg"><text>No growth history</text></svg>'
    
    max_count = max(s['count'] for s in snapshots)
    padding = 40
    chart_width = width - 2 * padding
    chart_height = height - 2 * padding
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg.append('  <style>')
    svg.append('    .axis{stroke:#666;stroke-width:1}')
    svg.append('    .line{stroke:#4a9;stroke-width:2;fill:none}')
    svg.append('    .point{fill:#4a9;r:4}')
    svg.append('    .label{font:10px sans-serif;fill:#aaa}')
    svg.append('    .title{font:14px sans-serif;fill:#333}')
    svg.append('  </style>')
    
    # Title
    svg.append(f'  <text x="{width//2}" y="20" class="title" text-anchor="middle">OPIC Field Growth Timeline</text>')
    
    # Axes
    svg.append(f'  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" class="axis"/>')
    svg.append(f'  <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" class="axis"/>')
    
    # Data points
    points = []
    for i, snapshot in enumerate(snapshots):
        x = padding + (i / (len(snapshots) - 1) * chart_width) if len(snapshots) > 1 else padding + chart_width / 2
        y = height - padding - (snapshot['count'] / max_count * chart_height)
        points.append((x, y, snapshot))
    
    # Draw line
    if len(points) > 1:
        path_d = f'M {points[0][0]},{points[0][1]}'
        for x, y, _ in points[1:]:
            path_d += f' L {x},{y}'
        svg.append(f'  <path d="{path_d}" class="line"/>')
    
    # Draw points and labels
    for x, y, snapshot in points:
        svg.append(f'  <circle cx="{x}" cy="{y}" class="point"/>')
        svg.append(f'  <text x="{x}" y="{height-padding+15}" class="label" text-anchor="middle">{snapshot["date"]}</text>')
        svg.append(f'  <text x="{x}" y="{y-5}" class="label" text-anchor="middle">{snapshot["count"]}</text>')
    
    # Y-axis labels
    for i in range(0, max_count + 1, max(1, max_count // 5)):
        y = height - padding - (i / max_count * chart_height)
        svg.append(f'  <text x="{padding-10}" y="{y+3}" class="label" text-anchor="end">{i}</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def generate_growth_rings_svg(snapshots, width=400, height=400):
    """Generate concentric rings visualization (like tree rings)."""
    if not snapshots:
        return '<svg xmlns="http://www.w3.org/2000/svg"><text>No growth history</text></svg>'
    
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2 - 20
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg.append('  <style>')
    svg.append('    .ring{fill:none;stroke-width:3}')
    svg.append('    .label{font:9px sans-serif;fill:#666;text-anchor:middle}')
    svg.append('    .title{font:12px sans-serif;fill:#333;text-anchor:middle}')
    svg.append('  </style>')
    
    svg.append(f'  <text x="{center_x}" y="15" class="title">OPIC Field Growth Rings</text>')
    
    max_count = max(s['count'] for s in snapshots)
    colors = ['#333', '#444', '#555', '#666', '#777', '#888']
    
    for i, snapshot in enumerate(snapshots):
        radius = 20 + (snapshot['count'] / max_count * (max_radius - 20))
        color = colors[i % len(colors)]
        svg.append(f'  <circle cx="{center_x}" cy="{center_y}" r="{radius}" class="ring" stroke="{color}"/>')
        
        # Label on right side
        label_x = center_x + radius + 10
        label_y = center_y
        svg.append(f'  <text x="{label_x}" y="{label_y+3}" class="label">{snapshot["date"]} ({snapshot["count"]})</text>')
    
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    import sys
    
    growth_dir = sys.argv[1] if len(sys.argv) > 1 else 'growth'
    output_type = sys.argv[2] if len(sys.argv) > 2 else 'timeline'
    
    snapshots = load_all_snapshots(growth_dir)
    
    if output_type == 'rings':
        svg = generate_growth_rings_svg(snapshots)
        output_file = Path(growth_dir) / 'growth-rings.svg'
    else:
        svg = generate_timeline_svg(snapshots)
        output_file = Path(growth_dir) / 'growth-timeline.svg'
    
    output_file.write_text(svg)
    print(f"Generated: {output_file}")

if __name__ == '__main__':
    import sys
    main()

