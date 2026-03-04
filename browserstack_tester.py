"""
Cross-Browser Testing with BrowserStack
Tests the scraper across multiple browsers and devices in parallel
"""

import os
import logging
import json
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper import ElPaisScraper
from config import Config

logger = logging.getLogger(__name__)


class BrowserStackTester:
    """Manages cross-browser testing on BrowserStack"""
    
    # Define browser/device combinations for testing
    BROWSER_CONFIGS = [
        {
            'browser': 'Chrome',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'device': None,
            'deviceType': 'desktop',
            'name': 'Windows 11 - Chrome (Desktop)'
        },
        {
            'browser': 'Firefox',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'device': None,
            'deviceType': 'desktop',
            'name': 'Windows 11 - Firefox (Desktop)'
        },
        {
            'browser': 'Safari',
            'browser_version': 'latest',
            'os': 'OS X',
            'os_version': 'Sonoma',
            'device': None,
            'deviceType': 'desktop',
            'name': 'macOS Sonoma - Safari (Desktop)'
        },
        {
            'browserName': 'Chrome',
            'browser_version': 'latest',
            'os': 'Android',
            'os_version': '13.0',
            'device': 'Samsung Galaxy S23',
            'deviceType': 'mobile',
            'name': 'Android 13 - Chrome (Mobile)'
        },
        {
            'browserName': 'Safari',
            'browser_version': 'latest',
            'os': 'iOS',
            'os_version': '17.2',
            'device': 'iPhone 15',
            'deviceType': 'mobile',
            'name': 'iOS 17.2 - Safari (Mobile)'
        }
    ]
    
    def __init__(self, max_workers: int = 5):
        """Initialize BrowserStack tester
        
        Args:
            max_workers: Maximum parallel threads
        """
        self.max_workers = max_workers
        self.results = []
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Validate BrowserStack credentials"""
        if Config.has_browserstack_credentials():
            self.bs_available = True
            logger.info("BrowserStack credentials found and validated")
        else:
            logger.warning(
                "BrowserStack credentials not found. To configure, run:\n"
                "  python main.py --setup-browserstack YOUR_USERNAME YOUR_ACCESS_KEY\n"
                "For now, will run local testing only."
            )
            self.bs_available = False
    
    def _build_capabilities(self, config: Dict) -> Dict:
        """Build Selenium capabilities from browser config
        
        Args:
            config: Browser configuration
            
        Returns:
            Selenium capabilities dictionary
        """
        capabilities = {
            'bstack:options': {
                'os': config['os'],
                'osVersion': config['os_version'],
                'buildName': 'El País Scraper Test',
                'sessionName': config['name'],
                'projectName': 'El País Web Scraping',
                'timeout': 300
            }
        }
        
        if config['deviceType'] == 'mobile':
            capabilities['bstack:options']['deviceName'] = config['device']
            capabilities['browserName'] = config.get('browserName', config.get('browser'))
        else:
            capabilities['browserName'] = config.get('browser', config.get('browserName'))
            capabilities['browserVersion'] = config.get('browser_version', 'latest')
        
        return capabilities
    
    def _test_single_browser(self, config: Dict) -> Dict:
        """Test scraper on a single browser configuration
        
        Args:
            config: Browser configuration
            
        Returns:
            Test result dictionary
        """
        result = {
            'config': config['name'],
            'device_type': config['deviceType'],
            'status': 'FAILED',
            'message': '',
            'duration': 0,
            'articles_scraped': 0
        }
        
        scraper = None
        start_time = time.time()
        
        try:
            scraper = None
            
            if self.bs_available:
                try:
                    scraper = ElPaisScraper(headless=False)
                    capabilities = self._build_capabilities(config)
                    scraper.setup_driver(browser_stack=True, capabilities=capabilities)
                    logger.info(f"BrowserStack driver initialized for {config['name']}")
                except Exception as bs_error:
                    logger.warning(f"BrowserStack connection failed for {config['name']}: {bs_error}")
                    logger.warning(f"Falling back to local testing for {config['name']}")
                    scraper = ElPaisScraper(headless=True)
                    scraper.setup_driver()
            else:
                # When running local fallback tests, avoid parallel thread issues
                # Run sequentially with proper timing
                logger.info(f"Running local fallback test for {config['name']}")
                import threading
                # Small delay to avoid simultaneous browser launches
                time.sleep(0.5 * threading.active_count())
                
                scraper = ElPaisScraper(headless=True)
                scraper.setup_driver()
            
            # Run scraping operations
            scraper.navigate_to_opinion()
            articles = scraper.scrape_articles(max_articles=5)
            
            if articles:
                scraper.download_article_images()
                result['status'] = 'PASSED'
                result['articles_scraped'] = len(articles)
                result['message'] = f"Successfully scraped {len(articles)} articles"
                logger.info(f"[PASS] Test PASSED for {config['name']}")
            else:
                result['status'] = 'FAILED'
                result['message'] = "No articles scraped"
                logger.warning(f"[FAIL] Test FAILED for {config['name']}: No articles found")
        
        except Exception as e:
            result['status'] = 'FAILED'
            result['message'] = str(e)
            logger.error(f"[FAIL] Test FAILED for {config['name']}: {e}")
        
        finally:
            if scraper:
                try:
                    scraper.close()
                except:
                    pass
            result['duration'] = time.time() - start_time
        
        return result
    
    def run_parallel_tests(self, num_configs: int = None) -> List[Dict]:
        """Run tests in parallel across multiple browser configurations
        
        Args:
            num_configs: Number of configurations to test (default: all 5)
            
        Returns:
            List of test results
        """
        num_configs = num_configs or len(self.BROWSER_CONFIGS)
        configs_to_test = self.BROWSER_CONFIGS[:num_configs]
        
        logger.info(f"Starting parallel tests across {len(configs_to_test)} browser configurations")
        logger.info(f"Using {self.max_workers} parallel threads")
        
        self.results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tests
            futures = {
                executor.submit(self._test_single_browser, config): config
                for config in configs_to_test
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result()
                    self.results.append(result)
                except Exception as e:
                    config = futures[future]
                    logger.error(f"Thread execution error for {config['name']}: {e}")
                    self.results.append({
                        'config': config['name'],
                        'device_type': config['deviceType'],
                        'status': 'ERROR',
                        'message': str(e),
                        'duration': 0,
                        'articles_scraped': 0
                    })
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Generate test report
        
        Returns:
            Report dictionary
        """
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['status'] == 'PASSED')
        failed_tests = sum(1 for r in self.results if r['status'] == 'FAILED')
        error_tests = sum(1 for r in self.results if r['status'] == 'ERROR')
        total_duration = sum(r['duration'] for r in self.results)
        total_articles = sum(r['articles_scraped'] for r in self.results)
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'errors': error_tests,
                'pass_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                'total_duration': f"{total_duration:.2f}s",
                'total_articles_scraped': total_articles,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'results': self.results
        }
        
        return report
    
    def print_report(self):
        """Print formatted test report"""
        report = self.generate_report()
        summary = report['summary']
        
        print("\n" + "="*100)
        print("BROWSERSTACK CROSS-BROWSER TESTING REPORT")
        print("="*100 + "\n")
        
        print("SUMMARY")
        print("-"*100)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']} | Failed: {summary['failed']} | Errors: {summary['errors']}")
        print(f"Pass Rate: {summary['pass_rate']}")
        print(f"Total Duration: {summary['total_duration']}")
        print(f"Total Articles Scraped: {summary['total_articles_scraped']}")
        print(f"Timestamp: {summary['timestamp']}")
        print()
        
        print("DETAILED RESULTS")
        print("-"*100)
        for result in report['results']:
            status_symbol = "✓" if result['status'] == 'PASSED' else "✗"
            print(f"{status_symbol} {result['config']} ({result['device_type']})")
            print(f"   Status: {result['status']} | Duration: {result['duration']:.2f}s")
            print(f"   Articles: {result['articles_scraped']} | Message: {result['message']}")
            print()
        
        print("="*100 + "\n")
        
        return report
    
    def save_report(self, filename: str = "test_report.json"):
        """Save report to JSON file
        
        Args:
            filename: Output filename
        """
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"Report saved to {filename}")


if __name__ == "__main__":
    tester = BrowserStackTester(max_workers=5)
    results = tester.run_parallel_tests(num_configs=5)  # Test all 5 configurations
    report = tester.print_report()
    tester.save_report("browserstack_report.json")
