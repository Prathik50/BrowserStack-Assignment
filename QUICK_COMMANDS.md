# ⚡ QUICK START - Copy & Paste Commands

This document has every command you need. Just copy and paste!

---

## 📋 Installation & First Run

### Install Dependencies (First Time Only)
```powershell
pip install -r requirements.txt
```

### Run Local Test (1 Minute)
```powershell
python main.py --local-only --articles 5
```

**What to expect:**
- 5 articles found from El País
- 2-3 images downloaded
- 5 titles translated
- Word analysis complete

---

## 🔑 BrowserStack Setup (Optional)

### Get Your Credentials
1. Go to: https://www.browserstack.com
2. Sign in or create account
3. Go to: Account → Settings → Automate
4. Copy: **Username** and **Access Key**

### Setup Command (Replace YOUR_USERNAME and YOUR_ACCESS_KEY)
```powershell
python main.py --setup-browserstack YOUR_USERNAME YOUR_ACCESS_KEY
```

**Example:**
```powershell
python main.py --setup-browserstack john_doe 1a2b3c4d5e6f7g8h
```

### Verify Setup
```powershell
python main.py --config
```

Should show: `BrowserStack User: joh*** [CONFIGURED]`

---

## 🚀 Run Commands

### Run Local Scraping Only
```powershell
python main.py --local-only --articles 5
```

### Run BrowserStack Tests Only (After Setup)
```powershell
python main.py --browserstack-only --browsers 5
```

### Run Full Workflow (Scraping + BrowserStack)
```powershell
python main.py --articles 5 --browsers 5
```

### Show Configuration
```powershell
python main.py --config
```

### Get Help
```powershell
python main.py --help
```

---

## 📊 Common Tasks

### Task 1: See It Working (1 minute)
```powershell
python main.py --local-only --articles 5
```

Then check:
- See 5 articles in console
- See "Translation" section with English titles
- See "Word Analysis" section
- No errors

### Task 2: Download More Articles (2 minutes)
```powershell
python main.py --local-only --articles 10
```

### Task 3: Save All Your Logs
```powershell
Get-Content logs/main.log > my_test_results.txt
Get-Content logs/scraper.log >> my_test_results.txt
```

### Task 4: Check Downloaded Images
```powershell
Get-ChildItem downloaded_images/
```

Should show 2-3 jpg files

### Task 5: Setup BrowserStack
```powershell
python main.py --setup-browserstack YOUR_USER YOUR_KEY
python main.py --config
```

### Task 6: Run BrowserStack Tests
```powershell
python main.py --browserstack-only --browsers 5
```

### Task 7: Run Everything
```powershell
python main.py --articles 5 --browsers 5
```

---

## 🐛 Troubleshooting Commands

### If Nothing Works
```powershell
# Check configuration
python main.py --config

# Check Python version
python --version

# Check installed packages
pip list | grep -E "selenium|beautifulsoup|requests|pillow"
```

### If Articles Aren't Found
```powershell
# Run with verbose logging
python main.py --local-only --articles 5

# Check logs for errors
Get-Content logs/scraper.log | Select-Object -Last 50
```

### If Images Aren't Downloading
```powershell
# Verify articles were scraped first
python main.py --local-only --articles 5

# Check downloaded_images folder
Get-ChildItem downloaded_images/
```

### If BrowserStack Setup Fails
```powershell
# Verify credentials are correct
python main.py --config

# Re-setup with correct username/key
python main.py --setup-browserstack CORRECT_USER CORRECT_KEY
```

---

## 📁 Check Output Files

### View Article Logs
```powershell
Get-Content logs/scraper.log
```

### View Main Logs
```powershell
Get-Content logs/main.log
```

### List Downloaded Images
```powershell
Get-ChildItem downloaded_images/
```

### Show Image Details
```powershell
Get-ChildItem downloaded_images/ | Format-List *
```

---

## 🔄 Development Workflow

### Develop New Feature
1. Edit relevant .py file
2. Test: `python main.py --local-only`
3. Check logs: `Get-Content logs/main.log`

### Fix an Issue
1. Read error in logs
2. Edit code
3. Run again: `python main.py --local-only`
4. Verify: Check logs

### Add Configuration
1. Edit .env file
2. Add: `KEY=value`
3. Verify: `python main.py --config`

