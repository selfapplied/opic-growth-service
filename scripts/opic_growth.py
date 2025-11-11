#!/usr/bin/env python3
"""
Cloud-hosted OPIC Growth Service — Daily Witness Daemon
Scans tiddlers, extracts layers, records growth snapshots.
"""

import re
import json
import sys
import yaml
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict

# Cloud-friendly paths
REPO_DIR = Path(__file__).resolve().parents[1]
TID_DIR = REPO_DIR / "tiddlers"
OUT_DIR = REPO_DIR / "growth"
OUT_DIR.mkdir(exist_ok=True)

def discover_all_layers(directory=None):
    """Discover layers from all OPIC tiddlers."""
    if directory is None:
        directory = TID_DIR if TID_DIR.exists() else REPO_DIR
    
    layers = []
    seen_names = set()
    sources = defaultdict(list)
    
    search_dirs = [Path(directory)]
    if TID_DIR.exists() and TID_DIR != Path(directory):
        search_dirs.append(TID_DIR)
    
    for search_dir in search_dirs:
        for tid_file in search_dir.glob('*.tid'):
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
                                    sources[name].append(str(tid_file.relative_to(REPO_DIR)))
                    
                    # Extract from markdown lists
                    list_matches = re.findall(r'\*\s+\*\*([^*]+)\*\*', text)
                    for name in list_matches:
                        name = name.strip()
                        if name and name not in seen_names:
                            layers.append({'name': name})
                            seen_names.add(name)
                            sources[name].append(str(tid_file.relative_to(REPO_DIR)))
            
            except Exception as e:
                print(f"Warning: {tid_file}: {e}", file=sys.stderr)
    
    return layers, sources

def load_growth_history(growth_dir=None):
    """Load previous growth snapshots."""
    if growth_dir is None:
        growth_dir = OUT_DIR
    
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

def save_snapshot(layers, sources, growth_dir=None):
    """Save current state as timestamped snapshot."""
    if growth_dir is None:
        growth_dir = OUT_DIR
    
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

def synthesize_autonomous_layers(existing_layers, all_text=""):
    """Attempt autopoietic synthesis to discover new layers from patterns."""
    try:
        # Import synthesis module
        import importlib.util
        synthesis_path = Path(__file__).parent / "autopoietic_synthesis.py"
        if synthesis_path.exists():
            spec = importlib.util.spec_from_file_location("synthesis", synthesis_path)
            synthesis_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(synthesis_module)
            
            # Run synthesis
            synthesized = synthesis_module.synthesize_new_layers(existing_layers, all_text)
            relationships = synthesis_module.discover_relationships(existing_layers, all_text)
            
            return synthesized + relationships
    except Exception as e:
        print(f"Note: Autopoietic synthesis unavailable: {e}", file=sys.stderr)
    
    return []

def main():
    # Discover current state (manual/explicit layers)
    layers, sources = discover_all_layers()
    
    # Attempt autopoietic synthesis
    # Read all tiddler content for analysis
    all_text = ""
    for tid_file in TID_DIR.glob('*.tid'):
        try:
            all_text += tid_file.read_text(encoding='utf-8') + "\n\n"
        except:
            pass
    
    # Load issue-based preferences
    try:
        import importlib.util
        prefs_path = Path(__file__).parent / "issue_preferences.py"
        if prefs_path.exists():
            spec = importlib.util.spec_from_file_location("prefs", prefs_path)
            prefs_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(prefs_module)
            
            preferences = prefs_module.parse_issue_preferences()
            if preferences:
                prefs_report = prefs_module.generate_preference_report(preferences)
                if prefs_report:
                    print(prefs_report, file=sys.stderr)
                    print("", file=sys.stderr)
    except Exception as e:
        preferences = []
        print(f"Note: Issue preferences unavailable: {e}", file=sys.stderr)
    
    # Synthesize new layers from patterns
    synthesized = synthesize_autonomous_layers(layers, all_text)
    
    # Apply preferences to boost matching concepts
    if preferences:
        synthesized = prefs_module.apply_preferences_to_synthesis(synthesized, preferences)
    
    # Add synthesized layers if confidence is high enough
    for synth_layer in synthesized:
        confidence_threshold = 0.4
        # Lower threshold if preference-matched
        if synth_layer.get('preference_match'):
            confidence_threshold = 0.3
        
        if synth_layer.get('confidence', 0) > confidence_threshold:
            layer_name = synth_layer['name']
            if layer_name not in {l.get('name') for l in layers}:
                layers.append({
                    'name': layer_name,
                    'color': synth_layer.get('color', '#999'),
                    'source': 'autopoietic_synthesis',
                    'confidence': synth_layer.get('confidence', 0.5)
                })
                sources[layer_name] = ['autopoietic_synthesis']
                print(f"[Autopoietic] Synthesized new layer: {layer_name} (confidence: {synth_layer.get('confidence', 0):.1%})", file=sys.stderr)
    
    # Load history
    history = load_growth_history()
    
    # Compute metrics
    metrics = compute_growth_metrics(layers, history)
    
    # Save snapshot
    snapshot_file = save_snapshot(layers, sources)
    
    # Generate report
    report = generate_growth_report(metrics, metrics['new_layers'], sources)
    print(report)
    
    # Save report
    report_file = OUT_DIR / f'{date.today().isoformat()}.txt'
    report_file.write_text(report)
    
    print(f"[✓] Updated growth log: {snapshot_file}")
    return snapshot_file

if __name__ == '__main__':
    main()

