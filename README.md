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
git clone https://github.com/SchmidtiTv/cbz_editor/cbz_editor
cd cbz_editor
pip install -e .
```

### Requirements

- Python 3.6 or higher
- The following Python packages (automatically installed with `pip`):
  - `click`

## Usage

Once installed, you can use the `cbz_editor` command. The tool provides two main commands: `init` and `process`.

### 1. Initialize the CBZ Editor

Before processing CBZ files, you need to run the `init` command to set up the project:

```bash
cbz_editor init
```

- **What it does**:
  - Creates the necessary `cbz` and `temp` directories if they don't exist.
  - Prompts for the series name and writer name (optional).
  - Stores this information in an XML file for later use.

### 2. Process CBZ Files

After initializing, you can process a CBZ volume using the `process` command. This command uses the CBZ files stored in the `cbz` directory and renames them sequentially.

```bash
cbz_editor process <volume_number>
```

- **Example**:
  ```bash
  cbz_editor process 2
  ```

- **What it does**:
  - Reads the CBZ files from the `cbz` directory.
  - Extracts and renames the images.
  - Creates a `ComicInfo.xml` file with metadata for the processed volume.

## Example Workflow

1. **Step 1**: Initialize the project:
   ```bash
   cbz_editor init
   ```
   This will create the `cbz` and `temp` directories and ask for the series name and writer name.

2. **Step 2**: Place your CBZ files inside the `cbz` directory.

3. **Step 3**: Process the CBZ files for a specific volume:
   ```bash
   cbz_editor process 1
   ```

4. **Step 4**: The tool will extract and rename the images, and the renamed images will be available in the current working directory, along with the `ComicInfo.xml` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for new features.