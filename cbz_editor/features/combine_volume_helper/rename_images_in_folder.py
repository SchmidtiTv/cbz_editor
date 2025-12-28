import os
import shutil
from typing import Tuple

from tqdm import tqdm


def rename_images_in_folder(chapter_folder: str, output_directory: str, current_number: int,
                            total_page_count: int) -> Tuple[int, int, int]:
    """Rename images in the given folder."""
    image_files = [f for f in sorted(os.listdir(chapter_folder)) if f.lower().endswith(('.jpg', '.jpeg'))]
    zeros_needed = 4

    for filename in tqdm(image_files, desc="Renaming images"):
        new_filename = f"{current_number:0{zeros_needed}d}.jpg"
        src = os.path.join(chapter_folder, filename)
        dst = os.path.join(output_directory, new_filename)
        shutil.move(src, dst)
        current_number += 1
        total_page_count += 1

    return current_number, total_page_count, zeros_needed
