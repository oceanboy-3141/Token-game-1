"""
Startup Dialog for Token Quest
Shows game mode selection, theme options, and other settings before starting
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
import os
import sys

# Add tutorial import
try:
    from tutorial import show_tutorial
except ImportError:
    def show_tutorial():
        messagebox.showinfo("Tutorial", "Tutorial system not available.")


class StartupDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Token Quest - Setup")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Make it start maximized
        self.root.state('zoomed') if os.name == 'nt' else self.root.attributes('-zoomed', True)
        
        # Center the window
        self.center_window()
        
        # Game settings
        self.settings = {
            'game_mode': 'normal',
            'difficulty': 'mixed',
            'category': 'all',
            'theme': 'light',
            'rounds': 10,
            'start_game': False
        }
        
        # Theme colors
        self.themes = {
            'light': {
                'bg': '#f0f0f0',
                'text': '#333333',
                'accent': '#2196F3',
                'button_bg': '#4CAF50',
                'card_bg': '#ffffff'
            },
            'dark': {
                'bg': '#2b2b2b',
                'text': '#ffffff',
                'accent': '#64B5F6',
                'button_bg': '#66BB6A',
                'card_bg': '#3c3c3c'
            },
            'blue': {
                'bg': '#E3F2FD',
                'text': '#0D47A1',
                'accent': '#1976D2',
                'button_bg': '#2196F3',
                'card_bg': '#BBDEFB'
            },
            'green': {
                'bg': '#E8F5E8',
                'text': '#1B5E20',
                'accent': '#388E3C',
                'button_bg': '#4CAF50',
                'card_bg': '#C8E6C9'
            }
        }
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the startup dialog interface."""
        # Title section
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20, fill='x')
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Token Quest",
            font=('Arial', 28, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Choose your game settings and start playing!",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle_label.pack(pady=5)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Tutorial button (prominently placed)
        tutorial_frame = tk.Frame(content_frame, bg='#f0f0f0')
        tutorial_frame.pack(fill='x', pady=10)
        
        tutorial_btn = tk.Button(
            tutorial_frame,
            text="🎓 How to Play - Interactive Tutorial",
            font=('Arial', 14, 'bold'),
            bg='#FF9800',
            fg='white',
            padx=30,
            pady=15,
            command=self.show_tutorial,
            relief='raised',
            bd=3
        )
        tutorial_btn.pack()
        
        # Quick start section
        self.create_quick_start_section(content_frame)
        
        # Separator
        separator = tk.Frame(content_frame, height=2, bg='#ddd')
        separator.pack(fill='x', pady=20)
        
        # Advanced settings section
        self.create_advanced_settings(content_frame)
        
        # Theme section
        self.create_theme_section(content_frame)
        
        # Action buttons
        self.create_action_buttons()
    
    def create_quick_start_section(self, parent):
        """Create the quick start buttons section."""
        quick_frame = tk.LabelFrame(
            parent,
            text="⚡ Quick Start",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        quick_frame.pack(fill='x', pady=10)
        
        buttons_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=15)
        
        # Game mode buttons
        modes = [
            ("🎯 Classic", "normal", "Find synonyms with similar token IDs", '#4CAF50'),
            ("🔄 Antonym", "antonym", "Find opposites with distant token IDs", '#FF5722'),
            ("📂 Category", "category", "Focus on specific word categories", '#9C27B0'),
            ("⚡ Random", "mixed", "Mix of all modes for variety", '#FF9800')
        ]
        
        for i, (text, mode, desc, color) in enumerate(modes):
            btn_frame = tk.Frame(buttons_frame, bg='#f0f0f0')
            btn_frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky='ew')
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                padx=20,
                pady=12,
                width=15,
                command=lambda m=mode: self.quick_start(m)
            )
            btn.pack()
            
            desc_label = tk.Label(
                btn_frame,
                text=desc,
                font=('Arial', 9),
                bg='#f0f0f0',
                fg='#666',
                wraplength=180
            )
            desc_label.pack(pady=2)
        
        # Configure grid weights
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
    
    def create_advanced_settings(self, parent):
        """Create the advanced settings section."""
        settings_frame = tk.LabelFrame(
            parent,
            text="🔧 Advanced Settings",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        settings_frame.pack(fill='x', pady=10)
        
        # Settings grid
        grid_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        grid_frame.pack(pady=10, padx=20)
        
        # Game Mode
        tk.Label(grid_frame, text="Game Mode:", font=('Arial', 11, 'bold'), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5, pady=8)
        self.mode_var = tk.StringVar(value='normal')
        mode_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.mode_var,
            values=['normal', 'antonym', 'category'],
            state='readonly',
            width=18
        )
        mode_combo.grid(row=0, column=1, padx=10, pady=8)
        
        # Difficulty
        tk.Label(grid_frame, text="Difficulty:", font=('Arial', 11, 'bold'), bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=5, pady=8)
        self.diff_var = tk.StringVar(value='mixed')
        diff_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.diff_var,
            values=['easy', 'medium', 'hard', 'mixed'],
            state='readonly',
            width=18
        )
        diff_combo.grid(row=0, column=3, padx=10, pady=8)
        
        # Category
        tk.Label(grid_frame, text="Category:", font=('Arial', 11, 'bold'), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5, pady=8)
        self.cat_var = tk.StringVar(value='all')
        cat_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.cat_var,
            values=['all', 'emotions', 'size', 'speed', 'quality', 'temperature', 'brightness', 'actions', 'difficulty'],
            state='readonly',
            width=18
        )
        cat_combo.grid(row=1, column=1, padx=10, pady=8)
        
        # Rounds
        tk.Label(grid_frame, text="Rounds:", font=('Arial', 11, 'bold'), bg='#f0f0f0').grid(row=1, column=2, sticky='w', padx=5, pady=8)
        self.rounds_var = tk.StringVar(value='10')
        rounds_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.rounds_var,
            values=['5', '10', '15', '20'],
            state='readonly',
            width=18
        )
        rounds_combo.grid(row=1, column=3, padx=10, pady=8)
    
    def create_theme_section(self, parent):
        """Create the theme selection section."""
        theme_frame = tk.LabelFrame(
            parent,
            text="🎨 Theme Selection",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        theme_frame.pack(fill='x', pady=10)
        
        themes_grid = tk.Frame(theme_frame, bg='#f0f0f0')
        themes_grid.pack(pady=15)
        
        self.theme_var = tk.StringVar(value='light')
        
        theme_options = [
            ("☀️ Light", "light", "#f0f0f0"),
            ("🌙 Dark", "dark", "#2b2b2b"), 
            ("💙 Ocean", "blue", "#E3F2FD"),
            ("🌿 Nature", "green", "#E8F5E8")
        ]
        
        for i, (text, theme, color) in enumerate(theme_options):
            theme_btn = tk.Radiobutton(
                themes_grid,
                text=text,
                variable=self.theme_var,
                value=theme,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='#333' if theme in ['light', 'blue', 'green'] else '#fff',
                selectcolor=color,
                padx=15,
                pady=8,
                command=lambda: self.preview_theme()
            )
            theme_btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        for i in range(4):
            themes_grid.grid_columnconfigure(i, weight=1)
    
    def create_action_buttons(self):
        """Create the action buttons."""
        action_frame = tk.Frame(self.root, bg='#f0f0f0')
        action_frame.pack(side='bottom', pady=20)
        
        start_btn = tk.Button(
            action_frame,
            text="🚀 Start Game",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=40,
            pady=12,
            command=self.start_game
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        leaderboard_btn = tk.Button(
            action_frame,
            text="🏆 View Leaderboards",
            font=('Arial', 14, 'bold'),
            bg='#FFD700',
            fg='black',
            padx=30,
            pady=12,
            command=self.show_leaderboard
        )
        leaderboard_btn.pack(side=tk.LEFT, padx=10)
        
        achievements_btn = tk.Button(
            action_frame,
            text="🎖️ Achievements",
            font=('Arial', 14, 'bold'),
            bg='#9C27B0',
            fg='white',
            padx=30,
            pady=12,
            command=self.show_achievements
        )
        achievements_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(
            action_frame,
            text="❌ Exit",
            font=('Arial', 12),
            bg='#666',
            fg='white',
            padx=20,
            pady=12,
            command=self.root.quit
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
    
    def show_tutorial(self):
        """Show the interactive tutorial."""
        try:
            show_tutorial()
        except Exception as e:
            messagebox.showerror("Tutorial Error", f"Could not start tutorial: {e}")
    
    def show_leaderboard(self):
        """Show the leaderboard window."""
        try:
            from leaderboard import Leaderboard
            
            # Create leaderboard window
            leaderboard_window = tk.Toplevel(self.root)
            leaderboard_window.title("🏆 Token Quest Leaderboards")
            leaderboard_window.geometry("800x600")
            leaderboard_window.configure(bg='#f0f0f0')
            leaderboard_window.transient(self.root)
            leaderboard_window.grab_set()
            
            # Initialize leaderboard
            leaderboard = Leaderboard()
            
            # Title
            title_label = tk.Label(
                leaderboard_window,
                text="🏆 TOKEN QUEST LEADERBOARDS 🏆",
                font=('Arial', 24, 'bold'),
                bg='#f0f0f0',
                fg='#2196F3'
            )
            title_label.pack(pady=20)
            
            # Create notebook for different game modes
            notebook = ttk.Notebook(leaderboard_window)
            notebook.pack(expand=True, fill='both', padx=20, pady=10)
            
            # Game modes to show
            game_modes = ['normal', 'antonym', 'category']
            mode_names = {'normal': '🎯 Classic Mode', 'antonym': '🔄 Antonym Mode', 'category': '📂 Category Mode'}
            
            for mode in game_modes:
                # Create frame for this mode
                mode_frame = tk.Frame(notebook, bg='white')
                notebook.add(mode_frame, text=mode_names[mode])
                
                # Get scores for this mode
                scores = leaderboard.get_top_scores(mode, limit=10)
                
                if scores:
                    # Create headers
                    headers_frame = tk.Frame(mode_frame, bg='white')
                    headers_frame.pack(fill='x', padx=20, pady=10)
                    
                    tk.Label(headers_frame, text="Rank", font=('Arial', 12, 'bold'), bg='white', width=6).pack(side=tk.LEFT)
                    tk.Label(headers_frame, text="Player", font=('Arial', 12, 'bold'), bg='white', width=20).pack(side=tk.LEFT)
                    tk.Label(headers_frame, text="Score", font=('Arial', 12, 'bold'), bg='white', width=10).pack(side=tk.LEFT)
                    tk.Label(headers_frame, text="Accuracy", font=('Arial', 12, 'bold'), bg='white', width=10).pack(side=tk.LEFT)
                    tk.Label(headers_frame, text="Date", font=('Arial', 12, 'bold'), bg='white', width=15).pack(side=tk.LEFT)
                    
                    # Create scrollable frame for scores
                    canvas = tk.Canvas(mode_frame, bg='white')
                    scrollbar = ttk.Scrollbar(mode_frame, orient='vertical', command=canvas.yview)
                    scrollable_frame = tk.Frame(canvas, bg='white')
                    
                    scrollable_frame.bind(
                        '<Configure>',
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                    
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    # Add scores
                    for i, score in enumerate(scores[:10], 1):
                        score_frame = tk.Frame(scrollable_frame, bg='white', relief='ridge', bd=1)
                        score_frame.pack(fill='x', padx=5, pady=2)
                        
                        # Rank with medal
                        rank_text = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else f"   {i}"
                        tk.Label(score_frame, text=rank_text, font=('Arial', 11), bg='white', width=6).pack(side=tk.LEFT)
                        tk.Label(score_frame, text=score.get('player_name', 'Anonymous'), font=('Arial', 11), bg='white', width=20).pack(side=tk.LEFT)
                        tk.Label(score_frame, text=str(score['score']), font=('Arial', 11, 'bold'), bg='white', width=10).pack(side=tk.LEFT)
                        tk.Label(score_frame, text=f"{score.get('accuracy', 0):.1f}%", font=('Arial', 11), bg='white', width=10).pack(side=tk.LEFT)
                        tk.Label(score_frame, text=score.get('date', 'Unknown'), font=('Arial', 11), bg='white', width=15).pack(side=tk.LEFT)
                    
                    canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
                    scrollbar.pack(side="right", fill="y", pady=10)
                else:
                    # No scores message
                    no_scores_label = tk.Label(
                        mode_frame,
                        text=f"No scores recorded for {mode_names[mode]} yet!\nPlay some games to see leaderboards here.",
                        font=('Arial', 14),
                        bg='white',
                        fg='#666',
                        justify='center'
                    )
                    no_scores_label.pack(expand=True)
            
            # Close button
            close_btn = tk.Button(
                leaderboard_window,
                text="❌ Close",
                font=('Arial', 12),
                bg='#666',
                fg='white',
                padx=20,
                pady=10,
                command=leaderboard_window.destroy
            )
            close_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Leaderboard Error", f"Could not show leaderboards: {e}")
    
    def show_achievements(self):
        """Show the achievements window."""
        try:
            from achievements import AchievementManager
            
            # Create achievements window
            achievements_window = tk.Toplevel(self.root)
            achievements_window.title("🎖️ Token Quest Achievements")
            achievements_window.geometry("900x700")
            achievements_window.configure(bg='#f0f0f0')
            achievements_window.transient(self.root)
            achievements_window.grab_set()
            
            # Initialize achievement manager
            achievement_manager = AchievementManager()
            
            # Title
            title_label = tk.Label(
                achievements_window,
                text="🎖️ ACHIEVEMENTS 🎖️",
                font=('Arial', 24, 'bold'),
                bg='#f0f0f0',
                fg='#9C27B0'
            )
            title_label.pack(pady=20)
            
            # Stats summary
            stats = achievement_manager.get_stats_summary()
            stats_frame = tk.Frame(achievements_window, bg='#ffffff', relief='raised', bd=2)
            stats_frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(
                stats_frame,
                text=f"📊 Progress: {stats['achievements_unlocked']}/{stats['total_achievements']} achievements ({stats['completion_percentage']:.1f}%)",
                font=('Arial', 14, 'bold'),
                bg='#ffffff',
                fg='#333'
            ).pack(pady=10)
            
            # Create notebook for different categories
            notebook = ttk.Notebook(achievements_window)
            notebook.pack(expand=True, fill='both', padx=20, pady=10)
            
            # Categories
            categories = [
                ('accuracy', '🎯 Accuracy'),
                ('streaks', '🔥 Streaks'), 
                ('exploration', '🌍 Exploration'),
                ('mastery', '🎮 Mastery'),
                ('education', '🎓 Education'),
                ('special', '⭐ Special'),
                ('score', '💯 Score'),
                ('social', '👥 Social')
            ]
            
            for category_id, category_name in categories:
                # Create frame for this category
                category_frame = tk.Frame(notebook, bg='white')
                notebook.add(category_frame, text=category_name)
                
                # Create scrollable frame
                canvas = tk.Canvas(category_frame, bg='white')
                scrollbar = ttk.Scrollbar(category_frame, orient='vertical', command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg='white')
                
                scrollable_frame.bind(
                    '<Configure>',
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Get achievements for this category
                achievements = achievement_manager.get_achievements_by_category(category_id)
                
                if achievements:
                    for achievement in achievements:
                        # Achievement card
                        ach_frame = tk.Frame(scrollable_frame, bg='#f8f8f8', relief='ridge', bd=2)
                        ach_frame.pack(fill='x', padx=10, pady=5)
                        
                        # Achievement header
                        header_frame = tk.Frame(ach_frame, bg='#f8f8f8')
                        header_frame.pack(fill='x', padx=10, pady=5)
                        
                        # Icon and name
                        icon_name_frame = tk.Frame(header_frame, bg='#f8f8f8')
                        icon_name_frame.pack(side=tk.LEFT, fill='x', expand=True)
                        
                        icon_label = tk.Label(
                            icon_name_frame,
                            text=achievement.icon,
                            font=('Arial', 20),
                            bg='#f8f8f8'
                        )
                        icon_label.pack(side=tk.LEFT)
                        
                        name_label = tk.Label(
                            icon_name_frame,
                            text=achievement.name,
                            font=('Arial', 14, 'bold'),
                            bg='#f8f8f8',
                            fg='#4CAF50' if achievement.unlocked else '#666'
                        )
                        name_label.pack(side=tk.LEFT, padx=(10, 0))
                        
                        # Status
                        status_text = "✅ UNLOCKED" if achievement.unlocked else f"🔒 {achievement.progress}/{achievement.target_value}"
                        status_label = tk.Label(
                            header_frame,
                            text=status_text,
                            font=('Arial', 10, 'bold'),
                            bg='#f8f8f8',
                            fg='#4CAF50' if achievement.unlocked else '#FF9800'
                        )
                        status_label.pack(side=tk.RIGHT)
                        
                        # Description
                        desc_label = tk.Label(
                            ach_frame,
                            text=achievement.description,
                            font=('Arial', 11),
                            bg='#f8f8f8',
                            fg='#666',
                            wraplength=700,
                            justify='left'
                        )
                        desc_label.pack(anchor='w', padx=10, pady=(0, 5))
                        
                        # Progress bar for incomplete achievements
                        if not achievement.unlocked and achievement.target_value > 1:
                            progress_frame = tk.Frame(ach_frame, bg='#f8f8f8')
                            progress_frame.pack(fill='x', padx=10, pady=(0, 5))
                            
                            progress_bg = tk.Frame(progress_frame, bg='#e0e0e0', height=8)
                            progress_bg.pack(fill='x')
                            
                            progress_percent = min(100, (achievement.progress / achievement.target_value) * 100)
                            if progress_percent > 0:
                                progress_fill = tk.Frame(progress_bg, bg='#FF9800', height=8)
                                progress_fill.place(x=0, y=0, relwidth=progress_percent/100, height=8)
                        
                        # Unlock date for completed achievements
                        if achievement.unlocked and achievement.unlock_date:
                            unlock_date = achievement.unlock_date[:10]  # Just the date part
                            date_label = tk.Label(
                                ach_frame,
                                text=f"🗓️ Unlocked: {unlock_date}",
                                font=('Arial', 9, 'italic'),
                                bg='#f8f8f8',
                                fg='#999'
                            )
                            date_label.pack(anchor='w', padx=10, pady=(0, 5))
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
            
            # Close button
            close_btn = tk.Button(
                achievements_window,
                text="❌ Close",
                font=('Arial', 12),
                bg='#666',
                fg='white',
                padx=20,
                pady=10,
                command=achievements_window.destroy
            )
            close_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Achievements Error", f"Could not show achievements: {e}")
    
    def quick_start(self, mode):
        """Quick start with a specific mode."""
        self.settings['game_mode'] = mode
        if mode == 'mixed':
            # For mixed mode, randomize other settings
            import random
            self.settings['game_mode'] = random.choice(['normal', 'antonym', 'category'])
            self.settings['difficulty'] = random.choice(['easy', 'medium', 'hard'])
            self.settings['category'] = random.choice(['emotions', 'size', 'speed', 'quality'])
        
        self.start_game()
    
    def preview_theme(self):
        """Preview the selected theme."""
        theme_name = self.theme_var.get()
        theme = self.themes[theme_name]
        
        # Update the main window colors
        self.root.configure(bg=theme['bg'])
        
        # Update all frames and labels
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget, theme)
    
    def update_widget_theme(self, widget, theme):
        """Recursively update widget themes."""
        try:
            widget_class = widget.winfo_class()
            
            if widget_class in ['Frame', 'Labelframe']:
                widget.configure(bg=theme['bg'])
            elif widget_class == 'Label':
                widget.configure(bg=theme['bg'], fg=theme['text'])
            elif widget_class == 'Button':
                # Don't change colored buttons, only default ones
                current_bg = widget.cget('bg')
                if current_bg in ['#f0f0f0', '#2b2b2b', '#E3F2FD', '#E8F5E8']:
                    widget.configure(bg=theme['card_bg'], fg=theme['text'])
            
            # Recursively update children
            for child in widget.winfo_children():
                self.update_widget_theme(child, theme)
        except:
            pass  # Some widgets might not support these options
    
    def start_game(self):
        """Start the game with selected settings."""
        # Collect settings from UI
        self.settings.update({
            'game_mode': self.mode_var.get(),
            'difficulty': self.diff_var.get(),
            'category': self.cat_var.get(),
            'rounds': int(self.rounds_var.get()),
            'theme': self.theme_var.get(),
            'start_game': True
        })
        
        self.root.quit()
    
    def get_settings(self) -> Dict:
        """Get the selected game settings."""
        return self.settings
    
    def run(self) -> Dict:
        """Run the startup dialog and return settings."""
        self.root.mainloop()
        return self.settings


def show_startup_dialog() -> Dict:
    """Show the startup dialog and return the selected settings."""
    dialog = StartupDialog()
    return dialog.run()


if __name__ == "__main__":
    settings = show_startup_dialog()
    print("Selected settings:", settings) 