"""
Leaderboard Module
Tracks high scores and statistics across different game modes
"""
import json
import os
from datetime import datetime
from typing import List, Dict


class Leaderboard:
    def __init__(self, data_dir: str = "game_data"):
        self.data_dir = data_dir
        self.leaderboard_file = os.path.join(data_dir, "leaderboard.json")
        self.leaderboard_data = self._load_leaderboard()
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def _load_leaderboard(self) -> Dict:
        """Load leaderboard data from file."""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default structure for new leaderboard
        return {
            'normal': [],
            'antonym': [],
            'category': [],
            'speed': [],
            'all_time_stats': {
                'total_games': 0,
                'total_score': 0,
                'best_accuracy': 0
            }
        }
    
    def _save_leaderboard(self):
        """Save leaderboard data to file."""
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.leaderboard_data, f, indent=2)
    
    def add_score(self, player_name: str, final_results: Dict):
        """Add a new score to the leaderboard."""
        game_mode = final_results.get('game_mode', 'normal')
        
        score_entry = {
            'player_name': player_name,
            'score': final_results['total_score'],
            'accuracy': final_results['accuracy'],
            'correct_guesses': final_results['correct_guesses'],
            'total_rounds': final_results['total_rounds'],
            'average_distance': final_results['average_distance'],
            'best_distance': final_results['best_distance'],
            'difficulty': final_results.get('difficulty', 'mixed'),
            'category': final_results.get('category', 'all'),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to appropriate game mode leaderboard
        if game_mode not in self.leaderboard_data:
            self.leaderboard_data[game_mode] = []
        
        self.leaderboard_data[game_mode].append(score_entry)
        
        # Sort by score (descending)
        self.leaderboard_data[game_mode].sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 50 scores per mode
        self.leaderboard_data[game_mode] = self.leaderboard_data[game_mode][:50]
        
        # Update all-time stats
        self.leaderboard_data['all_time_stats']['total_games'] += 1
        self.leaderboard_data['all_time_stats']['total_score'] += score_entry['score']
        if score_entry['accuracy'] > self.leaderboard_data['all_time_stats']['best_accuracy']:
            self.leaderboard_data['all_time_stats']['best_accuracy'] = score_entry['accuracy']
        
        self._save_leaderboard()
        
        return self._get_rank(game_mode, score_entry['score'])
    
    def _get_rank(self, game_mode: str, score: int) -> int:
        """Get the rank of a score in the leaderboard."""
        scores = [entry['score'] for entry in self.leaderboard_data.get(game_mode, [])]
        scores.sort(reverse=True)
        return scores.index(score) + 1 if score in scores else len(scores) + 1
    
    def get_top_scores(self, game_mode: str = 'normal', limit: int = 10) -> List[Dict]:
        """Get top scores for a specific game mode."""
        return self.leaderboard_data.get(game_mode, [])[:limit]
    
    def get_player_best(self, player_name: str, game_mode: str = 'normal') -> Dict:
        """Get a player's best score in a specific mode."""
        mode_scores = self.leaderboard_data.get(game_mode, [])
        player_scores = [entry for entry in mode_scores if entry['player_name'] == player_name]
        
        if player_scores:
            return max(player_scores, key=lambda x: x['score'])
        return None
    
    def get_statistics(self) -> Dict:
        """Get overall leaderboard statistics."""
        stats = self.leaderboard_data['all_time_stats'].copy()
        
        # Calculate mode-specific stats
        mode_stats = {}
        for mode, scores in self.leaderboard_data.items():
            if mode != 'all_time_stats' and scores:
                mode_stats[mode] = {
                    'total_games': len(scores),
                    'highest_score': max(entry['score'] for entry in scores),
                    'average_score': sum(entry['score'] for entry in scores) / len(scores),
                    'best_accuracy': max(entry['accuracy'] for entry in scores)
                }
        
        stats['mode_statistics'] = mode_stats
        return stats
    
    def is_high_score(self, score: int, game_mode: str = 'normal') -> bool:
        """Check if a score qualifies for the leaderboard."""
        mode_scores = self.leaderboard_data.get(game_mode, [])
        if len(mode_scores) < 10:  # Top 10 leaderboard
            return True
        return score > min(entry['score'] for entry in mode_scores[:10])
    
    def export_leaderboard(self, filename: str = None) -> str:
        """Export leaderboard to a formatted text file."""
        if not filename:
            filename = f"leaderboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("🏆 TOKEN QUEST LEADERBOARD 🏆\n")
            f.write("=" * 50 + "\n\n")
            
            for mode in ['normal', 'antonym', 'category', 'speed']:
                if mode in self.leaderboard_data and self.leaderboard_data[mode]:
                    f.write(f"🎮 {mode.upper()} MODE\n")
                    f.write("-" * 30 + "\n")
                    
                    for i, entry in enumerate(self.leaderboard_data[mode][:10], 1):
                        f.write(f"{i:2d}. {entry['player_name']:<15} | "
                               f"Score: {entry['score']:4d} | "
                               f"Accuracy: {entry['accuracy']:5.1f}% | "
                               f"Date: {entry['date']}\n")
                    f.write("\n")
            
            # Add statistics
            stats = self.get_statistics()
            f.write("📊 OVERALL STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Games Played: {stats['total_games']}\n")
            f.write(f"Average Score: {stats['total_score'] / max(1, stats['total_games']):.1f}\n")
            f.write(f"Best Accuracy Ever: {stats['best_accuracy']:.1f}%\n")
        
        return filepath 