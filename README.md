# CBZ Editor

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

CBZ Editor is a powerful and user-friendly command-line tool designed for processing and managing CBZ (Comic Book Zip) files. It offers a seamless way to extract, rename, and organize images from CBZ files, while also generating the necessary `ComicInfo.xml` metadata for comic book readers. Whether you're working with single issues or entire volumes, CBZ Editor simplifies your workflow, making it easy to manage and structure your comic archives.

## Features

- **Process CBZ Files**: Automatically extract, rename, and organize images from CBZ archives.
- **Custom Metadata Creation**: Generate a `ComicInfo.xml` file containing detailed information about the volume, series, writer, and more.
- **Cover Image Handling**: Optionally replace or prepend `title.jpg` as the cover image.
- **Additional Image Support**: Includes handling for extra images such as `p(n).jpg` before or after CBZ file extraction.
- **Interactive and Command-Line Modes**: Run interactively or provide all commands through a simple CLI.
- **Directory Management**: Automatically creates and manages necessary directories (`cbz`, `temp`).
- **Combine Processed Images into CBZ**: Combine extracted images into a new CBZ archive after processing.
- **Optional File Cleanup**: Move original files to a temporary directory after processing, keeping your workspace clean.

## Installation

You can install CBZ Editor by cloning the repository and installing it using `pip`:

```bash
git clone https://github.com/SchmidtiTv/cbz_editor
cd cbz_editor
pip install -e .
```

### Requirements

- Python 3.6 or higher
- Required Python packages (automatically installed with `pip`):
  - `click`
  - `tqdm`

## Usage

CBZ Editor provides a simple command-line interface (CLI) for initializing and processing CBZ files. The primary commands are `init` and `process`.

### 1. Initialize the CBZ Editor

Before processing any CBZ files, you need to initialize the project using the `init` command:

```bash
cbz_editor init
```

- **What it does**:
  - Creates the necessary `cbz` and `temp` directories (if they don’t exist).
  - Prompts you for the series name and writer name (optional).
  - Saves this information in an XML file (`config.xml`) for future use.

### 2. Process CBZ Files

After initialization, you can process CBZ files with the `process` command. This extracts the images from the CBZ files, renames them sequentially, and creates a new CBZ file along with a `ComicInfo.xml`.

```bash
cbz_editor process <volume_number> [--move-originals]
```

- **Example**:
  ```bash
  cbz_editor process 2
  ```

- **Optional Flag**:
  - `--move-originals`: Move the original CBZ files and images to a temporary directory after processing.
  
- **What it does**:
  - Reads and processes all CBZ files in the `cbz` directory.
  - Extracts images, handles additional images like `title.jpg` or `p(n).jpg`, and renames them.
  - Generates `ComicInfo.xml` with metadata such as the series name, volume number, page count, and writer.
  - Optionally combines the processed images into a new CBZ file.
  - Optionally moves the original files to a temp folder.

## Example Workflow

1. **Step 1**: Initialize the project:
   ```bash
   cbz_editor init
   ```
   This creates the necessary directories and prompts for the series and writer name.

2. **Step 2**: Add your CBZ files to the `cbz` directory.

3. **Step 3**: Optionally, add a `title.jpg` and any extra images (`p(n).jpg`) to the `cbz` directory.

4. **Step 4**: Process the CBZ files for a specific volume:
   ```bash
   cbz_editor process 1 --move-originals
   ```
   This extracts and renames the images, generates the `ComicInfo.xml`, creates a new combined CBZ, and moves the original files to the `temp` directory.

5. **Step 5**: Find the renamed images and the `ComicInfo.xml` file in the output directory.

## License

CBZ Editor is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

## Contributing

Contributions are welcome! Feel free to open issues for bugs, suggest new features, or submit pull requests. Your feedback helps make CBZ Editor better for everyone.