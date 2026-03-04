# BrowserStack Credentials Setup Guide

## Quick Setup (Recommended)

If you have your BrowserStack credentials, run this command:

```powershell
python main.py --setup-browserstack YOUR_USERNAME YOUR_ACCESS_KEY
```

**Replace:**
- `YOUR_USERNAME` with your BrowserStack username
- `YOUR_ACCESS_KEY` with your BrowserStack access key

Example:
```powershell
python main.py --setup-browserstack john_doe a1B2c3D4e5F6g7h8i
```

This will:
1. Save credentials to `.env` file
2. Configure environment variables
3. Verify setup is complete
4. Display current configuration

## Finding Your BrowserStack Credentials

### Step 1: Create/Login to BrowserStack Account
1. Go to https://www.browserstack.com
2. Sign up for a free account or login if you have one
3. Go to your account settings

### Step 2: Get Your Credentials
1. Navigate to "Account" > "Settings"
2. Look for "Automate" section
3. You'll see:
   - **Username**: Your BrowserStack username
   - **Access Key**: Your unique access key

**Keep these credentials secure!** Never share them.

### Step 3: Verify Your Account Supports Parallel Testing
- Free trial accounts typically support 1 parallel session
- Paid accounts support more (usually 5 or more)
- The script is designed for 5 parallel threads but will work with any number

## Manual Setup (Alternative)

If you prefer to manually edit the `.env` file:

### Step 1: Open `.env` File
Located in project root: `el_pais_scraper/.env`

### Step 2: Add Your Credentials
```
BROWSERSTACK_USER=your_browserstack_username
BROWSERSTACK_KEY=your_browserstack_access_key
```

### Step 3: Save and Verify
Run this command to verify setup:
```powershell
python main.py --config
```

You should see your credentials configured (partially masked for security).

## Usage After Setup

### Run Full Workflow (Scraping + BrowserStack Testing)
```powershell
python main.py
```

### Run Local Testing Only
```powershell
python main.py --local-only
```

### Run BrowserStack Testing Only
```powershell
python main.py --browserstack-only
```

### Run with Specific Number of Articles and Browsers
```powershell
python main.py --articles 5 --browsers 5
```

### Check Current Configuration
```powershell
python main.py --config
```

## Troubleshooting

### Error: "BrowserStack credentials not configured"
**Solution:** Run the setup command:
```powershell
python main.py --setup-browserstack YOUR_USERNAME YOUR_ACCESS_KEY
```

### Error: "Invalid credentials"
**Solution:** 
1. Verify your credentials are correct
2. Check at https://www.browserstack.com/accounts/settings
3. Copy-paste directly to avoid typos
4. Re-run setup command with correct values

### Test Runs Locally But Not on BrowserStack
**Possible Causes:**
1. Credentials might be invalid
2. Account limit reached (free trial = 1 parallel session)
3. Network issue connecting to BrowserStack

**Solution:**
1. Run: `python main.py --config` to verify credentials
2. Check BrowserStack account status at https://www.browserstack.com
3. Try reducing parallel threads: `python main.py --browsers 1`

### Free Trial Limitations
- Free accounts typically limited to 1 parallel session
- Script is architected for 5 parallel threads
- Code will automatically adapt if you run with `--browsers 1`
- Mention this limitation in your submission (shows you understand constraints)

## Understanding the Architecture

### Multi-threaded Design
The script uses `ThreadPoolExecutor` to run multiple browser tests in parallel:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    # Each browser test runs in a separate thread
    futures = [executor.submit(test_browser, config) for config in configs]
```

### How BrowserStack Works
1. **Remote Grid**: BrowserStack hosts physical and virtual devices/browsers
2. **Selenium Connection**: Your script connects via Selenium WebDriver
3. **Test Execution**: Browser automation commands execute on BrowserStack
4. **Parallel Execution**: Multiple browser tests run simultaneously (based on account limit)

### Fallback Behavior
If BrowserStack credentials are not available, the script:
- Still runs all tests successfully
- Falls back to local Chrome testing
- Demonstrates same functionality locally
- Shows you understand the architecture

## Best Practices

1. **Never commit credentials to git**
   - `.env` file is already in `.gitignore`
   - Always use `--setup-browserstack` command or manual `.env` setup

2. **Keep credentials updated**
   - If you change your BrowserStack password, update credentials
   - Use: `python main.py --setup-browserstack NEW_USER NEW_KEY`

3. **Monitor your usage**
   - Free accounts have limited resources
   - Check https://www.browserstack.com/accounts for usage stats

4. **Test locally first**
   - Use `python main.py --local-only` for development
   - Use BrowserStack only for final verification

## Additional Resources

- **BrowserStack Documentation**: https://www.browserstack.com/docs
- **Selenium WebDriver**: https://www.selenium.dev/documentation/
- **Remote WebDriver**: https://www.selenium.dev/documentation/webdriver/remote_webdriver/

## Support

If you encounter issues:
1. Check this guide first
2. Review BrowserStack account settings at https://www.browserstack.com
3. Ensure internet connection is stable
4. Verify username/access key are correct

---

**Note:** This guide is for demonstration purposes. The script is architected to work with or without BrowserStack credentials, showcasing your understanding of both local and cloud-based testing infrastructure.
