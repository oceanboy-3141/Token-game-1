"""
Game Logic Module
Handles scoring, word selection, and game state for Token Quest
"""
import random
from typing import List, Dict, Optional, Tuple
from token_handler import TokenHandler


class GameLogic:
    def __init__(self, max_rounds: int = 10, game_mode: str = 'normal', difficulty: str = 'mixed', category: str = 'all'):
        self.token_handler = TokenHandler()
        self.current_target_word = ""
        self.current_target_token_id = None
        self.score = 0
        self.round_number = 0
        self.max_rounds = max_rounds
        self.game_history = []
        self.correct_guesses = 0
        self.game_completed = False
        self.current_attempts = 0
        self.max_attempts = 3
        
        # Game mode settings
        self.game_mode = game_mode  # 'normal', 'antonym', 'category', 'speed', 'explorer'
        self.difficulty = difficulty  # 'easy', 'medium', 'hard', 'mixed'
        self.category = category  # 'all', 'emotions', 'size', 'speed', etc.
        self.time_limit = None  # For speed mode
        self.round_start_time = None
        
        # Comprehensive word list organized by categories and difficulty
        self.word_categories = {
            'emotions': {
                'easy': ['happy', 'sad', 'mad', 'glad', 'calm'],
                'medium': ['angry', 'upset', 'joyful', 'worried', 'excited', 'nervous'],
                'hard': ['elated', 'dejected', 'serene', 'melancholy', 'euphoric']
            },
            'size': {
                'easy': ['big', 'small', 'tiny', 'huge', 'tall'],
                'medium': ['large', 'petite', 'massive', 'mini', 'giant'],
                'hard': ['colossal', 'minuscule', 'immense', 'diminutive']
            },
            'speed': {
                'easy': ['fast', 'slow', 'quick', 'rapid'],
                'medium': ['swift', 'sluggish', 'speedy', 'gradual'],
                'hard': ['brisk', 'leisurely', 'hasty', 'lethargic']
            },
            'quality': {
                'easy': ['good', 'bad', 'nice', 'mean', 'kind'],
                'medium': ['great', 'awful', 'wonderful', 'terrible', 'excellent'],
                'hard': ['superb', 'atrocious', 'magnificent', 'dreadful']
            },
            'temperature': {
                'easy': ['hot', 'cold', 'warm', 'cool'],
                'medium': ['freezing', 'boiling', 'chilly', 'scorching'],
                'hard': ['frigid', 'sweltering', 'tepid', 'torrid']
            },
            'brightness': {
                'easy': ['light', 'dark', 'bright', 'dim'],
                'medium': ['brilliant', 'shadowy', 'gleaming', 'murky'],
                'hard': ['luminous', 'obscure', 'radiant', 'somber']
            },
            'actions': {
                'easy': ['run', 'walk', 'jump', 'sit', 'eat', 'drink'],
                'medium': ['sprint', 'stroll', 'leap', 'devour', 'sip'],
                'hard': ['dash', 'amble', 'bound', 'consume', 'quaff']
            },
            'difficulty': {
                'easy': ['easy', 'hard', 'simple', 'tough'],
                'medium': ['complex', 'effortless', 'challenging', 'basic'],
                'hard': ['intricate', 'elementary', 'arduous', 'facile']
            }
        }
        
        # Flatten all words for backward compatibility
        self.target_words = []
        for category in self.word_categories.values():
            for difficulty in category.values():
                self.target_words.extend(difficulty)
        
        # Add synonym/antonym pairs for research
        self.synonym_pairs = [
            ('happy', 'glad'), ('sad', 'upset'), ('big', 'large'), ('small', 'tiny'),
            ('fast', 'quick'), ('slow', 'gradual'), ('good', 'great'), ('bad', 'awful'),
            ('hot', 'warm'), ('cold', 'cool'), ('bright', 'light'), ('dark', 'dim')
        ]
        
        self.antonym_pairs = [
            ('happy', 'sad'), ('big', 'small'), ('fast', 'slow'), ('good', 'bad'),
            ('hot', 'cold'), ('light', 'dark'), ('easy', 'hard'), ('start', 'end')
        ]
        
        # Filter to only single-token words
        self.single_token_words = [
            word for word in self.target_words 
            if self.token_handler.is_single_token(word)
        ]
        
        # Prepare word list based on game settings
        self.active_word_list = self._prepare_word_list()
    
    def _prepare_word_list(self) -> list:
        """Prepare the active word list based on game mode, difficulty, and category settings."""
        words = []
        
        # Filter by category
        if self.category == 'all':
            categories_to_use = self.word_categories.keys()
        else:
            categories_to_use = [self.category] if self.category in self.word_categories else self.word_categories.keys()
        
        # Filter by difficulty
        if self.difficulty == 'mixed':
            difficulties_to_use = ['easy', 'medium', 'hard']
        else:
            difficulties_to_use = [self.difficulty] if self.difficulty in ['easy', 'medium', 'hard'] else ['easy', 'medium', 'hard']
        
        # Collect words based on filters
        for category in categories_to_use:
            for difficulty in difficulties_to_use:
                if difficulty in self.word_categories[category]:
                    words.extend(self.word_categories[category][difficulty])
        
        # Filter to only single-token words
        filtered_words = [word for word in words if self.token_handler.is_single_token(word)]
        
        return filtered_words if filtered_words else self.single_token_words  # Fallback to all words
    
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
        
        # Select random target word from active list
        self.current_target_word = random.choice(self.active_word_list)
        self.current_target_token_id = self.token_handler.get_single_token_id(
            self.current_target_word
        )
        
        # Reset attempts for new round
        self.current_attempts = 0
        self.max_attempts = 3
        
        # Set round start time for speed mode
        if self.game_mode == 'speed':
            import time
            self.round_start_time = time.time()
            if not self.time_limit:
                self.time_limit = 30  # 30 seconds default
        
        return {
            'target_word': self.current_target_word,
            'target_token_id': self.current_target_token_id,
            'round_number': self.round_number,
            'max_rounds': self.max_rounds,
            'attempts_left': self.max_attempts,
            'game_ended': False,
            'game_mode': self.game_mode,
            'difficulty': self.difficulty,
            'category': self.category,
            'time_limit': self.time_limit if self.game_mode == 'speed' else None
        }
    
    def submit_guess(self, guess_word: str) -> Dict:
        """Submit a guess and calculate score."""
        guess_word = guess_word.strip().lower()
        
        # Check if max attempts reached
        if self.current_attempts >= self.max_attempts:
            return {
                'valid_guess': False,
                'error': 'Maximum attempts (3) reached for this round',
                'max_attempts_reached': True
            }
        
        # Get guess token info
        guess_info = self.token_handler.get_word_info(guess_word)
        guess_token_id = self.token_handler.get_single_token_id(guess_word)
        
        # Calculate distance
        if guess_token_id is not None and self.current_target_token_id is not None:
            self.current_attempts += 1
            distance = abs(guess_token_id - self.current_target_token_id)
            
            # Calculate points using new system
            feedback = self._get_feedback(distance, guess_token_id, self.current_target_token_id)
            round_score = feedback['points']
            self.score += round_score
            
            # Check if correct
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
                'result_type': feedback['result'],
                'attempt_number': self.current_attempts
            }
            
            self.game_history.append(guess_record)
            
            # Get educational explanation and token fact
            educational_explanation = self.token_handler.get_educational_explanation(
                self.current_target_word, guess_word
            )
            token_fact = self.token_handler.get_random_token_fact()
            
            return {
                'valid_guess': True,
                'guess_word': guess_word,
                'guess_token_id': guess_token_id,
                'target_token_id': self.current_target_token_id,
                'distance': distance,
                'round_score': round_score,
                'total_score': self.score,
                'feedback': feedback,
                'guess_info': guess_info,
                'round_number': self.round_number,
                'max_rounds': self.max_rounds,
                'attempts_used': self.current_attempts,
                'attempts_left': self.max_attempts - self.current_attempts,
                'max_attempts_reached': self.current_attempts >= self.max_attempts,
                'educational_explanation': educational_explanation,
                'token_fact': token_fact
            }
        else:
            # Invalid guess (multi-token or not found) - still counts as attempt
            self.current_attempts += 1
            return {
                'valid_guess': False,
                'error': 'Word must be a single token',
                'guess_info': guess_info,
                'attempts_used': self.current_attempts,
                'attempts_left': self.max_attempts - self.current_attempts
            }
    
    def _calculate_points(self, distance: int) -> int:
        """Calculate points based on distance ranges."""
        if self.game_mode == 'antonym':
            # In antonym mode, higher distances get more points
            if distance >= 50000:
                return 10
            elif distance >= 30000:
                return 9
            elif distance >= 20000:
                return 8
            elif distance >= 10000:
                return 7
            elif distance >= 5000:
                return 6
            elif distance >= 1000:
                return 5
            else:
                return 0
        else:
            # Normal mode - closer distances get more points
            if distance <= 1:
                return 10
            elif distance <= 100:
                return 9
            elif distance <= 500:
                return 8
            elif distance <= 1000:
                return 7
            elif distance <= 5000:
                return 6
            elif distance <= 10000:
                return 5
            else:
                return 0
    
    def _get_feedback(self, distance: int, guess_token_id: int, target_token_id: int) -> dict:
        """Generate feedback with clear right/wrong indication and detailed token info."""
        
        # Calculate points (different for antonym mode)
        points = self._calculate_points(distance)
        
        # Antonym mode has different success criteria
        if self.game_mode == 'antonym':
            if distance >= 50000:
                return {
                    'message': f"🎯 PERFECT ANTONYM! 👍",
                    'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                    'result': 'PERFECT OPPOSITE',
                    'color': '#4CAF50',
                    'is_correct': True,
                    'points': points,
                    'encouragement': "Amazing! Maximum distance achieved! 🎉"
                }
            elif distance >= 30000:
                return {
                    'message': f"👍 GREAT ANTONYM! Very opposite!",
                    'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                    'result': 'EXCELLENT OPPOSITE',
                    'color': '#4CAF50',
                    'is_correct': True,
                    'points': points,
                    'encouragement': "Great opposite thinking! 🔥"
                }
            elif distance >= 10000:
                return {
                    'message': f"🤔 Getting more opposite... try for even more distant!",
                    'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                    'result': 'SOMEWHAT OPPOSITE',
                    'color': '#FF9800',
                    'is_correct': False,
                    'points': points,
                    'encouragement': "Think of more contrasting words! 💪"
                }
            else:
                return {
                    'message': f"❌ Too similar! Find the opposite meaning!",
                    'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                    'result': 'TOO SIMILAR',
                    'color': '#F44336',
                    'is_correct': False,
                    'points': points,
                    'encouragement': "Try words with opposite meanings! 💡"
                }
        elif distance <= 1:
            return {
                'message': f"🎯 YOU GOT IT! 👍",
                'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                'result': 'PERFECT',
                'color': '#4CAF50',
                'is_correct': True,
                'points': points,
                'encouragement': "Amazing! Perfect match! 🎉"
            }
        elif distance <= 100:
            return {
                'message': f"👍 YOU GOT IT! Aww so close!",
                'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                'result': 'EXCELLENT',
                'color': '#4CAF50',
                'is_correct': True,
                'points': points,
                'encouragement': "Great synonym sense! 🔥"
            }
        elif distance <= 500:
            return {
                'message': f"🤔 Almost there! Getting warmer...",
                'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                'result': 'CLOSE',
                'color': '#FF9800',
                'is_correct': False,
                'points': points,
                'encouragement': "You're on the right track! 💪"
            }
        elif distance <= 1000:
            return {
                'message': f"❄️ Getting colder... try something closer!",
                'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                'result': 'COLD',
                'color': '#FF5722',
                'is_correct': False,
                'points': points,
                'encouragement': "Think of more similar words! 🤔"
            }
        else:
            return {
                'message': f"❌ Too far apart! Try a different approach!",
                'detail': f"Your token ID: {guess_token_id} | Target: {target_token_id} | Distance: {distance}",
                'result': 'MISS',
                'color': '#F44336',
                'is_correct': False,
                'points': points,
                'encouragement': "Try completely different synonyms! 💡"
            }
    
    def get_hint(self) -> Dict:
        """Get an enhanced hint for the current target word."""
        if not self.current_target_token_id:
            return {'error': 'No active round'}
        
        # Get advanced nearby words with detailed info
        nearby_words_data = self.token_handler.get_advanced_nearby_words(
            self.current_target_token_id, 
            num_words=12
        )
        
        # Generate contextual hint based on target word
        hint_message, hint_type = self._generate_contextual_hint(self.current_target_word)
        
        # Separate semantic hints from token-based hints
        semantic_hints = self._get_semantic_hints(self.current_target_word)
        token_hints = [word['word'] for word in nearby_words_data[:6]]
        
        # Get a random educational fact
        token_fact = self.token_handler.get_random_token_fact()
        
        return {
            'target_word': self.current_target_word,
            'target_token_id': self.current_target_token_id,
            'hint_message': hint_message,
            'hint_type': hint_type,
            'semantic_hints': semantic_hints,
            'token_hints': token_hints,
            'nearby_words_data': nearby_words_data,
            'token_fact': token_fact,
            'token_range': f"Look for words with token IDs near {self.current_target_token_id}"
        }
    
    def _get_semantic_hints(self, word: str) -> List[str]:
        """Get semantic hints based on the word's meaning."""
        word = word.lower()
        
        # Create semantic hint mappings
        semantic_map = {
            # Emotions
            'happy': ['joyful', 'cheerful', 'pleased', 'content', 'glad'],
            'sad': ['unhappy', 'miserable', 'dejected', 'gloomy', 'upset'],
            'angry': ['mad', 'furious', 'irritated', 'annoyed', 'rage'],
            
            # Size
            'big': ['large', 'huge', 'massive', 'enormous', 'giant'],
            'small': ['tiny', 'little', 'mini', 'petite', 'compact'],
            
            # Speed
            'fast': ['quick', 'rapid', 'swift', 'speedy', 'hasty'],
            'slow': ['sluggish', 'gradual', 'leisurely', 'unhurried'],
            
            # Quality
            'good': ['excellent', 'great', 'wonderful', 'superb', 'fine'],
            'bad': ['awful', 'terrible', 'horrible', 'poor', 'dreadful'],
            
            # Temperature
            'hot': ['warm', 'boiling', 'scorching', 'heated', 'burning'],
            'cold': ['freezing', 'chilly', 'frigid', 'icy', 'cool'],
        }
        
        return semantic_map.get(word, [])
    
    def _generate_contextual_hint(self, word: str) -> tuple:
        """Generate contextual hints based on the target word."""
        word = word.lower()
        
        # Emotion words
        emotions_positive = ['happy', 'joy', 'glad', 'cheerful', 'pleased']
        emotions_negative = ['sad', 'angry', 'mad', 'upset', 'unhappy']
        
        # Size words  
        size_big = ['big', 'large', 'huge', 'giant', 'massive']
        size_small = ['small', 'tiny', 'little', 'mini', 'petite']
        
        # Speed words
        speed_fast = ['fast', 'quick', 'rapid', 'swift', 'speedy']
        speed_slow = ['slow', 'sluggish', 'gradual', 'leisurely']
        
        # Quality words
        quality_good = ['good', 'great', 'excellent', 'wonderful', 'amazing']
        quality_bad = ['bad', 'awful', 'terrible', 'horrible', 'poor']
        
        if word in emotions_positive:
            return "💖 Think of other positive emotions or feelings!", "emotion_positive"
        elif word in emotions_negative:
            return "💔 Consider other negative emotions or sad feelings", "emotion_negative"
        elif word in size_big:
            return "📏 Think of other words meaning large or expansive", "size_big"
        elif word in size_small:
            return "🤏 Consider other words meaning tiny or compact", "size_small"
        elif word in speed_fast:
            return "⚡ Think of other words meaning quick or rapid", "speed_fast"
        elif word in speed_slow:
            return "🐌 Consider other words meaning gradual or unhurried", "speed_slow"
        elif word in quality_good:
            return "⭐ Think of other positive quality words", "quality_good"
        elif word in quality_bad:
            return "👎 Consider other negative quality words", "quality_bad"
        else:
            return f"🤔 Think of words similar to '{word}' or with related meanings", "general"
    
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
            'game_completed': self.game_completed,
            'game_mode': self.game_mode,
            'difficulty': self.difficulty,
            'category': self.category
        }
    
    def change_game_settings(self, game_mode: str = None, difficulty: str = None, category: str = None):
        """Change game settings and refresh word list."""
        if game_mode:
            self.game_mode = game_mode
        if difficulty:
            self.difficulty = difficulty
        if category:
            self.category = category
        
        # Refresh the active word list
        self.active_word_list = self._prepare_word_list()
    
    @staticmethod
    def get_available_modes():
        """Get available game modes."""
        return {
            'normal': 'Classic synonym finding',
            'antonym': 'Find words with opposite meanings (maximum distance)',
            'category': 'Words from specific semantic category',
            'speed': 'Time-limited rounds for extra challenge'
        }
    
    @staticmethod
    def get_available_difficulties():
        """Get available difficulty levels."""
        return {
            'easy': 'Simple, common words',
            'medium': 'Moderate complexity words', 
            'hard': 'Advanced vocabulary words',
            'mixed': 'Random mix of all difficulties'
        }
    
    @staticmethod
    def get_available_categories():
        """Get available word categories."""
        return {
            'all': 'All word categories',
            'emotions': 'Feeling and emotion words',
            'size': 'Size and dimension words',
            'speed': 'Speed and pace words', 
            'quality': 'Quality and value words',
            'temperature': 'Temperature and heat words',
            'brightness': 'Light and darkness words',
            'actions': 'Action and movement words',
            'difficulty': 'Difficulty and complexity words'
        } 