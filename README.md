# El País Web Scraper - Complete Solution

A sophisticated Python-based web scraping solution demonstrating **Selenium automation**, **API integration**, **text processing**, and **cross-browser testing** with BrowserStack.

## 📋 Features

### 1. **Web Scraping** 🕷️
- Navigate to El País (Spanish news outlet)
- Ensure Spanish language display
- Extract articles from the Opinion section
- Scrape titles, content, and cover images
- Handle dynamic content with Selenium waits

### 2. **Image Download** 📸
- Automatically download article cover images
- Save images locally with proper naming
- Handle image processing with PIL

### 3. **API Integration** 🔄
- Translate article titles using free MyMemory API
- Fallback support for Google Cloud Translation API
- Async-friendly architecture

### 4. **Text Processing** 📊
- Analyze translated headers
- Identify words repeated 2+ times across all headers
- Display word frequency statistics

### 5. **Cross-Browser Testing** 🌐
- Test on BrowserStack across 5 parallel threads
- Support for desktop browsers (Chrome, Firefox, Safari)
- Support for mobile browsers (iOS, Android)
- Detailed test reports in JSON format

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser (for local testing)
- BrowserStack account (optional, for cross-browser testing)

### Installation

1. **Clone and navigate to the project:**
```bash
cd el_pais_scraper
```

2. **Create a Python virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows PowerShell
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your credentials
```

### Configuration

#### For Local Testing (No Setup Required)
The script works out of the box with the MyMemory free translation API.

#### For BrowserStack Testing

1. Get your BrowserStack credentials from [https://www.browserstack.com/accounts/settings](https://www.browserstack.com/accounts/settings)

2. Set environment variables:
```powershell
$env:BROWSERSTACK_USER = "your_username"
$env:BROWSERSTACK_KEY = "your_key"
```

Or add to `.env` file:
```
BROWSERSTACK_USER=your_username
BROWSERSTACK_KEY=your_key
```

#### For Google Translate API (Optional)
1. Create a Google Cloud project
2. Enable the Translation API
3. Create a service account and download credentials
4. Set environment variable:
```powershell
$env:GOOGLE_TRANSLATE_API_KEY = "your_api_key"
```

## 📖 Usage

### Basic Usage - Local Testing Only

```bash
python main.py
```

### Scrape Specific Number of Articles

```bash
python main.py --articles 10
```

### Test on Specific Number of Browsers

```bash
python main.py --browsers 3
```

### Local Testing Only (Skip BrowserStack)

```bash
python main.py --local-only
```

### BrowserStack Testing Only

```bash
python main.py --browserstack-only
```

### Full Custom Run

```bash
python main.py --articles 5 --browsers 5
```

## 📁 Project Structure

```
el_pais_scraper/
├── main.py                    # Main orchestrator
├── scraper.py                 # Web scraping module
├── translator.py              # Translation & text analysis
├── browserstack_tester.py     # Cross-browser testing
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── config/                   # Configuration files
├── logs/                     # Log files
└── downloaded_images/        # Downloaded article images
```

## 🔧 Module Documentation

### ElPaisScraper Class (`scraper.py`)

**Key Methods:**
- `setup_driver()` - Initialize Selenium WebDriver
- `navigate_to_opinion()` - Navigate to Opinion section
- `set_spanish_language()` - Ensure Spanish language
- `scrape_articles(max_articles)` - Scrape article data
- `download_article_images()` - Download cover images
- `print_articles()` - Display scraped data

**Usage Example:**
```python
from scraper import ElPaisScraper

scraper = ElPaisScraper(headless=True)
scraper.setup_driver()
scraper.navigate_to_opinion()
articles = scraper.scrape_articles(max_articles=5)
scraper.download_article_images()
scraper.print_articles()
scraper.close()
```

### ArticleTranslator Class (`translator.py`)

**Key Methods:**
- `translate_titles(titles)` - Translate Spanish titles to English
- `analyze_repeated_words(titles, min_occurrences)` - Find repeated words
- `print_translated_titles()` - Display translations
- `print_word_analysis()` - Display word frequency

**Usage Example:**
```python
from translator import ArticleTranslator

translator = ArticleTranslator(use_free_api=True)
results = translator.translate_titles(spanish_titles)
translator.print_translated_titles()
repeated = translator.analyze_repeated_words(results, min_occurrences=2)
translator.print_word_analysis()
```

### BrowserStackTester Class (`browserstack_tester.py`)

**Key Methods:**
- `run_parallel_tests(num_configs)` - Execute tests in parallel
- `generate_report()` - Create test report
- `print_report()` - Display formatted report
- `save_report(filename)` - Save report to JSON

**Browser Configurations:**
1. Windows 11 - Chrome (Desktop)
2. Windows 11 - Firefox (Desktop)
3. macOS Sonoma - Safari (Desktop)
4. Android 13 - Chrome (Mobile)
5. iOS 17.2 - Safari (Mobile)

**Usage Example:**
```python
from browserstack_tester import BrowserStackTester

