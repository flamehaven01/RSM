# engine/drift_sentinel.py - Enhanced v2.2
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

class DriftSentinel:
    """Enhanced drift monitoring with trajectory tracking."""

    def __init__(self, thresholds: Optional[Dict] = None):
        if thresholds is None:
            thresholds = {
                "di2_warning": 0.2,
                "di2_critical": 0.3,
                "ri_warning": 0.4,
                "ri_critical": 0.2,
                "trajectory_window": 5
            }
        self.thresholds = thresholds
        self.history = []

    def monitor_with_trajectory(self, di2: float, ri: float, timestamp: Optional[str] = None) -> Dict:
        """Enhanced monitoring with trajectory analysis."""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()

        # Record current state
        current_state = {
            "timestamp": timestamp,
            "di2": di2,
            "ri": ri,
            "alert": self._determine_alert_level(di2, ri)
        }

        self.history.append(current_state)

        # Maintain history window
        window_size = self.thresholds.get("trajectory_window", 5)
        if len(self.history) > window_size:
            self.history = self.history[-window_size:]

        # Calculate trajectory metrics
        trajectory_analysis = self._analyze_trajectory()

        return {
            **current_state,
            "trajectory": trajectory_analysis,
            "history_length": len(self.history),
            "thresholds": self.thresholds
        }

    def _determine_alert_level(self, di2: float, ri: float) -> str:
        """Determine alert level based on thresholds."""
        if di2 >= self.thresholds["di2_critical"] or ri <= self.thresholds["ri_critical"]:
            return "CRITICAL"
        elif di2 >= self.thresholds["di2_warning"] or ri <= self.thresholds["ri_warning"]:
            return "WARNING"
        else:
            return "STABLE"

    def _analyze_trajectory(self) -> Dict:
        """Analyze trajectory trends in the monitoring history."""
        if len(self.history) < 2:
            return {"trend": "insufficient_data", "stability": "unknown"}

        # Extract time series
        di2_values = [state["di2"] for state in self.history]
        ri_values = [state["ri"] for state in self.history]

        # Calculate trends (simple linear approximation)
        di2_trend = "increasing" if di2_values[-1] > di2_values[0] else "decreasing"
        ri_trend = "increasing" if ri_values[-1] > ri_values[0] else "decreasing"

        # Calculate stability (coefficient of variation)
        di2_stability = np.std(di2_values) / (np.mean(di2_values) + 1e-8)
        ri_stability = np.std(ri_values) / (np.mean(ri_values) + 1e-8)

        stability_level = "stable" if max(di2_stability, ri_stability) < 0.2 else "volatile"

        return {
            "di2_trend": di2_trend,
            "ri_trend": ri_trend,
            "stability": stability_level,
            "di2_volatility": di2_stability,
            "ri_volatility": ri_stability
        }