
## v1.0.0 (2026-01-04)
**Initial Release**

- **Feature**: **ZID Name Generation**. Automatically converts input strings into lowercased, hyphen-joined slugs using the first 6 words.
- **Feature**: **Umlaut Normalization**. Handles German special characters (ä, ö, ü, ß) by converting them to their ASCII equivalents.
- **Feature**: **Clipboard Integration**. Reads input from the clipboard if no argument is provided and writes the result back to the clipboard.
- **Feature**: **AutoHotkey v2 Integration**. Added support for seamless "Copy-Process-Paste" workflow via `zid-name.ahk`.
- **Feature**: **Python Execution**. Optimized for direct execution via Python interpreter for integration workflows.
