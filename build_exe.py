"""
Build Script for Token Synonym Game
Creates a standalone executable that can run without Python installed
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not available."""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📥 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def build_executable():
    """Build the standalone executable."""
    print("🔨 Building standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI only)
        "--name", "TokenSynonymGame",  # Executable name
        "--icon", "NONE",  # No icon (can add later)
        "--add-data", "game_data;game_data",  # Include data folder
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable built successfully!")
        print("📁 Find it in: dist/TokenSynonymGame.exe")
        print("\n🎉 You can now distribute this .exe file!")
        print("💡 Users can double-click it to play - no Python needed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def main():
    """Main build process."""
    print("🎯 Token Synonym Game - Executable Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found! Run this from the game directory.")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        print("\n🚀 Ready for distribution!")
        print("Users can now:")
        print("1. Double-click TokenSynonymGame.exe")
        print("2. Play immediately - no setup required!")
    else:
        print("\n❌ Build failed. Try running manually:")
        print("pip install pyinstaller")
        print("pyinstaller --onefile --windowed main.py")

if __name__ == "__main__":
    main() 