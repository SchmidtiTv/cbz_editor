import os
import shutil
from typing import Tuple, Optional
from rich.progress import Progress, TaskID, SpinnerColumn, BarColumn, TaskProgressColumn, TextColumn, MofNCompleteColumn


def rename_images_in_folder(
    chapter_folder: str,
    output_directory: str,
    current_number: int,
    total_page_count: int,
    progress: Optional[Progress] = None,
    task_id: Optional[TaskID] = None,
) -> Tuple[int, int, int]:
    """Rename images in the given folder."""
    image_files = [f for f in sorted(os.listdir(chapter_folder)) if f.lower().endswith(('.jpg', '.jpeg'))]
    zeros_needed = 4

    standalone = progress is None
    if standalone:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            transient=True,
        )
        progress.start()
        task_id = progress.add_task("Renaming images", total=len(image_files))
    else:
        progress.update(
            task_id,
            total=len(image_files),
            completed=0,
            description=f"Renaming [dim]{os.path.basename(chapter_folder)}[/dim]",
            visible=True,
        )

    for filename in image_files:
        new_filename = f"{current_number:0{zeros_needed}d}.jpg"
        shutil.move(os.path.join(chapter_folder, filename),
                    os.path.join(output_directory, new_filename))
        current_number += 1
        total_page_count += 1
        progress.advance(task_id)

    if standalone:
        progress.stop()

    return current_number, total_page_count, zeros_needed