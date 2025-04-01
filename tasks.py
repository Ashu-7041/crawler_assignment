import os
import sys
import traceback
import structlog

from services.crawler_service.crawler import CrawlerService
from services.crawler_service.crawler_repo import CrawlerServiceRepository

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from celery_config.celery import app
from logger import configure_logging

configure_logging()
logger = structlog.get_logger()


@app.task(queue="crawler_service")
def crawler_service(ecommerce_sites: list[str]):
    try:
        logger.info("Starting Crawler service")
        service = CrawlerService(repo=CrawlerServiceRepository())
        
        # Call start_crawling directly - it already handles threading internally
        service.start_crawling(ecommerce_sites)
        
        logger.info("Crawler service completed")
    except Exception:
        logger.error("Generic error", traceback=traceback.format_exc())
    except CrawlerService.CrawlingError:
        logger.error("Error in Crawler service", traceback=traceback.format_exc())