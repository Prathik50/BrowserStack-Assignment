"""
Setup and Installation Script
Helps users configure the project quickly
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def create_virtual_env():
    """Create Python virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print(f"✓ Virtual environment already exists at {venv_path}")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print(f"✓ Virtual environment created at {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def activate_venv_instruction():
    """Print virtual environment activation instruction"""
    print("\n" + "="*80)
    print("ACTIVATE VIRTUAL ENVIRONMENT")
    print("="*80)
    print("\nOn Windows PowerShell:")
    print("  .\\venv\\Scripts\\Activate.ps1\n")
    print("On Windows Command Prompt:")
    print("  .\\venv\\Scripts\\activate.bat\n")
    print("On macOS/Linux:")
    print("  source venv/bin/activate\n")
    print("="*80)


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies from requirements.txt...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from template"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print(f"✓ .env file already exists")
        return True
    
    if not env_example_path.exists():
        print("❌ .env.example not found")
        return False
    
    try:
        env_path.write_text(env_example_path.read_text())
        print(f"✓ Created .env file from template")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = ["logs", "downloaded_images", "config"]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")
    
    return True


def check_chrome_browser():
    """Check if Chrome browser is installed"""
    import platform
    
    system = platform.system()
    
    if system == "Windows":
        possible_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expandvars("%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"),
            os.path.expandvars("%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✓ Chrome browser found at: {path}")
                return True
    
    elif system == "Darwin":  # macOS
        path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(path):
            print(f"✓ Chrome browser found at: {path}")
            return True
    
    elif system == "Linux":
        import shutil
        if shutil.which("google-chrome") or shutil.which("chromium"):
            print("✓ Chrome browser found in PATH")
            return True
    
    print("⚠ Chrome browser not found. WebDriver will attempt to download a compatible version.")
    return True  # Still return True as webdriver-manager can handle this


def setup_browserstack_credentials():
    """Help user setup BrowserStack credentials"""
    print("\n" + "="*80)
    print("BROWSERSTACK SETUP (Optional)")
    print("="*80)
    print("\nTo use BrowserStack for cross-browser testing:")
    print("1. Create account at https://www.browserstack.com")
    print("2. Get your credentials from https://www.browserstack.com/accounts/settings")
    print("3. Update the .env file with:")
    print("   BROWSERSTACK_USER=your_username")
    print("   BROWSERSTACK_KEY=your_key")
    print("\nWithout BrowserStack, local testing will still work.")
    print("="*80 + "\n")


def main():
    """Main setup function"""
    print("\n" + "="*80)
    print("EL PAÍS SCRAPER - SETUP WIZARD")
    print("="*80 + "\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n[1/6] Creating directories...")
    if not create_directories():
        sys.exit(1)
    
    # Create virtual environment
    print("\n[2/6] Setting up virtual environment...")
    if not create_virtual_env():
        sys.exit(1)
    
    activate_venv_instruction()
    
    # Install dependencies
    print("\n[3/6] Installing Python dependencies...")
    if not install_dependencies():
        print("⚠ Consider running: pip install -r requirements.txt")
    
    # Create .env file
    print("\n[4/6] Setting up environment configuration...")
    if not create_env_file():
        print("⚠ Manually create .env file from .env.example")
    
    # Check Chrome browser
    print("\n[5/6] Checking Chrome browser...")
    check_chrome_browser()
    
    # BrowserStack setup info
    print("\n[6/6] BrowserStack configuration info...")
    setup_browserstack_credentials()
    
    # Final instructions
    print("\n" + "="*80)
    print("✓ SETUP COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("1. Activate virtual environment (see instructions above)")
    print("2. Edit .env file with your credentials (optional)")
    print("3. Run: python main.py\n")
    print("For more information, see README.md")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
