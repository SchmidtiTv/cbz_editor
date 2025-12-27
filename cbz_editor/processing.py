import os
import shutil
import logging
import zipfile
from typing import List, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring

from tqdm import tqdm

from .utils import create_directory, CBZ_DIR, TEMP_DIR

logger = logging.getLogger(__name__)


def extract_cbz_and_rename_images(cbz_directory: str, output_directory: str, volume_number: int,
                                  series_name: str, writer_name: str, move_originals: bool) -> None:
    current_number = 1
    total_page_count = 0
    create_directory(output_directory)

    # Handle title.jpg
    title_jpg_path = os.path.join(cbz_directory, "title.jpg")
    if os.path.exists(title_jpg_path):
        cover_path = os.path.join(output_directory, "001.jpg")
        shutil.copyfile(title_jpg_path, cover_path)
        logger.info("Cover image 'title.jpg' found and copied as '001.jpg'")
        total_page_count += 1
        current_number = 2

    # Handle additional p(n).jpg images
    p_images = sorted([f for f in os.listdir(cbz_directory)
                       if f.lower().startswith('p(') and f.lower().endswith('.jpg')])
    for i, p_image in enumerate(p_images, start=current_number):
        p_image_path = os.path.join(cbz_directory, p_image)
        new_filename = f"{i:03d}.jpg"
        shutil.copyfile(p_image_path, os.path.join(output_directory, new_filename))
        logger.info(f"Added additional image '{p_image}' as '{new_filename}'")
        total_page_count += 1
        current_number = i + 1

    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])
    for cbz_file in tqdm(cbz_files, desc="Processing CBZ files"):
        chapter_folder = os.path.join(output_directory, os.path.splitext(cbz_file)[0])
        create_directory(chapter_folder)

        with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
            zip_ref.extractall(chapter_folder)

        current_number, total_page_count = rename_images_in_folder(
            chapter_folder, output_directory, current_number, total_page_count)

    create_comicinfo_xml(output_directory, f"Volume {volume_number}", series_name, total_page_count,
                         volume_number, writer_name)
    create_combined_cbz(output_directory, f"Volume_{volume_number}.cbz")

    if move_originals:
        move_to_temp_folder(cbz_files, title_jpg_path, p_images, cbz_directory, volume_number)


def rename_images_in_folder(chapter_folder: str, output_directory: str, current_number: int,
                            total_page_count: int) -> Tuple[int, int]:
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


def create_comicinfo_xml(output_directory: str, volume_title: str, series_name: str, page_count: int,
                          volume_number: int, writer_name: str) -> None:
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
    logger.info(f"ComicInfo.xml created in {output_directory}")


def create_combined_cbz(output_directory: str, cbz_filename: str) -> None:
    """Creates a combined CBZ file."""
    cbz_path = os.path.join(output_directory, cbz_filename)
    with zipfile.ZipFile(cbz_path, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as cbz_file:
        for root, _, files in os.walk(output_directory):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                if os.path.abspath(file_path) == os.path.abspath(cbz_path):
                    continue
                if not (file.lower().endswith(('.jpg', '.jpeg')) or file == 'ComicInfo.xml'):
                    continue
                arcname = os.path.relpath(file_path, start=output_directory)
                cbz_file.write(file_path, arcname)
    logger.info(f"Combined CBZ file created: {cbz_path}")
    print(f"Finished combining CBZs: {cbz_path}")


def move_to_temp_folder(cbz_files: List[str], title_jpg_path: str, p_images: List[str],
                        cbz_directory: str, volume_number: int) -> None:
    """Moves original CBZ files and images to a temporary folder."""
    temp_dir = os.path.join(TEMP_DIR, f"Volume_{volume_number}")
    create_directory(temp_dir)

    for cbz_file in cbz_files:
        src = os.path.join(cbz_directory, cbz_file)
        dst = os.path.join(temp_dir, cbz_file)
        shutil.move(src, dst)
        logger.info(f"Moved '{cbz_file}' to '{temp_dir}'")

    if os.path.exists(title_jpg_path):
        shutil.move(title_jpg_path, os.path.join(temp_dir, "title.jpg"))
        logger.info(f"Moved 'title.jpg' to '{temp_dir}'")

    for p_image in p_images:
        shutil.move(os.path.join(cbz_directory, p_image), os.path.join(temp_dir, p_image))
        logger.info(f"Moved '{p_image}' to '{temp_dir}'")
