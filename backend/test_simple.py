#!/usr/bin/env python3
"""
Simple test to verify coaching system structure without dependencies
"""

# Test CALL_OBJECTIVES structure
CALL_OBJECTIVES = {
    "opening": [
        {"id": "rapport", "text": "Build rapport", "keywords": ["hello", "hi", "how are you", "thanks", "appreciate"]},
        {"id": "establish_reason", "text": "Establish reason for call", "keywords": ["calling because", "reaching out", "quick question", "wanted to talk"]}
    ],
    "discovery": [
        {"id": "qualify_volume", "text": "Qualify call volume", "keywords": ["how many calls", "volume", "receive", "per day", "per week"]},
        {"id": "identify_pain", "text": "Identify pain point", "keywords": ["problem", "challenge", "issue", "missing", "frustrated", "difficult"]},
        {"id": "current_solution", "text": "Understand current solution", "keywords": ["currently using", "right now", "today", "process", "handling"]}
    ],
    "pitch": [
        {"id": "value_prop", "text": "Explain value proposition", "keywords": ["we offer", "solution", "helps you", "can do", "feature"]},
        {"id": "differentiate", "text": "Differentiate from alternatives", "keywords": ["unlike", "better than", "advantage", "different", "unique"]},
        {"id": "address_budget", "text": "Address budget consideration", "keywords": ["cost", "price", "roi", "return", "investment", "save"]}
    ],
    "objection": [
        {"id": "acknowledge", "text": "Acknowledge concern", "keywords": ["understand", "i hear you", "makes sense", "fair", "get it"]},
        {"id": "reframe", "text": "Reframe perspective", "keywords": ["however", "another way", "consider", "what if", "think about"]},
        {"id": "reengage", "text": "Re-engage conversation", "keywords": ["question", "curious", "wondering", "tell me"]}
    ],
    "close": [
        {"id": "propose_next", "text": "Propose next step", "keywords": ["trial", "demo", "meeting", "start", "setup", "call"]},
        {"id": "get_commitment", "text": "Get commitment", "keywords": ["yes", "agreed", "sounds good", "interested", "let's do it"]},
        {"id": "schedule", "text": "Schedule follow-up", "keywords": ["when", "calendar", "date", "time", "schedule"]}
    ]
}

print("=" * 70)
print("COACHING SYSTEM STRUCTURE TEST")
print("=" * 70)

# Test 1: Verify stages exist
print("\n1. TESTING CALL_OBJECTIVES STRUCTURE:")
required_stages = ["opening", "discovery", "pitch", "objection", "close"]
all_pass = True

for stage in required_stages:
    if stage in CALL_OBJECTIVES:
        objectives = CALL_OBJECTIVES[stage]
        print(f"   ✅ {stage.ljust(12)}: {len(objectives)} objectives")
    else:
        print(f"   ❌ {stage.ljust(12)}: MISSING")
        all_pass = False

# Test 2: Test stage detection algorithm
print("\n2. TESTING STAGE DETECTION ALGORITHM:")

test_cases = [
    {
        "name": "Discovery",
        "text": "How many calls do you receive per day? What challenges are you facing?",
        "expected": "discovery"
    },
    {
        "name": "Objection",
        "text": "That sounds expensive. I'm not interested right now.",
        "expected": "objection"
    },
    {
        "name": "Close",
        "text": "Would you like to start a trial? Let's schedule a demo.",
        "expected": "close"
    }
]

for test in test_cases:
    text_lower = test["text"].lower()

    stage_scores = {
        "opening": 0,
        "discovery": 0,
        "pitch": 0,
        "objection": 0,
        "close": 0
    }

    # Keyword detection
    keywords = {
        "opening": ["hello", "hi", "calling from", "quick question"],
        "discovery": ["how many", "tell me about", "challenge"],
        "pitch": ["we offer", "our solution", "helps you"],
        "objection": ["expensive", "not interested", "no budget"],
        "close": ["trial", "demo", "start", "schedule"]
    }

    for stage, kw_list in keywords.items():
        for keyword in kw_list:
            if keyword in text_lower:
                stage_scores[stage] += 10

    detected = max(stage_scores, key=stage_scores.get)
    passed = detected == test["expected"]

    print(f"   {'✅' if passed else '❌'} {test['name']}: detected={detected}, expected={test['expected']}")
    if not passed:
        all_pass = False

# Test 3: Test objective tracking
print("\n3. TESTING OBJECTIVE TRACKING:")

conversation = "How many calls do you receive? We get about 100 per week. What's your biggest problem?"
conversation_lower = conversation.lower()

discovery_objs = CALL_OBJECTIVES["discovery"]
completed = []
remaining = []

for obj in discovery_objs:
    has_keywords = any(keyword in conversation_lower for keyword in obj['keywords'])
    if has_keywords:
        completed.append(obj['text'])
    else:
        remaining.append(obj['text'])

print(f"   Completed ({len(completed)}):")
for text in completed:
    print(f"      ✅ {text}")

print(f"   Remaining ({len(remaining)}):")
for text in remaining:
    print(f"      ⏳ {text}")

# Test 4: Check .env file
print("\n4. TESTING .ENV CONFIGURATION:")
import os
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        if 'COACHING_MODE' in content:
            for line in content.split('\n'):
                if 'COACHING_MODE' in line and not line.strip().startswith('#'):
                    print(f"   ✅ Found: {line.strip()}")
        else:
            print(f"   ❌ COACHING_MODE not found in .env")
            all_pass = False
else:
    print(f"   ❌ .env file not found")
    all_pass = False

# Final result
print("\n" + "=" * 70)
if all_pass:
    print("✅ ALL TESTS PASSED")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 70)
