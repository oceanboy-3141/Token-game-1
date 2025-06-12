"""
Token Handler Module
Manages all tiktoken operations for Token Quest
"""

import tiktoken
import random
import logging
from functools import lru_cache
from typing import List, Tuple, Optional, Dict


class TokenHandler:
    def __init__(self, encoding_name: str = "o200k_base"):
        """Initialize the token handler with specified encoding."""
        self.encoding_name = encoding_name
        self.encoder = tiktoken.get_encoding(encoding_name)
        
        # Educational facts about tokenization
        self.token_facts = [
            "🧠 Token IDs are assigned based on how frequently words appear in training data!",
            "📊 Lower token IDs usually represent more common words and characters.",
            "🔤 Words that start with spaces have different token IDs than the same word without spaces.",
            "🌍 The same word can have different token IDs in different tokenization schemes.",
            "📝 Compound words might tokenize differently than you expect!",
            "🎯 Token distance doesn't always correlate with semantic similarity.",
            "🔄 Some tokens represent parts of words, not complete words.",
            "💡 Tokenization is the first step in how AI models understand language!",
            "🎨 Creative spellings and internet slang can create surprising token patterns.",
            "📈 Token IDs can reveal biases in training data frequency."
        ]
        
        # Local cache for id→word look-ups (fast runtime, small memory)
        self._id_to_word: Dict[int, str] = {}
        # Configure logger
        self._logger = logging.getLogger(__name__)
        
    # ─────────────────────────────────────────────
    # Caching helpers
    # ─────────────────────────────────────────────

    @lru_cache(maxsize=100_000)
    def _encode_cached(self, text: str) -> Tuple[int, ...]:
        """Cached BPE encoding (immutable tuple so it can be cached)."""
        return tuple(self.encoder.encode(text))

    @lru_cache(maxsize=100_000)
    def _decode_single_cached(self, token_id: int) -> str:
        """Cached single-token decoding."""
        return self.encoder.decode([token_id])

    def _word_from_id(self, token_id: int) -> str:
        """Return decoded word for a token id using local + LRU cache."""
        if token_id in self._id_to_word:
            return self._id_to_word[token_id]
        try:
            word = self._decode_single_cached(token_id)
        except Exception as exc:
            self._logger.debug("Decode failed for id %s: %s", token_id, exc)
            word = ""
        self._id_to_word[token_id] = word
        return word

    # ─────────────────────────────────────────────
    # Public API (uses caches)
    # ─────────────────────────────────────────────

    def get_token_ids(self, text: str) -> List[int]:
        """Get token IDs for a given text."""
        return list(self._encode_cached(text))
    
    def get_single_token_id(self, word: str) -> Optional[int]:
        """Get token ID for a word if it's a single token, None otherwise."""
        token_ids = self.get_token_ids(word)
        if len(token_ids) == 1:
            return token_ids[0]
        return None
    
    def decode_tokens(self, token_ids: List[int]) -> str:
        """Decode token IDs back to text."""
        # Fast-path for single id using cache
        if len(token_ids) == 1:
            return self._decode_single_cached(token_ids[0])
        return self.encoder.decode(token_ids)
    
    def is_single_token(self, word: str) -> bool:
        """Check if a word is encoded as a single token."""
        return len(self.get_token_ids(word)) == 1
    
    def calculate_token_distance(self, word1: str, word2: str) -> Optional[int]:
        """Calculate the absolute distance between token IDs of two words."""
        id1 = self.get_single_token_id(word1)
        id2 = self.get_single_token_id(word2)
        
        if id1 is None or id2 is None:
            return None
        
        return abs(id1 - id2)
    
    def get_word_info(self, word: str) -> dict:
        """Get comprehensive token information for a word."""
        token_ids = self.get_token_ids(word)
        return {
            'word': word,
            'token_ids': token_ids,
            'token_count': len(token_ids),
            'is_single_token': len(token_ids) == 1,
            'primary_token_id': token_ids[0] if token_ids else None
        }
    
    def find_words_in_range(self, center_token_id: int, range_size: int = 100) -> List[str]:
        """Find valid words within a token ID range (useful for hints/suggestions)."""
        words = []
        start_id = max(0, center_token_id - range_size)
        end_id = center_token_id + range_size
        
        for token_id in range(start_id, end_id + 1):
            decoded = self._word_from_id(token_id)
            # Filter for real-looking words
            if decoded and decoded.isalpha() and len(decoded) > 1:
                words.append(decoded)
                
        return words[:20]  # Limit results
    
    def get_token_visualization_data(self, target_id: int, guess_id: int, range_size: int = 50) -> Dict:
        """Get data for visualizing token space around target and guess."""
        distance = abs(target_id - guess_id)
        
        # Create visualization range centered on target
        vis_start = max(0, target_id - range_size)
        vis_end = target_id + range_size
        
        # Find words in the visualization range
        nearby_words = []
        for token_id in range(vis_start, vis_end + 1, 5):  # Sample every 5th token
            decoded = self._word_from_id(token_id)
            if decoded and decoded.isalpha() and len(decoded) > 1:
                nearby_words.append({
                    'word': decoded,
                    'token_id': token_id,
                    'distance_from_target': abs(token_id - target_id)
                })
        
        return {
            'target_id': target_id,
            'guess_id': guess_id,
            'distance': distance,
            'visualization_range': (vis_start, vis_end),
            'nearby_words': nearby_words[:15],  # Limit for visualization
            'relative_position': self._get_relative_position(target_id, guess_id),
            'distance_category': self._categorize_distance(distance)
        }
    
    def _get_relative_position(self, target_id: int, guess_id: int) -> str:
        """Determine relative position of guess compared to target."""
        if guess_id < target_id:
            return "before"
        elif guess_id > target_id:
            return "after"
        else:
            return "exact"
    
    def _categorize_distance(self, distance: int) -> str:
        """Categorize the distance for educational feedback."""
        if distance == 0:
            return "perfect"
        elif distance <= 50:
            return "excellent"
        elif distance <= 200:
            return "good"
        elif distance <= 500:
            return "moderate"
        elif distance <= 1000:
            return "far"
        else:
            return "very_far"
    
    def get_educational_explanation(self, target_word: str, guess_word: str) -> str:
        """Generate educational explanation for why tokens are close/far."""
        target_id = self.get_single_token_id(target_word)
        guess_id = self.get_single_token_id(guess_word)
        
        if target_id is None or guess_id is None:
            return "One of the words isn't a single token, which affects comparison!"
        
        distance = abs(target_id - guess_id)
        
        # Generate explanation based on distance and word characteristics
        explanations = []
        
        if distance <= 50:
            explanations.append(f"🎯 Very close! '{target_word}' and '{guess_word}' have similar token IDs.")
            explanations.append("This suggests they might be processed similarly by the tokenizer.")
        elif distance <= 200:
            explanations.append(f"👍 Pretty close! These words are in the same token neighborhood.")
            explanations.append("They likely have similar frequency patterns in training data.")
        elif distance <= 1000:
            explanations.append(f"🤔 Moderately distant. These words are in different token regions.")
            explanations.append("They might have different usage patterns or frequencies.")
        else:
            explanations.append(f"📏 Quite far apart! These words are in very different token regions.")
            explanations.append("This suggests different frequency patterns or word characteristics.")
        
        # Add specific insights based on word patterns
        if target_word.lower().startswith(guess_word.lower()[:2]):
            explanations.append("💡 Interesting! These words share similar starting letters.")
        
        if len(target_word) == len(guess_word):
            explanations.append("📐 Both words have the same length - that's a curious coincidence!")
        
        return " ".join(explanations)
    
    def get_random_token_fact(self) -> str:
        """Get a random educational fact about tokenization."""
        return random.choice(self.token_facts)
    
    def get_advanced_nearby_words(self, target_id: int, num_words: int = 10) -> List[Dict]:
        """Get nearby words with detailed information for advanced hints."""
        nearby_words = []
        
        # Search in expanding ranges
        for range_size in [25, 50, 100, 200]:
            words_found = self.find_words_in_range(target_id, range_size)
            
            for word in words_found:
                word_id = self.get_single_token_id(word)
                if word_id and word_id != target_id:
                    nearby_words.append({
                        'word': word,
                        'token_id': word_id,
                        'distance': abs(word_id - target_id),
                        'direction': 'before' if word_id < target_id else 'after'
                    })
            
            if len(nearby_words) >= num_words:
                break
        
        # Sort by distance and return top results
        nearby_words.sort(key=lambda x: x['distance'])
        return nearby_words[:num_words] 