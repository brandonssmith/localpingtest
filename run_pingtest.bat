@echo off
echo PingTest - Network Ping Monitoring Application
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher and try again
    pause
    exit /b 1
)

REM Check if pingtest.py exists
if not exist "pingtest.py" (
    echo Error: pingtest.py not found in current directory
    pause
    exit /b 1
)

echo Starting PingTest...
echo Press Ctrl+C to stop the application
echo.

REM Run the pingtest application
python pingtest.py

pause 