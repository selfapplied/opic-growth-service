#!/usr/bin/env python3
"""
Generate AI-powered interpretive gloss for daily OPIC growth.
Optional enhancement that adds poetic/philosophical commentary.
"""

import sys
import yaml
import json
from pathlib import Path
from datetime import date

REPO_DIR = Path(__file__).resolve().parents[1]

def generate_gloss_manual(snapshot_data):
    """Generate a simple gloss without AI."""
    layers = snapshot_data.get('layers', [])
    layer_names = [l.get('name', '') for l in layers]
    count = len(layers)
    
    glosses = [
        f"Today the OPIC field resonates with {count} conceptual organs.",
        f"The witness observes {count} harmonic layers in the field.",
        f"{count} structural elements form today's resonance pattern.",
        f"The field expands: {count} layers detected by the witness.",
    ]
    
    # Simple rotation based on date
    day = date.today().day
    return glosses[day % len(glosses)]

def generate_gloss_openai(snapshot_data, api_key=None):
    """Generate gloss using OpenAI API."""
    try:
        import requests
        
        if not api_key:
            api_key = sys.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            return generate_gloss_manual(snapshot_data)
        
        layers = snapshot_data.get('layers', [])
        layer_names = [l.get('name', '') for l in layers]
        
        prompt = f"""Write a one-sentence poetic reflection on today's OPIC field growth.
        
Today's layers: {', '.join(layer_names[:5])}
Total: {len(layers)} layers

Write in the style of a witness observing structural evolution. Be concise and resonant."""
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'gpt-4',
                'messages': [
                    {'role': 'system', 'content': 'You are a witness observing the growth of a mathematical-philosophical field. Write concise, resonant reflections.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 100,
                'temperature': 0.8,
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return generate_gloss_manual(snapshot_data)
    
    except Exception as e:
        print(f"Warning: AI gloss generation failed: {e}", file=sys.stderr)
        return generate_gloss_manual(snapshot_data)

def main():
    snapshot_file = sys.argv[1] if len(sys.argv) > 1 else f"growth/{date.today().isoformat()}.yaml"
    
    snapshot_path = Path(snapshot_file)
    if not snapshot_path.is_absolute():
        snapshot_path = REPO_DIR / snapshot_path
    
    if not snapshot_path.exists():
        print(f"Error: Snapshot file not found: {snapshot_path}", file=sys.stderr)
        sys.exit(1)
    
    snapshot_data = yaml.safe_load(snapshot_path.read_text())
    
    # Try AI first, fallback to manual
    use_ai = sys.argv[2] == '--ai' if len(sys.argv) > 2 else True
    api_key = sys.environ.get('OPENAI_API_KEY')
    
    if use_ai and api_key:
        gloss = generate_gloss_openai(snapshot_data, api_key)
    else:
        gloss = generate_gloss_manual(snapshot_data)
    
    # Save to growth log
    gloss_file = REPO_DIR / "growth" / f"{date.today().isoformat()}-gloss.txt"
    gloss_file.write_text(gloss)
    
    # Also append to master growth log
    growth_log = REPO_DIR / "GROWTH.md"
    if not growth_log.exists():
        growth_log.write_text("# OPIC Field Growth Log\n\n")
    
    with open(growth_log, 'a') as f:
        f.write(f"\n## {date.today().isoformat()}\n\n{gloss}\n")
    
    print(gloss)
    print(f"\n[✓] Saved gloss to {gloss_file}")

if __name__ == '__main__':
    main()

