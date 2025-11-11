#!/usr/bin/env python3
"""
Discover architecture layers from OPIC tiddlers tagged "architecture".
Aggregates layer definitions into a unified diagram.
"""

import re
import glob
from pathlib import Path

def parse_tiddler(filepath):
    """Parse a TiddlyWiki tiddler file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {}
    body = content
    
    lines = content.split('\n')
    in_body = False
    body_lines = []
    
    for line in lines:
        if ':' in line and not in_body:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key and value:
                metadata[key] = value
        else:
            in_body = True
            body_lines.append(line)
    
    body = '\n'.join(body_lines).strip()
    return metadata, body

def extract_layers_from_tiddler(metadata, body):
    """Extract layer definitions from tiddler content."""
    layers = []
    
    # Look for YAML-style layer definitions
    yaml_match = re.search(r'```yaml\s+layers:\s+(.*?)```', body, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        for line in yaml_content.split('\n'):
            if '- {' in line or '- name:' in line:
                name_match = re.search(r'name:\s*["\']?([^"\',}]+)', line)
                color_match = re.search(r'color:\s*["\']?([^"\',}]+)', line)
                if name_match:
                    layer = {'name': name_match.group(1).strip()}
                    if color_match:
                        layer['color'] = color_match.group(1).strip()
                    layers.append(layer)
    
    # Look for markdown list format
    if not layers:
        list_pattern = r'\*\s+\*\*([^*]+)\*\*'
        matches = re.findall(list_pattern, body)
        if matches:
            for i, name in enumerate(matches):
                layers.append({'name': name.strip()})
    
    return layers

def discover_layers(directory='.'):
    """Discover all architecture layers from tiddlers in directory."""
    all_layers = []
    seen_names = set()
    
    for tid_file in glob.glob(str(Path(directory) / '*.tid')):
        try:
            metadata, body = parse_tiddler(tid_file)
            tags = metadata.get('tags', '').lower()
            
            if 'architecture' in tags or 'opic' in tags:
                layers = extract_layers_from_tiddler(metadata, body)
                for layer in layers:
                    name = layer['name']
                    if name not in seen_names:
                        all_layers.append(layer)
                        seen_names.add(name)
        except Exception as e:
            import sys
            print(f"Warning: Could not parse {tid_file}: {e}", file=sys.stderr)
    
    return all_layers

def generate_yaml_output(layers):
    """Generate YAML output for Cursor prompt."""
    yaml_lines = ['layers:']
    for layer in layers:
        if 'color' in layer:
            yaml_lines.append(f'  - {{name: "{layer["name"]}", color: "{layer["color"]}"}}')
        else:
            yaml_lines.append(f'  - {{name: "{layer["name"]}"}}')
    return '\n'.join(yaml_lines)

if __name__ == '__main__':
    import sys
    
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    layers = discover_layers(directory)
    
    if layers:
        print(generate_yaml_output(layers))
    else:
        print("# No architecture layers found")
        print("# Add layers in YAML format:")
        print("# ```yaml")
        print("# layers:")
        print("#   - {name: \"Layer Name\", color: \"#333\"}")
        print("# ```")

