import os
import sys

from celery import Celery
from celery.signals import setup_logging

from logger import configure_logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from config import BROKER_URL

app = Celery("crawler_processor", broker=BROKER_URL, include=["tasks"])
# If a worker shuts down before acknowledging a task, the broker will requeue the task.
app.autodiscover_tasks()
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.broker_transport_options = {'visibility_timeout': 3600}
app.conf.broker_connection_retry_on_startup = True


# @setup_logging.connect
# def setup_structlog_logging(**kwargs):
#     configure_logging()

