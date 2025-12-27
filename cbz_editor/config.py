from typing import Tuple
import os
import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring

CONFIG_FILE = 'config.xml'
logger = logging.getLogger(__name__)

def load_config() -> Tuple[str, str]:
    """Loads series and writer info from the config file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found. Please run 'init' first.")

    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()

    series_element = root.find('series_name')
    writer_element = root.find('writer_name')

    series_name = series_element.text if (series_element is not None and series_element.text) else ""
    writer_name = writer_element.text if (writer_element is not None and writer_element.text) else ""

    return series_name, writer_name

def save_config(series_name: str, writer_name: str) -> None:
    """Save the series and writer information in an XML file."""
    config = Element('config')

    series_element = SubElement(config, 'series_name')
    series_element.text = series_name

    writer_element = SubElement(config, 'writer_name')
    writer_element.text = writer_name

    # Write XML with declaration in UTF-8
    with open(CONFIG_FILE, 'wb') as f:
        f.write(tostring(config, encoding='utf-8', xml_declaration=True))

    logger.info(f"Configuration saved to {CONFIG_FILE}")
