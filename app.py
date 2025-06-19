import json
import logging
import os
import re
import secrets
import time
import uuid
from datetime import datetime

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Import your existing modules (no changes needed!)
from game_logic import GameLogic
from enhanced_data_collector import EnhancedDataCollector
from achievements import AchievementManager
from leaderboard import Leaderboard
from token_handler import TokenHandler
from config import SecurityConfig, CloudRunConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# SECURITY FIX: Use environment variable or generate secure random key
app.secret_key = SecurityConfig.SECRET_KEY if SecurityConfig.SECRET_KEY != 'dev-key-change-in-production' else secrets.token_hex(32)

# Global storage for active games (in production, use Redis or database)
active_games = {}

# MEMORY LEAK FIX: Track session creation time for cleanup
session_timestamps = {}

def cleanup_old_sessions():
    """Clean up old sessions to prevent memory leaks"""
    current_time = time.time()
    sessions_to_remove = []
    
    # Remove sessions older than 24 hours (86400 seconds)
    for session_id, timestamp in session_timestamps.items():
        if current_time - timestamp > 86400:  # 24 hours
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        if session_id in active_games:
            del active_games[session_id]
        if session_id in session_timestamps:
            del session_timestamps[session_id]
    
    logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")

def get_or_create_game_session():
    """Get existing game session or create new one"""
    if 'game_id' not in session:
        session['game_id'] = str(uuid.uuid4())
    
    game_id = session['game_id']
    
    # Clean up old sessions periodically (every 100 requests)
    if len(active_games) % 100 == 0:
        cleanup_old_sessions()
    
    if game_id not in active_games:
        # Create new game using your existing logic
        # Default settings - can be overridden by start_game
        default_settings = {
            'game_mode': 'normal',
            'difficulty': 'mixed',
            'category': 'all',
            'rounds': 10
        }
        
        active_games[game_id] = {
            'game_logic': GameLogic(max_rounds=default_settings['rounds']),
            'data_collector': EnhancedDataCollector('game_data'),
            'achievement_manager': AchievementManager(),
            'leaderboard': Leaderboard(),
            'settings': default_settings
        }
        
        # Track session creation time
        session_timestamps[game_id] = time.time()
    
    return active_games[game_id]

# INPUT VALIDATION FUNCTIONS
def validate_guess_input(guess):
    """Validate user guess input"""
    if not isinstance(guess, str):
        return False, "Guess must be a string"
    
    guess = guess.strip()
    
    if not guess:
        return False, "Guess cannot be empty"
    
    if len(guess) > 50:
        return False, "Guess too long (max 50 characters)"
    
    if len(guess) < 1:
        return False, "Guess too short (min 1 character)"
    
    # Allow only letters, numbers, and basic punctuation
    if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', guess):
        return False, "Guess contains invalid characters"
    
    return True, "Valid"

def validate_player_name(name):
    """Validate player name for leaderboard"""
    if not isinstance(name, str):
        return False, "Name must be a string"
    
    name = name.strip()
    
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) > 20:
        return False, "Name too long (max 20 characters)"
    
    if len(name) < 1:
        return False, "Name too short (min 1 character)"
    
    # Allow letters, numbers, spaces, and basic punctuation
    if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', name):
        return False, "Name contains invalid characters"
    
    return True, "Valid"

def validate_game_settings(data):
    """Validate game configuration settings"""
    errors = []
    
    # Validate game mode
    valid_modes = ['normal', 'synonym', 'antonym', 'speed']
    game_mode = data.get('game_mode', 'normal')
    if game_mode not in valid_modes:
        errors.append(f"Invalid game mode. Must be one of: {valid_modes}")
    
    # Validate difficulty
    valid_difficulties = ['easy', 'medium', 'hard', 'mixed']
    difficulty = data.get('difficulty', 'mixed')
    if difficulty not in valid_difficulties:
        errors.append(f"Invalid difficulty. Must be one of: {valid_difficulties}")
    
    # Validate category
    valid_categories = ['all', 'emotions', 'size', 'speed', 'quality', 'temperature', 'brightness', 'actions', 'difficulty']
    category = data.get('category', 'all')
    if category not in valid_categories:
        errors.append(f"Invalid category. Must be one of: {valid_categories}")
    
    # Validate rounds
    rounds = data.get('rounds', 10)
    try:
        rounds = int(rounds)
        if rounds < 1 or rounds > 50:
            errors.append("Rounds must be between 1 and 50")
    except (ValueError, TypeError):
        errors.append("Rounds must be a valid integer")
    
    return len(errors) == 0, errors

