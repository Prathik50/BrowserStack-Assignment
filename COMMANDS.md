# 🎯 EXACT COMMANDS - Run Your Solution

Copy and paste these commands exactly to run your solution.

---

## 🚀 Option 1: Fast Demo (30 Seconds)
**Best for:** Quick verification that everything works

```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
python demo.py
```

**What you'll see:**
- 5 articles (Spanish titles + content)
- Real translation to English
- Word frequency analysis
- All in under 1 second ✓

---

## 🌐 Option 2: Live Scraping (2 Minutes)
**Best for:** Show real El País scraping, translation, and analysis

```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
python main.py --local-only --articles 5
```

**What you'll see:**
- Real Selenium WebDriver launching Chrome
- Navigate to El País Opinion section
- Verify Spanish language (lang="es-ES")
- Extract 5 real articles
- Download real images
- Translate titles to English
- Analyze repeated words

---

## 🧪 Option 3: Full Stack with BrowserStack (5 Minutes)
**Best for:** Complete demonstration of all features

**Step 1: Set up credentials**
```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
Copy-Item .env.example .env
```

Then edit `.env` with your BrowserStack credentials:
```
BROWSERSTACK_USER=your_username
BROWSERSTACK_KEY=your_api_key
```

**Step 2: Run full stack**
```powershell
python main.py --browsers 5
```

**What you'll see:**
- Phase 1: Live scraping (as above)
- Phase 2: Real translation
- Phase 3: Text analysis
- Phase 4: 5 parallel browser tests
- Professional test report

---

## 📊 Additional Commands

### Scrape More Articles
```powershell
python main.py --local-only --articles 10
```

### Test Only 2 Browsers
```powershell
python main.py --browsers 2
```

### Only BrowserStack (Skip Scraping)
```powershell
python main.py --browserstack-only --browsers 5
```

### Run Unit Tests
```powershell
pytest tests_translator.py -v
```

### View Code Examples
```powershell
python examples.py
```

### Get Help
```powershell
python main.py --help
```

---

## ✅ Verification Steps

### 1. Verify Installation
```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
python -c "import selenium, requests, bs4, PIL; print('✓ All dependencies installed')"
```

### 2. Quick Test
```powershell
python demo.py
```

Expected output: 5 articles, Spanish titles, English translations

### 3. Live Test
```powershell
python main.py --local-only --articles 2
```

Expected output: Real El País articles with images

---

## 🔧 Troubleshooting Commands

### If imports fail
```powershell
pip install -r requirements.txt
```

### If Chrome driver times out
```powershell
# Try just the demo (no driver needed)
python demo.py

# Or try with only 2 articles
python main.py --local-only --articles 2
```

### If BrowserStack credentials not found
```powershell
# Check environment variables
$env:BROWSERSTACK_USER
$env:BROWSERSTACK_KEY

# Or check .env file
Get-Content .env
```

### Check logs
```powershell
Get-Content logs/main.log | Select-Object -Last 50
```

---

## 📝 Common Command Patterns

### Run with custom settings
```powershell
# 10 articles, no BrowserStack
python main.py --local-only --articles 10

# 5 articles, 3 browser tests
python main.py --articles 5 --browsers 3

# Only BrowserStack, 5 browsers
python main.py --browserstack-only --browsers 5
```

### View results
```powershell
# View translation results
python -c "from translator import ArticleTranslator; t = ArticleTranslator()"

# View scraped images
ls downloaded_images/

# View test reports
Get-Content test_reports/browserstack_results.json
```

---

## ⚡ Quick Interview Flow

```powershell
# 1. Show it works fast (30 seconds)
python demo.py

# (Recruiter is impressed)

# 2. Show the code structure
code scraper.py
code translator.py
code browserstack_tester.py

# 3. Run live demo (2 minutes)
python main.py --local-only --articles 5

# (Recruiter sees real scraping, translation, analysis)

# 4. Explain BrowserStack testing
# (Show how to run full stack if they want to see it)
python main.py --browsers 5
# (After BrowserStack setup)
```

---

## 📋 File Locations

```powershell
# Navigate to project
cd c:\Users\ADMIN\pro\proj\el_pais_scraper

# View all files
ls -la

# View specific module
code scraper.py
code translator.py
code browserstack_tester.py
code main.py

# View documentation
code START_HERE.md
code SUBMISSION_GUIDE.md
code 3STEP_FINISH_LINE.md
code BROWSERSTACK_SETUP.md
```

---

## 🎓 Next Steps

1. **Right now:** `python demo.py`
2. **In 2 minutes:** `python main.py --local-only --articles 5`
3. **For interview:** Read `SUBMISSION_GUIDE.md`
4. **For full stack:** `python main.py --browsers 5` (after setup)

---

**You're ready!** Copy the command for your situation and run it. ✅
