"""
GUI Interface Module
Simple tkinter-based interface for Token Synonym Game
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from game_logic import GameLogic
from data_collector import DataCollector


class TokenGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Token Synonym Game - Research Edition")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize game components
        self.game_logic = GameLogic()
        self.data_collector = DataCollector()
        
        # Game state
        self.current_round_active = False
        
        # Setup UI
        self.setup_ui()
        
        # Start first round
        self.start_new_round()
    
    def setup_ui(self):
        """Setup the main user interface."""
        # Main title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🎯 Token Synonym Game", 
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
        
        # Game info frame
        info_frame = tk.Frame(self.root, bg='#f0f0f0')
        info_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            info_frame,
            text="Score: 0",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.round_label = tk.Label(
            info_frame,
            text="Round: 1 / 10",
            font=('Arial', 14),
            bg='#f0f0f0'
        )
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.accuracy_label = tk.Label(
            info_frame,
            text="Correct: 0",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#4CAF50'
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=20)
        
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
        game_menu.add_command(label="Statistics", command=self.show_statistics)
        game_menu.add_separator()
        game_menu.add_command(label="Export Data", command=self.export_data)
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
        self.target_info_label.config(text=f"Token ID: {round_info['target_token_id']}")
        self.round_label.config(text=f"Round: {round_info['round_number']} / {round_info['max_rounds']}")
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.current_round_active = True
        
        # Clear previous feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        # Re-enable next button
        self.next_btn.config(state='normal')
    
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
        
        info_text = f"Your word: {result['guess_info']['word']} (Token ID: {result['guess_token_id']})\n"
        info_text += f"Distance: {result['distance']} | Round Score: +{result['round_score']}"
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 12),
            bg='white',
            fg='#333'
        )
        info_label.pack(pady=8)
    
    def show_hint(self):
        """Show a hint for the current round."""
        hint = self.game_logic.get_hint()
        
        if 'error' in hint:
            messagebox.showwarning("No Hint Available", hint['error'])
        else:
            messagebox.showinfo("Hint", hint['message'])
    
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