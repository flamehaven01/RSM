#!/usr/bin/env python3
"""
Test suite for RSM Simulator v2.2
Comprehensive validation and unit tests
"""

import unittest
import numpy as np
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.vme import VMEEngine
from engine.ri import calc_ri, calculate_enhanced_symbolic_conflicts
from engine.drift_sentinel import DriftSentinel
from modal.tarot import TarotOntology
from modal.saju import SajuOntology
from modal.astrology import AstrologyOntology
from rsm_simulator import RSMSimulator

class TestRSMComponents(unittest.TestCase):
    """Test individual RSM components."""

    @classmethod
    def setUpClass(cls):
        """Set up test data and components."""
        cls.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

        # Initialize symbolic systems
        cls.tarot = TarotOntology(os.path.join(cls.data_dir, "tarot_meanings.json"))
        cls.saju = SajuOntology(os.path.join(cls.data_dir, "saju_elements.json"))
        cls.astrology = AstrologyOntology(os.path.join(cls.data_dir, "astrology_mappings.json"))

        # Initialize VME engine
        cls.vme_engine = VMEEngine(cls.tarot, cls.saju, cls.astrology)

    def test_vme_normalization(self):
        """Test VME vector normalization."""
        test_input = {"tarot": "The Fool"}
        vme = self.vme_engine.calc_vme(test_input)

        # Check normalization
        norm = np.linalg.norm(vme)
        self.assertAlmostEqual(norm, 1.0, places=6,
                              msg=f"VME not normalized: {norm}")

        # Check dimensions
        self.assertEqual(len(vme), 3,
                        msg=f"VME should have 3 dimensions, got {len(vme)}")

    def test_vme_with_multiple_systems(self):
        """Test VME calculation with multiple symbolic systems."""
        test_input = {
            "tarot": "Death",
            "saju": "Fire Yang",
            "astrology": "Scorpio"
        }

        vme = self.vme_engine.calc_vme(test_input)

        # Verify normalization
        norm = np.linalg.norm(vme)
        self.assertAlmostEqual(norm, 1.0, places=6)

        # Check that all values are finite
        self.assertTrue(np.all(np.isfinite(vme)),
                       msg="VME contains non-finite values")

    def test_vme_audit_trail(self):
        """Test VME calculation with audit trail."""
        test_input = {"tarot": "The Magician", "astrology": "Leo"}
        vme, audit = self.vme_engine.calc_vme_with_audit_trail(test_input)

        # Check audit structure
        required_keys = ["timestamp", "input", "validation_steps",
                        "calculation_steps", "systems_used"]
        for key in required_keys:
            self.assertIn(key, audit, msg=f"Missing audit key: {key}")

        # Check systems used
        self.assertIn("tarot", audit["systems_used"])
        self.assertIn("astrology", audit["systems_used"])

    def test_ri_calculation(self):
        """Test Resonance Index calculation."""
        # Test with known VME
        vme = np.array([0.5, 0.5, 0.707])  # Approximately normalized
        vme = vme / np.linalg.norm(vme)  # Ensure normalization

        ri = calc_ri(vme)

        # RI should be in [0, 1] range
        self.assertGreaterEqual(ri, 0.0, msg=f"RI below 0: {ri}")
        self.assertLessEqual(ri, 1.0, msg=f"RI above 1: {ri}")

        # RI should be finite
        self.assertTrue(np.isfinite(ri), msg=f"RI is not finite: {ri}")

    def test_ri_with_context_weights(self):
        """Test RI calculation with context weights."""
        vme = np.array([0.577, 0.577, 0.577])  # Normalized
        context_weights = {"chaos": 0.5, "rebirth": 1.0, "transformation": 0.8}

        ri = calc_ri(vme, context_weights)

        self.assertGreaterEqual(ri, 0.0)
        self.assertLessEqual(ri, 1.0)

    def test_symbolic_conflicts(self):
        """Test enhanced symbolic conflicts calculation."""
        # High conflict scenario
        high_conflict_vme = np.array([1.0, 0.0, 0.0])
        conflict_high = calculate_enhanced_symbolic_conflicts(high_conflict_vme)

        # Low conflict scenario
        low_conflict_vme = np.array([0.577, 0.577, 0.577])
        conflict_low = calculate_enhanced_symbolic_conflicts(low_conflict_vme)

        # High conflict should produce higher penalty
        self.assertGreater(conflict_high, conflict_low,
                          msg="High conflict should produce higher penalty")

        # Conflicts should be non-negative and capped
        self.assertGreaterEqual(conflict_high, 0.0)
        self.assertLessEqual(conflict_high, 0.3)

    def test_drift_sentinel(self):
        """Test DriftSentinel monitoring."""
        sentinel = DriftSentinel()

        # Test stable scenario
        stable_di2, stable_ri = 0.05, 0.8
        report = sentinel.monitor_with_trajectory(stable_di2, stable_ri)

        self.assertEqual(report["alert"], "STABLE")
        self.assertIn("trajectory", report)

        # Test warning scenario
        warning_di2, warning_ri = 0.25, 0.3
        report = sentinel.monitor_with_trajectory(warning_di2, warning_ri)

        self.assertIn(report["alert"], ["WARNING", "CRITICAL"])

    def test_tarot_ontology(self):
        """Test Tarot ontology functionality."""
        # Test card parsing
        dimensions = self.tarot.parse_card("The Fool")
        required_dims = ["chaos", "rebirth", "transformation"]

        for dim in required_dims:
            self.assertIn(dim, dimensions)
            self.assertGreaterEqual(dimensions[dim], 0.0)
            self.assertLessEqual(dimensions[dim], 1.0)

        # Test metadata
        metadata = self.tarot.get_card_metadata("Death")
        self.assertIn("element", metadata)

        # Test confidence level
        confidence = self.tarot.get_confidence_level("The Magician")
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_invalid_inputs(self):
        """Test handling of invalid inputs."""
        # Invalid tarot card
        with self.assertRaises(ValueError):
            self.vme_engine.calc_vme({"tarot": "Invalid Card"})

        # Invalid data type
        with self.assertRaises(TypeError):
            self.vme_engine.calc_vme("not a dict")

        # Empty input
        vme = self.vme_engine.calc_vme({})
        self.assertEqual(len(vme), 3)
        self.assertAlmostEqual(np.linalg.norm(vme), 1.0, places=6)

