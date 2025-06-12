from __future__ import annotations

"""Token Quest – Flask Web Interface
A minimal Flask port that replaces the Tk GUI.
Keeps business logic in ``game_logic.py`` and exposes REST-like JSON endpoints
so a lightweight front-end (plain HTML+JS or React, etc.) can consume them.

The first version focuses on single-player; sessions are in-memory and keyed
by a browser cookie.  No persistent DB is required.
"""

import uuid
from datetime import datetime
from typing import Dict

from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from pathlib import Path

from game_logic import GameLogic, TokenGame
from token_handler import TokenHandler
from config import get_web_config, get_game_config
from async_data_collector import AsyncDataCollector
from token_cache import get_global_cache

app = Flask(__name__)
app.secret_key = "token-quest-secret-replace-me"  # TODO: read from env in prod

# Load configuration
web_config = get_web_config()
game_config = get_game_config()

app.config['SECRET_KEY'] = web_config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = web_config.database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[web_config.api_rate_limit]
)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Game statistics
    total_games = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=0)
    favorite_difficulty = db.Column(db.String(20), default='medium')
    
    # Relationships
    game_sessions = db.relationship('GameSession', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'total_games': self.total_games,
            'total_score': self.total_score,
            'best_score': self.best_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_data = db.Column(db.Text)  # JSON data
    score = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20))
    game_mode = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'score': self.score,
            'difficulty': self.difficulty,
            'game_mode': self.game_mode,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class GameSettingsForm(FlaskForm):
    difficulty = SelectField('Difficulty', choices=[
        ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')
    ])
    game_mode = SelectField('Game Mode', choices=[
        ('classic', 'Classic'), ('antonym', 'Antonym'), ('category', 'Category')
    ])
    submit = SubmitField('Save Settings')

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize game components
token_handler = TokenHandler()
data_collector = None
token_cache = get_global_cache()

# Routes
@app.route('/')
def index():
    """Main game interface."""
    if current_user.is_authenticated:
        return render_template('game.html', user=current_user.to_dict())
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    recent_sessions = GameSession.query.filter_by(user_id=current_user.id)\
        .order_by(GameSession.created_at.desc()).limit(10).all()
    
    return render_template('profile.html', 
                         user=current_user.to_dict(),
                         recent_sessions=[s.to_dict() for s in recent_sessions])

# API Routes
@app.route('/api/start_game', methods=['POST'])
@login_required
@limiter.limit("10/minute")
def api_start_game():
    """Start a new game session."""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', game_config.default_difficulty)
        game_mode = data.get('game_mode', game_config.default_game_mode)
        
        # Create new game session
        game_session = GameSession(
            user_id=current_user.id,
            difficulty=difficulty,
            game_mode=game_mode
        )
        db.session.add(game_session)
        db.session.commit()
        
        # Initialize game
        game = TokenGame(difficulty=difficulty, game_mode=game_mode)
        target_word, target_token_id = game.get_current_target()
        
        # Store game state in session
        session['game_session_id'] = game_session.id
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
            'session_id': game_session.id,
            'target_word': target_word,
            'target_token_id': target_token_id,
            'difficulty': difficulty,
            'game_mode': game_mode
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/make_guess', methods=['POST'])
@login_required
@limiter.limit("30/minute")
def api_make_guess():
    """Process a guess."""
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
        max_score = game_config.perfect_score
        score = max(0, max_score - int(distance * game_config.distance_penalty_factor))
        
        # Update game state
        game_state['attempts'] += 1
        game_state['score'] += score
        session['game_state'] = game_state
        
        # Check if correct
        is_correct = distance == 0
        
        # Save guess data
        if game_config.data_collection_enabled and current_user.is_authenticated:
            global data_collector
            if data_collector is None:
                data_collector = AsyncDataCollector(game_config.research_data_dir)
            
            # Record the guess (simplified for web version)
            guess_data = {
                'user_id': current_user.id,
                'session_id': session.get('game_session_id'),
                'guess_word': guess_word,
                'guess_token_id': guess_token_id,
                'target_word': game_state['target_word'],
                'target_token_id': target_token_id,
                'distance': distance,
                'score': score,
                'is_correct': is_correct,
                'timestamp': datetime.utcnow().isoformat()
            }
        
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
@login_required
@limiter.limit("20/minute")
def api_get_hints():
    """Get hints for the current target word."""
    try:
        game_state = session.get('game_state')
        if not game_state:
            return jsonify({'success': False, 'error': 'No active game'}), 400
        
        target_token_id = game_state['target_token_id']
        
        # Get nearby words from cache
        nearby_words = token_cache.get_nearby_words(
            target_token_id, 
            game_config.token_range_for_hints
        )
        
        # Format hints
        hints = []
        for word, token_id, distance in nearby_words[:game_config.nearby_words_count]:
            if word.lower() != game_state['target_word'].lower():
                hints.append({
                    'word': word,
                    'token_id': token_id,
                    'distance': distance
                })
        
        return jsonify({
            'success': True,
            'hints': hints,
            'target_token_id': target_token_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/end_game', methods=['POST'])
@login_required
def api_end_game():
    """End the current game session."""
    try:
        game_state = session.get('game_state')
        game_session_id = session.get('game_session_id')
        
        if game_session_id and game_state:
            # Update game session in database
            game_session = GameSession.query.get(game_session_id)
            if game_session:
                game_session.score = game_state['score']
                game_session.completed_at = datetime.utcnow()
                game_session.session_data = json.dumps(game_state)
                
                # Update user statistics
                current_user.total_games += 1
                current_user.total_score += game_state['score']
                if game_state['score'] > current_user.best_score:
                    current_user.best_score = game_state['score']
                
                db.session.commit()
        
        # Clear session
        session.pop('game_state', None)
        session.pop('game_session_id', None)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/leaderboard')
def api_leaderboard():
    """Get leaderboard data."""
    try:
        # Top players by best score
        top_players = User.query.order_by(User.best_score.desc()).limit(10).all()
        
        # Recent high scores
        recent_scores = GameSession.query.filter(GameSession.completed_at.isnot(None))\
            .order_by(GameSession.score.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'top_players': [
                {
                    'username': user.username,
                    'best_score': user.best_score,
                    'total_games': user.total_games
                }
                for user in top_players
            ],
            'recent_scores': [
                {
                    'username': session.user.username,
                    'score': session.score,
                    'difficulty': session.difficulty,
                    'completed_at': session.completed_at.isoformat() if session.completed_at else None
                }
                for session in recent_scores
            ]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(
        host=web_config.host,
        port=web_config.port,
        debug=web_config.debug
    ) 