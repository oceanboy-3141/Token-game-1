"""
Animation System for Token Quest
Contains smooth transitions, visual effects, and interactive animations
"""
import tkinter as tk
from .material_components import MaterialColors, MaterialUtils


class AnimationManager:
    """Manages smooth animations and visual effects for the UI"""
    
    def __init__(self):
        self.animation_queue = []
        self.animation_running = False
    
    def smooth_color_transition(self, widget, start_color, end_color, duration=200, steps=10):
        """Smoothly transition widget color from start to end."""
        if self.animation_running:
            return
            
        self.animation_running = True
        
        def animate_step(step):
            if step > steps:
                self.animation_running = False
                return
            
            # Calculate progress ratio
            ratio = step / steps
            
            # Blend colors
            current_color = MaterialUtils.blend_colors(start_color, end_color, ratio)
            
            try:
                widget.configure(bg=current_color)
                widget.after(duration // steps, lambda: animate_step(step + 1))
            except tk.TclError:
                # Widget was destroyed
                self.animation_running = False
        
        animate_step(0)
    
    def animate_feedback_entry(self, widget):
        """Animate entry widget to show feedback (expand effect)."""
        original_height = widget.winfo_reqheight()
        
        def expand_step(current_height):
            if current_height >= original_height * 1.2:
                # Shrink back
                widget.configure(height=int(original_height))
                return
            
            widget.configure(height=int(current_height))
            widget.after(20, lambda: expand_step(current_height + 2))
        
        expand_step(original_height)
    
    def pulse_animation(self, widget, scale_factor=1.1, duration=300):
        """Create a pulse animation effect on a widget."""
        try:
            original_font = widget.cget('font')
            if isinstance(original_font, str):
                # If font is a string, we can't easily scale it
                return
            
            family, size, style = original_font
            new_size = int(size * scale_factor)
            
            # Scale up
            widget.configure(font=(family, new_size, style))
            
            # Scale back down after duration
            def scale_down():
                try:
                    widget.configure(font=original_font)
                except tk.TclError:
                    pass  # Widget was destroyed
            
            widget.after(duration, scale_down)
            
        except (tk.TclError, ValueError, TypeError):
            # Fallback: simple color flash
            original_bg = widget.cget('bg')
            widget.configure(bg=MaterialColors.PRIMARY_LIGHT)
            widget.after(duration, lambda: self._safe_configure(widget, bg=original_bg))
    
    def fade_in_animation(self, widget, duration=300, steps=10):
        """Fade in a widget smoothly."""
        # Start with transparent (simulate with background blending)
        parent_bg = widget.master.cget('bg') if hasattr(widget.master, 'cget') else MaterialColors.BACKGROUND
        
        def fade_step(step):
            if step > steps:
                return
            
            # Calculate alpha
            alpha = step / steps
            
            # Blend with parent background
            if hasattr(widget, 'cget') and 'bg' in widget.keys():
                target_bg = widget.cget('bg')
                current_bg = MaterialUtils.blend_colors(parent_bg, target_bg, alpha)
                self._safe_configure(widget, bg=current_bg)
            
            widget.after(duration // steps, lambda: fade_step(step + 1))
        
        fade_step(0)
    
    def slide_in_animation(self, widget, direction='left', distance=100, duration=300):
        """Slide widget in from specified direction."""
        # Get current position
        try:
            current_x = widget.winfo_x()
            current_y = widget.winfo_y()
            
            # Calculate start position
            if direction == 'left':
                start_x = current_x - distance
                start_y = current_y
            elif direction == 'right':
                start_x = current_x + distance
                start_y = current_y
            elif direction == 'top':
                start_x = current_x
                start_y = current_y - distance
            else:  # bottom
                start_x = current_x
                start_y = current_y + distance
            
            # Move to start position
            widget.place(x=start_x, y=start_y)
            
            # Animate to final position
            steps = 20
            dx = (current_x - start_x) / steps
            dy = (current_y - start_y) / steps
            
            def slide_step(step):
                if step > steps:
                    widget.place(x=current_x, y=current_y)
                    return
                
                new_x = start_x + (dx * step)
                new_y = start_y + (dy * step)
                widget.place(x=int(new_x), y=int(new_y))
                widget.after(duration // steps, lambda: slide_step(step + 1))
            
            slide_step(0)
            
        except tk.TclError:
            pass  # Widget geometry not available
    
    def bounce_animation(self, widget, intensity=10, duration=400):
        """Create a bounce effect on widget."""
        try:
            original_y = widget.winfo_y()
            steps = 16
            
            def bounce_step(step):
                if step > steps:
                    widget.place(y=original_y)
                    return
                
                # Calculate bounce position using sine wave
                import math
                progress = step / steps
                bounce_offset = intensity * math.sin(progress * math.pi * 2) * (1 - progress)
                new_y = original_y - int(bounce_offset)
                
                widget.place(y=new_y)
                widget.after(duration // steps, lambda: bounce_step(step + 1))
            
            bounce_step(0)
            
        except tk.TclError:
            pass
    
    def typewriter_animation(self, label, text, delay=50):
        """Animate text appearing character by character."""
        def type_char(index):
            if index > len(text):
                return
            
            current_text = text[:index]
            self._safe_configure(label, text=current_text)
            
            if index < len(text):
                label.after(delay, lambda: type_char(index + 1))
        
        type_char(0)
    
    def progress_bar_animation(self, progressbar, target_value, duration=1000):
        """Animate progress bar to target value."""
        try:
            current_value = progressbar['value']
            steps = 30
            increment = (target_value - current_value) / steps
            
            def progress_step(step):
                if step > steps:
                    progressbar['value'] = target_value
                    return
                
                new_value = current_value + (increment * step)
                progressbar['value'] = new_value
                progressbar.after(duration // steps, lambda: progress_step(step + 1))
            
            progress_step(0)
            
        except (tk.TclError, KeyError):
            pass
    
    def shake_animation(self, widget, intensity=5, duration=300):
        """Create a shake effect for error feedback."""
        try:
            original_x = widget.winfo_x()
            steps = 12
            
            def shake_step(step):
                if step > steps:
                    widget.place(x=original_x)
                    return
                
                # Alternate left and right
                offset = intensity if step % 2 == 0 else -intensity
                # Decrease intensity over time
                offset = int(offset * (1 - step / steps))
                
                widget.place(x=original_x + offset)
                widget.after(duration // steps, lambda: shake_step(step + 1))
            
            shake_step(0)
            
        except tk.TclError:
            pass
    
    def glow_animation(self, widget, glow_color=None, duration=500):
        """Create a glow effect by changing border/background."""
        if not glow_color:
            glow_color = MaterialColors.PRIMARY_LIGHT
        
        try:
            original_bg = widget.cget('bg')
            
            # Pulse between original and glow color
            def glow_step(step, direction=1):
                if step <= 0 and direction == -1:
                    widget.configure(bg=original_bg)
                    return
                
                max_steps = 10
                if step >= max_steps and direction == 1:
                    direction = -1
                
                ratio = step / max_steps
                current_color = MaterialUtils.blend_colors(original_bg, glow_color, ratio)
                widget.configure(bg=current_color)
                
                next_step = step + direction
                widget.after(duration // 20, lambda: glow_step(next_step, direction))
            
            glow_step(0)
            
        except tk.TclError:
            pass
    
    def _safe_configure(self, widget, **kwargs):
        """Safely configure widget, handling TclError."""
        try:
            widget.configure(**kwargs)
        except tk.TclError:
            pass  # Widget was destroyed or invalid
    
    def stop_all_animations(self):
        """Stop all running animations."""
        self.animation_running = False
        self.animation_queue.clear()


class TokenVisualizationAnimations:
    """Specialized animations for token space visualization"""
    
    @staticmethod
    def animate_token_line_draw(canvas, start_pos, end_pos, color, duration=1000):
        """Animate drawing a line between tokens."""
        steps = 30
        
        def draw_step(step):
            if step > steps:
                return
            
            # Calculate current endpoint
            progress = step / steps
            current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
            
            # Clear previous line
            canvas.delete("animated_line")
            
            # Draw line up to current point
            canvas.create_line(
                start_pos[0], start_pos[1],
                current_x, current_y,
                fill=color, width=2, tags="animated_line"
            )
            
            canvas.after(duration // steps, lambda: draw_step(step + 1))
        
        draw_step(0)
    
    @staticmethod
    def animate_token_highlight(canvas, item_id, duration=800):
        """Animate highlighting a token on the canvas."""
        original_color = canvas.itemcget(item_id, 'fill')
        highlight_color = MaterialColors.WARNING
        
        steps = 16
        
        def highlight_step(step, direction=1):
            if step <= 0 and direction == -1:
                try:
                    canvas.itemconfig(item_id, fill=original_color)
                except tk.TclError:
                    pass
                return
            
            max_steps = 8
            if step >= max_steps and direction == 1:
                direction = -1
            
            ratio = step / max_steps
            current_color = MaterialUtils.blend_colors(original_color, highlight_color, ratio)
            
            try:
                canvas.itemconfig(item_id, fill=current_color)
                next_step = step + direction
                canvas.after(duration // 16, lambda: highlight_step(next_step, direction))
            except tk.TclError:
                pass  # Canvas item was deleted
        
        highlight_step(0)
    
    @staticmethod
    def animate_distance_visualization(canvas, target_pos, guess_pos, distance_value):
        """Animate the visualization of distance between tokens."""
        # Create pulsing connection line
        line_id = canvas.create_line(
            target_pos[0], target_pos[1],
            guess_pos[0], guess_pos[1],
            fill=MaterialColors.INFO, width=2, dash=(5, 5)
        )
        
        # Create distance label
        mid_x = (target_pos[0] + guess_pos[0]) // 2
        mid_y = (target_pos[1] + guess_pos[1]) // 2
        
        distance_label = canvas.create_text(
            mid_x, mid_y - 20,
            text=f"Distance: {distance_value}",
            font=('Arial', 10, 'bold'),
            fill=MaterialColors.INFO
        )
        
        # Animate pulsing
        def pulse_step(step):
            if step > 20:
                return
            
            # Pulse the line width
            width = 2 + int(2 * abs(0.5 - (step % 10) / 10))
            try:
                canvas.itemconfig(line_id, width=width)
                canvas.after(100, lambda: pulse_step(step + 1))
            except tk.TclError:
                pass
        
        pulse_step(0) 