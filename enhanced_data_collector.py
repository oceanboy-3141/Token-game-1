"""
Enhanced Data Collector for Token Quest
Comprehensive research data collection and automatic saving for AI researchers
"""
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import time


class EnhancedDataCollector:
    """
    Enhanced data collector that automatically saves comprehensive research data
    for AI researchers studying token relationships and semantic similarity
    """
    
    def __init__(self, research_data_dir: str):
        self.research_data_dir = research_data_dir
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure directory exists
        os.makedirs(research_data_dir, exist_ok=True)
        
        # Comprehensive data storage
        self.session_data = {
            'session_info': {
                'session_id': self.session_id,
                'start_time': datetime.now().isoformat(),
                'end_time': None,
                'total_games': 0,
                'total_rounds': 0,
                'total_guesses': 0
            },
            'games': [],
            'rounds': [],
            'guesses': [],
            'hint_usage': [],
            'educational_interactions': [],
            'token_analysis': [],
            'performance_metrics': []
        }
        
        # Real-time auto-save files
        self.setup_auto_save_files()
        
        print(f"📊 Research data collector ready: {research_data_dir}")
        print(f"🔍 DEBUG: Data collector will save to: {os.path.abspath(research_data_dir)}")
        print(f"🔍 DEBUG: Session ID: {self.session_id}")
        print(f"🔍 DEBUG: Files will be created: {list(self.files.keys())}")
    
    def setup_auto_save_files(self):
        """Setup auto-save files for continuous data collection."""
        timestamp = datetime.now().strftime("%Y%m%d")
        
        # Create daily research files
        self.files = {
            'daily_comprehensive': os.path.join(self.research_data_dir, f"comprehensive_research_data_{timestamp}.json"),
            'guesses_detailed': os.path.join(self.research_data_dir, f"detailed_guesses_{timestamp}.csv"),
            'token_relationships': os.path.join(self.research_data_dir, f"token_relationships_{timestamp}.csv"),
            'semantic_analysis': os.path.join(self.research_data_dir, f"semantic_analysis_{timestamp}.json"),
            'performance_metrics': os.path.join(self.research_data_dir, f"performance_metrics_{timestamp}.csv"),
            'session_summary': os.path.join(self.research_data_dir, f"session_{self.session_id}_summary.json"),
            'session': os.path.join(self.research_data_dir, f"session_{self.session_id}.json")
        }
        
        # Initialize CSV files with headers
        self._initialize_csv_files()
    
    def _initialize_csv_files(self):
        """Initialize CSV files with appropriate headers."""
        # Detailed guesses CSV
        if not os.path.exists(self.files['guesses_detailed']):
            with open(self.files['guesses_detailed'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'session_id', 'game_id', 'round_id', 'guess_number',
                    'target_word', 'target_token_id', 'guess_word', 'guess_token_id',
                    'token_distance', 'semantic_category', 'points_earned', 'total_score',
                    'time_to_guess_ms', 'hint_used', 'game_mode', 'difficulty', 'category',
                    'target_word_length', 'guess_word_length', 'alphabetical_distance',
                    'is_correct', 'accuracy_level', 'educational_context'
                ])
        
        # Token relationships CSV
        if not os.path.exists(self.files['token_relationships']):
            with open(self.files['token_relationships'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'word_pair_id', 'word1', 'word1_token_id', 
                    'word2', 'word2_token_id', 'token_distance', 'semantic_relationship',
                    'game_context', 'player_perceived_similarity', 'actual_similarity_score',
                    'word1_category', 'word2_category', 'frequency_difference',
                    'length_difference', 'alphabetical_closeness'
                ])
        
        # Performance metrics CSV
        if not os.path.exists(self.files['performance_metrics']):
            with open(self.files['performance_metrics'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'session_id', 'metric_type', 'metric_name', 'value',
                    'context', 'game_mode', 'round_number', 'cumulative_score',
                    'accuracy_percentage', 'average_distance', 'improvement_rate'
                ])
    
    def log_game_start(self, game_config: Dict):
        """Log the start of a new game with comprehensive configuration."""
        game_id = f"{self.session_id}_game_{len(self.session_data['games']) + 1}"
        
        game_data = {
            'game_id': game_id,
            'session_id': self.session_id,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'configuration': game_config,
            'rounds': [],
            'total_score': 0,
            'total_rounds': 0,
            'correct_guesses': 0,
            'hints_used': 0,
            'average_response_time': 0,
            'educational_interactions': 0
        }
        
        self.session_data['games'].append(game_data)
        self.session_data['session_info']['total_games'] += 1
        
        # Auto-save immediately
        self._auto_save_session()
        
        print(f"🎮 Game started: {game_id}")
        print(f"🔍 DEBUG: Game data saved to session file")
    
    def log_round_start(self, round_info: Dict):
        """Log the start of a new round with detailed context."""
        round_id = f"{self.session_id}_round_{len(self.session_data['rounds']) + 1}"
        
        round_data = {
            'round_id': round_id,
            'session_id': self.session_id,
            'game_id': self.session_data['games'][-1]['game_id'] if self.session_data['games'] else 'unknown',
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'round_number': round_info.get('current_round', 0),
            'target_word': round_info.get('target_word', ''),
            'target_token_id': round_info.get('target_token_id', 0),
            'game_mode': round_info.get('game_mode', 'normal'),
            'difficulty': round_info.get('difficulty', 'mixed'),
            'category': round_info.get('category', 'all'),
            'guesses': [],
            'hints_requested': 0,
            'round_score': 0,
            'completed': False
        }
        
        self.session_data['rounds'].append(round_data)
        self.session_data['session_info']['total_rounds'] += 1
        
        # Auto-save
        self._auto_save_session()
    
    def log_comprehensive_guess(self, guess_result: Dict):
        """Log a comprehensive guess with detailed analysis for research."""
        timestamp = datetime.now().isoformat()
        guess_start_time = getattr(self, '_guess_start_time', time.time())
        response_time_ms = int((time.time() - guess_start_time) * 1000)
        
        # Get current context
        current_round = self.session_data['rounds'][-1] if self.session_data['rounds'] else {}
        current_game = self.session_data['games'][-1] if self.session_data['games'] else {}
        
        # Comprehensive guess data
        comprehensive_guess = {
            'timestamp': timestamp,
            'session_id': self.session_id,
            'game_id': current_game.get('game_id', 'unknown'),
            'round_id': current_round.get('round_id', 'unknown'),
            'guess_number': len(current_round.get('guesses', [])) + 1,
            'target_word': current_round.get('target_word', ''),
            'target_token_id': current_round.get('target_token_id', 0),
            'guess_word': guess_result.get('guess_word', ''),
            'guess_token_id': guess_result.get('guess_token_id', 0),
            'token_distance': guess_result.get('distance', 0),
            'points_earned': guess_result.get('round_score', 0),
            'total_score': guess_result.get('total_score', 0),
            'response_time_ms': response_time_ms,
            'hint_used': getattr(self, '_hint_used_this_guess', False),
            'game_mode': current_round.get('game_mode', 'normal'),
            'difficulty': current_round.get('difficulty', 'mixed'),
            'category': current_round.get('category', 'all'),
            'educational_context': guess_result.get('feedback', {}).get('explanation', ''),
            'accuracy_level': self._categorize_accuracy(guess_result.get('distance', float('inf'))),
            'semantic_analysis': self._analyze_semantic_relationship(
                current_round.get('target_word', ''),
                guess_result.get('guess_word', ''),
                guess_result.get('distance', 0)
            )
        }
        
        # Add to session data
        self.session_data['guesses'].append(comprehensive_guess)
        if current_round:
            current_round['guesses'].append(comprehensive_guess)
        
        print(f"🔍 DEBUG: Guess logged - Target: {comprehensive_guess['target_word']}, Guess: {comprehensive_guess['guess_word']}")
        print(f"🔍 DEBUG: Saving to: {self.research_data_dir}")
        
        self.session_data['session_info']['total_guesses'] += 1
        
        # Log to CSV immediately for research analysis
        self._append_to_csv_immediately(comprehensive_guess)
        
        # Log token relationship for research
        self._log_token_relationship(comprehensive_guess)
        
        # Reset guess tracking
        self._hint_used_this_guess = False
        
        # Auto-save
        self._auto_save_session()
    
    def log_hint_usage(self, hint_data: Dict):
        """Log hint usage for educational research."""
        hint_log = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'hint_type': hint_data.get('hint_type', 'general'),
            'target_word': hint_data.get('target_word', ''),
            'hint_content': hint_data.get('context_hint', ''),
            'educational_value': hint_data.get('educational_content', ''),
            'semantic_hints_provided': len(hint_data.get('semantic_hints', [])),
            'token_hints_provided': len(hint_data.get('nearby_words', []))
        }
        
        self.session_data['hint_usage'].append(hint_log)
        self._hint_used_this_guess = True
        
        # Log performance metric
        self._log_performance_metric('hint_usage', 'hints_requested', 1, hint_log)
    
    def log_game_completion(self, final_results: Dict):
        """Log comprehensive game completion data."""
        if not self.session_data['games']:
            return
        
        current_game = self.session_data['games'][-1]
        current_game['end_time'] = datetime.now().isoformat()
        current_game['final_results'] = final_results
        current_game['total_score'] = final_results.get('final_score', 0)
        current_game['correct_guesses'] = final_results.get('correct_guesses', 0)
        current_game['total_rounds'] = final_results.get('total_rounds', 0)
        
        # Calculate advanced metrics
        game_guesses = [g for g in self.session_data['guesses'] if g['game_id'] == current_game['game_id']]
        if game_guesses:
            current_game['average_distance'] = sum(g['token_distance'] for g in game_guesses) / len(game_guesses)
            current_game['average_response_time'] = sum(g['response_time_ms'] for g in game_guesses) / len(game_guesses)
            current_game['accuracy_distribution'] = self._calculate_accuracy_distribution(game_guesses)
        
        # Log performance metrics
        self._log_performance_metric('game_completion', 'final_score', current_game['total_score'], current_game)
        self._log_performance_metric('game_completion', 'accuracy_rate', 
                                   (current_game['correct_guesses'] / max(current_game['total_rounds'], 1)) * 100, current_game)
        
        # Auto-save
        self._auto_save_session()
        
        print(f"🏁 Game completed: {current_game['game_id']}")
    
    def _append_to_csv_immediately(self, guess_data: Dict):
        """Immediately append guess data to CSV for real-time research analysis."""
        try:
            with open(self.files['guesses_detailed'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Calculate additional research metrics
                target_word = guess_data.get('target_word', '')
                guess_word = guess_data.get('guess_word', '')
                
                row = [
                    guess_data.get('timestamp', ''),
                    guess_data.get('session_id', ''),
                    guess_data.get('game_id', ''),
                    guess_data.get('round_id', ''),
                    guess_data.get('guess_number', 0),
                    target_word,
                    guess_data.get('target_token_id', 0),
                    guess_word,
                    guess_data.get('guess_token_id', 0),
                    guess_data.get('token_distance', 0),
                    guess_data.get('category', ''),
                    guess_data.get('points_earned', 0),
                    guess_data.get('total_score', 0),
                    guess_data.get('response_time_ms', 0),
                    guess_data.get('hint_used', False),
                    guess_data.get('game_mode', ''),
                    guess_data.get('difficulty', ''),
                    guess_data.get('category', ''),
                    len(target_word),
                    len(guess_word),
                    abs(ord(target_word[0].lower()) - ord(guess_word[0].lower())) if target_word and guess_word else 0,
                    guess_data.get('token_distance', 0) <= 50,  # is_correct threshold
                    guess_data.get('accuracy_level', ''),
                    guess_data.get('educational_context', '')
                ]
                
                writer.writerow(row)
        except Exception as e:
            print(f"❌ Error writing to CSV: {e}")
    
    def _log_token_relationship(self, guess_data: Dict):
        """Log token relationship data for semantic similarity research."""
        try:
            target_word = guess_data.get('target_word', '')
            guess_word = guess_data.get('guess_word', '')
            
            if not target_word or not guess_word:
                return
            
            with open(self.files['token_relationships'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Analyze semantic relationship
                semantic_analysis = guess_data.get('semantic_analysis', {})
                
                row = [
                    guess_data.get('timestamp', ''),
                    f"{target_word}_{guess_word}_{int(time.time())}",
                    target_word,
                    guess_data.get('target_token_id', 0),
                    guess_word,
                    guess_data.get('guess_token_id', 0),
                    guess_data.get('token_distance', 0),
                    semantic_analysis.get('relationship_type', 'unknown'),
                    guess_data.get('game_mode', ''),
                    semantic_analysis.get('perceived_similarity', 'medium'),
                    semantic_analysis.get('similarity_score', 0.5),
                    guess_data.get('category', ''),
                    semantic_analysis.get('guess_category', ''),
                    semantic_analysis.get('frequency_difference', 0),
                    abs(len(target_word) - len(guess_word)),
                    semantic_analysis.get('alphabetical_closeness', 0)
                ]
                
                writer.writerow(row)
        except Exception as e:
            print(f"❌ Error logging token relationship: {e}")
    
    def _log_performance_metric(self, metric_type: str, metric_name: str, value: Any, context: Dict):
        """Log performance metrics for research analysis."""
        try:
            with open(self.files['performance_metrics'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                row = [
                    datetime.now().isoformat(),
                    self.session_id,
                    metric_type,
                    metric_name,
                    value,
                    json.dumps(context, default=str),
                    context.get('game_mode', ''),
                    context.get('round_number', 0),
                    context.get('total_score', 0),
                    context.get('accuracy_percentage', 0),
                    context.get('average_distance', 0),
                    context.get('improvement_rate', 0)
                ]
                
                writer.writerow(row)
        except Exception as e:
            print(f"❌ Error logging performance metric: {e}")
    
    def _analyze_semantic_relationship(self, target_word: str, guess_word: str, distance: int) -> Dict:
        """Analyze semantic relationship between target and guess for research."""
        analysis = {
            'relationship_type': 'unknown',
            'perceived_similarity': 'medium',
            'similarity_score': 0.5,
            'frequency_difference': 0,
            'alphabetical_closeness': 0,
            'guess_category': 'unknown'
        }
        
        if not target_word or not guess_word:
            return analysis
        
        # Basic analysis
        if distance <= 10:
            analysis['relationship_type'] = 'very_similar'
            analysis['perceived_similarity'] = 'high'
            analysis['similarity_score'] = 0.9
        elif distance <= 50:
            analysis['relationship_type'] = 'similar'
            analysis['perceived_similarity'] = 'medium_high'
            analysis['similarity_score'] = 0.7
        elif distance <= 200:
            analysis['relationship_type'] = 'somewhat_similar'
            analysis['perceived_similarity'] = 'medium'
            analysis['similarity_score'] = 0.5
        else:
            analysis['relationship_type'] = 'different'
            analysis['perceived_similarity'] = 'low'
            analysis['similarity_score'] = 0.3
        
        # Alphabetical closeness
        if target_word and guess_word:
            analysis['alphabetical_closeness'] = abs(ord(target_word[0].lower()) - ord(guess_word[0].lower()))
        
        return analysis
    
    def _categorize_accuracy(self, distance: int) -> str:
        """Categorize accuracy for research analysis."""
        if distance <= 10:
            return 'excellent'
        elif distance <= 50:
            return 'good'
        elif distance <= 200:
            return 'fair'
        else:
            return 'poor'
    
    def _calculate_accuracy_distribution(self, guesses: List[Dict]) -> Dict:
        """Calculate accuracy distribution for research metrics."""
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        
        for guess in guesses:
            accuracy = guess.get('accuracy_level', 'poor')
            distribution[accuracy] = distribution.get(accuracy, 0) + 1
        
        return distribution
    
    def _auto_save_session(self):
        """Automatically save session data."""
        try:
            # Update session info
            self.session_data['session_info']['end_time'] = datetime.now().isoformat()
            
            # Save comprehensive session data
            with open(self.files['session_summary'], 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, default=str)
            
            # Save to daily comprehensive file
            daily_data = self._load_daily_data()
            daily_data[self.session_id] = self.session_data
            
            with open(self.files['daily_comprehensive'], 'w', encoding='utf-8') as f:
                json.dump(daily_data, f, indent=2, default=str)
            
            # Save session data
            with open(self.files['session'], 'w') as f:
                json.dump(self.session_data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error auto-saving session: {e}")
    
    def _load_daily_data(self) -> Dict:
        """Load existing daily data."""
        try:
            if os.path.exists(self.files['daily_comprehensive']):
                with open(self.files['daily_comprehensive'], 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading daily data: {e}")
        
        return {}
    
    def export_comprehensive_data(self, options: Dict = None) -> List[str]:
        """Export comprehensive research data in multiple formats."""
        if options is None:
            options = {'csv_format': True, 'json_format': True, 'excel_format': True}
        
        exported_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Export as Excel for easy analysis
            if options.get('excel_format', True):
                excel_file = os.path.join(self.research_data_dir, f"comprehensive_research_export_{timestamp}.xlsx")
                self._export_to_excel(excel_file)
                exported_files.append(excel_file)
            
            # Export JSON summary
            if options.get('json_format', True):
                json_file = os.path.join(self.research_data_dir, f"research_summary_{timestamp}.json")
                research_summary = self._generate_research_summary()
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(research_summary, f, indent=2, default=str)
                exported_files.append(json_file)
            
            # Export consolidated CSV
            if options.get('csv_format', True):
                csv_file = os.path.join(self.research_data_dir, f"consolidated_analysis_{timestamp}.csv")
                self._export_consolidated_csv(csv_file)
                exported_files.append(csv_file)
            
            print(f"📊 Comprehensive data exported: {len(exported_files)} files")
            return exported_files
            
        except Exception as e:
            print(f"❌ Error exporting comprehensive data: {e}")
            return []
    
    def _export_to_excel(self, filename: str):
        """Export data to Excel format for researchers (simplified without pandas)."""
        try:
            # For now, we'll create additional CSV files instead of Excel
            # This avoids the pandas dependency
            base_name = filename.replace('.xlsx', '')
            
            # Export guesses as separate CSV
            if os.path.exists(self.files['guesses_detailed']):
                import shutil
                shutil.copy2(self.files['guesses_detailed'], f"{base_name}_guesses.csv")
            
            print(f"✅ Data exported as CSV files (Excel export requires pandas installation)")
                
        except Exception as e:
            print(f"❌ Error creating export: {e}")
    
    def _generate_research_summary(self) -> Dict:
        """Generate comprehensive research summary."""
        summary = {
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'session_id': self.session_id,
                'data_collection_version': '2.0',
                'research_focus': 'token_space_semantic_similarity'
            },
            'session_overview': self.session_data['session_info'],
            'games_summary': {
                'total_games': len(self.session_data['games']),
                'total_rounds': len(self.session_data['rounds']),
                'total_guesses': len(self.session_data['guesses']),
                'total_hints': len(self.session_data['hint_usage'])
            },
            'research_insights': self._calculate_research_insights(),
            'token_analysis': self._analyze_token_patterns(),
            'semantic_patterns': self._analyze_semantic_patterns(),
            'raw_data_files': list(self.files.keys())
        }
        
        return summary
    
    def _calculate_research_insights(self) -> Dict:
        """Calculate research insights from collected data."""
        insights = {
            'average_token_distance': 0,
            'distance_distribution': {},
            'semantic_accuracy_correlation': 0,
            'response_time_patterns': {},
            'hint_effectiveness': {},
            'mode_performance_comparison': {}
        }
        
        if self.session_data['guesses']:
            distances = [g['token_distance'] for g in self.session_data['guesses']]
            insights['average_token_distance'] = sum(distances) / len(distances)
            
            # Distance distribution
            for distance in distances:
                if distance <= 10:
                    category = 'very_close'
                elif distance <= 50:
                    category = 'close'
                elif distance <= 200:
                    category = 'moderate'
                else:
                    category = 'far'
                
                insights['distance_distribution'][category] = insights['distance_distribution'].get(category, 0) + 1
        
        return insights
    
    def _analyze_token_patterns(self) -> Dict:
        """Analyze token ID patterns for research."""
        return {
            'token_clustering_analysis': 'To be implemented with more data',
            'frequency_correlation': 'Requires external frequency data',
            'positional_analysis': 'Based on token ID ranges'
        }
    
    def _analyze_semantic_patterns(self) -> Dict:
        """Analyze semantic similarity patterns."""
        return {
            'category_clustering': 'Analyze within-category vs cross-category guesses',
            'synonym_detection': 'Track synonym pairs in token space',
            'antonym_patterns': 'Analyze antonym token distances'
        }
    
    def _export_consolidated_csv(self, filename: str):
        """Export consolidated CSV for statistical analysis."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if not self.session_data['guesses']:
                    return
                
                # Write header
                writer = csv.writer(f)
                writer.writerow([
                    'session_id', 'timestamp', 'target_word', 'guess_word',
                    'token_distance', 'points_earned', 'accuracy_level',
                    'game_mode', 'category', 'hint_used'
                ])
                
                # Write data
                for guess in self.session_data['guesses']:
                    writer.writerow([
                        guess.get('session_id', ''),
                        guess.get('timestamp', ''),
                        guess.get('target_word', ''),
                        guess.get('guess_word', ''),
                        guess.get('token_distance', 0),
                        guess.get('points_earned', 0),
                        guess.get('accuracy_level', ''),
                        guess.get('game_mode', ''),
                        guess.get('category', ''),
                        guess.get('hint_used', False)
                    ])
                
        except Exception as e:
            print(f"❌ Error creating consolidated CSV: {e}")
    
    def save_session(self):
        """Save final session data."""
        self._auto_save_session()
        
        print(f"💾 Session data saved to: {self.research_data_dir}")
        print(f"📊 Total data points collected:")
        print(f"   • Games: {len(self.session_data['games'])}")
        print(f"   • Rounds: {len(self.session_data['rounds'])}")
        print(f"   • Guesses: {len(self.session_data['guesses'])}")
        print(f"   • Hints: {len(self.session_data['hint_usage'])}")
        
        return self.files['session'] 