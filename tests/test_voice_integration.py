#!/usr/bin/env python3
"""
Tests for the Voice Integration Layer module.
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from voice_integration import (
    VoicePattern,
    FeedbackCoupling,
    VoiceInputProcessor,
    SpeechToText,
    TextToSpeech,
    AudioPatternRecognizer,
    VoiceCommandInterpreter,
    FeedbackCouplingEngine,
    VoiceIntegrationLayer,
    get_voice_layer_metadata
)


def test_voice_pattern_creation():
    """Test VoicePattern dataclass creation."""
    pattern = VoicePattern(
        pattern_id="test_001",
        pattern_type="command",
        content="open settings",
        confidence=0.9,
        timestamp="2025-01-01T00:00:00"
    )
    
    assert pattern.pattern_id == "test_001"
    assert pattern.pattern_type == "command"
    assert pattern.confidence == 0.9
    
    # Test to_dict
    pattern_dict = pattern.to_dict()
    assert pattern_dict['pattern_id'] == "test_001"
    assert pattern_dict['content'] == "open settings"
    
    print("✓ VoicePattern creation test passed")


def test_voice_input_processor():
    """Test VoiceInputProcessor functionality."""
    processor = VoiceInputProcessor()
    
    # Test audio processing
    result = processor.process_audio_input(b"test audio data")
    assert result['status'] == 'processed'
    assert result['size'] == 15  # len(b"test audio data")
    assert processor.processed_count == 1
    
    # Test buffering
    processor.buffer_input(b"chunk1")
    processor.buffer_input(b"chunk2")
    assert len(processor.buffer) == 2
    
    chunks = processor.flush_buffer()
    assert len(chunks) == 2
    assert len(processor.buffer) == 0
    
    print("✓ VoiceInputProcessor test passed")


def test_speech_to_text():
    """Test SpeechToText functionality."""
    stt = SpeechToText()
    
    # Test recognition
    result = stt.recognize(b"audio data", language='en-US')
    assert result['language'] == 'en-US'
    assert result['status'] == 'ready'
    
    # Test vocabulary
    stt.add_vocabulary(['custom', 'words'])
    assert 'custom' in stt.vocabulary
    assert 'words' in stt.vocabulary
    
    # Test stats
    stats = stt.get_recognition_stats()
    assert stats['total'] == 1
    
    print("✓ SpeechToText test passed")


def test_text_to_speech():
    """Test TextToSpeech functionality."""
    tts = TextToSpeech()
    
    # Test synthesis
    result = tts.synthesize("Hello world")
    assert result['text'] == "Hello world"
    assert result['voice'] == 'default'
    assert result['status'] == 'ready'
    
    # Test voice profiles
    tts.add_voice_profile('custom', pitch=1.5, rate=1.2, volume=0.8)
    assert 'custom' in tts.voice_profiles
    assert tts.voice_profiles['custom']['pitch'] == 1.5
    
    # Test set voice
    assert tts.set_voice('custom') is True
    assert tts.current_voice == 'custom'
    assert tts.set_voice('nonexistent') is False
    
    # Test queue
    pos = tts.queue_speech("Queued message")
    assert pos == 0
    assert len(tts.synthesis_queue) == 1
    
    print("✓ TextToSpeech test passed")


def test_audio_pattern_recognizer():
    """Test AudioPatternRecognizer functionality."""
    recognizer = AudioPatternRecognizer()
    
    # Test command patterns
    patterns = recognizer.analyze_text("open calendar")
    assert len(patterns) > 0
    assert patterns[0]['type'] == 'app_launch'
    assert patterns[0]['target'] == 'calendar'
    
    patterns = recognizer.analyze_text("search for documents")
    assert patterns[0]['type'] == 'search'
    
    patterns = recognizer.analyze_text("what is the time?")
    assert patterns[0]['type'] == 'help'
    
    # Test query detection
    patterns = recognizer.analyze_text("Is this a question?")
    assert patterns[0]['type'] == 'query'
    
    # Test statement detection
    patterns = recognizer.analyze_text("This is a statement")
    assert patterns[0]['type'] == 'statement'
    
    # Test statistics
    stats = recognizer.get_pattern_statistics()
    assert stats['app_launch'] == 1
    assert stats['search'] == 1
    
    # Test most common
    common = recognizer.get_most_common_patterns(3)
    assert len(common) <= 3
    
    print("✓ AudioPatternRecognizer test passed")


def test_voice_command_interpreter():
    """Test VoiceCommandInterpreter functionality."""
    interpreter = VoiceCommandInterpreter()
    
    # Test interpretation without handlers
    pattern = {'type': 'app_launch', 'target': 'calendar', 'action': 'open'}
    result = interpreter.interpret(pattern)
    assert result['status'] == 'interpreted'
    assert result['action'] == 'app_launch'
    assert result['parameters']['target'] == 'calendar'
    
    # Test with custom handler
    def custom_handler(pattern):
        return {'action': 'custom_action', 'parameters': {'custom': True}}
    
    interpreter.register_handler('custom', custom_handler)
    assert 'custom' in interpreter.get_supported_commands()
    
    pattern = {'type': 'custom'}
    result = interpreter.interpret(pattern)
    assert result['status'] == 'executed'
    assert result['action'] == 'custom_action'
    
    print("✓ VoiceCommandInterpreter test passed")


def test_feedback_coupling_engine():
    """Test FeedbackCouplingEngine functionality."""
    engine = FeedbackCouplingEngine()
    
    # Test coupling creation
    pattern = VoicePattern(
        pattern_id="test",
        pattern_type="command",
        content="test command",
        confidence=0.8
    )
    
    coupling = engine.create_coupling(
        input_pattern=pattern,
        system_response="executed",
        adaptation_type="learning"
    )
    
    assert coupling.coupling_id.startswith("fc_")
    assert coupling.adaptation_type == "learning"
    assert coupling.evolution_delta > 0
    
    # Test evolution state
    state = engine.get_evolution_state()
    assert state['total_adaptations'] == 1
    assert state['evolution_delta'] > 0
    
    # Test adaptation summary
    summary = engine.get_adaptation_summary()
    assert summary['total'] == 1
    assert summary['cumulative_delta'] > 0
    
    print("✓ FeedbackCouplingEngine test passed")


def test_voice_integration_layer():
    """Test VoiceIntegrationLayer main class."""
    layer = VoiceIntegrationLayer()
    
    # Test session creation
    assert layer.session_id.startswith("voice_")
    
    # Test voice processing pipeline
    result = layer.process_voice_input(b"test audio", language='en-US')
    assert result['session_id'] == layer.session_id
    assert 'stages' in result
    assert 'audio_processing' in result['stages']
    assert 'speech_to_text' in result['stages']
    
    # Test synthesis
    synthesis = layer.synthesize_response("Hello")
    assert synthesis['text'] == "Hello"
    assert synthesis['status'] == 'ready'
    
    # Test layer status
    status = layer.get_layer_status()
    assert 'components' in status
    assert 'input_processor' in status['components']
    assert 'speech_to_text' in status['components']
    assert 'feedback_engine' in status['components']
    
    print("✓ VoiceIntegrationLayer test passed")


def test_layer_metadata():
    """Test get_voice_layer_metadata function."""
    metadata = get_voice_layer_metadata()
    
    assert metadata['name'] == 'Voice Integration Layer'
    assert metadata['version'] == '1.0'
    assert len(metadata['components']) == 6
    assert len(metadata['features']) == 6
    assert len(metadata['integration']) == 3
    
    # Check component names
    component_names = [c['name'] for c in metadata['components']]
    assert 'Voice Input Processor' in component_names
    assert 'Speech Recognition' in component_names
    assert 'Voice Output Synthesizer' in component_names
    
    print("✓ Layer metadata test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Voice Integration Layer - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_voice_pattern_creation,
        test_voice_input_processor,
        test_speech_to_text,
        test_text_to_speech,
        test_audio_pattern_recognizer,
        test_voice_command_interpreter,
        test_feedback_coupling_engine,
        test_voice_integration_layer,
        test_layer_metadata,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
