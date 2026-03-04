"""
Configuration Module for El País Scraper
Manages environment variables, credentials, and application settings
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Central configuration management"""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    IMAGES_DIR = PROJECT_ROOT / "downloaded_images"
    
    # Ensure directories exist
    LOGS_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    
    # BrowserStack Configuration
    BROWSERSTACK_USER = os.getenv('BROWSERSTACK_USER', '').strip()
    BROWSERSTACK_KEY = os.getenv('BROWSERSTACK_KEY', '').strip()
    BROWSERSTACK_HUB_URL = f"https://{BROWSERSTACK_USER}:{BROWSERSTACK_KEY}@hub.browserstack.com/wd/hub" if BROWSERSTACK_USER and BROWSERSTACK_KEY else None
    
    # Validate BrowserStack credentials
    @classmethod
    def has_browserstack_credentials(cls) -> bool:
        """Check if BrowserStack credentials are configured"""
        return bool(cls.BROWSERSTACK_USER and cls.BROWSERSTACK_KEY) and \
               cls.BROWSERSTACK_USER != 'your_browserstack_username' and \
               cls.BROWSERSTACK_KEY != 'your_browserstack_access_key'
    
    @classmethod
    def get_browserstack_url(cls) -> Optional[str]:
        """Get BrowserStack Hub URL if credentials available"""
        if cls.has_browserstack_credentials():
            return cls.BROWSERSTACK_HUB_URL
        return None
    
    # Scraper Configuration
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
    MAX_ARTICLES = int(os.getenv('MAX_ARTICLES', '5'))
    MAX_WAIT_TIME = int(os.getenv('MAX_WAIT_TIME', '20'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    SCRAPER_LOG = LOGS_DIR / "scraper.log"
    MAIN_LOG = LOGS_DIR / "main.log"
    BROWSERSTACK_LOG = LOGS_DIR / "browserstack.log"
    
    # El País URLs
    EL_PAIS_BASE = "https://www.elpais.com"
    EL_PAIS_OPINION = "https://www.elpais.com/opinion/"
    
    # API Configuration
    MYMEMORY_API = "https://api.mymemory.translated.net/get"
    GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY', '').strip()
    
    @classmethod
    def print_config(cls):
        """Print current configuration (mask sensitive data)"""
        print("\n" + "="*80)
        print("CONFIGURATION SUMMARY")
        print("="*80)
        print(f"Project Root: {cls.PROJECT_ROOT}")
        print(f"Logs Directory: {cls.LOGS_DIR}")
        print(f"Images Directory: {cls.IMAGES_DIR}")
        print(f"Headless Mode: {cls.HEADLESS_MODE}")
        print(f"Max Articles: {cls.MAX_ARTICLES}")
        print(f"Max Wait Time: {cls.MAX_WAIT_TIME}s")
        print(f"Log Level: {cls.LOG_LEVEL}")
        
        if cls.has_browserstack_credentials():
            bs_user_masked = cls.BROWSERSTACK_USER[:3] + '*' * (len(cls.BROWSERSTACK_USER) - 3)
            bs_key_masked = cls.BROWSERSTACK_KEY[:4] + '*' * (len(cls.BROWSERSTACK_KEY) - 4)
            print(f"BrowserStack User: {bs_user_masked} [CONFIGURED]")
            print(f"BrowserStack Key: {bs_key_masked} [CONFIGURED]")
        else:
            print(f"BrowserStack: NOT CONFIGURED (set BROWSERSTACK_USER and BROWSERSTACK_KEY in .env)")
        
        print("="*80 + "\n")


class CredentialManager:
    """Manages BrowserStack credentials configuration"""
    
    ENV_FILE = Path(__file__).parent / ".env"
    
    @classmethod
    def setup_credentials(cls, username: str, access_key: str) -> bool:
        """Setup BrowserStack credentials in .env file
        
        Args:
            username: BrowserStack username
            access_key: BrowserStack access key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read existing .env content
            env_content = ""
            if cls.ENV_FILE.exists():
                with open(cls.ENV_FILE, 'r') as f:
                    env_content = f.read()
            
            # Update or add credentials
            lines = env_content.split('\n')
            updated_lines = []
            user_found = False
            key_found = False
            
            for line in lines:
                if line.startswith('BROWSERSTACK_USER='):
                    updated_lines.append(f'BROWSERSTACK_USER={username}')
                    user_found = True
                elif line.startswith('BROWSERSTACK_KEY='):
                    updated_lines.append(f'BROWSERSTACK_KEY={access_key}')
                    key_found = True
                else:
                    updated_lines.append(line)
            
            # Add if not found
            if not user_found:
                updated_lines.insert(0, f'BROWSERSTACK_USER={username}')
            if not key_found:
                updated_lines.insert(1 if user_found else 1, f'BROWSERSTACK_KEY={access_key}')
            
            # Write back to file
            with open(cls.ENV_FILE, 'w') as f:
                f.write('\n'.join(updated_lines))
            
            # Reload environment
            os.environ['BROWSERSTACK_USER'] = username
            os.environ['BROWSERSTACK_KEY'] = access_key
            
            print(f"[SUCCESS] BrowserStack credentials saved to {cls.ENV_FILE}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save credentials: {e}")
            return False
    
    @classmethod
    def verify_credentials(cls) -> bool:
        """Verify BrowserStack credentials are valid"""
        if not Config.has_browserstack_credentials():
            return False
        
        print("[SUCCESS] BrowserStack credentials are configured")
        return True
