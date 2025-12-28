import os
import zipfile
from typing import Tuple

from tqdm import tqdm

from .rename_images_in_folder import rename_images_in_folder
from cbz_editor.utils import create_directory


def extract_and_order_chapters(cbz_directory: str, current_number: int, output_directory: str,
                               total_page_count: int) -> Tuple[list[str], int]:
    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])
    for cbz_file in tqdm(cbz_files, desc="Processing CBZ files"):
        chapter_folder = os.path.join(output_directory, os.path.splitext(cbz_file)[0])
        create_directory(chapter_folder)

        with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
            zip_ref.extractall(chapter_folder)

        current_number, total_page_count = rename_images_in_folder(chapter_folder, output_directory,
                                                                       current_number,
                                                                       total_page_count)
    return cbz_files, total_page_count