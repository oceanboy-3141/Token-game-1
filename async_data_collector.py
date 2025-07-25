"""
Async Data Collector for Token Quest
High-performance data collection with background processing
"""
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import queue
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class GameSession:
    session_id: str
    start_time: str
    end_time: str = None
    total_games: int = 0
    total_rounds: int = 0
    total_guesses: int = 0

@dataclass
class GameData:
    game_id: str
    session_id: str
    start_time: str
    end_time: str = None
    difficulty: str = None
    game_mode: str = None
    total_rounds: int = 0
    score: int = 0

@dataclass
class RoundData:
    round_id: str
    game_id: str
    target_word: str
    target_token_id: int
    start_time: str
    end_time: str = None
    attempts: int = 0
    hints_used: int = 0

@dataclass
class GuessData:
    guess_id: str
    round_id: str
    guessed_word: str
    guessed_token_id: int
    token_distance: int
    timestamp: str
    is_correct: bool = False
    hint_used: bool = False

class AsyncDataCollector:
    def __init__(self, research_data_dir: str):
        self.research_data_dir = Path(research_data_dir)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure directory exists
        self.research_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup async writing
        self._write_queue = queue.Queue()
        self._write_thread = threading.Thread(target=self._write_worker, daemon=True)
        self._write_thread.start()
        
        # Thread pool for CPU-bound tasks
        self._thread_pool = ThreadPoolExecutor(max_workers=2)
        
        # Initialize session
        self.current_session = GameSession(
            session_id=self.session_id,
            start_time=datetime.now().isoformat()
        )
        
        # Setup file paths
        self.files = {
            'session': self.research_data_dir / f'session_{self.session_id}.json',
            'games': self.research_data_dir / f'games_{self.session_id}.json',
            'rounds': self.research_data_dir / f'rounds_{self.session_id}.json',
            'guesses': self.research_data_dir / f'guesses_{self.session_id}.json',
            'guesses_detailed': self.research_data_dir / f'guesses_detailed_{self.session_id}.csv'
        }
        
        # Initialize CSV files
        self._init_csv_files()
        
        logger.info("Async data collector initialized: %s", research_data_dir)
    
    def _init_csv_files(self):
        """Initialize CSV files with headers."""
        headers = [
            'guess_id', 'round_id', 'game_id', 'session_id',
            'guessed_word', 'guessed_token_id', 'target_word',
            'target_token_id', 'token_distance', 'timestamp',
            'is_correct', 'hint_used', 'game_mode', 'difficulty'
        ]
        
        def _write_headers():
            with open(self.files['guesses_detailed'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        
        self._queue_write(_write_headers)
    
    def _write_worker(self):
        """Background thread that processes write requests."""
        while True:
            try:
                task = self._write_queue.get()
                if task is None:  # Shutdown signal
                    break
                func, args, kwargs = task
                func(*args, **kwargs)
            except Exception as e:
                logger.error("Error in write worker: %s", e, exc_info=True)
            finally:
                self._write_queue.task_done()
    
    def _queue_write(self, func, *args, **kwargs):
        """Queue a write operation to be performed asynchronously."""
        self._write_queue.put((func, args, kwargs))
    
    def start_game(self, game_mode: str, difficulty: str) -> str:
        """Start a new game and return its ID."""
        game_id = f"{self.session_id}_game_{len(self.current_session.games) + 1}"
        game_data = GameData(
            game_id=game_id,
            session_id=self.session_id,
            start_time=datetime.now().isoformat(),
            game_mode=game_mode,
            difficulty=difficulty
        )
        
        def _save_game():
            with open(self.files['games'], 'a', encoding='utf-8') as f:
                json.dump(asdict(game_data), f)
                f.write('\n')
        
        self._queue_write(_save_game)
        return game_id
    
    def record_guess(self, guess_data: GuessData):
        """Record a guess asynchronously."""
        def _save_guess():
            # Save to JSON
            with open(self.files['guesses'], 'a', encoding='utf-8') as f:
                json.dump(asdict(guess_data), f)
                f.write('\n')
            
            # Save to CSV
            with open(self.files['guesses_detailed'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    guess_data.guess_id,
                    guess_data.round_id,
                    guess_data.guessed_word,
                    guess_data.guessed_token_id,
                    guess_data.token_distance,
                    guess_data.timestamp,
                    guess_data.is_correct,
                    guess_data.hint_used
                ])
        
        self._queue_write(_save_guess)
    
    def end_session(self):
        """End the current session and save final data."""
        self.current_session.end_time = datetime.now().isoformat()
        
        def _save_session():
            with open(self.files['session'], 'w', encoding='utf-8') as f:
                json.dump(asdict(self.current_session), f, indent=2)
        
        self._queue_write(_save_session)
        # Signal write thread to stop
        self._write_queue.put(None)
        # Wait for queue to empty
        self._write_queue.join()
        # Shutdown thread pool
        self._thread_pool.shutdown(wait=True)
