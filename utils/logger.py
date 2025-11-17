from loguru import logger
import sys
import os

os.makedirs("logs", exist_ok=True)

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level="INFO",
)
logger.add(
    "logs/runLogs.log",
    level="DEBUG",
    rotation="1 MB",
)