# Getting Started - El País Web Scraper

## 🚀 Fastest Setup (Windows PowerShell)

### Option 1: Automatic Setup Script (Recommended)

```powershell
# Navigate to project directory
cd c:\Users\ADMIN\pro\proj\el_pais_scraper

# Run setup script
.\setup.ps1

# Follow the prompts
```

**This will:**
1. Create virtual environment
2. Install all dependencies
3. Create .env file
4. Optionally run the scraper

### Option 2: Batch File Setup (Windows CMD)

```cmd
cd c:\Users\ADMIN\pro\proj\el_pais_scraper
setup.bat
```

### Option 3: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (optional)
copy .env.example .env

# 5. Run the scraper
python main.py
```

---

## 🎯 Run the Scraper

### Basic Run
```bash
python main.py
```

### With Options
```bash
python main.py --articles 10       # Scrape 10 articles
python main.py --browsers 5        # Test 5 browsers
python main.py --local-only        # No BrowserStack
python main.py --help              # Show all options
```

---

## 📊 What You'll See

### Console Output:
```
╔════════════════════════════════════════════════╗
║  EL PAÍS - SECCIÓN DE OPINIÓN                 ║
║  (PRIMEROS 5 ARTÍCULOS)                       ║
╚════════════════════════════════════════════════╝

Artículo 1:
Título: [Article title in Spanish]
Contenido: [Article content summary]
Imagen: [Image URL]

[... 4 more articles ...]

════════════════════════════════════════════════════════════════
TRADUCCIÓN DE TÍTULOS AL INGLÉS
════════════════════════════════════════════════════════════════

Artículo 1:
  Original (ES): [Spanish title]
  Traducido (EN): [English translation]

[... 4 more translations ...]

════════════════════════════════════════════════════════════════
ANÁLISIS DE PALABRAS REPETIDAS (mínimo 2 veces)
════════════════════════════════════════════════════════════════

  'word': 3 veces
  'another_word': 2 veces
```

---

## 📁 Output Files

### Downloaded Images
```
downloaded_images/
├── article_1_1234567890.jpg
├── article_2_1234567890.jpg
├── article_3_1234567890.jpg
├── article_4_1234567890.jpg
└── article_5_1234567890.jpg
```

### Log Files
```
logs/
├── scraper.log              # Scraping operations
├── main.log                 # Main workflow
└── browserstack_report.json # Test results (if BrowserStack used)
```

---

## 🔧 Configuration (Optional)

### For BrowserStack Testing

Edit `.env` file and add:
```
BROWSERSTACK_USER=your_username
BROWSERSTACK_KEY=your_key
```

Get credentials from: https://www.browserstack.com/accounts/settings

Then run:
```bash
python main.py --browsers 5
```

### For Google Translate API

Add to `.env`:
```
GOOGLE_TRANSLATE_API_KEY=your_api_key
```

---

## 📚 Documentation

| File | Content |
|------|---------|
| README.md | Complete reference (500+ lines) |
| QUICKSTART.md | Quick commands |
| PROJECT_SUMMARY.md | Project overview |
| INDEX.md | Complete file index |
| EXECUTION_GUIDE.py | Interactive guide |
| examples.py | 10 code examples |

---

## ✅ Verify Installation

After setup, you should see:

1. **Virtual environment created**: `venv/` folder exists
2. **Dependencies installed**: `pip list` shows all packages
3. **.env file created**: `.env` file exists
4. **Can import modules**: `python -c "from scraper import ElPaisScraper"`
5. **Can run**: `python main.py` executes successfully

---

## 🆘 Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python from https://www.python.org/

### Issue: "Permission denied" on setup.ps1
**Solution**: Run PowerShell as Administrator or:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "No module named 'selenium'"
**Solution**: Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: "Chrome not found"
**Solution**: WebDriver manager will auto-download Chrome, or install from https://www.google.com/chrome/

### Issue: No articles scraped
**Solution**: Check internet connection, try `python main.py --local-only`

---

## 💡 Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check installed packages
pip list

# Run only scraping (no translation/testing)
python scraper.py

# Run examples
python examples.py

# View help
python main.py --help
```

---

## 🎓 Learning Path

1. **First time?** Read this file (you're here!)
2. **Quick start?** See QUICKSTART.md
3. **Need details?** Read README.md
4. **Want examples?** Run `python examples.py`
5. **Understanding code?** Check inline comments in .py files

---

## 🔗 Useful Links

- **El País Website**: https://www.elpais.com
- **Selenium Documentation**: https://selenium.dev
- **BrowserStack**: https://www.browserstack.com
- **Python Documentation**: https://docs.python.org/3/
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Setup (first time) | 5-10 min |
| Scraping 5 articles | 15-30 sec |
| Translation | 5-10 sec |
| Word analysis | <1 sec |
| Image download | 10-20 sec |
| Cross-browser test | 4-6 min |
| **Complete workflow** | **6-10 min** |

---

## 🎯 Next Steps

### 1. Complete Setup
```powershell
.\setup.ps1
```

### 2. Run the Scraper
```powershell
python main.py
```

### 3. Explore Results
- Check `downloaded_images/` for article images
- Check `logs/` for detailed logs
- Review console output

### 4. Try Examples
```powershell
python examples.py
```

### 5. Read Documentation
- Open README.md
- Check QUICKSTART.md
- Review code examples

---

## 📞 Need Help?

1. **Check logs**: Look in `logs/scraper.log`
2. **Read docs**: See README.md and QUICKSTART.md
3. **Run examples**: `python examples.py`
4. **Check code**: Inline comments explain logic
5. **Try help**: `python main.py --help`

---

## ✨ You're Ready!

The system is now ready to scrape El País articles, translate them, analyze word frequency, and run cross-browser tests.

**Start with**: `python main.py`

Enjoy! 🕷️
