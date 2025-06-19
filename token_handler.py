"""
Token Handler Module for Token Quest
Handles tiktoken encoding/decoding and token analysis
"""
import logging
import random
from typing import List, Tuple, Optional, Dict

import tiktoken

# Configure logging
logger = logging.getLogger(__name__)


class TokenHandler:
    def __init__(self, encoding_name: str = "cl100k_base"):
        """Initialize with tiktoken encoder."""
        try:
            self.encoder = tiktoken.get_encoding(encoding_name)
            self.encoding_name = encoding_name
        except Exception as e:
            logger.error(f"Failed to initialize tiktoken encoder: {e}")
            raise
        
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
    
    def encode_text(self, text: str) -> List[int]:
        """Encode text to token IDs."""
        try:
            return self.encoder.encode(text)
        except Exception as e:
            logger.error(f"Error encoding text '{text}': {e}")
            return []
    
    def decode_tokens(self, tokens: List[int]) -> str:
        """Decode token IDs back to text."""
        try:
            return self.encoder.decode(tokens)
        except Exception as e:
            logger.error(f"Error decoding tokens {tokens}: {e}")
            return ""
    
    def get_single_token_id(self, word: str) -> Optional[int]:
        """Get the token ID for a word if it's encoded as a single token."""
        try:
            tokens = self.encode_text(word.strip())
            return tokens[0] if len(tokens) == 1 else None
        except Exception as e:
            logger.error(f"Error getting single token ID for '{word}': {e}")
            return None
    
    def is_single_token(self, word: str) -> bool:
        """Check if a word is encoded as exactly one token."""
        try:
            tokens = self.encode_text(word.strip())
            return len(tokens) == 1
        except Exception as e:
            logger.error(f"Error checking if '{word}' is single token: {e}")
            return False
    
    def get_token_string(self, token_id: int) -> str:
        """Get the string representation of a token ID."""
        try:
            return self.encoder.decode([token_id])
        except Exception as e:
            logger.error(f"Error decoding token {token_id}: {e}")
            return f"[TOKEN_{token_id}]"
    
    def get_word_info(self, word: str) -> Dict:
        """Get comprehensive information about how a word is tokenized."""
        try:
            tokens = self.encode_text(word)
            
            info = {
                'word': word,
                'token_count': len(tokens),
                'tokens': tokens,
                'is_single_token': len(tokens) == 1,
                'token_strings': []
            }
            
            # Get string representation of each token
            for token in tokens:
                try:
                    token_str = self.encoder.decode([token])
                    info['token_strings'].append({
                        'token_id': token,
                        'token_string': token_str
                    })
                except Exception as e:
                    logger.error(f"Error decoding individual token {token}: {e}")
                    info['token_strings'].append({
                        'token_id': token,
                        'token_string': f"[ERROR_TOKEN_{token}]"
                    })
            
            return info
        
        except Exception as e:
            logger.error(f"Error getting word info for '{word}': {e}")
            return {
                'word': word,
                'token_count': 0,
                'tokens': [],
                'is_single_token': False,
                'token_strings': [],
                'error': str(e)
            }
    
    def get_nearby_tokens(self, token_id: int, range_size: int = 10) -> List[Dict]:
        """Get tokens near the given token ID for hints."""
        try:
            nearby_tokens = []
            
            # Get tokens in range around the target
            start_id = max(0, token_id - range_size)
            end_id = min(100000, token_id + range_size + 1)  # Reasonable upper bound
            
            for tid in range(start_id, end_id):
                if tid != token_id:
                    try:
                        token_str = self.encoder.decode([tid])
                        # Filter out non-word tokens (special characters, etc.)
                        if len(token_str.strip()) > 0 and token_str.strip().isalpha():
                            nearby_tokens.append({
                                'token_id': tid,
                                'token_string': token_str.strip(),
                                'distance': abs(tid - token_id)
                            })
                    except Exception:
                        continue
            
            # Sort by distance and return closest ones
            nearby_tokens.sort(key=lambda x: x['distance'])
            return nearby_tokens[:10]  # Return top 10 closest
            
        except Exception as e:
            logger.error(f"Error in get_nearby_tokens for token {token_id}: {e}")
            return []
    
    def calculate_token_distance(self, word1: str, word2: str) -> Optional[int]:
        """Calculate distance between single-token words."""
        token1 = self.get_single_token_id(word1)
        token2 = self.get_single_token_id(word2)
        
        if token1 is None or token2 is None:
            return None
        
        return abs(token1 - token2)
    
    def find_words_in_range(self, center_token_id: int, max_distance: int = 50) -> List[Dict]:
        """Find valid words within a certain token distance."""
        words_found = []
        
        start_id = max(0, center_token_id - max_distance)
        end_id = min(100000, center_token_id + max_distance + 1)
        
        for token_id in range(start_id, end_id):
            try:
                word = self.encoder.decode([token_id])
                if (word.strip().isalpha() and 
                    2 <= len(word.strip()) <= 15 and 
                    self.is_single_token(word.strip())):
                    words_found.append({
                        'word': word.strip(),
                        'token_id': token_id,
                        'distance': abs(token_id - center_token_id)
                    })
            except Exception:
                continue
        
        # Sort by distance
        words_found.sort(key=lambda x: x['distance'])
        return words_found
    
    def get_random_single_token_word(self) -> Tuple[str, int]:
        """Get a random word that encodes to a single token."""
        max_attempts = 1000
        attempts = 0
        
        # Common single-token words to try first
        common_words = [
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "by", "from", "up", "about", "into", "through", "during", "before",
            "after", "above", "below", "between", "among", "cat", "dog", "house",
            "tree", "car", "book", "water", "fire", "earth", "air", "light",
            "dark", "good", "bad", "big", "small", "hot", "cold", "fast", "slow"
        ]
        
        # Try common words first
        for word in common_words:
            if self.is_single_token(word):
                token_id = self.get_single_token_id(word)
                if token_id is not None:
                    return word, token_id
        
        # If no common words work, try random approach
        while attempts < max_attempts:
            # Generate random token ID in reasonable range
            token_id = random.randint(1000, 50000)
            
            try:
                word = self.encoder.decode([token_id])
                # Check if it's a valid word (alphabetic and reasonable length)
                if (word.strip().isalpha() and 
                    2 <= len(word.strip()) <= 15 and 
                    self.is_single_token(word.strip())):
                    return word.strip(), token_id
            except Exception:
                pass
            
            attempts += 1
        
        # Fallback - return a guaranteed working word
        return "token", self.get_single_token_id("token") or 1000
    
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