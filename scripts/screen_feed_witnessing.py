#!/usr/bin/env python3
"""
Screen Feed Witnessing Layer: Live UX paradigm learning through visual observation.
Provides screen capture, UI element recognition, interaction pattern detection, and feedback coupling.
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field


REPO_DIR = Path(__file__).resolve().parents[1]


@dataclass
class UIElement:
    """Represents a recognized UI element."""
    element_id: str
    element_type: str  # button, input, menu, window, dialog, etc.
    position: Tuple[int, int]  # (x, y)
    size: Tuple[int, int]  # (width, height)
    text: str = ""
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'element_id': self.element_id,
            'element_type': self.element_type,
            'position': self.position,
            'size': self.size,
            'text': self.text,
            'metadata': self.metadata
        }


@dataclass
class InteractionPattern:
    """Represents a detected user interaction pattern."""
    pattern_id: str
    pattern_type: str  # click, drag, scroll, type, gesture
    timestamp: str
    ui_element: Optional[UIElement] = None
    confidence: float = 0.0
    context: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type,
            'timestamp': self.timestamp,
            'ui_element': self.ui_element.to_dict() if self.ui_element else None,
            'confidence': self.confidence,
            'context': self.context
        }


@dataclass
class UXParadigm:
    """Represents a learned UX paradigm or design pattern."""
    paradigm_id: str
    paradigm_name: str
    description: str
    occurrences: int = 0
    confidence: float = 0.0
    examples: list = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'paradigm_id': self.paradigm_id,
            'paradigm_name': self.paradigm_name,
            'description': self.description,
            'occurrences': self.occurrences,
            'confidence': self.confidence,
            'examples': self.examples
        }


class ScreenCapture:
    """Captures and processes screen state for observation."""
    
    def __init__(self):
        self.capture_history = []
        self.capture_count = 0
        self.capture_interval = 1.0  # seconds
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> dict:
        """
        Capture screen or screen region.
        
        Args:
            region: Optional (x, y, width, height) tuple for partial capture
        
        Returns:
            Dictionary with capture metadata and status
        
        In a full implementation, this would use screen capture APIs.
        For now, provides a structured interface for screen observation.
        """
        capture = {
            'capture_id': f"cap_{self.capture_count}",
            'timestamp': datetime.now().isoformat(),
            'region': region,
            'full_screen': region is None,
            'status': 'captured',
            'resolution': (1920, 1080) if region is None else (region[2], region[3])
        }
        
        self.capture_count += 1
        self.capture_history.append(capture)
        
        return capture
    
    def set_capture_interval(self, seconds: float) -> None:
        """Set the interval between automatic captures."""
        self.capture_interval = max(0.1, min(60.0, seconds))
    
    def get_capture_stats(self) -> dict:
        """Get statistics on screen captures."""
        return {
            'total_captures': self.capture_count,
            'history_size': len(self.capture_history),
            'capture_interval': self.capture_interval
        }


class UIElementRecognizer:
    """Recognizes and classifies UI elements from screen captures."""
    
    # Common UI element patterns based on visual characteristics
    ELEMENT_TYPES = [
        'button', 'input', 'text', 'image', 'menu', 'toolbar', 
        'window', 'dialog', 'tab', 'list', 'dropdown', 'checkbox',
        'radio', 'slider', 'scrollbar', 'icon', 'link', 'label'
    ]
    
    def __init__(self):
        self.recognized_elements = []
        self.element_cache = {}
        self.recognition_count = 0
    
    def recognize_elements(self, screen_data: dict) -> List[UIElement]:
        """
        Recognize UI elements from screen capture data.
        
        In a full implementation, this would use computer vision and OCR.
        For now, provides a structured interface for UI recognition.
        """
        elements = []
        
        # Simulate element recognition
        # In real implementation, would analyze screen_data pixel data
        capture_id = screen_data.get('capture_id', 'unknown')
        
        # Cache check
        if capture_id in self.element_cache:
            return self.element_cache[capture_id]
        
        self.recognition_count += 1
        
        # Cache the results
        self.element_cache[capture_id] = elements
        self.recognized_elements.extend(elements)
        
        return elements
    
    def classify_element(self, visual_features: dict) -> str:
        """
        Classify UI element type based on visual features.
        
        Args:
            visual_features: Dictionary containing visual properties
                            (color, shape, size, text, etc.)
        
        Returns:
            Element type classification
        """
        # Simple heuristic-based classification
        # Real implementation would use ML models
        
        if 'has_text_input' in visual_features and visual_features['has_text_input']:
            return 'input'
        
        if 'is_clickable' in visual_features and visual_features['is_clickable']:
            if visual_features.get('has_border', False):
                return 'button'
            return 'link'
        
        if 'is_container' in visual_features and visual_features['is_container']:
            return 'window' if visual_features.get('has_titlebar', False) else 'panel'
        
        return 'unknown'
    
    def get_recognition_stats(self) -> dict:
        """Get statistics on element recognition."""
        element_types = defaultdict(int)
        for element in self.recognized_elements:
            element_types[element.element_type] += 1
        
        return {
            'total_recognized': len(self.recognized_elements),
            'unique_captures': self.recognition_count,
            'by_type': dict(element_types)
        }


class InteractionPatternDetector:
    """Detects and analyzes user interaction patterns."""
    
    # Common interaction patterns
    INTERACTION_TYPES = [
        'click', 'double_click', 'right_click', 'drag', 'drop',
        'scroll', 'type', 'hover', 'gesture', 'key_combo', 'swipe'
    ]
    
    def __init__(self):
        self.detected_patterns = []
        self.pattern_sequences = []
        self.pattern_counts = defaultdict(int)
    
    def detect_interaction(self, event_type: str, ui_element: Optional[UIElement] = None,
                          metadata: Optional[dict] = None) -> InteractionPattern:
        """
        Detect and record an interaction pattern.
        
        Args:
            event_type: Type of interaction (click, scroll, type, etc.)
            ui_element: Optional UI element involved in interaction
            metadata: Additional context about the interaction
        
        Returns:
            InteractionPattern object
        """
        pattern_id = f"int_{len(self.detected_patterns)}"
        timestamp = datetime.now().isoformat()
        
        pattern = InteractionPattern(
            pattern_id=pattern_id,
            pattern_type=event_type,
            timestamp=timestamp,
            ui_element=ui_element,
            confidence=0.9,
            context=metadata or {}
        )
        
        self.detected_patterns.append(pattern)
        self.pattern_counts[event_type] += 1
        
        return pattern
    
    def analyze_pattern_sequence(self, patterns: List[InteractionPattern]) -> dict:
        """
        Analyze a sequence of interaction patterns to identify workflows.
        
        Args:
            patterns: List of interaction patterns to analyze
        
        Returns:
            Analysis results including common sequences and workflows
        """
        if not patterns:
            return {'sequences': [], 'common_workflows': []}
        
        # Build sequence representation
        sequence = [p.pattern_type for p in patterns]
        
        # Detect common subsequences (simplified)
        analysis = {
            'sequence_length': len(sequence),
            'unique_interactions': len(set(sequence)),
            'pattern_types': list(set(sequence)),
            'timestamp_range': (patterns[0].timestamp, patterns[-1].timestamp)
        }
        
        self.pattern_sequences.append(analysis)
        
        return analysis
    
    def get_pattern_statistics(self) -> dict:
        """Get statistics on detected interaction patterns."""
        return {
            'total_patterns': len(self.detected_patterns),
            'by_type': dict(self.pattern_counts),
            'sequences_analyzed': len(self.pattern_sequences)
        }
    
    def get_most_common_interactions(self, n: int = 5) -> List[Tuple[str, int]]:
        """Get the most common interaction types."""
        sorted_patterns = sorted(
            self.pattern_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_patterns[:n]


class UXParadigmExtractor:
    """Extracts and learns UX paradigms from observed interactions."""
    
    # Known UX paradigms to recognize
    KNOWN_PARADIGMS = {
        'drag_and_drop': {
            'name': 'Drag and Drop',
            'description': 'Direct manipulation through dragging objects',
            'pattern': ['click', 'drag', 'drop']
        },
        'context_menu': {
            'name': 'Context Menu',
            'description': 'Right-click menu for contextual actions',
            'pattern': ['right_click', 'click']
        },
        'keyboard_shortcuts': {
            'name': 'Keyboard Shortcuts',
            'description': 'Key combinations for quick actions',
            'pattern': ['key_combo']
        },
        'hover_preview': {
            'name': 'Hover Preview',
            'description': 'Information displayed on mouse hover',
            'pattern': ['hover']
        },
        'scroll_navigation': {
            'name': 'Scroll Navigation',
            'description': 'Continuous scrolling for content browsing',
            'pattern': ['scroll']
        }
    }
    
    def __init__(self):
        self.learned_paradigms = {}
        self.paradigm_occurrences = defaultdict(int)
    
    def extract_paradigm(self, interaction_sequence: List[InteractionPattern]) -> Optional[UXParadigm]:
        """
        Extract UX paradigm from interaction sequence.
        
        Args:
            interaction_sequence: Sequence of user interactions
        
        Returns:
            UXParadigm if pattern matches known paradigm, None otherwise
        """
        if not interaction_sequence:
            return None
        
        # Get pattern types from sequence
        pattern_types = [p.pattern_type for p in interaction_sequence]
        
        # Check against known paradigms
        for paradigm_key, paradigm_def in self.KNOWN_PARADIGMS.items():
            if self._matches_pattern(pattern_types, paradigm_def['pattern']):
                # Found matching paradigm
                self.paradigm_occurrences[paradigm_key] += 1
                
                if paradigm_key not in self.learned_paradigms:
                    paradigm = UXParadigm(
                        paradigm_id=paradigm_key,
                        paradigm_name=paradigm_def['name'],
                        description=paradigm_def['description'],
                        occurrences=1,
                        confidence=0.7,
                        examples=[interaction_sequence[0].to_dict()]
                    )
                    self.learned_paradigms[paradigm_key] = paradigm
                else:
                    paradigm = self.learned_paradigms[paradigm_key]
                    paradigm.occurrences += 1
                    paradigm.confidence = min(0.99, paradigm.confidence + 0.05)
                    if len(paradigm.examples) < 10:
                        paradigm.examples.append(interaction_sequence[0].to_dict())
                
                return self.learned_paradigms[paradigm_key]
        
        return None
    
    def _matches_pattern(self, observed: List[str], expected: List[str]) -> bool:
        """Check if observed pattern matches expected pattern."""
        if len(observed) < len(expected):
            return False
        
        # Simple subsequence matching
        for i in range(len(observed) - len(expected) + 1):
            if observed[i:i+len(expected)] == expected:
                return True
        
        return False
    
    def get_paradigm_summary(self) -> dict:
        """Get summary of learned UX paradigms."""
        return {
            'total_paradigms': len(self.learned_paradigms),
            'paradigm_list': list(self.learned_paradigms.keys()),
            'occurrences': dict(self.paradigm_occurrences)
        }
    
    def get_top_paradigms(self, n: int = 5) -> List[UXParadigm]:
        """Get most commonly used UX paradigms."""
        sorted_paradigms = sorted(
            self.learned_paradigms.values(),
            key=lambda p: p.occurrences,
            reverse=True
        )
        return sorted_paradigms[:n]


class OSEvolutionController:
    """
    Controls personalized OS evolution based on observed patterns.
    Implements piecewise computing for gradual adaptation.
    """
    
    def __init__(self):
        self.adaptations = []
        self.evolution_state = {
            'version': '1.0.0',
            'total_adaptations': 0,
            'learning_rate': 0.01,
            'evolution_delta': 0.0,
            'active_adaptations': []
        }
        self.adaptation_history = []
    
    def propose_adaptation(self, paradigm: UXParadigm, 
                          interaction_data: dict) -> dict:
        """
        Propose an OS adaptation based on learned UX paradigm.
        
        Args:
            paradigm: The UX paradigm to adapt to
            interaction_data: Context about user interactions
        
        Returns:
            Proposed adaptation details
        """
        adaptation = {
            'adaptation_id': f"adapt_{len(self.adaptations)}",
            'timestamp': datetime.now().isoformat(),
            'paradigm': paradigm.paradigm_name,
            'type': 'ui_enhancement',
            'description': f"Adapt system to support {paradigm.paradigm_name}",
            'confidence': paradigm.confidence,
            'evolution_delta': self._calculate_delta(paradigm),
            'status': 'proposed'
        }
        
        self.adaptations.append(adaptation)
        
        return adaptation
    
    def apply_adaptation(self, adaptation_id: str) -> bool:
        """
        Apply a proposed adaptation in piecewise manner.
        
        Args:
            adaptation_id: ID of adaptation to apply
        
        Returns:
            True if successful, False otherwise
        """
        adaptation = None
        for adapt in self.adaptations:
            if adapt['adaptation_id'] == adaptation_id:
                adaptation = adapt
                break
        
        if not adaptation:
            return False
        
        if adaptation['status'] != 'proposed':
            return False
        
        # Apply the adaptation (piecewise)
        adaptation['status'] = 'applied'
        adaptation['applied_at'] = datetime.now().isoformat()
        
        # Update evolution state
        self.evolution_state['total_adaptations'] += 1
        self.evolution_state['evolution_delta'] += adaptation['evolution_delta']
        self.evolution_state['active_adaptations'].append(adaptation_id)
        
        # Record in history
        self.adaptation_history.append({
            'adaptation_id': adaptation_id,
            'timestamp': adaptation['applied_at'],
            'delta': adaptation['evolution_delta']
        })
        
        return True
    
    def _calculate_delta(self, paradigm: UXParadigm) -> float:
        """Calculate evolution delta for paradigm adaptation."""
        base_delta = self.evolution_state['learning_rate']
        
        # Scale by paradigm confidence and usage
        delta = base_delta * paradigm.confidence * (paradigm.occurrences / 10.0)
        
        return min(delta, 0.1)  # Cap at 0.1 for safety
    
    def get_evolution_state(self) -> dict:
        """Get current evolution state."""
        return self.evolution_state.copy()
    
    def get_adaptation_summary(self) -> dict:
        """Get summary of adaptations."""
        proposed = sum(1 for a in self.adaptations if a['status'] == 'proposed')
        applied = sum(1 for a in self.adaptations if a['status'] == 'applied')
        
        return {
            'total': len(self.adaptations),
            'proposed': proposed,
            'applied': applied,
            'cumulative_delta': self.evolution_state['evolution_delta']
        }


class ScreenFeedWitnessingLayer:
    """
    Main integration layer combining all screen witnessing components.
    Provides unified interface for screen-based UX paradigm learning.
    """
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.ui_recognizer = UIElementRecognizer()
        self.pattern_detector = InteractionPatternDetector()
        self.paradigm_extractor = UXParadigmExtractor()
        self.evolution_controller = OSEvolutionController()
        
        self.session_id = f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.witnessing_log = []
        self.privacy_consent = False
    
    def set_privacy_consent(self, consent: bool) -> None:
        """Set user privacy consent for screen witnessing."""
        self.privacy_consent = consent
    
    def witness_interaction(self, event_type: str, 
                          screen_region: Optional[Tuple[int, int, int, int]] = None,
                          metadata: Optional[dict] = None) -> dict:
        """
        Witness and process a user interaction.
        
        Complete pipeline:
        1. Capture screen state
        2. Recognize UI elements
        3. Detect interaction pattern
        4. Extract UX paradigm
        5. Propose OS adaptation
        
        Args:
            event_type: Type of interaction (click, scroll, etc.)
            screen_region: Optional region to capture
            metadata: Additional context
        
        Returns:
            Complete witnessing result
        """
        if not self.privacy_consent:
            return {
                'status': 'denied',
                'message': 'Privacy consent required for screen witnessing'
            }
        
        result = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Stage 1: Screen capture
        capture = self.screen_capture.capture_screen(screen_region)
        result['stages']['screen_capture'] = capture
        
        # Stage 2: UI element recognition
        elements = self.ui_recognizer.recognize_elements(capture)
        result['stages']['ui_recognition'] = {
            'element_count': len(elements),
            'elements': [e.to_dict() for e in elements]
        }
        
        # Stage 3: Interaction pattern detection
        ui_element = elements[0] if elements else None
        pattern = self.pattern_detector.detect_interaction(
            event_type, ui_element, metadata
        )
        result['stages']['pattern_detection'] = pattern.to_dict()
        
        # Stage 4: UX paradigm extraction
        recent_patterns = self.pattern_detector.detected_patterns[-5:]
        paradigm = self.paradigm_extractor.extract_paradigm(recent_patterns)
        if paradigm:
            result['stages']['paradigm_extraction'] = paradigm.to_dict()
            
            # Stage 5: OS evolution proposal
            adaptation = self.evolution_controller.propose_adaptation(
                paradigm, {'pattern': pattern.to_dict()}
            )
            result['stages']['evolution_proposal'] = adaptation
        
        # Log witnessing event
        self.witnessing_log.append(result)
        
        return result
    
    def get_layer_status(self) -> dict:
        """Get status of all screen witnessing components."""
        return {
            'session_id': self.session_id,
            'privacy_consent': self.privacy_consent,
            'witnessing_count': len(self.witnessing_log),
            'components': {
                'screen_capture': self.screen_capture.get_capture_stats(),
                'ui_recognizer': self.ui_recognizer.get_recognition_stats(),
                'pattern_detector': self.pattern_detector.get_pattern_statistics(),
                'paradigm_extractor': self.paradigm_extractor.get_paradigm_summary(),
                'evolution_controller': self.evolution_controller.get_evolution_state()
            }
        }
    
    def export_witnessing_log(self, output_path: Optional[Path] = None) -> str:
        """Export witnessing log to JSON."""
        if output_path is None:
            output_path = REPO_DIR / "growth" / f"screen_log_{self.session_id}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            'session_id': self.session_id,
            'export_timestamp': datetime.now().isoformat(),
            'witnessing_events': self.witnessing_log,
            'status': self.get_layer_status()
        }
        
        output_path.write_text(json.dumps(log_data, indent=2, default=str))
        return str(output_path)
    
    def get_ux_insights(self) -> dict:
        """Get insights about learned UX patterns and paradigms."""
        top_patterns = self.pattern_detector.get_most_common_interactions()
        top_paradigms = self.paradigm_extractor.get_top_paradigms()
        
        return {
            'most_common_interactions': [
                {'type': t, 'count': c} for t, c in top_patterns
            ],
            'learned_paradigms': [p.to_dict() for p in top_paradigms],
            'evolution_summary': self.evolution_controller.get_adaptation_summary()
        }


def get_screen_layer_metadata() -> dict:
    """
    Get metadata about the screen feed witnessing layer.
    Used by the autopoietic synthesis system.
    """
    return {
        'name': 'Screen Feed Witnessing Layer',
        'version': '1.0',
        'components': [
            {'name': 'Screen Capture', 'color': '#333'},
            {'name': 'UI Element Recognition', 'color': '#444'},
            {'name': 'Interaction Pattern Detector', 'color': '#555'},
            {'name': 'UX Paradigm Extractor', 'color': '#666'},
            {'name': 'Feedback Coupling Engine', 'color': '#777'},
            {'name': 'OS Evolution Controller', 'color': '#888'}
        ],
        'features': [
            'Screen capture and analysis',
            'UI element recognition',
            'Interaction pattern detection',
            'UX paradigm extraction',
            'Real-time feedback coupling',
            'Personalized OS evolution based on usage'
        ],
        'capabilities': [
            'Witness user interactions',
            'Learn current UX paradigms',
            'Detect feedback couplings',
            'Enable piecewise computing evolution',
            'Adapt OS to user patterns'
        ],
        'integration': [
            'Works with voice integration',
            'Feeds into JIT Language Model',
            'Contributes to OPIC field resonance'
        ]
    }


def main():
    """Demonstrate screen feed witnessing layer functionality."""
    print("Screen Feed Witnessing Layer — OPIC Growth Service")
    print("=" * 60)
    
    # Initialize layer
    layer = ScreenFeedWitnessingLayer()
    
    # Display metadata
    metadata = get_screen_layer_metadata()
    print(f"\nLayer: {metadata['name']} v{metadata['version']}")
    
    print("\nComponents:")
    for component in metadata['components']:
        print(f"  • {component['name']}")
    
    print("\nFeatures:")
    for feature in metadata['features']:
        print(f"  • {feature}")
    
    print("\nCapabilities:")
    for capability in metadata['capabilities']:
        print(f"  • {capability}")
    
    print("\nIntegration:")
    for integration in metadata['integration']:
        print(f"  • {integration}")
    
    # Privacy consent demo
    print("\n" + "=" * 60)
    print("Privacy & Consent:")
    print("  Screen witnessing requires user consent")
    print("  All processing is local and privacy-preserving")
    layer.set_privacy_consent(True)
    print("  [✓] Privacy consent granted")
    
    # Test interaction witnessing
    print("\n" + "=" * 60)
    print("Interaction Witnessing Demo:")
    
    sample_interactions = [
        ('click', None, {'target': 'button'}),
        ('scroll', None, {'direction': 'down'}),
        ('type', None, {'text': 'sample input'}),
        ('right_click', None, {'target': 'menu'}),
        ('drag', None, {'from': (100, 100), 'to': (200, 200)}),
    ]
    
    for event_type, region, meta in sample_interactions:
        result = layer.witness_interaction(event_type, region, meta)
        if result.get('status') != 'denied':
            print(f"  Witnessed: {event_type} → {result['stages']['pattern_detection']['pattern_type']}")
    
    # Display UX insights
    print("\n" + "=" * 60)
    print("UX Insights:")
    insights = layer.get_ux_insights()
    
    print("  Most Common Interactions:")
    for interaction in insights['most_common_interactions'][:3]:
        print(f"    • {interaction['type']}: {interaction['count']} times")
    
    if insights['learned_paradigms']:
        print("\n  Learned UX Paradigms:")
        for paradigm in insights['learned_paradigms'][:3]:
            print(f"    • {paradigm['paradigm_name']}: {paradigm['occurrences']} occurrences")
    
    # Display layer status
    status = layer.get_layer_status()
    print(f"\n  Session: {status['session_id']}")
    print(f"  Witnessing events: {status['witnessing_count']}")
    print(f"  Privacy consent: {'Yes' if status['privacy_consent'] else 'No'}")
    
    print("\n[✓] Screen Feed Witnessing Layer initialized")
    return layer


if __name__ == '__main__':
    main()
