from dataclasses import asdict
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from services.entities import ProductUrls

import structlog
from logger import configure_logging
configure_logging()
logger = structlog.get_logger(__name__)
from db.mongodb import MongoDB

class CrawlerServiceRepository:
    
    class CrawlerServiceRepositoryError(Exception):
        pass

    def __init__(self):
        self.mongo_conn = MongoDB(db_name="ecommerce_crawler")
        
    def save_crawled_data(self, data: ProductUrls):
        try:
            crawled_data = asdict(data)
            self.mongo_conn.save_documents("product_urls", [crawled_data])
        except self.mongo_conn.MongoDBError as e:
            logger.error(f"Error saving crawled data to MongoDB: {e}")
            raise self.CrawlerServiceRepositoryError(f"Error saving crawled data to MongoDB: {e}")
