import os
import zipfile
import shutil
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
import click

CONFIG_FILE = 'config.xml'
CBZ_DIR = 'cbz'
TEMP_DIR = 'temp'

@click.group()
def cli() -> None:
    """CBZ Processor CLI"""
    pass

@cli.command()
def help() -> None:
    """Show help for CLI commands."""
    click.echo(cli.get_help(click.Context(cli)))

@cli.command()
def init() -> None:
    """Initialize the cbz_editor by setting up directories and storing metadata."""
    # Check or create cbz and temp directories
    if not os.path.exists(CBZ_DIR):
        os.makedirs(CBZ_DIR)
        click.echo(f"Created directory: {CBZ_DIR}")
    else:
        click.echo(f"Directory '{CBZ_DIR}' already exists.")

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        click.echo(f"Created directory: {TEMP_DIR}")
    else:
        click.echo(f"Directory '{TEMP_DIR}' already exists.")

    # Ask for series name and writer name (optional)
    series_name = click.prompt("Enter the series name")
    writer_name = click.prompt("Enter the writer's name (optional)", default="", show_default=False)

    # Save data to XML for later use
    save_config(series_name, writer_name)
    click.echo(f"Stored series and writer info in {CONFIG_FILE}")

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
    click.echo(f"Configuration saved to {CONFIG_FILE}")

def load_config() -> tuple[str, str]:
    """Load the series and writer information from the XML config file."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please run 'init' command first.")
    
    tree = parse(CONFIG_FILE)
    root = tree.getroot()
    series_name = root.find('series_name').text
    writer_name = root.find('writer_name').text

    return series_name, writer_name

@cli.command()
@click.argument('volume_number', type=int)
def process(volume_number: int) -> None:
    """Process CBZ files and rename images for the given volume."""
    # Load configuration from XML
    try:
        series_name, writer_name = load_config()
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    # Define output directory as the current directory
    output_directory = os.getcwd()

    # Process the cbz directory
    extract_cbz_and_rename_images(CBZ_DIR, output_directory, volume_number, series_name, writer_name)

def extract_cbz_and_rename_images(cbz_directory: str, output_directory: str, volume_number: int, series_name: str, writer_name: str) -> None:
    current_number = 1
    total_page_count = 0  # This will track the total number of pages across all CBZ files

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get and process CBZ files
    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])
    chapter_mapping = {}

    for cbz_file in cbz_files:
        chapter_str = os.path.splitext(cbz_file)[0].split(' ')[1]
        chapter_num = float(chapter_str)
        rounded_num = ceil(chapter_num)

        # Adjust chapters to avoid overwriting
        while rounded_num in chapter_mapping:
            rounded_num += 1

        chapter_mapping[rounded_num] = cbz_file

    # Sort by the adjusted chapter numbers
    sorted_chapters = sorted(chapter_mapping.items())

    for idx, (chapter_number, cbz_file) in enumerate(sorted_chapters, start=1):
        volume_title = f"Chapter {idx}"  # Renaming chapters to be sequential
        chapter_folder = os.path.join(output_directory, volume_title)

        # Create a folder for the chapter
        if not os.path.exists(chapter_folder):
            os.makedirs(chapter_folder)

        # Extract the .cbz file (which is a .zip file) to the chapter folder
        with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
            zip_ref.extractall(chapter_folder)

        # Rename the images within the extracted folder
        for filename in sorted(os.listdir(chapter_folder)):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                new_filename = f"{current_number:03d}.jpg"  # Use 001, 002, etc.
                current_number += 1
                total_page_count += 1  # Increment the total page count
                src = os.path.join(chapter_folder, filename)
                dst = os.path.join(output_directory, new_filename)  # Save the renamed file to the output directory
                shutil.move(src, dst)  # Move and rename the file
                click.echo(f"Renamed and moved '{src}' to '{dst}'")

    # Create the ComicInfo.xml file for the volume after processing all CBZ files
    create_comicinfo_xml(output_directory, f"Volume {volume_number}", series_name, total_page_count, volume_number, writer_name)

    click.echo("Extraction, renaming, and ComicInfo.xml creation completed.")

def create_comicinfo_xml(output_directory: str, volume_title: str, series_name: str, page_count: int, volume_number: int, writer_name: str) -> None:
    """Creates a ComicInfo.xml file in the output directory."""
    from xml.etree.ElementTree import Element, SubElement, tostring

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

    # Convert the ElementTree to a string and write to file
    comic_info_str = tostring(comic_info, encoding='utf-8', method='xml').decode('utf-8')

    with open(os.path.join(output_directory, "ComicInfo.xml"), 'w', encoding='utf-8') as f:
        f.write(comic_info_str)

    click.echo(f"ComicInfo.xml created in {output_directory}")

if __name__ == '__main__':
    cli()
