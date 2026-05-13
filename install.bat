@echo off
REM Installation script for TermAssist on Windows

echo 🚀 Installing TermAssist...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

echo ✅ Python found

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt --user

REM Install package
echo 📦 Installing TermAssist...
pip install -e . --user

REM Create config directory
if not exist "%USERPROFILE%\.config\termassist" mkdir "%USERPROFILE%\.config\termassist"

echo.
echo ✅ Installation complete!
echo.
echo Usage:
echo   termassist              # Start interactive mode
echo   termassist "your query" # One-shot mode
echo   tai                     # Short alias
echo.
echo Configuration file: %USERPROFILE%\.config\termassist\config.yaml
echo.
pause
