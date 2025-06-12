"""
Configuration Management for Token Quest
Centralized settings and configuration handling
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class GameConfig:
    """Game configuration settings."""
    # Game settings
    default_difficulty: str = "medium"
    default_game_mode: str = "classic"
    max_attempts_per_round: int = 10
    hint_cost: int = 5  # Points deducted for using hints
    
    # Scoring settings
    perfect_score: int = 100
    distance_penalty_factor: float = 0.5
    time_bonus_enabled: bool = True
    time_bonus_factor: float = 0.1
    
    # UI settings
    window_width: int = 1000
    window_height: int = 700
    theme: str = "light"
    font_size: int = 12
    animation_speed: float = 1.0
    
    # Performance settings
    cache_enabled: bool = True
    async_data_collection: bool = True
    preload_word_lists: bool = True
    max_cache_size: int = 10000
    
    # Data collection settings
    data_collection_enabled: bool = True
    auto_save_interval: int = 30  # seconds
    research_data_dir: str = "research_data"
    
    # Token settings
    encoding_name: str = "o200k_base"
    token_range_for_hints: int = 50
    nearby_words_count: int = 10

@dataclass
class WebConfig:
    """Web application configuration."""
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = False
    secret_key: str = "your-secret-key-change-this"
    
    # Database settings
    database_url: str = "sqlite:///token_quest.db"
    
    # Session settings
    session_timeout: int = 3600  # 1 hour
    
    # API settings
    api_rate_limit: str = "100/hour"
    
    # Security settings
    csrf_enabled: bool = True
    secure_cookies: bool = False  # Set to True in production

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.game_config = GameConfig()
        self.web_config = WebConfig()
        
        # Load configuration if file exists
        self.load_config()
        
        logger.info("Configuration manager initialized")
    
    def load_config(self):
        """Load configuration from file."""
        if not self.config_file.exists():
            logger.info("Config file not found, using defaults")
            self.save_config()  # Create default config file
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load game config
            if 'game' in data:
                game_data = data['game']
                for key, value in game_data.items():
                    if hasattr(self.game_config, key):
                        setattr(self.game_config, key, value)
            
            # Load web config
            if 'web' in data:
                web_data = data['web']
                for key, value in web_data.items():
                    if hasattr(self.web_config, key):
                        setattr(self.web_config, key, value)
            
            logger.info("Configuration loaded from %s", self.config_file)
        
        except Exception as e:
            logger.error("Error loading config: %s", e, exc_info=True)
            logger.info("Using default configuration")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            config_data = {
                'game': asdict(self.game_config),
                'web': asdict(self.web_config)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info("Configuration saved to %s", self.config_file)
        
        except Exception as e:
            logger.error("Error saving config: %s", e, exc_info=True)
    
    def get_game_config(self) -> GameConfig:
        """Get game configuration."""
        return self.game_config
    
    def get_web_config(self) -> WebConfig:
        """Get web configuration."""
        return self.web_config
    
    def update_game_setting(self, key: str, value: Any):
        """Update a game setting."""
        if hasattr(self.game_config, key):
            setattr(self.game_config, key, value)
            self.save_config()
            logger.info("Updated game setting: %s = %s", key, value)
        else:
            logger.warning("Unknown game setting: %s", key)
    
    def update_web_setting(self, key: str, value: Any):
        """Update a web setting."""
        if hasattr(self.web_config, key):
            setattr(self.web_config, key, value)
            self.save_config()
            logger.info("Updated web setting: %s = %s", key, value)
        else:
            logger.warning("Unknown web setting: %s", key)
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.game_config = GameConfig()
        self.web_config = WebConfig()
        self.save_config()
        logger.info("Configuration reset to defaults")
    
    def get_data_dir(self) -> Path:
        """Get the data directory path."""
        data_dir = Path(self.game_config.research_data_dir)
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    def get_cache_dir(self) -> Path:
        """Get the cache directory path."""
        cache_dir = Path("cache")
        cache_dir.mkdir(exist_ok=True)
        return cache_dir

# Global configuration manager
_config_manager: Optional[ConfigManager] = None

def get_config() -> ConfigManager:
    """Get the global configuration manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_game_config() -> GameConfig:
    """Get game configuration."""
    return get_config().get_game_config()

def get_web_config() -> WebConfig:
    """Get web configuration."""
    return get_config().get_web_config() 