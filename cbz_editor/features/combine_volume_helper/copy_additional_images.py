import os
import shutil
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from cbz_editor.features.combine_volume import VolumeBuilder


def copy_additional_images(obj: "VolumeBuilder", cbz_directory: str, current_number: int, output_directory: str,
                           total_page_count: int) -> \
        Tuple[int, list[str], int]:
    p_images = sorted([f for f in os.listdir(cbz_directory)
                       if f.lower().startswith('p(') and f.lower().endswith('.jpg')])
    obj.logger.info(f"Found {len(p_images)} additional images in {cbz_directory}")
    for i, p_image in enumerate(p_images, start=current_number):
        p_image_path = os.path.join(cbz_directory, p_image)
        new_filename = f"{i:03d}.jpg"
        shutil.copyfile(p_image_path, os.path.join(output_directory, new_filename))
        obj.logger.info(f"Added additional image '{p_image}' as '{new_filename}'")
        total_page_count += 1
        current_number = i + 1
    return current_number, p_images, total_page_count