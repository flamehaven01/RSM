# RSM Engine Package
# Resonant Structures of Meaning - Core Implementation

from .vme import VMEEngine
from .ri import calc_ri, calculate_enhanced_symbolic_conflicts
from .drift_sentinel import DriftSentinel

__version__ = "2.2"
__all__ = ["VMEEngine", "calc_ri", "calculate_enhanced_symbolic_conflicts", "DriftSentinel"]