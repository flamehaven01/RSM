#!/usr/bin/env python3
"""
RSM Simulator v2.2 - Complete Implementation
Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI
"""

import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.vme import VMEEngine
from engine.ri import calc_ri, calculate_enhanced_symbolic_conflicts
from engine.drift_sentinel import DriftSentinel
from modal.tarot import TarotOntology
from modal.saju import SajuOntology
from modal.astrology import AstrologyOntology

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RSMSimulator:
    """Main RSM Simulator class integrating all components."""

    def __init__(self, data_dir: str = "data"):
        """Initialize RSM Simulator with symbolic system databases."""
        self.data_dir = data_dir

        # Initialize symbolic systems
        try:
            self.tarot = TarotOntology(os.path.join(data_dir, "tarot_meanings.json"))
            self.saju = SajuOntology(os.path.join(data_dir, "saju_elements.json"))
            self.astrology = AstrologyOntology(os.path.join(data_dir, "astrology_mappings.json"))

            # Initialize core engines
            self.vme_engine = VMEEngine(self.tarot, self.saju, self.astrology)
            self.drift_sentinel = DriftSentinel()

            logger.info("RSM Simulator v2.2 initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize RSM Simulator: {e}")
            raise

    def process_symbolic_input(self, symbolic_input: Dict, with_audit: bool = True) -> Dict:
        """Process symbolic input through complete RSM pipeline."""

        if with_audit:
            vme, audit_trail = self.vme_engine.calc_vme_with_audit_trail(symbolic_input)
        else:
            vme = self.vme_engine.calc_vme(symbolic_input)
            audit_trail = None

        # Calculate Resonance Index
        ri = calc_ri(vme)

        # Calculate DI2 (Drift Index squared) - for single point, use minimal variance
        di2 = 0.01  # Minimal drift for single calculation

        # Monitor drift
        drift_report = self.drift_sentinel.monitor_with_trajectory(di2, ri)

        # Compile results
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": symbolic_input,
            "vme": vme.tolist(),
            "resonance_index": ri,
            "drift_index_squared": di2,
            "drift_status": drift_report["alert"],
            "drift_analysis": drift_report,
            "version": "2.2"
        }

        if audit_trail:
            result["audit_trail"] = audit_trail

        return result

    def run_validation_suite(self) -> Dict:
        """Run comprehensive validation tests."""
        logger.info("Running RSM validation suite...")

        validation_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": [],
            "overall_status": "UNKNOWN"
        }

        # Test 1: Basic VME calculation
        try:
            test_input = {"tarot": "The Fool", "astrology": "Aries"}
            result = self.process_symbolic_input(test_input, with_audit=False)

            # Validate VME is normalized
            vme_norm = np.linalg.norm(result["vme"])
            if abs(vme_norm - 1.0) < 1e-6:
                validation_results["tests_passed"] += 1
                validation_results["test_results"].append({
                    "test": "VME_normalization",
                    "status": "PASS",
                    "details": f"VME norm: {vme_norm}"
                })
            else:
                validation_results["tests_failed"] += 1
                validation_results["test_results"].append({
                    "test": "VME_normalization",
                    "status": "FAIL",
                    "details": f"VME norm: {vme_norm}, expected: 1.0"
                })

        except Exception as e:
            validation_results["tests_failed"] += 1
            validation_results["test_results"].append({
                "test": "VME_normalization",
                "status": "ERROR",
                "details": str(e)
            })

        # Test 2: RI range validation
        try:
            test_input = {"saju": "Fire Yang", "astrology": "Leo"}
            result = self.process_symbolic_input(test_input, with_audit=False)

            ri = result["resonance_index"]
            if 0.0 <= ri <= 1.0:
                validation_results["tests_passed"] += 1
                validation_results["test_results"].append({
                    "test": "RI_range_validation",
                    "status": "PASS",
                    "details": f"RI: {ri}"
                })
            else:
                validation_results["tests_failed"] += 1
                validation_results["test_results"].append({
                    "test": "RI_range_validation",
                    "status": "FAIL",
                    "details": f"RI: {ri}, expected: [0.0, 1.0]"
                })

        except Exception as e:
            validation_results["tests_failed"] += 1
            validation_results["test_results"].append({
                "test": "RI_range_validation",
                "status": "ERROR",
                "details": str(e)
            })

        # Test 3: System info validation
        try:
            info = self.vme_engine.get_system_info()
            required_keys = ["tarot_cards", "saju_pillars", "astrology_signs", "version"]

            if all(key in info for key in required_keys) and info["version"] == "2.2":
                validation_results["tests_passed"] += 1
                validation_results["test_results"].append({
                    "test": "system_info_validation",
                    "status": "PASS",
                    "details": f"System info: {info}"
                })
            else:
                validation_results["tests_failed"] += 1
                validation_results["test_results"].append({
                    "test": "system_info_validation",
                    "status": "FAIL",
                    "details": f"Missing keys or wrong version: {info}"
                })

        except Exception as e:
            validation_results["tests_failed"] += 1
            validation_results["test_results"].append({
                "test": "system_info_validation",
                "status": "ERROR",
                "details": str(e)
            })

        # Test 4: Drift monitoring
        try:
            # Simulate multiple RI values for drift analysis
            ri_values = [0.8, 0.75, 0.7, 0.85, 0.9]
            di2_values = [0.01, 0.02, 0.015, 0.025, 0.005]

            for ri, di2 in zip(ri_values, di2_values):
                drift_report = self.drift_sentinel.monitor_with_trajectory(di2, ri)

            # Check if trajectory analysis is working
            final_report = self.drift_sentinel.monitor_with_trajectory(0.01, 0.85)
            if "trajectory" in final_report and "stability" in final_report["trajectory"]:
                validation_results["tests_passed"] += 1
                validation_results["test_results"].append({
                    "test": "drift_monitoring",
                    "status": "PASS",
                    "details": f"Trajectory analysis: {final_report['trajectory']}"
                })
            else:
                validation_results["tests_failed"] += 1
                validation_results["test_results"].append({
                    "test": "drift_monitoring",
                    "status": "FAIL",
                    "details": f"Missing trajectory data: {final_report}"
                })

        except Exception as e:
            validation_results["tests_failed"] += 1
            validation_results["test_results"].append({
                "test": "drift_monitoring",
                "status": "ERROR",
                "details": str(e)
            })

        # Determine overall status
        total_tests = validation_results["tests_passed"] + validation_results["tests_failed"]
        if validation_results["tests_failed"] == 0:
            validation_results["overall_status"] = "ALL_PASS"
        elif validation_results["tests_passed"] > validation_results["tests_failed"]:
            validation_results["overall_status"] = "MOSTLY_PASS"
        else:
            validation_results["overall_status"] = "FAIL"

        logger.info(f"Validation complete: {validation_results['tests_passed']}/{total_tests} tests passed")
        return validation_results

    def demo_run(self) -> Dict:
        """Run demonstration of RSM capabilities."""
        logger.info("Running RSM demonstration...")

        demo_inputs = [
            {"tarot": "Death", "astrology": "Scorpio"},
            {"tarot": "The Magician", "saju": "Fire Yang"},
            {"saju": "Water Yang", "astrology": "Cancer"},
            {"tarot": "The Tower", "saju": "Metal Yin", "astrology": "Aries"}
        ]

        demo_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "demo_cases": [],
            "summary": {}
        }

        for i, test_input in enumerate(demo_inputs, 1):
            logger.info(f"Processing demo case {i}: {test_input}")

            try:
                result = self.process_symbolic_input(test_input, with_audit=True)
                demo_results["demo_cases"].append({
                    "case_number": i,
                    "input": test_input,
                    "vme": result["vme"],
                    "resonance_index": result["resonance_index"],
                    "drift_status": result["drift_status"],
                    "confidence": result["audit_trail"]["overall_confidence"] if "audit_trail" in result else 0.5
                })

            except Exception as e:
                logger.error(f"Demo case {i} failed: {e}")
                demo_results["demo_cases"].append({
                    "case_number": i,
                    "input": test_input,
                    "error": str(e)
                })

        # Calculate summary statistics
        successful_cases = [case for case in demo_results["demo_cases"] if "error" not in case]

        if successful_cases:
            ri_values = [case["resonance_index"] for case in successful_cases]
            demo_results["summary"] = {
                "successful_cases": len(successful_cases),
                "failed_cases": len(demo_results["demo_cases"]) - len(successful_cases),
                "average_ri": np.mean(ri_values),
                "ri_std": np.std(ri_values),
                "min_ri": np.min(ri_values),
                "max_ri": np.max(ri_values)
            }

        return demo_results

