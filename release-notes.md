
## v1.3.3 (2026-01-05)
**Robust Extension Handling**

- **Fix**: **Iterative Extension Detection**. Fixed a bug where configuring a high extension depth (e.g., 3) would cause detection to fail entirely if an invalid separator was encountered. The script now intelligently falls back to the longest valid extension suffix (e.g., correctly finding `.ext1.ext2` even if `.invalid.ext1.ext2` was checked).
- **Testing**: **Regression Prevention**. Added specific test cases to ensure complex filenames with "spaces and dots" are handled correctly without breaking valid extensions.

## v1.3.2 (2026-01-05)
**Stabilization & Consistency**

- **Refactor**: **Clean Codebase**. Removed accidental code duplication in the main utility script (`zid_name.py`).
- **Improvement**: **Modern Configuration**. Finalized the transition to integer-based extension handling (`preserve_extension_depth`) in both configuration files and the test suite, retiring legacy boolean flags.
- **Documentation**: **Enhanced Config Templates**. `config.ini.template` now includes clear comments explaining the priority and usage of extension handling features.
- **Testing**: **Testing Reliability**. Updated all tests to correctly verify the new configuration logic, ensuring robust regression testing.

## v1.2.8 (2026-01-05)
**Slug Extension Control & Test Refactoring**

- **Feature**: **Slug Extension Appending**. Added `add_extension_to_slug` option to `config.ini`. When enabled, file extensions are preserved and attached to the end of the slug (hyphenated) even if the filename is truncated by the word count limit (e.g., `...long-title-pdf`).
- **Improvement**: **Test Suite Organization**. completely refactored the monolithic `test_zid_name.py` into modular files (`test_basics.py`, `test_zid_logic.py`, `test_extensions.py`) for better maintainability and discovery.
- **Config**: Added `add_extension_to_slug` (default `false` or `true` depending on user preference, default in template is `false`).

## v1.2.4 (2026-01-05)
**Extension Handling & Robustness**

- **Feature**: **Extension Preservation**. Added `extension_nesting_level` setting to control how many file extensions are preserved (e.g., `.tar.gz` vs `.pdf`). Supports "up-to" logic, gracefully handling files with fewer extensions than configured.
- **Improvement**: **Smart Extension Detection**. The script now intelligently distinguishes between file extensions and text punctuation. Dot-separated parts containing spaces (e.g., `End of sentence. Start of new`) are treated as text to be slugified, not as extensions.
- **Improvement**: **Double Separator Cleanup**. Automatically collapses multiple separators (e.g., `--`) into one, ensuring clean slugs even when replacements generate extra hyphens.
- **Fix**: **Configuration Stability**. Resolved a crash caused by duplicate keys in `config.ini` when trying to map `. ` to dashes.
- **Config**: Added `extension_nesting_level` (default `0`) to `[Settings]`.

## v1.2.0 (2026-01-05)
**Batch Processing & Smart Sanitization**

- **Feature**: **Batch Mode Support**. Multi-line selections can now be processed in one go. The script intelligently detects if the input contains ZID task lines.
- **Feature**: **Markdown Heading Support**. Headings (`#` to `######`) are now supported as prefixes, similar to list markers.
- **Feature**: **Smart Sanitization**. 
    - **Single-line** inputs are always sanitized to support manual substring or title-to-filename workflows.
    - **Multi-line** blocks respect the new `process_non_zid_lines` config flag to preserve technical structure while allowing ZID generation for headings.
- **Improvement**: **Sentence Boundary Handling**. The script now converts `. ` (dot space) into a separator, ensuring multi-sentence inputs produce clean slugs without formatting artifacts.
- **Improvement**: **List Marker Preservation**. Standardized regex now recognizes and preserves indentation, bullets, checkboxes (`- [ ]`, `- [x]`), and numbering.
- **Improvement**: **Sanitization Refinement**. Added automatic stripping of trailing separators (e.g., `-`) from the generated slugs.
- **Config**: Added `process_non_zid_lines` (default `false`) to control whether lines without ZIDs should be slugified in batch mode.
- **Testing**: Unified and expanded test suite with coverage for mixed content, complex prefixes, and configuration permutations.


**Enhanced Configurability & Obsidian Integration**

- **Feature**: **External Configuration (`config.ini`)**. Key settings like `slug_word_count`, `separator`, and `replacements` are now externalized.
- **Feature**: **ZID-Aware Logic**. The script now correctly identifies 14-digit timestamps at the start of lines and excludes them from the word limit count, matching Obsidian template behavior.
- **Feature**: **Character Replacement Table**. Users can now define custom replacements in `config.ini`, supporting multi-language workflows (e.g., German umlauts).
- **Feature**: **Case-Sensitive Replacements**. Improved character handling ensures `Ä` and `ä` can be mapped to different or same strings accurately before final lowercasing.
- **Improvement**: **Internal Documentation**. All code comments and docstrings have been translated to English.
- **Improvement**: **Naming Alignment**. Internal variables and functions now match the naming conventions of the Kardenwort Obsidian templates.

## v1.0.0 (2026-01-04)
**Initial Release**

- **Feature**: **ZID Name Generation**. Automatically converts input strings into lowercased, hyphen-joined slugs using the first 6 words.
- **Feature**: **Umlaut Normalization**. Handles German special characters (ä, ö, ü, ß) by converting them to their ASCII equivalents.
- **Feature**: **Clipboard Integration**. Reads input from the clipboard if no argument is provided and writes the result back to the clipboard.
- **Feature**: **AutoHotkey v2 Integration**. Added support for seamless "Copy-Process-Paste" workflow via `zid-name.ahk`.
- **Feature**: **Python Execution**. Optimized for direct execution via Python interpreter for integration workflows.
