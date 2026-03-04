# El País Scraper - Windows PowerShell Setup Script
# Run this script with: .\setup.ps1

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "EL PAÍS WEB SCRAPER - WINDOWS POWERSHELL SETUP" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "[1/4] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists, skipping..." -ForegroundColor Gray
} else {
    try {
        python -m venv venv
        Write-Host "  ✓ Virtual environment created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Activate virtual environment
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "  ✓ Virtual environment activated!" -ForegroundColor Green
} catch {
    Write-Host "  ✗ ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "  Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "  ✓ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "  ✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Create .env file
Write-Host "[4/4] Setting up configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  .env file already exists, skipping..." -ForegroundColor Gray
} else {
    try {
        Copy-Item ".env.example" ".env"
        Write-Host "  ✓ .env file created from template" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ WARNING: Failed to create .env file" -ForegroundColor Yellow
    }
}
Write-Host ""

# Display completion message
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Virtual environment is activated. You can now run:" -ForegroundColor Green
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""

Write-Host "Other options:" -ForegroundColor Green
Write-Host "  python main.py --help              (Show all options)" -ForegroundColor White
Write-Host "  python main.py --articles 10       (Scrape 10 articles)" -ForegroundColor White
Write-Host "  python main.py --local-only        (Local testing only)" -ForegroundColor White
Write-Host "  python examples.py                 (Run code examples)" -ForegroundColor White
Write-Host ""

Write-Host "For more information, see:" -ForegroundColor Green
Write-Host "  - README.md (complete documentation)" -ForegroundColor White
Write-Host "  - QUICKSTART.md (quick reference)" -ForegroundColor White
Write-Host "  - EXECUTION_GUIDE.py (interactive guide)" -ForegroundColor White
Write-Host ""

Write-Host "Optional: Configure BrowserStack in .env file for cross-browser testing:" -ForegroundColor Yellow
Write-Host "  BROWSERSTACK_USER=your_username" -ForegroundColor White
Write-Host "  BROWSERSTACK_KEY=your_key" -ForegroundColor White
Write-Host ""

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Optionally run the scraper
$runNow = Read-Host "Run the scraper now? (y/n)"
if ($runNow -eq "y" -or $runNow -eq "Y") {
    Write-Host ""
    Write-Host "Starting El País Scraper..." -ForegroundColor Green
    Write-Host ""
    python main.py
} else {
    Write-Host "Setup complete. You can run 'python main.py' whenever you're ready." -ForegroundColor Green
}
