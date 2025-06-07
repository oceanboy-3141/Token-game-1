"""
Token Handler Module
Manages all tiktoken operations for the Token Synonym Game
"""

import tiktoken
from typing import List, Tuple, Optional


class TokenHandler:
    def __init__(self, encoding_name: str = "o200k_base"):
        """Initialize the token handler with specified encoding."""
        self.encoding_name = encoding_name
        self.encoder = tiktoken.get_encoding(encoding_name)
        
    def get_token_ids(self, text: str) -> List[int]:
        """Get token IDs for a given text."""
        return self.encoder.encode(text)
    
    def get_single_token_id(self, word: str) -> Optional[int]:
        """Get token ID for a word if it's a single token, None otherwise."""
        token_ids = self.get_token_ids(word)
        if len(token_ids) == 1:
            return token_ids[0]
        return None
    
    def decode_tokens(self, token_ids: List[int]) -> str:
        """Decode token IDs back to text."""
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
            try:
                decoded = self.encoder.decode([token_id])
                # Filter for actual words (basic filtering)
                if decoded.strip() and decoded.isalpha() and len(decoded.strip()) > 1:
                    words.append(decoded.strip())
            except:
                continue
                
        return words[:20]  # Limit results 