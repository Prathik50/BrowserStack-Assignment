@echo off
REM El País Scraper - Windows Setup Script
REM This script automates the setup process on Windows

echo.
echo ============================================================================
echo EL PAÍS WEB SCRAPER - WINDOWS SETUP
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo [1/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Install dependencies
echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Create .env file
echo [4/4] Setting up configuration...
if exist .env (
    echo .env file already exists, skipping...
) else (
    copy .env.example .env
    echo .env file created from template
)
echo.

REM Display completion message
echo ============================================================================
echo SETUP COMPLETE!
echo ============================================================================
echo.
echo Virtual environment is activated. You can now run:
echo   python main.py
echo.
echo Other options:
echo   python main.py --help              (Show all options)
echo   python main.py --articles 10       (Scrape 10 articles)
echo   python main.py --local-only        (Local testing only)
echo   python examples.py                 (Run code examples)
echo.
echo For more information, see:
echo   - README.md (complete documentation)
echo   - QUICKSTART.md (quick reference)
echo   - EXECUTION_GUIDE.py (interactive guide)
echo.
echo Optional: Configure BrowserStack in .env file for cross-browser testing
echo   BROWSERSTACK_USER=your_username
echo   BROWSERSTACK_KEY=your_key
echo.
echo ============================================================================
echo.

REM Optionally run the scraper
set /p run_now="Run the scraper now? (y/n): "
if /i "%run_now%"=="y" (
    python main.py
) else (
    echo Setup complete. You can run 'python main.py' whenever you're ready.
)

pause
