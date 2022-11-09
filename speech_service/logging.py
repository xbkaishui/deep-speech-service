# encoding: utf-8

import logging
import os
import sys
from types import FrameType
from typing import cast

from loguru import logger

from speech_service.config import DEBUG, LOG_PATH

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOGGING_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # disable access log
    logging_logger = logging.getLogger("uvicorn.access")
    logging_logger.handlers = []
    logging_logger.propagate = False

    # configure loguru to stdout and file
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS,
                                "format": "{time} | {process} | {thread} | {level} | {function}:{line} {message}"}])
    info_log_path = os.path.join(LOG_PATH, 'info.log')
    error_log_path = os.path.join(LOG_PATH, 'error.log')
    logger.add(info_log_path, format="{time} | {thread} | {level} | {function}:{line} {message}", rotation="00:00",
               retention="10 days", encoding='utf-8', level='INFO', backtrace=True, diagnose=True)  # Automatically rotate too big file
    logger.add(error_log_path, format="{time} | {thread} | {level} | {function}:{line} {message}", rotation="00:00",
               retention="10 days", encoding='utf-8', level='ERROR', backtrace=True, diagnose=True)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )
