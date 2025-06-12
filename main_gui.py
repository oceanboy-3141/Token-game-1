"""
Main GUI Interface for Token Quest
Core application window and game interface using modular components
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import os

from material_components import MaterialColors, MaterialComponents, MaterialTypography
from animations import AnimationManager
from dialogs import DialogManager
from game_logic import GameLogic
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
        self.root.title("Token Quest - Educational Research Edition")
        self.root.geometry("1200x800")
        
        # Initialize component managers
        self.animation_manager = AnimationManager()
        self.dialog_manager = DialogManager(self.root)
        
        # Material Design window setup
        self._setup_window()
        
        # Initialize game components with enhanced data collection
        self.game_logic = GameLogic()
        self.data_collector = self._create_enhanced_data_collector()
        self.leaderboard = Leaderboard()
        
        # Initialize achievements
        try:
            from achievements import AchievementManager
            self.achievement_manager = AchievementManager()
        except ImportError:
            self.achievement_manager = None
        
        # Game state
        self.current_round_active = False
        
        # Setup modern UI
        self.setup_material_ui()
        
        # Configure ttk styles
        MaterialComponents.configure_ttk_styles()
    
    def _create_enhanced_data_collector(self):
        """Create enhanced data collector with automatic comprehensive logging."""
        # Try to create the directory structure the user requested
        possible_paths = [
            # User's preferred location
            os.path.expanduser("~/Desktop/Game Coding Projects/vibe coding/Token data from token game"),
            # Alternative desktop location
            os.path.join(os.path.expanduser("~"), "Desktop", "Token data from token game"),
            # Current directory fallback
            os.path.join(os.getcwd(), "Token data from token game"),
            # Game data subdirectory fallback
            os.path.join(os.getcwd(), "game_data", "comprehensive_research_data")
        ]
        
        research_data_dir = None
        for path in possible_paths:
            try:
                os.makedirs(path, exist_ok=True)
                # Test write access
                test_file = os.path.join(path, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                research_data_dir = path
                print(f"✅ Research data directory created: {research_data_dir}")
                break
            except Exception as e:
                print(f"❌ Could not create {path}: {e}")
                continue
        
        if not research_data_dir:
            research_data_dir = "game_data"  # Final fallback
            os.makedirs(research_data_dir, exist_ok=True)
        
        from enhanced_data_collector import EnhancedDataCollector
        return EnhancedDataCollector(research_data_dir)
    
    def _setup_window(self):
        """Configure the main window with material design principles."""
        self.root.configure(bg=MaterialColors.BACKGROUND)
        
        # Make responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if screen_width >= 1400 and screen_height >= 900:
            try:
                self.root.state('zoomed' if os.name == 'nt' else 'normal')
            except:
                pass
        
        # Center the window
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
    
    def setup_material_ui(self):
        """Setup the main UI with material design components."""
        # Main container
        self.main_container = tk.Frame(self.root, bg=MaterialColors.BACKGROUND)
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Setup sections
        self._setup_header()
        self._setup_game_area()
        self._setup_footer()
        self._setup_menu()
    
    def _setup_header(self):
        """Setup header with title and progress."""
        self.header_frame = tk.Frame(self.main_container, bg=MaterialColors.BACKGROUND)
        self.header_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        self.title_label = MaterialComponents.create_material_label(
            self.header_frame, "🎯 Token Quest - Research Edition", 'headline_large',
            fg=MaterialColors.PRIMARY
        )
        self.title_label.pack()
        
        # Progress bars
        self._setup_progress_bars()
    
    def _setup_progress_bars(self):
        """Setup progress tracking."""
        progress_frame = tk.Frame(self.header_frame, bg=MaterialColors.BACKGROUND)
        progress_frame.pack(fill='x', pady=10)
        
        # Game progress
        self.game_progress = ttk.Progressbar(
            progress_frame, style="Material.Horizontal.TProgressbar", mode='determinate'
        )
        self.game_progress.pack(fill='x', pady=2)
        
        self.progress_label = MaterialComponents.create_material_label(
            progress_frame, "Ready to start!", 'body'
        )
        self.progress_label.pack()
    
    def _setup_game_area(self):
        """Setup main game area."""
        self.game_frame = tk.Frame(self.main_container, bg=MaterialColors.BACKGROUND)
        self.game_frame.pack(fill='both', expand=True)
        
        # Game controls
        controls_card, _ = MaterialComponents.create_material_card(self.game_frame)
        controls_card.pack(fill='x', pady=10)
        
        # Target word display
        self.target_label = MaterialComponents.create_material_label(
            controls_card, "Click 'New Game' to start!", 'headline_medium',
            fg=MaterialColors.PRIMARY
        )
        self.target_label.pack(pady=10)
        
        # Input
        self.guess_frame, self.guess_entry = MaterialComponents.create_material_entry(
            controls_card, "Enter your guess..."
        )
        self.guess_frame.pack(fill='x', pady=10)
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())
        
        # Buttons
        button_frame = tk.Frame(controls_card, bg=MaterialColors.SURFACE)
        button_frame.pack(fill='x', pady=10)
        
        MaterialComponents.create_material_button(
            button_frame, "Submit Guess", self.submit_guess, 'primary'
        ).pack(side='left', padx=5)
        
        MaterialComponents.create_material_button(
            button_frame, "💡 Hint", self.show_hint, 'secondary'
        ).pack(side='left', padx=5)
        
        MaterialComponents.create_material_button(
            button_frame, "🆕 New Game", self.new_game, 'outline'
        ).pack(side='left', padx=5)
        
        # Results area
        results_card, _ = MaterialComponents.create_material_card(self.game_frame)
        results_card.pack(fill='both', expand=True, pady=10)
        
        self.results_text = tk.Text(
            results_card, height=15, font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE_VARIANT, fg=MaterialColors.ON_SURFACE,
            relief='flat', wrap='word'
        )
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _setup_footer(self):
        """Setup footer with score."""
        self.footer_frame = tk.Frame(self.main_container, bg=MaterialColors.BACKGROUND)
        self.footer_frame.pack(fill='x', pady=(10, 0))
        
        self.score_label = MaterialComponents.create_material_label(
            self.footer_frame, "💯 Score: 0", 'title_medium', fg=MaterialColors.PRIMARY
        )
        self.score_label.pack(side='left')
        
        self.status_label = MaterialComponents.create_material_label(
            self.footer_frame, "Ready to play! 🎮", 'body'
        )
        self.status_label.pack(side='right')
    
    def _setup_menu(self):
        """Setup menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎮 Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_command(label="Settings", command=self.show_settings)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.exit_app)
        
        # Data menu
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📊 Data", menu=data_menu)
        data_menu.add_command(label="Statistics", command=self.show_statistics)
        data_menu.add_command(label="Export Data", command=self.export_data)
    
    # Core game methods
    def new_game(self):
        """Start a new game."""
        self.game_logic.reset_game()
        self.start_new_round()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🎮 New game started! Good luck!\n" + "="*50 + "\n")
        
        # Log comprehensive game start
        self.data_collector.log_game_start({
            'mode': self.game_logic.game_mode,
            'difficulty': self.game_logic.difficulty,
            'category': self.game_logic.category,
            'max_rounds': self.game_logic.max_rounds
        })
    
    def start_new_round(self):
        """Start a new round."""
        round_info = self.game_logic.start_new_round()
        
        if round_info.get('game_ended', False):
            self.show_final_results(round_info)
            return
        
        # Update UI
        self.target_label.config(text=f"🎯 {round_info['target_word']} (Token ID: {round_info['target_token_id']})")
        self.guess_entry.delete(0, tk.END)
        self.update_progress(round_info)
        
        # Log comprehensive round start
        self.data_collector.log_round_start(round_info)
        
        self.current_round_active = True
        self.status_label.config(text="Make your guess! 🎯")
    
    def submit_guess(self):
        """Submit a guess."""
        if not self.current_round_active:
            return
        
        guess = self.guess_entry.get().strip()
        if not guess or guess == "Enter your guess...":
            self.animation_manager.shake_animation(self.guess_frame)
            return
        
        # Process guess
        result = self.game_logic.submit_guess(guess)
        
        # Log comprehensive guess data
        self.data_collector.log_comprehensive_guess(result)
        
        # Update UI
        self.show_result(result)
        self.update_progress()
        
        # Check for round end
        if result.get('max_attempts_reached') or result.get('distance', float('inf')) <= 10:
            self.current_round_active = False
            self.root.after(2000, self.start_new_round)  # Auto-advance after 2 seconds
    
    def show_result(self, result):
        """Display guess result."""
        self.results_text.insert(tk.END, f"\n🎯 Target: {self.game_logic.current_target_word} (ID: {self.game_logic.current_target_token_id})\n")
        self.results_text.insert(tk.END, f"💭 Guess: {result['guess_word']} (ID: {result.get('guess_token_id', 'N/A')})\n")
        self.results_text.insert(tk.END, f"📏 Distance: {result['distance']}\n")
        self.results_text.insert(tk.END, f"💰 Points: {result['round_score']}\n")
        
        if 'feedback' in result:
            self.results_text.insert(tk.END, f"📝 {result['feedback']['explanation']}\n")
        
        self.results_text.insert(tk.END, "-" * 50 + "\n")
        self.results_text.see(tk.END)
        
        # Update score
        self.score_label.config(text=f"💯 Score: {self.game_logic.score}")
        
        # Visual feedback
        if result['distance'] <= 50:
            self.animation_manager.pulse_animation(self.target_label)
    
    def show_hint(self):
        """Show hint."""
        if not self.current_round_active:
            return
        
        hint_data = self.game_logic.get_hint()
        # Simple hint display for now
        hint_text = hint_data.get('context_hint', 'No hint available')
        messagebox.showinfo("💡 Hint", hint_text)
        
        # Log hint usage
        self.data_collector.log_hint_usage(hint_data)
    
    def show_final_results(self, round_info):
        """Show final game results."""
        final_results = self.game_logic.get_final_results()
        
        # Log comprehensive game completion
        self.data_collector.log_game_completion(final_results)
        
        result_text = f"""
🎉 Game Complete!

Final Score: {final_results['final_score']}
Correct Guesses: {final_results['correct_guesses']}/{final_results['total_rounds']}

Great job exploring token space! 🚀
        """
        messagebox.showinfo("Game Complete", result_text)
        
        self.current_round_active = False
        self.status_label.config(text="Game complete! 🎉")
    
    def update_progress(self, round_info=None):
        """Update progress bars."""
        if round_info is None:
            round_info = {
                'current_round': self.game_logic.round_number,
                'max_rounds': self.game_logic.max_rounds
            }
        
        progress = (round_info['current_round'] / round_info['max_rounds']) * 100
        self.game_progress['value'] = progress
        self.progress_label.config(text=f"Round {round_info['current_round']}/{round_info['max_rounds']}")
    
    # Menu actions
    def show_settings(self):
        """Show settings dialog."""
        messagebox.showinfo("Settings", "Settings dialog coming soon!")
    
    def show_statistics(self):
        """Show statistics."""
        stats = self.game_logic.get_game_stats()
        stats_text = f"""
📊 Game Statistics

Games Played: {stats.get('games_played', 0)}
Total Score: {stats.get('total_score', 0)}
Average Score: {stats.get('average_score', 0):.1f}
        """
        messagebox.showinfo("Statistics", stats_text)
    
    def export_data(self):
        """Export comprehensive research data."""
        try:
            files = self.data_collector.export_comprehensive_data()
            messagebox.showinfo("Export Complete", f"Research data exported!\nFiles: {', '.join(files)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def exit_app(self):
        """Exit application."""
        if messagebox.askokcancel("Exit", "Save data and exit?"):
            self.data_collector.save_session()
            self.root.quit()
    
    def run(self):
        """Start the GUI."""
        self.root.mainloop() 