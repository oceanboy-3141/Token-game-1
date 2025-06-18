#!/usr/bin/env python3
"""
Test script to verify scoring works correctly in Flask Token Game
"""

import requests
import json
import time

def test_scoring():
    """Test the scoring system with the Flask API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Token Game Scoring System...")
    
    # Test 1: Start a new game
    print("\n1. Starting new game...")
    response = requests.post(f"{base_url}/api/start_game", 
                           json={
                               "game_mode": "normal",
                               "difficulty": "mixed", 
                               "category": "all",
                               "rounds": 3
                           })
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Game started successfully!")
            print(f"   Target word: {data['round_info']['target_word']}")
            print(f"   Target token ID: {data['round_info']['target_token_id']}")
        else:
            print(f"❌ Failed to start game: {data.get('error')}")
            return False
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return False
    
    # Test 2: Submit a guess
    print("\n2. Submitting guess...")
    target_word = data['round_info']['target_word']
    
    # Try guessing the exact target word (should get perfect score)
    response = requests.post(f"{base_url}/api/submit_guess",
                           json={"guess": target_word})
    
    if response.status_code == 200:
        guess_data = response.json()
        if guess_data.get('success') and guess_data['result']['valid_guess']:
            result = guess_data['result']
            print(f"✅ Guess processed successfully!")
            print(f"   Guess: {result['guess_word']}")
            print(f"   Distance: {result['distance']}")
            print(f"   Points earned: {result['points']}")
            print(f"   Total score: {result['total_score']}")
            print(f"   Correct: {result['correct']}")
            
            # Verify scoring logic
            if result['distance'] == 0 and result['points'] == 10:
                print("✅ Perfect match scoring works correctly!")
            else:
                print(f"⚠️  Expected distance=0 and points=10, got distance={result['distance']} and points={result['points']}")
        else:
            print(f"❌ Failed to process guess: {guess_data}")
            return False
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return False
    
    # Test 3: Check game status
    print("\n3. Checking game status...")
    response = requests.get(f"{base_url}/api/game_status")
    
    if response.status_code == 200:
        status = response.json()
        print(f"✅ Game status retrieved!")
        print(f"   Current round: {status['current_round']}")
        print(f"   Total score: {status['total_score']}")
        print(f"   Correct guesses: {status['correct_guesses']}")
        
        # Verify score consistency
        if status['total_score'] == result['total_score']:
            print("✅ Score consistency verified!")
        else:
            print(f"⚠️  Score mismatch: status={status['total_score']}, result={result['total_score']}")
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return False
    
    # Test 4: Submit another guess to test scoring accumulation
    print("\n4. Testing score accumulation...")
    
    # Start next round first
    response = requests.post(f"{base_url}/api/start_game", json={})
    if response.status_code == 200:
        round_data = response.json()
        if round_data.get('success'):
            new_target = round_data['round_info']['target_word']
            print(f"   Next target: {new_target}")
            
            # Submit a guess with some distance
            test_guess = "happy" if new_target != "happy" else "sad"
            response = requests.post(f"{base_url}/api/submit_guess",
                                   json={"guess": test_guess})
            
            if response.status_code == 200:
                guess_data = response.json()
                if guess_data.get('success') and guess_data['result']['valid_guess']:
                    new_result = guess_data['result']
                    print(f"   New guess points: {new_result['points']}")
                    print(f"   New total score: {new_result['total_score']}")
                    
                    # Verify score accumulation
                    expected_total = status['total_score'] + new_result['points']
                    if new_result['total_score'] == expected_total:
                        print("✅ Score accumulation works correctly!")
                    else:
                        print(f"⚠️  Score accumulation issue: expected {expected_total}, got {new_result['total_score']}")
                else:
                    print(f"❌ Second guess failed: {guess_data}")
            else:
                print(f"❌ HTTP Error on second guess: {response.status_code}")
        else:
            print(f"❌ Failed to start next round: {round_data}")
    else:
        print(f"❌ HTTP Error starting next round: {response.status_code}")
    
    print("\n🎉 Scoring system test completed!")
    return True

if __name__ == "__main__":
    try:
        test_scoring()
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc() 