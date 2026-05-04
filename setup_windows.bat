@echo off
REM Windows batch script to setup Python environment
REM Run this before running plot_graphs.py

echo ======================================================
echo NS-3 TCP Comparison - Windows Setup
echo ======================================================
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
python -m pip install --quiet matplotlib numpy pandas scipy seaborn

if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ======================================================
echo Setup Complete!
echo ======================================================
echo.
echo You can now run: python python-analysis/plot_graphs.py
echo.
pause
