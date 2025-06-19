"""
Achievement System for Token Quest
Tracks player progress and unlocks achievements based on gameplay
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logger = logging.getLogger(__name__)


class Achievement:
    def __init__(self, id: str, name: str, description: str, category: str, 
                 condition: Dict, reward_points: int = 0, icon: str = "🏆"):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.condition = condition
        self.reward_points = reward_points
        self.icon = icon
        self.unlocked = False
        self.unlock_date = None
        self.progress = 0
        self.max_progress = condition.get('target_value', 1)

class AchievementManager:
    def __init__(self, achievements_file='game_data/achievements.json'):
        self.achievements_file = achievements_file
        self.achievements = {}
        self.stats = {
            'games_played': 0,
            'total_score': 0,
            'perfect_guesses': 0,
            'hints_used': 0,
            'best_streak': 0,
            'current_streak': 0,
            'total_guesses': 0,
            'distances_under_10': 0,
            'distances_under_50': 0,
            'games_won': 0,
            'different_modes_played': set(),
            'categories_mastered': set(),
            'total_playtime_minutes': 0
        }
        
        # Define all achievements
        self._define_achievements()
        
        # Load existing progress
        self._load_achievements()

    def _define_achievements(self):
        """Define all available achievements."""
        achievement_definitions = [
            # Beginner achievements
            {
                'id': 'first_game',
                'name': 'First Steps',
                'description': 'Complete your first game',
                'category': 'beginner',
                'condition': {'type': 'games_played', 'operator': '>=', 'target_value': 1},
                'reward_points': 10,
                'icon': '🎮'
            },
            {
                'id': 'perfect_guess',
                'name': 'Bull\'s Eye',
                'description': 'Make a perfect guess (distance = 0)',
                'category': 'skill',
                'condition': {'type': 'perfect_guesses', 'operator': '>=', 'target_value': 1},
                'reward_points': 25,
                'icon': '🎯'
            },
            {
                'id': 'close_call',
                'name': 'Close Call',
                'description': 'Get within 10 tokens of the target',
                'category': 'skill',
                'condition': {'type': 'distances_under_10', 'operator': '>=', 'target_value': 5},
                'reward_points': 15,
                'icon': '🔥'
            },
            
            # Progress achievements
            {
                'id': 'novice_player',
                'name': 'Novice Player',
                'description': 'Play 5 games',
                'category': 'progress',
                'condition': {'type': 'games_played', 'operator': '>=', 'target_value': 5},
                'reward_points': 20,
                'icon': '🎭'
            },
            {
                'id': 'experienced_player',
                'name': 'Experienced Player',
                'description': 'Play 25 games',
                'category': 'progress',
                'condition': {'type': 'games_played', 'operator': '>=', 'target_value': 25},
                'reward_points': 50,
                'icon': '🎖️'
            },
            {
                'id': 'token_master',
                'name': 'Token Master',
                'description': 'Play 100 games',
                'category': 'mastery',
                'condition': {'type': 'games_played', 'operator': '>=', 'target_value': 100},
                'reward_points': 100,
                'icon': '👑'
            },
            
            # Score achievements
            {
                'id': 'high_scorer',
                'name': 'High Scorer',
                'description': 'Reach 1000 total points',
                'category': 'scoring',
                'condition': {'type': 'total_score', 'operator': '>=', 'target_value': 1000},
                'reward_points': 30,
                'icon': '⭐'
            },
            {
                'id': 'point_collector',
                'name': 'Point Collector',
                'description': 'Reach 5000 total points',
                'category': 'scoring',
                'condition': {'type': 'total_score', 'operator': '>=', 'target_value': 5000},
                'reward_points': 75,
                'icon': '💎'
            },
            
            # Special achievements
            {
                'id': 'streak_master',
                'name': 'Streak Master',
                'description': 'Get 5 correct guesses in a row',
                'category': 'special',
                'condition': {'type': 'best_streak', 'operator': '>=', 'target_value': 5},
                'reward_points': 40,
                'icon': '🔥'
            },
            {
                'id': 'no_hints_needed',
                'name': 'No Hints Needed',
                'description': 'Complete a game without using hints',
                'category': 'special',
                'condition': {'type': 'no_hint_game', 'operator': '==', 'target_value': 1},
                'reward_points': 35,
                'icon': '🧠'
            },
            
            # Mode-specific achievements
            {
                'id': 'mode_explorer',
                'name': 'Mode Explorer',
                'description': 'Try all different game modes',
                'category': 'exploration',
                'condition': {'type': 'different_modes_played', 'operator': '>=', 'target_value': 3},
                'reward_points': 45,
                'icon': '🗺️'
            }
        ]
        
        # Create Achievement objects
        for defn in achievement_definitions:
            achievement = Achievement(**defn)
            self.achievements[achievement.id] = achievement

    def _load_achievements(self):
        """Load achievement progress from file."""
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r') as f:
                    data = json.load(f)
                    
                    # Load stats
                    self.stats.update(data.get('stats', {}))
                    
                    # Convert set back from list for JSON compatibility
                    if 'different_modes_played' in self.stats and isinstance(self.stats['different_modes_played'], list):
                        self.stats['different_modes_played'] = set(self.stats['different_modes_played'])
                    if 'categories_mastered' in self.stats and isinstance(self.stats['categories_mastered'], list):
                        self.stats['categories_mastered'] = set(self.stats['categories_mastered'])
                    
                    # Load achievement progress
                    achievements_data = data.get('achievements', {})
                    for achievement_id, progress_data in achievements_data.items():
                        if achievement_id in self.achievements:
                            self.achievements[achievement_id].unlocked = progress_data.get('unlocked', False)
                            self.achievements[achievement_id].unlock_date = progress_data.get('unlock_date')
                            self.achievements[achievement_id].progress = progress_data.get('progress', 0)
                            
        except Exception as e:
            logger.error(f"Error loading achievements file: {e}")
        except:
            logger.error(f"Unexpected error loading achievements")

    def _save_achievements(self):
        """Save achievement progress to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.achievements_file), exist_ok=True)
            
            # Prepare data for JSON serialization
            stats_for_json = self.stats.copy()
            # Convert sets to lists for JSON compatibility
            if 'different_modes_played' in stats_for_json and isinstance(stats_for_json['different_modes_played'], set):
                stats_for_json['different_modes_played'] = list(stats_for_json['different_modes_played'])
            if 'categories_mastered' in stats_for_json and isinstance(stats_for_json['categories_mastered'], set):
                stats_for_json['categories_mastered'] = list(stats_for_json['categories_mastered'])
            
            data = {
                'stats': stats_for_json,
                'achievements': {
                    achievement_id: {
                        'unlocked': achievement.unlocked,
                        'unlock_date': achievement.unlock_date,
                        'progress': achievement.progress,
                        'max_progress': achievement.max_progress
                    }
                    for achievement_id, achievement in self.achievements.items()
                },
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.achievements_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving achievements file: {e}")
        except:
            logger.error(f"Unexpected error saving achievements")

    def track_event(self, event_type: str, data: Dict[str, Any] = None):
        """Track a game event and update achievements."""
        if data is None:
            data = {}
            
        logger.debug(f"Achievement tracking: {event_type}")
        
        # Update stats based on event type
        if event_type == 'game_completed':
            self.stats['games_played'] += 1
            logger.debug(f"Games played now: {self.stats['games_played']}")
            self.stats['total_score'] += data.get('final_score', 0)
            if data.get('won', False):
                self.stats['games_won'] += 1
            
            # Track game mode
            game_mode = data.get('game_mode', 'normal')
            self.stats['different_modes_played'].add(game_mode)
            
            # Check for no-hints achievement
            if data.get('hints_used', 0) == 0:
                self._check_condition_achievement('no_hints_needed', 'no_hint_game', 1)
            
        elif event_type == 'guess_made':
            self.stats['total_guesses'] += 1
            distance = data.get('distance', float('inf'))
            
            if distance == 0:
                self.stats['perfect_guesses'] += 1
                self.stats['current_streak'] += 1
                self.stats['best_streak'] = max(self.stats['best_streak'], self.stats['current_streak'])
            else:
                self.stats['current_streak'] = 0
                
            if distance <= 10:
                self.stats['distances_under_10'] += 1
            if distance <= 50:
                self.stats['distances_under_50'] += 1
                
        elif event_type == 'hint_used':
            self.stats['hints_used'] += 1
        
        # Check all achievements for updates
        self._check_achievements()
        
        # Save progress
        self._save_achievements()

    def _check_achievements(self):
        """Check all achievements for completion."""
        newly_unlocked = []
        
        for achievement in self.achievements.values():
            if not achievement.unlocked:
                # Update progress and check completion
                old_progress = achievement.progress
                achievement.progress = self._calculate_progress(achievement)
                
                # Check if achievement is unlocked
                if self._check_condition(achievement.condition):
                    achievement.unlocked = True
                    achievement.unlock_date = datetime.now().isoformat()
                    newly_unlocked.append(achievement)
        
        if newly_unlocked:
            logger.info(f"New achievements unlocked: {[a.name for a in newly_unlocked]}")
        
        return newly_unlocked

    def _calculate_progress(self, achievement: Achievement) -> int:
        """Calculate current progress for an achievement."""
        condition = achievement.condition
        stat_type = condition['type']
        
        if stat_type in self.stats:
            current_value = self.stats[stat_type]
            if isinstance(current_value, set):
                return len(current_value)
            return current_value
        
        return 0

    def _check_condition_achievement(self, achievement_id: str, stat_type: str, value: Any):
        """Helper to check a specific condition achievement."""
        if achievement_id in self.achievements:
            achievement = self.achievements[achievement_id]
            if not achievement.unlocked and self._check_single_condition(stat_type, value, achievement.condition):
                achievement.unlocked = True
                achievement.unlock_date = datetime.now().isoformat()
                return [achievement]
        return []

    def _check_condition(self, condition: Dict) -> bool:
        """Check if a condition is met."""
        stat_type = condition['type']
        operator = condition['operator']
        target_value = condition['target_value']
        
        if stat_type not in self.stats:
            return False
        
        current_value = self.stats[stat_type]
        if isinstance(current_value, set):
            current_value = len(current_value)
        
        return self._check_single_condition(stat_type, current_value, condition)

    def _check_single_condition(self, stat_type: str, current_value: Any, condition: Dict) -> bool:
        """Check a single condition."""
        operator = condition['operator']
        target_value = condition['target_value']
        
        if operator == '>=':
            return current_value >= target_value
        elif operator == '==':
            return current_value == target_value
        elif operator == '>':
            return current_value > target_value
        elif operator == '<=':
            return current_value <= target_value
        elif operator == '<':
            return current_value < target_value
        
        return False

    def get_achievements_summary(self) -> Dict:
        """Get a summary of all achievements."""
        unlocked_count = sum(1 for a in self.achievements.values() if a.unlocked)
        total_count = len(self.achievements)
        
        unlocked_achievements = [
            {
                'id': a.id,
                'name': a.name,
                'description': a.description,
                'category': a.category,
                'icon': a.icon,
                'unlock_date': a.unlock_date,
                'reward_points': a.reward_points
            }
            for a in self.achievements.values() if a.unlocked
        ]
        
        pending_achievements = [
            {
                'id': a.id,
                'name': a.name,
                'description': a.description,
                'category': a.category,
                'icon': a.icon,
                'progress': a.progress,
                'max_progress': a.max_progress,
                'progress_percentage': (a.progress / max(a.max_progress, 1)) * 100,
                'reward_points': a.reward_points
            }
            for a in self.achievements.values() if not a.unlocked
        ]
        
        return {
            'summary': {
                'unlocked_count': unlocked_count,
                'total_count': total_count,
                'completion_percentage': (unlocked_count / total_count) * 100 if total_count > 0 else 0,
                'total_reward_points': sum(a.reward_points for a in self.achievements.values() if a.unlocked)
            },
            'unlocked_achievements': unlocked_achievements,
            'pending_achievements': pending_achievements,
            'stats': self.stats.copy()  # Return a copy to prevent external modification
        }

    def get_achievement_by_id(self, achievement_id: str) -> Dict:
        """Get details of a specific achievement."""
        if achievement_id not in self.achievements:
            return None
        
        achievement = self.achievements[achievement_id]
        return {
            'id': achievement.id,
            'name': achievement.name,
            'description': achievement.description,
            'category': achievement.category,
            'icon': achievement.icon,
            'unlocked': achievement.unlocked,
            'unlock_date': achievement.unlock_date,
            'progress': achievement.progress,
            'max_progress': achievement.max_progress,
            'reward_points': achievement.reward_points
        } 