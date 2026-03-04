# El País Scraper - Quick Start Guide

## 🚀 30-Second Setup

### On Windows PowerShell:

```powershell
# 1. Navigate to project directory
cd el_pais_scraper

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the scraper
python main.py
```

## ✨ Available Commands

```powershell
# Default: Scrape 5 articles, test 5 browsers locally
python main.py

# Scrape 10 articles only
python main.py --articles 10

# Local testing only (no BrowserStack)
python main.py --local-only

# Cross-browser testing on 3 browsers
python main.py --browsers 3

# Scrape articles + test on specific browsers
python main.py --articles 5 --browsers 5

# Get help
python main.py --help
```

## 📊 Expected Output

The script will produce:

1. **Console Output:**
   - Article titles and content in Spanish
   - Translated titles in English
   - Word frequency analysis
   - Test results summary

2. **Downloaded Files:**
   - Article cover images in `downloaded_images/` folder
   - Log files in `logs/` folder
   - Test report in `logs/browserstack_report.json`

3. **Log Files:**
   - `logs/scraper.log` - Scraping operations
   - `logs/main.log` - Main workflow
   - `logs/browserstack_report.json` - Test results

## 🔧 Optional Configuration

### For BrowserStack Testing:

1. Sign up at https://www.browserstack.com
2. Get credentials from account settings
3. Set environment variables:

```powershell
$env:BROWSERSTACK_USER = "your_username"
$env:BROWSERSTACK_KEY = "your_key"

# Then run
python main.py --browsers 5
```

### For Google Translate API:

1. Create Google Cloud project
2. Enable Translation API
3. Set environment variable:

```powershell
$env:GOOGLE_TRANSLATE_API_KEY = "your_key"
```

## ❓ Troubleshooting

### Issue: Module not found
**Solution:** Make sure you activated the virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: Chrome not found
**Solution:** Install Chrome or let webdriver-manager auto-download it
```powershell
pip install --upgrade webdriver-manager
```

### Issue: Can't connect to El País
**Solution:** Check your internet connection or try with VPN

### Issue: Translation API rate limit
**Solution:** Wait a few minutes or use Google Translate API instead

## 📚 Full Documentation

For detailed information, see `README.md`

## 💡 Quick Examples

### Example 1: Basic Scraping
```python
from scraper import ElPaisScraper

scraper = ElPaisScraper(headless=True)
scraper.setup_driver()
scraper.navigate_to_opinion()
articles = scraper.scrape_articles(max_articles=5)
scraper.print_articles()
scraper.close()
```

### Example 2: Translation and Analysis
```python
from translator import ArticleTranslator

translator = ArticleTranslator(use_free_api=True)
titles = ["El futuro de España", "La política actual"]
results = translator.translate_titles(titles)
translator.print_translated_titles()
translator.print_word_analysis()
```

### Example 3: Custom Browser Testing
```python
from browserstack_tester import BrowserStackTester

tester = BrowserStackTester(max_workers=3)
results = tester.run_parallel_tests(num_configs=3)
tester.print_report()
```

## 🎯 Project Structure

```
el_pais_scraper/
├── main.py                  # Main entry point
├── scraper.py               # Web scraping
├── translator.py            # Translation & analysis
├── browserstack_tester.py   # Cross-browser testing
├── setup.py                 # Setup wizard
├── requirements.txt         # Dependencies
├── .env.example            # Configuration template
├── README.md               # Full documentation
└── QUICKSTART.md           # This file
```

## 🔗 Useful Links

- **El País:** https://www.elpais.com
- **Selenium:** https://selenium.dev
- **BrowserStack:** https://www.browserstack.com
- **BeautifulSoup:** https://www.crummy.com/software/BeautifulSoup/
- **MyMemory API:** https://mymemory.translated.net/

## 📞 Need Help?

1. Check the logs in `logs/` directory
2. Review error messages
3. See README.md for detailed documentation
4. Check test output for specific errors

## ✅ Success Indicators

You'll know it's working when you see:
- ✓ Articles being scraped
- ✓ Images being downloaded
- ✓ Titles being translated
- ✓ Word frequency analysis
- ✓ Test results summary

Enjoy scraping! 🕷️
