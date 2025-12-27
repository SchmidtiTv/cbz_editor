import os
import logging

logger = logging.getLogger(__name__)

CBZ_DIR = 'cbz'
TEMP_DIR = 'temp'


def create_directory(directory: str) -> None:
    """Creates a directory if it doesn't already exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Directory created: {directory}")
    else:
        logger.info(f"Directory already exists: {directory}")

