"""
Comprehensive Execution Guide and Examples
Run this script to demonstrate all features of the El País Scraper
"""

import os
import sys
from pathlib import Path

# Example usage patterns and demonstrations

DEMO_SCRIPT = """
# ============================================================================
# EL PAÍS WEB SCRAPER - COMPLETE DEMONSTRATION
# ============================================================================
# This script demonstrates all capabilities of the El País scraper with
# web scraping, API integration, text processing, and cross-browser testing

import logging
import sys
from scraper import ElPaisScraper
from translator import ArticleTranslator
from browserstack_tester import BrowserStackTester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*100)
print("EL PAÍS WEB SCRAPER - COMPLETE DEMONSTRATION")
print("="*100)

# ============================================================================
# PHASE 1: WEB SCRAPING
# ============================================================================
print("\\n[PHASE 1] WEB SCRAPING WITH SELENIUM")
print("-"*100)

logger.info("Initializing web scraper...")
scraper = ElPaisScraper(headless=True)

try:
    # Setup WebDriver
    logger.info("Setting up Selenium WebDriver...")
    scraper.setup_driver()
    
    # Navigate to El País Opinion section
    logger.info("Navigating to El País Opinion section...")
    scraper.navigate_to_opinion()
    
    # Ensure Spanish language
    logger.info("Ensuring Spanish language display...")
    scraper.set_spanish_language()
    
    # Scrape articles
    logger.info("Scraping first 5 articles...")
    articles = scraper.scrape_articles(max_articles=5)
    
    # Display results
    scraper.print_articles()
    
    print("\\n✓ Phase 1 Complete: Successfully scraped {0} articles".format(len(articles)))
    
except Exception as e:
    logger.error("Phase 1 failed: {0}".format(e))
    sys.exit(1)

finally:
    scraper.close()

# ============================================================================
# PHASE 2: IMAGE DOWNLOAD
# ============================================================================
print("\\n[PHASE 2] DOWNLOADING ARTICLE IMAGES")
print("-"*100)

logger.info("Downloading article cover images...")
try:
    image_map = scraper.download_article_images()
    print("\\n✓ Phase 2 Complete: Downloaded {0} images".format(len(image_map)))
    
    # Show downloaded images
    for title, filepath in image_map.items():
        print("  - {0}: {1}".format(title[:50], filepath))
        
except Exception as e:
    logger.warning("Phase 2 warning: {0}".format(e))

# ============================================================================
# PHASE 3: TRANSLATION AND TEXT ANALYSIS
# ============================================================================
print("\\n[PHASE 3] TRANSLATION AND TEXT ANALYSIS")
print("-"*100)

logger.info("Translating article titles...")
try:
    translator = ArticleTranslator(use_free_api=True)
    
    # Extract titles
    titles = [article['title'] for article in articles]
    logger.info("Extracted {0} titles for translation".format(len(titles)))
    
    # Translate titles
    translated_results = translator.translate_titles(titles)
    
    # Display translations
    translator.print_translated_titles()
    
    # Analyze repeated words
    logger.info("Analyzing word frequency in translated titles...")
    repeated_words = translator.analyze_repeated_words(
        translated_results,
        min_occurrences=2
    )
    
    translator.print_word_analysis(min_occurrences=2)
    
    print("\\n✓ Phase 3 Complete: Translated {0} titles, found {1} repeated words".format(
        len(translated_results), len(repeated_words)
    ))
    
except Exception as e:
    logger.error("Phase 3 failed: {0}".format(e))
    sys.exit(1)

# ============================================================================
# PHASE 4: CROSS-BROWSER TESTING (Optional - BrowserStack)
# ============================================================================
print("\\n[PHASE 4] CROSS-BROWSER TESTING")
print("-"*100)

logger.info("Initializing cross-browser testing...")
try:
    tester = BrowserStackTester(max_workers=5)
    
    if not tester.bs_available:
        print("\\n⚠ BrowserStack credentials not configured")
        print("  To enable BrowserStack testing:")
        print("  1. Sign up at https://www.browserstack.com")
        print("  2. Set environment variables:")
        print("     BROWSERSTACK_USER=your_username")
        print("     BROWSERSTACK_KEY=your_key")
        print("  3. Re-run the script")
    else:
        logger.info("Running parallel tests on 5 browser configurations...")
        
        # Run tests
        results = tester.run_parallel_tests(num_configs=5)
        
        # Display report
        report = tester.print_report()
        
        # Save report
        tester.save_report("logs/browserstack_test_report.json")
        
        print("\\n✓ Phase 4 Complete: Completed {0} cross-browser tests".format(len(results)))
    
except Exception as e:
    logger.warning("Phase 4 warning: {0}".format(e))

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\\n" + "="*100)
print("DEMONSTRATION COMPLETE")
print("="*100)
print("""
Summary of what was accomplished:

