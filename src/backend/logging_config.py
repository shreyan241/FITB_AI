# src/fitb_ai_backend/logging_config.py
from loguru import logger
import sys
import os
from pathlib import Path

# Get the base directory (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Remove default handlers to prevent duplicate logs
logger.remove()
# Add a console handler
logger.add(sys.stdout, level="DEBUG", colorize=True)
# Add a file handler
logger.add(LOGS_DIR / "app.log", rotation="10 MB", retention="14 days", level="INFO", encoding="utf-8")

# Optional: Set logger levels for different modules
# logger.disable("some_module")
