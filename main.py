#!/usr/bin/env python3
"""
Token Synonym Game - Main Entry Point
Research project to analyze token ID relationships and synonym clustering

Author: Research Team
Purpose: Investigate if LLMs place synonyms similarly in token space
"""

import sys
import os

# Add current directory to path to ensure module imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tiktoken
except ImportError:
    print("ERROR: tiktoken not installed!")
    print("Please install it with: pip install tiktoken")
    sys.exit(1) 

from gui_interface import TokenGameGUI


def main():
    """Main function to start the Token Synonym Game."""
    print("🎯 Starting Token Synonym Game...")
    print("Research Edition - Analyzing Token ID Relationships")
    print("-" * 50)
    
    try:
        # Test tiktoken installation
        enc = tiktoken.get_encoding("o200k_base")
        test_tokens = enc.encode("hello world")
        print(f"✅ tiktoken working! Test encoding: {test_tokens}")
        
        print("🖥️ Starting GUI interface...")
        
        # Start the GUI game
        game = TokenGameGUI()
        print("✅ GUI created successfully")
        game.run()
        
        print("\n👋 Thanks for playing! Your data helps our research.")
        
    except ImportError as e:
        if "tkinter" in str(e):
            print(f"❌ tkinter error: {e}")
            print("\nTkinter GUI is not available. This might be because:")
            print("1. You're running in a headless environment")
            print("2. tkinter is not installed with your Python")
            print("3. You're using WSL without X11 forwarding")
            print("\nTry installing tkinter: sudo apt-get install python3-tk")
        else:
            print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure tiktoken is installed: pip install tiktoken")
        print("2. Check that all game files are in the same directory")
        print("3. Ensure you have tkinter installed (usually comes with Python)")
        sys.exit(1)


if __name__ == "__main__":
    main() 