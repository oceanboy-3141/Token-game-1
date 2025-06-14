from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
import uuid

# Import your existing modules (no changes needed!)
from game_logic import GameLogic
from enhanced_data_collector import EnhancedDataCollector
from achievements import AchievementManager
from leaderboard import Leaderboard

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Global storage for active games (in production, use Redis or database)
active_games = {}

def get_or_create_game_session():
    """Get existing game session or create new one"""
    if 'game_id' not in session:
        session['game_id'] = str(uuid.uuid4())
    
    game_id = session['game_id']
    
    if game_id not in active_games:
        # Create new game using your existing logic
        active_games[game_id] = {
            'game_logic': GameLogic(),
            'data_collector': EnhancedDataCollector('game_data'),
            'achievement_manager': AchievementManager(),
            'leaderboard': Leaderboard(),
            'settings': {
                'game_mode': 'normal',
                'difficulty': 'mixed',
                'category': 'all',
                'rounds': 10
            }
        }
    
    return active_games[game_id]

@app.route('/')
def index():
    """Main game page"""
    game_session = get_or_create_game_session()
    return render_template('game.html')

@app.route('/settings')
def settings():
    """Game settings page"""
    return render_template('settings.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Start a new game round"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    
    # Apply any settings from the request
    settings = request.json or {}
    if settings:
        game_session['settings'].update(settings)
        # Update game logic with new settings
        game_logic.change_game_settings(
            game_mode=settings.get('game_mode', 'normal'),
            difficulty=settings.get('difficulty', 'mixed'),
            category=settings.get('category', 'all')
        )
    
    # Start new round using existing logic
    round_info = game_logic.start_new_round()
    
    return jsonify({
        'success': True,
        'round_info': round_info,
        'settings': game_session['settings']
    })

@app.route('/api/submit_guess', methods=['POST'])
def submit_guess():
    """Submit a guess"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    data_collector = game_session['data_collector']
    
    guess_word = request.json.get('guess', '').strip()
    
    if not guess_word:
        return jsonify({'success': False, 'error': 'No guess provided'})
    
    # Use existing game logic
    result = game_logic.submit_guess(guess_word)
    
    # Log data using existing system
    if result.get('valid_guess'):
        data_collector.log_guess(
            target_word=game_logic.current_target_word,
            target_token_id=game_logic.current_target_token_id,
            guess_word=guess_word,
            guess_token_id=result.get('guess_token_id'),
            distance=result.get('distance'),
            points=result.get('points'),
            round_number=game_logic.round_number
        )
    
    return jsonify({
        'success': True,
        'result': result
    })

@app.route('/api/get_hint', methods=['GET'])
def get_hint():
    """Get hint for current round"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    
    hint_info = game_logic.get_hint()
    return jsonify(hint_info)

@app.route('/api/game_status', methods=['GET'])
def game_status():
    """Get current game status"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    
    return jsonify({
        'current_round': game_logic.round_number,
        'max_rounds': game_logic.max_rounds,
        'score': game_logic.score,
        'correct_guesses': game_logic.correct_guesses,
        'current_target_word': game_logic.current_target_word,
        'current_target_token_id': game_logic.current_target_token_id,
        'attempts_left': game_logic.max_attempts - game_logic.current_attempts,
        'game_completed': game_logic.game_completed,
        'settings': game_session['settings']
    })

@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Get player achievements"""
    game_session = get_or_create_game_session()
    achievement_manager = game_session['achievement_manager']
    
    return jsonify({
        'achievements': achievement_manager.get_all_achievements(),
        'unlocked': achievement_manager.get_unlocked_achievements()
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard data"""
    game_session = get_or_create_game_session()
    leaderboard = game_session['leaderboard']
    
    return jsonify({
        'leaderboard': leaderboard.get_top_scores(10)
    })

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start completely new game"""
    game_id = session.get('game_id')
    if game_id and game_id in active_games:
        del active_games[game_id]
    
    # Create new session
    session['game_id'] = str(uuid.uuid4())
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 