1. WEB SCRAPING ✓
   - Successfully navigated to El País website
   - Ensured Spanish language display
   - Scraped 5 articles from Opinion section
   - Extracted titles, content, and image URLs

2. IMAGE DOWNLOAD ✓
   - Downloaded cover images for articles
   - Saved images to 'downloaded_images/' directory

3. TEXT PROCESSING & TRANSLATION ✓
   - Translated article titles from Spanish to English
   - Analyzed word frequency in translated titles
   - Identified repeated words

4. CROSS-BROWSER TESTING ✓
   - (Configured and ready for BrowserStack)
   - Would test across 5 browser/device combinations
   - Generate detailed test reports

Output Files:
- Article images: downloaded_images/
- Logs: logs/scraper.log, logs/main.log
- Test report: logs/browserstack_test_report.json

For more information, see README.md or QUICKSTART.md
""")
print("="*100)
"""

def print_menu():
    """Print interactive menu"""
    print("\n" + "="*100)
    print("EL PAÍS SCRAPER - EXECUTION MODES")
    print("="*100)
    print("""
1. Quick Start (Default)
   Command: python main.py
   What it does: Scrapes 5 articles, translates, downloads images, tests locally
   Time: ~2-3 minutes

2. Full Local Demo
   Command: python main.py --articles 5
   What it does: Same as quick start with detailed output
   Time: ~2-3 minutes

3. Advanced Scraping (10 articles)
   Command: python main.py --articles 10
   What it does: Scrapes 10 articles instead of 5
   Time: ~4-5 minutes

4. Cross-Browser Testing (Requires BrowserStack)
   Command: python main.py --browsers 5
   What it does: Tests on 5 different browsers in parallel
   Time: ~4-6 minutes
   Prerequisites: BROWSERSTACK_USER and BROWSERSTACK_KEY environment variables

5. Full Workflow (Everything)
   Command: python main.py --articles 5 --browsers 5
   What it does: Complete scraping + cross-browser testing
   Time: ~6-9 minutes
   Prerequisites: BrowserStack credentials (optional, will skip if not available)

6. Local Only (No BrowserStack)
   Command: python main.py --local-only
   What it does: Scraping, translation, analysis - no cross-browser testing
   Time: ~2-3 minutes

7. Custom Configuration
   Command: python main.py --articles 3 --browsers 2
   What it does: Scrape 3 articles, test 2 browser configurations
   Time: ~1-2 minutes

COMMON PATTERNS:
═══════════════════════════════════════════════════════════════════════════════

Quick Test (1 minute):
  python main.py --articles 3 --browsers 1 --local-only

Production Run (5 minutes):
  python main.py --articles 5 --browsers 5

Deep Analysis (10+ articles):
  python main.py --articles 15

Development/Debug:
  python scraper.py          # Just test scraping
  python translator.py       # Just test translation
  python browserstack_tester.py  # Just test BrowserStack

DETAILED WORKFLOW:
═══════════════════════════════════════════════════════════════════════════════

Step 1: Activate Virtual Environment
  Windows PowerShell:
    .\\venv\\Scripts\\Activate.ps1
  
  Windows Command Prompt:
    .\\venv\\Scripts\\activate.bat

Step 2: Install Dependencies
  pip install -r requirements.txt

Step 3: Configure Environment (Optional)
  Edit .env file with BrowserStack credentials

Step 4: Run the Scraper
  python main.py

EXPECTED OUTPUT:
═══════════════════════════════════════════════════════════════════════════════

Console Output:
  ✓ Article titles in Spanish
  ✓ Article content
  ✓ Image download progress
  ✓ Translated titles in English
  ✓ Word frequency analysis
  ✓ Cross-browser test results

Log Files:
  logs/scraper.log           - Scraping operations
  logs/main.log              - Main workflow
  logs/browserstack_report.json  - Test report (if BrowserStack enabled)

Downloaded Files:
  downloaded_images/article_1_*.jpg
  downloaded_images/article_2_*.jpg
  ... (one for each article)

ADVANCED USAGE:
═══════════════════════════════════════════════════════════════════════════════

Import and Use Directly in Python:

  from scraper import ElPaisScraper
  
  scraper = ElPaisScraper(headless=False)  # Show browser
  scraper.setup_driver()
  scraper.navigate_to_opinion()
  articles = scraper.scrape_articles(max_articles=10)
  scraper.print_articles()
  scraper.close()

Use Translation Module:

  from translator import ArticleTranslator
  
  translator = ArticleTranslator(use_free_api=True)
  results = translator.translate_titles(spanish_titles)
  translator.print_translated_titles()
  
Use BrowserStack Tester:

  from browserstack_tester import BrowserStackTester
  
  tester = BrowserStackTester(max_workers=5)
  results = tester.run_parallel_tests(num_configs=5)
  tester.print_report()

TROUBLESHOOTING:
═══════════════════════════════════════════════════════════════════════════════

Issue: "ModuleNotFoundError: No module named 'selenium'"
Solution: Make sure virtual environment is activated
  .\\venv\\Scripts\\Activate.ps1

Issue: "Chrome not found"
Solution: WebDriver manager will auto-download compatible Chrome
  or install Chrome manually from https://www.google.com/chrome/

Issue: "Connection timeout to elpais.com"
Solution: Check internet connection, try with VPN

Issue: "BrowserStack authentication failed"
Solution: Verify credentials in .env or environment variables
  $env:BROWSERSTACK_USER = "your_username"
  $env:BROWSERSTACK_KEY = "your_key"

Issue: "No articles scraped"
Solution: Website layout may have changed, check logs for details
  Check: logs/scraper.log for specific errors

PERFORMANCE NOTES:
═══════════════════════════════════════════════════════════════════════════════

Scraping:           15-30 seconds (5 articles)
Image Download:     10-20 seconds (5 images)
Translation:        5-10 seconds (5 titles, using free API)
Word Analysis:      <1 second
Local BrowserStack: N/A (uses local browser)
Cross-Browser:      4-6 minutes (5 browsers, parallel)

Total Full Workflow: ~6-10 minutes

GETTING HELP:
═══════════════════════════════════════════════════════════════════════════════

1. Check logs directory for detailed error messages
2. Read README.md for comprehensive documentation
3. See QUICKSTART.md for quick reference
4. Review this file for detailed examples
5. Check individual module docstrings for API details
""")
    print("="*100)

