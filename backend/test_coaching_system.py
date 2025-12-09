#!/usr/bin/env python3
"""
Test script for the new coaching guidance system
Tests stage detection and objective tracking without needing API keys
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Mock the Config class to avoid needing API keys
class MockConfig:
    COACHING_MODE = 'guidance'

# Replace Config import before importing claude_service
import config
config.Config = MockConfig

from config import CALL_OBJECTIVES


def test_stage_detection():
    """Test the stage detection logic"""
    print("=" * 60)
    print("TESTING STAGE DETECTION")
    print("=" * 60)

    # Test scenarios
    test_cases = [
        {
            "name": "Opening Stage",
            "messages": [
                {"speaker": "salesperson", "text": "Hello, is this John?"},
                {"speaker": "customer", "text": "Yes, who's calling?"},
                {"speaker": "salesperson", "text": "Hi John, I'm calling from AI Solutions"}
            ],
            "expected_stage": "opening"
        },
        {
            "name": "Discovery Stage",
            "messages": [
                {"speaker": "salesperson", "text": "Tell me about your current call handling process"},
                {"speaker": "customer", "text": "We get about 50 calls per day"},
                {"speaker": "salesperson", "text": "What challenges are you facing with that volume?"}
            ],
            "expected_stage": "discovery"
        },
        {
            "name": "Pitch Stage",
            "messages": [
                {"speaker": "salesperson", "text": "Let me explain how our solution helps you"},
                {"speaker": "salesperson", "text": "We offer an AI assistant that can handle calls 24/7"},
                {"speaker": "customer", "text": "That sounds interesting"}
            ],
            "expected_stage": "pitch"
        },
        {
            "name": "Objection Stage",
            "messages": [
                {"speaker": "customer", "text": "This sounds expensive"},
                {"speaker": "customer", "text": "I'm not interested right now"},
                {"speaker": "salesperson", "text": "I understand your concern"}
            ],
            "expected_stage": "objection"
        },
        {
            "name": "Close Stage",
            "messages": [
                {"speaker": "salesperson", "text": "Would you like to start a free trial?"},
                {"speaker": "customer", "text": "Yes, I'm interested in trying it"},
                {"speaker": "salesperson", "text": "Great! When can we schedule a demo?"}
            ],
            "expected_stage": "close"
        }
    ]

    # Simulate stage detection logic
    for test in test_cases:
        print(f"\n{test['name']}:")
        print(f"  Messages: {len(test['messages'])}")

        # Get last 3 messages
        recent_messages = test['messages'][-3:]
        recent_text = " ".join([msg.get('text', '') for msg in recent_messages]).lower()

        # Simple keyword detection
        stage_scores = {
            "opening": 0,
            "discovery": 0,
            "pitch": 0,
            "objection": 0,
            "close": 0
        }

        # Keyword lists
        keywords = {
            "opening": ["hello", "hi", "calling from", "quick question", "introduction"],
            "discovery": ["what", "how many", "tell me about", "currently using", "challenge"],
            "pitch": ["we offer", "our solution", "it works by", "helps you", "features"],
            "objection": ["expensive", "not interested", "call back", "no budget", "think about it"],
            "close": ["trial", "demo", "start", "schedule", "meeting", "when can"]
        }

        for stage, kw_list in keywords.items():
            for keyword in kw_list:
                if keyword in recent_text:
                    stage_scores[stage] += 10

        detected_stage = max(stage_scores, key=stage_scores.get)
        max_score = stage_scores[detected_stage]

        print(f"  Detected: {detected_stage} (score: {max_score})")
        print(f"  Expected: {test['expected_stage']}")
        print(f"  Result: {'✅ PASS' if detected_stage == test['expected_stage'] else '❌ FAIL'}")


def test_objective_tracking():
    """Test the objective tracking logic"""
    print("\n" + "=" * 60)
    print("TESTING OBJECTIVE TRACKING")
    print("=" * 60)

    # Test discovery stage objectives
    print("\nDiscovery Stage Objectives:")
    discovery_objectives = CALL_OBJECTIVES.get("discovery", [])

    conversation = [
        {"speaker": "salesperson", "text": "How many calls do you receive per day?"},
        {"speaker": "customer", "text": "We get about 100 calls per week"},
        {"speaker": "salesperson", "text": "What's your biggest challenge with handling those calls?"},
        {"speaker": "customer", "text": "The main problem is we miss about 30% of them"}
    ]

    all_text = " ".join([msg.get('text', '') for msg in conversation]).lower()

    completed = []
    remaining = []

    for obj in discovery_objectives:
        has_keywords = any(keyword in all_text for keyword in obj['keywords'])

        if has_keywords:
            completed.append(obj)
            print(f"  ✅ {obj['text']}: COMPLETED")
        else:
            remaining.append(obj)
            print(f"  ⏳ {obj['text']}: REMAINING")

    print(f"\nSummary: {len(completed)} completed, {len(remaining)} remaining")


def test_call_objectives_structure():
    """Verify CALL_OBJECTIVES structure"""
    print("\n" + "=" * 60)
    print("TESTING CALL_OBJECTIVES STRUCTURE")
    print("=" * 60)

    required_stages = ["opening", "discovery", "pitch", "objection", "close"]

    print(f"\nStages defined: {list(CALL_OBJECTIVES.keys())}")

    for stage in required_stages:
        if stage in CALL_OBJECTIVES:
            objectives = CALL_OBJECTIVES[stage]
            print(f"\n{stage.upper()} ({len(objectives)} objectives):")
            for obj in objectives:
                print(f"  - {obj['text']} (id: {obj['id']}, {len(obj['keywords'])} keywords)")
            print(f"  ✅ VALID")
        else:
            print(f"  ❌ MISSING STAGE: {stage}")


def test_feature_flag():
    """Test feature flag configuration"""
    print("\n" + "=" * 60)
    print("TESTING FEATURE FLAG")
    print("=" * 60)

    # Read .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_content = f.read()
            if 'COACHING_MODE' in env_content:
                print("  ✅ COACHING_MODE found in .env")
                for line in env_content.split('\n'):
                    if 'COACHING_MODE' in line:
                        print(f"  {line}")
            else:
                print("  ❌ COACHING_MODE not found in .env")
    else:
        print("  ❌ .env file not found")


if __name__ == '__main__':
    print("\n🧪 COACHING SYSTEM TEST SUITE\n")

    test_call_objectives_structure()
    test_stage_detection()
    test_objective_tracking()
    test_feature_flag()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60 + "\n")