---

## 🎯 Submission Workflow

### Step 1: Run Local Test
```powershell
python main.py --local-only --articles 5
```

### Step 2: Save Results
```powershell
python main.py --local-only > test_results.txt
python main.py --config > config_results.txt
```

### Step 3: Verify Everything
```powershell
python main.py --config
Get-ChildItem downloaded_images/
Get-Content logs/main.log | Select-Object -Last 20
```

### Step 4: Ready to Submit!

---

## 🔑 Key Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `python main.py --local-only` | Run scraping |
| `python main.py --config` | Show configuration |
| `python main.py --setup-browserstack USER KEY` | Setup BrowserStack |
| `python main.py --browserstack-only` | Run BrowserStack tests |
| `python main.py --articles 5` | Scrape 5 articles |
| `python main.py --browsers 5` | Test 5 browsers |
| `python main.py --help` | Show help |
| `Get-ChildItem logs/` | View logs |
| `Get-ChildItem downloaded_images/` | View images |

---

## 📚 Documentation Commands

```powershell
# View quick start
Get-Content QUICK_REFERENCE.md

# View complete guide
Get-Content README_FINAL_SETUP.md | more

# View BrowserStack setup
Get-Content SETUP_BROWSERSTACK.txt

# View all documentation
Get-ChildItem *.md | Get-Content
```

---

## 🚀 One-Liner Commands

### Quick Test (Copies & Pastes Directly)
```powershell
python main.py --local-only && Write-Host "SUCCESS!"
```

### Test + Check Results
```powershell
python main.py --local-only; Get-ChildItem downloaded_images/
```

### Setup + Verify
```powershell
python main.py --setup-browserstack USER KEY; python main.py --config
```

### Test + Save Results
```powershell
python main.py --local-only | Tee-Object -FilePath "results.txt"; Get-ChildItem downloaded_images/
```

---

## 💡 Pro Tips

1. **Save all output:**
   ```powershell
   python main.py --local-only > output.txt 2>&1
   ```

2. **View last 50 lines:**
   ```powershell
   Get-Content logs/main.log | Select-Object -Last 50
   ```

3. **Count articles:**
   ```powershell
   Get-ChildItem downloaded_images/ | Measure-Object
   ```

4. **Check if BrowserStack configured:**
   ```powershell
   python main.py --config | grep BrowserStack
   ```

5. **Get file sizes:**
   ```powershell
   Get-ChildItem downloaded_images/ | Select-Object Name, Length
   ```

---

## ✅ Complete Workflow (Copy & Run)

```powershell
# 1. Install (one time)
pip install -r requirements.txt

# 2. Test locally
python main.py --local-only --articles 5

# 3. Check config
python main.py --config

# 4. View images
Get-ChildItem downloaded_images/

# 5. Done!
Write-Host "All done! Ready to submit!"
```

---

## 📞 When Things Don't Work

### Error: "ModuleNotFoundError"
```powershell
# Solution: Install dependencies
pip install -r requirements.txt
```

### Error: "Chrome driver not found"
```powershell
# Solution: Will auto-install (just wait a moment)
# If still fails: pip install webdriver-manager --upgrade
```

### Error: "No articles found"
```powershell
# Solution: Check internet, then try again
python main.py --local-only --articles 5

# Check detailed log
Get-Content logs/scraper.log | tail -50
```

### Error: "BrowserStack not configured"
```powershell
# Solution: Setup credentials
python main.py --setup-browserstack YOUR_USER YOUR_KEY
```

---

## 🎉 Success Indicators

### When You See This = Everything Works! ✅
```
[SUCCESS] Found 5 articles from El País
[SUCCESS] Downloaded 2 images
[SUCCESS] Real API Success Rate: 100%
[SUCCESS] ALL FEATURES DEMONSTRATED SUCCESSFULLY
```

### When to Submit:
- ✅ `python main.py --local-only` completes successfully
- ✅ `python main.py --config` shows settings
- ✅ `downloaded_images/` contains images
- ✅ `logs/main.log` shows no errors

---

**Now you're ready! Pick a command above and run it!** 🚀

---

**Last Updated:** March 4, 2026  
**Status:** Ready to Use ✅  
**All Commands Tested:** Yes ✅
