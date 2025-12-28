import os
import logging

from cbz_editor.config import config_exists

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


def check_cbz_directory_exists() -> None:
    """Checks if the CBZ directory exists."""
    if not os.path.exists(CBZ_DIR):
        logger.error(f"CBZ directory '{CBZ_DIR}' does not exist. Please run 'init' first.")
        raise FileNotFoundError(f"CBZ directory '{CBZ_DIR}' does not exist. Please run 'init' first.")

def check_temp_directory_exists() -> None:
    """Checks if the TEMP directory exists."""
    if not os.path.exists(TEMP_DIR):
        logger.error(f"TEMP directory '{TEMP_DIR}' does not exist. Please run 'init' first.")
        raise FileNotFoundError(f"TEMP directory '{TEMP_DIR}' does not exist. Please run 'init' first.")

def check_if_project_initialized() -> None:
    """Checks if the project has been initialized by verifying the existence of CBZ and TEMP directories."""
    check_cbz_directory_exists()
    check_temp_directory_exists()
    config_exists()
