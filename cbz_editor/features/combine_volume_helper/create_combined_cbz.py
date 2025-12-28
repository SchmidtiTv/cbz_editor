import os
import zipfile
from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from cbz_editor.features.combine_volume import VolumeBuilder


def create_combined_cbz(obj: "VolumeBuilder", output_directory: str, cbz_filename: str) -> None:
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
                arc_name = os.path.relpath(file_path, start=output_directory)
                cbz_file.write(file_path, arc_name)

    obj.logger.info(f"Combined CBZ file created: {cbz_path}")
    click.echo(f"Finished combining CBZs: {cbz_path}")
