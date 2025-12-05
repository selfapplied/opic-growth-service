#!/usr/bin/env python3
"""
Voice Integration Layer: Live UX paradigm learning through audio input/output.
Provides voice processing, speech recognition, synthesis, and feedback coupling.
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional
from dataclasses import dataclass, field


REPO_DIR = Path(__file__).resolve().parents[1]


@dataclass
class VoicePattern:
    """Represents a detected voice interaction pattern."""
    pattern_id: str
    pattern_type: str  # command, query, statement, feedback
    content: str
    confidence: float = 0.0
    timestamp: str = ""
    context: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type,
            'content': self.content,
            'confidence': self.confidence,
            'timestamp': self.timestamp,
            'context': self.context
        }


@dataclass
class FeedbackCoupling:
    """Represents a feedback coupling between voice and system."""
    coupling_id: str
    input_pattern: VoicePattern
    system_response: str
    adaptation_type: str  # learning, correction, confirmation
    evolution_delta: float = 0.0
    
    def to_dict(self):
        """Convert to dictionary representation."""
        return {
            'coupling_id': self.coupling_id,
            'input_pattern': self.input_pattern.to_dict(),
            'system_response': self.system_response,
            'adaptation_type': self.adaptation_type,
            'evolution_delta': self.evolution_delta
        }


class VoiceInputProcessor:
    """Processes voice input for pattern analysis."""
    
    def __init__(self):
        self.buffer = []
        self.processed_count = 0
    
    def process_audio_input(self, audio_data: bytes) -> dict:
        """
        Process raw audio input data.
        
        In a full implementation, this would interface with audio hardware.
        For now, provides a structured interface for audio processing.
        """
        processed = {
            'timestamp': datetime.now().isoformat(),
            'size': len(audio_data) if audio_data else 0,
            'status': 'processed',
            'format': 'raw'
        }
        self.processed_count += 1
        return processed
    
    def buffer_input(self, audio_chunk: bytes) -> None:
        """Buffer audio input for batch processing."""
        self.buffer.append({
            'data': audio_chunk,
            'timestamp': datetime.now().isoformat()
        })
    
    def flush_buffer(self) -> list:
        """Flush and return buffered audio chunks."""
        chunks = self.buffer.copy()
        self.buffer = []
        return chunks


class SpeechToText:
    """Converts speech to text using abstracted recognition."""
    
    def __init__(self):
        self.recognition_history = []
        self.vocabulary = set()
    
    def recognize(self, audio_data: bytes, language: str = 'en-US') -> dict:
        """
        Convert audio to text.
        
        This provides the interface for speech recognition.
        Actual implementation would use Web Speech API or similar.
        """
        result = {
            'text': '',
            'confidence': 0.0,
            'language': language,
            'alternatives': [],
            'timestamp': datetime.now().isoformat(),
            'status': 'ready'
        }
        
        # Track recognition attempt
        self.recognition_history.append({
            'timestamp': result['timestamp'],
            'language': language,
            'success': result['confidence'] > 0.5
        })
        
        return result
    
    def add_vocabulary(self, words: list) -> None:
        """Add custom vocabulary for improved recognition."""
        self.vocabulary.update(words)
    
    def get_recognition_stats(self) -> dict:
        """Get statistics on recognition performance."""
        total = len(self.recognition_history)
        if total == 0:
            return {'total': 0, 'success_rate': 0.0}
        
        successful = sum(1 for r in self.recognition_history if r['success'])
        return {
            'total': total,
            'successful': successful,
            'success_rate': successful / total
        }


class TextToSpeech:
    """Synthesizes speech from text."""
    
    def __init__(self):
        self.synthesis_queue = []
        self.voice_profiles = {
            'default': {'pitch': 1.0, 'rate': 1.0, 'volume': 1.0}
        }
        self.current_voice = 'default'
    
    def synthesize(self, text: str, voice: Optional[str] = None) -> dict:
        """
        Synthesize speech from text.
        
        This provides the interface for speech synthesis.
        Actual implementation would use Web Speech API or similar.
        """
        voice = voice or self.current_voice
        profile = self.voice_profiles.get(voice, self.voice_profiles['default'])
        
        result = {
            'text': text,
            'voice': voice,
            'pitch': profile['pitch'],
            'rate': profile['rate'],
            'volume': profile['volume'],
            'timestamp': datetime.now().isoformat(),
            'status': 'ready'
        }
        
        return result
    
    def queue_speech(self, text: str, voice: Optional[str] = None) -> int:
        """Queue text for synthesis and return queue position."""
        self.synthesis_queue.append({
            'text': text,
            'voice': voice or self.current_voice,
            'timestamp': datetime.now().isoformat()
        })
        return len(self.synthesis_queue) - 1
    
    def add_voice_profile(self, name: str, pitch: float = 1.0, 
                          rate: float = 1.0, volume: float = 1.0) -> None:
        """Add a custom voice profile."""
        self.voice_profiles[name] = {
            'pitch': max(0.1, min(2.0, pitch)),
            'rate': max(0.1, min(10.0, rate)),
            'volume': max(0.0, min(1.0, volume))
        }
    
    def set_voice(self, voice: str) -> bool:
        """Set the current voice profile."""
        if voice in self.voice_profiles:
            self.current_voice = voice
            return True
        return False


class AudioPatternRecognizer:
    """Recognizes patterns in audio interactions."""
    
    # Command patterns for voice interpretation
    COMMAND_PATTERNS = [
        (r'^(open|launch|start)\s+(.+)$', 'app_launch'),
        (r'^(close|quit|exit)\s+(.+)$', 'app_close'),
        (r'^(search|find|look for)\s+(.+)$', 'search'),
        (r'^(go to|navigate to|show)\s+(.+)$', 'navigate'),
        (r'^(create|new|make)\s+(.+)$', 'create'),
        (r'^(delete|remove)\s+(.+)$', 'delete'),
        (r'^(save|store)\s+(.+)$', 'save'),
        (r'^(help|assist|what is)\s*(.*)$', 'help'),
        (r'^(cancel|stop|abort)$', 'cancel'),
        (r'^(undo|reverse)$', 'undo'),
        (r'^(redo|repeat)$', 'redo'),
    ]
    
    def __init__(self):
        self.patterns = []
        self.pattern_history = []
        self.pattern_counts = defaultdict(int)
    
    def analyze_text(self, text: str) -> list:
        """Analyze transcribed text for patterns."""
        detected = []
        text_lower = text.lower().strip()
        
        for pattern, pattern_type in self.COMMAND_PATTERNS:
            match = re.match(pattern, text_lower, re.IGNORECASE)
            if match:
                groups = match.groups()
                detected.append({
                    'type': pattern_type,
                    'action': groups[0] if groups else '',
                    'target': groups[1] if len(groups) > 1 else '',
                    'confidence': 0.9,
                    'raw_text': text
                })
                self.pattern_counts[pattern_type] += 1
        
        # If no command pattern matched, classify as query or statement
        if not detected:
            if text_lower.endswith('?'):
                detected.append({
                    'type': 'query',
                    'content': text,
                    'confidence': 0.8,
                    'raw_text': text
                })
                self.pattern_counts['query'] += 1
            else:
                detected.append({
                    'type': 'statement',
                    'content': text,
                    'confidence': 0.7,
                    'raw_text': text
                })
                self.pattern_counts['statement'] += 1
        
        self.pattern_history.extend(detected)
        return detected
    
    def get_pattern_statistics(self) -> dict:
        """Get statistics on detected patterns."""
        return dict(self.pattern_counts)
    
    def get_most_common_patterns(self, n: int = 5) -> list:
        """Get the most commonly used patterns."""
        sorted_patterns = sorted(
            self.pattern_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_patterns[:n]


class VoiceCommandInterpreter:
    """Interprets voice commands for system actions."""
    
    def __init__(self):
        self.command_handlers = {}
        self.interpretation_history = []
    
    def register_handler(self, command_type: str, handler: callable) -> None:
        """Register a handler for a command type."""
        self.command_handlers[command_type] = handler
    
    def interpret(self, pattern: dict) -> dict:
        """
        Interpret a detected pattern as a system command.
        
        Returns interpretation result with suggested action.
        """
        interpretation = {
            'pattern': pattern,
            'timestamp': datetime.now().isoformat(),
            'status': 'interpreted',
            'action': None,
            'parameters': {}
        }
        
        pattern_type = pattern.get('type', '')
        
        if pattern_type in self.command_handlers:
            # Execute registered handler
            handler = self.command_handlers[pattern_type]
            try:
                result = handler(pattern)
                interpretation['action'] = result.get('action')
                interpretation['parameters'] = result.get('parameters', {})
                interpretation['status'] = 'executed'
            except Exception as e:
                interpretation['status'] = 'error'
                interpretation['error'] = str(e)
        else:
            # Default interpretation based on pattern type
            interpretation['action'] = pattern_type
            interpretation['parameters'] = {
                'target': pattern.get('target', pattern.get('content', '')),
                'action': pattern.get('action', '')
            }
        
        self.interpretation_history.append(interpretation)
        return interpretation
    
    def get_supported_commands(self) -> list:
        """Get list of supported command types."""
        return list(self.command_handlers.keys())


class FeedbackCouplingEngine:
    """
    Creates feedback loops between voice interactions and system evolution.
    Enables personalized OS adaptation based on voice patterns.
    """
    
    def __init__(self):
        self.couplings = []
        self.adaptation_history = []
        self.evolution_state = {
            'total_adaptations': 0,
            'learning_rate': 0.01,
            'evolution_delta': 0.0
        }
    
    def create_coupling(self, input_pattern: VoicePattern, 
                        system_response: str,
                        adaptation_type: str = 'learning') -> FeedbackCoupling:
        """Create a feedback coupling between voice and system."""
        coupling_id = f"fc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.couplings)}"
        
        coupling = FeedbackCoupling(
            coupling_id=coupling_id,
            input_pattern=input_pattern,
            system_response=system_response,
            adaptation_type=adaptation_type,
            evolution_delta=self._calculate_evolution_delta(input_pattern, adaptation_type)
        )
        
        self.couplings.append(coupling)
        self._apply_adaptation(coupling)
        
        return coupling
    
    def _calculate_evolution_delta(self, pattern: VoicePattern, 
                                    adaptation_type: str) -> float:
        """Calculate the evolution delta for an adaptation."""
        base_delta = self.evolution_state['learning_rate']
        
        # Adjust based on confidence
        delta = base_delta * pattern.confidence
        
        # Adjust based on adaptation type
        type_multipliers = {
            'learning': 1.0,
            'correction': 1.5,
            'confirmation': 0.5
        }
        delta *= type_multipliers.get(adaptation_type, 1.0)
        
        return delta
    
    def _apply_adaptation(self, coupling: FeedbackCoupling) -> None:
        """Apply adaptation from coupling to evolution state."""
        self.evolution_state['total_adaptations'] += 1
        self.evolution_state['evolution_delta'] += coupling.evolution_delta
        
        self.adaptation_history.append({
            'coupling_id': coupling.coupling_id,
            'timestamp': datetime.now().isoformat(),
            'delta': coupling.evolution_delta,
            'cumulative_delta': self.evolution_state['evolution_delta']
        })
    
    def get_evolution_state(self) -> dict:
        """Get current evolution state."""
        return self.evolution_state.copy()
    
    def get_adaptation_summary(self) -> dict:
        """Get summary of adaptations."""
        if not self.adaptation_history:
            return {
                'total': 0,
                'average_delta': 0.0,
                'cumulative_delta': 0.0
            }
        
        deltas = [a['delta'] for a in self.adaptation_history]
        return {
            'total': len(self.adaptation_history),
            'average_delta': sum(deltas) / len(deltas),
            'cumulative_delta': self.evolution_state['evolution_delta']
        }


class VoiceIntegrationLayer:
    """
    Main integration layer combining all voice components.
    Provides unified interface for voice-based UX paradigm learning.
    """
    
    def __init__(self):
        self.input_processor = VoiceInputProcessor()
        self.speech_to_text = SpeechToText()
        self.text_to_speech = TextToSpeech()
        self.pattern_recognizer = AudioPatternRecognizer()
        self.command_interpreter = VoiceCommandInterpreter()
        self.feedback_engine = FeedbackCouplingEngine()
        
        self.session_id = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.interaction_log = []
    
    def process_voice_input(self, audio_data: bytes, 
                            language: str = 'en-US') -> dict:
        """
        Process voice input through the complete pipeline.
        
        Pipeline:
        1. Process audio input
        2. Convert speech to text
        3. Recognize patterns
        4. Interpret commands
        5. Create feedback coupling
        """
        result = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Stage 1: Process audio
        audio_result = self.input_processor.process_audio_input(audio_data)
        result['stages']['audio_processing'] = audio_result
        
        # Stage 2: Speech to text
        stt_result = self.speech_to_text.recognize(audio_data, language)
        result['stages']['speech_to_text'] = stt_result
        
        # If we got text, continue pipeline
        if stt_result.get('text'):
            # Stage 3: Pattern recognition
            patterns = self.pattern_recognizer.analyze_text(stt_result['text'])
            result['stages']['pattern_recognition'] = patterns
            
            # Stage 4: Command interpretation
            if patterns:
                interpretation = self.command_interpreter.interpret(patterns[0])
                result['stages']['command_interpretation'] = interpretation
                
                # Stage 5: Feedback coupling
                voice_pattern = VoicePattern(
                    pattern_id=f"vp_{len(self.interaction_log)}",
                    pattern_type=patterns[0].get('type', 'unknown'),
                    content=stt_result['text'],
                    confidence=patterns[0].get('confidence', 0.0),
                    timestamp=result['timestamp']
                )
                
                coupling = self.feedback_engine.create_coupling(
                    input_pattern=voice_pattern,
                    system_response=interpretation.get('status', 'processed'),
                    adaptation_type='learning'
                )
                result['stages']['feedback_coupling'] = coupling.to_dict()
        
        # Log interaction
        self.interaction_log.append(result)
        
        return result
    
    def synthesize_response(self, text: str, voice: Optional[str] = None) -> dict:
        """Synthesize a voice response."""
        return self.text_to_speech.synthesize(text, voice)
    
    def get_layer_status(self) -> dict:
        """Get status of all voice integration components."""
        return {
            'session_id': self.session_id,
            'interaction_count': len(self.interaction_log),
            'components': {
                'input_processor': {
                    'processed_count': self.input_processor.processed_count,
                    'buffer_size': len(self.input_processor.buffer)
                },
                'speech_to_text': self.speech_to_text.get_recognition_stats(),
                'text_to_speech': {
                    'queue_size': len(self.text_to_speech.synthesis_queue),
                    'voice_profiles': list(self.text_to_speech.voice_profiles.keys())
                },
                'pattern_recognizer': self.pattern_recognizer.get_pattern_statistics(),
                'command_interpreter': {
                    'history_size': len(self.command_interpreter.interpretation_history),
                    'supported_commands': self.command_interpreter.get_supported_commands()
                },
                'feedback_engine': self.feedback_engine.get_evolution_state()
            }
        }
    
    def export_interaction_log(self, output_path: Optional[Path] = None) -> str:
        """Export interaction log to JSON."""
        if output_path is None:
            output_path = REPO_DIR / "growth" / f"voice_log_{self.session_id}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = {
            'session_id': self.session_id,
            'export_timestamp': datetime.now().isoformat(),
            'interactions': self.interaction_log,
            'status': self.get_layer_status()
        }
        
        output_path.write_text(json.dumps(log_data, indent=2, default=str))
        return str(output_path)


def get_voice_layer_metadata() -> dict:
    """
    Get metadata about the voice integration layer.
    Used by the autopoietic synthesis system.
    """
    return {
        'name': 'Voice Integration Layer',
        'version': '1.0',
        'components': [
            {'name': 'Voice Input Processor', 'color': '#333'},
            {'name': 'Speech Recognition', 'color': '#444'},
            {'name': 'Pattern Analyzer', 'color': '#555'},
            {'name': 'Feedback Coupling', 'color': '#666'},
            {'name': 'OS Evolution Engine', 'color': '#777'},
            {'name': 'Voice Output Synthesizer', 'color': '#888'}
        ],
        'features': [
            'Voice input processing',
            'Speech-to-text conversion',
            'Text-to-speech synthesis',
            'Audio pattern recognition',
            'Voice command interpretation',
            'Feedback coupling for personalized OS evolution'
        ],
        'integration': [
            'Piecewise computing architecture',
            'Real-time UX paradigm learning',
            'Personalized adaptation based on voice patterns'
        ]
    }


def main():
    """Demonstrate voice integration layer functionality."""
    print("Voice Integration Layer — OPIC Growth Service")
    print("=" * 50)
    
    # Initialize layer
    layer = VoiceIntegrationLayer()
    
    # Display metadata
    metadata = get_voice_layer_metadata()
    print(f"\nLayer: {metadata['name']} v{metadata['version']}")
    print("\nComponents:")
    for component in metadata['components']:
        print(f"  • {component['name']}")
    
    print("\nFeatures:")
    for feature in metadata['features']:
        print(f"  • {feature}")
    
    print("\nIntegration:")
    for integration in metadata['integration']:
        print(f"  • {integration}")
    
    # Test pattern recognition with sample text
    print("\n" + "=" * 50)
    print("Pattern Recognition Demo:")
    
    sample_commands = [
        "open calendar",
        "search for documents",
        "what is the weather?",
        "save my work",
        "navigate to settings"
    ]
    
    for command in sample_commands:
        patterns = layer.pattern_recognizer.analyze_text(command)
        if patterns:
            p = patterns[0]
            print(f"  '{command}' → {p['type']} (confidence: {p['confidence']:.0%})")
    
    # Display layer status
    status = layer.get_layer_status()
    print(f"\nSession: {status['session_id']}")
    print(f"Pattern statistics: {status['components']['pattern_recognizer']}")
    
    print("\n[✓] Voice Integration Layer initialized")
    return layer


if __name__ == '__main__':
    main()
