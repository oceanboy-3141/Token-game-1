"""
Material Design Components for Token Quest
Contains design system constants, styling utilities, and reusable UI components
"""
import tkinter as tk
from tkinter import ttk


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


class MaterialComponents:
    """Reusable Material Design UI components"""
    
    @staticmethod
    def create_material_card(parent, **kwargs):
        """Create a material design card with elevation effect."""
        # Default card styling
        card_config = {
            'bg': MaterialColors.SURFACE,
            'relief': 'flat',
            'bd': 0,
            'highlightthickness': 1,
            'highlightcolor': MaterialColors.OUTLINE,
            'highlightbackground': MaterialColors.OUTLINE,
            'padx': 16,
            'pady': 16
        }
        
        # Override with any provided kwargs
        card_config.update(kwargs)
        
        card = tk.Frame(parent, **card_config)
        
        # Add subtle shadow effect (simulation with border)
        shadow = tk.Frame(parent, bg='#E0E0E0', height=2, bd=0)
        
        return card, shadow
    
    @staticmethod
    def create_material_button(parent, text, command, style='primary', **kwargs):
        """Create a material design button with hover effects."""
        # Button style configurations
        styles = {
            'primary': {
                'bg': MaterialColors.PRIMARY,
                'fg': 'white',
                'activebackground': MaterialColors.PRIMARY_DARK,
                'activeforeground': 'white',
                'hover_bg': MaterialColors.PRIMARY_LIGHT
            },
            'secondary': {
                'bg': MaterialColors.SECONDARY,
                'fg': MaterialColors.ON_SURFACE,
                'activebackground': MaterialColors.SECONDARY_DARK,
                'activeforeground': 'white',
                'hover_bg': MaterialColors.SECONDARY_LIGHT
            },
            'outline': {
                'bg': MaterialColors.SURFACE,
                'fg': MaterialColors.PRIMARY,
                'activebackground': MaterialColors.PRIMARY_LIGHT,
                'activeforeground': MaterialColors.PRIMARY_DARK,
                'relief': 'solid',
                'bd': 1,
                'hover_bg': MaterialColors.PRIMARY_LIGHT
            },
            'success': {
                'bg': MaterialColors.SUCCESS,
                'fg': 'white',
                'activebackground': '#45A049',
                'activeforeground': 'white',
                'hover_bg': '#66BB6A'
            },
            'warning': {
                'bg': MaterialColors.WARNING,
                'fg': 'white',
                'activebackground': '#F57C00',
                'activeforeground': 'white',
                'hover_bg': '#FFB74D'
            },
            'error': {
                'bg': MaterialColors.ERROR,
                'fg': 'white',
                'activebackground': '#D32F2F',
                'activeforeground': 'white',
                'hover_bg': '#EF5350'
            }
        }
        
        # Get style configuration
        style_config = styles.get(style, styles['primary'])
        
        # Default button configuration
        button_config = {
            'text': text,
            'command': command,
            'font': MaterialTypography.LABEL_MEDIUM,
            'relief': 'flat',
            'bd': 0,
            'padx': 24,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        # Apply style
        button_config.update({k: v for k, v in style_config.items() if k != 'hover_bg'})
        
        # Override with any provided kwargs
        button_config.update(kwargs)
        
        button = tk.Button(parent, **button_config)
        
        # Add hover effects
        def on_enter(e):
            button.configure(bg=style_config['hover_bg'])
        
        def on_leave(e):
            button.configure(bg=style_config['bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    @staticmethod
    def configure_ttk_styles():
        """Configure ttk widget styles for material design."""
        style = ttk.Style()
        
        # Configure Progressbar
        style.configure(
            "Material.Horizontal.TProgressbar",
            background=MaterialColors.PRIMARY,
            troughcolor=MaterialColors.SURFACE_VARIANT,
            borderwidth=0,
            lightcolor=MaterialColors.PRIMARY_LIGHT,
            darkcolor=MaterialColors.PRIMARY_DARK,
            relief='flat'
        )
        
        # Configure Notebook (for tabbed interfaces)
        style.configure(
            "Material.TNotebook",
            background=MaterialColors.BACKGROUND,
            borderwidth=0,
            focuscolor='none'
        )
        
        style.configure(
            "Material.TNotebook.Tab",
            background=MaterialColors.SURFACE_VARIANT,
            foreground=MaterialColors.ON_SURFACE_VARIANT,
            padding=[20, 10],
            font=MaterialTypography.LABEL_MEDIUM
        )
        
        style.map(
            "Material.TNotebook.Tab",
            background=[("selected", MaterialColors.SURFACE)],
            foreground=[("selected", MaterialColors.PRIMARY)],
            expand=[("selected", [1, 1, 1, 0])]
        )
    
    @staticmethod
    def create_material_entry(parent, placeholder="", **kwargs):
        """Create a material design entry field with placeholder support."""
        entry_frame = tk.Frame(parent, bg=MaterialColors.SURFACE)
        
        # Entry configuration
        entry_config = {
            'font': MaterialTypography.BODY_MEDIUM,
            'bg': MaterialColors.SURFACE,
            'fg': MaterialColors.ON_SURFACE,
            'relief': 'flat',
            'bd': 0,
            'highlightthickness': 2,
            'highlightcolor': MaterialColors.PRIMARY,
            'highlightbackground': MaterialColors.OUTLINE,
            'insertbackground': MaterialColors.PRIMARY
        }
        
        entry_config.update(kwargs)
        entry = tk.Entry(entry_frame, **entry_config)
        
        # Placeholder functionality
        if placeholder:
            entry.insert(0, placeholder)
            entry.configure(fg=MaterialColors.ON_SURFACE_VARIANT)
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.configure(fg=MaterialColors.ON_SURFACE)
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.configure(fg=MaterialColors.ON_SURFACE_VARIANT)
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        entry.pack(fill='x', padx=4, pady=4)
        
        # Bottom border line
        border = tk.Frame(entry_frame, height=1, bg=MaterialColors.OUTLINE)
        border.pack(fill='x', side='bottom')
        
        return entry_frame, entry
    
    @staticmethod
    def create_material_label(parent, text, style='body', **kwargs):
        """Create a material design label with typography."""
        typography_styles = {
            'headline_large': MaterialTypography.HEADLINE_LARGE,
            'headline_medium': MaterialTypography.HEADLINE_MEDIUM,
            'headline_small': MaterialTypography.HEADLINE_SMALL,
            'title_large': MaterialTypography.TITLE_LARGE,
            'title_medium': MaterialTypography.TITLE_MEDIUM,
            'title_small': MaterialTypography.TITLE_SMALL,
            'body_large': MaterialTypography.BODY_LARGE,
            'body': MaterialTypography.BODY_MEDIUM,
            'body_small': MaterialTypography.BODY_SMALL,
            'label_large': MaterialTypography.LABEL_LARGE,
            'label': MaterialTypography.LABEL_MEDIUM,
            'label_small': MaterialTypography.LABEL_SMALL
        }
        
        label_config = {
            'text': text,
            'font': typography_styles.get(style, MaterialTypography.BODY_MEDIUM),
            'bg': MaterialColors.BACKGROUND,
            'fg': MaterialColors.ON_SURFACE
        }
        
        label_config.update(kwargs)
        return tk.Label(parent, **label_config)


class MaterialUtils:
    """Utility functions for Material Design operations"""
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb):
        """Convert RGB tuple to hex color."""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    @staticmethod
    def blend_colors(color1, color2, ratio):
        """Blend two hex colors with given ratio (0.0 to 1.0)."""
        rgb1 = MaterialUtils.hex_to_rgb(color1)
        rgb2 = MaterialUtils.hex_to_rgb(color2)
        
        blended = tuple(int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio) for i in range(3))
        return MaterialUtils.rgb_to_hex(blended)
    
    @staticmethod
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
                MaterialUtils.apply_theme_to_widget(child, theme)
        except:
            pass  # Some widgets might not support these options 