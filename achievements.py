"""
Token Quest Achievements System
Tracks and manages player achievements and unlocks
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class Achievement:
    def __init__(self, id: str, name: str, description: str, icon: str, 
                 category: str, target_value: int = 1, hidden: bool = False):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.target_value = target_value
        self.hidden = hidden
        self.unlocked = False
        self.unlock_date = None
        self.progress = 0


class AchievementManager:
    def __init__(self):
        self.achievements = {}
        self.stats = {
            'games_played': 0,
            'total_score': 0,
            'perfects': 0,
            'excellents': 0,
            'perfect_streak': 0,
            'max_perfect_streak': 0,
            'correct_streak': 0,
            'max_correct_streak': 0,
            'words_tried': set(),
            'hints_viewed': 0,
            'tutorials_completed': 0,
            'data_exports': 0,
            'leaderboard_submissions': 0,
            'mode_wins': {'normal': 0, 'antonym': 0, 'category': 0},
            'categories_played': set(),
            'night_games': 0,
            'morning_games': 0,
            'comeback_wins': 0
        }
        
        self._define_achievements()
        self._load_progress()
        self._reset_test_achievements()
    
    def _define_achievements(self):
        # Test Achievement (resets each session)
        self._add_achievement("test_achievement", "🧪 Test Achievement", "Start any game to test the notification system", "🧪", "test", 1)
        
        # Accuracy Achievements
        self._add_achievement("perfect_shot", "Perfect Shot", "Get a perfect match (distance 0-1)", "🎯", "accuracy", 1)
        self._add_achievement("sharpshooter", "Sharpshooter", "Get 5 perfect matches", "🔫", "accuracy", 5)
        self._add_achievement("marksman", "Marksman", "Get 10 perfect matches", "🏹", "accuracy", 10)
        self._add_achievement("word_sniper", "Word Sniper", "Get 3 perfects in a row", "🎯", "streaks", 3)
        
        # Exploration Achievements
        self._add_achievement("word_explorer", "Word Explorer", "Try 50 different words", "🌍", "exploration", 50)
        self._add_achievement("vocabulary_master", "Vocabulary Master", "Try 100 different words", "📚", "exploration", 100)
        self._add_achievement("token_researcher", "Token Researcher", "Play 25 complete games", "🔬", "exploration", 25)
        
        # Mode Mastery Achievements
        self._add_achievement("synonym_specialist", "Synonym Specialist", "Win 5 normal mode games", "💙", "mastery", 5)
        self._add_achievement("antonym_expert", "Antonym Expert", "Win 5 antonym mode games", "🔄", "mastery", 5)
        self._add_achievement("category_king", "Category King", "Play all 8 categories", "👑", "mastery", 8)
        
        # Streak Achievements
        self._add_achievement("hot_streak", "Hot Streak", "Get 3 correct guesses in a row", "🔥", "streaks", 3)
        self._add_achievement("on_fire", "On Fire", "Get 5 correct guesses in a row", "🔥", "streaks", 5)
        self._add_achievement("unstoppable", "Unstoppable", "Get 7 correct guesses in a row", "🌟", "streaks", 7)
        
        # Educational Achievements
        self._add_achievement("token_student", "Token Student", "View hints 25 times", "🎓", "education", 25)
        self._add_achievement("token_scholar", "Token Scholar", "Complete the tutorial", "📖", "education", 1)
        self._add_achievement("research_contributor", "Research Contributor", "Export data 5 times", "📊", "education", 5)
        
        # Special Achievements
        self._add_achievement("lucky_shot", "Lucky Shot", "Get a perfect on your first guess of a round", "🍀", "special", 1)
        self._add_achievement("comeback_kid", "Comeback Kid", "Win a game after being behind at halftime", "💪", "special", 1)
        self._add_achievement("night_owl", "Night Owl", "Play 10 games after 10 PM", "🦉", "special", 10)
        self._add_achievement("early_bird", "Early Bird", "Play 10 games before 6 AM", "🐦", "special", 10)
        self._add_achievement("speed_demon", "Speed Demon", "Complete a game in under 2 minutes", "⚡", "special", 1)
        
        # Score Achievements
        self._add_achievement("high_scorer", "High Scorer", "Score 8000+ points in a single game", "💯", "score", 8000)
        self._add_achievement("point_collector", "Point Collector", "Accumulate 50,000 total points", "��", "score", 50000)
        
        # Social Achievements
        self._add_achievement("leaderboard_climber", "Leaderboard Climber", "Submit 5 scores to leaderboard", "🏔️", "social", 5)
    
    def _add_achievement(self, id: str, name: str, description: str, icon: str, 
                        category: str, target_value: int = 1, hidden: bool = False):
        self.achievements[id] = Achievement(id, name, description, icon, category, target_value, hidden)
    
    def _load_progress(self):
        try:
            achievements_file = os.path.join('game_data', 'achievements.json')
            if os.path.exists(achievements_file):
                with open(achievements_file, 'r') as f:
                    data = json.load(f)
                    
                    if 'stats' in data:
                        saved_stats = data['stats']
                        if 'words_tried' in saved_stats:
                            saved_stats['words_tried'] = set(saved_stats['words_tried'])
                        if 'categories_played' in saved_stats:
                            saved_stats['categories_played'] = set(saved_stats['categories_played'])
                        self.stats.update(saved_stats)
                    
                    if 'achievements' in data:
                        for ach_id, ach_data in data['achievements'].items():
                            if ach_id in self.achievements:
                                achievement = self.achievements[ach_id]
                                achievement.progress = ach_data.get('progress', 0)
                                achievement.unlocked = ach_data.get('unlocked', False)
                                achievement.unlock_date = ach_data.get('unlock_date')
        except Exception as e:
            print(f"Error loading achievements: {e}")
    
    def _save_progress(self):
        try:
            os.makedirs('game_data', exist_ok=True)
            achievements_file = os.path.join('game_data', 'achievements.json')
            
            stats_to_save = self.stats.copy()
            stats_to_save['words_tried'] = list(self.stats['words_tried'])
            stats_to_save['categories_played'] = list(self.stats['categories_played'])
            
            achievements_data = {}
            for ach_id, achievement in self.achievements.items():
                achievements_data[ach_id] = {
                    'progress': achievement.progress,
                    'unlocked': achievement.unlocked,
                    'unlock_date': achievement.unlock_date
                }
            
            data = {
                'stats': stats_to_save,
                'achievements': achievements_data
            }
            
            with open(achievements_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving achievements: {e}")
    
    def track_game_event(self, event_type: str, **kwargs) -> List[Achievement]:
        newly_unlocked = []
        print(f"🎖️ Achievement tracking: {event_type}")  # Debug logging
        
        if event_type == "game_started":
            self.stats['games_played'] += 1
            print(f"📊 Games played now: {self.stats['games_played']}")  # Debug
            current_hour = datetime.now().hour
            if current_hour >= 22 or current_hour <= 2:
                self.stats['night_games'] += 1
            elif current_hour <= 6:
                self.stats['morning_games'] += 1
        
        elif event_type == "perfect_guess":
            self.stats['perfects'] += 1
            self.stats['perfect_streak'] += 1
            self.stats['correct_streak'] += 1
            self.stats['max_perfect_streak'] = max(self.stats['max_perfect_streak'], self.stats['perfect_streak'])
            self.stats['max_correct_streak'] = max(self.stats['max_correct_streak'], self.stats['correct_streak'])
            
            if kwargs.get('first_guess_of_round', False):
                newly_unlocked.extend(self._check_achievement_unlock('lucky_shot', 1))
        
        elif event_type == "excellent_guess":
            self.stats['excellents'] += 1
            self.stats['correct_streak'] += 1
            self.stats['max_correct_streak'] = max(self.stats['max_correct_streak'], self.stats['correct_streak'])
            self.stats['perfect_streak'] = 0
        
        elif event_type == "incorrect_guess":
            self.stats['perfect_streak'] = 0
            self.stats['correct_streak'] = 0
        
        elif event_type == "word_tried":
            word = kwargs.get('word', '').lower()
            if word:
                self.stats['words_tried'].add(word)
        
        elif event_type == "hint_viewed":
            self.stats['hints_viewed'] += 1
        
        elif event_type == "tutorial_completed":
            self.stats['tutorials_completed'] += 1
        
        elif event_type == "data_exported":
            self.stats['data_exports'] += 1
        
        elif event_type == "leaderboard_submission":
            self.stats['leaderboard_submissions'] += 1
        
        elif event_type == "game_won":
            mode = kwargs.get('mode', 'normal')
            if mode in self.stats['mode_wins']:
                self.stats['mode_wins'][mode] += 1
            
            score = kwargs.get('score', 0)
            self.stats['total_score'] += score
            
            # Check for high scorer achievement (8000+ in single game)
            if score >= 8000:
                newly_unlocked.extend(self._check_achievement_unlock('high_scorer', 1))
            
            if kwargs.get('comeback', False):
                self.stats['comeback_wins'] += 1
        
        elif event_type == "category_played":
            category = kwargs.get('category')
            if category and category != 'all':
                self.stats['categories_played'].add(category)
        
        newly_unlocked.extend(self._check_all_achievements())
        self._save_progress()
        
        if newly_unlocked:
            print(f"🏆 New achievements unlocked: {[a.name for a in newly_unlocked]}")  # Debug
        
        return newly_unlocked
    
    def _reset_test_achievements(self):
        """Reset test achievements each session for testing purposes."""
        if "test_achievement" in self.achievements:
            test_ach = self.achievements["test_achievement"]
            test_ach.unlocked = False
            test_ach.progress = 0
            test_ach.unlock_date = None
    
    def _check_all_achievements(self) -> List[Achievement]:
        newly_unlocked = []
        
        # Check test achievement
        newly_unlocked.extend(self._check_achievement_unlock('test_achievement', self.stats['games_played']))
        
        newly_unlocked.extend(self._check_achievement_unlock('perfect_shot', self.stats['perfects']))
        newly_unlocked.extend(self._check_achievement_unlock('sharpshooter', self.stats['perfects']))
        newly_unlocked.extend(self._check_achievement_unlock('marksman', self.stats['perfects']))
        newly_unlocked.extend(self._check_achievement_unlock('word_sniper', self.stats['max_perfect_streak']))
        
        newly_unlocked.extend(self._check_achievement_unlock('hot_streak', self.stats['max_correct_streak']))
        newly_unlocked.extend(self._check_achievement_unlock('on_fire', self.stats['max_correct_streak']))
        newly_unlocked.extend(self._check_achievement_unlock('unstoppable', self.stats['max_correct_streak']))
        
        newly_unlocked.extend(self._check_achievement_unlock('word_explorer', len(self.stats['words_tried'])))
        newly_unlocked.extend(self._check_achievement_unlock('vocabulary_master', len(self.stats['words_tried'])))
        newly_unlocked.extend(self._check_achievement_unlock('token_researcher', self.stats['games_played']))
        
        newly_unlocked.extend(self._check_achievement_unlock('token_student', self.stats['hints_viewed']))
        newly_unlocked.extend(self._check_achievement_unlock('token_scholar', self.stats['tutorials_completed']))
        newly_unlocked.extend(self._check_achievement_unlock('research_contributor', self.stats['data_exports']))
        
        newly_unlocked.extend(self._check_achievement_unlock('synonym_specialist', self.stats['mode_wins']['normal']))
        newly_unlocked.extend(self._check_achievement_unlock('antonym_expert', self.stats['mode_wins']['antonym']))
        newly_unlocked.extend(self._check_achievement_unlock('category_king', len(self.stats['categories_played'])))
        
        newly_unlocked.extend(self._check_achievement_unlock('night_owl', self.stats['night_games']))
        newly_unlocked.extend(self._check_achievement_unlock('early_bird', self.stats['morning_games']))
        newly_unlocked.extend(self._check_achievement_unlock('comeback_kid', self.stats['comeback_wins']))
        
        newly_unlocked.extend(self._check_achievement_unlock('point_collector', self.stats['total_score']))
        newly_unlocked.extend(self._check_achievement_unlock('leaderboard_climber', self.stats['leaderboard_submissions']))
        
        return newly_unlocked
    
    def _check_achievement_unlock(self, achievement_id: str, current_value: int = None) -> List[Achievement]:
        if achievement_id not in self.achievements:
            return []
        
        achievement = self.achievements[achievement_id]
        
        if achievement.unlocked:
            return []
        
        if current_value is not None:
            achievement.progress = current_value
        
        if achievement.progress >= achievement.target_value:
            achievement.unlocked = True
            achievement.unlock_date = datetime.now().isoformat()
            return [achievement]
        
        return []
    
    def get_achievements_by_category(self, category: str = None) -> List[Achievement]:
        if category is None:
            return list(self.achievements.values())
        return [ach for ach in self.achievements.values() if ach.category == category]
    
    def get_unlocked_achievements(self) -> List[Achievement]:
        return [ach for ach in self.achievements.values() if ach.unlocked]
    
    def get_all_achievements(self) -> List[Dict]:
        """Get all achievements with their data"""
        return [
            {
                'id': ach.id,
                'name': ach.name,
                'description': ach.description,
                'icon': ach.icon,
                'category': ach.category,
                'progress': ach.progress,
                'target': ach.target_value,
                'unlocked': ach.unlocked,
                'unlock_date': ach.unlock_date,
                'percentage': min(100, (ach.progress / ach.target_value) * 100)
            }
            for ach in self.achievements.values()
        ]
    
    def get_achievement_progress(self, achievement_id: str) -> Dict:
        if achievement_id not in self.achievements:
            return {}
        
        achievement = self.achievements[achievement_id]
        return {
            'id': achievement.id,
            'name': achievement.name,
            'description': achievement.description,
            'icon': achievement.icon,
            'category': achievement.category,
            'progress': achievement.progress,
            'target': achievement.target_value,
            'unlocked': achievement.unlocked,
            'unlock_date': achievement.unlock_date,
            'percentage': min(100, (achievement.progress / achievement.target_value) * 100)
        }
    
    def get_stats_summary(self) -> Dict:
        return {
            'games_played': self.stats['games_played'],
            'total_score': self.stats['total_score'],
            'perfects': self.stats['perfects'],
            'words_tried': len(self.stats['words_tried']),
            'max_streak': self.stats['max_correct_streak'],
            'achievements_unlocked': len(self.get_unlocked_achievements()),
            'total_achievements': len(self.achievements),
            'completion_percentage': (len(self.get_unlocked_achievements()) / len(self.achievements)) * 100
        } 