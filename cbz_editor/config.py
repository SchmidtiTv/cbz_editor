from typing import Tuple
import os
import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring

CONFIG_FILE = 'config.xml'
logger = logging.getLogger(__name__)

def load_config() -> Tuple[str, str, str]:
    """Loads series and writer info from the config file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found. Please run 'init' first.")

    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()

    series_element = root.find('series_name')
    writer_element = root.find('writer_name')
    output_directory_schema = root.find('output_directory')

    series_name = series_element.text if (series_element is not None and series_element.text) else ""
    writer_name = writer_element.text if (writer_element is not None and writer_element.text) else ""
    output_directory_schema = output_directory_schema.text if (
            output_directory_schema is not None and output_directory_schema.text) else "Volume_%d"

    return series_name, writer_name, output_directory_schema


def save_config(series_name: str, writer_name: str, output_directory_schema: str) -> None:
    """Save the series and writer information in an XML file."""
    config = Element('config')

    series_element = SubElement(config, 'series_name')
    series_element.text = series_name

    writer_element = SubElement(config, 'writer_name')
    writer_element.text = writer_name

    output_directory_element = SubElement(config, 'output_directory')
    output_directory_element.text = output_directory_schema

    # Write XML with declaration in UTF-8
    with open(CONFIG_FILE, 'wb') as f:
        f.write(tostring(config, encoding='utf-8', xml_declaration=True))

    logger.info(
        f"Configuration saved to {CONFIG_FILE} with series '{series_name}' and writer '{writer_name}' and output directory '{output_directory_schema}'.")


def config_exists() -> None:
    """Check if the configuration file exists."""
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"Configuration file '{CONFIG_FILE}' does not exist. Please run 'init' first.")
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' does not exist. Please run 'init' first.")
