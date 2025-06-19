"""
Data Collection Module for Token Quest
Basic data collection and logging functionality
"""
import csv
import json
import logging
import os
from datetime import datetime
from typing import List, Dict

# Configure logging
logger = logging.getLogger(__name__)


class DataCollector:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.daily_log_file = os.path.join(data_dir, f"daily_log_{datetime.now().strftime('%Y%m%d')}.json")
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize daily log structure
        self.daily_data = self._load_daily_log()
    
    def _load_daily_log(self) -> Dict:
        """Load existing daily log or create new one."""
        if os.path.exists(self.daily_log_file):
            try:
                with open(self.daily_log_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error reading daily log file {self.daily_log_file}: {e}")
                return self._create_empty_log()
            except Exception as e:
                logger.error(f"Unexpected error reading daily log file {self.daily_log_file}: {e}")
                return self._create_empty_log()
        else:
            return self._create_empty_log()
    
    def _create_empty_log(self) -> Dict:
        """Create empty daily log structure."""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'games': [],
            'total_games': 0,
            'total_score': 0,
            'total_guesses': 0,
            'perfect_guesses': 0
        }
    
    def _save_daily_log(self):
        """Save daily log to file."""
        try:
            with open(self.daily_log_file, 'w') as f:
                json.dump(self.daily_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving daily log: {e}")
    
    def log_game_start(self, game_config: Dict):
        """Log the start of a new game."""
        game_id = f"game_{len(self.daily_data['games']) + 1}_{datetime.now().strftime('%H%M%S')}"
        
        game_entry = {
            'game_id': game_id,
            'start_time': datetime.now().isoformat(),
            'config': game_config,
            'rounds': [],
            'completed': False
        }
        
        self.daily_data['games'].append(game_entry)
        self._save_daily_log()
        
        return game_id
    
    def log_round(self, game_id: str, round_data: Dict):
        """Log a round result."""
        # Find the game
        game = next((g for g in self.daily_data['games'] if g['game_id'] == game_id), None)
        if not game:
            return
        
        round_entry = {
            'round_number': len(game['rounds']) + 1,
            'target_word': round_data.get('target_word', ''),
            'guess': round_data.get('guess', ''),
            'distance': round_data.get('distance', 0),
            'points': round_data.get('points', 0),
            'correct': round_data.get('correct', False),
            'timestamp': datetime.now().isoformat()
        }
        
        game['rounds'].append(round_entry)
        
        # Update daily stats
        self.daily_data['total_guesses'] += 1
        if round_entry['correct']:
            self.daily_data['perfect_guesses'] += 1
        
        self._save_daily_log()
    
    def log_game_completion(self, game_id: str, final_results: Dict):
        """Log game completion."""
        # Find the game
        game = next((g for g in self.daily_data['games'] if g['game_id'] == game_id), None)
        if not game:
            return
        
        game['completed'] = True
        game['end_time'] = datetime.now().isoformat()
        game['final_results'] = final_results
        
        # Update daily totals
        self.daily_data['total_games'] += 1
        self.daily_data['total_score'] += final_results.get('total_score', 0)
        
        self._save_daily_log()
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export collected data to CSV."""
        if not filename:
            filename = f"token_quest_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'game_id', 'round_number', 'target_word', 'guess',
                'distance', 'points', 'correct', 'timestamp'
            ])
            
            # Write data
            for game in self.daily_data['games']:
                for round_data in game.get('rounds', []):
                    writer.writerow([
                        game['game_id'],
                        round_data['round_number'],
                        round_data['target_word'],
                        round_data['guess'],
                        round_data['distance'],
                        round_data['points'],
                        round_data['correct'],
                        round_data['timestamp']
                    ])
        
        return filepath
    
    def get_daily_summary(self) -> Dict:
        """Get summary of today's data."""
        completed_games = [g for g in self.daily_data['games'] if g.get('completed', False)]
        
        if not completed_games:
            return {
                'date': self.daily_data['date'],
                'total_games': 0,
                'average_score': 0,
                'accuracy_rate': 0,
                'total_rounds': 0
            }
        
        total_score = sum(g['final_results'].get('total_score', 0) for g in completed_games)
        total_rounds = sum(len(g.get('rounds', [])) for g in completed_games)
        correct_guesses = sum(1 for g in completed_games for r in g.get('rounds', []) if r.get('correct', False))
        
        return {
            'date': self.daily_data['date'],
            'total_games': len(completed_games),
            'average_score': total_score / len(completed_games) if completed_games else 0,
            'accuracy_rate': (correct_guesses / total_rounds * 100) if total_rounds > 0 else 0,
            'total_rounds': total_rounds,
            'total_guesses': self.daily_data['total_guesses'],
            'perfect_guesses': self.daily_data['perfect_guesses']
        } 