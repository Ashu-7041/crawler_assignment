from datetime import datetime
import os
import sys

from services.crawler_service.crawler_repo import CrawlerServiceRepository
from services.entities import ProductUrls

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import time
import re
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import structlog
from logger import configure_logging
configure_logging()
logger = structlog.get_logger(__name__)

class CrawlerService:
    
    class CrawlingError(Exception):
        pass
    
    def __init__(self, repo: CrawlerServiceRepository):
        self.repo = repo

    def webdriver_setup(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            return chrome_options
        except self.CrawlingError as e:
            logger.error(f"Error setting up webdriver: {e}")
            raise self.CrawlingError(f"Error setting up webdriver: {e}")

    def is_product_url(self, url: str):
        PRODUCT_PATTERNS = [r"/product/", r"/p/", r"/item/", r"/products/", r"/collections/"]
        """Check if a URL matches known product patterns."""
        return any(re.search(pattern, url) for pattern in PRODUCT_PATTERNS)

    def crawl_website(self, domain: str):
        chrome_options = self.webdriver_setup()
        logger.info(f"Started Crawling: {domain}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(domain)

        time.sleep(5)

        product_urls = set()
        links = driver.find_elements(By.TAG_NAME, "a")

        try:
            links = driver.find_elements(By.TAG_NAME, "a")
        except self.CrawlingError as e:
            logger.error(f"Error fetching links from {domain}")
            return

        if links:
            for link in links:
                url = link.get_attribute("href")
                if url and self.is_product_url(url):
                    product_urls.add(url)

        driver.quit()

        if product_urls:
            try:
                self.repo.save_crawled_data(ProductUrls(domain=domain, product_urls=list(product_urls), created_at=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            except self.repo.CrawlerServiceRepositoryError as e:
                logger.error(f"Error saving crawled data to MongoDB: {e}")
                raise self.CrawlingError(f"Error saving crawled data to MongoDB: {e}")
            
    def start_crawling(self, ecommerce_sites: list[str]):
        """Start crawling all given e-commerce sites using multi-threading."""
        threads = []
        for site in ecommerce_sites:
            thread = threading.Thread(target=self.crawl_website, args=(site,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
