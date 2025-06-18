#!/usr/bin/env python3
"""
Quick test to verify the bug fixes:
1. Round count fix
2. Word validation fix
"""

import requests
import json

def test_fixes():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Token Game Fixes")
    print("=" * 40)
    
    # Test 1: Round count fix
    print("\n📊 Test 1: Round Count Fix")
    print("-" * 25)
    
    # Test with 5 rounds
    settings = {
        "game_mode": "normal",
        "difficulty": "mixed", 
        "category": "all",
        "rounds": 5
    }
    
    response = requests.post(f"{base_url}/api/start_game", json=settings)
    data = response.json()
    
    if response.status_code == 200 and data['success']:
        round_info = data['round_info']
        print(f"✅ Game started successfully")
        print(f"   Current round: {round_info['current_round']}")
        print(f"   Max rounds: {round_info['max_rounds']}")
        
        if round_info['max_rounds'] == 5:
            print("✅ PASS: Round count is correctly set to 5")
        else:
            print(f"❌ FAIL: Expected 5 rounds, got {round_info['max_rounds']}")
    else:
        print(f"❌ FAIL: Could not start game - {data}")
        return
    
    # Test 2: Word validation fix with "drink"
    print("\n🔤 Test 2: Word Validation Fix")
    print("-" * 30)
    
    guess_response = requests.post(
        f"{base_url}/api/submit_guess",
        json={"guess": "drink"}
    )
    
    print(f"   Response status: {guess_response.status_code}")
    print(f"   Response headers: {dict(guess_response.headers)}")
    
    try:
        guess_data = guess_response.json()
        print(f"   Response JSON: {json.dumps(guess_data, indent=2)}")
        
        if guess_response.status_code == 200 and guess_data['success']:
            result = guess_data['result']
            print(f"✅ Guess submitted successfully")
            print(f"   Word: {result['guess_word']}")
            print(f"   Valid guess: {result['valid_guess']}")
            
            if result['valid_guess']:
                print("✅ PASS: 'drink' is now accepted as a valid word")
                print(f"   Points awarded: {result.get('points', 0)}")
                print(f"   Feedback: {result.get('feedback', {}).get('message', 'No message')}")
            else:
                print(f"❌ FAIL: 'drink' still rejected - {result.get('error', 'No error message')}")
        else:
            print(f"❌ FAIL: Could not submit guess - {guess_data}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"   Raw response: {guess_response.text}")
    except Exception as e:
        print(f"❌ Unexpected error processing response: {e}")
        print(f"   Raw response: {guess_response.text}")
    
    print("\n🎮 Test Summary")
    print("=" * 40)
    print("If both tests passed, the bugs have been fixed!")
    print("You can now:")
    print("1. ✅ Set custom round counts (like 5 rounds)")
    print("2. ✅ Use words like 'drink' that are in the game vocabulary")

if __name__ == "__main__":
    try:
        test_fixes()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the game server.")
        print("   Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 