import structlog
from celery_config.celery import app as celery_app
from logger import configure_logging

configure_logging()
logger = structlog.get_logger()

ecommerce_sites = [
    "https://www.virgio.com/",
    "https://www.westside.com/",
]

def trigger_crawler_service(ecommerce_sites: list[str]):
    logger.info("Triggering Crawler service", ecommerce_sites=ecommerce_sites)
    celery_app.send_task(
        "tasks.crawler_service",
        kwargs={"ecommerce_sites": ecommerce_sites},
        queue="crawler_service",
)

        
trigger_crawler_service(ecommerce_sites)