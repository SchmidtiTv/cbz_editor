import os
import zipfile
import shutil
import logging
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
import click
from math import ceil

CONFIG_FILE = 'config.xml'
CBZ_DIR = 'cbz'
TEMP_DIR = 'temp'

# Setup logging
logging.basicConfig(filename='cbz_editor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@click.group()
def cli() -> None:
    """CBZ Processor CLI"""
    pass

@cli.command()
@click.option('--series', help="The name of the series", required=False)
@click.option('--writer', help="The writer's name", required=False)
def init(series: str, writer: str) -> None:
    """Initialize the cbz_editor by setting up directories and storing metadata."""
    create_directory(CBZ_DIR)
    create_directory(TEMP_DIR)

    series_name = series or click.prompt("Enter the series name")
    writer_name = writer or click.prompt("Enter the writer's name (optional)", default="", show_default=False)

    save_config(series_name, writer_name)
    click.echo(f"Stored series and writer info in {CONFIG_FILE}")

def create_directory(directory: str) -> None:
    """Creates a directory if it doesn't already exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        click.echo(f"Created directory: {directory}")
        logging.info(f"Directory created: {directory}")
    else:
        click.echo(f"Directory '{directory}' already exists.")
        logging.info(f"Directory already exists: {directory}")

def save_config(series_name: str, writer_name: str) -> None:
    """Save the series and writer information in an XML file."""
    config = Element('config')
    series_element = SubElement(config, 'series_name')
    series_element.text = series_name
    
    writer_element = SubElement(config, 'writer_name')
    writer_element.text = writer_name

    tree = ElementTree(config)
    with open(CONFIG_FILE, 'wb') as f:
        tree.write(f)
    logging.info(f"Configuration saved to {CONFIG_FILE}")

@cli.command()
@click.argument('volume_number', type=int)
@click.option('--output-dir', help="The output directory for processed files", default=os.getcwd())
def process(volume_number: int, output_dir: str) -> None:
    """Process CBZ files and rename images for the given volume."""
    try:
        series_name, writer_name = load_config()
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    extract_cbz_and_rename_images(CBZ_DIR, output_dir, volume_number, series_name, writer_name)

def extract_cbz_and_rename_images(cbz_directory: str, output_directory: str, volume_number: int, series_name: str, writer_name: str) -> None:
    current_number = 1
    total_page_count = 0
    create_directory(output_directory)

    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])
    chapter_mapping = {}

    for cbz_file in cbz_files:
        try:
            chapter_str = os.path.splitext(cbz_file)[0].split(' ')[1]
            chapter_num = float(chapter_str)
            rounded_num = ceil(chapter_num)
            while rounded_num in chapter_mapping:
                rounded_num += 1
            chapter_mapping[rounded_num] = cbz_file
        except IndexError:
            logging.error(f"Error processing file: {cbz_file}")
            continue

    sorted_chapters = sorted(chapter_mapping.items())

    for idx, (chapter_number, cbz_file) in enumerate(sorted_chapters, start=1):
        volume_title = f"Chapter {idx}"
        chapter_folder = os.path.join(output_directory, volume_title)
        create_directory(chapter_folder)

        with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
            zip_ref.extractall(chapter_folder)

        current_number, total_page_count = rename_images_in_folder(chapter_folder, output_directory, current_number, total_page_count)

    create_comicinfo_xml(output_directory, f"Volume {volume_number}", series_name, total_page_count, volume_number, writer_name)
    click.echo("Extraction, renaming, and ComicInfo.xml creation completed.")

def rename_images_in_folder(chapter_folder: str, output_directory: str, current_number: int, total_page_count: int) -> tuple[int, int]:
    """Rename images in the given folder."""
    for filename in sorted(os.listdir(chapter_folder)):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            new_filename = f"{current_number:03d}.jpg"
            src = os.path.join(chapter_folder, filename)
            dst = os.path.join(output_directory, new_filename)
            shutil.move(src, dst)
            logging.info(f"Renamed and moved '{src}' to '{dst}'")
            current_number += 1
            total_page_count += 1
    return current_number, total_page_count

if __name__ == '__main__':
    cli()
