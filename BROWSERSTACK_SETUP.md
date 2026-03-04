# 🌐 BrowserStack Setup Guide

This guide explains how to set up and run the El País scraper on **BrowserStack with 5 parallel threads** across multiple browsers and devices.

---

## 📋 Prerequisites

✅ **Already Installed:**
- Python 3.13
- All dependencies (from `requirements.txt`)

✅ **You Need:**
- BrowserStack account (free trial available)
- BrowserStack username and API key

---

## 🔑 Step 1: Get BrowserStack Credentials

### Option A: Free Trial (Recommended for Testing)

1. Go to [https://www.browserstack.com](https://www.browserstack.com)
2. Click **"Sign Up"** (free trial available)
3. Complete registration
4. Go to **Account Settings** → **API Keys**
5. Copy your **username** and **access key**

### Option B: Existing Account
If you already have a BrowserStack account:
1. Log in at [https://www.browserstack.com/accounts/settings](https://www.browserstack.com/accounts/settings)
2. Navigate to **API Keys**
3. Copy your **username** and **access key**

---

## 🔐 Step 2: Configure Environment Variables

### On Windows (PowerShell)

#### Method 1: Create `.env` File (Recommended)

1. Navigate to the project folder:
```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
```

2. Copy the example file:
```powershell
Copy-Item .env.example .env
```

3. Edit `.env` file with your credentials:
```bash
# Replace with your actual BrowserStack credentials
BROWSERSTACK_USER=your_username_here
BROWSERSTACK_KEY=your_access_key_here
HEADLESS_MODE=false
```

#### Method 2: Set System Environment Variables

```powershell
[Environment]::SetEnvironmentVariable("BROWSERSTACK_USER", "your_username", "User")
[Environment]::SetEnvironmentVariable("BROWSERSTACK_KEY", "your_access_key", "User")
```

Then restart PowerShell for changes to take effect.

#### Method 3: Inline (For Testing)

```powershell
$env:BROWSERSTACK_USER = "your_username"
$env:BROWSERSTACK_KEY = "your_access_key"
python main.py --browsers 5
```

---

## ✅ Step 3: Verify BrowserStack Credentials

Run this quick test to verify your credentials are working:

```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
python -c "import os; print('BROWSERSTACK_USER:', os.getenv('BROWSERSTACK_USER')); print('BROWSERSTACK_KEY:', os.getenv('BROWSERSTACK_KEY', 'NOT SET')[:5] + '...' if os.getenv('BROWSERSTACK_KEY') else 'NOT SET')"
```

Expected output:
```
BROWSERSTACK_USER: your_username
BROWSERSTACK_KEY: your_...
```

---

## 🚀 Step 4: Run on BrowserStack

### Run 5 Parallel Browser Tests

```powershell
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
python main.py --browsers 5
```

This will test across:
1. **Windows 11 - Chrome** (Desktop)
2. **Windows 11 - Firefox** (Desktop)
3. **macOS Sonoma - Safari** (Desktop)
4. **Android 13 - Chrome** (Mobile)
5. **iOS 17.2 - Safari** (Mobile)

### Expected Output

```
[PHASE 3] BROWSERSTACK CROSS-BROWSER TESTING
────────────────────────────────────────────────
Running 5 parallel browser tests...

✓ Windows 11 - Chrome (Desktop)          [PASSED] ✓ 5 articles scraped
✓ Windows 11 - Firefox (Desktop)         [PASSED] ✓ 5 articles scraped
✓ macOS Sonoma - Safari (Desktop)        [PASSED] ✓ 5 articles scraped
✓ Android 13 - Chrome (Mobile)          [PASSED] ✓ 5 articles scraped
✓ iOS 17.2 - Safari (Mobile)            [PASSED] ✓ 5 articles scraped

Test Duration: 45.2 seconds
Success Rate: 100% (5/5 tests passed)
```

---

## 📊 Browser Configurations

The solution tests these 5 specific configurations:

| # | Browser | OS | Version | Type |
|---|---------|----|----|------|
| 1 | Chrome | Windows 11 | Latest | Desktop |
| 2 | Firefox | Windows 11 | Latest | Desktop |
| 3 | Safari | macOS Sonoma | Latest | Desktop |
| 4 | Chrome | Android 13 | Latest | Mobile |
| 5 | Safari | iOS 17.2 | Latest | Mobile |

**All run in parallel** using ThreadPoolExecutor with 5 workers.

---

## 🔍 Detailed BrowserStack Testing Workflow

### What Happens During Testing

1. **Parallel Execution:**
   - 5 threads start simultaneously
   - Each thread controls a different browser/device combination
   - Tests run concurrently on BrowserStack's remote servers

2. **Per-Browser Test:**
   - Navigate to El País Opinion section
   - Verify Spanish language (lang="es-ES")
   - Scrape first 5 articles
   - Extract titles, content, images
   - Generate test results

3. **Reporting:**
   - Individual test results saved to `test_reports/browserstack_results.json`
   - Summary printed to console
   - Pass/fail status for each browser

---

## 📈 View Test Results

### Live Results

During execution, view real-time results on BrowserStack dashboard:
```
https://www.browserstack.com/dashboard
```

### Local Results

After execution, view detailed results:

```powershell
# View JSON report
Get-Content test_reports\browserstack_results.json

# View formatted summary
python -c "import json; r = json.load(open('test_reports/browserstack_results.json')); [print(f\"{x['config']}: {x['status']}\") for x in r['tests']]"
```

---

## 🛠️ Troubleshooting

### Issue: "BrowserStack credentials not found"

**Solution:** Verify credentials are set correctly:

```powershell
# Check environment variables
$env:BROWSERSTACK_USER
$env:BROWSERSTACK_KEY

# Or check .env file exists and has content
Get-Content .env
```

### Issue: "Authentication failed"

**Solution:** Verify your credentials are correct:
1. Log in to BrowserStack at [https://www.browserstack.com](https://www.browserstack.com)
2. Go to **Account Settings** → **API Keys**
3. Copy the exact **username** and **access key**
4. Update `.env` file with correct values

### Issue: "Connection timeout"

**Solution:** This usually means network issue or BrowserStack is unreachable:
```powershell
# Check internet connection
Test-NetConnection browserstack.com -Port 443

# Try again with verbose logging
python main.py --browsers 5 --verbose
```

### Issue: "Not enough quota"

**Solution:** BrowserStack free trial has session limits:
- Free tier: Limited concurrent sessions
- Upgrade account or wait for reset
- Check usage at [https://www.browserstack.com/dashboard](https://www.browserstack.com/dashboard)

---

## 💡 Advanced Configuration

### Custom Number of Tests

Run only 2 browsers instead of 5:

```powershell
python main.py --browsers 2
```

### Local Testing (Without BrowserStack)

If credentials not available, falls back to local Chrome:

```powershell
python main.py --local-only
```

### Debug Mode

Run with verbose logging:

```powershell
python main.py --browsers 5 --verbose
```

---

## 📝 Complete Example Workflow

Here's a complete example from start to finish:

```powershell
# 1. Navigate to project
cd c:\Users\ADMIN\pro\proj\el_pais_scraper

# 2. Create .env from example
Copy-Item .env.example .env

# 3. Edit .env with your BrowserStack credentials
# (Use Notepad or VS Code)
notepad .env

# 4. Verify credentials work
python -c "import os; print(f'Configured: {os.getenv(\"BROWSERSTACK_USER\")}')"

# 5. Run 5 parallel browser tests
python main.py --browsers 5

# 6. View results
Get-Content test_reports\browserstack_results.json | ConvertFrom-Json | Select-Object -ExpandProperty tests | Format-Table
```

---

## 🎯 What Gets Tested

Each browser test verifies:

✅ **Navigation:**
- ✓ Loads El País website
- ✓ Navigates to Opinion section
- ✓ Verifies Spanish language

✅ **Scraping:**
- ✓ Extracts 5+ articles
- ✓ Gets titles (in Spanish)
- ✓ Gets article content
- ✓ Gets image URLs

✅ **Image Handling:**
- ✓ Downloads cover images
- ✓ Saves to local disk
- ✓ Handles missing images gracefully

✅ **Error Handling:**
- ✓ Recovers from network errors
- ✓ Handles missing elements
- ✓ Provides detailed logging

---

## 📊 Performance Expectations

| Configuration | Typical Time |
|---|---|
| Single test (one browser) | 8-12 seconds |
| 5 parallel tests | 10-15 seconds (parallel, not sequential) |
| Full run (scraping + translation + analysis) | 20-30 seconds |

---

## ✨ Success Indicators

You know everything is working when:

1. ✅ `.env` file created with real credentials
2. ✅ `main.py --browsers 5` completes without authentication errors
3. ✅ All 5 browser tests show **[PASSED]** status
4. ✅ Test report generated in `test_reports/browserstack_results.json`
5. ✅ Each test successfully scraped articles

---

## 📞 Getting Help

### BrowserStack Support
- Official docs: [https://www.browserstack.com/docs](https://www.browserstack.com/docs)
- API reference: [https://www.browserstack.com/docs/automate/selenium/getting-started](https://www.browserstack.com/docs/automate/selenium/getting-started)

### Local Testing Fallback
If BrowserStack issues occur, test locally first:
```powershell
python main.py --local-only --articles 5
```

---

## 🎉 You're Ready!

You now have a complete multi-browser testing solution that:
- ✅ Tests across 5 different browser/device combinations
- ✅ Runs in parallel on BrowserStack infrastructure
- ✅ Demonstrates professional testing practices
- ✅ Shows enterprise-grade cross-browser compatibility

**Next step:** Follow the complete flow in [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)

---

**Status:** ✅ Ready for BrowserStack execution  
**Last Updated:** March 4, 2026
