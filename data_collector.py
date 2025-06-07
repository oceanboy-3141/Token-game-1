"""
Data Collector Module
Handles data logging and export for research analysis
"""
import json
import csv
import os
from datetime import datetime
from typing import List, Dict


class DataCollector:
    def __init__(self, data_dir: str = "game_data"):
        self.data_dir = data_dir
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_data = []
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def log_guess(self, guess_data: Dict):
        """Log a single guess with timestamp."""
        log_entry = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            **guess_data
        }
        
        self.session_data.append(log_entry)
        
        # Also append to daily log file
        daily_file = os.path.join(
            self.data_dir, 
            f"daily_log_{datetime.now().strftime('%Y%m%d')}.json"
        )
        
        # Read existing data
        existing_data = []
        if os.path.exists(daily_file):
            try:
                with open(daily_file, 'r') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []
        
        # Append new entry
        existing_data.append(log_entry)
        
        # Write back
        with open(daily_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
    
    def save_session(self):
        """Save current session data to a dedicated file."""
        session_file = os.path.join(
            self.data_dir, 
            f"session_{self.session_id}.json"
        )
        
        session_summary = {
            'session_id': self.session_id,
            'start_time': self.session_data[0]['timestamp'] if self.session_data else None,
            'end_time': datetime.now().isoformat(),
            'total_guesses': len(self.session_data),
            'guesses': self.session_data
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_summary, f, indent=2)
        
        return session_file
    
    def export_to_csv(self, filename: str = None):
        """Export session data to CSV for analysis."""
        if not filename:
            filename = f"token_game_data_{self.session_id}.csv"
        
        csv_file = os.path.join(self.data_dir, filename)
        
        if not self.session_data:
            return None
        
        # Define CSV headers
        headers = [
            'session_id', 'timestamp', 'round', 'target_word', 'target_token_id',
            'guess_word', 'guess_token_id', 'distance', 'round_score', 'total_score'
        ]
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for entry in self.session_data:
                # Flatten the data for CSV
                csv_row = {
                    'session_id': entry['session_id'],
                    'timestamp': entry['timestamp'],
                    'round': entry['round'],
                    'target_word': entry['target_word'],
                    'target_token_id': entry['target_token_id'],
                    'guess_word': entry['guess_word'],
                    'guess_token_id': entry['guess_token_id'],
                    'distance': entry['distance'],
                    'round_score': entry['round_score'],
                    'total_score': entry['total_score']
                }
                writer.writerow(csv_row)
        
        return csv_file
    
    def get_research_summary(self) -> Dict:
        """Generate a summary for research analysis."""
        if not self.session_data:
            return {'error': 'No data collected'}
        
        # Calculate research metrics
        distances = [entry['distance'] for entry in self.session_data]
        
        # Analyze synonym patterns
        word_pairs = []
        for entry in self.session_data:
            word_pairs.append({
                'target': entry['target_word'],
                'guess': entry['guess_word'],
                'distance': entry['distance'],
                'semantic_closeness': self._estimate_semantic_closeness(entry['distance'])
            })
        
        return {
            'session_summary': {
                'total_guesses': len(self.session_data),
                'unique_targets': len(set(entry['target_word'] for entry in self.session_data)),
                'average_distance': sum(distances) / len(distances),
                'min_distance': min(distances),
                'max_distance': max(distances),
                'median_distance': sorted(distances)[len(distances)//2]
            },
            'word_pairs': word_pairs,
            'distance_distribution': self._get_distance_distribution(distances)
        }
    
    def _estimate_semantic_closeness(self, distance: int) -> str:
        """Estimate semantic closeness based on token distance."""
        if distance <= 10:
            return "very_close"
        elif distance <= 50:
            return "close"
        elif distance <= 100:
            return "moderate"
        elif distance <= 500:
            return "distant"
        else:
            return "very_distant"
    
    def _get_distance_distribution(self, distances: List[int]) -> Dict:
        """Get distribution of distances for analysis."""
        distribution = {
            'very_close': 0,    # 0-10
            'close': 0,         # 11-50
            'moderate': 0,      # 51-100
            'distant': 0,       # 101-500
            'very_distant': 0   # 500+
        }
        
        for distance in distances:
            if distance <= 10:
                distribution['very_close'] += 1
            elif distance <= 50:
                distribution['close'] += 1
            elif distance <= 100:
                distribution['moderate'] += 1
            elif distance <= 500:
                distribution['distant'] += 1
            else:
                distribution['very_distant'] += 1
        
        return distribution 