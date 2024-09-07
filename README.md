# CBZ Editor

CBZ Editor is a command-line tool to process and manage CBZ (Comic Book Zip) files. It allows you to extract, rename, and organize images from CBZ files, while also generating `ComicInfo.xml` metadata. The tool simplifies working with comic book archives, making it easy to structure volumes and chapters.

## Features

- **Process CBZ Files**: Extract and rename images from CBZ archives.
- **Interactive Mode**: The tool guides you through setting up the necessary configurations.
- **Automatic Metadata Creation**: Generates a `ComicInfo.xml` file with volume and series information.
- **Directory Management**: Automatically creates necessary directories like `cbz` and `temp`.
- **Command-Line Interface**: Easy-to-use CLI powered by `click`.

## Installation

You can install the CBZ Editor by cloning this repository and using `pip`:

```bash
git clone https://github.com/yourusername/cbz_editor
cd cbz_editor
pip install -e .
