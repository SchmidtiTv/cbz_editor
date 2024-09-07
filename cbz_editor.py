import os
import zipfile
import shutil
import logging
from xml.etree.ElementTree import Element, SubElement, tostring
import click
from math import ceil
from tqdm import tqdm

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
@click.option('--move-originals', is_flag=True, help="Move original files to a temp folder after processing.")
def process(volume_number: int, output_dir: str, move_originals: bool) -> None:
    """Process CBZ files and rename images for the given volume."""
    try:
        series_name, writer_name = load_config()
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    extract_cbz_and_rename_images(CBZ_DIR, output_dir, volume_number, series_name, writer_name, move_originals)

def extract_cbz_and_rename_images(cbz_directory: str, output_directory: str, volume_number: int, series_name: str, writer_name: str, move_originals: bool) -> None:
    current_number = 1
    total_page_count = 0
    create_directory(output_directory)

    # Handle title.jpg
    title_jpg_path = os.path.join(cbz_directory, "title.jpg")
    if os.path.exists(title_jpg_path):
        cover_path = os.path.join(output_directory, "001.jpg")
        shutil.copyfile(title_jpg_path, cover_path)
        click.echo(f"Cover image 'title.jpg' found and copied as '001.jpg'")
        total_page_count += 1
        current_number = 2

    # Handle additional p(n).jpg images
    p_images = sorted([f for f in os.listdir(cbz_directory) if f.lower().startswith('p(') and f.lower().endswith('.jpg')])
    for i, p_image in enumerate(p_images, start=current_number):
        p_image_path = os.path.join(cbz_directory, p_image)
        new_filename = f"{i:03d}.jpg"
        shutil.copyfile(p_image_path, os.path.join(output_directory, new_filename))
        click.echo(f"Added additional image '{p_image}' as '{new_filename}'")
        total_page_count += 1
        current_number = i + 1

    # Process CBZ files and rename images
    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])
    for cbz_file in tqdm(cbz_files, desc="Processing CBZ files"):
        chapter_folder = os.path.join(output_directory, os.path.splitext(cbz_file)[0])
        create_directory(chapter_folder)

        with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
            zip_ref.extractall(chapter_folder)

        current_number, total_page_count = rename_images_in_folder(chapter_folder, output_directory, current_number, total_page_count)

    # Create ComicInfo.xml
    create_comicinfo_xml(output_directory, f"Volume {volume_number}", series_name, total_page_count, volume_number, writer_name)

    # Combine into CBZ
    create_combined_cbz(output_directory, f"Volume_{volume_number}.cbz")
    
    # Move original files if requested
    if move_originals:
        move_to_temp_folder(cbz_files, title_jpg_path, p_images, cbz_directory, volume_number)

def rename_images_in_folder(chapter_folder: str, output_directory: str, current_number: int, total_page_count: int) -> tuple[int, int]:
    """Rename images in the given folder."""
    image_files = [f for f in sorted(os.listdir(chapter_folder)) if f.lower().endswith(('.jpg', '.jpeg'))]
    for filename in tqdm(image_files, desc="Renaming images"):
        new_filename = f"{current_number:03d}.jpg"
        src = os.path.join(chapter_folder, filename)
        dst = os.path.join(output_directory, new_filename)
        shutil.move(src, dst)
        current_number += 1
        total_page_count += 1
    return current_number, total_page_count

def create_comicinfo_xml(output_directory: str, volume_title: str, series_name: str, page_count: int, volume_number: int, writer_name: str) -> None:
    """Creates a ComicInfo.xml file in the output directory."""
    comic_info = Element("ComicInfo", {
        "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })

    title = SubElement(comic_info, "Title")
    title.text = volume_title

    series = SubElement(comic_info, "Series")
    series.text = series_name

    volume = SubElement(comic_info, "Volume")
    volume.text = str(volume_number)

    page_count_element = SubElement(comic_info, "PageCount")
    page_count_element.text = str(page_count)

    if writer_name:
        writer_element = SubElement(comic_info, "Writer")
        writer_element.text = writer_name

    comic_info_str = tostring(comic_info, encoding='utf-8', method='xml').decode('utf-8')

    with open(os.path.join(output_directory, "ComicInfo.xml"), 'w', encoding='utf-8') as f:
        f.write(comic_info_str)
    logging.info(f"ComicInfo.xml created in {output_directory}")

def create_combined_cbz(output_directory: str, cbz_filename: str) -> None:
    """Creates a combined CBZ file."""
    cbz_path = os.path.join(output_directory, cbz_filename)
    with zipfile.ZipFile(cbz_path, 'w') as cbz_file:
        for root, _, files in os.walk(output_directory):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=output_directory)
                cbz_file.write(file_path, arcname)
    click.echo(f"Combined CBZ file created: {cbz_path}")

def move_to_temp_folder(cbz_files: list, title_jpg_path: str, p_images: list, cbz_directory: str, volume_number: int) -> None:
    """Moves original CBZ files and images to a temporary folder."""
    temp_dir = os.path.join(TEMP_DIR, f"Volume_{volume_number}")
    create_directory(temp_dir)

    # Move CBZ files
    for cbz_file in cbz_files:
        src = os.path.join(cbz_directory, cbz_file)
        dst = os.path.join(temp_dir, cbz_file)
        shutil.move(src, dst)
        logging.info(f"Moved '{cbz_file}' to '{temp_dir}'")

    # Move title.jpg
    if os.path.exists(title_jpg_path):
        shutil.move(title_jpg_path, os.path.join(temp_dir, "title.jpg"))
        logging.info(f"Moved 'title.jpg' to '{temp_dir}'")

    # Move additional p(n).jpg images
    for p_image in p_images:
        shutil.move(os.path.join(cbz_directory, p_image), os.path.join(temp_dir, p_image))
        logging.info(f"Moved '{p_image}' to '{temp_dir}'")

if __name__ == '__main__':
    cli()
