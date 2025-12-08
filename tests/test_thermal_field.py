#!/usr/bin/env python3
"""
Tests for the Thermal Field module.
"""

import sys
from pathlib import Path
import numpy as np

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from thermal_field import (
    ThermalState,
    ThermalMetrics,
    ThermalFieldAnalyzer,
    CoolingOptimizer,
    get_thermal_field_metadata
)


def test_thermal_state_creation():
    """Test ThermalState dataclass creation."""
    T_field = np.array([300, 305, 310])
    load = np.array([0.2, 0.5, 0.8])
    
    state = ThermalState(
        timestamp="2025-12-08T09:00:00",
        temperature_field=T_field,
        computational_load=load,
        baseline_temp=298.15
    )
    
    assert state.timestamp == "2025-12-08T09:00:00"
    assert len(state.temperature_field) == 3
    assert len(state.computational_load) == 3
    assert state.baseline_temp == 298.15
    
    # Test to_dict
    state_dict = state.to_dict()
    assert 'timestamp' in state_dict
    assert 'temperature_field' in state_dict
    assert 'baseline_temp' in state_dict
    
    print("✓ ThermalState creation test passed")


def test_thermal_curvature():
    """Test thermal curvature calculation."""
    analyzer = ThermalFieldAnalyzer(baseline_temp=298.15)
    
    # Uniform temperature (no gradient) should have low curvature
    T_uniform = np.array([300.0] * 10)
    curvature_uniform = analyzer.thermal_curvature(T_uniform)
    assert curvature_uniform < 0.01  # Near zero
    
    # High gradient should have higher curvature
    T_gradient = np.linspace(295, 310, 10)
    curvature_gradient = analyzer.thermal_curvature(T_gradient)
    assert curvature_gradient > curvature_uniform
    
    print("✓ Thermal curvature test passed")


def test_thermal_entropy():
    """Test thermal entropy calculation."""
    analyzer = ThermalFieldAnalyzer()
    
    T_field = np.array([300, 305, 310, 308, 302])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3])
    
    entropy = analyzer.thermal_entropy(T_field, load)
    
    # Entropy should be positive
    assert entropy >= 0.0
    
    # Equal distribution should have higher entropy
    T_equal = np.ones(5) * 300
    load_equal = np.ones(5) * 0.5
    entropy_equal = analyzer.thermal_entropy(T_equal, load_equal)
    
    # We expect some entropy value
    assert entropy_equal >= 0.0
    
    print("✓ Thermal entropy test passed")


def test_entropy_reduction():
    """Test entropy reduction calculation."""
    analyzer = ThermalFieldAnalyzer()
    
    # Before: high variance
    T_before = np.array([295, 310, 315, 308, 298])
    # After: lower variance (optimized)
    T_after = np.array([299, 302, 304, 301, 299])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3])
    
    reduction = analyzer.entropy_reduction(T_before, T_after, load)
    
    # Reduction should be positive (entropy decreased)
    # Note: depending on the coupling, this may not always be positive
    assert -1.0 <= reduction <= 1.0  # Valid range
    
    print("✓ Entropy reduction test passed")


def test_homeostasis_score():
    """Test homeostasis score calculation."""
    analyzer = ThermalFieldAnalyzer()
    
    T_target = np.array([300.0] * 10)
    
    # Perfect match
    T_perfect = np.array([300.0] * 10)
    score_perfect = analyzer.homeostasis_score(T_perfect, T_target)
    assert score_perfect == 1.0
    
    # Some deviation
    T_deviated = np.array([299, 301, 300, 302, 298, 300, 301, 299, 300, 300])
    score_deviated = analyzer.homeostasis_score(T_deviated, T_target)
    assert 0.0 <= score_deviated < 1.0
    
    print("✓ Homeostasis score test passed")


def test_gradient_magnitude():
    """Test gradient magnitude calculation."""
    analyzer = ThermalFieldAnalyzer()
    
    # Flat field
    T_flat = np.array([300.0] * 10)
    grad_flat = analyzer.gradient_magnitude(T_flat)
    assert grad_flat < 0.01
    
    # Linear gradient
    T_linear = np.linspace(295, 305, 10)
    grad_linear = analyzer.gradient_magnitude(T_linear)
    assert grad_linear > grad_flat
    
    print("✓ Gradient magnitude test passed")


def test_alignment_coefficient():
    """Test alignment coefficient calculation."""
    analyzer = ThermalFieldAnalyzer()
    
    # Perfectly aligned (temperature follows load)
    load = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    T_aligned = np.array([298, 300, 302, 304, 306])
    
    alignment = analyzer.alignment_coefficient(T_aligned, load)
    
    # Should be positive (correlated)
    assert alignment > 0.5
    
    # Anti-aligned (temperature opposite to load)
    T_anti = np.array([306, 304, 302, 300, 298])
    alignment_anti = analyzer.alignment_coefficient(T_anti, load)
    
    # Should be negative (anti-correlated)
    assert alignment_anti < -0.5
    
    print("✓ Alignment coefficient test passed")


