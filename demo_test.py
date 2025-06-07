#!/usr/bin/env python3
"""
Demo Test for Token Synonym Game
Shows the new feedback system and 10-round structure
"""

from game_logic import GameLogic

def demo_game():
    """Run a quick demo of the improved game logic."""
    print("🎯 Token Synonym Game - Demo Test")
    print("=" * 50)
    
    game = GameLogic(max_rounds=3)  # Shorter demo
    
    # Demo words for testing
    test_guesses = [
        ("happy", "glad"),    # Should be close
        ("big", "large"),     # Should be close  
        ("good", "bad")       # Should be far
    ]
    
    for i, (target_hint, guess) in enumerate(test_guesses):
        print(f"\n🎮 Round {i+1}")
        print("-" * 30)
        
        # Start round
        round_info = game.start_new_round()
        if round_info.get('game_ended'):
            print("🏁 Game Complete!")
            break
            
        target_word = round_info['target_word']
        target_id = round_info['target_token_id']
        
        print(f"Target: {target_word.upper()} (Token ID: {target_id})")
        print(f"Demo guess: {guess}")
        
        # Submit guess
        result = game.submit_guess(guess)
        
        if result['valid_guess']:
            feedback = result['feedback']
            print(f"Result: {feedback['result']} - {feedback['message']}")
            print(f"Distance: {result['distance']} | Score: +{result['round_score']}")
            print(f"Correct: {'✓' if feedback['is_correct'] else '✗'}")
        else:
            print(f"Invalid: {result['error']}")
    
    # Show final stats
    print(f"\n📊 Final Stats:")
    print(f"Total Score: {game.score}")
    print(f"Correct Guesses: {game.correct_guesses}")
    
    if game.game_history:
        accuracy = (game.correct_guesses / len(game.game_history)) * 100
        print(f"Accuracy: {accuracy:.1f}%")

if __name__ == "__main__":
    demo_game() 