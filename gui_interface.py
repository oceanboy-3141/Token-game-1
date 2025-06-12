"""
GUI Interface Module
Modern Material Design interface for Token Quest
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import time
from game_logic import GameLogic
from enhanced_data_collector import EnhancedDataCollector
from leaderboard import Leaderboard

# Add tutorial import
try:
    from tutorial import show_tutorial
except ImportError:
    def show_tutorial():
        messagebox.showinfo("Tutorial", "Tutorial system not available.")


class MaterialColors:
    """Material Design 3.0 Color Palette"""
    # Primary colors
    PRIMARY = '#1976D2'
    PRIMARY_LIGHT = '#42A5F5'
    PRIMARY_DARK = '#1565C0'
    
    # Secondary colors
    SECONDARY = '#03DAC6'
    SECONDARY_LIGHT = '#66FFF9'
    SECONDARY_DARK = '#00A896'
    
    # Surface and background
    SURFACE = '#FFFFFF'
    SURFACE_VARIANT = '#F5F5F5'
    BACKGROUND = '#FAFAFA'
    
    # Text colors
    ON_SURFACE = '#1D1B20'
    ON_SURFACE_VARIANT = '#49454F'
    OUTLINE = '#79747E'
    
    # Status colors
    SUCCESS = '#4CAF50'
    WARNING = '#FF9800'
    ERROR = '#F44336'
    INFO = '#2196F3'
    
    # Special colors for game
    TARGET_HIGHLIGHT = '#E3F2FD'
    HINT_BACKGROUND = '#F3E5F5'
    RESULT_EXCELLENT = '#E8F5E8'
    RESULT_GOOD = '#FFF3E0'
    RESULT_NEEDS_WORK = '#FFEBEE'


class MaterialTypography:
    """Material Design Typography Scale"""
    HEADLINE_LARGE = ('Segoe UI', 32, 'bold')
    HEADLINE_MEDIUM = ('Segoe UI', 28, 'bold')
    HEADLINE_SMALL = ('Segoe UI', 24, 'bold')
    
    TITLE_LARGE = ('Segoe UI', 22, 'normal')
    TITLE_MEDIUM = ('Segoe UI', 16, 'bold')
    TITLE_SMALL = ('Segoe UI', 14, 'bold')
    
    BODY_LARGE = ('Segoe UI', 16, 'normal')
    BODY_MEDIUM = ('Segoe UI', 14, 'normal')
    BODY_SMALL = ('Segoe UI', 12, 'normal')
    
    LABEL_LARGE = ('Segoe UI', 14, 'bold')
    LABEL_MEDIUM = ('Segoe UI', 12, 'bold')
    LABEL_SMALL = ('Segoe UI', 11, 'bold')


class TokenGameGUI:
    def __init__(self, researcher_settings=None):
        self.root = tk.Tk()
        self.root.title("Token Quest - Educational Research Edition")
        self.root.geometry("1200x800")
        
        # Store researcher settings
        self.researcher_settings = researcher_settings or {}
        
        # Material Design window setup
        self._setup_window()
        
        # Animation states
        self.animation_queue = []
        self.animation_running = False
        
        # Initialize game components
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
        
        # Window management - keep track of open popups
        self.active_popup = None
        
        # Setup modern UI
        self.setup_material_ui()
        
        # Configure ttk styles
        self._configure_ttk_styles()
    
    def _create_enhanced_data_collector(self):
        """Create an enhanced data collector with automatic comprehensive logging."""
        import os
        
        # Check if researcher mode is enabled with custom folder
        if self.researcher_settings.get('researcher_mode') and self.researcher_settings.get('research_folder'):
            research_folder_name = self.researcher_settings['research_folder']
            print(f"🔬 Researcher Mode ENABLED - Using folder: '{research_folder_name}'")
            print(f"🔍 DEBUG: Full researcher settings: {self.researcher_settings}")
            
            # Try multiple locations for the researcher folder
            possible_paths = [
                # FIRST: Current game directory (where you're looking!)
                os.path.join(os.getcwd(), research_folder_name),
                # SECOND: Game data subdirectory
                os.path.join(os.getcwd(), "research_data", research_folder_name),
                # Desktop location (fallback)
                os.path.join(os.path.expanduser("~"), "Desktop", research_folder_name),
                # Documents location (fallback)
                os.path.join(os.path.expanduser("~"), "Documents", research_folder_name)
            ]
            print(f"🔍 DEBUG: Trying these paths: {possible_paths}")
        else:
            # Default paths for regular users
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
        for i, path in enumerate(possible_paths):
            try:
                print(f"🔍 DEBUG: Trying path {i+1}/{len(possible_paths)}: {path}")
                os.makedirs(path, exist_ok=True)
                # Test write access
                test_file = os.path.join(path, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                research_data_dir = path
                if self.researcher_settings.get('researcher_mode'):
                    print(f"🔬 RESEARCHER MODE: Data directory created at: {research_data_dir}")
                    print(f"📊 ALL game data will be saved IMMEDIATELY to this folder!")
                    print(f"🔍 DEBUG: You should see files appear in: {research_data_dir}")
                else:
                    print(f"✅ Research data directory created: {research_data_dir}")
                break
            except Exception as e:
                print(f"❌ Could not create {path}: {e}")
                continue
        
        if not research_data_dir:
            research_data_dir = "game_data"  # Final fallback
            os.makedirs(research_data_dir, exist_ok=True)
        
        return EnhancedDataCollector(research_data_dir)

    def show_inline_error(self, title: str, message: str):
        """Show an inline error message without disrupting the main window."""
        # Clear any existing feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        # Create error card
        error_card = self.create_material_card(self.feedback_frame, pady=20)
        error_card.pack(fill='x', pady=16)
        error_card.configure(bg='#FFEBEE')  # Light red background
        
        # Error icon and title
        header_frame = tk.Frame(error_card, bg='#FFEBEE')
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=MaterialTypography.TITLE_MEDIUM,
            bg='#FFEBEE',
            fg='#D32F2F'
        )
        title_label.pack()
        
        # Error message
        message_label = tk.Label(
            error_card,
            text=message,
            font=MaterialTypography.BODY_MEDIUM,
            bg='#FFEBEE',
            fg='#B71C1C',
            wraplength=600,
            justify='center'
        )
        message_label.pack(pady=(0, 10))
        
        # Auto-clear after 3 seconds
        self.root.after(3000, lambda: error_card.destroy() if error_card.winfo_exists() else None)
        
        # Focus back to entry
        self.guess_entry.focus()
    
    def show_inline_message(self, title: str, message: str):
        """Show an inline informational message without disrupting the main window."""
        # Clear any existing feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        # Create info card
        info_card = self.create_material_card(self.feedback_frame, pady=20)
        info_card.pack(fill='x', pady=16)
        info_card.configure(bg='#E8F5E8')  # Light green background
        
        # Info icon and title
        header_frame = tk.Frame(info_card, bg='#E8F5E8')
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=MaterialTypography.TITLE_MEDIUM,
            bg='#E8F5E8',
            fg='#2E7D32'
        )
        title_label.pack()
        
        # Info message
        message_label = tk.Label(
            info_card,
            text=message,
            font=MaterialTypography.BODY_MEDIUM,
            bg='#E8F5E8',
            fg='#1B5E20',
            wraplength=600,
            justify='center'
        )
        message_label.pack(pady=(0, 10))

    def _close_active_popup(self):
        """Close any currently active popup window."""
        if self.active_popup and self.active_popup.winfo_exists():
            self.active_popup.destroy()
        self.active_popup = None
    
    def _create_popup(self, title, geometry, bg='white'):
        """Create a new popup window, closing any existing one."""
        self._close_active_popup()
        
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(geometry)
        popup.configure(bg=bg)
        popup.transient(self.root)
        popup.grab_set()
        
        self.active_popup = popup
        
        # Bind close event to clear reference
        def on_close():
            self.active_popup = None
            popup.destroy()
        
        popup.protocol("WM_DELETE_WINDOW", on_close)
        
        return popup
    
    def show_achievement_notification(self, achievement):
        """Show a notification when an achievement is unlocked."""
        notification = tk.Toplevel(self.root)
        notification.title("🎖️ Achievement Unlocked!")
        notification.geometry("400x200")
        notification.configure(bg='#4CAF50')
        notification.transient(self.root)
        notification.attributes("-topmost", True)
        
        # Position in top-right corner
        notification.geometry("+{}+{}".format(
            self.root.winfo_rootx() + self.root.winfo_width() - 420,
            self.root.winfo_rooty() + 20
        ))
        
        # Content
        tk.Label(
            notification,
            text="🎖️ ACHIEVEMENT UNLOCKED! 🎖️",
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=10)
        
        tk.Label(
            notification,
            text=f"{achievement.icon} {achievement.name}",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=5)
        
        tk.Label(
            notification,
            text=achievement.description,
            font=('Arial', 11),
            bg='#4CAF50',
            fg='white',
            wraplength=350,
            justify='center'
        ).pack(pady=5)
        
        # Auto-close after 4 seconds
        notification.after(4000, notification.destroy)
        
        # Add click to close
        def close_notification(event=None):
            notification.destroy()
        
        notification.bind("<Button-1>", close_notification)
        for widget in notification.winfo_children():
            widget.bind("<Button-1>", close_notification)
    
    def _setup_window(self):
        """Configure the main window with material design principles."""
        # Modern window appearance
        self.root.configure(bg=MaterialColors.BACKGROUND)
        
        # Make responsive - start maximized on larger screens
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if screen_width >= 1400 and screen_height >= 900:
            try:
                self.root.state('zoomed')
            except:
                try:
                    self.root.attributes('-zoomed', True)
                except:
                    # Fallback to large window
                    self.root.geometry("1400x900")
        
        # Modern window icon and properties
        self.root.resizable(True, True)
        self.root.minsize(800, 600)  # Minimum responsive size
    
    def _configure_ttk_styles(self):
        """Configure modern ttk widget styles."""
        style = ttk.Style()
        
        # Configure progress bar styles with material colors
        style.configure(
            'Material.Horizontal.TProgressbar',
            background=MaterialColors.PRIMARY,
            troughcolor=MaterialColors.SURFACE_VARIANT,
            borderwidth=0,
            lightcolor=MaterialColors.PRIMARY_LIGHT,
            darkcolor=MaterialColors.PRIMARY_DARK
        )
        
        # Configure modern button style
        style.configure(
            'Material.TButton',
            font=MaterialTypography.LABEL_MEDIUM,
            padding=(16, 8)
        )
        
        # Configure notebook style
        style.configure(
            'Material.TNotebook',
            background=MaterialColors.SURFACE,
            borderwidth=0
        )
        
        style.configure(
            'Material.TNotebook.Tab',
            font=MaterialTypography.LABEL_MEDIUM,
            padding=(12, 8)
        )
    
    def create_material_card(self, parent, **kwargs):
        """Create a material design card with elevation effect."""
        card = tk.Frame(
            parent,
            bg=kwargs.get('bg', MaterialColors.SURFACE),
            relief='flat',
            bd=0,
            padx=kwargs.get('padx', 24),
            pady=kwargs.get('pady', 16)
        )
        
        # Add subtle shadow effect using additional frames
        shadow_frame = tk.Frame(
            parent,
            bg='#E0E0E0',  # Light shadow color
            height=2
        )
        
        return card
    
    def create_material_button(self, parent, text, command, style='primary', **kwargs):
        """Create a material design button with proper styling."""
        if style == 'primary':
            bg_color = MaterialColors.PRIMARY
            fg_color = MaterialColors.SURFACE
            hover_color = MaterialColors.PRIMARY_LIGHT
        elif style == 'secondary':
            bg_color = MaterialColors.SECONDARY
            fg_color = MaterialColors.ON_SURFACE
            hover_color = MaterialColors.SECONDARY_LIGHT
        elif style == 'success':
            bg_color = MaterialColors.SUCCESS
            fg_color = MaterialColors.SURFACE
            hover_color = '#66BB6A'
        elif style == 'warning':
            bg_color = MaterialColors.WARNING
            fg_color = MaterialColors.SURFACE
            hover_color = '#FFB74D'
        else:
            bg_color = MaterialColors.SURFACE_VARIANT
            fg_color = MaterialColors.ON_SURFACE
            hover_color = '#EEEEEE'
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=kwargs.get('font', MaterialTypography.LABEL_MEDIUM),
            bg=bg_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=fg_color,
            relief='flat',
            borderwidth=0,
            padx=kwargs.get('padx', 24),
            pady=kwargs.get('pady', 12),
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(e):
            btn.configure(bg=hover_color)
        
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def setup_material_ui(self):
        """Setup the main user interface with Material Design principles."""
        
        # Create main container with proper spacing
        main_container = tk.Frame(self.root, bg=MaterialColors.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=32, pady=24)
        
        # Header section with app title
        header_card = self.create_material_card(main_container, pady=20)
        header_card.pack(fill='x', pady=(0, 24))
        
        # App title with modern typography
        title_label = tk.Label(
            header_card,
            text="🎯 Token Quest",
            font=MaterialTypography.HEADLINE_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_card,
            text="Explore semantic relationships through tokenization • Educational Research Edition",
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Stats section with material cards
        stats_container = tk.Frame(main_container, bg=MaterialColors.BACKGROUND)
        stats_container.pack(fill='x', pady=(0, 24))
        
        # Create three stat cards in a row
        stats_row = tk.Frame(stats_container, bg=MaterialColors.BACKGROUND)
        stats_row.pack(fill='x')
        
        # Score card
        score_card = self.create_material_card(stats_row, padx=16, pady=12)
        score_card.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        tk.Label(
            score_card,
            text="SCORE",
            font=MaterialTypography.LABEL_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack()
        
        self.score_label = tk.Label(
            score_card,
            text="0",
            font=MaterialTypography.HEADLINE_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.SUCCESS
        )
        self.score_label.pack()
        
        # Round card
        round_card = self.create_material_card(stats_row, padx=16, pady=12)
        round_card.pack(side='left', fill='x', expand=True, padx=(8, 8))
        
        tk.Label(
            round_card,
            text="ROUND",
            font=MaterialTypography.LABEL_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack()
        
        self.round_label = tk.Label(
            round_card,
            text="1 / 10",
            font=MaterialTypography.HEADLINE_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.PRIMARY
        )
        self.round_label.pack()
        
        # Accuracy card
        accuracy_card = self.create_material_card(stats_row, padx=16, pady=12)
        accuracy_card.pack(side='left', fill='x', expand=True, padx=(8, 0))
        
        tk.Label(
            accuracy_card,
            text="CORRECT",
            font=MaterialTypography.LABEL_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack()
        
        self.accuracy_label = tk.Label(
            accuracy_card,
            text="0",
            font=MaterialTypography.HEADLINE_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.SUCCESS
        )
        self.accuracy_label.pack()
        
        # Progress bars in a dedicated card
        progress_card = self.create_material_card(main_container, pady=20)
        progress_card.pack(fill='x', pady=(0, 24))
        
        tk.Label(
            progress_card,
            text="Progress Tracking",
            font=MaterialTypography.TITLE_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE
        ).pack(anchor='w')
        
        # Game progress
        progress_frame1 = tk.Frame(progress_card, bg=MaterialColors.SURFACE)
        progress_frame1.pack(fill='x', pady=(12, 8))
        
        tk.Label(
            progress_frame1,
            text="Game Progress",
            font=MaterialTypography.BODY_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack(anchor='w')
        
        self.round_progress = ttk.Progressbar(
            progress_frame1,
            length=300,
            mode='determinate',
            style='Material.Horizontal.TProgressbar'
        )
        self.round_progress.pack(anchor='w', pady=(4, 0), fill='x')
        
        # Round attempts progress  
        progress_frame2 = tk.Frame(progress_card, bg=MaterialColors.SURFACE)
        progress_frame2.pack(fill='x', pady=(8, 0))
        
        tk.Label(
            progress_frame2,
            text="Round Attempts",
            font=MaterialTypography.BODY_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack(anchor='w')
        
        self.attempts_progress = ttk.Progressbar(
            progress_frame2,
            length=300,
            mode='determinate',
            style='Material.Horizontal.TProgressbar'
        )
        self.attempts_progress.pack(anchor='w', pady=(4, 0), fill='x')
        
        # Target word section - hero card
        target_card = self.create_material_card(main_container, pady=32)
        target_card.pack(fill='x', pady=(0, 24))
        
        tk.Label(
            target_card,
            text="Target Word",
            font=MaterialTypography.TITLE_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack()
        
        # Target word with enhanced styling
        self.target_word_label = tk.Label(
            target_card,
            text="...",
            font=MaterialTypography.HEADLINE_LARGE,
            bg=MaterialColors.TARGET_HIGHLIGHT,
            fg=MaterialColors.PRIMARY,
            padx=32,
            pady=16
        )
        self.target_word_label.pack(pady=(16, 8))
        
        self.target_info_label = tk.Label(
            target_card,
            text="Token ID: ...",
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        )
        self.target_info_label.pack()
        
        # Input section card
        input_card = self.create_material_card(main_container, pady=24)
        input_card.pack(fill='x', pady=(0, 24))
        
        tk.Label(
            input_card,
            text="Your Guess",
            font=MaterialTypography.TITLE_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE
        ).pack()
        
        # Modern input field with enhanced styling
        input_frame = tk.Frame(input_card, bg=MaterialColors.SURFACE)
        input_frame.pack(pady=(16, 0))
        
        self.guess_entry = tk.Entry(
            input_frame,
            font=MaterialTypography.BODY_LARGE,
            width=25,
            justify='center',
            relief='flat',
            bd=2,
            highlightthickness=2,
            highlightcolor=MaterialColors.PRIMARY
        )
        self.guess_entry.pack(pady=8)
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())
        
        # Action buttons with material design
        button_card = self.create_material_card(main_container, pady=20)
        button_card.pack(fill='x', pady=(0, 24))
        
        button_container = tk.Frame(button_card, bg=MaterialColors.SURFACE)
        button_container.pack()
        
        # Primary action button
        self.submit_btn = self.create_material_button(
            button_container,
            "Submit Guess",
            self.submit_guess,
            style='primary',
            font=MaterialTypography.LABEL_LARGE
        )
        self.submit_btn.pack(side='left', padx=(0, 12))
        
        # Secondary action buttons
        self.hint_btn = self.create_material_button(
            button_container,
            "💡 Get Hint",
            self.show_hint,
            style='secondary',
            font=MaterialTypography.LABEL_MEDIUM
        )
        self.hint_btn.pack(side='left', padx=(12, 12))
        
        self.next_btn = self.create_material_button(
            button_container,
            "Next Round",
            self.start_new_round,
            style='outline',
            font=MaterialTypography.LABEL_MEDIUM
        )
        self.next_btn.pack(side='left', padx=(12, 12))
        
        self.settings_btn = self.create_material_button(
            button_container,
            "⚙️ Settings",
            self.show_game_settings,
            style='outline',
            font=MaterialTypography.LABEL_MEDIUM
        )
        self.settings_btn.pack(side='left', padx=(12, 0))
        
        # Feedback area with scrolling (initially hidden)
        feedback_outer = tk.Frame(main_container, bg=MaterialColors.BACKGROUND)
        feedback_outer.pack(fill='x', pady=(0, 24))
        
        # Create scrollable feedback area
        feedback_canvas = tk.Canvas(
            feedback_outer, 
            bg=MaterialColors.BACKGROUND,
            highlightthickness=0,
            height=300  # Max height before scrolling - reduced for better visibility
        )
        feedback_scrollbar = ttk.Scrollbar(feedback_outer, orient="vertical", command=feedback_canvas.yview)
        self.feedback_frame = tk.Frame(feedback_canvas, bg=MaterialColors.BACKGROUND)
        
        self.feedback_frame.bind(
            "<Configure>",
            lambda e: feedback_canvas.configure(scrollregion=feedback_canvas.bbox("all"))
        )
        
        feedback_canvas.create_window((0, 0), window=self.feedback_frame, anchor="nw")
        feedback_canvas.configure(yscrollcommand=feedback_scrollbar.set)
        
        feedback_canvas.pack(side="left", fill="both", expand=True)
        feedback_scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            feedback_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        feedback_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Setup modern menu
        self._setup_material_menu()
    
    def _setup_material_menu(self):
        """Setup a modern menu bar with material design styling."""
        menubar = tk.Menu(self.root, bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE)
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0, bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="🎮 New Game", command=self.new_game)
        game_menu.add_command(label="⚙️ Game Settings", command=self.show_game_settings)
        game_menu.add_separator()
        game_menu.add_command(label="🎓 Tutorial", command=self.show_tutorial)
        game_menu.add_separator()
        game_menu.add_command(label="🏆 Leaderboard", command=self.show_leaderboard)
        game_menu.add_command(label="🎖️ Achievements", command=self.show_achievements)
        game_menu.add_command(label="📊 Statistics", command=self.show_statistics)
        game_menu.add_command(label="📤 Export Data", command=self.export_data)
        game_menu.add_separator()
        game_menu.add_command(label="❌ Exit", command=self.root.quit)
    
    def smooth_color_transition(self, widget, start_color, end_color, duration=200, steps=10):
        """Create a smooth color transition animation."""
        if self.animation_running:
            return
        
        self.animation_running = True
        
        # Parse RGB values
        start_rgb = self._hex_to_rgb(start_color)
        end_rgb = self._hex_to_rgb(end_color)
        
        step_delay = duration // steps
        
        def animate_step(step):
            if step <= steps:
                # Calculate interpolated color
                progress = step / steps
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress)
                
                color = f'#{r:02x}{g:02x}{b:02x}'
                widget.configure(bg=color)
                
                self.root.after(step_delay, lambda: animate_step(step + 1))
            else:
                self.animation_running = False
        
        animate_step(0)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def animate_feedback_entry(self, widget):
        """Animate feedback appearance with smooth entry."""
        original_height = widget.winfo_reqheight()
        widget.configure(height=0)
        
        def expand_step(current_height):
            if current_height < original_height:
                new_height = min(current_height + 5, original_height)
                widget.configure(height=new_height)
                self.root.after(10, lambda: expand_step(new_height))
        
        expand_step(0)
    
    def pulse_animation(self, widget, scale_factor=1.1, duration=300):
        """Create a subtle pulse animation for important elements."""
        try:
            original_font = widget.cget('font')
            
            if isinstance(original_font, str):
                # Handle string font - more robust parsing
                if original_font.startswith('{') and original_font.endswith('}'):
                    # Handle tuple-like string format
                    original_font = original_font.strip('{}').replace("'", "").split()
                    font_family = original_font[0] if original_font else 'Segoe UI'
                    font_size = int(original_font[1]) if len(original_font) > 1 and original_font[1].isdigit() else 12
                else:
                    # Handle space-separated format
                    font_parts = original_font.split()
                    font_family = font_parts[0] if font_parts else 'Segoe UI'
                    # Look for numeric part
                    font_size = 12
                    for part in font_parts:
                        if part.isdigit():
                            font_size = int(part)
                            break
            else:
                # Handle tuple font
                font_family = original_font[0] if original_font and len(original_font) > 0 else 'Segoe UI'
                font_size = original_font[1] if original_font and len(original_font) > 1 else 12
            
            larger_size = int(font_size * scale_factor)
            larger_font = (font_family, larger_size, 'bold')
            
            # Grow
            widget.configure(font=larger_font)
            
            # Shrink back after duration
            self.root.after(duration, lambda: widget.configure(font=original_font))
        except Exception as e:
            # Fallback: just skip animation if there's any font parsing issue
            pass
    
    def start_new_round(self):
        """Start a new round of the game."""
        if not self.game_logic:
            return
        
        # Track game started for achievements (only on first round)
        if hasattr(self.game_logic, 'current_round') and self.game_logic.current_round == 1:
            if self.achievement_manager:
                new_achievements = self.achievement_manager.track_game_event("game_started")
                for achievement in new_achievements:
                    self.show_achievement_notification(achievement)
                    print(f"🏆 Achievement unlocked: {achievement.name}")
        
        round_info = self.game_logic.start_new_round()
        
        if 'error' in round_info or round_info.get('game_ended', False):
            self.show_final_results(round_info)
            return
        
        # Update UI
        self.target_word_label.config(
            text=round_info['target_word'].upper(),
            fg=MaterialColors.PRIMARY,
            bg=MaterialColors.TARGET_HIGHLIGHT
        )
        
        self.target_info_label.config(text=f"Token ID: {round_info['target_token_id']}")
        self.round_label.config(text=f"{round_info['current_round']} / {round_info['max_rounds']}")
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state='normal')
        self.submit_btn.config(state='normal', text="Submit Guess")
        
        # Clear previous feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        # Update progress bars
        self.update_progress_bars(round_info)
        
        # Update next button
        if round_info['current_round'] < round_info['max_rounds']:
            self.next_btn.config(text="Skip Round", state='normal')
        
        print(f"🎯 Round {round_info['current_round']} started: {round_info['target_word']}")
        self.current_round_active = True
    
    def update_progress_bars(self, round_info=None):
        """Update progress bars to show game and round progress."""
        if round_info:
            # Update game progress
            game_progress = (round_info['current_round'] / round_info['max_rounds']) * 100
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
            self.show_inline_error("⚠️ No Active Round", "Please start a new round first!")
            return
        
        guess = self.guess_entry.get().strip()
        if not guess:
            self.show_inline_error("⚠️ Empty Guess", "Please enter a word!")
            return
        
        result = self.game_logic.submit_guess(guess)
        
        if result['valid_guess']:
            # Track achievement events
            if self.achievement_manager:
                # Track word tried
                self.achievement_manager.track_game_event("word_tried", word=guess)
                
                # Track guess accuracy
                feedback = result['feedback']
                is_first_attempt = result.get('attempts_used', 1) == 1
                
                if feedback['is_correct']:
                    if result['distance'] <= 1:
                        new_achievements = self.achievement_manager.track_game_event("perfect_guess", first_guess_of_round=is_first_attempt)
                    else:
                        new_achievements = self.achievement_manager.track_game_event("excellent_guess")
                else:
                    new_achievements = self.achievement_manager.track_game_event("incorrect_guess")
                
                # Show achievement notifications
                for achievement in new_achievements:
                    self.show_achievement_notification(achievement)
            
            # Valid guess - show results
            self.show_guess_result(result)
            
            # Log data for research
            self.data_collector.log_comprehensive_guess(result)
            
            # Update score display
            self.score_label.config(text=str(result['total_score']))
            
            # Update accuracy display
            self.accuracy_label.config(text=str(self.game_logic.correct_guesses))
            
            # Update progress bars
            self.update_progress_bars()
            
            # Clear the guess entry
            self.guess_entry.delete(0, tk.END)
            
            # SIMPLIFIED AUTO-ADVANCE LOGIC - Check if max attempts reached or word is correct
            if result.get('max_attempts_reached') or result['feedback']['is_correct']:
                print(f"🔄 Auto-advancing: max_attempts={result.get('max_attempts_reached')}, correct={result['feedback']['is_correct']}")
                # Show a brief inline message and auto-advance
                if result.get('max_attempts_reached'):
                    self.show_inline_message("🔄 Round Complete", f"3 attempts used! Moving to next word...\nAttempts used: {result.get('attempts_used', 0)}")
                else:
                    self.show_inline_message("🎉 Correct!", "Great job! Moving to next word...")
                
                # Auto-advance after brief delay to show message
                self.root.after(1500, self.start_new_round)
                return
            
            # Check if this was the last round
            if result['current_round'] >= result['max_rounds']:
                # Enable "Next Round" button to show final results
                self.next_btn.config(text="View Results", bg='#4CAF50')
            
        else:
            # Invalid guess - check if max attempts reached
            if result.get('max_attempts_reached'):
                print(f"🔄 Invalid guess but max attempts reached: {result.get('attempts_used', 0)}")
                self.show_inline_message("🔄 Round Complete", f"3 attempts used! Moving to next word...\nAttempts used: {result.get('attempts_used', 0)}")
                # Auto advance after showing message briefly
                self.root.after(1500, self.start_new_round)
            else:
                self.show_inline_error("❌ Invalid Guess", result['error'])
            return
    
    def show_guess_result(self, result):
        """Display the result of a guess with enhanced material design feedback and animations."""
        # Clear previous feedback
        for widget in self.feedback_frame.winfo_children():
            widget.destroy()
        
        feedback = result['feedback']
        
        # Animate target word feedback with smooth color transition
        feedback_color = feedback['color']
        self.smooth_color_transition(
            self.target_word_label, 
            MaterialColors.TARGET_HIGHLIGHT, 
            feedback_color,
            duration=300
        )
        
        # Update target word with animated feedback
        self.target_word_label.config(
            text=feedback['result'],
            fg=MaterialColors.SURFACE
        )
        
        # Pulse animation for the target word
        self.pulse_animation(self.target_word_label, scale_factor=1.15, duration=500)
        
        # Create material design result card
        result_card = self.create_material_card(self.feedback_frame, pady=24)
        result_card.pack(fill='x', pady=16)
        
        # Determine result styling based on feedback
        if feedback['is_correct']:
            card_bg = MaterialColors.RESULT_EXCELLENT
            accent_color = MaterialColors.SUCCESS
        elif 'CLOSE' in feedback['result']:
            card_bg = MaterialColors.RESULT_GOOD  
            accent_color = MaterialColors.WARNING
        else:
            card_bg = MaterialColors.RESULT_NEEDS_WORK
            accent_color = MaterialColors.ERROR
        
        result_card.configure(bg=card_bg)
        
        # Result header with material typography
        header_frame = tk.Frame(result_card, bg=card_bg)
        header_frame.pack(fill='x', pady=(0, 16))
        
        feedback_label = tk.Label(
            header_frame,
            text=feedback['message'],
            font=MaterialTypography.TITLE_LARGE,
            bg=card_bg,
            fg=accent_color
        )
        feedback_label.pack()
        
        # Token Space Visualization with enhanced styling
        if 'guess_token_id' in result and 'target_token_id' in result:
            self.create_material_token_visualization(result_card, result, bg_color=card_bg)
        
        # Detailed info with modern card design
        info_card = tk.Frame(result_card, bg=MaterialColors.SURFACE, relief='flat', bd=0)
        info_card.pack(fill='x', padx=16, pady=8)
        
        # Score and calculation info
        guess_id = result['guess_token_id']
        target_id = result['target_token_id']
        larger_id = max(guess_id, target_id)
        smaller_id = min(guess_id, target_id)
        
        tk.Label(
            info_card,
            text=f"Your word: {result['guess_word']}",
            font=MaterialTypography.BODY_LARGE,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE
        ).pack(pady=(12, 4))
        
        tk.Label(
            info_card,
            text=f"Token ID: {guess_id} • Distance: {result['distance']} • Score: +{result['round_score']}",
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE_VARIANT
        ).pack(pady=(0, 12))
        
        # Educational explanation with material design
        if 'educational_explanation' in result:
            edu_card = tk.Frame(result_card, bg=MaterialColors.HINT_BACKGROUND, relief='flat', bd=0)
            edu_card.pack(fill='x', padx=16, pady=8)
            
            tk.Label(
                edu_card,
                text="🧠 Educational Insight",
                font=MaterialTypography.TITLE_SMALL,
                bg=MaterialColors.HINT_BACKGROUND,
                fg=MaterialColors.ON_SURFACE
            ).pack(anchor='w', padx=16, pady=(12, 8))
            
            tk.Label(
                edu_card,
                text=result['educational_explanation'],
                font=MaterialTypography.BODY_MEDIUM,
                bg=MaterialColors.HINT_BACKGROUND,
                fg=MaterialColors.ON_SURFACE_VARIANT,
                wraplength=600,
                justify='left'
            ).pack(anchor='w', padx=16, pady=(0, 12))
        
        # Token fact with modern styling and enhanced visibility
        if 'token_fact' in result:
            fact_card = tk.Frame(result_card, bg='#E8F5E8', relief='solid', bd=2)  # More visible background
            fact_card.pack(fill='x', padx=16, pady=12)
            
            # Enhanced header with more emphasis
            tk.Label(
                fact_card,
                text="💡 Did You Know? (Educational Fact)",
                font=MaterialTypography.TITLE_MEDIUM,  # Larger font
                bg='#E8F5E8',
                fg=MaterialColors.SUCCESS
            ).pack(anchor='w', padx=16, pady=(16, 8))
            
            tk.Label(
                fact_card,
                text=result['token_fact'],
                font=MaterialTypography.BODY_LARGE,  # Larger font for fact
                bg='#E8F5E8',
                fg=MaterialColors.ON_SURFACE,
                wraplength=600,
                justify='left'
            ).pack(anchor='w', padx=16, pady=(0, 16))
        
        # Animate the result card entry
        self.animate_feedback_entry(result_card)
        
        # Schedule to reset target word display with smooth transition (much faster)
        self.root.after(1000, lambda: self.reset_target_display_smooth())
    
    def create_material_token_visualization(self, parent, result, bg_color):
        """Create a modern material design token space visualization."""
        vis_card = tk.Frame(parent, bg=MaterialColors.SURFACE, relief='flat', bd=0)
        vis_card.pack(fill='x', padx=16, pady=8)
        
        tk.Label(
            vis_card,
            text="📊 Token Space Visualization",
            font=MaterialTypography.TITLE_SMALL,
            bg=MaterialColors.SURFACE,
            fg=MaterialColors.ON_SURFACE
        ).pack(pady=(12, 8))
        
        # Get visualization data
        if hasattr(self.game_logic, 'token_handler'):
            viz_data = self.game_logic.token_handler.get_token_visualization_data(
                result.get('target_token_id', 0),
                result.get('guess_token_id', 0)
            )
            
            # Create canvas for visualization with modern styling
            canvas = tk.Canvas(
                vis_card, 
                height=100, 
                bg=MaterialColors.SURFACE,
                highlightthickness=0,
                relief='flat'
            )
            canvas.pack(fill='x', padx=16, pady=(0, 12))
            
            # Draw token visualization after a short delay with animation
            canvas.after(200, lambda: self.draw_material_token_space(canvas, viz_data))
    
    def draw_material_token_space(self, canvas, viz_data):
        """Draw a modern material design token space visualization."""
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1:  # Canvas not ready, try again
            canvas.after(100, lambda: self.draw_material_token_space(canvas, viz_data))
            return
        
        # Clear canvas
        canvas.delete("all")
        
        # Calculate positions
        target_id = viz_data['target_id']
        guess_id = viz_data['guess_id']
        vis_range = viz_data['visualization_range']
        range_size = vis_range[1] - vis_range[0]
        
        if range_size == 0:
            return
        
        # Material design spacing and positioning
        margin = width * 0.08
        usable_width = width - (2 * margin)
        
        target_x = margin + ((target_id - vis_range[0]) / range_size) * usable_width
        guess_x = margin + ((guess_id - vis_range[0]) / range_size) * usable_width
        
        # Draw modern timeline base
        canvas.create_line(
            margin, height//2, 
            width-margin, height//2, 
            width=3, 
            fill=MaterialColors.OUTLINE,
            capstyle='round'
        )
        
        # Draw target with material design styling
        canvas.create_oval(
            target_x-10, height//2-10, 
            target_x+10, height//2+10, 
            fill=MaterialColors.PRIMARY,
            outline=MaterialColors.PRIMARY_DARK, 
            width=2
        )
        
        canvas.create_text(
            target_x, height//2-25, 
            text='🎯 Target', 
            font=MaterialTypography.BODY_SMALL,
            fill=MaterialColors.PRIMARY
        )
        
        # Draw guess with color based on distance category
        distance_category = viz_data['distance_category']
        color_map = {
            'perfect': MaterialColors.SUCCESS,
            'excellent': MaterialColors.SUCCESS,
            'good': MaterialColors.WARNING,
            'moderate': MaterialColors.WARNING,
            'far': MaterialColors.ERROR,
            'very_far': MaterialColors.ERROR
        }
        guess_color = color_map.get(distance_category, MaterialColors.ERROR)
        
        canvas.create_oval(
            guess_x-8, height//2-8, 
            guess_x+8, height//2+8, 
            fill=guess_color,
            outline=MaterialColors.ON_SURFACE, 
            width=2
        )
        
        canvas.create_text(
            guess_x, height//2+25, 
            text='Your Guess', 
            font=MaterialTypography.BODY_SMALL,
            fill=MaterialColors.ON_SURFACE
        )
        
        # Draw animated distance line if positions are different
        if abs(target_x - guess_x) > 15:  
            canvas.create_line(
                target_x, height//2, 
                guess_x, height//2, 
                width=2, 
                fill=MaterialColors.SECONDARY,
                dash=(8, 4)
            )
            
            # Distance label with modern styling
            mid_x = (target_x + guess_x) / 2
            canvas.create_text(
                mid_x, height//2-12, 
                text=f'Distance: {viz_data["distance"]}', 
                font=MaterialTypography.LABEL_MEDIUM,
                fill=MaterialColors.SECONDARY
            )
        
        # Add range indicators with subtle styling
        canvas.create_text(
            margin, height-12, 
            text=str(vis_range[0]), 
            font=MaterialTypography.BODY_SMALL,
            fill=MaterialColors.ON_SURFACE_VARIANT
        )
        
        canvas.create_text(
            width-margin, height-12, 
            text=str(vis_range[1]), 
            font=MaterialTypography.BODY_SMALL,
            fill=MaterialColors.ON_SURFACE_VARIANT
        )
    
    def reset_target_display_smooth(self):
        """Reset the target word display with smooth color transition."""
        if hasattr(self, 'game_logic') and self.game_logic.current_target_word:
            # Smooth transition back to original colors
            self.smooth_color_transition(
                self.target_word_label,
                self.target_word_label.cget('bg'),
                MaterialColors.TARGET_HIGHLIGHT,
                duration=400
            )
            
            # Reset text and styling
            self.root.after(400, lambda: self.target_word_label.config(
                text=self.game_logic.current_target_word.upper(),
                fg=MaterialColors.PRIMARY
            ))
    
    def show_hint(self):
        """Show enhanced hint with contextual suggestions and progressive revelation."""
        hint_data = self.game_logic.get_hint()
        
        if 'error' in hint_data:
            self.show_inline_error("💡 No Hint Available", hint_data['error'])
            return
        
        # Track hint viewed for achievements
        if self.achievement_manager:
            new_achievements = self.achievement_manager.track_game_event("hint_viewed")
            for achievement in new_achievements:
                self.show_achievement_notification(achievement)
        
        # Create enhanced hint popup
        hint_window = self._create_popup("💡 Enhanced Hint System", "600x550", '#f9f9f9')
        
        # Title
        tk.Label(
            hint_window,
            text=f"Hints for: {hint_data['target_word'].upper()}",
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
            wraplength=550,
            fg='#333'
        ).pack(pady=10)
        
        # Create notebook for different hint types
        notebook = ttk.Notebook(hint_window)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Semantic Hints Tab
        semantic_frame = tk.Frame(notebook, bg='#f0f8ff')
        notebook.add(semantic_frame, text="🧠 Semantic Hints")
        
        tk.Label(
            semantic_frame,
            text="Words with similar meanings:",
            font=('Arial', 11, 'bold'),
            bg='#f0f8ff',
            fg='#333'
        ).pack(pady=10)
        
        if hint_data['semantic_hints']:
            semantic_words_frame = tk.Frame(semantic_frame, bg='#f0f8ff')
            semantic_words_frame.pack(pady=5)
            
            for i, word in enumerate(hint_data['semantic_hints'][:6]):
                word_btn = tk.Button(
                    semantic_words_frame,
                    text=word,
                    font=('Arial', 10),
                    bg='#e8f5e8',
                    fg='#2c5e2c',
                    relief='raised',
                    padx=8,
                    pady=2,
                    command=lambda w=word: self.insert_hint_word(w, hint_window)
                )
                word_btn.grid(row=i//3, column=i%3, padx=5, pady=2)
        else:
            tk.Label(
                semantic_frame,
                text="No semantic hints available for this word.",
                font=('Arial', 10, 'italic'),
                bg='#f0f8ff',
                fg='#666'
            ).pack(pady=10)
        
        # Token-Based Hints Tab
        token_frame = tk.Frame(notebook, bg='#fff8f0')
        notebook.add(token_frame, text="🔢 Token Space Hints")
        
        tk.Label(
            token_frame,
            text="Words with nearby token IDs:",
            font=('Arial', 11, 'bold'),
            bg='#fff8f0',
            fg='#333'
        ).pack(pady=10)
        
        tk.Label(
            token_frame,
            text=hint_data['token_range'],
            font=('Arial', 10),
            bg='#fff8f0',
            fg='#666'
        ).pack(pady=5)
        
        if hint_data['token_hints']:
            token_words_frame = tk.Frame(token_frame, bg='#fff8f0')
            token_words_frame.pack(pady=5)
            
            for i, word in enumerate(hint_data['token_hints'][:6]):
                word_btn = tk.Button(
                    token_words_frame,
                    text=word,
                    font=('Arial', 10),
                    bg='#f0f8ff',
                    fg='#2c5e8c',
                    relief='raised',
                    padx=8,
                    pady=2,
                    command=lambda w=word: self.insert_hint_word(w, hint_window)
                )
                word_btn.grid(row=i//3, column=i%3, padx=5, pady=2)
        
        # Educational Tab
        edu_frame = tk.Frame(notebook, bg='#f8f0ff')
        notebook.add(edu_frame, text="📚 Learn About Tokens")
        
        tk.Label(
            edu_frame,
            text="💡 Token Education",
            font=('Arial', 12, 'bold'),
            bg='#f8f0ff',
            fg='#2c2c5e'
        ).pack(pady=10)
        
        tk.Label(
            edu_frame,
            text=hint_data['token_fact'],
            font=('Arial', 10),
            bg='#f8f0ff',
            fg='#333',
            wraplength=500,
            justify='left'
        ).pack(pady=10, padx=20)
        
        # Add detailed token information
        nearby_data = hint_data.get('nearby_words_data', [])
        if nearby_data:
            tk.Label(
                edu_frame,
                text="🔍 Nearby Token Analysis:",
                font=('Arial', 10, 'bold'),
                bg='#f8f0ff',
                fg='#2c2c5e'
            ).pack(pady=(10,5))
            
            analysis_text = ""
            for word_data in nearby_data[:3]:
                analysis_text += f"• '{word_data['word']}' (ID: {word_data['token_id']}, Distance: {word_data['distance']})\n"
            
            tk.Label(
                edu_frame,
                text=analysis_text,
                font=('Arial', 9),
                bg='#f8f0ff',
                fg='#333',
                justify='left'
            ).pack(pady=5, padx=20)
        
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
        ).pack(pady=10)
    
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
            # Track tutorial completion for achievements
            if self.achievement_manager:
                new_achievements = self.achievement_manager.track_game_event("tutorial_completed")
                for achievement in new_achievements:
                    self.show_achievement_notification(achievement)
        except Exception as e:
            messagebox.showerror("Tutorial Error", f"Could not start tutorial: {e}")
    
    def show_game_settings(self):
        """Show game settings dialog for mode, difficulty, and category selection."""
        settings_window = self._create_popup("🎮 Game Settings", "500x600", '#f0f0f0')
        
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
        self.root.title(f"Token Quest - Educational Research Edition{mode_text}")
        
        # Close settings window
        settings_window.destroy()
        
        # Start a new game with new settings
        if messagebox.askyesno("New Game", "Settings applied! Start a new game with these settings?"):
            self.new_game()
    
    def show_leaderboard(self):
        """Show the leaderboard window."""
        leaderboard_window = self._create_popup("🏆 Leaderboard", "700x500", '#f0f0f0')
        
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
    
    def show_achievements(self):
        """Show the achievements window."""
        try:
            if not self.achievement_manager:
                messagebox.showinfo("Achievements", "Achievement system not available.")
                return
                
            # Create achievements window
            achievements_window = self._create_popup("🎖️ Token Quest Achievements", "900x700", '#f0f0f0')
            
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
            stats = self.achievement_manager.get_stats_summary()
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
                ('test', '🧪 Test'),
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
                achievements = self.achievement_manager.get_achievements_by_category(category_id)
                
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
        # Temporarily release grab to avoid conflict with simpledialog
        results_window.grab_release()
        
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
            self.data_collector = self._create_enhanced_data_collector()  # New session
            
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
            # Use the enhanced data collector's export method
            exported_files = self.data_collector.export_comprehensive_data()
            session_file = self.data_collector.save_session()
            
            # Track data export for achievements
            if self.achievement_manager:
                new_achievements = self.achievement_manager.track_game_event("data_exported")
                for achievement in new_achievements:
                    self.show_achievement_notification(achievement)
            
            files_list = "\n".join([f"- {file}" for file in exported_files])
            message = f"Data exported successfully!\n\nFiles created:\n{files_list}\n- {session_file}"
            self.show_inline_message("📊 Export Successful", message)
        except Exception as e:
            self.show_inline_error("📊 Export Error", f"Failed to export data: {str(e)}")
    
    def show_final_results(self, round_info):
        """Show final game results in a popup."""
        final_results = self.game_logic.get_final_results()
        
        # Create results window
        results_window = self._create_popup("🎉 Game Complete!", "600x500", '#f0f0f0')
        
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
        
        def play_again():
            results_window.destroy()
            self.new_game()
        
        play_again_btn = tk.Button(
            button_frame,
            text="🎮 Play Again",
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            command=play_again
        )
        play_again_btn.pack(side=tk.LEFT, padx=10)
        
        # Check if this is a high score
        game_mode = final_results.get('game_mode', 'normal')
        is_high_score = self.leaderboard.is_high_score(final_results['total_score'], game_mode)
        
        if is_high_score:
            def submit_score():
                self.submit_to_leaderboard(final_results, results_window)
            
            leaderboard_btn = tk.Button(
                button_frame,
                text="🏆 Submit to Leaderboard",
                font=('Arial', 14, 'bold'),
                bg='#FFD700',
                fg='black',
                padx=20,
                pady=10,
                command=submit_score
            )
            leaderboard_btn.pack(side=tk.LEFT, padx=10)
        
        def export_and_close():
            self.export_data()
            results_window.destroy()
        
        export_btn = tk.Button(
            button_frame,
            text="📊 Export Data",
            font=('Arial', 14),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            command=export_and_close
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        # Add proper exit button
        exit_btn = tk.Button(
            button_frame,
            text="🚪 Exit Game",
            font=('Arial', 14),
            bg='#D32F2F',
            fg='white',
            padx=20,
            pady=10,
            command=self.exit_application
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # Disable main game controls
        self.current_round_active = False
        self.next_btn.config(text="Game Complete", state='disabled')
    
    def exit_application(self):
        """Exit the application."""
        self.root.quit()
    
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