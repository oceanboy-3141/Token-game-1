"""
GUI Interface Module
Simple tkinter-based interface for Token Quest
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from game_logic import GameLogic
from data_collector import DataCollector
from leaderboard import Leaderboard

# Add tutorial import
try:
    from tutorial import show_tutorial
except ImportError:
    def show_tutorial():
        messagebox.showinfo("Tutorial", "Tutorial system not available.")


class TokenGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Token Quest - Research Edition")
        self.root.geometry("1000x700")
        
        # Make it start maximized on Windows
        try:
            self.root.state('zoomed')
        except:
            try:
                self.root.attributes('-zoomed', True)
            except:
                pass  # If maximizing fails, just use the set size
        self.root.configure(bg='#f0f0f0')
        
        # Initialize game components
        self.game_logic = GameLogic()
        self.data_collector = DataCollector()
        self.leaderboard = Leaderboard()
        
        # Game state
        self.current_round_active = False
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface."""
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 Token Quest", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Find words with similar token IDs!",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle_label.pack()
        
        # Game info frame with progress bars
        info_frame = tk.Frame(self.root, bg='#f0f0f0')
        info_frame.pack(pady=10, fill='x', padx=20)
        
        # Top stats row
        stats_row1 = tk.Frame(info_frame, bg='#f0f0f0')
        stats_row1.pack(fill='x', pady=5)
        
        self.score_label = tk.Label(
            stats_row1,
            text="Score: 0",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.round_label = tk.Label(
            stats_row1,
            text="Round: 1 / 10",
            font=('Arial', 14),
            bg='#f0f0f0'
        )
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.accuracy_label = tk.Label(
            stats_row1,
            text="Correct: 0",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#4CAF50'
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=20)
        
        # Progress bars row
        progress_row = tk.Frame(info_frame, bg='#f0f0f0')
        progress_row.pack(fill='x', pady=5)
        
        # Round progress bar
        tk.Label(progress_row, text="Game Progress:", font=('Arial', 10), bg='#f0f0f0').pack(anchor='w')
        self.round_progress = ttk.Progressbar(
            progress_row, 
            length=200, 
            mode='determinate',
            style='Green.Horizontal.TProgressbar'
        )
        self.round_progress.pack(anchor='w', pady=2)
        
        # Attempts progress (for current round)
        tk.Label(progress_row, text="Round Attempts:", font=('Arial', 10), bg='#f0f0f0').pack(anchor='w', pady=(10,0))
        self.attempts_progress = ttk.Progressbar(
            progress_row, 
            length=200, 
            mode='determinate',
            style='Blue.Horizontal.TProgressbar'
        )
        self.attempts_progress.pack(anchor='w', pady=2)
        
        # Target word frame
        target_frame = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        target_frame.pack(pady=20, padx=50, fill='x')
        
        tk.Label(
            target_frame,
            text="Target Word:",
            font=('Arial', 14),
            bg='white'
        ).pack(pady=5)
        
        self.target_word_label = tk.Label(
            target_frame,
            text="...",
            font=('Arial', 28, 'bold'),
            bg='white',
            fg='#2196F3'
        )
        self.target_word_label.pack(pady=10)
        
        self.target_info_label = tk.Label(
            target_frame,
            text="Token ID: ...",
            font=('Arial', 12),
            bg='white',
            fg='#666'
        )
        self.target_info_label.pack(pady=5)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="Your guess:",
            font=('Arial', 14),
            bg='#f0f0f0'
        ).pack()
        
        self.guess_entry = tk.Entry(
            input_frame,
            font=('Arial', 16),
            width=20,
            justify='center'
        )
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.submit_btn = tk.Button(
            button_frame,
            text="Submit Guess",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            command=self.submit_guess
        )
        self.submit_btn.pack(side=tk.LEFT, padx=10)
        
        self.hint_btn = tk.Button(
            button_frame,
            text="Get Hint",
            font=('Arial', 12),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=10,
            command=self.show_hint
        )
        self.hint_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = tk.Button(
            button_frame,
            text="Next Round",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            command=self.start_new_round
        )
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        self.settings_btn = tk.Button(
            button_frame,
            text="⚙️ Settings",
            font=('Arial', 12),
            bg='#9C27B0',
            fg='white',
            padx=20,
            pady=10,
            command=self.show_game_settings
        )
        self.settings_btn.pack(side=tk.LEFT, padx=10)
        
        # Tutorial button
        self.tutorial_btn = tk.Button(
            button_frame,
            text="🎓 Tutorial",
            font=('Arial', 12),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=10,
            command=self.show_tutorial
        )
        self.tutorial_btn.pack(side=tk.LEFT, padx=10)
        
        # Feedback frame
        self.feedback_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.feedback_frame.pack(pady=20, fill='x', padx=50)
        
        # Results area
        results_frame = tk.Frame(self.root, bg='#f0f0f0')
        results_frame.pack(pady=10, fill='both', expand=True, padx=50)
        
        tk.Label(
            results_frame,
            text="Recent Results:",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=8,
            font=('Courier', 10),
            bg='white'
        )
        self.results_text.pack(fill='both', expand=True, pady=5)
        
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Game Settings", command=self.show_game_settings)
        game_menu.add_separator()
        game_menu.add_command(label="🎓 Tutorial", command=self.show_tutorial)
        game_menu.add_separator()
        game_menu.add_command(label="Leaderboard", command=self.show_leaderboard)
        game_menu.add_command(label="Statistics", command=self.show_statistics)
        game_menu.add_command(label="Export Data", command=self.export_data)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
    
    def start_new_round(self):
        """Start a new round."""
        round_info = self.game_logic.start_new_round()
        
        # Check if game has ended
        if round_info.get('game_ended', False):
            self.show_final_results(round_info)
            return
        
        if 'error' in round_info:
            messagebox.showinfo("Game Complete", "Game has already ended!")
            return
        
        self.target_word_label.config(
            text=round_info['target_word'].upper(),
            fg='black',  # Reset to default color
            bg='#f0f0f0'  # Reset to default background
        )
        # Update info labels with game mode context
        mode_text = ""
        if round_info['game_mode'] == 'antonym':
            mode_text = " | 🔄 ANTONYM MODE: Find opposite words!"
        elif round_info['game_mode'] == 'category':
            mode_text = f" | 📂 CATEGORY: {round_info['category'].title()} words only"
        elif round_info['game_mode'] == 'speed':
            mode_text = f" | ⚡ SPEED MODE: {round_info['time_limit']}s per round!"
        
        info_text = f"Token ID: {round_info['target_token_id']}"
        if round_info['difficulty'] != 'mixed':
            info_text += f" | Difficulty: {round_info['difficulty'].title()}"
        info_text += mode_text
        
        self.target_info_label.config(text=info_text)
        self.round_label.config(text=f"Round: {round_info['round_number']} / {round_info['max_rounds']}")
        
        # Update progress bars
        self.update_progress_bars(round_info)
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.current_round_active = True
        
        # Clear previous feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        # Re-enable next button
        self.next_btn.config(state='normal')
    
    def update_progress_bars(self, round_info=None):
        """Update progress bars to show game and round progress."""
        if round_info:
            # Update game progress
            game_progress = (round_info['round_number'] / round_info['max_rounds']) * 100
            self.round_progress['value'] = game_progress
            
            # Reset attempts progress for new round
            self.attempts_progress['value'] = 0
        
        # Update attempts progress
        attempts_used = self.game_logic.current_attempts
        max_attempts = self.game_logic.max_attempts
        attempts_progress = (attempts_used / max_attempts) * 100
        self.attempts_progress['value'] = attempts_progress
    
    def submit_guess(self):
        """Submit the player's guess."""
        if not self.current_round_active:
            messagebox.showwarning("No Active Round", "Please start a new round first!")
            return
        
        guess = self.guess_entry.get().strip()
        if not guess:
            messagebox.showwarning("Empty Guess", "Please enter a word!")
            return
        
        result = self.game_logic.submit_guess(guess)
        
        if result['valid_guess']:
            # Valid guess - show results
            self.show_guess_result(result)
            
            # Log data for research
            self.data_collector.log_guess(self.game_logic.game_history[-1])
            
            # Update score display
            self.score_label.config(text=f"Score: {result['total_score']}")
            
            # Update accuracy display
            self.accuracy_label.config(text=f"Correct: {self.game_logic.correct_guesses}")
            
            # Update progress bars
            self.update_progress_bars()
            
            # Add to results log (commented out - removing ugly log display)
            # self.add_to_results_log(result)
            
            # Check if max attempts reached or word is correct - auto advance
            if result.get('max_attempts_reached') or result['feedback']['is_correct']:
                # Auto-advance to next word after a short delay
                self.root.after(2000, self.start_new_round)  # 2 second delay
                self.next_btn.config(state='disabled')  # Disable button during auto-advance
            
            # Check if this was the last round
            if result['round_number'] >= result['max_rounds']:
                # Enable "Next Round" button to show final results
                self.next_btn.config(text="View Results", bg='#4CAF50')
            
        else:
            # Invalid guess - check if max attempts reached
            if result.get('max_attempts_reached'):
                messagebox.showinfo("Max Attempts", "3 attempts used! Moving to next word...")
                self.start_new_round()  # Auto advance
            else:
                messagebox.showerror("Invalid Guess", result['error'])
            return
        
            self.guess_entry.delete(0, tk.END)
    
    def show_guess_result(self, result):
        """Display the result of a guess."""
        # Clear previous feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        feedback = result['feedback']
        
        # Update the target word display to show feedback instead
        self.target_word_label.config(
            text=feedback['result'],
            fg='white',
            bg=feedback['color']
        )
        
        # Create result display with colored background
        result_frame = tk.Frame(
            self.feedback_frame, 
            bg=feedback['color'], 
            relief='raised', 
            bd=3
        )
        result_frame.pack(fill='x', pady=10)
        
        # Feedback message (bigger and more prominent)
        feedback_label = tk.Label(
            result_frame,
            text=feedback['message'],
            font=('Arial', 16, 'bold'),
            bg=feedback['color'],
            fg='white'
        )
        feedback_label.pack(pady=10)
        
        # Detailed info with contrasting background
        info_frame = tk.Frame(result_frame, bg='white', relief='sunken', bd=1)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        # Calculate display values (always show larger - smaller = difference)
        guess_id = result['guess_token_id']
        target_id = self.game_logic.current_target_token_id
        larger_id = max(guess_id, target_id)
        smaller_id = min(guess_id, target_id)
        
        info_text = f"Your word: {result['guess_info']['word']} (Token ID: {result['guess_token_id']})\n"
        info_text += f"Calculation: {larger_id} - {smaller_id} = {result['distance']} | Round Score: +{result['round_score']}"
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 12),
            bg='white',
            fg='#333'
        )
        info_label.pack(pady=8)
        
        # Schedule to change back to target word after 3 seconds
        self.root.after(3000, lambda: self.reset_target_display())
    
    def reset_target_display(self):
        """Reset the target word display back to showing the target word."""
        if hasattr(self, 'game_logic') and self.game_logic.current_target_word:
            self.target_word_label.config(
                text=self.game_logic.current_target_word.upper(),
                fg='#2196F3',
                bg='white'
            )
    
    def show_hint(self):
        """Show enhanced hint with contextual suggestions."""
        hint_data = self.game_logic.get_hint()
        
        if 'error' in hint_data:
            messagebox.showwarning("No Hint Available", hint_data['error'])
            return
        
        # Create enhanced hint popup
        hint_window = tk.Toplevel(self.root)
        hint_window.title("💡 Enhanced Hint")
        hint_window.geometry("500x400")
        hint_window.configure(bg='#f9f9f9')
        hint_window.transient(self.root)
        
        # Title
        tk.Label(
            hint_window,
            text=f"Hint for: {hint_data['target_word'].upper()}",
            font=('Arial', 16, 'bold'),
            bg='#f9f9f9',
            fg='#2196F3'
        ).pack(pady=10)
        
        # Contextual hint message
        tk.Label(
            hint_window,
            text=hint_data['hint_message'],
            font=('Arial', 12),
            bg='#f9f9f9',
            wraplength=450,
            fg='#333'
        ).pack(pady=10)
        
        # Token range info
        tk.Label(
            hint_window,
            text=hint_data['token_range'],
            font=('Arial', 10),
            bg='#f9f9f9',
            fg='#666'
        ).pack(pady=5)
        
        # Suggested words section
        if hint_data['suggested_words']:
            tk.Label(
                hint_window,
                text="💭 Words with nearby token IDs:",
                font=('Arial', 11, 'bold'),
                bg='#f9f9f9',
                fg='#333'
            ).pack(pady=(10, 5))
            
            # Create frame for word suggestions
            words_frame = tk.Frame(hint_window, bg='#f9f9f9')
            words_frame.pack(pady=5)
            
            # Display suggested words as clickable buttons
            for i, word in enumerate(hint_data['suggested_words'][:6]):
                word_btn = tk.Button(
                    words_frame,
                    text=word,
                    font=('Arial', 10),
                    bg='#E3F2FD',
                    fg='#1976D2',
                    relief='raised',
                    padx=8,
                    pady=2,
                    command=lambda w=word: self.insert_hint_word(w, hint_window)
                )
                word_btn.grid(row=i//3, column=i%3, padx=5, pady=2)
        
        # Close button
        tk.Button(
            hint_window,
            text="Got it! 👍",
            command=hint_window.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5
        ).pack(pady=20)
    
    def insert_hint_word(self, word, hint_window):
        """Insert a suggested word into the guess entry."""
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.insert(0, word)
        hint_window.destroy()
        self.guess_entry.focus()
    
    def show_tutorial(self):
        """Show the interactive tutorial."""
        try:
            show_tutorial()
        except Exception as e:
            messagebox.showerror("Tutorial Error", f"Could not start tutorial: {e}")
    
    def show_game_settings(self):
        """Show game settings dialog for mode, difficulty, and category selection."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("🎮 Game Settings")
        settings_window.geometry("500x600")
        settings_window.configure(bg='#f0f0f0')
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Title
        tk.Label(
            settings_window,
            text="🎮 Game Settings",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        ).pack(pady=20)
        
        # Game Mode Section
        mode_frame = tk.LabelFrame(settings_window, text="Game Mode", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        mode_frame.pack(pady=10, padx=20, fill='x')
        
        self.mode_var = tk.StringVar(value=self.game_logic.game_mode)
        modes = self.game_logic.get_available_modes()
        
        for mode, description in modes.items():
            mode_radio = tk.Radiobutton(
                mode_frame,
                text=f"{mode.title()}: {description}",
                variable=self.mode_var,
                value=mode,
                font=('Arial', 10),
                bg='#f0f0f0',
                wraplength=400,
                justify='left'
            )
            mode_radio.pack(anchor='w', pady=2, padx=10)
        
        # Difficulty Section
        diff_frame = tk.LabelFrame(settings_window, text="Difficulty", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        diff_frame.pack(pady=10, padx=20, fill='x')
        
        self.diff_var = tk.StringVar(value=self.game_logic.difficulty)
        difficulties = self.game_logic.get_available_difficulties()
        
        for diff, description in difficulties.items():
            diff_radio = tk.Radiobutton(
                diff_frame,
                text=f"{diff.title()}: {description}",
                variable=self.diff_var,
                value=diff,
                font=('Arial', 10),
                bg='#f0f0f0',
                wraplength=400,
                justify='left'
            )
            diff_radio.pack(anchor='w', pady=2, padx=10)
        
        # Category Section
        cat_frame = tk.LabelFrame(settings_window, text="Word Category", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        cat_frame.pack(pady=10, padx=20, fill='x')
        
        self.cat_var = tk.StringVar(value=self.game_logic.category)
        categories = self.game_logic.get_available_categories()
        
        for cat, description in categories.items():
            cat_radio = tk.Radiobutton(
                cat_frame,
                text=f"{cat.title()}: {description}",
                variable=self.cat_var,
                value=cat,
                font=('Arial', 10),
                bg='#f0f0f0',
                wraplength=400,
                justify='left'
            )
            cat_radio.pack(anchor='w', pady=2, padx=10)
        
        # Buttons
        button_frame = tk.Frame(settings_window, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        apply_btn = tk.Button(
            button_frame,
            text="Apply Settings",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: self.apply_game_settings(settings_window)
        )
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Arial', 12),
            bg='#666',
            fg='white',
            padx=20,
            pady=10,
            command=settings_window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def apply_game_settings(self, settings_window):
        """Apply the selected game settings."""
        # Get selected values
        new_mode = self.mode_var.get()
        new_difficulty = self.diff_var.get()
        new_category = self.cat_var.get()
        
        # Update game logic
        self.game_logic.change_game_settings(
            game_mode=new_mode,
            difficulty=new_difficulty,
            category=new_category
        )
        
        # Update window title to show current mode
        mode_text = f" - {new_mode.title()} Mode" if new_mode != 'normal' else ""
        self.root.title(f"Token Quest - Research Edition{mode_text}")
        
        # Close settings window
        settings_window.destroy()
        
        # Start a new game with new settings
        if messagebox.askyesno("New Game", "Settings applied! Start a new game with these settings?"):
            self.new_game()
    
    def show_leaderboard(self):
        """Show the leaderboard window."""
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("🏆 Leaderboard")
        leaderboard_window.geometry("700x500")
        leaderboard_window.configure(bg='#f0f0f0')
        leaderboard_window.transient(self.root)
        
        # Title
        tk.Label(
            leaderboard_window,
            text="🏆 LEADERBOARD 🏆",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#FFD700'
        ).pack(pady=20)
        
        # Mode selection
        mode_frame = tk.Frame(leaderboard_window, bg='#f0f0f0')
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Game Mode:", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.leaderboard_mode_var = tk.StringVar(value='normal')
        mode_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.leaderboard_mode_var,
            values=['normal', 'antonym', 'category', 'speed'],
            state='readonly',
            width=15
        )
        mode_combo.pack(side=tk.LEFT, padx=10)
        mode_combo.bind('<<ComboboxSelected>>', lambda e: self.update_leaderboard_display())
        
        # Leaderboard display
        display_frame = tk.Frame(leaderboard_window, bg='white', relief='raised', bd=2)
        display_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Create text widget for leaderboard
        self.leaderboard_text = scrolledtext.ScrolledText(
            display_frame,
            font=('Courier', 11),
            bg='white',
            fg='#333',
            height=15
        )
        self.leaderboard_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(leaderboard_window, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            padx=15,
            pady=5,
            command=self.update_leaderboard_display
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(
            button_frame,
            text="📁 Export",
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            padx=15,
            pady=5,
            command=self.export_leaderboard
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="❌ Close",
            font=('Arial', 10),
            bg='#666',
            fg='white',
            padx=15,
            pady=5,
            command=leaderboard_window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Initial display
        self.update_leaderboard_display()
    
    def update_leaderboard_display(self):
        """Update the leaderboard display with current mode."""
        mode = self.leaderboard_mode_var.get()
        top_scores = self.leaderboard.get_top_scores(mode, 15)
        
        self.leaderboard_text.delete(1.0, tk.END)
        
        if not top_scores:
            self.leaderboard_text.insert(tk.END, f"No scores yet for {mode.title()} mode!\nBe the first to play and set a record! 🎯")
            return
        
        # Header
        header = f"🎮 {mode.upper()} MODE - TOP SCORES\n"
        header += "=" * 60 + "\n\n"
        header += f"{'Rank':<4} {'Player':<15} {'Score':<6} {'Accuracy':<8} {'Date':<12}\n"
        header += "-" * 60 + "\n"
        
        self.leaderboard_text.insert(tk.END, header)
        
        # Scores
        for i, entry in enumerate(top_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            line = f"{medal} {i:<2} {entry['player_name']:<15} {entry['score']:<6} {entry['accuracy']:<7.1f}% {entry['date'][:10]}\n"
            self.leaderboard_text.insert(tk.END, line)
        
        # Statistics
        stats = self.leaderboard.get_statistics()
        if mode in stats.get('mode_statistics', {}):
            mode_stats = stats['mode_statistics'][mode]
            stats_text = f"\n📊 {mode.upper()} MODE STATISTICS\n"
            stats_text += "-" * 30 + "\n"
            stats_text += f"Total Games: {mode_stats['total_games']}\n"
            stats_text += f"Highest Score: {mode_stats['highest_score']}\n"
            stats_text += f"Average Score: {mode_stats['average_score']:.1f}\n"
            stats_text += f"Best Accuracy: {mode_stats['best_accuracy']:.1f}%\n"
            
            self.leaderboard_text.insert(tk.END, stats_text)
    
    def export_leaderboard(self):
        """Export leaderboard to file."""
        try:
            filepath = self.leaderboard.export_leaderboard()
            messagebox.showinfo("Export Successful", f"Leaderboard exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export leaderboard: {str(e)}")
    
    def submit_to_leaderboard(self, final_results, results_window):
        """Submit score to leaderboard."""
        player_name = simpledialog.askstring(
            "Leaderboard Submission",
            "Enter your name for the leaderboard:",
            initialvalue="Anonymous"
        )
        
        if player_name:
            try:
                rank = self.leaderboard.add_score(player_name.strip(), final_results)
                game_mode = final_results.get('game_mode', 'normal')
                
                messagebox.showinfo(
                    "🏆 Leaderboard Success!",
                    f"Congratulations!\n\n"
                    f"Your score of {final_results['total_score']} has been added to the "
                    f"{game_mode.title()} mode leaderboard!\n\n"
                    f"Your rank: #{rank}"
                )
                
                results_window.destroy()
                
                # Ask if they want to view the leaderboard
                if messagebox.askyesno("View Leaderboard", "Would you like to view the updated leaderboard?"):
                    self.show_leaderboard()
                    
            except Exception as e:
                messagebox.showerror("Leaderboard Error", f"Failed to submit score: {str(e)}")
    
    def add_to_results_log(self, result):
        """Add result to the scrollable results log."""
        target_word = self.game_logic.current_target_word
        guess_word = result['guess_info']['word']
        distance = result['distance']
        score = result['round_score']
        
        feedback = result['feedback']
        result_symbol = "✓" if feedback['is_correct'] else "✗"
        
        log_entry = f"Round {self.game_logic.round_number}: {result_symbol} {target_word} → {guess_word} | Distance: {distance} | Score: +{score} | {feedback['result']}\n"
        
        self.results_text.insert(tk.END, log_entry)
        self.results_text.see(tk.END)
    
    def new_game(self):
        """Start a completely new game."""
        if messagebox.askyesno("New Game", "Start a new game? This will reset your score."):
            # Save current session data
            self.data_collector.save_session()
            
            # Reset game
            self.game_logic.reset_game()
            self.data_collector = DataCollector()  # New session
            
            # Reset UI
            self.score_label.config(text="Score: 0")
            self.accuracy_label.config(text="Correct: 0")
            self.results_text.delete(1.0, tk.END)
            
            # Reset button states
            self.next_btn.config(text="Next Round", bg='#2196F3', state='normal')
            self.current_round_active = False
            
            # Clear feedback
            for widget in self.feedback_frame.winfo_children():
                widget.destroy()
            
            # Start new round
            self.start_new_round()
    
    def show_statistics(self):
        """Show game statistics."""
        stats = self.game_logic.get_game_stats()
        
        if stats['total_rounds'] == 0:
            messagebox.showinfo("Statistics", "No games played yet!")
            return
        
        stats_text = f"""Game Statistics:
        
Total Rounds: {stats['total_rounds']}
Current Score: {stats['total_score']}
Average Distance: {stats['average_distance']:.1f}
Best Distance: {stats['best_distance']}
Worst Distance: {stats['worst_distance']}"""
        
        messagebox.showinfo("Statistics", stats_text)
    
    def export_data(self):
        """Export game data for research."""
        try:
            csv_file = self.data_collector.export_to_csv()
            session_file = self.data_collector.save_session()
            
            message = f"Data exported successfully!\n\nFiles created:\n- {csv_file}\n- {session_file}"
            messagebox.showinfo("Export Successful", message)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
    
    def show_final_results(self, round_info):
        """Show final game results in a popup."""
        final_results = self.game_logic.get_final_results()
        
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("🎉 Game Complete!")
        results_window.geometry("600x500")
        results_window.configure(bg='#f0f0f0')
        results_window.transient(self.root)
        results_window.grab_set()
        
        # Title
        title_label = tk.Label(
            results_window,
            text="🎉 GAME COMPLETE! 🎉",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#4CAF50'
        )
        title_label.pack(pady=20)
        
        # Results frame
        results_frame = tk.Frame(results_window, bg='white', relief='raised', bd=2)
        results_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Score section
        score_label = tk.Label(
            results_frame,
            text=f"Final Score: {final_results['total_score']}",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2196F3'
        )
        score_label.pack(pady=10)
        
        # Stats
        stats_text = f"""
📊 GAME STATISTICS 📊

✓ Correct Guesses: {final_results['correct_guesses']} / 10
📈 Accuracy: {final_results['accuracy']:.1f}%
🎯 Average Distance: {final_results['average_distance']:.1f}
🏆 Best Distance: {final_results['best_distance']}
        """
        
        stats_label = tk.Label(
            results_frame,
            text=stats_text,
            font=('Arial', 14),
            bg='white',
            fg='#333',
            justify='left'
        )
        stats_label.pack(pady=20)
        
        # Performance rating based on accuracy
        accuracy = final_results['accuracy']
        if accuracy >= 80:
            rating = "🌟 AMAZING! You got most words right!"
            rating_color = '#4CAF50'
        elif accuracy >= 60:
            rating = "⭐ GREAT! You're good at finding synonyms!"
            rating_color = '#8BC34A'
        elif accuracy >= 40:
            rating = "👍 GOOD! You got some words right!"
            rating_color = '#FFC107'
        else:
            rating = "🤔 OKAY! Keep practicing to get better!"
            rating_color = '#FF9800'
        
        rating_label = tk.Label(
            results_frame,
            text=rating,
            font=('Arial', 16, 'bold'),
            bg='white',
            fg=rating_color
        )
        rating_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(results_frame, bg='white')
        button_frame.pack(pady=20)
        
        play_again_btn = tk.Button(
            button_frame,
            text="🎮 Play Again",
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: [results_window.destroy(), self.new_game()]
        )
        play_again_btn.pack(side=tk.LEFT, padx=10)
        
        # Check if this is a high score
        game_mode = final_results.get('game_mode', 'normal')
        is_high_score = self.leaderboard.is_high_score(final_results['total_score'], game_mode)
        
        if is_high_score:
            leaderboard_btn = tk.Button(
                button_frame,
                text="🏆 Submit to Leaderboard",
                font=('Arial', 14, 'bold'),
                bg='#FFD700',
                fg='black',
                padx=20,
                pady=10,
                command=lambda: self.submit_to_leaderboard(final_results, results_window)
            )
            leaderboard_btn.pack(side=tk.LEFT, padx=10)
        
        export_btn = tk.Button(
            button_frame,
            text="📊 Export Data",
            font=('Arial', 14),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: [self.export_data(), results_window.destroy()]
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = tk.Button(
            button_frame,
            text="❌ Close",
            font=('Arial', 14),
            bg='#666',
            fg='white',
            padx=20,
            pady=10,
            command=results_window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=10)
        
        # Disable main game controls
        self.current_round_active = False
        self.next_btn.config(text="Game Complete", state='disabled')
    
    def run(self):
        """Start the game."""
        self.root.mainloop()
        
        # Save data when closing
        try:
            self.data_collector.save_session()
        except:
            pass


if __name__ == "__main__":
    game = TokenGameGUI()
    game.run() 