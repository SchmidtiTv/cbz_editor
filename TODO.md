# High-Priority Improvements
- [ ] Add comprehensive error handling — Handle missing/corrupted CBZ files, unreadable images, and disk space issues with graceful fallbacks.
- [ ] Implement unit and integration tests — Add pytest tests for core functions (extract_cbz_and_rename_images, create_comicinfo_xml, etc.).
- [ ] Add input validation — Validate volume numbers, series names, and file paths before processing.
- [ ] Add logging configuration to CLI — Currently only logs to file; add optional --verbose/--quiet flags for user feedback.
- [ ] Handle edge cases in image renaming — Support PNG/WebP, nested folder structures, and duplicate filenames gracefully.
- [ ] Improve Config Management — Add commands to view/edit config.xml from CLI (e.g., cbz-editor config set series "New Series").
- [x] Make '--output-dir' default configurable — Allow setting a default output directory in config.xml to avoid specifying each time.

## Medium-Priority Features
- [ ] Support batch processing multiple volumes — Process volumes 1–N in a single command with --volumes 1-5.
- [ ] Add image validation — Verify images are valid before adding to CBZ (corrupt file detection).
- [ ] Expand ComicInfo.xml metadata — Add optional fields: issue numbers, publication date, description, genre.
- [ ] Add progress hooks — Display real-time status in UI (already have tqdm; enhance with completion percentage).
- [ ] Improve file cleanup — Offer safe deletion of temporary/chapter folders after successful CBZ creation.

## Code Quality & Maintenance
- [ ] Refactor extract_cbz_and_rename_images — Function is long (50+ lines); split into smaller helpers.
- [ ] Add type hints to all functions — Currently partial; complete coverage for better IDE support.
- [ ] Remove platform-specific assumptions — Ensure cross-platform path handling (currently Windows).