def sanitize_file_path(path):
    """Sanitize file paths to prevent directory traversal"""
    # Remove any path traversal attempts
    path = path.replace('..', '').replace('/', '').replace('\\', '')
    # Ensure it's a safe filename
    path = re.sub(r'[<>:"|?*]', '', path)
    return path

# Health check endpoint for Cloud Run
@app.route('/health')
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

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
    """Interactive tutorial with Tokky using real tiktoken data"""
    # Create token handler instance
    token_handler = TokenHandler()
    
    # Get real token IDs for tutorial examples
    tutorial_examples = {
        'happy': token_handler.get_single_token_id('happy'),
        'bright': token_handler.get_single_token_id('bright'),
        'joyful': token_handler.get_single_token_id('joyful'),
    }
    
    # Calculate real distance between happy and joyful if both are single tokens
    happy_joyful_distance = None
    if tutorial_examples['happy'] and tutorial_examples['joyful']:
        happy_joyful_distance = abs(tutorial_examples['happy'] - tutorial_examples['joyful'])
    
    return render_template('tutorial.html', 
                         tutorial_examples=tutorial_examples,
                         happy_joyful_distance=happy_joyful_distance)

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

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Start a new game"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    data_collector = game_session['data_collector']
    achievement_manager = game_session['achievement_manager']
    
    data = request.json or {}
    
    # INPUT VALIDATION: Validate game settings
    is_valid, validation_errors = validate_game_settings(data)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': 'Invalid game settings',
            'details': validation_errors
        })
    
    game_mode = data.get('game_mode', 'normal')
    difficulty = data.get('difficulty', 'mixed')
    category = data.get('category', 'all')
    rounds = data.get('rounds', 10)
    
    # Update game settings including max_rounds
    game_logic.change_game_settings(game_mode, difficulty, category)
    game_logic.max_rounds = rounds  # Update max_rounds
    
    # Update session settings
    game_session['settings'] = {
        'game_mode': game_mode,
        'difficulty': difficulty,
        'category': category,
        'rounds': rounds
    }
    
    try:
        # Start new round
        round_info = game_logic.start_new_round()
        
        # Check if there was an error starting the round
        if 'error' in round_info:
            return jsonify({
                'success': False,
                'error': round_info['error']
            })
        
        # Track achievement events
        newly_unlocked = []
        newly_unlocked.extend(achievement_manager.track_game_event("game_started"))
        if category != 'all':
            newly_unlocked.extend(achievement_manager.track_game_event("category_played", category=category))
        
        # Log game start in data collector
        game_config = {
            'game_mode': game_mode,
            'difficulty': difficulty,
            'category': category,
            'max_rounds': rounds
        }
        data_collector.log_game_start(game_config)
        
        # Prepare response
        response = {
            'success': True,
            'round_info': round_info,
            'settings': game_session['settings'],
            'newly_unlocked_achievements': [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'icon': ach.icon,
                    'category': ach.category
                }
                for ach in newly_unlocked
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to start game: {str(e)}'
        })

@app.route('/api/submit_guess', methods=['POST'])
def submit_guess():
    """Submit a guess and get results"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    data_collector = game_session['data_collector']
    achievement_manager = game_session['achievement_manager']
    
    # INPUT VALIDATION: Check if request has JSON data
    if not request.json:
        return jsonify({
            'success': False,
            'error': 'Invalid request format',
            'result': {}
        })
    
    guess_word = request.json.get('guess', '')
    
    # INPUT VALIDATION: Validate guess input
    is_valid, validation_message = validate_guess_input(guess_word)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': validation_message,
            'result': {}
        })
    
    guess_word = guess_word.strip().lower()
    
    # Submit guess to game logic
    result = game_logic.submit_guess(guess_word)
    
    # Track achievement events
    newly_unlocked = []
    
    if result.get('valid_guess'):
        # Track word tried
        newly_unlocked.extend(achievement_manager.track_game_event("word_tried", word=guess_word))
        
        # Track guess quality
        feedback = result.get('feedback', '')
        distance = result.get('distance', float('inf'))
        first_guess = game_logic.current_attempts == 1
        
        if feedback == 'Perfect!' or distance <= 1:
            newly_unlocked.extend(achievement_manager.track_game_event("perfect_guess", first_guess_of_round=first_guess))
        elif feedback == 'Excellent!' or distance <= 10:
            newly_unlocked.extend(achievement_manager.track_game_event("excellent_guess"))
        else:
            newly_unlocked.extend(achievement_manager.track_game_event("incorrect_guess"))
        
        # Check for game completion
        if result.get('game_ended'):
            game_stats = game_logic.get_final_results()
            score = game_stats.get('total_score', 0)
            mode = game_logic.game_mode
            
            newly_unlocked.extend(achievement_manager.track_game_event(
                "game_won", 
                mode=mode, 
                score=score,
                comeback=False  # TODO: Add comeback detection logic
            ))
    
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
        'result': result,
        'newly_unlocked_achievements': [
            {
                'id': ach.id,
                'name': ach.name,
                'description': ach.description,
                'icon': ach.icon,
                'category': ach.category
            }
            for ach in newly_unlocked
        ]
    })

@app.route('/api/get_hint', methods=['GET'])
def get_hint():
    """Get hint for current round"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    achievement_manager = game_session['achievement_manager']
    
    hint_info = game_logic.get_hint()
    
    # Track hint viewed achievement
    newly_unlocked = achievement_manager.track_game_event("hint_viewed")
    
    hint_info['newly_unlocked_achievements'] = [
        {
            'id': ach.id,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'category': ach.category
        }
        for ach in newly_unlocked
    ]
    
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
        'total_score': game_logic.score,  # Add consistent total_score field
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
    
    # Get unlocked achievements as dictionaries
    unlocked_achievements = [
        {
            'id': ach.id,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'category': ach.category,
            'unlocked': ach.unlocked,
            'unlock_date': ach.unlock_date
        }
        for ach in achievement_manager.get_unlocked_achievements()
    ]
    
    return jsonify({
        'achievements': achievement_manager.get_all_achievements(),
        'unlocked': unlocked_achievements,
        'stats': achievement_manager.get_stats_summary()
    })