def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*100)
    print("SETUP INSTRUCTIONS")
    print("="*100)
    print("""
WINDOWS POWERSHELL:
═══════════════════════════════════════════════════════════════════════════════

# 1. Navigate to project
cd el_pais_scraper

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\\venv\\Scripts\\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file (optional, for BrowserStack)
Copy-Item .env.example .env
# Edit .env with your credentials

# 6. Run the scraper
python main.py

WINDOWS COMMAND PROMPT:
═══════════════════════════════════════════════════════════════════════════════

cd el_pais_scraper
python -m venv venv
.\\venv\\Scripts\\activate.bat
pip install -r requirements.txt
python main.py

MACOS/LINUX:
═══════════════════════════════════════════════════════════════════════════════

cd el_pais_scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

ONE-LINER SETUP (Windows PowerShell):
═══════════════════════════════════════════════════════════════════════════════

python -m venv venv; .\\venv\\Scripts\\Activate.ps1; pip install -r requirements.txt; python main.py
""")
    print("="*100)

def main():
    """Main menu"""
    print("\n" + "="*100)
    print("EL PAÍS WEB SCRAPER - EXECUTION GUIDE")
    print("="*100)
    print("""
This is a comprehensive guide to running the El País Web Scraper.

QUICK START:
  python main.py

FILES IN THIS PROJECT:
  main.py                 - Main entry point (start here!)
  scraper.py              - Web scraping with Selenium
  translator.py           - Translation & text analysis
  browserstack_tester.py  - Cross-browser testing
  README.md               - Full documentation
  QUICKSTART.md           - Quick reference
  requirements.txt        - Python dependencies

Choose an option:
  1. Show execution modes and commands
  2. Show setup instructions
  3. Show example code
  4. Run the scraper now
  5. Exit

Enter your choice (1-5): 
""")
    
    choice = input().strip()
    
    if choice == "1":
        print_menu()
    elif choice == "2":
        print_setup_instructions()
    elif choice == "3":
        print("\n" + "="*100)
        print("EXAMPLE CODE")
        print("="*100)
        print(DEMO_SCRIPT)
    elif choice == "4":
        print("\nRunning: python main.py")
        print("="*100)
        os.system("python main.py")
    else:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    # Uncomment the line below to run in interactive mode
    # main()
    
    # Or just print the menu
    print_menu()
    print_setup_instructions()
