#!/usr/bin/env python3
"""
Simple Play Script for Token Quest
Shows game mode selection and starts the game
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import main functionality
from main import main

if __name__ == "__main__":
    print("🎯 Welcome to Token Quest!")
    print("This will show you game mode options...")
    print("-" * 40)
    main() 