@app.route('/api/submit_score', methods=['POST'])
def submit_score():
    """Submit score to leaderboard"""
    game_session = get_or_create_game_session()
    game_logic = game_session['game_logic']
    leaderboard = game_session['leaderboard']
    achievement_manager = game_session['achievement_manager']
    
    # INPUT VALIDATION: Check if request has JSON data
    if not request.json:
        return jsonify({'success': False, 'error': 'Invalid request format'})
    
    data = request.json
    player_name = data.get('player_name', '')
    
    # INPUT VALIDATION: Validate player name
    is_valid, validation_message = validate_player_name(player_name)
    if not is_valid:
        return jsonify({'success': False, 'error': validation_message})
    
    player_name = player_name.strip()
    
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
        
        # Track leaderboard submission achievement
        newly_unlocked = achievement_manager.track_game_event("leaderboard_submission")
        
        return jsonify({
            'success': True,
            'rank': rank,
            'score': final_results['total_score'],
            'is_high_score': leaderboard.is_high_score(
                final_results['total_score'], 
                final_results.get('game_mode', 'normal')
            ),
            'newly_unlocked_achievements': [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'icon': ach.icon,
                    'category': ach.category
                }
                for ach in newly_unlocked
            ]
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

@app.route('/api/tutorial_guess', methods=['POST'])
def tutorial_guess():
    """Handle practice guesses in tutorial with real tiktoken"""
    data = request.json
    guess_word = data.get('guess', '').strip().lower()
    target_word = data.get('target', 'bright').lower()
    
    if not guess_word:
        return jsonify({'success': False, 'error': 'No guess provided'})
    
    # Create token handler
    token_handler = TokenHandler()
    
    # Get real token IDs
    target_token_id = token_handler.get_single_token_id(target_word)
    guess_token_id = token_handler.get_single_token_id(guess_word)
    
    if target_token_id is None:
        return jsonify({'success': False, 'error': f'Target word "{target_word}" is not a single token'})
    
    if guess_token_id is None:
        return jsonify({'success': False, 'error': f'Guess word "{guess_word}" is not a single token'})
    
    # Calculate real distance
    distance = abs(target_token_id - guess_token_id)
    
    # Calculate points based on distance (same scoring as main game)
    if distance == 0:
        points = 100
    elif distance <= 50:
        points = max(95 - (distance - 1) // 5, 80)
    elif distance <= 200:
        points = max(80 - (distance - 51) // 15, 60)
    elif distance <= 500:
        points = max(60 - (distance - 201) // 30, 40)
    elif distance <= 1000:
        points = max(40 - (distance - 501) // 50, 20)
    else:
        points = max(20 - (distance - 1001) // 200, 5)
    
    # Get educational explanation
    explanation = token_handler.get_educational_explanation(target_word, guess_word)
    
    return jsonify({
        'success': True,
        'target_word': target_word,
        'target_token_id': target_token_id,
        'guess_word': guess_word,
        'guess_token_id': guess_token_id,
        'distance': distance,
        'points': points,
        'explanation': explanation,
        'is_exact_match': distance == 0
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
    # For Cloud Run, we need to listen on the port provided by the PORT environment variable
    port = CloudRunConfig.PORT
    # Use debug=False for production
    debug = not CloudRunConfig.IS_PRODUCTION
    app.run(debug=debug, host='0.0.0.0', port=port) 