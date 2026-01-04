
## v1.1.0 (2026-01-04)
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
