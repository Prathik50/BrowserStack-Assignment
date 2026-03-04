"""
Simple Examples - El País Scraper Usage Patterns
Run these examples to understand how to use each module
"""

# Example 1: Basic Web Scraping
# ============================================================================

def example_basic_scraping():
    """Scrape articles from El País Opinion section"""
    from scraper import ElPaisScraper
    
    # Create scraper instance
    scraper = ElPaisScraper(headless=True)
    
    try:
        # Setup WebDriver
        scraper.setup_driver()
        
        # Navigate to Opinion section
        scraper.navigate_to_opinion()
        
        # Scrape articles
        articles = scraper.scrape_articles(max_articles=5)
        
        # Print results
        scraper.print_articles()
        
        # Download images
        images = scraper.download_article_images()
        print(f"\nDownloaded {len(images)} images")
        
    finally:
        scraper.close()


# Example 2: Translation and Analysis
# ============================================================================

def example_translation():
    """Translate titles and analyze word frequency"""
    from translator import ArticleTranslator
    
    # Sample Spanish titles
    titles = [
        "El futuro de la política española",
        "Cómo cambia la economía mundial",
        "La importancia de la educación",
        "Los retos de la tecnología",
        "España en la encrucijada política"
    ]
    
    # Create translator
    translator = ArticleTranslator(use_free_api=True)
    
    # Translate titles
    results = translator.translate_titles(titles)
    
    # Print translations
    translator.print_translated_titles()
    
    # Analyze word frequency
    repeated_words = translator.analyze_repeated_words(results, min_occurrences=2)
    
    print("\nRepeated words (2+ occurrences):")
    for word, count in repeated_words.items():
        print(f"  '{word}': {count} times")


# Example 3: Complete Workflow
# ============================================================================

def example_complete_workflow():
    """Run complete scraping, translation, and analysis"""
    from scraper import ElPaisScraper
    from translator import ArticleTranslator
    
    print("="*80)
    print("COMPLETE WORKFLOW EXAMPLE")
    print("="*80)
    
    # Step 1: Scrape
    print("\n[STEP 1] Scraping articles...")
    scraper = ElPaisScraper(headless=True)
    articles = []
    
    try:
        scraper.setup_driver()
        scraper.navigate_to_opinion()
        articles = scraper.scrape_articles(max_articles=5)
        print(f"✓ Scraped {len(articles)} articles")
    finally:
        scraper.close()
    
    # Step 2: Download images
    print("\n[STEP 2] Downloading images...")
    try:
        images = scraper.download_article_images()
        print(f"✓ Downloaded {len(images)} images")
    except Exception as e:
        print(f"⚠ Image download failed: {e}")
    
    # Step 3: Translate
    print("\n[STEP 3] Translating titles...")
    translator = ArticleTranslator(use_free_api=True)
    titles = [article['title'] for article in articles]
    results = translator.translate_titles(titles)
    print(f"✓ Translated {len(results)} titles")
    
    # Step 4: Analyze
    print("\n[STEP 4] Analyzing repeated words...")
    repeated = translator.analyze_repeated_words(results, min_occurrences=2)
    print(f"✓ Found {len(repeated)} repeated words")
    
    # Print summary
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE")
    print("="*80)
    print(f"Articles scraped: {len(articles)}")
    print(f"Images downloaded: {len(images) if 'images' in locals() else 0}")
    print(f"Titles translated: {len(results)}")
    print(f"Repeated words found: {len(repeated)}")


# Example 4: Cross-Browser Testing
# ============================================================================

def example_cross_browser_testing():
    """Run cross-browser tests on BrowserStack"""
    from browserstack_tester import BrowserStackTester
    
    print("="*80)
    print("CROSS-BROWSER TESTING EXAMPLE")
    print("="*80)
    
    # Create tester
    tester = BrowserStackTester(max_workers=5)
    
    # Check credentials
    if not tester.bs_available:
        print("""
        ⚠ BrowserStack not configured
        To enable cross-browser testing:
        
        1. Sign up at https://www.browserstack.com
        2. Set environment variables:
           set BROWSERSTACK_USER=your_username
           set BROWSERSTACK_KEY=your_key
        3. Re-run this example
        """)
        return
    
    # Run tests
    print("\nRunning tests on 5 browser configurations...")
    results = tester.run_parallel_tests(num_configs=5)
    
    # Print report
    tester.print_report()
    
    # Save report
    tester.save_report("test_report.json")
    print("\nReport saved to test_report.json")


# Example 5: Error Handling
# ============================================================================

