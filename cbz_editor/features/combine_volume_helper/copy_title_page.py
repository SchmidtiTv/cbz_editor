import os
import shutil
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from cbz_editor.features.combine_volume import VolumeBuilder


def copy_title_page(obj: "VolumeBuilder", cbz_directory: str, current_number: int, output_directory: str,
                    total_page_count: int) -> Tuple[int, str, int]:
    title_jpg_path = os.path.join(cbz_directory, "title.jpg")
    if os.path.exists(title_jpg_path):
        cover_path = os.path.join(output_directory, "001.jpg")
        shutil.copyfile(title_jpg_path, cover_path)
        obj.logger.info("Cover image 'title.jpg' found and copied as '001.jpg'")
        total_page_count += 1
        current_number = 2
    return current_number, title_jpg_path, total_page_count