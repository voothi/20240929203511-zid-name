# ZID Name Utility

[![Version](https://img.shields.io/badge/version-v1.1.0-blue)](https://github.com/voothi/20240929203511-zid-name)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight utility for generating clean, lowercased, and hyphen-separated slugs from text. Specifically designed for creating Zettelkasten ID (ZID) note titles and filenames.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
    - [From Source](#from-source)
    - [Standalone Executable](#standalone-executable)
- [Configuration](#configuration)
- [Usage](#usage)
- [AutoHotkey Integration](#autohotkey-integration)
- [Development](#development)
- [Kardenwort](#kardenwort)
- [License](#license)

---

## Description
`zid-name` is a focused tool that processes an input string or the current clipboard content. It extracts the first 6 words, replaces special characters (including German umlauts), and joins them with hyphens in lowercase. This ensures consistent and cross-platform friendly filenames and note titles.

[Return to Top](#zid-name-utility)

## Features
- **Smart Slug Generation**: Converts titles into clean filenames (e.g., `My Note Title` → `my-note-title`).
- **ZID-Awareness**: Automatically detects 14-digit timestamps (ZIDs) at the start of the input and excludes them from the word count.
- **External Configuration**: Customize the word limit, character replacements, and formatting via `config.ini`.
- **Word Limiting**: Automatically trims the result (excluding ZID) to the configured word count (default: 6).
- **Umlaut Handling**: Replaces `ä`, `ö`, `ü`, and `ß` with `ae`, `oe`, `ue`, and `ss`.
- **Character Normalization**: Replaces dots, underscores, and special punctuation with hyphens.
- **Clipboard Integration**: Seamlessly reads from and writes back to the system clipboard.
- **Fast Execution**: Designed to be run as a quick background utility.

[Return to Top](#zid-name-utility)

## Installation

### From Source
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install pyperclip
   ```
3. Run the script:
   ```bash
   python zid_name.py
   ```

### Standalone Executable
You can find pre-built executables in the `dist/` folder or under the Releases section.

[Return to Top](#zid-name-utility)

## Configuration
You can customize the script's behavior by modifying the `config.ini` file in the application directory.

```ini
[Settings]
slug_word_count = 6
allowed_chars_regex = [^a-zA-Zа-яА-ЯёЁ0-9\s-]

[Format]
lowercase = true
separator = -

[Replacements]
ä = ae
ö = oe
ü = ue
ß = ss
```

### Settings
- **slug_word_count**: The maximum number of words to include in the generated slug (default: 6). This count excludes the 14-digit ZID if present at the start of the input.
- **allowed_chars_regex**: A regular expression defining which characters are kept before splitting into words.

### Format
- **lowercase**: If `true`, the final output will be converted to lowercase.
- **separator**: The character used to join words (e.g., `-` or `_`).

### Replacements
A list of specific character-to-string mappings. This is useful for handling umlauts or specific punctuation.

[Return to Top](#zid-name-utility)

## Usage

1. **Copy** the title or text you want to convert.
2. **Execute** the script using Python:
   ```powershell
   python u:\voothi\20240929203511-zid-name\zid_name.py
   ```
   *Note: You can also provide the string as a direct argument:*
   ```powershell
   python zid_name.py "My New Note Title"
   ```
3. **Paste** the generated ZID name into your destination.

The terminal will display the processed string for quick verification.

[Return to Top](#zid-name-utility)

## AutoHotkey Integration

For a more seamless workflow, you can use the **[zid-name.ahk](https://github.com/voothi/20240411110510-autohotkey/blob/main/zid-name.ahk)** script. 

This script maps the process to `Ctrl + Alt + ;`, performing the following steps automatically:
1. **Copies** the currently selected text.
2. **Processes** it through the Python script.
3. **Pastes** the cleaned ZID name back into your active window.

> [!IMPORTANT]
> You must update the paths in the `RunWait` command within the `.ahk` script to match your local installation of Python and the location of `zid_name.py`.

## Development

### Verification Tests
A Python test suite is available in the `tests/` directory to verify the logic for umlaut handling, ZID-awareness, and word counting.

To run the tests:
```bash
python tests/test_zid_name.py
```
*Note: The tests rely on the current settings in `config.ini`. Ensure `slug_word_count` is set to 3 for the default test cases to pass.*

[Return to Top](#zid-name-utility)

## Kardenwort Ecosystem

This project is part of the **[Kardenwort](https://github.com/kardenwort)** environment, designed to create a focused and efficient learning ecosystem.

[Return to Top](#table-of-contents)

## License
MIT License. See LICENSE file for details.

[Return to Top](#zid-name-utility)