tester = BrowserStackTester(max_workers=5)
results = tester.run_parallel_tests(num_configs=5)
report = tester.print_report()
tester.save_report("report.json")
```

## 📊 Output Examples

### Scraped Articles
```
════════════════════════════════════════════════════════════════════════════════
EL PAÍS - SECCIÓN DE OPINIÓN (PRIMEROS 5 ARTÍCULOS)
════════════════════════════════════════════════════════════════════════════════

Artículo 1:
Título: El futuro de la política española
Contenido: En estos tiempos turbulentos, España se enfrenta a decisiones críticas...
Imagen: https://example.com/image.jpg
────────────────────────────────────────────────────────────────────────────────
```

### Translated Titles
```
════════════════════════════════════════════════════════════════════════════════
TRADUCCIÓN DE TÍTULOS AL INGLÉS
════════════════════════════════════════════════════════════════════════════════

Artículo 1:
  Original (ES): El futuro de la política española
  Traducido (EN): The future of Spanish politics
```

### Word Analysis
```
════════════════════════════════════════════════════════════════════════════════
ANÁLISIS DE PALABRAS REPETIDAS (mínimo 2 veces)
════════════════════════════════════════════════════════════════════════════════

  'politics': 3 veces
  'government': 2 veces
  'spain': 2 veces
```

### Test Report
```
════════════════════════════════════════════════════════════════════════════════
BROWSERSTACK CROSS-BROWSER TESTING REPORT
════════════════════════════════════════════════════════════════════════════════

SUMMARY
────────────────────────────────────────────────────────────────────────────────
Total Tests: 5
Passed: 4 | Failed: 1 | Errors: 0
Pass Rate: 80.0%
Total Duration: 245.32s
Total Articles Scraped: 20
```

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/
```

### Test with Coverage

```bash
pytest --cov=. tests/
```

## 🔍 Troubleshooting

### Selenium WebDriver Issues
- Ensure Chrome is installed
- WebDriver is auto-downloaded by webdriver-manager
- Check proxy settings if behind corporate firewall

### BrowserStack Connection
```powershell
# Test credentials
$env:BROWSERSTACK_USER = "your_username"
$env:BROWSERSTACK_KEY = "your_key"
python -c "import os; print(os.getenv('BROWSERSTACK_USER'))"
```

### Translation API Issues
- MyMemory API is rate-limited (~100 requests/hour free)
- For production, use Google Cloud Translation API
- Add retry logic with exponential backoff if needed

### Image Download Failures
- Check internet connection
- Verify image URLs are accessible
- Check disk space in `downloaded_images/` folder

## 📝 Logs

Logs are saved to `logs/` directory:
- `scraper.log` - Scraping operations
- `main.log` - Main workflow
- `browserstack_report.json` - Test results

## 🛠️ Advanced Features

### Custom Selectors

Modify `_extract_article_data()` in `scraper.py` for different CSS selectors:

```python
# Example: Custom selector for different HTML structure
title_elem = element.find('h2', class_='custom-title-class')
```

### Parallel Browser Testing

Adjust worker count in `main.py`:

```python
tester = BrowserStackTester(max_workers=10)  # More parallel threads
```

### Custom Translation API

Implement in `translator.py`:

```python
def _translate_with_custom_api(self, text: str) -> str:
    # Your custom translation logic
    pass
```

## 🔐 Security Best Practices

1. **Never commit credentials:**
   - Use `.env` file (added to `.gitignore`)
   - Use environment variables
   - Store secrets in secure vaults

2. **Handle sensitive data:**
   - Don't log credentials
   - Use HTTPS for API calls
   - Validate SSL certificates

3. **User-Agent headers:**
   - Websites respect proper User-Agent headers
   - Avoid aggressive scraping patterns

## 📚 Technologies Used

- **Selenium WebDriver** - Browser automation
- **BeautifulSoup** - HTML parsing
- **Requests** - HTTP client
- **Pillow** - Image processing
- **MyMemory API** - Free translation service
- **Google Cloud Translation** - Optional premium translation
- **BrowserStack** - Cross-browser testing platform
- **Python concurrent.futures** - Parallel execution

## 📄 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify environment variables are set correctly

## 🎯 Performance Notes

- **Scraping:** ~15-30 seconds for 5 articles
- **Translation:** ~2-5 seconds per title (MyMemory API)
- **Image Download:** ~10-20 seconds for 5 images
- **BrowserStack Tests:** ~4-6 minutes total for 5 browsers (parallel)

## 🔄 CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: python main.py --local-only
```

---

**Created:** 2024
**Version:** 1.0.0
