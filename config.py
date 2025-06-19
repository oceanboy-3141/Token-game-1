"""
Configuration Module for Token Quest
Centralized configuration settings to avoid hardcoded values throughout the codebase
"""
import os

class GameConfig:
    """Game-related configuration settings"""
    # Default game settings
    DEFAULT_TIME_LIMIT = 30  # seconds for speed mode
    DEFAULT_ROUNDS = 10
    MIN_ROUNDS = 1
    MAX_ROUNDS = 50
    
    # Scoring settings
    PERFECT_GUESS_POINTS = 100
    EXCELLENT_GUESS_POINTS = 50
    GOOD_GUESS_POINTS = 25
    CLOSE_GUESS_POINTS = 10
    
    # Distance categories
    PERFECT_DISTANCE = 0
    EXCELLENT_MAX_DISTANCE = 10
    GOOD_MAX_DISTANCE = 50
    CLOSE_MAX_DISTANCE = 200
    
    # Game modes
    VALID_MODES = ['normal', 'synonym', 'antonym', 'speed']
    VALID_DIFFICULTIES = ['easy', 'medium', 'hard', 'mixed']
    VALID_CATEGORIES = ['all', 'emotions', 'size', 'speed', 'quality', 'temperature', 'brightness', 'actions', 'difficulty']

class ValidationConfig:
    """Input validation settings"""
    MAX_GUESS_LENGTH = 50
    MIN_GUESS_LENGTH = 1
    MAX_PLAYER_NAME_LENGTH = 20
    MIN_PLAYER_NAME_LENGTH = 1
    
    # Regex patterns
    VALID_GUESS_PATTERN = r'^[a-zA-Z0-9\s\-\'\.]+$'
    VALID_NAME_PATTERN = r'^[a-zA-Z0-9\s\-\'\.]+$'

class DataConfig:
    """Data collection and storage settings"""
    DEFAULT_DATA_DIR = 'game_data'
    SESSION_CLEANUP_INTERVAL_HOURS = 24
    SESSION_CLEANUP_CHECK_FREQUENCY = 100  # every N requests
    
    # File settings
    LEADERBOARD_TOP_COUNT = 100
    DAILY_LEADERBOARD_COUNT = 10
    DAILY_DATA_RETENTION_DAYS = 30
    
    # CSV export settings
    MAX_EXPORT_ROWS = 10000

class TokenConfig:
    """Token handling configuration"""
    DEFAULT_ENCODING = "cl100k_base"
    TOKEN_SEARCH_RANGE = 100000  # reasonable upper bound for token IDs
    NEARBY_TOKENS_COUNT = 10
    
    # Word filtering for token analysis
    MIN_WORD_LENGTH = 2
    MAX_WORD_LENGTH = 15

class SecurityConfig:
    """Security and safety settings"""
    # File operations
    FILE_OPERATION_TIMEOUT = 30  # seconds
    MAX_BACKUP_FILES = 5
    
    # Rate limiting (if implemented)
    MAX_REQUESTS_PER_MINUTE = 60
    
    # Flask secret key (use environment variable in production)
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')

class LoggingConfig:
    """Logging configuration"""
    DEFAULT_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Log file settings
    MAX_LOG_FILE_SIZE_MB = 10
    MAX_LOG_FILES = 5

class CloudRunConfig:
    """Cloud Run specific configuration"""
    # Port configuration
    PORT = int(os.environ.get('PORT', 8080))
    
    # Environment detection
    IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production'
    
    # Resource limits
    MEMORY_LIMIT = '1Gi'
    CPU_LIMIT = '1'
    MAX_INSTANCES = 10
    CONCURRENCY = 80
    
    # Timeout settings
    REQUEST_TIMEOUT = 300  # 5 minutes
    
    # Health check settings
    HEALTH_CHECK_PATH = '/health' 