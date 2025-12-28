import os
from xml.etree.ElementTree import Element, SubElement, tostring
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cbz_editor.features.combine_volume import VolumeBuilder


def create_comicinfo_xml(obj: "VolumeBuilder", output_directory: str, volume_title: str, series_name: str,
                         page_count: int,
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

    obj.logger.info(f"ComicInfo.xml created in {output_directory}")
