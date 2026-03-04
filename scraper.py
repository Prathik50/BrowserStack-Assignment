"""
El País Web Scraper with Translation and Image Download
Demonstrates: Web Scraping, API Integration, Text Processing, Cross-Browser Testing
"""

import os
import sys
import logging
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ElPaisScraper:
    """Scrapes articles from El País Opinion section"""
    
    BASE_URL = "https://www.elpais.com"
    OPINION_URL = "https://www.elpais.com/opinion/"
    MAX_WAIT_TIME = 20
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper with Selenium WebDriver
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.articles_data = []
        self.images_directory = Path("downloaded_images")
        self.images_directory.mkdir(exist_ok=True)
        logger.info("ElPaisScraper initialized")
    
    def setup_driver(self, browser_stack=False, capabilities=None):
        """Setup Selenium WebDriver
        
        Args:
            browser_stack: Use BrowserStack remote driver
            capabilities: Custom capabilities for remote driver
        """
        try:
            if browser_stack and capabilities:
                self.driver = self._setup_browserstack_driver(capabilities)
                logger.info(f"BrowserStack driver initialized with {capabilities}")
            else:
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                
                # Try to get ChromeDriver with timeout handling
                try:
                    service = Service(ChromeDriverManager(timeout=10).install())
                except Exception as e:
                    logger.warning(f"ChromeDriverManager download failed, using auto driver path: {e}")
                    # Fallback: Let Selenium find Chrome automatically without explicit driver path
                    service = None
                
                self.driver = webdriver.Chrome(service=service, options=options) if service else webdriver.Chrome(options=options)
                logger.info("Local Chrome driver initialized")
                
        except Exception as e:
            logger.error(f"Failed to setup driver: {e}")
            raise
    
    def _setup_browserstack_driver(self, capabilities):
        """Setup BrowserStack remote driver
        
        Args:
            capabilities: Browser capabilities for BrowserStack
        """
        from config import Config
        
        bs_url = Config.get_browserstack_url()
        
        if not bs_url:
            raise ValueError("BrowserStack credentials not configured. Run: python main.py --setup-browserstack USERNAME KEY")
        
        logger.info(f"Connecting to BrowserStack at {bs_url[:50]}...")
        return webdriver.Remote(command_executor=bs_url, options=capabilities)
    
    def set_spanish_language(self):
        """Ensure website is displayed in Spanish"""
        try:
            wait = WebDriverWait(self.driver, self.MAX_WAIT_TIME)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            
            # Check current language and switch if needed
            current_url = self.driver.current_url
            if "en.elpais.com" in current_url:
                logger.info("Switching from English to Spanish version")
                spanish_url = current_url.replace("en.elpais.com", "elpais.com")
                self.driver.get(spanish_url)
            
            # Set language preference cookie
            try:
                self.driver.add_cookie({
                    'name': 'locale',
                    'value': 'es',
                    'domain': '.elpais.com'
                })
            except:
                logger.debug("Could not set locale cookie")
            
            # Verify language is Spanish by checking HTML lang attribute
            html_elem = self.driver.find_element(By.TAG_NAME, "html")
            lang_attr = html_elem.get_attribute("lang")
            logger.info(f"HTML lang attribute: {lang_attr}")
            
            if lang_attr and lang_attr.startswith("es"):
                logger.info(f"[SUCCESS] Confirmed: Website is in Spanish (lang={lang_attr})")
            else:
                logger.warning(f"Website lang attribute is '{lang_attr}', expected 'es-ES' or 'es'")
            
            logger.info("Spanish language configuration complete")
            time.sleep(2)
            
        except Exception as e:
            logger.warning(f"Could not set Spanish language: {e}")
    
    def navigate_to_opinion(self):
        """Navigate to El País Opinion section"""
        try:
            logger.info(f"Navigating to {self.OPINION_URL}")
            self.driver.get(self.OPINION_URL)
            
            wait = WebDriverWait(self.driver, self.MAX_WAIT_TIME)
            
            # Try multiple selectors to find article elements (more robust)
            article_found = False
            selectors = [
                (By.CSS_SELECTOR, "article"),
                (By.CSS_SELECTOR, "article.c.c-d"),
                (By.CSS_SELECTOR, "div[data-component='Article']"),
                (By.XPATH, "//article"),
                (By.XPATH, "//h2[@class]")
            ]
            
            for selector_type, selector_value in selectors:
                try:
                    logger.info(f"Trying selector: {selector_type} = {selector_value}")
                    wait.until(EC.presence_of_all_elements_located((selector_type, selector_value)))
                    logger.info(f"[SUCCESS] Found article elements using: {selector_value}")
                    article_found = True
                    break
                except:
                    logger.debug(f"Selector failed: {selector_value}")
                    continue
            
            if not article_found:
                logger.warning("Could not find articles with any selector, but page loaded")
            
            # Ensure Spanish language
            self.set_spanish_language()
            
            # Try to find and verify Opinion section header
            try:
                opinion_header = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Opini')]"))
                )
                logger.info(f"[SUCCESS] Found Opinion section header: {opinion_header.text}")
            except:
                logger.warning("Could not locate Opinion section header, but page loaded")
            
            time.sleep(2)
            logger.info("Successfully navigated to Opinion section")
            
        except Exception as e:
            logger.error(f"Failed to navigate to Opinion section: {e}")
            raise
    
    def scrape_articles(self, max_articles: int = 5) -> List[Dict]:
        """Scrape articles from Opinion section
        
        Args:
            max_articles: Maximum number of articles to scrape
            
        Returns:
            List of article data dictionaries
        """
        try:
            wait = WebDriverWait(self.driver, self.MAX_WAIT_TIME)
            
            # Wait for page to load
            time.sleep(3)  # Allow JavaScript to render all content
            
            # Parse page with BeautifulSoup for easier data extraction
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            articles = []
            
            logger.info("Attempting to find article containers...")
            
            # Strategy 1: Find all article tags (most common)
            article_elements_html = soup.find_all('article', limit=max_articles * 3)
            logger.info(f"Strategy 1 (article tags): Found {len(article_elements_html)} elements")
            
            # Strategy 2: Find all h2/h3 links (fallback - these are usually article headlines)
            if len(article_elements_html) < max_articles:
                logger.info("Strategy 2 (finding h2/h3 headlines)...")
                headlines = soup.find_all(['h2', 'h3'], limit=max_articles * 5)
                article_elements_html = []
                for h in headlines:
                    # Get the link inside the headline
                    link = h.find('a', href=True)
                    if link:
                        # Use parent or the header itself as container
                        parent = h.parent if h.parent else h
                        article_elements_html.append(parent)
                logger.info(f"Strategy 2 (h2/h3 links): Found {len(article_elements_html)} elements")
            
            # Strategy 3: Look for specific El Pais structure
            if len(article_elements_html) < max_articles:
                logger.info("Strategy 3 (El Pais specific structure)...")
                # Look for elements with data attributes or specific classes
                all_items = soup.find_all(['div', 'li'], attrs={'data-id': True}, limit=max_articles * 3)
                if all_items:
                    article_elements_html = all_items
                    logger.info(f"Strategy 3 (data attributes): Found {len(article_elements_html)} elements")
            
            # Strategy 4: Just find all links and extract surrounding context
            if len(article_elements_html) < max_articles:
                logger.info("Strategy 4 (raw link extraction)...")
                all_links = soup.find_all('a', href=True, limit=max_articles * 10)
                article_elements_html = []
                for link in all_links:
                    # Filter for article-like links
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    if href and text and len(text) > 5 and ('/opinion/' in href or '/articulo/' in href or '/cultura/' in href):
                        # Get parent element as context
                        parent = link.parent if link.parent else link
                        article_elements_html.append(parent)
                        if len(article_elements_html) >= max_articles * 3:
                            break
                logger.info(f"Strategy 4 (link extraction): Found {len(article_elements_html)} elements")
            
            if not article_elements_html:
                logger.warning("Could not find any article containers with any strategy")
                logger.info("Dumping page structure for debugging...")
                # Save page for debugging
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                logger.info("Page source saved to debug_page.html for inspection")
                return []
            
            logger.info(f"[SUCCESS] Found {len(article_elements_html)} potential article elements")
            
            # Extract article data from containers
            for idx, element in enumerate(article_elements_html[:max_articles * 3]):
                try:
                    article_data = self._extract_article_data(element)
                    if article_data and article_data.get('title'):
                        articles.append(article_data)
                        if len(articles) >= max_articles:
                            break
                        logger.info(f"[SUCCESS] Extracted article {len(articles)}: {article_data['title'][:60]}...")
                        
                except Exception as e:
                    logger.debug(f"Error extracting article {idx}: {e}")
                    continue
            
            self.articles_data = articles
            logger.info(f"[SUCCESS] Successfully scraped {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to scrape articles: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def _extract_article_data(self, element) -> Dict:
        """Extract data from an article element
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            Dictionary containing article data
        """
        try:
            article = {
                'title': None,
                'content': None,
                'image_url': None,
                'article_url': None
            }
            
            # Extract title - first try to find h1, h2, h3 directly
            for tag in ['h1', 'h2', 'h3']:
                title_elem = element.find(tag)
                if title_elem:
                    article['title'] = title_elem.get_text(strip=True)
                    break
            
            # If no heading found, look for a link's text
            if not article['title']:
                link_elem = element.find('a', href=True)
                if link_elem:
                    article['title'] = link_elem.get_text(strip=True)
            
            # Clean up the title - remove timestamps and extra info
            if article['title']:
                # Remove author names and dates (after | symbol)
                if '|' in article['title']:
                    article['title'] = article['title'].split('|')[0].strip()
                # Remove common section prefixes
                for prefix in ['EDITORIAL', 'TRIBUNA', 'DEBATE', 'EXPOSICION', 'EXPOS', 'editorial']:
                    if article['title'].upper().startswith(prefix.upper()):
                        article['title'] = article['title'][len(prefix):].strip()
                        break
                # Limit length
                if len(article['title']) > 150:
                    article['title'] = article['title'][:150] + '...'
            
            # Extract content - look for any paragraph
            paragraphs = element.find_all('p')
            if paragraphs:
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 30:  # Skip very short paragraphs
                        article['content'] = text[:300]  # First 300 chars
                        break
            
            if not article['content']:
                # Fallback: take meaningful text from element
                all_text = element.get_text(strip=True)
                if all_text and len(all_text) > 50:
                    article['content'] = all_text[50:300]
            
            # Extract image URL - look for any image
            img_elem = element.find('img')
            if img_elem:
                article['image_url'] = img_elem.get('src') or img_elem.get('data-src')
                if article['image_url'] and not article['image_url'].startswith('http'):
                    article['image_url'] = urljoin(self.BASE_URL, article['image_url'])
            
            # Extract article URL - look for first link with href
            link_elem = element.find('a', href=True)
            if link_elem:
                article['article_url'] = link_elem.get('href')
                if not article['article_url'].startswith('http'):
                    article['article_url'] = urljoin(self.BASE_URL, article['article_url'])
            
            # Only return if we have at least a title (and it's not too generic)
            if article['title'] and len(article['title']) > 5 and article['title'].lower() not in ['editorial', 'debate', 'tribuna']:
                return article
            elif article['title'] and len(article['title']) > 20:  # Accept longer generic titles
                return article
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting article data: {e}")
            return None
    
    def download_article_images(self) -> Dict[str, str]:
        """Download and save cover images for articles
        
        Returns:
            Dictionary mapping article titles to image file paths
        """
        image_map = {}
        
        if not self.articles_data:
            logger.warning("No articles to download images for")
            return image_map
        
        for idx, article in enumerate(self.articles_data, 1):
            if article.get('image_url'):
                try:
                    logger.info(f"Downloading image for article {idx}: {article['title'][:50]}...")
                    
                    # Use requests library to download image
                    response = requests.get(article['image_url'], timeout=10)
                    response.raise_for_status()
                    
                    # Sanitize filename
                    safe_title = "".join(c for c in article['title'][:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"article_{idx}_{safe_title}.jpg"
                    filepath = self.images_directory / filename
                    
                    # Open image with Pillow and save
                    img = Image.open(BytesIO(response.content))
                    img.save(filepath, 'JPEG', quality=85)
                    
                    image_map[article['title']] = str(filepath)
                    logger.info(f"[SUCCESS] Image saved: {filepath}")
                    
                except requests.exceptions.Timeout:
                    logger.warning(f"Timeout downloading image for article {idx}: {article['image_url'][:50]}...")
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request error downloading image for article {idx}: {e}")
                except Exception as e:
                    logger.warning(f"Failed to process image for article {idx}: {e}")
        
        logger.info(f"[SUCCESS] Downloaded {len(image_map)} images successfully")
        return image_map
    
    def print_articles(self):
        """Print article titles and content in Spanish"""
        print("\n" + "="*100)
        print("EL PAIS - SECCION DE OPINION (PRIMEROS 5 ARTICULOS - DATOS EN VIVO)")
        print("="*100 + "\n")
        
        if not self.articles_data:
            print("[ERROR] No articles were scraped from the Opinion section")
            return
        
        for idx, article in enumerate(self.articles_data, 1):
            print(f"[ARTICLE {idx}]")
            print(f"   Titulo: {article.get('title', 'N/A')}")
            print(f"   Contenido: {article.get('content', 'N/A')[:150]}...")
            if article.get('image_url'):
                print(f"   Imagen URL: {article['image_url'][:70]}...")
            if article.get('article_url'):
                print(f"   Enlace: {article['article_url'][:70]}...")
            print("-" * 100 + "\n")
        
        print(f"[SUCCESS] Total de articulos extraidos: {len(self.articles_data)}")
        print("="*100 + "\n")
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")


if __name__ == "__main__":
    scraper = ElPaisScraper(headless=True)
    try:
        scraper.setup_driver()
        scraper.navigate_to_opinion()
        articles = scraper.scrape_articles(max_articles=5)
        scraper.print_articles()
        scraper.download_article_images()
    finally:
        scraper.close()
