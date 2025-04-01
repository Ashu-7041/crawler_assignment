import logging

import structlog


def configure_logging():
    # Set up the standard Python logger
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
            structlog.processors.add_log_level,
            structlog.contextvars.merge_contextvars,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.JSONRenderer(sort_keys=False),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
