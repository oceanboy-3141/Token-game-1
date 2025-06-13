"""
Dialog Windows and Popups for Token Quest
Contains all modal dialogs, popups, and secondary windows
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from .material_components import MaterialColors, MaterialComponents, MaterialTypography, MaterialUtils
from .animations import AnimationManager


class DialogManager:
    """Manages all dialog windows and popups for the application"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.active_popup = None
        self.animation_manager = AnimationManager()
    
    def _close_active_popup(self):
        """Close any currently active popup window."""
        if self.active_popup and self.active_popup.winfo_exists():
            self.active_popup.destroy()
        self.active_popup = None
    
    def _create_popup(self, title, geometry, bg='white'):
        """Create a new popup window, closing any existing one."""
        self._close_active_popup()
        
        popup = tk.Toplevel(self.parent)
        popup.title(title)
        popup.geometry(geometry)
        popup.configure(bg=bg)
        popup.transient(self.parent)
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
        notification = tk.Toplevel(self.parent)
        notification.title("🎖️ Achievement Unlocked!")
        notification.geometry("400x200")
        notification.configure(bg=MaterialColors.SUCCESS)
        notification.transient(self.parent)
        notification.attributes("-topmost", True)
        
        # Position in top-right corner
        notification.geometry("+{}+{}".format(
            self.parent.winfo_rootx() + self.parent.winfo_width() - 420,
            self.parent.winfo_rooty() + 20
        ))
        
        # Content
        tk.Label(
            notification,
            text="🎖️ ACHIEVEMENT UNLOCKED! 🎖️",
            font=MaterialTypography.TITLE_MEDIUM,
            bg=MaterialColors.SUCCESS,
            fg='white'
        ).pack(pady=10)
        
        tk.Label(
            notification,
            text=f"{achievement.icon} {achievement.name}",
            font=MaterialTypography.TITLE_LARGE,
            bg=MaterialColors.SUCCESS,
            fg='white'
        ).pack(pady=5)
        
        tk.Label(
            notification,
            text=achievement.description,
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SUCCESS,
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
        
        # Add slide-in animation
        self.animation_manager.slide_in_animation(notification, 'right', 200, 300)
    
    def show_hint_dialog(self, hint_data, target_word, insert_callback=None):
        """Show the comprehensive hint dialog with tabbed interface."""
        hint_window = self._create_popup("💡 Smart Hints", "800x600", MaterialColors.BACKGROUND)
        
        # Main container
        main_frame = tk.Frame(hint_window, bg=MaterialColors.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = MaterialComponents.create_material_label(
            main_frame, f"🎯 Finding words similar to: {target_word}", 'title_large'
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        MaterialComponents.configure_ttk_styles()
        notebook = ttk.Notebook(main_frame, style="Material.TNotebook")
        notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # Semantic Hints Tab
        semantic_frame = tk.Frame(notebook, bg=MaterialColors.SURFACE)
        notebook.add(semantic_frame, text="🧠 Semantic Hints")
        self._create_semantic_hints_tab(semantic_frame, hint_data, insert_callback)
        
        # Token Space Tab
        token_frame = tk.Frame(notebook, bg=MaterialColors.SURFACE)
        notebook.add(token_frame, text="🔢 Token Space")
        self._create_token_hints_tab(token_frame, hint_data, insert_callback)
        
        # Educational Tab
        educational_frame = tk.Frame(notebook, bg=MaterialColors.SURFACE)
        notebook.add(educational_frame, text="📚 Learn More")
        self._create_educational_tab(educational_frame, hint_data)
        
        # Close button
        MaterialComponents.create_material_button(
            main_frame, "Close Hints", hint_window.destroy, 'outline'
        ).pack(pady=10)
        
        return hint_window
    
    def _create_semantic_hints_tab(self, parent, hint_data, insert_callback):
        """Create the semantic hints tab content."""
        scroll_frame = scrolledtext.ScrolledText(
            parent, wrap='word', height=15, width=70,
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add semantic hints
        semantic_hints = hint_data.get('semantic_hints', [])
        if semantic_hints:
            scroll_frame.insert('end', "🧠 Words with similar meanings:\n\n")
            for i, word in enumerate(semantic_hints, 1):
                scroll_frame.insert('end', f"{i}. {word}\n")
                
                # Add clickable button for each word
                if insert_callback:
                    button_frame = tk.Frame(parent, bg=MaterialColors.SURFACE)
                    MaterialComponents.create_material_button(
                        button_frame, f"Use '{word}'", 
                        lambda w=word: insert_callback(w), 'secondary'
                    ).pack(side='left', padx=5)
        
        # Add contextual hint
        context_hint = hint_data.get('context_hint', '')
        if context_hint:
            scroll_frame.insert('end', f"\n💡 Context Hint:\n{context_hint}\n")
        
        scroll_frame.config(state='disabled')
    
    def _create_token_hints_tab(self, parent, hint_data, insert_callback):
        """Create the token space hints tab content."""
        # Token info section
        info_frame = tk.Frame(parent, bg=MaterialColors.SURFACE)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        target_id = hint_data.get('target_token_id', 'N/A')
        MaterialComponents.create_material_label(
            info_frame, f"🎯 Target Token ID: {target_id}", 'title_medium'
        ).pack(anchor='w')
        
        # Nearby tokens section
        nearby_frame = tk.Frame(parent, bg=MaterialColors.SURFACE)
        nearby_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        MaterialComponents.create_material_label(
            nearby_frame, "🔢 Words with nearby Token IDs:", 'title_small'
        ).pack(anchor='w', pady=(0, 10))
        
        # Create scrollable list of nearby tokens
        token_list_frame = tk.Frame(nearby_frame, bg=MaterialColors.SURFACE)
        token_list_frame.pack(fill='both', expand=True)
        
        # Add canvas for scrolling
        canvas = tk.Canvas(token_list_frame, bg=MaterialColors.SURFACE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(token_list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=MaterialColors.SURFACE)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Add nearby words
        nearby_words = hint_data.get('nearby_words', [])
        for word_info in nearby_words:
            word = word_info.get('word', 'Unknown')
            token_id = word_info.get('token_id', 'N/A')
            distance = word_info.get('distance', 'N/A')
            
            word_frame = tk.Frame(scrollable_frame, bg=MaterialColors.SURFACE_VARIANT, relief='solid', bd=1)
            word_frame.pack(fill='x', pady=2, padx=5)
            
            info_text = f"{word} (ID: {token_id}, Distance: {distance})"
            MaterialComponents.create_material_label(
                word_frame, info_text, 'body'
            ).pack(side='left', padx=10, pady=5)
            
            if insert_callback:
                MaterialComponents.create_material_button(
                    word_frame, "Use", lambda w=word: insert_callback(w), 'outline'
                ).pack(side='right', padx=10, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_educational_tab(self, parent, hint_data):
        """Create the educational content tab."""
        scroll_frame = scrolledtext.ScrolledText(
            parent, wrap='word', height=15, width=70,
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Educational content
        educational_content = """
📚 Understanding Token Space

🔤 What are tokens?
Tokens are the basic units that language models use to process text. Each word, punctuation mark, or word fragment gets assigned a unique numerical ID called a token ID.

🎯 Why do token IDs matter?
• Lower token IDs usually represent more common words
• Words with similar token IDs might be processed similarly by AI models
• Token distance can sometimes (but not always) reflect semantic similarity

🧠 Research Insights:
• This game helps explore whether synonyms cluster together in token space
• Token frequency in training data affects ID assignment
• Different tokenization schemes can produce different patterns

💡 Did You Know?
The relationship between token proximity and semantic similarity is an active area of AI research. Your gameplay contributes to understanding these patterns!

🔬 What We're Learning:
• Do humans perceive word similarity the same way tokenizers do?
• Can token ID distance predict semantic relationships?
• How do different word categories cluster in token space?
        """
        
        scroll_frame.insert('end', educational_content)
        scroll_frame.config(state='disabled')
    
    def show_game_settings_dialog(self, current_settings, apply_callback):
        """Show the game settings configuration dialog."""
        settings_window = self._create_popup("⚙️ Game Settings", "500x600", MaterialColors.BACKGROUND)
        
        # Main container
        main_frame = tk.Frame(settings_window, bg=MaterialColors.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        MaterialComponents.create_material_label(
            main_frame, "⚙️ Configure Game Settings", 'title_large'
        ).pack(pady=(0, 20))
        
        # Settings variables
        settings_vars = {}
        
        # Game Mode Section
        mode_frame, _ = MaterialComponents.create_material_card(main_frame)
        mode_frame.pack(fill='x', pady=10)
        
        MaterialComponents.create_material_label(
            mode_frame, "🎮 Game Mode", 'title_medium'
        ).pack(anchor='w')
        
        settings_vars['game_mode'] = tk.StringVar(value=current_settings.get('game_mode', 'normal'))
        modes = [('Normal Mode', 'normal'), ('Antonym Mode', 'antonym'), ('Category Mode', 'category')]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame, text=text, variable=settings_vars['game_mode'], value=value,
                bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE,
                selectcolor=MaterialColors.PRIMARY_LIGHT,
                font=MaterialTypography.BODY_MEDIUM
            ).pack(anchor='w', padx=20)
        
        # Difficulty Section
        diff_frame, _ = MaterialComponents.create_material_card(main_frame)
        diff_frame.pack(fill='x', pady=10)
        
        MaterialComponents.create_material_label(
            diff_frame, "📊 Difficulty Level", 'title_medium'
        ).pack(anchor='w')
        
        settings_vars['difficulty'] = tk.StringVar(value=current_settings.get('difficulty', 'mixed'))
        difficulties = [('Mixed', 'mixed'), ('Easy', 'easy'), ('Medium', 'medium'), ('Hard', 'hard')]
        
        for text, value in difficulties:
            tk.Radiobutton(
                diff_frame, text=text, variable=settings_vars['difficulty'], value=value,
                bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE,
                selectcolor=MaterialColors.PRIMARY_LIGHT,
                font=MaterialTypography.BODY_MEDIUM
            ).pack(anchor='w', padx=20)
        
        # Category Section
        cat_frame, _ = MaterialComponents.create_material_card(main_frame)
        cat_frame.pack(fill='x', pady=10)
        
        MaterialComponents.create_material_label(
            cat_frame, "📂 Word Category", 'title_medium'
        ).pack(anchor='w')
        
        settings_vars['category'] = tk.StringVar(value=current_settings.get('category', 'all'))
        categories = [
            ('All Categories', 'all'), ('Emotions', 'emotions'), 
            ('Size', 'size'), ('Speed', 'speed'), ('Quality', 'quality')
        ]
        
        for text, value in categories:
            tk.Radiobutton(
                cat_frame, text=text, variable=settings_vars['category'], value=value,
                bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE,
                selectcolor=MaterialColors.PRIMARY_LIGHT,
                font=MaterialTypography.BODY_MEDIUM
            ).pack(anchor='w', padx=20)
        
        # Rounds Section
        rounds_frame, _ = MaterialComponents.create_material_card(main_frame)
        rounds_frame.pack(fill='x', pady=10)
        
        MaterialComponents.create_material_label(
            rounds_frame, "🎯 Number of Rounds", 'title_medium'
        ).pack(anchor='w')
        
        settings_vars['rounds'] = tk.IntVar(value=current_settings.get('rounds', 10))
        rounds_scale = tk.Scale(
            rounds_frame, from_=5, to=25, orient='horizontal',
            variable=settings_vars['rounds'],
            bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE,
            highlightthickness=0, troughcolor=MaterialColors.PRIMARY_LIGHT
        )
        rounds_scale.pack(fill='x', padx=20, pady=10)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=MaterialColors.BACKGROUND)
        button_frame.pack(fill='x', pady=20)
        
        def apply_settings():
            new_settings = {key: var.get() for key, var in settings_vars.items()}
            apply_callback(new_settings, settings_window)
        
        MaterialComponents.create_material_button(
            button_frame, "Apply Settings", apply_settings, 'primary'
        ).pack(side='right', padx=5)
        
        MaterialComponents.create_material_button(
            button_frame, "Cancel", settings_window.destroy, 'outline'
        ).pack(side='right', padx=5)
        
        return settings_window
    
    def show_statistics_dialog(self, stats_data):
        """Show detailed game statistics."""
        stats_window = self._create_popup("📊 Game Statistics", "600x500", MaterialColors.BACKGROUND)
        
        # Main container with scrolling
        main_frame = tk.Frame(stats_window, bg=MaterialColors.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        MaterialComponents.create_material_label(
            main_frame, "📊 Your Token Quest Statistics", 'title_large'
        ).pack(pady=(0, 20))
        
        # Create scrollable text area
        stats_text = scrolledtext.ScrolledText(
            main_frame, wrap='word', height=20, width=70,
            font=MaterialTypography.BODY_MEDIUM,
            bg=MaterialColors.SURFACE, fg=MaterialColors.ON_SURFACE
        )
        stats_text.pack(fill='both', expand=True)
        
        # Format and display statistics
        stats_content = self._format_statistics(stats_data)
        stats_text.insert('end', stats_content)
        stats_text.config(state='disabled')
        
        # Close button
        MaterialComponents.create_material_button(
            main_frame, "Close", stats_window.destroy, 'primary'
        ).pack(pady=10)
        
        return stats_window
    
    def _format_statistics(self, stats_data):
        """Format statistics data for display."""
        content = "🎯 GAME PERFORMANCE\n"
        content += "=" * 50 + "\n\n"
        
        # Basic stats
        content += f"🎮 Games Played: {stats_data.get('games_played', 0)}\n"
        content += f"💯 Total Score: {stats_data.get('total_score', 0):,}\n"
        content += f"🎯 Perfect Matches: {stats_data.get('perfects', 0)}\n"
        content += f"⭐ Excellent Matches: {stats_data.get('excellents', 0)}\n"
        content += f"🔥 Best Streak: {stats_data.get('max_correct_streak', 0)}\n\n"
        
        # Advanced stats
        content += "📈 ADVANCED METRICS\n"
        content += "=" * 50 + "\n\n"
        
        total_words = len(stats_data.get('words_tried', set()))
        content += f"📚 Unique Words Tried: {total_words}\n"
        content += f"💡 Hints Viewed: {stats_data.get('hints_viewed', 0)}\n"
        content += f"📊 Data Exports: {stats_data.get('data_exports', 0)}\n"
        content += f"🏆 Leaderboard Submissions: {stats_data.get('leaderboard_submissions', 0)}\n\n"
        
        # Mode performance
        content += "🎮 MODE PERFORMANCE\n"
        content += "=" * 50 + "\n\n"
        mode_wins = stats_data.get('mode_wins', {})
        content += f"🎯 Normal Mode Wins: {mode_wins.get('normal', 0)}\n"
        content += f"🔄 Antonym Mode Wins: {mode_wins.get('antonym', 0)}\n"
        content += f"📂 Category Mode Wins: {mode_wins.get('category', 0)}\n\n"
        
        # Categories explored
        categories_played = stats_data.get('categories_played', set())
        if categories_played:
            content += "📂 CATEGORIES EXPLORED\n"
            content += "=" * 50 + "\n\n"
            for category in sorted(categories_played):
                content += f"• {category.title()}\n"
            content += "\n"
        
        # Time patterns
        content += "⏰ PLAY PATTERNS\n"
        content += "=" * 50 + "\n\n"
        content += f"🌙 Night Games (after 10 PM): {stats_data.get('night_games', 0)}\n"
        content += f"🌅 Early Games (before 6 AM): {stats_data.get('morning_games', 0)}\n"
        content += f"💪 Comeback Wins: {stats_data.get('comeback_wins', 0)}\n"
        
        return content
    
    def show_export_dialog(self, export_callback):
        """Show data export options dialog."""
        export_window = self._create_popup("📊 Export Game Data", "400x300", MaterialColors.BACKGROUND)
        
        # Main container
        main_frame = tk.Frame(export_window, bg=MaterialColors.BACKGROUND)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        MaterialComponents.create_material_label(
            main_frame, "📊 Export Your Research Data", 'title_large'
        ).pack(pady=(0, 20))
        
        # Export options
        export_vars = {
            'session_data': tk.BooleanVar(value=True),
            'summary_stats': tk.BooleanVar(value=True),
            'csv_format': tk.BooleanVar(value=True),
            'json_format': tk.BooleanVar(value=False)
        }
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=MaterialColors.BACKGROUND)
        button_frame.pack(fill='x', pady=20)
        
        def do_export():
            options = {key: var.get() for key, var in export_vars.items()}
            export_callback(options, export_window)
        
        MaterialComponents.create_material_button(
            button_frame, "Export Data", do_export, 'success'
        ).pack(side='right', padx=5)
        
        MaterialComponents.create_material_button(
            button_frame, "Cancel", export_window.destroy, 'outline'
        ).pack(side='right', padx=5)
        
        return export_window 