def main():
    """Main entry point for RSM Simulator."""
    print("=" * 50)
    print("RSM Simulator v2.2")
    print("Resonant Structures of Meaning")
    print("=" * 50)

    try:
        # Initialize simulator
        simulator = RSMSimulator()

        # Run validation suite
        print("\n[>] Running validation suite...")
        validation_results = simulator.run_validation_suite()
        print(f"[+] Validation: {validation_results['overall_status']}")
        print(f"    Tests passed: {validation_results['tests_passed']}")
        print(f"    Tests failed: {validation_results['tests_failed']}")

        # Run demonstration
        print("\n[>] Running demonstration...")
        demo_results = simulator.demo_run()

        if demo_results["summary"]:
            summary = demo_results["summary"]
            print(f"[+] Demo complete:")
            print(f"    Successful cases: {summary['successful_cases']}")
            print(f"    Average RI: {summary['average_ri']:.3f}")
            print(f"    RI range: [{summary['min_ri']:.3f}, {summary['max_ri']:.3f}]")

        # Interactive mode
        print("\n[>] Enter interactive mode (press Enter for sample, 'q' to quit):")

        while True:
            user_input = input("\nRSM> ").strip()

            if user_input.lower() in ['q', 'quit', 'exit']:
                break
            elif user_input == "":
                # Sample input
                sample_input = {"tarot": "The Fool", "astrology": "Aries"}
                print(f"[>] Processing sample: {sample_input}")
                result = simulator.process_symbolic_input(sample_input)
                print(f"[+] VME: {result['vme']}")
                print(f"[+] RI: {result['resonance_index']:.3f}")
                print(f"[+] Status: {result['drift_status']}")
            else:
                try:
                    # Try to parse as JSON
                    symbolic_input = json.loads(user_input)
                    result = simulator.process_symbolic_input(symbolic_input)
                    print(f"[+] VME: {result['vme']}")
                    print(f"[+] RI: {result['resonance_index']:.3f}")
                    print(f"[+] Status: {result['drift_status']}")
                except json.JSONDecodeError:
                    print("[-] Invalid JSON format. Example: {\"tarot\": \"The Fool\", \"astrology\": \"Aries\"}")
                except Exception as e:
                    print(f"[-] Error: {e}")

        print("\n[+] RSM Simulator session complete.")

    except Exception as e:
        print(f"[-] Fatal error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())