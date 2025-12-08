#!/usr/bin/env python3
"""
Thermal Field Visualizer — Generate SVG visualizations of thermal field dynamics.

Demonstrates:
1. Temperature field before/after optimization
2. Thermal curvature visualization
3. Entropy reduction over time
4. Load-temperature alignment
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from thermal_field import (
    ThermalFieldAnalyzer,
    ThermalState,
    CoolingOptimizer
)
import numpy as np


def generate_thermal_comparison_svg(before_state, after_state, metrics_before, metrics_after):
    """
    Generate SVG comparing thermal states before and after optimization.
    
    Args:
        before_state: ThermalState before optimization
        after_state: ThermalState after optimization
        metrics_before: ThermalMetrics before
        metrics_after: ThermalMetrics after
    
    Returns:
        SVG string
    """
    width = 800
    height = 400
    
    # Normalize temperature fields for visualization
    T_before = before_state.temperature_field
    T_after = after_state.temperature_field
    load = before_state.computational_load
    
    n_points = len(T_before)
    x_scale = (width - 100) / n_points
    
    # Create SVG
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '.title{font:16px sans-serif;fill:#fff;font-weight:bold}',
        '.label{font:12px sans-serif;fill:#aaa}',
        '.metric{font:11px monospace;fill:#0f0}',
        '.temp-line{fill:none;stroke-width:2}',
        '.load-bar{opacity:0.3}',
        '</style>',
        '<rect width="100%" height="100%" fill="#111"/>',
        
        # Title
        '<text x="400" y="30" class="title" text-anchor="middle">Thermal Field Optimization</text>',
        
        # Before section
        '<text x="200" y="60" class="title" text-anchor="middle">Before</text>',
    ]
    
    # Before: Load bars (background)
    for i in range(n_points):
        x = 50 + i * x_scale
        bar_height = load[i] * 100
        y = 200 - bar_height
        svg.append(f'<rect x="{x}" y="{y}" width="{x_scale-2}" height="{bar_height}" '
                  f'class="load-bar" fill="#444"/>')
    
    # Before: Temperature line
    before_points = []
    T_min, T_max = np.min(T_before), np.max(T_before)
    T_range = T_max - T_min if T_max > T_min else 1
    for i in range(n_points):
        x = 50 + i * x_scale + x_scale/2
        # Scale to 0-150 range for visualization
        y = 200 - ((T_before[i] - T_min) / T_range) * 150
        before_points.append(f"{x},{y}")
    
    svg.append(f'<polyline points="{" ".join(before_points)}" class="temp-line" stroke="#f00"/>')
    
    # Before: Metrics
    svg.extend([
        '<text x="50" y="230" class="metric">',
        f'Curvature: {metrics_before.curvature:.4f} rad',
        '</text>',
        '<text x="50" y="245" class="metric">',
        f'Entropy: {metrics_before.entropy:.4f}',
        '</text>',
        '<text x="50" y="260" class="metric">',
        f'Alignment: {metrics_before.alignment_coefficient:.4f}',
        '</text>',
    ])
    
    # After section
    svg.append('<text x="600" y="60" class="title" text-anchor="middle">After AI Optimization</text>')
    
    # After: Load bars (background)
    for i in range(n_points):
        x = 450 + i * x_scale
        bar_height = load[i] * 100
        y = 200 - bar_height
        svg.append(f'<rect x="{x}" y="{y}" width="{x_scale-2}" height="{bar_height}" '
                  f'class="load-bar" fill="#444"/>')
    
    # After: Temperature line
    after_points = []
    for i in range(n_points):
        x = 450 + i * x_scale + x_scale/2
        y = 200 - ((T_after[i] - T_min) / T_range) * 150
        after_points.append(f"{x},{y}")
    
    svg.append(f'<polyline points="{" ".join(after_points)}" class="temp-line" stroke="#0f0"/>')
    
    # After: Metrics
    svg.extend([
        '<text x="450" y="230" class="metric">',
        f'Curvature: {metrics_after.curvature:.4f} rad',
        '</text>',
        '<text x="450" y="245" class="metric">',
        f'Entropy: {metrics_after.entropy:.4f}',
        '</text>',
        '<text x="450" y="260" class="metric">',
        f'Alignment: {metrics_after.alignment_coefficient:.4f}',
        '</text>',
    ])
    
    # Improvements summary
    entropy_reduction = (metrics_before.entropy - metrics_after.entropy) / metrics_before.entropy
    curvature_reduction = metrics_before.curvature - metrics_after.curvature
    alignment_improvement = metrics_after.alignment_coefficient - metrics_before.alignment_coefficient
    
    svg.extend([
        '<text x="400" y="290" class="title" text-anchor="middle">Improvements</text>',
        '<text x="400" y="310" class="metric" text-anchor="middle">',
        f'Entropy Reduction: {entropy_reduction:.1%} | ',
        f'Curvature: -{curvature_reduction:.4f} | ',
        f'Alignment: +{alignment_improvement:.4f}',
        '</text>',
        
        # Legend
        '<text x="50" y="350" class="label">Gray bars: Computational load</text>',
        '<text x="50" y="365" class="label">Red line: Temperature (before)</text>',
        '<text x="50" y="380" class="label">Green line: Temperature (after)</text>',
    ])
    
    svg.append('</svg>')
    
    return '\n'.join(svg)


def generate_optimization_timeline_svg(states, metrics_list):
    """
    Generate SVG showing optimization progress over time.
    
    Args:
        states: List of ThermalState objects
        metrics_list: List of ThermalMetrics objects
    
    Returns:
        SVG string
    """
    width = 800
    height = 400
    
    n_steps = len(metrics_list)
    x_scale = (width - 100) / max(n_steps - 1, 1)
    
    # Extract metric arrays
    curvatures = [m.curvature for m in metrics_list]
    entropies = [m.entropy for m in metrics_list]
    alignments = [m.alignment_coefficient for m in metrics_list]
    
    # Normalize for visualization
    curv_min, curv_max = min(curvatures), max(curvatures)
    entr_min, entr_max = min(entropies), max(entropies)
    align_min, align_max = min(alignments), max(alignments)
    
    def normalize(val, vmin, vmax):
        if vmax == vmin:
            return 0.5
        return (val - vmin) / (vmax - vmin)
    
    # Create SVG
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '.title{font:16px sans-serif;fill:#fff;font-weight:bold}',
        '.label{font:12px sans-serif;fill:#aaa}',
        '.metric-line{fill:none;stroke-width:2}',
        '.axis{stroke:#444;stroke-width:1}',
        '</style>',
        '<rect width="100%" height="100%" fill="#111"/>',
        
        # Title
        '<text x="400" y="30" class="title" text-anchor="middle">Optimization Timeline</text>',
        
        # Axes
        '<line x1="50" y1="50" x2="50" y2="300" class="axis"/>',
        '<line x1="50" y1="300" x2="750" y2="300" class="axis"/>',
        
        # Y-axis label
        '<text x="30" y="175" class="label" text-anchor="middle" transform="rotate(-90 30 175)">',
        'Normalized Metric Value',
        '</text>',
        
        # X-axis label
        '<text x="400" y="330" class="label" text-anchor="middle">Optimization Step</text>',
    ]
    
    # Plot curvature (red)
    curv_points = []
    for i, curv in enumerate(curvatures):
        x = 50 + i * x_scale
        y = 300 - normalize(curv, curv_min, curv_max) * 250
        curv_points.append(f"{x},{y}")
    svg.append(f'<polyline points="{" ".join(curv_points)}" class="metric-line" stroke="#f00"/>')
    
    # Plot entropy (yellow)
    entr_points = []
    for i, entr in enumerate(entropies):
        x = 50 + i * x_scale
        y = 300 - normalize(entr, entr_min, entr_max) * 250
        entr_points.append(f"{x},{y}")
    svg.append(f'<polyline points="{" ".join(entr_points)}" class="metric-line" stroke="#ff0"/>')
    
    # Plot alignment (green)
    align_points = []
    for i, align in enumerate(alignments):
        x = 50 + i * x_scale
        y = 300 - normalize(align, align_min, align_max) * 250
        align_points.append(f"{x},{y}")
    svg.append(f'<polyline points="{" ".join(align_points)}" class="metric-line" stroke="#0f0"/>')
    
    # Legend
    svg.extend([
        '<rect x="550" y="350" width="15" height="3" fill="#f00"/>',
        '<text x="570" y="355" class="label">Curvature (lower is better)</text>',
        '<rect x="550" y="365" width="15" height="3" fill="#ff0"/>',
        '<text x="570" y="370" class="label">Entropy (lower is better)</text>',
        '<rect x="550" y="380" width="15" height="3" fill="#0f0"/>',
        '<text x="570" y="385" class="label">Alignment (higher is better)</text>',
    ])
    
    svg.append('</svg>')
    
    return '\n'.join(svg)


def main():
    """Generate thermal field visualizations."""
    print("Thermal Field Visualizer")
    print("=" * 50)
    
    # Create analyzer and optimizer
    analyzer = ThermalFieldAnalyzer(baseline_temp=298.15)
    optimizer = CoolingOptimizer(alpha=0.2, beta=0.8)
    
    # Initial thermal state (suboptimal)
    T_initial = np.array([295, 310, 315, 312, 305, 298, 296, 295, 294, 293])
    load = np.array([0.2, 0.8, 0.9, 0.8, 0.6, 0.3, 0.2, 0.1, 0.1, 0.05])
    
    before_state = ThermalState(
        timestamp='2025-12-08T10:00:00',
        temperature_field=T_initial,
        computational_load=load,
        baseline_temp=298.15
    )
    
    # Analyze before
    metrics_before = analyzer.analyze_state(before_state)
    print("\nBefore Optimization:")
    print(f"  Curvature: {metrics_before.curvature:.4f}")
    print(f"  Entropy: {metrics_before.entropy:.4f}")
    print(f"  Alignment: {metrics_before.alignment_coefficient:.4f}")
    
    # Optimize
    T_optimized = T_initial.copy()
    states = [before_state]
    metrics_list = [metrics_before]
    
    for step in range(10):
        T_optimized = optimizer.optimize_temperature(T_optimized, load, dt=0.5)
        state = ThermalState(
            timestamp=f'2025-12-08T10:{step+1:02d}:00',
            temperature_field=T_optimized,
            computational_load=load,
            baseline_temp=298.15
        )
        metrics = analyzer.analyze_state(state)
        states.append(state)
        metrics_list.append(metrics)
    
    after_state = states[-1]
    metrics_after = metrics_list[-1]
    
    print("\nAfter Optimization (10 steps):")
    print(f"  Curvature: {metrics_after.curvature:.4f}")
    print(f"  Entropy: {metrics_after.entropy:.4f}")
    print(f"  Alignment: {metrics_after.alignment_coefficient:.4f}")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    
    # Comparison visualization
    comparison_svg = generate_thermal_comparison_svg(
        before_state, after_state, metrics_before, metrics_after
    )
    
    output_dir = Path(__file__).parent.parent / "growth"
    output_dir.mkdir(exist_ok=True)
    
    comparison_file = output_dir / "thermal-field-comparison.svg"
    with open(comparison_file, 'w') as f:
        f.write(comparison_svg)
    print(f"  Saved: {comparison_file}")
    
    # Timeline visualization
    timeline_svg = generate_optimization_timeline_svg(states, metrics_list)
    timeline_file = output_dir / "thermal-field-timeline.svg"
    with open(timeline_file, 'w') as f:
        f.write(timeline_svg)
    print(f"  Saved: {timeline_file}")
    
    print("\n" + "=" * 50)
    print("Thermal field visualizations generated successfully!")
    print("\nThe visualizations show how AI optimization:")
    print("  • Smooths temperature gradients (reduces curvature)")
    print("  • Aligns cooling with load (reduces entropy)")
    print("  • Improves overall system homeostasis")
    print("\nThis is 'teaching heat to speak' in action.")


if __name__ == '__main__':
    main()
