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
#home page
@app.route('/')
def home():
    """Home page with game mode selection"""
    return render_template('home.html')

@app.route('/game')
def game():
    """Main game page"""
    game_session = get_or_create_game_session()
    return render_template('game.html')

@app.route('/setup/<mode>')
def game_setup(mode):
    """Game setup page for specific mode"""
    mode_info = {
        'synonym': {
            'name': 'Synonym Hunt',
            'icon': '🤝',
            'description': 'Find words with similar meanings and discover if they have close token IDs!'
        },
        'antonym': {
            'name': 'Antonym Challenge', 
            'icon': '⚡',
            'description': 'Find words with opposite meanings and see how far apart their tokens are!'
        },

        'speed': {
            'name': 'Speed Mode',
            'icon': '⚡',
            'description': 'Race against time to find similar words as quickly as possible!'
        }
    }
    
    if mode not in mode_info:
        return redirect(url_for('home'))
    
    return render_template('game_setup.html', 
                         mode=mode,
                         mode_name=mode_info[mode]['name'],
                         mode_icon=mode_info[mode]['icon'],
                         mode_description=mode_info[mode]['description'])

@app.route('/tutorial')
def tutorial():
    """Interactive tutorial with Tokky"""
    return render_template('tutorial.html')

@app.route('/settings')
def settings():
    """Appearance settings page"""
    return render_template('settings.html')

@app.route('/leaderboards')
def leaderboards():
    """Leaderboards page"""
    # Get a game session to access leaderboards (doesn't need to be user-specific)
    game_session = get_or_create_game_session()
    leaderboard = game_session['leaderboard']
    
    # Get leaderboard data for all game modes
    leaderboard_data = {}
    for mode in ['normal', 'synonym', 'antonym', 'speed']:
        leaderboard_data[mode] = leaderboard.get_top_scores(mode, 10)
    
    # Get overall statistics
    stats = leaderboard.get_statistics()
    
    return render_template('leaderboards.html', 
                         leaderboard_data=leaderboard_data,
                         stats=stats)

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Start a new game round"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    data_collector = game_session['data_collector']
    
    # Apply any settings from the request
    settings = request.json or {}
    if settings:
        game_session['settings'].update(settings)
        # Update game logic with new settings
        final_game_mode = settings.get('game_mode', 'normal')
        # If speed mode is enabled, use speed as the game mode
        if settings.get('is_speed_mode', False):
            final_game_mode = 'speed'
        
        game_logic.change_game_settings(
            game_mode=final_game_mode,
            difficulty=settings.get('difficulty', 'mixed'),
            category=settings.get('category', 'all')
        )
        
        # Set time limit for speed mode
        if settings.get('is_speed_mode', False) and settings.get('time_limit'):
            game_logic.time_limit = settings.get('time_limit', 30)
    
    try:
        # Start new round using existing logic
        round_info = game_logic.start_new_round()
        
        # Check if there was an error starting the round
        if 'error' in round_info:
            return jsonify({
                'success': False,
                'error': round_info['error']
            })
        
        # Log the round start
        if round_info.get('current_round') == 1:
            # Log game start on first round
            game_config = {
                'game_mode': final_game_mode,
                'difficulty': settings.get('difficulty', 'mixed'),
                'category': settings.get('category', 'all'),
                'max_rounds': round_info.get('max_rounds', 10)
            }
            data_collector.log_game_start(game_config)
        
        # Log round start
        data_collector.log_round_start(round_info)
        
        return jsonify({
            'success': True,
            'round_info': round_info,
            'settings': game_session['settings']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to start game: {str(e)}'
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
        # Create comprehensive guess data for the enhanced data collector
        guess_data = {
            'target_word': game_logic.current_target_word,
            'target_token_id': game_logic.current_target_token_id,
            'guess_word': guess_word,
            'guess_token_id': result.get('guess_token_id'),
            'distance': result.get('distance'),
            'points': result.get('points'),
            'round_number': game_logic.round_number,
            'attempts_used': game_logic.current_attempts,
            'feedback': result.get('feedback', ''),
            'correct': result.get('correct', False)
        }
        data_collector.log_comprehensive_guess(guess_data)
    
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

@app.route('/api/submit_score', methods=['POST'])
def submit_score():
    """Submit score to leaderboard"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    leaderboard = game_session['leaderboard']
    
    data = request.json
    player_name = data.get('player_name', '').strip()
    
    if not player_name:
        return jsonify({'success': False, 'error': 'Player name is required'})
    
    if len(player_name) > 20:
        return jsonify({'success': False, 'error': 'Player name must be 20 characters or less'})
    
    # Check if game is completed
    if not game_logic.game_completed:
        return jsonify({'success': False, 'error': 'Game not completed yet'})
    
    # Get final results from game logic
    final_results = game_logic.get_final_results()
    
    # Add player name to results
    final_results['player_name'] = player_name
    
    # Submit to leaderboard
    try:
        rank = leaderboard.add_score(player_name, final_results)
        
        return jsonify({
            'success': True,
            'rank': rank,
            'score': final_results['total_score'],
            'is_high_score': leaderboard.is_high_score(
                final_results['total_score'], 
                final_results.get('game_mode', 'normal')
            )
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_final_results', methods=['GET'])
def get_final_results():
    """Get final game results for score submission"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    
    if not game_logic.game_completed:
        return jsonify({'success': False, 'error': 'Game not completed'})
    
    final_results = game_logic.get_final_results()
    return jsonify({
        'success': True,
        'results': final_results
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
    app.run(debug=True, host='0.0.0.0', port=5000) 