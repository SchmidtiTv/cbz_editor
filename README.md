# CBZ Editor

A CLI tool to batch-rename, organize, and tag CBZ volumes with `ComicInfo.xml` metadata.

## Quick Start

1. **Install:**
```bash
git clone https://github.com/SchmidtiTv/cbz_editor
cd cbz_editor
pip install -e .
```


2. **Setup:**
```bash
cbz-editor init
```


*Creates folders and stores your Series/Writer info.*
3. **Run:**
Put your files in `/cbz` and run:
```bash
cbz-editor process 1 --move-originals
```



---

## Features

* **Sequential Renaming:** Fixes messy filenames (e.g., `001.jpg`, `002.jpg`).
* **Auto-Metadata:** Generates `ComicInfo.xml` for readers like Kavita or Komga.
* **Cover Support:** Automatically picks up `title.jpg` as the cover.
* **Clean Workspace:** Uses a `--move-originals` flag to archive source files to `/temp`.

## Project Structure

* `/cbz`: Drop your raw `.cbz` and images here.
* `/temp`: Where originals go after processing.
* `config.xml`: Stores your series metadata.

## License

MIT License © 2024 SchmidtiTv