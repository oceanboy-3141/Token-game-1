#!/usr/bin/env python3
"""
Quick Start Launcher for Token Quest
Allows users to quickly select game modes and start playing
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .gui_interface import TokenGameGUI
from game_logic import GameLogic


class QuickStartLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Token Quest - Quick Start")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Game settings
        self.game_mode = tk.StringVar(value='normal')
        self.difficulty = tk.StringVar(value='mixed')
        self.category = tk.StringVar(value='all')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the launcher interface."""
        # Title
        title_label = tk.Label(
            self.root,
            text="🎯 Token Quest",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root,
            text="Select your game mode and start playing!",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle_label.pack(pady=5)
        
        # Quick start buttons
        quick_frame = tk.Frame(self.root, bg='#f0f0f0')
        quick_frame.pack(pady=20)
        
        tk.Label(
            quick_frame,
            text="⚡ Quick Start",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        ).pack()
        
        quick_buttons_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        quick_buttons_frame.pack(pady=10)
        
        # Quick start buttons
        self.create_quick_button(quick_buttons_frame, "🎯 Classic", "normal", "Play the classic synonym finding game!")
        self.create_quick_button(quick_buttons_frame, "🔄 Antonym", "antonym", "Find words with opposite meanings!")
        self.create_quick_button(quick_buttons_frame, "📂 Category", "category", "Focus on specific word types!")
        
        # Advanced settings section
        settings_frame = tk.LabelFrame(
            self.root,
            text="🔧 Advanced Settings",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        )
        settings_frame.pack(pady=20, padx=40, fill='x')
        
        # Settings grid
        settings_grid = tk.Frame(settings_frame, bg='#f0f0f0')
        settings_grid.pack(pady=10, padx=10, fill='x')
        
        # Game Mode
        tk.Label(settings_grid, text="Game Mode:", font=('Arial', 12, 'bold'), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        mode_combo = ttk.Combobox(
            settings_grid,
            textvariable=self.game_mode,
            values=['normal', 'antonym', 'category'],
            state='readonly',
            width=15
        )
        mode_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Difficulty
        tk.Label(settings_grid, text="Difficulty:", font=('Arial', 12, 'bold'), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        diff_combo = ttk.Combobox(
            settings_grid,
            textvariable=self.difficulty,
            values=['easy', 'medium', 'hard', 'mixed'],
            state='readonly',
            width=15
        )
        diff_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Category
        tk.Label(settings_grid, text="Category:", font=('Arial', 12, 'bold'), bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        cat_combo = ttk.Combobox(
            settings_grid,
            textvariable=self.category,
            values=['all', 'emotions', 'size', 'speed', 'quality', 'temperature', 'brightness', 'actions', 'difficulty'],
            state='readonly',
            width=15
        )
        cat_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Action buttons
        action_frame = tk.Frame(self.root, bg='#f0f0f0')
        action_frame.pack(pady=20)
        
        start_btn = tk.Button(
            action_frame,
            text="🚀 Start Game",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=30,
            pady=10,
            command=self.start_game
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(
            action_frame,
            text="❌ Exit",
            font=('Arial', 12),
            bg='#666',
            fg='white',
            padx=20,
            pady=10,
            command=self.root.quit
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
    
    def create_quick_button(self, parent, text, mode, description):
        """Create a quick start button."""
        btn_frame = tk.Frame(parent, bg='#f0f0f0')
        btn_frame.pack(side=tk.LEFT, padx=10)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=15,
            command=lambda: self.quick_start(mode)
        )
        btn.pack()
        
        desc_label = tk.Label(
            btn_frame,
            text=description,
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666',
            wraplength=150
        )
        desc_label.pack(pady=5)
    
    def quick_start(self, mode):
        """Quick start with a specific mode."""
        self.game_mode.set(mode)
        self.start_game()
    
    def start_game(self):
        """Start the game with selected settings."""
        try:
            # Close launcher
            self.root.withdraw()
            
            # Create game with selected settings
            game_logic = GameLogic(
                max_rounds=10,
                game_mode=self.game_mode.get(),
                difficulty=self.difficulty.get(),
                category=self.category.get()
            )
            
            # Start GUI
            game_gui = TokenGameGUI()
            game_gui.game_logic = game_logic
            
            # Update window title
            mode_text = f" - {self.game_mode.get().title()} Mode" if self.game_mode.get() != 'normal' else ""
            game_gui.root.title(f"Token Quest - Research Edition{mode_text}")
            
            # Start first round
            game_gui.start_new_round()
            
            # Run the game
            game_gui.run()
            
            # When game closes, show launcher again
            self.root.deiconify()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start game: {str(e)}")
            self.root.deiconify()
    
    def run(self):
        """Run the launcher."""
        self.root.mainloop()


def main():
    """Main function to start the launcher."""
    try:
        launcher = QuickStartLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error starting launcher: {e}")
        # Fallback to direct game start
        from main import main as game_main
        game_main()


if __name__ == "__main__":
    main() 