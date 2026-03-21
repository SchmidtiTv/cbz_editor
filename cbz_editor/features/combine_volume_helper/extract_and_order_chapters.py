import os
import zipfile
from typing import Tuple
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TextColumn, MofNCompleteColumn

from .rename_images_in_folder import rename_images_in_folder
from cbz_editor.utils import create_directory


def extract_and_order_chapters(
    cbz_directory: str,
    current_number: int,
    output_directory: str,
    total_page_count: int,
) -> Tuple[list[str], int]:
    cbz_files = sorted([f for f in os.listdir(cbz_directory) if f.lower().endswith('.cbz')])

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
    ) as progress:
        cbz_task = progress.add_task("Processing CBZ files", total=len(cbz_files))
        img_task = progress.add_task("Renaming images", total=0, visible=False)

        for cbz_file in cbz_files:
            chapter_folder = os.path.join(output_directory, os.path.splitext(cbz_file)[0])
            create_directory(chapter_folder)

            with zipfile.ZipFile(os.path.join(cbz_directory, cbz_file), 'r') as zip_ref:
                zip_ref.extractall(chapter_folder)

            current_number, total_page_count, _ = rename_images_in_folder(
                chapter_folder, output_directory, current_number, total_page_count,
                progress=progress, task_id=img_task,
            )

            progress.advance(cbz_task)

        progress.update(img_task, visible=False)

    return cbz_files, total_page_count