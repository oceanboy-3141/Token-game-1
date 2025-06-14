@echo off
REM ================================================================
REM  Token Quest – One-click launcher (Windows)
REM  Uses Conda if available, otherwise falls back to Python venv
REM ================================================================

REM --- Try to locate Conda ---------------------------------------------------
where conda >nul 2>nul
if %ERRORLEVEL% EQU 0 goto :use_conda

echo Conda not found. Using Python's built-in venv instead.

REM --- Create venv if it doesn't exist ---------------------------------------
if not exist .venv (
    echo Creating virtual environment in .venv ...
    python -m venv .venv || goto :venv_error
)

REM --- Activate venv ---------------------------------------------------------
call .\.venv\Scripts\activate || goto :venv_error

REM --- Install/update requirements ------------------------------------------
echo Installing/updating Python packages...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt || goto :pip_error

goto :start_server

:use_conda
REM --- Does the environment already exist? ----------------------------------
call conda env list | findstr /I "tokenquest" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Creating Conda environment ^'tokenquest^' with Python 3.10...
    call conda create -y -n tokenquest python=3.10
)

REM --- Activate environment --------------------------------------------------
call conda activate tokenquest
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate Conda environment. Make sure Conda is initialized in this shell.
    pause
    exit /b 1
)

REM --- Install/update requirements ------------------------------------------
echo Installing/updating Python packages...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt || goto :pip_error

goto :start_server

:start_server

echo.
echo ================================================================
echo  ✅  Environment ready. Launching Token Quest server...
echo ================================================================

REM --- Start lightweight web server so fewer dependencies are required ---
python simple_web_app.py

echo.
echo Server exited. Press any key to close this window.
pause
exit /b 0

:venv_error
echo [ERROR] Failed to create or activate Python virtual environment.
pause
exit /b 1

:pip_error
echo.
echo [ERROR] pip reported a failure while installing packages.
pause
exit /b 1 