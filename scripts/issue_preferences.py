#!/usr/bin/env python3
"""
Issue-based preferences: Read GitHub issues to guide autopoietic synthesis.
Allows human intention to guide autonomous growth.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

REPO_DIR = Path(__file__).resolve().parents[1]

def parse_issue_preferences():
    """Parse GitHub issues for OPIC growth preferences."""
    try:
        import subprocess
        import json
        
        # Fetch issues with label "opic-growth" or "field-priority"
        result = subprocess.run(
            ['gh', 'issue', 'list', '--label', 'opic-growth,field-priority', '--json', 'number,title,body,labels'],
            capture_output=True,
            text=True,
            cwd=REPO_DIR
        )
        
        if result.returncode != 0:
            # Fallback: try reading from local file if gh CLI unavailable
            return read_local_preferences()
        
        issues = json.loads(result.stdout)
        preferences = []
        
        for issue in issues:
            # Extract key concepts from issue title and body
            text = f"{issue.get('title', '')} {issue.get('body', '')}"
            
            # Look for explicit layer requests
            layer_patterns = [
                r'layer[:\s]+["\']?([^"\'\n]+)["\']?',
                r'concept[:\s]+["\']?([^"\'\n]+)["\']?',
                r'organ[:\s]+["\']?([^"\'\n]+)["\']?',
                r'add[:\s]+["\']?([^"\'\n]+)["\']?',
                r'priority[:\s]+["\']?([^"\'\n]+)["\']?',
            ]
            
            for pattern in layer_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    match = match.strip()
                    if len(match) > 2:
                        preferences.append({
                            'concept': match,
                            'priority': calculate_priority(issue),
                            'source': f"issue #{issue.get('number')}",
                            'title': issue.get('title', ''),
                            'labels': [l.get('name') for l in issue.get('labels', [])]
                        })
            
            # Also extract capitalized terms as potential concepts
            capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            for term in capitalized[:5]:  # Limit to top 5 per issue
                if len(term) > 3:
                    preferences.append({
                        'concept': term,
                        'priority': calculate_priority(issue) * 0.7,  # Lower weight for inferred
                        'source': f"issue #{issue.get('number')}",
                        'title': issue.get('title', ''),
                        'labels': [l.get('name') for l in issue.get('labels', [])]
                    })
        
        return preferences
    
    except Exception as e:
        print(f"Note: Issue preferences unavailable: {e}", file=sys.stderr)
        return read_local_preferences()

def calculate_priority(issue):
    """Calculate priority based on issue labels and state."""
    priority = 1.0
    
    labels = [l.get('name', '').lower() for l in issue.get('labels', [])]
    
    # Higher priority for certain labels
    if 'priority' in labels or 'high-priority' in labels:
        priority *= 2.0
    if 'field-priority' in labels:
        priority *= 1.5
    if 'urgent' in labels:
        priority *= 1.8
    
    return priority

def read_local_preferences():
    """Fallback: read preferences from local file."""
    prefs_file = REPO_DIR / "PREFERENCES.md"
    if prefs_file.exists():
        text = prefs_file.read_text()
        preferences = []
        
        # Extract concepts from markdown
        for line in text.split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('*'):
                concept = re.sub(r'^[-*]\s*', '', line.strip())
                if len(concept) > 2:
                    preferences.append({
                        'concept': concept,
                        'priority': 1.0,
                        'source': 'PREFERENCES.md',
                        'title': 'Local preferences',
                        'labels': []
                    })
        
        return preferences
    
    return []

def apply_preferences_to_synthesis(synthesized_layers, preferences):
    """Boost confidence of synthesized layers that match preferences."""
    if not preferences:
        return synthesized_layers
    
    # Create concept map from preferences
    pref_concepts = {}
    for pref in preferences:
        concept_lower = pref['concept'].lower()
        if concept_lower not in pref_concepts:
            pref_concepts[concept_lower] = []
        pref_concepts[concept_lower].append(pref)
    
    # Boost matching layers
    for layer in synthesized_layers:
        layer_name_lower = layer.get('name', '').lower()
        
        # Check for exact or partial matches
        for pref_concept, prefs in pref_concepts.items():
            if pref_concept in layer_name_lower or layer_name_lower in pref_concept:
                # Boost confidence based on priority
                max_priority = max(p.get('priority', 1.0) for p in prefs)
                layer['confidence'] = min(layer.get('confidence', 0.5) * max_priority, 1.0)
                layer['preference_match'] = True
                layer['preference_source'] = prefs[0].get('source', 'issue')
                break
    
    return synthesized_layers

def generate_preference_report(preferences):
    """Generate report of active preferences."""
    if not preferences:
        return None
    
    report = []
    report.append("Active Growth Preferences:")
    report.append("=" * 50)
    
    # Group by source
    by_source = defaultdict(list)
    for pref in preferences:
        by_source[pref['source']].append(pref)
    
    for source, prefs in by_source.items():
        report.append(f"\n{source}:")
        for pref in prefs:
            priority_str = "🔴" if pref['priority'] > 1.5 else "🟡" if pref['priority'] > 1.0 else "🟢"
            report.append(f"  {priority_str} {pref['concept']} (priority: {pref['priority']:.1f}x)")
            if pref.get('title'):
                report.append(f"     → {pref['title']}")
    
    return '\n'.join(report)

def main():
    """Test issue preference parsing."""
    preferences = parse_issue_preferences()
    
    if preferences:
        report = generate_preference_report(preferences)
        print(report)
        print(f"\nFound {len(preferences)} preference concepts")
    else:
        print("No preferences found. Create GitHub issues with label 'opic-growth' to guide synthesis.")
        print("\nExample issue:")
        print("  Title: Add Resonance Field Layer")
        print("  Labels: opic-growth, field-priority")
        print("  Body: We need a layer that measures harmonic resonance patterns.")

if __name__ == '__main__':
    main()

