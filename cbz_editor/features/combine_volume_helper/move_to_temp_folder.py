import os
import shutil
from typing import List, TYPE_CHECKING

from cbz_editor.utils import create_directory, TEMP_DIR

if TYPE_CHECKING:
    from cbz_editor.features.combine_volume import VolumeBuilder


def move_to_temp_folder(obj: "VolumeBuilder", cbz_files: List[str], title_jpg_path: str, p_images: List[str],
                        cbz_directory: str, volume_number: int) -> None:
    """Moves original CBZ files and images to a temporary folder."""
    temp_dir = os.path.join(TEMP_DIR, f"Volume_{volume_number}")
    create_directory(temp_dir)

    for cbz_file in cbz_files:
        src = os.path.join(cbz_directory, cbz_file)
        dst = os.path.join(temp_dir, cbz_file)
        shutil.move(src, dst)
        obj.logger.info(f"Moved '{cbz_file}' to '{temp_dir}'")

    if os.path.exists(title_jpg_path):
        shutil.move(title_jpg_path, os.path.join(temp_dir, "title.jpg"))
        obj.logger.info(f"Moved 'title.jpg' to '{temp_dir}'")

    for p_image in p_images:
        shutil.move(os.path.join(cbz_directory, p_image), os.path.join(temp_dir, p_image))
        obj.logger.info(f"Moved '{p_image}' to '{temp_dir}'")