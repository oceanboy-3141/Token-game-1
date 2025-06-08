@echo off
title Token Synonym Game
echo 🎯 Starting Token Synonym Game...
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Try to install tiktoken if missing
echo 📦 Checking dependencies...
python -c "import tiktoken" >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing tiktoken...
    pip install tiktoken
    if errorlevel 1 (
        echo ❌ Failed to install tiktoken!
        echo Please run: pip install tiktoken
        pause
        exit /b 1
    )
)

REM Run the game
echo ✅ All dependencies ready!
echo 🎮 Launching game...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Game ended with an error.
    pause
) 