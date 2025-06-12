"""
Token Cache System for Token Quest
High-performance caching for token lookups and word mappings
"""
import tiktoken
import json
import os
from typing import Dict, List, Optional, Set
from pathlib import Path
import logging
from functools import lru_cache
import threading
import time

logger = logging.getLogger(__name__)

class TokenCache:
    """High-performance token cache with persistent storage."""
    
    def __init__(self, cache_dir: str = "cache", encoding_name: str = "o200k_base"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.encoding_name = encoding_name
        self.encoder = tiktoken.get_encoding(encoding_name)
        
        # Cache files
        self.word_to_token_file = self.cache_dir / f"word_to_token_{encoding_name}.json"
        self.token_to_word_file = self.cache_dir / f"token_to_word_{encoding_name}.json"
        self.nearby_tokens_file = self.cache_dir / f"nearby_tokens_{encoding_name}.json"
        
        # In-memory caches
        self._word_to_token_cache: Dict[str, int] = {}
        self._token_to_word_cache: Dict[int, str] = {}
        self._nearby_tokens_cache: Dict[int, List[int]] = {}
        
        # Thread safety
        self._cache_lock = threading.RLock()
        
        # Load existing caches
        self._load_caches()
        
        logger.info("Token cache initialized with encoding: %s", encoding_name)
    
    def _load_caches(self):
        """Load caches from disk."""
        try:
            if self.word_to_token_file.exists():
                with open(self.word_to_token_file, 'r', encoding='utf-8') as f:
                    self._word_to_token_cache = json.load(f)
                logger.info("Loaded %d word-to-token mappings", len(self._word_to_token_cache))
            
            if self.token_to_word_file.exists():
                with open(self.token_to_word_file, 'r', encoding='utf-8') as f:
                    # Convert string keys back to integers
                    data = json.load(f)
                    self._token_to_word_cache = {int(k): v for k, v in data.items()}
                logger.info("Loaded %d token-to-word mappings", len(self._token_to_word_cache))
            
            if self.nearby_tokens_file.exists():
                with open(self.nearby_tokens_file, 'r', encoding='utf-8') as f:
                    # Convert string keys back to integers
                    data = json.load(f)
                    self._nearby_tokens_cache = {int(k): v for k, v in data.items()}
                logger.info("Loaded %d nearby token mappings", len(self._nearby_tokens_cache))
        
        except Exception as e:
            logger.error("Error loading caches: %s", e, exc_info=True)
    
    def _save_caches(self):
        """Save caches to disk."""
        try:
            with self._cache_lock:
                # Save word-to-token cache
                with open(self.word_to_token_file, 'w', encoding='utf-8') as f:
                    json.dump(self._word_to_token_cache, f, indent=2)
                
                # Save token-to-word cache (convert int keys to strings for JSON)
                with open(self.token_to_word_file, 'w', encoding='utf-8') as f:
                    data = {str(k): v for k, v in self._token_to_word_cache.items()}
                    json.dump(data, f, indent=2)
                
                # Save nearby tokens cache
                with open(self.nearby_tokens_file, 'w', encoding='utf-8') as f:
                    data = {str(k): v for k, v in self._nearby_tokens_cache.items()}
                    json.dump(data, f, indent=2)
                
                logger.debug("Caches saved to disk")
        
        except Exception as e:
            logger.error("Error saving caches: %s", e, exc_info=True)
    
    @lru_cache(maxsize=10000)
    def get_token_id(self, word: str) -> Optional[int]:
        """Get token ID for a word with caching."""
        word = word.strip().lower()
        
        # Check cache first
        with self._cache_lock:
            if word in self._word_to_token_cache:
                return self._word_to_token_cache[word]
        
        # Encode the word
        try:
            tokens = self.encoder.encode(word)
            if len(tokens) == 1:
                token_id = tokens[0]
                
                # Cache the result
                with self._cache_lock:
                    self._word_to_token_cache[word] = token_id
                    self._token_to_word_cache[token_id] = word
                
                return token_id
            else:
                # Multi-token word - cache as None
                with self._cache_lock:
                    self._word_to_token_cache[word] = None
                return None
        
        except Exception as e:
            logger.error("Error encoding word '%s': %s", word, e)
            return None
    
    @lru_cache(maxsize=10000)
    def get_word_from_token(self, token_id: int) -> Optional[str]:
        """Get word from token ID with caching."""
        # Check cache first
        with self._cache_lock:
            if token_id in self._token_to_word_cache:
                return self._token_to_word_cache[token_id]
        
        # Decode the token
        try:
            word = self.encoder.decode([token_id])
            
            # Cache the result
            with self._cache_lock:
                self._token_to_word_cache[token_id] = word
                self._word_to_token_cache[word.lower()] = token_id
            
            return word
        
        except Exception as e:
            logger.error("Error decoding token %d: %s", token_id, e)
            return None
    
    def get_nearby_tokens(self, token_id: int, range_size: int = 100) -> List[int]:
        """Get tokens near the given token ID."""
        cache_key = token_id
        
        # Check cache first
        with self._cache_lock:
            if cache_key in self._nearby_tokens_cache:
                return self._nearby_tokens_cache[cache_key]
        
        # Generate nearby tokens
        nearby = []
        for offset in range(-range_size, range_size + 1):
            nearby_token = token_id + offset
            if nearby_token >= 0:  # Ensure valid token ID
                nearby.append(nearby_token)
        
        # Cache the result
        with self._cache_lock:
            self._nearby_tokens_cache[cache_key] = nearby
        
        return nearby
    
    def get_nearby_words(self, token_id: int, range_size: int = 50) -> List[tuple]:
        """Get words with tokens near the given token ID."""
        nearby_tokens = self.get_nearby_tokens(token_id, range_size)
        nearby_words = []
        
        for nearby_token in nearby_tokens:
            word = self.get_word_from_token(nearby_token)
            if word and word.strip() and word.isalpha():  # Only valid alphabetic words
                distance = abs(nearby_token - token_id)
                nearby_words.append((word.strip(), nearby_token, distance))
        
        # Sort by distance
        nearby_words.sort(key=lambda x: x[2])
        return nearby_words
    
    def preload_word_list(self, words: List[str]):
        """Preload a list of words into the cache."""
        logger.info("Preloading %d words into cache...", len(words))
        start_time = time.time()
        
        for word in words:
            self.get_token_id(word)
        
        elapsed = time.time() - start_time
        logger.info("Preloaded %d words in %.2f seconds", len(words), elapsed)
        
        # Save caches after preloading
        self._save_caches()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._cache_lock:
            return {
                'word_to_token_entries': len(self._word_to_token_cache),
                'token_to_word_entries': len(self._token_to_word_cache),
                'nearby_tokens_entries': len(self._nearby_tokens_cache),
                'lru_cache_info': {
                    'get_token_id': self.get_token_id.cache_info()._asdict(),
                    'get_word_from_token': self.get_word_from_token.cache_info()._asdict()
                }
            }
    
    def clear_cache(self):
        """Clear all caches."""
        with self._cache_lock:
            self._word_to_token_cache.clear()
            self._token_to_word_cache.clear()
            self._nearby_tokens_cache.clear()
            self.get_token_id.cache_clear()
            self.get_word_from_token.cache_clear()
        
        logger.info("All caches cleared")
    
    def save_and_close(self):
        """Save caches and cleanup."""
        self._save_caches()
        logger.info("Token cache saved and closed")

# Global cache instance
_global_cache: Optional[TokenCache] = None

def get_global_cache(encoding_name: str = "o200k_base") -> TokenCache:
    """Get or create the global token cache instance."""
    global _global_cache
    if _global_cache is None or _global_cache.encoding_name != encoding_name:
        _global_cache = TokenCache(encoding_name=encoding_name)
    return _global_cache 