#!/usr/bin/env python3
"""
Tests for the Screen Feed Witnessing Layer module.
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from screen_feed_witnessing import (
    UIElement,
    InteractionPattern,
    UXParadigm,
    ScreenCapture,
    UIElementRecognizer,
    InteractionPatternDetector,
    UXParadigmExtractor,
    OSEvolutionController,
    ScreenFeedWitnessingLayer,
    get_screen_layer_metadata
)


def test_ui_element_creation():
    """Test UIElement dataclass creation."""
    element = UIElement(
        element_id="elem_001",
        element_type="button",
        position=(100, 200),
        size=(80, 30),
        text="Click Me"
    )
    
    assert element.element_id == "elem_001"
    assert element.element_type == "button"
    assert element.position == (100, 200)
    assert element.size == (80, 30)
    assert element.text == "Click Me"
    
    # Test to_dict
    element_dict = element.to_dict()
    assert element_dict['element_id'] == "elem_001"
    assert element_dict['element_type'] == "button"
    assert element_dict['position'] == (100, 200)
    
    print("✓ UIElement creation test passed")


def test_interaction_pattern_creation():
    """Test InteractionPattern dataclass creation."""
    ui_element = UIElement("elem_001", "button", (100, 200), (80, 30))
    
    pattern = InteractionPattern(
        pattern_id="pat_001",
        pattern_type="click",
        timestamp="2025-01-01T00:00:00",
        ui_element=ui_element,
        confidence=0.9
    )
    
    assert pattern.pattern_id == "pat_001"
    assert pattern.pattern_type == "click"
    assert pattern.ui_element.element_type == "button"
    assert pattern.confidence == 0.9
    
    # Test to_dict
    pattern_dict = pattern.to_dict()
    assert pattern_dict['pattern_type'] == "click"
    assert pattern_dict['ui_element']['element_type'] == "button"
    
    print("✓ InteractionPattern creation test passed")


def test_ux_paradigm_creation():
    """Test UXParadigm dataclass creation."""
    paradigm = UXParadigm(
        paradigm_id="drag_drop",
        paradigm_name="Drag and Drop",
        description="Direct manipulation through dragging",
        occurrences=5,
        confidence=0.85
    )
    
    assert paradigm.paradigm_id == "drag_drop"
    assert paradigm.paradigm_name == "Drag and Drop"
    assert paradigm.occurrences == 5
    assert paradigm.confidence == 0.85
    
    # Test to_dict
    paradigm_dict = paradigm.to_dict()
    assert paradigm_dict['paradigm_name'] == "Drag and Drop"
    assert paradigm_dict['occurrences'] == 5
    
    print("✓ UXParadigm creation test passed")


def test_screen_capture():
    """Test ScreenCapture functionality."""
    capture = ScreenCapture()
    
    # Test full screen capture
    result = capture.capture_screen()
    assert result['status'] == 'captured'
    assert result['full_screen'] is True
    assert capture.capture_count == 1
    
    # Test region capture
    region = (0, 0, 800, 600)
    result = capture.capture_screen(region)
    assert result['region'] == region
    assert result['full_screen'] is False
    assert result['resolution'] == (800, 600)
    assert capture.capture_count == 2
    
    # Test capture interval
    capture.set_capture_interval(2.5)
    assert capture.capture_interval == 2.5
    
    # Test stats
    stats = capture.get_capture_stats()
    assert stats['total_captures'] == 2
    assert stats['capture_interval'] == 2.5
    
    print("✓ ScreenCapture test passed")


def test_ui_element_recognizer():
    """Test UIElementRecognizer functionality."""
    recognizer = UIElementRecognizer()
    
    # Test element recognition
    screen_data = {'capture_id': 'test_001', 'data': 'mock_data'}
    elements = recognizer.recognize_elements(screen_data)
    assert isinstance(elements, list)
    assert recognizer.recognition_count == 1
    
    # Test cache
    elements2 = recognizer.recognize_elements(screen_data)
    assert recognizer.recognition_count == 1  # Should use cache
    
    # Test element classification
    visual_features = {'has_text_input': True}
    element_type = recognizer.classify_element(visual_features)
    assert element_type == 'input'
    
    visual_features = {'is_clickable': True, 'has_border': True}
    element_type = recognizer.classify_element(visual_features)
    assert element_type == 'button'
    
    visual_features = {'is_clickable': True, 'has_border': False}
    element_type = recognizer.classify_element(visual_features)
    assert element_type == 'link'
    
    visual_features = {'is_container': True, 'has_titlebar': True}
    element_type = recognizer.classify_element(visual_features)
    assert element_type == 'window'
    
    # Test stats
    stats = recognizer.get_recognition_stats()
    assert stats['unique_captures'] == 1
    
    print("✓ UIElementRecognizer test passed")


def test_interaction_pattern_detector():
    """Test InteractionPatternDetector functionality."""
    detector = InteractionPatternDetector()
    
    # Test interaction detection
    ui_element = UIElement("elem_001", "button", (100, 200), (80, 30))
    pattern = detector.detect_interaction('click', ui_element, {'target': 'button'})
    
    assert pattern.pattern_type == 'click'
    assert pattern.ui_element.element_type == "button"
    assert pattern.confidence == 0.9
    assert detector.pattern_counts['click'] == 1
    
    # Test multiple interactions
    detector.detect_interaction('scroll')
    detector.detect_interaction('type')
    detector.detect_interaction('click')
    
    assert detector.pattern_counts['click'] == 2
    assert detector.pattern_counts['scroll'] == 1
    assert detector.pattern_counts['type'] == 1
    
    # Test sequence analysis
    patterns = detector.detected_patterns
    analysis = detector.analyze_pattern_sequence(patterns)
    assert analysis['sequence_length'] == len(patterns)
    assert 'unique_interactions' in analysis
    
    # Test statistics
    stats = detector.get_pattern_statistics()
    assert stats['total_patterns'] == 4
    assert stats['by_type']['click'] == 2
    
    # Test most common
    common = detector.get_most_common_interactions(3)
    assert len(common) <= 3
    assert common[0][0] == 'click'  # Most common
    assert common[0][1] == 2  # Count
    
    print("✓ InteractionPatternDetector test passed")


def test_ux_paradigm_extractor():
    """Test UXParadigmExtractor functionality."""
    extractor = UXParadigmExtractor()
    
    # Test drag and drop pattern
    patterns = [
        InteractionPattern("p1", "click", "2025-01-01T00:00:00"),
        InteractionPattern("p2", "drag", "2025-01-01T00:00:01"),
        InteractionPattern("p3", "drop", "2025-01-01T00:00:02"),
    ]
    
    paradigm = extractor.extract_paradigm(patterns)
    assert paradigm is not None
    assert paradigm.paradigm_id == 'drag_and_drop'
    assert paradigm.paradigm_name == 'Drag and Drop'
    assert paradigm.occurrences == 1
    
    # Test repeated pattern increases confidence
    initial_confidence = paradigm.confidence
    paradigm2 = extractor.extract_paradigm(patterns)
    assert paradigm2.occurrences == 2
    assert paradigm2.confidence > initial_confidence
    
    # Test context menu pattern
    patterns = [
        InteractionPattern("p4", "right_click", "2025-01-01T00:00:03"),
        InteractionPattern("p5", "click", "2025-01-01T00:00:04"),
    ]
    
    paradigm = extractor.extract_paradigm(patterns)
    assert paradigm is not None
    assert paradigm.paradigm_id == 'context_menu'
    
    # Test keyboard shortcut pattern
    patterns = [
        InteractionPattern("p6", "key_combo", "2025-01-01T00:00:05"),
    ]
    
    paradigm = extractor.extract_paradigm(patterns)
    assert paradigm is not None
    assert paradigm.paradigm_id == 'keyboard_shortcuts'
    
    # Test summary
    summary = extractor.get_paradigm_summary()
    assert summary['total_paradigms'] == 3
    assert 'drag_and_drop' in summary['paradigm_list']
    assert summary['occurrences']['drag_and_drop'] == 2
    
    # Test top paradigms
    top = extractor.get_top_paradigms(2)
    assert len(top) <= 2
    assert top[0].paradigm_id == 'drag_and_drop'  # Most used
    
    print("✓ UXParadigmExtractor test passed")


def test_os_evolution_controller():
    """Test OSEvolutionController functionality."""
    controller = OSEvolutionController()
    
    # Test adaptation proposal
    paradigm = UXParadigm(
        paradigm_id="test",
        paradigm_name="Test Paradigm",
        description="Test",
        occurrences=5,
        confidence=0.8
    )
    
    adaptation = controller.propose_adaptation(paradigm, {'context': 'test'})
    assert adaptation['adaptation_id'].startswith('adapt_')
    assert adaptation['paradigm'] == 'Test Paradigm'
    assert adaptation['status'] == 'proposed'
    assert adaptation['evolution_delta'] > 0
    
    # Test adaptation application
    adaptation_id = adaptation['adaptation_id']
    success = controller.apply_adaptation(adaptation_id)
    assert success is True
    
    # Check evolution state
    state = controller.get_evolution_state()
    assert state['total_adaptations'] == 1
    assert state['evolution_delta'] > 0
    assert adaptation_id in state['active_adaptations']
    
    # Test cannot apply twice
    success = controller.apply_adaptation(adaptation_id)
    assert success is False
    
    # Test adaptation summary
    summary = controller.get_adaptation_summary()
    assert summary['total'] == 1
    assert summary['proposed'] == 0  # Was applied
    assert summary['applied'] == 1
    assert summary['cumulative_delta'] > 0
    
    print("✓ OSEvolutionController test passed")


def test_screen_feed_witnessing_layer():
    """Test ScreenFeedWitnessingLayer main class."""
    layer = ScreenFeedWitnessingLayer()
    
    # Test session creation
    assert layer.session_id.startswith("screen_")
    assert layer.privacy_consent is False
    
    # Test privacy consent requirement
    result = layer.witness_interaction('click')
    assert result['status'] == 'denied'
    
    # Grant consent
    layer.set_privacy_consent(True)
    assert layer.privacy_consent is True
    
    # Test witnessing pipeline
    result = layer.witness_interaction('click', metadata={'target': 'button'})
    assert result.get('status') != 'denied'
    assert 'stages' in result
    assert 'screen_capture' in result['stages']
    assert 'ui_recognition' in result['stages']
    assert 'pattern_detection' in result['stages']
    
    # Witness more interactions to trigger paradigm extraction
    layer.witness_interaction('click')
    layer.witness_interaction('drag')
    layer.witness_interaction('drop')
    result = layer.witness_interaction('click')
    
    # Check for paradigm extraction and evolution proposal
    if 'paradigm_extraction' in result['stages']:
        assert 'evolution_proposal' in result['stages']
    
    # Test layer status
    status = layer.get_layer_status()
    assert 'components' in status
    assert 'screen_capture' in status['components']
    assert 'ui_recognizer' in status['components']
    assert 'pattern_detector' in status['components']
    assert 'paradigm_extractor' in status['components']
    assert 'evolution_controller' in status['components']
    assert status['privacy_consent'] is True
    assert status['witnessing_count'] > 0
    
    # Test UX insights
    insights = layer.get_ux_insights()
    assert 'most_common_interactions' in insights
    assert 'learned_paradigms' in insights
    assert 'evolution_summary' in insights
    
    print("✓ ScreenFeedWitnessingLayer test passed")


def test_layer_metadata():
    """Test get_screen_layer_metadata function."""
    metadata = get_screen_layer_metadata()
    
    assert metadata['name'] == 'Screen Feed Witnessing Layer'
    assert metadata['version'] == '1.0'
    assert len(metadata['components']) == 6
    assert len(metadata['features']) == 6
    assert len(metadata['capabilities']) == 5
    assert len(metadata['integration']) == 3
    
    # Check component names
    component_names = [c['name'] for c in metadata['components']]
    assert 'Screen Capture' in component_names
    assert 'UI Element Recognition' in component_names
    assert 'OS Evolution Controller' in component_names
    
    # Check features
    assert 'Screen capture and analysis' in metadata['features']
    assert 'Interaction pattern detection' in metadata['features']
    
    # Check capabilities
    assert 'Witness user interactions' in metadata['capabilities']
    assert 'Learn current UX paradigms' in metadata['capabilities']
    
    # Check integration
    assert 'Works with voice integration' in metadata['integration']
    assert 'Feeds into JIT Language Model' in metadata['integration']
    
    print("✓ Layer metadata test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Screen Feed Witnessing Layer - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_ui_element_creation,
        test_interaction_pattern_creation,
        test_ux_paradigm_creation,
        test_screen_capture,
        test_ui_element_recognizer,
        test_interaction_pattern_detector,
        test_ux_paradigm_extractor,
        test_os_evolution_controller,
        test_screen_feed_witnessing_layer,
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
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
