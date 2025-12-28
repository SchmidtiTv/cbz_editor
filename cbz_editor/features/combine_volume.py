import os

from cbz_editor.logger.logger import Logger
from cbz_editor.utils import create_directory
from .combine_volume_helper.copy_additional_images import copy_additional_images
from .combine_volume_helper.copy_title_page import copy_title_page
from .combine_volume_helper.create_combined_cbz import create_combined_cbz
from .combine_volume_helper.create_comicinfo_xml import create_comicinfo_xml
from .combine_volume_helper.extract_and_order_chapters import extract_and_order_chapters
from .combine_volume_helper.move_to_temp_folder import move_to_temp_folder


class VolumeBuilder:
    """Class to build a volume from CBZ files."""

    def __init__(self, cbz_directory: str, output_directory: str, volume_number: int,
                 series_name: str, writer_name: str, move_originals: bool, logger: Logger) -> None:
        self.cbz_directory = cbz_directory
        self.output_directory = output_directory
        self.volume_number = volume_number
        self.series_name = series_name
        self.writer_name = writer_name
        self.move_originals = move_originals
        self.logger = logger

    def build(self) -> None:
        """Run the build process."""
        output_directory_folder = self.output_directory.replace("%d", str(self.volume_number))
        output_directory = os.path.join(os.curdir, output_directory_folder)

        current_number = 1
        total_page_count = 0

        create_directory(output_directory)

        # Handle title.jpg
        current_number, title_jpg_path, total_page_count = copy_title_page(self, self.cbz_directory, current_number,
                                                                           output_directory,
                                                                           total_page_count)

        # Handle additional p(n).jpg images and if exist add them in front of the volume after title.jpg
        current_number, p_images, total_page_count = copy_additional_images(self, self.cbz_directory, current_number,
                                                                            output_directory,
                                                                            total_page_count)

        cbz_files, total_page_count = extract_and_order_chapters(self.cbz_directory, current_number, output_directory,
                                                                 total_page_count)

        create_comicinfo_xml(self, output_directory, f"Volume {self.volume_number}", self.series_name, total_page_count,
                             self.volume_number, self.writer_name)
        create_combined_cbz(self, output_directory, f"Volume_{self.volume_number}.cbz")

        if self.move_originals:
            move_to_temp_folder(self, cbz_files, title_jpg_path, p_images, self.cbz_directory, self.volume_number)
