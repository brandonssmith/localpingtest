# PingTest - Network Ping Monitoring Application
# PowerShell Launcher Script

Write-Host "PingTest - Network Ping Monitoring Application" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.6 or higher and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pingtest.py exists
if (-not (Test-Path "pingtest.py")) {
    Write-Host "Error: pingtest.py not found in current directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting PingTest..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Run the pingtest application
try {
    python pingtest.py
} catch {
    Write-Host "Application stopped or encountered an error" -ForegroundColor Yellow
}

Read-Host "Press Enter to exit" 