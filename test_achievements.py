"""
Test script for the achievements system
"""

from achievements import AchievementManager
import tkinter as tk
from tkinter import messagebox

def test_achievement_notification():
    """Test the achievement notification system."""
    
    # Create a test window
    root = tk.Tk()
    root.title("🧪 Achievement Test")
    root.geometry("300x200")
    root.configure(bg='#f0f0f0')
    
    def show_test_notification():
        # Create achievement manager
        am = AchievementManager()
        
        # Track a game start event (should unlock test achievement)
        new_achievements = am.track_game_event("game_started")
        
        if new_achievements:
            # Show notification for each new achievement
            for achievement in new_achievements:
                show_achievement_popup(achievement)
        else:
            messagebox.showinfo("No New Achievements", "Test achievement already unlocked this session.")
    
    def show_achievement_popup(achievement):
        """Show achievement notification popup."""
        notification = tk.Toplevel(root)
        notification.title("🎖️ Achievement Unlocked!")
        notification.geometry("400x200")
        notification.configure(bg='#4CAF50')
        notification.transient(root)
        notification.attributes("-topmost", True)
        
        # Position in center
        notification.geometry("+{}+{}".format(
            root.winfo_rootx() + 50,
            root.winfo_rooty() + 50
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
        
        # Close button
        tk.Button(
            notification,
            text="✅ Awesome!",
            font=('Arial', 12),
            bg='#2E7D32',
            fg='white',
            padx=20,
            pady=5,
            command=notification.destroy
        ).pack(pady=10)
    
    # Test UI
    tk.Label(
        root,
        text="🧪 Achievement System Test",
        font=('Arial', 16, 'bold'),
        bg='#f0f0f0',
        fg='#333'
    ).pack(pady=20)
    
    tk.Button(
        root,
        text="🎖️ Test Achievement Notification",
        font=('Arial', 12, 'bold'),
        bg='#4CAF50',
        fg='white',
        padx=20,
        pady=10,
        command=show_test_notification
    ).pack(pady=20)
    
    tk.Button(
        root,
        text="❌ Close",
        font=('Arial', 10),
        bg='#666',
        fg='white',
        padx=20,
        pady=5,
        command=root.destroy
    ).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_achievement_notification() 