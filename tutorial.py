"""
Tutorial System for Token Quest
Interactive tutorial that explains how to play the game
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os


class TutorialDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎓 Token Quest - Tutorial")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Make it start maximized
        try:
            self.root.state('zoomed')
        except:
            try:
                self.root.attributes('-zoomed', True)
            except:
                pass
        
        # Tutorial state
        self.current_step = 0
        self.total_steps = 7
        
        # Tutorial content
        self.tutorial_steps = [
            {
                'title': '🎯 Welcome to Token Quest!',
                'content': '''Token Quest is a research game that explores how AI language models organize words!

🔬 THE SCIENCE:
• Every word gets converted to "tokens" with unique ID numbers
• Words with similar meanings might have similar token IDs
• Your job is to find words that are close in "token space"

🎮 YOUR MISSION:
• You'll see a target word with its token ID
• Guess a word you think has a similar (or opposite) token ID
• Get points based on how close your guess is!

This helps researchers understand how AI sees language!''',
                'image': '🧠',
                'color': '#2196F3'
            },
            {
                'title': '🎯 Game Modes Explained',
                'content': '''Token Quest has different ways to play:

🎯 CLASSIC MODE:
• Find words with SIMILAR meanings
• Closer token IDs = higher scores
• Example: "happy" and "glad" might have close token IDs

🔄 ANTONYM MODE:
• Find words with OPPOSITE meanings
• Farther token IDs = higher scores  
• Example: "hot" and "cold" should have distant token IDs

📂 CATEGORY MODE:
• All words come from one category (emotions, sizes, etc.)
• Focus on specific types of words

⚡ RANDOM MODE:
• Mix of all modes for variety!''',
                'image': '🎮',
                'color': '#4CAF50'
            },
            {
                'title': '🔢 How Scoring Works',
                'content': '''Understanding the token ID calculation:

📊 THE CALCULATION:
• Target word: "happy" (Token ID: 5432)
• Your guess: "glad" (Token ID: 5500)
• Distance: 5500 - 5432 = 68

🏆 SCORING RANGES:
• Distance 0-1: 10 points (Perfect!)
• Distance 2-100: 9 points (Excellent!)
• Distance 101-500: 8 points (Great!)
• Distance 501-1000: 7 points (Good!)
• Distance 1001-5000: 6 points (Okay!)
• Distance 5001+: 5 points or less

💡 TIP: We always show the larger number minus smaller number so there are no negative numbers!''',
                'image': '🧮',
                'color': '#FF9800'
            },
            {
                'title': '💡 Getting Hints',
                'content': '''Stuck? Use the hint system!

🔍 HINT FEATURES:
• Click "Get Hint" button for help
• Get contextual clues based on word type
• See suggested words with nearby token IDs
• Click suggested words to auto-fill them

📝 HINT EXAMPLES:
• For "happy": "💖 Think of other positive emotions!"
• For "big": "📏 Think of other words meaning large"
• Shows actual words like: "glad", "cheerful", "joyful"

🎯 STRATEGY TIP:
• Use hints to learn patterns
• Notice which words cluster together
• Build your intuition about token relationships!''',
                'image': '💡',
                'color': '#9C27B0'
            },
            {
                'title': '🏆 Leaderboards & Competition',
                'content': '''Compete and track your progress!

📈 LEADERBOARDS:
• Separate rankings for each game mode
• Top 15 players shown
• Track accuracy and high scores
• Export your achievements

🎯 WHAT'S TRACKED:
• Total score across 10 rounds
• Accuracy percentage (correct guesses)
• Best single-round distance
• Game mode and difficulty played

🏅 ACHIEVEMENTS:
• High scores unlock leaderboard entry
• Compare with other players
• See improvement over time
• Export data for research!''',
                'image': '🏆',
                'color': '#FFD700'
            },
            {
                'title': '🎨 Themes & Customization',
                'content': '''Make the game your own!

🌈 AVAILABLE THEMES:
• ☀️ Light: Clean, bright interface
• 🌙 Dark: Easy on the eyes for long sessions
• 💙 Ocean: Calming blue colors
• 🌿 Nature: Relaxing green theme

⚙️ GAME SETTINGS:
• Change modes anytime with Settings button
• Adjust difficulty (Easy/Medium/Hard/Mixed)
• Select specific word categories
• Choose number of rounds (5/10/15/20)

🎮 QUICK ACCESS:
• Settings available in-game
• Quick restart options
• Easy mode switching''',
                'image': '🎨',
                'color': '#E91E63'
            },
            {
                'title': '🚀 Ready to Play!',
                'content': '''You're all set to start your Token Quest adventure!

🎯 QUICK START TIPS:
• Start with Classic mode to learn the basics
• Use hints liberally at first
• Pay attention to which words cluster together
• Try different themes to find your favorite

🔬 RESEARCH IMPACT:
• Your gameplay helps real AI research
• Data helps understand how language models work
• Every game contributes to scientific knowledge

🏆 CHALLENGE YOURSELF:
• Try all game modes
• Aim for the leaderboards
• Experiment with different word categories
• Share your discoveries!

Ready to explore the hidden structure of language? Let's play!''',
                'image': '🚀',
                'color': '#4CAF50'
            }
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the tutorial interface."""
        # Header
        header_frame = tk.Frame(self.root, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=10)
        
        self.title_label = tk.Label(
            header_frame,
            text="🎓 Token Quest Tutorial",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        self.title_label.pack()
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg='#f0f0f0')
        progress_frame.pack(fill='x', padx=40, pady=10)
        
        tk.Label(
            progress_frame,
            text="Tutorial Progress:",
            font=('Arial', 12),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(anchor='w', pady=5)
        
        self.step_label = tk.Label(
            progress_frame,
            text="Step 1 of 7",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666'
        )
        self.step_label.pack(anchor='w')
        
        # Main content area with scrolling
        self.setup_content_area()
        
        # Navigation buttons
        self.setup_navigation()
        
        # Display first step
        self.update_content()
    
    def setup_content_area(self):
        """Setup the scrollable content area."""
        # Create main content frame
        content_container = tk.Frame(self.root, bg='#f0f0f0')
        content_container.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(content_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg='white')
        
        # Configure scrolling
        self.content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrolling components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def setup_navigation(self):
        """Setup navigation buttons."""
        nav_frame = tk.Frame(self.root, bg='#f0f0f0')
        nav_frame.pack(side='bottom', fill='x', pady=20)
        
        button_container = tk.Frame(nav_frame, bg='#f0f0f0')
        button_container.pack()
        
        # Previous button
        self.prev_btn = tk.Button(
            button_container,
            text="◀️ Previous",
            font=('Arial', 12),
            bg='#666',
            fg='white',
            padx=20,
            pady=10,
            command=self.previous_step,
            state='disabled'
        )
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        # Next button
        self.next_btn = tk.Button(
            button_container,
            text="Next ▶️",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            command=self.next_step
        )
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        # Skip tutorial button
        skip_btn = tk.Button(
            button_container,
            text="⚡ Skip Tutorial",
            font=('Arial', 12),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=10,
            command=self.skip_tutorial
        )
        skip_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(
            button_container,
            text="❌ Close",
            font=('Arial', 12),
            bg='#F44336',
            fg='white',
            padx=20,
            pady=10,
            command=self.close_tutorial
        )
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def update_content(self):
        """Update the content area with current step."""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        step = self.tutorial_steps[self.current_step]
        
        # Step title with icon
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill='x', pady=20)
        
        # Large emoji icon
        icon_label = tk.Label(
            title_frame,
            text=step['image'],
            font=('Arial', 48),
            bg='white'
        )
        icon_label.pack()
        
        # Title
        title_label = tk.Label(
            title_frame,
            text=step['title'],
            font=('Arial', 22, 'bold'),
            bg='white',
            fg=step['color']
        )
        title_label.pack(pady=10)
        
        # Content
        content_label = tk.Label(
            self.content_frame,
            text=step['content'],
            font=('Arial', 14),
            bg='white',
            fg='#333',
            wraplength=800,
            justify='left'
        )
        content_label.pack(padx=40, pady=20)
        
        # Update progress
        progress = ((self.current_step + 1) / self.total_steps) * 100
        self.progress_bar['value'] = progress
        self.step_label.config(text=f"Step {self.current_step + 1} of {self.total_steps}")
        
        # Update button states
        self.prev_btn.config(state='normal' if self.current_step > 0 else 'disabled')
        
        if self.current_step == self.total_steps - 1:
            self.next_btn.config(text="🚀 Start Playing!", bg='#4CAF50')
        else:
            self.next_btn.config(text="Next ▶️", bg='#4CAF50')
    
    def next_step(self):
        """Go to next tutorial step."""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_content()
        else:
            # Last step - close tutorial
            self.close_tutorial()
    
    def previous_step(self):
        """Go to previous tutorial step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_content()
    
    def skip_tutorial(self):
        """Skip to the end of tutorial."""
        if messagebox.askyesno("Skip Tutorial", "Are you sure you want to skip the tutorial?"):
            self.close_tutorial()
    
    def close_tutorial(self):
        """Close the tutorial and launch the main game."""
        self.root.destroy()  # Destroy tutorial window
        
        # Import and launch the main game
        try:
            import main
            main.main()  # Start the main game
        except Exception as e:
            print(f"Error launching main game: {e}")
            # Fallback: try to run the game directly
            try:
                import subprocess
                import sys
                import os
                
                # Get the current directory and run main.py
                current_dir = os.path.dirname(os.path.abspath(__file__))
                main_py = os.path.join(current_dir, 'main.py')
                subprocess.Popen([sys.executable, main_py])
            except Exception as e2:
                print(f"Fallback launch also failed: {e2}")
                # Just close tutorial if all else fails
                pass
    
    def run(self):
        """Run the tutorial."""
        self.root.mainloop()


def show_tutorial():
    """Show the tutorial dialog."""
    tutorial = TutorialDialog()
    tutorial.run()


if __name__ == "__main__":
    show_tutorial() 