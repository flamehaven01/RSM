# engine/ri.py - Enhanced Resonance Index v2.2
import numpy as np
from typing import Dict, Optional

def calc_ri(vme: np.ndarray, context_weights: Optional[Dict] = None,
           confidence_factor: float = 1.0) -> float:
    """Enhanced RI calculation with confidence weighting."""
    dims = ["chaos", "rebirth", "transformation"]

    if context_weights is None:
        context_weights = {dim: 1.0 for dim in dims}

    # Ensure we have weights for all dimensions
    weights = np.array([context_weights.get(dim, 1.0) for dim in dims])

    # Weighted projection
    projection = np.dot(vme, weights)

    # Normalization factor
    norm_factor = np.sqrt(np.sum(weights**2))
    if norm_factor == 0:
        raise ValueError("Context weights normalization factor is zero")

    weighted_projection = projection / norm_factor

    # Enhanced discordance penalty
    penalty = calculate_enhanced_symbolic_conflicts(vme)

    # Apply confidence factor
    ri_raw = weighted_projection - penalty
    ri_adjusted = ri_raw * confidence_factor

    # Clamp to [0, 1] range
    return max(0.0, min(1.0, ri_adjusted))

def calculate_enhanced_symbolic_conflicts(vme: np.ndarray) -> float:
    """Enhanced conflict calculation with adaptive penalties."""
    chaos, rebirth, transformation = vme

    # Primary conflicts (opposing forces)
    conflict_1 = abs(chaos - rebirth) * 0.15  # Chaos vs stability
    conflict_2 = abs(rebirth - transformation) * 0.1  # Different change types
    conflict_3 = abs(chaos - transformation) * 0.12  # Destructive vs constructive

    # Secondary conflicts (adaptive based on magnitudes)
    high_chaos_penalty = max(0, chaos - 0.8) * 0.05  # Excessive chaos
    low_energy_penalty = max(0, 0.2 - min(chaos, rebirth, transformation)) * 0.08  # Stagnation

    total_penalty = conflict_1 + conflict_2 + conflict_3 + high_chaos_penalty + low_energy_penalty

    return min(0.3, total_penalty)  # Cap maximum penalty at 30%