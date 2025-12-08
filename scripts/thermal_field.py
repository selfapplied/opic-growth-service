#!/usr/bin/env python3
"""
Thermal Field Module — Data Center Cooling as Field Dynamics

Maps data center thermal management to OPIC field equations.
Implements thermal curvature, entropy reduction, and homeostasis metrics.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, field as dc_field
import json


# Numerical stability constant
EPSILON = 1e-10

# Temperature-load scaling coefficient (K per unit load)
# Justification: Typical data centers run 5-10K warmer under high load
# This allows efficiency gains by not over-cooling high-load zones
TEMP_LOAD_COEFFICIENT = 5.0


@dataclass
class ThermalState:
    """Represents a thermal state with temperature field and load."""
    timestamp: str
    temperature_field: np.ndarray
    computational_load: np.ndarray
    baseline_temp: float = 298.15  # Kelvin (25°C)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'timestamp': self.timestamp,
            'temperature_field': self.temperature_field.tolist(),
            'computational_load': self.computational_load.tolist(),
            'baseline_temp': self.baseline_temp
        }


@dataclass
class ThermalMetrics:
    """Thermal field analysis metrics."""
    curvature: float
    entropy: float
    homeostasis_score: float
    gradient_magnitude: float
    alignment_coefficient: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'curvature': float(self.curvature),
            'entropy': float(self.entropy),
            'homeostasis_score': float(self.homeostasis_score),
            'gradient_magnitude': float(self.gradient_magnitude),
            'alignment_coefficient': float(self.alignment_coefficient)
        }


class ThermalFieldAnalyzer:
    """
    Analyzes thermal fields in data center contexts.
    Maps temperature distributions to field curvature and entropy.
    """
    
    def __init__(self, baseline_temp: float = 298.15):
        """
        Initialize thermal field analyzer.
        
        Args:
            baseline_temp: Reference temperature in Kelvin (default 25°C)
        """
        self.baseline_temp = baseline_temp
        self.history: List[ThermalState] = []
        
    def thermal_curvature(self, 
                         T_field: np.ndarray, 
                         T_baseline: Optional[float] = None) -> float:
        """
        Compute thermal curvature from temperature field.
        
        κ(x,t) = tan⁻¹(|∇T|/T₀)
        
        Args:
            T_field: Temperature field array
            T_baseline: Reference temperature (uses instance default if None)
            
        Returns:
            Thermal curvature value
        """
        if T_baseline is None:
            T_baseline = self.baseline_temp
            
        # Compute gradient magnitude
        gradient = np.gradient(T_field)
        if isinstance(gradient, list):
            grad_magnitude = np.sqrt(sum(g**2 for g in gradient))
        else:
            grad_magnitude = np.abs(gradient)
            
        # Average gradient magnitude
        avg_grad = np.mean(grad_magnitude)
        
        # Compute curvature
        curvature = np.arctan(avg_grad / T_baseline)
        
        return float(curvature)
    
    def thermal_entropy(self, 
                       T_field: np.ndarray, 
                       load_field: np.ndarray) -> float:
        """
        Compute thermal entropy from temperature and load distribution.
        
        S_thermal = -Σ p_i ln p_i
        
        Where p_i represents normalized temperature-load coupling.
        
        Args:
            T_field: Temperature field
            load_field: Computational load field
            
        Returns:
            Thermal entropy value
        """
        # Normalize fields to probability distributions
        T_norm = np.abs(T_field - self.baseline_temp)
        T_norm = T_norm / (np.sum(T_norm) + EPSILON)
        
        load_norm = load_field / (np.sum(load_field) + EPSILON)
        
        # Compute coupling distribution
        coupling = T_norm * load_norm
        coupling = coupling / (np.sum(coupling) + EPSILON)
        
        # Remove zeros to avoid log(0)
        coupling_nonzero = coupling[coupling > EPSILON]
        
        # Compute entropy
        entropy = -np.sum(coupling_nonzero * np.log(coupling_nonzero))
        
        return float(entropy)
    
    def entropy_reduction(self, 
                         T_before: np.ndarray, 
                         T_after: np.ndarray,
                         load: np.ndarray) -> float:
        """
        Measure entropy reduction from optimization.
        
        ΔS = (S_before - S_after) / S_before
        
        Args:
            T_before: Temperature field before optimization
            T_after: Temperature field after optimization
            load: Computational load field
            
        Returns:
            Fractional entropy reduction (0 to 1)
        """
        S_before = self.thermal_entropy(T_before, load)
        S_after = self.thermal_entropy(T_after, load)
        
        if S_before < EPSILON:
            return 0.0
            
        reduction = (S_before - S_after) / S_before
        
        return float(reduction)
    
    def homeostasis_score(self, 
                         T_actual: np.ndarray, 
                         T_target: np.ndarray) -> float:
        """
        Measure how well system maintains thermal equilibrium.
        
        H = 1 - mean(|T_actual - T_target|) / std(T_target)
        
        Higher score indicates better homeostasis.
        
        Args:
            T_actual: Actual temperature field
            T_target: Target temperature field
            
        Returns:
            Homeostasis score (0 to 1, higher is better)
        """
        deviation = np.abs(T_actual - T_target)
        mean_dev = np.mean(deviation)
        std_target = np.std(T_target)
        
        if std_target < EPSILON:
            # If target is constant, perfect match gives score of 1
            return 1.0 if mean_dev < EPSILON else 0.0
            
        score = 1.0 - (mean_dev / std_target)
        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
        
        return float(score)
    
    def gradient_magnitude(self, T_field: np.ndarray) -> float:
        """
        Compute average gradient magnitude of temperature field.
        
        |∇T| = √((∂T/∂x)² + (∂T/∂y)² + ...)
        
        Args:
            T_field: Temperature field
            
        Returns:
            Average gradient magnitude
        """
        gradient = np.gradient(T_field)
        if isinstance(gradient, list):
            grad_mag = np.sqrt(sum(g**2 for g in gradient))
        else:
            grad_mag = np.abs(gradient)
            
        return float(np.mean(grad_mag))
    
    def alignment_coefficient(self, 
                             T_field: np.ndarray, 
                             load_field: np.ndarray) -> float:
        """
        Measure alignment between temperature and load distributions.
        
        A = correlation(T_gradient, load_gradient)
        
        High alignment means cooling follows load (good).
        Low alignment means wasted cooling (bad).
        
        Args:
            T_field: Temperature field
            load_field: Computational load field
            
        Returns:
            Alignment coefficient (-1 to 1, higher is better)
        """
        # Normalize both fields
        T_norm = (T_field - np.mean(T_field)) / (np.std(T_field) + EPSILON)
        load_norm = (load_field - np.mean(load_field)) / (np.std(load_field) + EPSILON)
        
        # Compute correlation
        correlation = np.mean(T_norm * load_norm)
        
        return float(correlation)
    
    def analyze_state(self, 
                     state: ThermalState,
                     target_temp: Optional[np.ndarray] = None) -> ThermalMetrics:
        """
        Perform complete thermal field analysis on a state.
        
        Args:
            state: ThermalState to analyze
            target_temp: Target temperature field (uses baseline if None)
            
        Returns:
            ThermalMetrics with all computed values
        """
        if target_temp is None:
            target_temp = np.ones_like(state.temperature_field) * state.baseline_temp
            
        metrics = ThermalMetrics(
            curvature=self.thermal_curvature(state.temperature_field, state.baseline_temp),
            entropy=self.thermal_entropy(state.temperature_field, state.computational_load),
            homeostasis_score=self.homeostasis_score(state.temperature_field, target_temp),
            gradient_magnitude=self.gradient_magnitude(state.temperature_field),
            alignment_coefficient=self.alignment_coefficient(
                state.temperature_field, 
                state.computational_load
            )
        )
        
        # Store in history
        self.history.append(state)
        
        return metrics
    
    def optimization_summary(self, 
                            before: ThermalState,
                            after: ThermalState,
                            target_temp: Optional[np.ndarray] = None) -> Dict:
        """
        Summarize optimization results comparing before and after states.
        
        Args:
            before: ThermalState before optimization
            after: ThermalState after optimization
            target_temp: Target temperature field
            
        Returns:
            Dictionary with optimization metrics
        """
        metrics_before = self.analyze_state(before, target_temp)
        metrics_after = self.analyze_state(after, target_temp)
        
        entropy_reduction = self.entropy_reduction(
            before.temperature_field,
            after.temperature_field,
            before.computational_load
        )
        
        summary = {
            'before': metrics_before.to_dict(),
            'after': metrics_after.to_dict(),
            'improvements': {
                'entropy_reduction': entropy_reduction,
                'curvature_reduction': metrics_before.curvature - metrics_after.curvature,
                'homeostasis_improvement': metrics_after.homeostasis_score - metrics_before.homeostasis_score,
                'gradient_reduction': metrics_before.gradient_magnitude - metrics_after.gradient_magnitude,
                'alignment_improvement': metrics_after.alignment_coefficient - metrics_before.alignment_coefficient
            }
        }
        
        return summary


class CoolingOptimizer:
    """
    Simulates cooling optimization as a field morphism.
    Traditional cooling: C_cool: Load → Temperature (constant)
    Optimized cooling: C_AI: (Load, Airflow, Time) → Temperature (adaptive)
    """
    
    def __init__(self, alpha: float = 0.1, beta: float = 0.5):
        """
        Initialize cooling optimizer.
        
        Args:
            alpha: Thermal diffusivity (airflow coefficient)
            beta: Load coupling coefficient
        """
        self.alpha = alpha  # Airflow responsiveness
        self.beta = beta    # Load sensitivity
        
    def optimize_temperature(self, 
                            T_current: np.ndarray,
                            load: np.ndarray,
                            dt: float = 1.0) -> np.ndarray:
        """
        Apply cooling optimization step.
        
        ∂T/∂t = α∇²T - β(T - T_load)
        
        Args:
            T_current: Current temperature field
            load: Computational load field
            dt: Time step
            
        Returns:
            Optimized temperature field
        """
        # Convert load to target temperature
        # Higher load → slightly higher optimal temperature (efficiency)
        T_load = 298.15 + TEMP_LOAD_COEFFICIENT * (load / (np.max(load) + EPSILON))
        
        # Apply Laplacian (diffusion term)
        # Note: For 1D arrays, this computes second derivative via finite differences
        # For proper multi-dimensional Laplacian, use scipy.ndimage.laplace
        laplacian = np.gradient(np.gradient(T_current))
        if isinstance(laplacian, list):
            laplacian_sum = sum(laplacian)
        else:
            laplacian_sum = laplacian
            
        # Apply field equation
        dT_dt = self.alpha * laplacian_sum - self.beta * (T_current - T_load)
        
        # Update temperature
        T_new = T_current + dt * dT_dt
        
        return T_new


def get_thermal_field_metadata() -> Dict:
    """
    Get metadata about the thermal field module.
    
    Returns:
        Dictionary with module metadata
    """
    return {
        'name': 'Thermal Field Module',
        'version': '1.0',
        'description': 'Data center cooling optimization as field dynamics',
        'components': [
            {
                'name': 'ThermalFieldAnalyzer',
                'purpose': 'Analyze temperature fields as curvature and entropy'
            },
            {
                'name': 'CoolingOptimizer',
                'purpose': 'Optimize cooling as adaptive field morphism'
            }
        ],
        'metrics': [
            'thermal_curvature',
            'thermal_entropy',
            'homeostasis_score',
            'gradient_magnitude',
            'alignment_coefficient'
        ],
        'field_equations': [
            'κ(x,t) = tan⁻¹(|∇T|/T₀)',
            'S_thermal = -Σ p_i ln p_i',
            '∂T/∂t = α∇²T - β(T - T_load)'
        ]
    }


if __name__ == '__main__':
    # Example usage
    print("Thermal Field Module — Demo")
    print("=" * 50)
    
    # Create sample thermal state (1D for simplicity)
    T_before = np.array([300, 305, 310, 308, 302, 299, 298, 297, 296, 295])  # Kelvin
    load = np.array([0.2, 0.8, 0.9, 0.7, 0.3, 0.1, 0.05, 0.1, 0.2, 0.15])
    
    before_state = ThermalState(
        timestamp='2025-12-08T09:00:00',
        temperature_field=T_before,
        computational_load=load,
        baseline_temp=298.15
    )
    
    # Analyze before state
    analyzer = ThermalFieldAnalyzer()
    metrics_before = analyzer.analyze_state(before_state)
    
    print("\nBefore Optimization:")
    print(f"  Curvature: {metrics_before.curvature:.4f}")
    print(f"  Entropy: {metrics_before.entropy:.4f}")
    print(f"  Homeostasis: {metrics_before.homeostasis_score:.4f}")
    print(f"  Alignment: {metrics_before.alignment_coefficient:.4f}")
    
    # Apply optimization
    optimizer = CoolingOptimizer(alpha=0.1, beta=0.5)
    T_after = optimizer.optimize_temperature(T_before, load, dt=1.0)
    
    after_state = ThermalState(
        timestamp='2025-12-08T09:01:00',
        temperature_field=T_after,
        computational_load=load,
        baseline_temp=298.15
    )
    
    # Get optimization summary
    summary = analyzer.optimization_summary(before_state, after_state)
    
    print("\nAfter Optimization:")
    print(f"  Curvature: {summary['after']['curvature']:.4f}")
    print(f"  Entropy: {summary['after']['entropy']:.4f}")
    print(f"  Homeostasis: {summary['after']['homeostasis_score']:.4f}")
    print(f"  Alignment: {summary['after']['alignment_coefficient']:.4f}")
    
    print("\nImprovements:")
    print(f"  Entropy Reduction: {summary['improvements']['entropy_reduction']:.2%}")
    print(f"  Curvature Reduction: {summary['improvements']['curvature_reduction']:.4f}")
    print(f"  Homeostasis Gain: {summary['improvements']['homeostasis_improvement']:.4f}")
    print(f"  Alignment Gain: {summary['improvements']['alignment_improvement']:.4f}")
    
    print("\n" + "=" * 50)
    print("Teaching heat to speak...")
