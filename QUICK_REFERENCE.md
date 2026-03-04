# QUICK REFERENCE - El País Scraper

## 🚀 Get Started in 60 Seconds

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run (local only)
python main.py --local-only

# Done! Check output for:
# ✓ 5 articles found
# ✓ 2 images downloaded  
# ✓ 5 titles translated
# ✓ Word analysis complete
```

---

## 📋 All Commands

```powershell
# Show configuration
python main.py --config

# Local scraping only
python main.py --local-only --articles 5

# Setup BrowserStack credentials
python main.py --setup-browserstack USERNAME ACCESS_KEY

# BrowserStack tests only
python main.py --browserstack-only --browsers 5

# Full workflow (scraping + BrowserStack)
python main.py --articles 5 --browsers 5
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Main orchestrator |
| `scraper.py` | Selenium scraping |
| `translator.py` | API + text analysis |
| `browserstack_tester.py` | Cross-browser testing |
| `config.py` | Configuration management |
| `.env` | Credentials & settings |
| `requirements.txt` | Dependencies |

---

## ✅ Features

1. **Web Scraping** - Finds articles from El País
2. **Real API** - Translates Spanish→English  
3. **Text Analysis** - Word frequency counting
4. **Image Download** - Saves article images
5. **5 Parallel Threads** - ThreadPoolExecutor
6. **BrowserStack** - Cloud cross-browser testing

---

## 🧪 Test Output

```
[SUCCESS] Found 5 articles from El País Opinion
[SUCCESS] Downloaded 2 images successfully
[SUCCESS] Translated 5 titles to English
[SUCCESS] Analyzed word frequency
[SUCCESS] Ready for BrowserStack testing
```

---

## 🔑 BrowserStack Setup

### Quick Setup
```powershell
python main.py --setup-browserstack YOUR_USERNAME YOUR_ACCESS_KEY
```

### Get Credentials
1. Go to https://www.browserstack.com
2. Sign in
3. Account → Settings → Automate
4. Copy Username and Access Key

### Verify Setup
```powershell
python main.py --config
```

Should show: `BrowserStack User: *** [CONFIGURED]`

---

## 📊 What It Does

```
[PHASE 1] WEB SCRAPING
↓
Find El País Opinion articles → Extract titles, content, URLs, images
↓
[PHASE 2] API INTEGRATION  
↓
Translate Spanish titles to English via MyMemory API
↓
[PHASE 3] TEXT ANALYSIS
↓
Analyze word frequency in translations
↓
[PHASE 4] BROWSERSTACK TESTING (Optional)
↓
Test on 5 browser configurations in parallel
```

---

## 🛠️ Configuration

Edit `.env` file:

```ini
BROWSERSTACK_USER=your_username
BROWSERSTACK_KEY=your_access_key
HEADLESS_MODE=true
MAX_ARTICLES=5
MAX_WAIT_TIME=20
LOG_LEVEL=INFO
```

---

## 📍 Output Locations

| Output | Location |
|--------|----------|
| Logs | `logs/scraper.log`, `logs/main.log` |
| Images | `downloaded_images/article_*.jpg` |
| Reports | `logs/browserstack_report.json` |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| No articles found | Check internet, El País might be down |
| Images not downloading | Run `python main.py --local-only` to debug |
| API timeout | Check internet, try again in a moment |
| BrowserStack fails | Run `python main.py --setup-browserstack USER KEY` |

---

## 📞 Help

- **Setup issues?** Read `BROWSERSTACK_CREDENTIALS_SETUP.md`
- **Want details?** Read `README_FINAL_SETUP.md`
- **Submission help?** Read `SUBMISSION_INSTRUCTIONS.md`
- **Code details?** See inline comments in each module

---

## ✨ Key Points

✅ **Real Selenium** - Not simulated  
✅ **Real API** - Not mocked  
✅ **Production Code** - Error handling, logging, config  
✅ **Cloud Ready** - BrowserStack support  
✅ **Fallback Safe** - Works without credentials  
✅ **Well Documented** - Complete guides included  

---

## 🎯 Success Indicators

When you run `python main.py --local-only`, you should see:

```
[SUCCESS] WebDriver initialized
[SUCCESS] Navigated to Opinion section
[SUCCESS] Found 15 potential article elements
[SUCCESS] Extracted article 1: [Spanish title]...
[SUCCESS] Extracted article 2: ...
[SUCCESS] Extracted article 3: ...
[SUCCESS] Extracted article 4: ...
[SUCCESS] Extracted article 5: ...
[SUCCESS] Successfully scraped 5 articles
[SUCCESS] Downloaded 2 images
[SUCCESS] Real API Call Success Rate: 100%
[SUCCESS] Successfully translated 5 titles
```

✅ If you see this = Everything works!

---

## 🚀 Ready?

```powershell
python main.py --local-only
```

Then check:
- ✅ Logs show 5 articles found
- ✅ `downloaded_images/` has images
- ✅ Translations in output
- ✅ Word analysis complete

**You're done!** 🎉

---

**Quick Links:**
- [Setup Guide](BROWSERSTACK_CREDENTIALS_SETUP.md)
- [Project README](README_FINAL_SETUP.md)
- [Submission Help](SUBMISSION_INSTRUCTIONS.md)
- [Full Status](FINAL_STATUS.md)
