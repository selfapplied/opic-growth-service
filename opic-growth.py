#!/usr/bin/env python3
"""
Autopoietic witness: living diagram service that tracks OPIC field growth.
Observes tiddlers, detects new conceptual organs, expands SVG accordingly.
"""

import re
import json
import sys
import yaml
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict

def discover_all_layers(directory='.'):
    """Discover layers from all OPIC tiddlers."""
    layers = []
    seen_names = set()
    sources = defaultdict(list)
    
    for tid_file in Path(directory).glob('*.tid'):
        try:
            text = tid_file.read_text(encoding='utf-8')
            
            # Check if OPIC-related
            if 'opic' in text.lower() or 'architecture' in text.lower():
                # Extract from YAML blocks
                yaml_matches = re.findall(r'```yaml\s+layers:\s+(.*?)```', text, re.DOTALL)
                for yaml_block in yaml_matches:
                    for line in yaml_block.split('\n'):
                        name_match = re.search(r'name:\s*["\']?([^"\',}]+)', line)
                        color_match = re.search(r'color:\s*["\']?([^"\',}]+)', line)
                        if name_match:
                            name = name_match.group(1).strip()
                            if name not in seen_names:
                                layer = {'name': name}
                                if color_match:
                                    layer['color'] = color_match.group(1).strip()
                                layers.append(layer)
                                seen_names.add(name)
                                sources[name].append(str(tid_file))
                
                # Extract from markdown lists
                list_matches = re.findall(r'\*\s+\*\*([^*]+)\*\*', text)
                for name in list_matches:
                    name = name.strip()
                    if name and name not in seen_names:
                        layers.append({'name': name})
                        seen_names.add(name)
                        sources[name].append(str(tid_file))
        
        except Exception as e:
            print(f"Warning: {tid_file}: {e}", file=sys.stderr)
    
    return layers, sources

def load_growth_history(growth_dir='growth'):
    """Load previous growth snapshots."""
    growth_path = Path(growth_dir)
    growth_path.mkdir(exist_ok=True)
    
    history = []
    for snapshot_file in sorted(growth_path.glob('*.yaml')):
        try:
            data = yaml.safe_load(snapshot_file.read_text())
            timestamp = snapshot_file.stem
            history.append({
                'date': timestamp,
                'layers': data.get('layers', []),
                'count': len(data.get('layers', []))
            })
        except Exception as e:
            print(f"Warning: Could not load {snapshot_file}: {e}", file=sys.stderr)
    
    return history

def compute_growth_metrics(current_layers, history):
    """Compute growth rate and delta."""
    if not history:
        return {
            'delta': len(current_layers),
            'growth_rate': 1.0,
            'new_layers': current_layers,
            'total_layers': len(current_layers)
        }
    
    prev_layers = history[-1]['layers']
    prev_names = {l.get('name') for l in prev_layers}
    curr_names = {l.get('name') for l in current_layers}
    
    new_names = curr_names - prev_names
    new_layers = [l for l in current_layers if l.get('name') in new_names]
    
    delta = len(current_layers) - len(prev_layers)
    growth_rate = delta / len(prev_layers) if prev_layers else 1.0
    
    return {
        'delta': delta,
        'growth_rate': growth_rate,
        'new_layers': new_layers,
        'total_layers': len(current_layers)
    }

def save_snapshot(layers, sources, growth_dir='growth'):
    """Save current state as timestamped snapshot."""
    growth_path = Path(growth_dir)
    growth_path.mkdir(exist_ok=True)
    
    timestamp = date.today().isoformat()
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'date': timestamp,
        'layers': layers,
        'sources': {name: list(set(srcs)) for name, srcs in sources.items()}
    }
    
    snapshot_file = growth_path / f'{timestamp}.yaml'
    snapshot_file.write_text(yaml.dump(snapshot, default_flow_style=False))
    
    # Also save JSON for easy consumption
    json_file = growth_path / f'{timestamp}.json'
    json_file.write_text(json.dumps(snapshot, indent=2))
    
    return snapshot_file

def generate_growth_report(metrics, new_layers, sources):
    """Generate human-readable growth report."""
    report = []
    report.append(f"OPIC Field Growth Report — {date.today().isoformat()}")
    report.append("=" * 50)
    report.append(f"Total layers: {metrics['total_layers']}")
    report.append(f"New layers: {metrics['delta']}")
    report.append(f"Growth rate: {metrics['growth_rate']:.2%}")
    report.append("")
    
    if new_layers:
        report.append("New conceptual organs detected:")
        for layer in new_layers:
            name = layer.get('name')
            srcs = sources.get(name, [])
            report.append(f"  • {name}")
            if srcs:
                report.append(f"    → from: {', '.join(srcs)}")
        report.append("")
    
    return '\n'.join(report)

def main():
    import sys
    
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    growth_dir = sys.argv[2] if len(sys.argv) > 2 else 'growth'
    
    # Discover current state
    layers, sources = discover_all_layers(directory)
    
    # Load history
    history = load_growth_history(growth_dir)
    
    # Compute metrics
    metrics = compute_growth_metrics(layers, history)
    
    # Save snapshot
    snapshot_file = save_snapshot(layers, sources, growth_dir)
    
    # Generate report
    report = generate_growth_report(metrics, metrics['new_layers'], sources)
    print(report)
    
    # Save report
    report_file = Path(growth_dir) / f'{date.today().isoformat()}.txt'
    report_file.write_text(report)
    
    return snapshot_file

if __name__ == '__main__':
    import sys
    main()