class TestRSMSimulator(unittest.TestCase):
    """Test complete RSM Simulator functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up RSM Simulator for testing."""
        cls.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        cls.simulator = RSMSimulator(cls.data_dir)

    def test_simulator_initialization(self):
        """Test simulator initialization."""
        info = self.simulator.vme_engine.get_system_info()
        self.assertEqual(info["version"], "2.2")
        self.assertGreater(info["tarot_cards"], 0)
        self.assertGreater(info["saju_pillars"], 0)
        self.assertGreater(info["astrology_signs"], 0)

    def test_symbolic_input_processing(self):
        """Test complete symbolic input processing."""
        test_input = {"tarot": "Death", "astrology": "Scorpio"}
        result = self.simulator.process_symbolic_input(test_input)

        # Check result structure
        required_keys = ["timestamp", "input", "vme", "resonance_index",
                        "drift_status", "version"]
        for key in required_keys:
            self.assertIn(key, result)

        # Check RI range
        ri = result["resonance_index"]
        self.assertGreaterEqual(ri, 0.0)
        self.assertLessEqual(ri, 1.0)

        # Check VME
        vme = result["vme"]
        self.assertEqual(len(vme), 3)
        vme_norm = np.linalg.norm(vme)
        self.assertAlmostEqual(vme_norm, 1.0, places=6)

    def test_validation_suite(self):
        """Test the built-in validation suite."""
        results = self.simulator.run_validation_suite()

        self.assertIn("overall_status", results)
        self.assertGreater(results["tests_passed"], 0)

        # Should have passed most tests
        total_tests = results["tests_passed"] + results["tests_failed"]
        pass_rate = results["tests_passed"] / total_tests
        self.assertGreater(pass_rate, 0.5, msg="Less than 50% of tests passed")

class TestMathematicalProperties(unittest.TestCase):
    """Test mathematical properties of RSM components."""

    def test_vme_mathematical_properties(self):
        """Test mathematical properties of VME calculation."""
        # Test linearity properties
        tarot = TarotOntology(os.path.join("data", "tarot_meanings.json"))
        saju = SajuOntology(os.path.join("data", "saju_elements.json"))
        astrology = AstrologyOntology(os.path.join("data", "astrology_mappings.json"))

        vme_engine = VMEEngine(tarot, saju, astrology)

        # Test with single system
        single_input = {"tarot": "The Fool"}
        vme_single = vme_engine.calc_vme(single_input)

        # Test determinism - same input should give same output
        vme_single_2 = vme_engine.calc_vme(single_input)
        np.testing.assert_array_almost_equal(vme_single, vme_single_2,
                                           decimal=10,
                                           err_msg="VME calculation not deterministic")

    def test_ri_mathematical_bounds(self):
        """Test mathematical bounds of RI calculation."""
        # Test extreme cases
        extreme_vmes = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
            np.array([0.577, 0.577, 0.577])  # Balanced
        ]

        for vme in extreme_vmes:
            ri = calc_ri(vme)
            self.assertGreaterEqual(ri, 0.0, msg=f"RI negative for VME {vme}")
            self.assertLessEqual(ri, 1.0, msg=f"RI > 1 for VME {vme}")
            self.assertTrue(np.isfinite(ri), msg=f"RI not finite for VME {vme}")

def run_tests():
    """Run all tests and return results."""
    print("=" * 60)
    print("RSM Simulator v2.2 - Test Suite")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Add test classes
    test_classes = [TestRSMComponents, TestRSMSimulator, TestMathematicalProperties]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.splitlines()[-1]}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.splitlines()[-1]}")

    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
    print(f"\nSuccess rate: {success_rate*100:.1f}%")

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)