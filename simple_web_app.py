"""
Simple Token Quest Web Application
Minimal Flask interface without heavy dependencies
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Import our game modules
from game_logic import TokenGame
from token_handler import TokenHandler

app = Flask(__name__)
app.secret_key = 'token-quest-secret-change-in-production'

# Initialize game components
token_handler = TokenHandler()

# Simple database functions
def init_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect('token_quest.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_games INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            best_score INTEGER DEFAULT 0
        )
    ''')
    
    # Game sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER DEFAULT 0,
            difficulty TEXT,
            game_mode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_by_username(username):
    """Get user by username."""
    conn = sqlite3.connect('token_quest.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    """Create a new user."""
    conn = sqlite3.connect('token_quest.db')
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def check_user_password(user, password):
    """Check if password is correct."""
    return check_password_hash(user[3], password)  # password_hash is at index 3

def update_user_stats(user_id, score):
    """Update user statistics."""
    conn = sqlite3.connect('token_quest.db')
    cursor = conn.cursor()
    
    # Get current stats
    cursor.execute('SELECT total_games, total_score, best_score FROM users WHERE id = ?', (user_id,))
    stats = cursor.fetchone()
    
    if stats:
        total_games = stats[0] + 1
        total_score = stats[1] + score
        best_score = max(stats[2], score)
        
        cursor.execute(
            'UPDATE users SET total_games = ?, total_score = ?, best_score = ? WHERE id = ?',
            (total_games, total_score, best_score, user_id)
        )
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    """Main page."""
    if 'user_id' in session:
        return render_template('simple_game.html')
    return render_template('simple_index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        if user and check_user_password(user, password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('simple_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if create_user(username, email, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists', 'error')
    
    return render_template('simple_register.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# API Routes
@app.route('/api/start_game', methods=['POST'])
def api_start_game():
    """Start a new game session."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'medium')
        game_mode = data.get('game_mode', 'classic')
        
        # Initialize game
        game = TokenGame(difficulty=difficulty, game_mode=game_mode)
        target_word, target_token_id = game.get_current_target()
        
        # Store game state in session
        session['game_state'] = {
            'target_word': target_word,
            'target_token_id': target_token_id,
            'attempts': 0,
            'score': 0,
            'difficulty': difficulty,
            'game_mode': game_mode
        }
        
        return jsonify({
            'success': True,
            'target_word': target_word,
            'target_token_id': target_token_id,
            'difficulty': difficulty,
            'game_mode': game_mode
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/make_guess', methods=['POST'])
def api_make_guess():
    """Process a guess."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        guess_word = data.get('word', '').strip().lower()
        
        if not guess_word:
            return jsonify({'success': False, 'error': 'No word provided'}), 400
        
        # Get game state
        game_state = session.get('game_state')
        if not game_state:
            return jsonify({'success': False, 'error': 'No active game'}), 400
        
        # Process guess
        guess_token_id = token_handler.get_token_id(guess_word)
        if guess_token_id is None:
            return jsonify({
                'success': False,
                'error': 'Word not found in token vocabulary or is multi-token'
            }), 400
        
        target_token_id = game_state['target_token_id']
        distance = abs(guess_token_id - target_token_id)
        
        # Calculate score
        max_score = 100
        score = max(0, max_score - int(distance * 0.5))
        
        # Update game state
        game_state['attempts'] += 1
        game_state['score'] += score
        session['game_state'] = game_state
        
        # Check if correct
        is_correct = distance == 0
        
        return jsonify({
            'success': True,
            'guess_word': guess_word,
            'guess_token_id': guess_token_id,
            'target_token_id': target_token_id,
            'distance': distance,
            'score': score,
            'total_score': game_state['score'],
            'attempts': game_state['attempts'],
            'is_correct': is_correct
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_hints', methods=['POST'])
def api_get_hints():
    """Get hints for the current target word."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        game_state = session.get('game_state')
        if not game_state:
            return jsonify({'success': False, 'error': 'No active game'}), 400
        
        # Simple hints for now
        hints = [
            "Try words with similar meanings",
            "Consider the semantic category",
            "Think about word frequency",
            "Look for related concepts"
        ]
        
        return jsonify({
            'success': True,
            'hints': hints,
            'target_token_id': game_state['target_token_id']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/end_game', methods=['POST'])
def api_end_game():
    """End the current game session."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    try:
        game_state = session.get('game_state')
        
        if game_state:
            # Update user statistics
            update_user_stats(session['user_id'], game_state['score'])
            
            # Save game session to database
            conn = sqlite3.connect('token_quest.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO game_sessions (user_id, score, difficulty, game_mode, completed_at) VALUES (?, ?, ?, ?, ?)',
                (session['user_id'], game_state['score'], game_state['difficulty'], game_state['game_mode'], datetime.now())
            )
            conn.commit()
            conn.close()
        
        # Clear session
        session.pop('game_state', None)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000) 