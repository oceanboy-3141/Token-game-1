"""
Comprehensive Achievement System Tests
Tests all 25+ achievements across categories to verify they trigger correctly
"""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from achievements import AchievementManager


class TestAchievements(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with fresh achievement manager"""
        # Create temporary directory for test data
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock the achievements module's file operations to use temp directory
        self.patcher = patch('achievements.os.path.join')
        self.mock_join = self.patcher.start()
        
        def mock_join_func(*args):
            if len(args) >= 2 and args[0] == 'game_data':
                return os.path.join(self.temp_dir, *args[1:])
            return os.path.join(*args)
        
        self.mock_join.side_effect = mock_join_func
        
        # Create achievement manager after mocking
        self.achievement_manager = AchievementManager()
    
    def tearDown(self):
        """Clean up test environment"""
        # Stop the patcher
        self.patcher.stop()
        
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_test_achievement(self):
        """Test the test achievement (should unlock on first game)"""
        initial_unlocked = len(self.achievement_manager.get_unlocked_achievements())
        
        # Track game start event
        newly_unlocked = self.achievement_manager.track_game_event("game_started")
        
        # Test achievement should be unlocked
        self.assertGreaterEqual(len(newly_unlocked), 1)
        test_unlocked = any(ach.id == "test_achievement" for ach in newly_unlocked)
        self.assertTrue(test_unlocked)
        self.assertTrue(self.achievement_manager.achievements["test_achievement"].unlocked)
    
    def test_accuracy_achievements(self):
        """Test all accuracy-based achievements"""
        # Test Perfect Guesser (10 perfect scores)
        for i in range(10):
            self.achievement_manager.track_perfect_guess()
        
        achievements = self.achievement_manager.get_unlocked_achievements()
        perfect_guesser = next((a for a in achievements if a['id'] == 'perfect_guesser'), None)
        self.assertIsNotNone(perfect_guesser, "Perfect Guesser achievement should be unlocked")
    
    def test_streak_achievements(self):
        """Test streak-based achievements"""
        # Test Word Sniper (3 perfects in a row)
        for i in range(3):
            self.achievement_manager.track_game_event("perfect_guess")
        self.assertTrue(self.achievement_manager.achievements["word_sniper"].unlocked)
        
        # Test Hot Streak (3 correct in a row)
        self.achievement_manager.stats['max_correct_streak'] = 0  # Reset
        for i in range(3):
            self.achievement_manager.track_game_event("excellent_guess")
        self.assertTrue(self.achievement_manager.achievements["hot_streak"].unlocked)
        
        # Test On Fire (5 correct in a row)
        self.achievement_manager.stats['max_correct_streak'] = 0  # Reset
        for i in range(5):
            self.achievement_manager.track_game_event("perfect_guess")
        self.assertTrue(self.achievement_manager.achievements["on_fire"].unlocked)
        
        # Test Unstoppable (7 correct in a row)
        self.achievement_manager.stats['max_correct_streak'] = 0  # Reset
        for i in range(7):
            self.achievement_manager.track_game_event("perfect_guess")
        self.assertTrue(self.achievement_manager.achievements["unstoppable"].unlocked)
    
    def test_exploration_achievements(self):
        """Test exploration-based achievements"""
        # Test Word Explorer (50 different words)
        for i in range(50):
            self.achievement_manager.track_game_event("word_tried", word=f"word{i}")
        self.assertTrue(self.achievement_manager.achievements["word_explorer"].unlocked)
        
        # Test Vocabulary Master (100 different words)
        for i in range(50, 100):  # Add 50 more unique words
            self.achievement_manager.track_game_event("word_tried", word=f"word{i}")
        self.assertTrue(self.achievement_manager.achievements["vocabulary_master"].unlocked)
        
        # Test Token Researcher (25 games)
        for i in range(25):
            self.achievement_manager.track_game_event("game_started")
        self.assertTrue(self.achievement_manager.achievements["token_researcher"].unlocked)
    
    def test_mode_mastery_achievements(self):
        """Test mode mastery achievements"""
        # Test Synonym Specialist (5 normal mode wins)
        for i in range(5):
            self.achievement_manager.track_game_event("game_won", mode="normal", score=1000)
        self.assertTrue(self.achievement_manager.achievements["synonym_specialist"].unlocked)
        
        # Test Antonym Expert (5 antonym mode wins)
        for i in range(5):
            self.achievement_manager.track_game_event("game_won", mode="antonym", score=1000)
        self.assertTrue(self.achievement_manager.achievements["antonym_expert"].unlocked)
        
        # Test Category King (8 categories)
        categories = ['emotions', 'size', 'speed', 'quality', 'temperature', 'brightness', 'actions', 'difficulty']
        for category in categories:
            self.achievement_manager.track_game_event("category_played", category=category)
        self.assertTrue(self.achievement_manager.achievements["category_king"].unlocked)
    
    def test_educational_achievements(self):
        """Test educational achievements"""
        # Test Token Student (25 hints)
        for i in range(25):
            self.achievement_manager.track_game_event("hint_viewed")
        self.assertTrue(self.achievement_manager.achievements["token_student"].unlocked)
        
        # Test Token Scholar (complete tutorial)
        self.achievement_manager.track_game_event("tutorial_completed")
        self.assertTrue(self.achievement_manager.achievements["token_scholar"].unlocked)
        
        # Test Research Contributor (5 data exports)
        for i in range(5):
            self.achievement_manager.track_game_event("data_exported")
        self.assertTrue(self.achievement_manager.achievements["research_contributor"].unlocked)
    
    def test_special_achievements(self):
        """Test special achievements"""
        # Test Lucky Shot (perfect on first guess)
        self.achievement_manager.track_game_event("perfect_guess", first_guess_of_round=True)
        self.assertTrue(self.achievement_manager.achievements["lucky_shot"].unlocked)
        
        # Test Comeback Kid (win after being behind)
        self.achievement_manager.track_game_event("game_won", mode="normal", score=1000, comeback=True)
        self.assertTrue(self.achievement_manager.achievements["comeback_kid"].unlocked)
    
    def test_score_achievements(self):
        """Test score-based achievements"""
        # Test Point Collector (50,000 total points)
        self.achievement_manager.track_game_event("game_won", mode="normal", score=50000)
        self.assertTrue(self.achievement_manager.achievements["point_collector"].unlocked)
    
    def test_social_achievements(self):
        """Test social achievements"""
        # Test Leaderboard Climber (5 submissions)
        for i in range(5):
            self.achievement_manager.track_game_event("leaderboard_submission")
        self.assertTrue(self.achievement_manager.achievements["leaderboard_climber"].unlocked)
    
    def test_achievement_progress_tracking(self):
        """Test that achievement progress is tracked correctly"""
        # Test progress tracking for word explorer
        for i in range(25):  # Halfway to 50
            self.achievement_manager.track_game_event("word_tried", word=f"test{i}")
        
        progress = self.achievement_manager.get_achievement_progress("word_explorer")
        self.assertEqual(progress['progress'], 25)
        self.assertEqual(progress['target'], 50)
        self.assertEqual(progress['percentage'], 50.0)
        self.assertFalse(progress['unlocked'])
    
    def test_achievement_categories(self):
        """Test achievement categorization"""
        accuracy_achievements = self.achievement_manager.get_achievements_by_category("accuracy")
        self.assertEqual(len(accuracy_achievements), 3)  # perfect_shot, sharpshooter, marksman
        
        streak_achievements = self.achievement_manager.get_achievements_by_category("streaks")
        self.assertEqual(len(streak_achievements), 4)  # word_sniper, hot_streak, on_fire, unstoppable
        
        all_achievements = self.achievement_manager.get_achievements_by_category()
        self.assertGreaterEqual(len(all_achievements), 25)  # Should have 25+ achievements
    
    def test_stats_summary(self):
        """Test stats summary functionality"""
        # Add some stats
        self.achievement_manager.track_game_event("game_started")
        self.achievement_manager.track_game_event("perfect_guess")
        self.achievement_manager.track_game_event("word_tried", word="test")
        
        stats = self.achievement_manager.get_stats_summary()
        
        self.assertEqual(stats['games_played'], 1)
        self.assertEqual(stats['perfects'], 1)
        self.assertEqual(stats['words_tried'], 1)
        self.assertGreaterEqual(stats['achievements_unlocked'], 1)
        self.assertGreater(stats['completion_percentage'], 0)


if __name__ == '__main__':
    unittest.main() 