def example_error_handling():
    """Demonstrate error handling"""
    from scraper import ElPaisScraper
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    scraper = ElPaisScraper(headless=True)
    
    try:
        scraper.setup_driver()
        scraper.navigate_to_opinion()
        
        # Handle case where no articles found
        articles = scraper.scrape_articles(max_articles=5)
        
        if not articles:
            logger.warning("No articles found!")
            return
        
        print(f"✓ Successfully scraped {len(articles)} articles")
        
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        scraper.close()
        logger.info("Cleanup complete")


# Example 6: Custom Configuration
# ============================================================================

def example_custom_configuration():
    """Use custom configuration"""
    from scraper import ElPaisScraper
    
    # Custom settings
    config = {
        'headless': False,  # Show browser
        'max_articles': 10,
        'max_wait_time': 30
    }
    
    # Create scraper with custom config
    scraper = ElPaisScraper(headless=config['headless'])
    
    try:
        scraper.setup_driver()
        scraper.navigate_to_opinion()
        
        # Use custom max_articles
        articles = scraper.scrape_articles(max_articles=config['max_articles'])
        
        print(f"Scraped {len(articles)} articles with custom config")
        
    finally:
        scraper.close()


# Example 7: Using Individual Functions
# ============================================================================

def example_individual_functions():
    """Use specific functions without full workflow"""
    from translator import ArticleTranslator
    
    # Just translate without scraping
    titles = [
        "Breaking news from Spain",
        "Economic updates"
    ]
    
    translator = ArticleTranslator(use_free_api=True)
    
    # Translate just one title
    try:
        translated = translator._translate_with_free_api(titles[0])
        print(f"Original: {titles[0]}")
        print(f"Translated: {translated}")
    except Exception as e:
        print(f"Translation failed: {e}")
    
    # Analyze words without full workflow
    mock_results = [
        {'original': 'T1', 'translated': 'This is a test and this is great'},
        {'original': 'T2', 'translated': 'This test is important and great'},
    ]
    
    repeated = ArticleTranslator.analyze_repeated_words(mock_results, min_occurrences=2)
    print(f"\nRepeated words: {repeated}")


# Example 8: Logging Configuration
# ============================================================================

def example_logging_setup():
    """Setup logging for debugging"""
    import logging
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured")
    logger.debug("Debug information")
    logger.warning("Warning message")
    logger.error("Error message")


# Example 9: CLI Usage
# ============================================================================

def example_cli_usage():
    """Examples of CLI usage"""
    print("""
    COMMAND LINE EXAMPLES:
    
    # Basic usage
    python main.py
    
    # Scrape more articles
    python main.py --articles 10
    
    # Test more browsers
    python main.py --browsers 3
    
    # Local testing only
    python main.py --local-only
    
    # Custom parameters
    python main.py --articles 5 --browsers 2
    
    # Get help
    python main.py --help
    """)


# Example 10: Integration with Other Tools
# ============================================================================

def example_integration():
    """Integrate with other Python libraries"""
    from scraper import ElPaisScraper
    import pandas as pd
    
    # Example: Save to CSV using pandas
    scraper = ElPaisScraper(headless=True)
    
    try:
        scraper.setup_driver()
        scraper.navigate_to_opinion()
        articles = scraper.scrape_articles(max_articles=5)
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'title': a['title'],
                'content': a['content'][:100] if a['content'] else '',
                'image_url': a['image_url']
            }
            for a in articles
        ])
        
        # Save to CSV
        df.to_csv('articles.csv', index=False)
        print("✓ Saved articles to articles.csv")
        
    except Exception as e:
        print(f"Integration failed: {e}")
    finally:
        scraper.close()


# Main Menu
# ============================================================================

if __name__ == "__main__":
    import sys
    
    examples = {
        '1': ('Basic Scraping', example_basic_scraping),
        '2': ('Translation & Analysis', example_translation),
        '3': ('Complete Workflow', example_complete_workflow),
        '4': ('Cross-Browser Testing', example_cross_browser_testing),
        '5': ('Error Handling', example_error_handling),
        '6': ('Custom Configuration', example_custom_configuration),
        '7': ('Individual Functions', example_individual_functions),
        '8': ('Logging Setup', example_logging_setup),
        '9': ('CLI Usage', example_cli_usage),
        '10': ('Integration', example_integration),
    }
    
    print("\n" + "="*80)
    print("EL PAÍS SCRAPER - CODE EXAMPLES")
    print("="*80)
    
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    
    print("\nSelect an example to run (1-10) or 'all' to run all: ")
    choice = input().strip()
    
    if choice == 'all':
        for key, (name, func) in examples.items():
            print(f"\n{'='*80}")
            print(f"Running: {name}")
            print('='*80)
            try:
                func()
            except Exception as e:
                print(f"Error: {e}")
    elif choice in examples:
        name, func = examples[choice]
        print(f"\n{'='*80}")
        print(f"Running: {name}")
        print('='*80)
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice!")