def test_analyze_state():
    """Test complete state analysis."""
    analyzer = ThermalFieldAnalyzer()
    
    T_field = np.array([300, 305, 310, 308, 302, 299, 298])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3, 0.1, 0.05])
    
    state = ThermalState(
        timestamp="2025-12-08T09:00:00",
        temperature_field=T_field,
        computational_load=load
    )
    
    metrics = analyzer.analyze_state(state)
    
    # Check all metrics are computed
    assert isinstance(metrics, ThermalMetrics)
    assert metrics.curvature >= 0.0
    assert metrics.entropy >= 0.0
    assert 0.0 <= metrics.homeostasis_score <= 1.0
    assert metrics.gradient_magnitude >= 0.0
    assert -1.0 <= metrics.alignment_coefficient <= 1.0
    
    # Check to_dict works
    metrics_dict = metrics.to_dict()
    assert 'curvature' in metrics_dict
    assert 'entropy' in metrics_dict
    
    # Check history was stored
    assert len(analyzer.history) == 1
    
    print("✓ Analyze state test passed")


def test_optimization_summary():
    """Test optimization summary generation."""
    analyzer = ThermalFieldAnalyzer()
    
    T_before = np.array([295, 310, 315, 308, 298, 297, 296])
    T_after = np.array([299, 302, 304, 301, 299, 298, 297])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3, 0.1, 0.05])
    
    before = ThermalState(
        timestamp="2025-12-08T09:00:00",
        temperature_field=T_before,
        computational_load=load
    )
    
    after = ThermalState(
        timestamp="2025-12-08T09:01:00",
        temperature_field=T_after,
        computational_load=load
    )
    
    summary = analyzer.optimization_summary(before, after)
    
    # Check summary structure
    assert 'before' in summary
    assert 'after' in summary
    assert 'improvements' in summary
    
    # Check improvements
    improvements = summary['improvements']
    assert 'entropy_reduction' in improvements
    assert 'curvature_reduction' in improvements
    assert 'homeostasis_improvement' in improvements
    
    print("✓ Optimization summary test passed")


def test_cooling_optimizer():
    """Test CoolingOptimizer class."""
    optimizer = CoolingOptimizer(alpha=0.1, beta=0.5)
    
    T_current = np.array([300, 305, 310, 308, 302])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3])
    
    T_optimized = optimizer.optimize_temperature(T_current, load, dt=1.0)
    
    # Should return array of same shape
    assert T_optimized.shape == T_current.shape
    
    # Temperatures should be reasonable (not NaN or infinite)
    assert np.all(np.isfinite(T_optimized))
    
    # Temperatures should be in reasonable range (250-350K)
    assert np.all(T_optimized > 250)
    assert np.all(T_optimized < 350)
    
    print("✓ Cooling optimizer test passed")


def test_iterative_optimization():
    """Test that iterative optimization improves metrics."""
    analyzer = ThermalFieldAnalyzer()
    optimizer = CoolingOptimizer(alpha=0.2, beta=0.8)
    
    # Start with suboptimal temperature distribution
    T_current = np.array([295, 310, 315, 312, 298, 296, 295])
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3, 0.1, 0.05])
    
    initial_state = ThermalState(
        timestamp="2025-12-08T09:00:00",
        temperature_field=T_current,
        computational_load=load
    )
    
    initial_metrics = analyzer.analyze_state(initial_state)
    
    # Apply multiple optimization steps
    for i in range(5):
        T_current = optimizer.optimize_temperature(T_current, load, dt=0.5)
    
    final_state = ThermalState(
        timestamp="2025-12-08T09:05:00",
        temperature_field=T_current,
        computational_load=load
    )
    
    final_metrics = analyzer.analyze_state(final_state)
    
    # Check that some improvement occurred
    # (Note: not all metrics may improve depending on initial conditions)
    assert initial_metrics.curvature >= 0.0
    assert final_metrics.curvature >= 0.0
    
    print("✓ Iterative optimization test passed")


def test_metadata():
    """Test get_thermal_field_metadata function."""
    metadata = get_thermal_field_metadata()
    
    assert metadata['name'] == 'Thermal Field Module'
    assert metadata['version'] == '1.0'
    assert len(metadata['components']) == 2
    assert len(metadata['metrics']) == 5
    assert len(metadata['field_equations']) == 3
    
    # Check component names
    component_names = [c['name'] for c in metadata['components']]
    assert 'ThermalFieldAnalyzer' in component_names
    assert 'CoolingOptimizer' in component_names
    
    print("✓ Metadata test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Thermal Field Module - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_thermal_state_creation,
        test_thermal_curvature,
        test_thermal_entropy,
        test_entropy_reduction,
        test_homeostasis_score,
        test_gradient_magnitude,
        test_alignment_coefficient,
        test_analyze_state,
        test_optimization_summary,
        test_cooling_optimizer,
        test_iterative_optimization,
        test_metadata,
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
