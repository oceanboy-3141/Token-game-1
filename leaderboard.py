"""
Leaderboard System for Token Quest
Manages high scores, player rankings, and competitive features
"""
import json
import logging
import os
from datetime import datetime
from typing import List, Dict

from file_lock_utils import safe_json_write, safe_json_read

# Configure logging
logger = logging.getLogger(__name__)


class Leaderboard:
    def __init__(self, leaderboard_file='game_data/leaderboard.json'):
        self.leaderboard_file = leaderboard_file
        self.leaderboard_data = self._load_leaderboard()
    
    def _load_leaderboard(self) -> Dict:
        """Load leaderboard data from file with race condition protection."""
        # RACE CONDITION FIX: Use safe file reading with locking
        data = safe_json_read(self.leaderboard_file, {
            'high_scores': [],
            'all_time_records': {
                'highest_score': {'score': 0, 'player': '', 'date': ''},
                'most_correct': {'correct': 0, 'player': '', 'date': ''},
                'perfect_games': {'count': 0, 'player': '', 'date': ''},
                'fastest_completion': {'time': float('inf'), 'player': '', 'date': ''}
            },
            'daily_leaders': {},
            'statistics': {
                'total_games_played': 0,
                'total_players': 0,
                'average_score': 0.0
            }
        })
        
        return data
    
    def _save_leaderboard(self):
        """Save leaderboard data to file with race condition protection."""
        os.makedirs(os.path.dirname(self.leaderboard_file), exist_ok=True)
        
        # RACE CONDITION FIX: Use safe file writing with locking
        success = safe_json_write(self.leaderboard_file, self.leaderboard_data, indent=2)
        if not success:
            logger.warning(f"Failed to save leaderboard data to {self.leaderboard_file}")
    
    def submit_score(self, player_name: str, score: int, game_data: Dict) -> Dict:
        """Submit a score to the leaderboard."""
        if not player_name or score < 0:
            return {'success': False, 'error': 'Invalid player name or score'}
        
        # Create score entry
        score_entry = {
            'player': player_name,
            'score': score,
            'date': datetime.now().isoformat(),
            'correct_guesses': game_data.get('correct_guesses', 0),
            'total_rounds': game_data.get('total_rounds', 0),
            'game_mode': game_data.get('game_mode', 'normal'),
            'difficulty': game_data.get('difficulty', 'mixed'),
            'category': game_data.get('category', 'all'),
            'completion_time': game_data.get('completion_time', 0),
            'hints_used': game_data.get('hints_used', 0),
            'accuracy_percentage': (game_data.get('correct_guesses', 0) / max(game_data.get('total_rounds', 1), 1)) * 100
        }
        
        # Add to high scores
        self.leaderboard_data['high_scores'].append(score_entry)
        
        # Sort by score (descending) and keep top 100
        self.leaderboard_data['high_scores'].sort(key=lambda x: x['score'], reverse=True)
        self.leaderboard_data['high_scores'] = self.leaderboard_data['high_scores'][:100]
        
        # Update all-time records
        self._update_records(score_entry)
        
        # Update daily leaders
        self._update_daily_leaders(score_entry)
        
        # Update statistics
        self._update_statistics()
        
        # Save to file
        self._save_leaderboard()
        
        # Determine ranking
        ranking = next((i + 1 for i, entry in enumerate(self.leaderboard_data['high_scores']) 
                       if entry['player'] == player_name and entry['score'] == score), None)
        
        return {
            'success': True,
            'ranking': ranking,
            'total_entries': len(self.leaderboard_data['high_scores']),
            'is_new_record': self._check_new_records(score_entry)
        }
    
    def _update_records(self, score_entry: Dict):
        """Update all-time records if applicable."""
        records = self.leaderboard_data['all_time_records']
        
        # Highest score
        if score_entry['score'] > records['highest_score']['score']:
            records['highest_score'] = {
                'score': score_entry['score'],
                'player': score_entry['player'],
                'date': score_entry['date']
            }
        
        # Most correct guesses
        if score_entry['correct_guesses'] > records['most_correct']['correct']:
            records['most_correct'] = {
                'correct': score_entry['correct_guesses'],
                'player': score_entry['player'],
                'date': score_entry['date']
            }
        
        # Perfect games (all correct)
        if score_entry['accuracy_percentage'] == 100.0:
            if score_entry['player'] not in [r.get('player', '') for r in records.get('perfect_games', [])]:
                if 'perfect_games' not in records or not isinstance(records['perfect_games'], list):
                    records['perfect_games'] = []
                records['perfect_games'].append({
                    'player': score_entry['player'],
                    'score': score_entry['score'],
                    'date': score_entry['date']
                })
        
        # Fastest completion (if completion time is tracked)
        completion_time = score_entry.get('completion_time', 0)
        if completion_time > 0 and completion_time < records['fastest_completion']['time']:
            records['fastest_completion'] = {
                'time': completion_time,
                'player': score_entry['player'],
                'date': score_entry['date']
            }
    
    def _update_daily_leaders(self, score_entry: Dict):
        """Update daily leaderboard."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.leaderboard_data['daily_leaders']:
            self.leaderboard_data['daily_leaders'][today] = []
        
        self.leaderboard_data['daily_leaders'][today].append(score_entry)
        
        # Sort daily scores and keep top 10
        self.leaderboard_data['daily_leaders'][today].sort(key=lambda x: x['score'], reverse=True)
        self.leaderboard_data['daily_leaders'][today] = self.leaderboard_data['daily_leaders'][today][:10]
        
        # Clean up old daily data (keep last 30 days)
        cutoff_date = datetime.now()
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - 30)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        dates_to_remove = [date for date in self.leaderboard_data['daily_leaders'].keys() if date < cutoff_str]
        for date in dates_to_remove:
            del self.leaderboard_data['daily_leaders'][date]
    
    def _update_statistics(self):
        """Update general statistics."""
        stats = self.leaderboard_data['statistics']
        high_scores = self.leaderboard_data['high_scores']
        
        stats['total_games_played'] = len(high_scores)
        stats['total_players'] = len(set(entry['player'] for entry in high_scores))
        
        if high_scores:
            stats['average_score'] = sum(entry['score'] for entry in high_scores) / len(high_scores)
        else:
            stats['average_score'] = 0.0
    
    def _check_new_records(self, score_entry: Dict) -> Dict:
        """Check if this score set any new records."""
        records = self.leaderboard_data['all_time_records']
        new_records = {}
        
        if score_entry['score'] == records['highest_score']['score']:
            new_records['highest_score'] = True
        
        if score_entry['correct_guesses'] == records['most_correct']['correct']:
            new_records['most_correct'] = True
        
        if score_entry['accuracy_percentage'] == 100.0:
            new_records['perfect_game'] = True
        
        completion_time = score_entry.get('completion_time', 0)
        if completion_time > 0 and completion_time == records['fastest_completion']['time']:
            new_records['fastest_completion'] = True
        
        return new_records
    
    def get_leaderboard(self, category: str = 'all', limit: int = 50) -> Dict:
        """Get leaderboard data."""
        if category == 'all':
            scores = self.leaderboard_data['high_scores'][:limit]
        elif category == 'daily':
            today = datetime.now().strftime('%Y-%m-%d')
            scores = self.leaderboard_data['daily_leaders'].get(today, [])[:limit]
        else:
            # Filter by game mode, difficulty, or category
            scores = [entry for entry in self.leaderboard_data['high_scores'] 
                     if entry.get('game_mode') == category or 
                        entry.get('difficulty') == category or 
                        entry.get('category') == category][:limit]
        
        return {
            'scores': scores,
            'records': self.leaderboard_data['all_time_records'],
            'statistics': self.leaderboard_data['statistics']
        }
    
    def get_player_stats(self, player_name: str) -> Dict:
        """Get statistics for a specific player."""
        player_scores = [entry for entry in self.leaderboard_data['high_scores'] 
                        if entry['player'] == player_name]
        
        if not player_scores:
            return {'found': False}
        
        return {
            'found': True,
            'total_games': len(player_scores),
            'best_score': max(score['score'] for score in player_scores),
            'average_score': sum(score['score'] for score in player_scores) / len(player_scores),
            'best_ranking': min(i + 1 for i, entry in enumerate(self.leaderboard_data['high_scores']) 
                              if entry['player'] == player_name),
            'perfect_games': sum(1 for score in player_scores if score['accuracy_percentage'] == 100.0),
            'recent_games': sorted(player_scores, key=lambda x: x['date'], reverse=True)[:5]
        } 