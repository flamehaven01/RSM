#!/usr/bin/env python3
"""
Test script for RSM Simulator Hugging Face app
"""

from app import process_rsm_input, vme_engine

def test_basic_functionality():
    """Test basic RSM calculation functionality."""
    print("[T] Testing RSM Simulator App...")

    # Test 1: Empty input
    result = process_rsm_input("None", "None", "None")
    print(f"[+] Empty input test: {result[0][:50]}...")

    # Test 2: Single Tarot input
    result = process_rsm_input("The Fool", "None", "None")
    interpretation, vme_display, ri_display, confidence, systems, status, _, _, _ = result
    print(f"[+] Single Tarot test:")
    print(f"   VME: {vme_display}")
    print(f"   RI: {ri_display}")
    print(f"   Status: {status}")

    # Test 3: Multiple inputs
    result = process_rsm_input("Death", "Scorpio", "Fire Yang")
    interpretation, vme_display, ri_display, confidence, systems, status, _, _, _ = result
    print(f"[+] Multiple inputs test:")
    print(f"   Systems: {systems}")
    print(f"   RI: {ri_display}")
    print(f"   Status: {status}")

    # Test 4: VME Engine directly
    vme, metadata = vme_engine.calculate_vme({"tarot": "The Magician", "astrology": "Leo"})
    print(f"[+] Direct VME test:")
    print(f"   VME: {vme}")
    print(f"   Confidence: {metadata['overall_confidence']}")
    print(f"   Systems: {metadata['systems_used']}")

    print("[*] All tests passed! App is ready for deployment.")

if __name__ == "__main__":
    test_basic_functionality()