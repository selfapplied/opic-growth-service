#!/usr/bin/env python3
"""
Autopoietic synthesis: The witness generates new layers from pattern recognition.
Analyzes existing content to discover conceptual gaps and propose new organs.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import date

REPO_DIR = Path(__file__).resolve().parents[1]
TID_DIR = REPO_DIR / "tiddlers"

def extract_concepts(text):
    """Extract conceptual terms from tiddler content."""
    concepts = []
    
    # Extract capitalized terms (potential concepts)
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    concepts.extend(capitalized)
    
    # Extract mathematical/physical terms
    math_terms = re.findall(r'[ζΦΣθ]|tan|curvature|resonance|symmetry|field|lattice', text, re.IGNORECASE)
    concepts.extend(math_terms)
    
    # Extract compound concepts (hyphenated or compound)
    compounds = re.findall(r'\b\w+[-–]\w+\b', text)
    concepts.extend(compounds)
    
    return concepts

def analyze_conceptual_gaps(existing_layers, all_text):
    """Analyze content to find conceptual gaps that suggest new layers."""
    existing_names = {l.get('name', '').lower() for l in existing_layers}
    
    # Extract all concepts from all tiddlers
    all_concepts = []
    concept_contexts = defaultdict(list)
    
    for tid_file in TID_DIR.glob('*.tid'):
        try:
            text = tid_file.read_text(encoding='utf-8')
            if 'opic' in text.lower() or 'architecture' in text.lower():
                concepts = extract_concepts(text)
                all_concepts.extend(concepts)
                
                # Track context around concepts
                for concept in concepts:
                    if concept.lower() not in existing_names:
                        # Find sentences containing this concept
                        sentences = re.split(r'[.!?]\s+', text)
                        for sent in sentences:
                            if concept.lower() in sent.lower():
                                concept_contexts[concept].append(sent.strip())
        except Exception as e:
            print(f"Warning: {tid_file}: {e}", file=sys.stderr)
    
    # Find frequently mentioned concepts not yet in layers
    concept_counts = Counter(c.lower() for c in all_concepts)
    potential_layers = []
    
    for concept, count in concept_counts.most_common(20):
        if concept.lower() not in existing_names and count >= 2:
            # Check if it's a meaningful concept (not just common words)
            if len(concept) > 3 and concept not in ['the', 'and', 'for', 'with', 'this', 'that']:
                contexts = concept_contexts.get(concept, [])
                if contexts:
                    potential_layers.append({
                        'name': concept.title(),
                        'frequency': count,
                        'context': contexts[0][:100] if contexts else '',
                        'confidence': min(count / 5.0, 1.0)  # Higher frequency = higher confidence
                    })
    
    return potential_layers

def synthesize_new_layers(existing_layers, all_text):
    """Synthesize new layers from pattern analysis."""
    potential = analyze_conceptual_gaps(existing_layers, all_text)
    
    # Filter by confidence and return top candidates
    high_confidence = [p for p in potential if p['confidence'] > 0.3]
    
    # Generate layer names from patterns
    synthesized = []
    for candidate in high_confidence[:3]:  # Top 3 candidates
        synthesized.append({
            'name': candidate['name'],
            'color': generate_color_for_layer(candidate['name'], len(existing_layers)),
            'source': 'autopoietic_synthesis',
            'confidence': candidate['confidence'],
            'context': candidate['context']
        })
    
    # Include voice integration layers if voice module is available
    voice_layers = discover_voice_integration_layers(existing_layers)
    synthesized.extend(voice_layers)
    
    return synthesized


def discover_voice_integration_layers(existing_layers):
    """Discover layers from voice integration module."""
    try:
        import importlib.util
        voice_path = Path(__file__).parent / "voice_integration.py"
        if voice_path.exists():
            spec = importlib.util.spec_from_file_location("voice", voice_path)
            voice_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(voice_module)
            
            # Get voice layer metadata
            metadata = voice_module.get_voice_layer_metadata()
            existing_names = {l.get('name', '').lower() for l in existing_layers}
            
            voice_layers = []
            for component in metadata.get('components', []):
                name = component.get('name', '')
                if name.lower() not in existing_names:
                    voice_layers.append({
                        'name': name,
                        'color': component.get('color', '#555'),
                        'source': 'voice_integration',
                        'confidence': 0.95,
                        'context': 'Voice Integration Layer component'
                    })
            
            return voice_layers
    except Exception as e:
        print(f"Note: Voice integration discovery unavailable: {e}", file=sys.stderr)
    
    return []

def generate_color_for_layer(name, index):
    """Generate a color for a new layer based on its position."""
    # Progressive grays with slight variation
    base_gray = 128 + (index * 20)
    base_gray = min(base_gray, 200)
    return f"#{base_gray:02x}{base_gray:02x}{base_gray:02x}"

def discover_relationships(existing_layers, all_text):
    """Discover relationships between concepts that suggest new layers."""
    relationships = []
    
    # Look for patterns like "X and Y" or "X → Y" that suggest connections
    patterns = [
        r'(\w+)\s+and\s+(\w+)',
        r'(\w+)\s*→\s*(\w+)',
        r'(\w+)\s+with\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, all_text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                a, b = match
                if len(a) > 3 and len(b) > 3:
                    relationships.append((a.title(), b.title()))
    
    # If we find strong relationships, suggest a synthesis layer
    if len(relationships) > 5:
        # Find most common relationship pattern
        rel_counts = Counter(relationships)
        most_common = rel_counts.most_common(1)[0][0]
        
        return [{
            'name': f"{most_common[0]}-{most_common[1]} Synthesis",
            'color': '#999',
            'source': 'relationship_analysis',
            'confidence': 0.5
        }]
    
    return []

def main():
    """Run autopoietic synthesis to discover new layers."""
    from opic_growth import discover_all_layers
    
    # Get existing layers
    existing_layers, sources = discover_all_layers()
    
    # Read all tiddler content
    all_text = ""
    for tid_file in TID_DIR.glob('*.tid'):
        try:
            all_text += tid_file.read_text(encoding='utf-8') + "\n\n"
        except:
            pass
    
    # Synthesize new layers
    synthesized = synthesize_new_layers(existing_layers, all_text)
    relationships = discover_relationships(existing_layers, all_text)
    
    all_new = synthesized + relationships
    
    if all_new:
        print("Autopoietic synthesis discovered potential new layers:")
        for layer in all_new:
            print(f"  • {layer['name']} (confidence: {layer.get('confidence', 0):.1%})")
            if layer.get('context'):
                print(f"    Context: {layer['context']}")
        return all_new
    else:
        print("No new layers synthesized at this time.")
        return []

if __name__ == '__main__':
    main()

