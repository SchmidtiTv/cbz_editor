# CBZ Editor

A CLI tool to batch-rename, organize, and tag CBZ volumes with `ComicInfo.xml` metadata.

## Quick Start

1. Install:

```bash
git clone https://github.com/SchmidtiTv/cbz_editor
cd cbz_editor
pip install -e .
```

2. Setup:

```bash
cbz-editor init
```

Creates folders and stores your Series/Writer info and the Schema for the Output Folders in `config.xml`.

3. Run:
   Put chapter `.cbz` files and optional images (e.g., `title.jpg`, `p(n).jpg`) into the `cbz` folder, then:

```bash
cbz-editor build_volume 1 --move-originals
```

- `--move-originals` moves the source `.cbz` and extra images into `temp/Volume_1` after processing.

---

## What it does

- Sequential Renaming: outputs `0001.jpg`, `0002.jpg`, ...
- Cover Support: uses `title.jpg` as `0001.jpg` when present.
- Extra Pages: copies any `p(n).jpg` into the sequence before chapters.
- Auto-Metadata: writes `ComicInfo.xml` (Title, Series, Volume, PageCount, optional Writer).
- Combined Archive: creates `Volume_X.cbz` containing only numbered images and `ComicInfo.xml`.
- Safe Archiving: avoids re-adding the output CBZ to itself and supports large volumes (ZIP64).

## Requirements

- Python 3.8+
- Runtime dependencies are installed via `setup.py`:
    - `click` (CLI)
    - `tqdm` (progress bars)

## Project Structure

- Working folders created/used:
    - `cbz/`   — drop your raw `.cbz` and optional images here
    - `temp/`  — originals archived after processing when `--move-originals` is used
    - `config.xml` — stores series metadata

## License

MIT License © 2025 Schmidti