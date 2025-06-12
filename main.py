#!/usr/bin/env python3
"""
Token Quest - Main Entry Point
Research project to analyze token ID relationships and semantic clustering

Author: Research Team
Purpose: Investigate if LLMs place semantically similar words similarly in token space
"""

import sys
import os
import subprocess

# Add current directory to path to ensure module imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Auto-install tiktoken if missing
try:
    import tiktoken
except ImportError:
    print("📦 tiktoken not found, installing automatically...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tiktoken"])
        print("✅ tiktoken installed successfully!")
        import tiktoken
    except subprocess.CalledProcessError:
        print("❌ Failed to install tiktoken automatically!")
        print("Please install it manually with: pip install tiktoken")
        sys.exit(1)
    except ImportError:
        print("❌ Still can't import tiktoken after installation!")
        print("Please try restarting your Python environment")
        sys.exit(1)

from main_gui import TokenGameGUI
from game_logic import GameLogic
from startup_dialog import show_startup_dialog


def apply_theme_and_title(game, settings):
    """Apply the selected theme and update window title."""
    # Update window title with mode information
    mode = settings.get('game_mode', 'normal')
    mode_text = f" - {mode.title()} Mode" if mode != 'normal' else ""
    game.root.title(f"Token Quest - Research Edition{mode_text}")
    
    # Theme colors
    themes = {
        'light': {'bg': '#f0f0f0', 'text': '#333333', 'card_bg': '#ffffff'},
        'dark': {'bg': '#2b2b2b', 'text': '#ffffff', 'card_bg': '#3c3c3c'},
        'blue': {'bg': '#E3F2FD', 'text': '#0D47A1', 'card_bg': '#BBDEFB'},
        'green': {'bg': '#E8F5E8', 'text': '#1B5E20', 'card_bg': '#C8E6C9'}
    }
    
    theme_name = settings.get('theme', 'light')
    if theme_name in themes:
        theme = themes[theme_name]
        
        # Apply theme to main window
        game.root.configure(bg=theme['bg'])
        
        # Apply theme to all UI elements
        apply_theme_to_widget(game.root, theme)


def apply_theme_to_widget(widget, theme):
    """Recursively apply theme to widgets."""
    try:
        widget_class = widget.winfo_class()
        
        if widget_class in ['Frame', 'Labelframe']:
            widget.configure(bg=theme['bg'])
        elif widget_class == 'Label':
            widget.configure(bg=theme['bg'], fg=theme['text'])
        elif widget_class == 'Button':
            # Only change buttons with default colors
            current_bg = widget.cget('bg')
            if current_bg in ['#f0f0f0', 'SystemButtonFace']:
                widget.configure(bg=theme['card_bg'], fg=theme['text'])
        
        # Recursively apply to children
        for child in widget.winfo_children():
            apply_theme_to_widget(child, theme)
    except:
        pass  # Some widgets might not support these options


def main():
    """Main function to start Token Quest."""
    print("🎯 Starting Token Quest...")
    print("Research Edition - Analyzing Token ID Relationships")
    print("-" * 50)
    
    try:
        # Test tiktoken installation
        enc = tiktoken.get_encoding("o200k_base")
        test_tokens = enc.encode("hello world")
        print(f"✅ tiktoken working! Test encoding: {test_tokens}")
        
        print("🖥️ Showing startup dialog...")
        
        # Show startup dialog to get user preferences
        settings = show_startup_dialog()
        
        # Check if user wants to start the game
        if not settings.get('start_game', False):
            print("👋 Goodbye!")
            return
        
        print(f"🎮 Starting game with settings: {settings}")
        
        # Create game logic with selected settings
        game_logic = GameLogic(
            max_rounds=settings.get('rounds', 10),
            game_mode=settings.get('game_mode', 'normal'),
            difficulty=settings.get('difficulty', 'mixed'),
            category=settings.get('category', 'all')
        )
        
        # Start the GUI game
        game = TokenGameGUI()
        game.game_logic = game_logic
        
        # Apply theme and update title
        apply_theme_and_title(game, settings)
        
        # Start first round with the configured game logic
        game.start_new_round()
        
        print("✅ GUI created successfully")
        game.run()
        
        print("\n👋 Thanks for playing! Your data helps our research.")
        
    except ImportError as e:
        if "tkinter" in str(e):
            print(f"❌ tkinter error: {e}")
            print("\nTkinter GUI is not available. This might be because:")
            print("1. You're running in a headless environment")
            print("2. tkinter is not installed with your Python")
            print("3. You're using WSL without X11 forwarding")
            print("\nTry installing tkinter: sudo apt-get install python3-tk")
        else:
            print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure tiktoken is installed: pip install tiktoken")
        print("2. Check that all game files are in the same directory")
        print("3. Ensure you have tkinter installed (usually comes with Python)")
        sys.exit(1)


if __name__ == "__main__":
    main() 