@echo off
setlocal

REM Navigate to this script's directory
cd /d "%~dp0"

REM Check for Python launcher (py)
where py >nul 2>nul
if %errorlevel% neq 0 (
  echo Python not found. Please install Python 3.11 from https://www.python.org/downloads/windows/
  echo Make sure to check "Add Python to PATH" during installation. Then run this again.
  pause
  exit /b 1
)

REM Upgrade pip and install dependencies (user scope)
py -3 -m pip install --user --upgrade pip
py -3 -m pip install --user -r "requirements.txt"

REM Launch the game
py -3 "code (finish)\main.py"

endlocal

