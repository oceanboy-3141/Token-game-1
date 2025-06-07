"""
Game Logic Module
Handles scoring, word selection, and game state for Token Synonym Game
"""
import random
from typing import List, Dict, Optional, Tuple
from token_handler import TokenHandler


class GameLogic:
    def __init__(self, max_rounds: int = 10):
        self.token_handler = TokenHandler()
        self.current_target_word = ""
        self.current_target_token_id = None
        self.score = 0
        self.round_number = 0
        self.max_rounds = max_rounds
        self.game_history = []
        self.correct_guesses = 0
        self.game_completed = False
        
        # Predefined word list (single tokens, good for synonyms)
        self.target_words = [
            "happy", "sad", "big", "small", "fast", "slow", "hot", "cold",
            "good", "bad", "new", "old", "high", "low", "strong", "weak",
            "light", "dark", "easy", "hard", "love", "hate", "win", "lose",
            "start", "end", "open", "close", "buy", "sell", "give", "take",
            "run", "walk", "jump", "fall", "eat", "drink", "sleep", "wake",
            "work", "play", "learn", "teach", "help", "hurt", "build", "break"
        ]
        
        # Filter to only single-token words
        self.single_token_words = [
            word for word in self.target_words 
            if self.token_handler.is_single_token(word)
        ]
    
    def start_new_round(self) -> Dict:
        """Start a new round with a random target word."""
        if self.game_completed:
            return {'error': 'Game already completed'}
        
        self.round_number += 1
        
        # Check if game should end
        if self.round_number > self.max_rounds:
            self.game_completed = True
            return {
                'game_ended': True,
                'final_score': self.score,
                'correct_guesses': self.correct_guesses,
                'total_rounds': self.max_rounds
            }
        
        # Select random target word
        self.current_target_word = random.choice(self.single_token_words)
        self.current_target_token_id = self.token_handler.get_single_token_id(
            self.current_target_word
        )
        
        return {
            'target_word': self.current_target_word,
            'target_token_id': self.current_target_token_id,
            'round_number': self.round_number,
            'max_rounds': self.max_rounds,
            'game_ended': False
        }
    
    def submit_guess(self, guess_word: str) -> Dict:
        """Submit a guess and calculate score."""
        guess_word = guess_word.strip().lower()
        
        # Get guess token info
        guess_info = self.token_handler.get_word_info(guess_word)
        guess_token_id = self.token_handler.get_single_token_id(guess_word)
        
        # Calculate distance
        if guess_token_id is not None and self.current_target_token_id is not None:
            distance = abs(guess_token_id - self.current_target_token_id)
            
            # Calculate score (closer = higher score)
            round_score = max(0, 1000 - distance)
            self.score += round_score
            
            # Get feedback and check if correct
            feedback = self._get_feedback(distance)
            if feedback['is_correct']:
                self.correct_guesses += 1
            
            # Record this guess
            guess_record = {
                'round': self.round_number,
                'target_word': self.current_target_word,
                'target_token_id': self.current_target_token_id,
                'guess_word': guess_word,
                'guess_token_id': guess_token_id,
                'distance': distance,
                'round_score': round_score,
                'total_score': self.score,
                'is_correct': feedback['is_correct'],
                'result_type': feedback['result']
            }
            
            self.game_history.append(guess_record)
            
            return {
                'valid_guess': True,
                'guess_token_id': guess_token_id,
                'distance': distance,
                'round_score': round_score,
                'total_score': self.score,
                'feedback': feedback,
                'guess_info': guess_info,
                'round_number': self.round_number,
                'max_rounds': self.max_rounds
            }
        else:
            # Invalid guess (multi-token or not found)
            return {
                'valid_guess': False,
                'error': 'Word must be a single token',
                'guess_info': guess_info
            }
    
    def _get_feedback(self, distance: int) -> dict:
        """Generate feedback with clear right/wrong indication."""
        if distance == 0:
            return {
                'message': "🎯 PERFECT! Exact same token ID!",
                'result': 'PERFECT',
                'color': '#4CAF50',
                'is_correct': True
            }
        elif distance <= 10:
            return {
                'message': "🔥 EXCELLENT! Extremely close!",
                'result': 'EXCELLENT',
                'color': '#4CAF50',
                'is_correct': True
            }
        elif distance <= 50:
            return {
                'message': "⭐ GREAT! Very close synonym!",
                'result': 'GREAT',
                'color': '#8BC34A',
                'is_correct': True
            }
        elif distance <= 100:
            return {
                'message': "👍 GOOD! Pretty close!",
                'result': 'GOOD',
                'color': '#FFC107',
                'is_correct': True
            }
        elif distance <= 500:
            return {
                'message': "🤔 OKAY! Getting warmer...",
                'result': 'OKAY',
                'color': '#FF9800',
                'is_correct': False
            }
        else:
            return {
                'message': "❌ MISS! Try closer synonyms!",
                'result': 'MISS',
                'color': '#F44336',
                'is_correct': False
            }
    
    def get_hint(self) -> Dict:
        """Get a helpful hint for the current round."""
        if not self.current_target_token_id:
            return {'error': 'No active round'}
        
        # Find words in the nearby token range
        nearby_words = self.token_handler.find_words_in_range(
            self.current_target_token_id, 50
        )
        
        return {
            'hint_words': nearby_words[:5],  # Show up to 5 nearby words
            'message': f"Try words similar to: {', '.join(nearby_words[:3])}"
        }
    
    def get_game_stats(self) -> Dict:
        """Get current game statistics."""
        if not self.game_history:
            return {
                'total_rounds': 0,
                'average_distance': 0,
                'best_distance': 0,
                'total_score': self.score
            }
        
        distances = [record['distance'] for record in self.game_history]
        
        return {
            'total_rounds': len(self.game_history),
            'average_distance': sum(distances) / len(distances),
            'best_distance': min(distances),
            'worst_distance': max(distances),
            'total_score': self.score,
            'current_round': self.round_number
        }
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.score = 0
        self.round_number = 0
        self.current_target_word = ""
        self.current_target_token_id = None
        self.game_history = []
        self.correct_guesses = 0
        self.game_completed = False
    
    def get_final_results(self) -> Dict:
        """Get final game results summary."""
        if not self.game_completed and self.round_number < self.max_rounds:
            return {'error': 'Game not completed yet'}
        
        accuracy = (self.correct_guesses / max(1, len(self.game_history))) * 100
        
        return {
            'total_score': self.score,
            'correct_guesses': self.correct_guesses,
            'total_rounds': len(self.game_history),
            'accuracy': accuracy,
            'average_distance': sum(r['distance'] for r in self.game_history) / max(1, len(self.game_history)),
            'best_distance': min(r['distance'] for r in self.game_history) if self.game_history else 0,
            'game_completed': self.game_completed
        } 