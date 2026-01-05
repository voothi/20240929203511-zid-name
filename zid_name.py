import argparse
import pyperclip
import re
import configparser
import os

def get_config():
    """Reads all settings from config.ini."""
    config = configparser.ConfigParser(delimiters=('=',))
    config.optionxform = str  # Preserve case for keys
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    defaults = {
        'slug_word_count': 4,
        'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
        'lowercase': True,
        'separator': '-',
        'replacements': {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
            'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '.': '-'
        }
    }

    if not os.path.exists(config_path):
        return defaults

    try:
        config.read(config_path)
        
        settings = {
            'slug_word_count': config.getint('Settings', 'slug_word_count', fallback=defaults['slug_word_count']),
            'allowed_chars_regex': config.get('Settings', 'allowed_chars_regex', fallback=defaults['allowed_chars_regex']),
            'lowercase': config.getboolean('Format', 'lowercase', fallback=defaults['lowercase']),
            'separator': config.get('Format', 'separator', fallback=defaults['separator']),
            'replacements': {}
        }

        if 'Replacements' in config:
            for key, value in config['Replacements'].items():
                settings['replacements'][key] = value
        else:
            settings['replacements'] = defaults['replacements']
            
        return settings
    except (configparser.Error, ValueError):
        return defaults

def get_clipboard_text():
    return pyperclip.paste()

def set_clipboard_text(text):
    pyperclip.copy(text)

def sanitizeName(inputString, cfg):
    """
    Sanitizes a string: keeps only the first N words (from config),
    joins them with separator, and converts to lowercase.
    This function corresponds to sanitizeName in Obsidian templates.
    """
    # 1. Character replacements
    processedString = inputString
    for char, replacement in cfg['replacements'].items():
        processedString = processedString.replace(char, replacement)

    # 2. Regex filtering
    cleanedForSplitting = re.sub(cfg['allowed_chars_regex'], '', processedString)

    # 3. Splitting and limiting
    words = cleanedForSplitting.split()
    firstWords = words[:cfg['slug_word_count']]

    # 4. Joining with separator
    finalName = cfg['separator'].join(firstWords)

    # 5. Remove trailing separators (new requirement)
    finalName = finalName.rstrip(cfg['separator'])

    # 6. Case conversion (must be last)
    if cfg['lowercase']:
        finalName = finalName.lower()

    return finalName

def process_line(line, cfg):
    """
    Processes a single line: Detects ZID and handles word limit accordingly.
    """
    # Regex to detect ZID at the start (matching Obsidian template zidLineRegex)
    # Group 1: Prefix (indentation, bullets, checkboxes)
    # Group 2: ZID (14 digits)
    # Group 3: Remaining text
    zidLineRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+)?)(\d{14})\s+(.*)$'
    zid_match = re.match(zidLineRegex, line)
    
    if zid_match:
        prefix = zid_match.group(1) or ""
        zid = zid_match.group(2)
        raw_text = zid_match.group(3)
        safe_name = sanitizeName(raw_text, cfg)
        return f"{prefix}{zid}{cfg['separator']}{safe_name}"
    else:
        # If no ZID found, check if it's just a text line we might want to sanitize?
        # The requirement says: "If it doesn't match, return the line exactly as it was"
        # BUT the original code (lines 98-99) called sanitizeName on the whole string if no ZID was found.
        # This behavior for SINGLE line input might be desired, but for BATCH mode (multi-line),
        # preserving non-matching lines is safer for mixed content.
        # However, for backward compatibility with single-line usage where someone just pastes "My Title",
        # we might want to keep that.
        # Let's check if the whole input was multi-line or not in process_string.
        # For this helper, let's assume if it's not a ZID line, we return it as is if it's part of a batch?
        # Or does the user want "My Title" -> "my-title"?
        # User request: "If it doesn't match, return the line exactly as it was (preserving comments or empty lines)."
        return line

def process_string(input_string):
    """
    Main processing logic: Handles batch processing for multi-line strings.
    """
    cfg = get_config()
    lines = input_string.splitlines()
    
    # Heuristic: Check if ANY line matches the ZID pattern to trigger strict "Batch Mode".
    # If NO lines match ZID regex, we might fall back to "Single Title Mode" to preserve
    # the behavior of pasting "My Cool Title" -> "my-cool-title".
    
    zidLineRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+)?)(\d{14})\s+(.*)$'
    has_zid = any(re.match(zidLineRegex, line) for line in lines)
    
    processed_lines = []
    
    if has_zid:
        for line in lines:
            processed_lines.append(process_line(line, cfg))
    else:
        # No ZIDs found in the entire block.
        # If it's a single line, we definitely want to sanitize it (legacy behavior).
        # If it's multiple lines, do we sanitize each line? Or treated as one block?
        # The prompt says: "If you select 5 task lines, it tries to create one giant slug."
        # indicating the previous behavior was bad for multiple lines.
        # Let's treat it line-by-line using sanitizeName if it's not empty.
        # But wait, User said: "If it doesn't match, return the line exactly as it was".
        # That applies to "Batch Mode" where "Mode Detection: Check if ANY of those lines match...".
        # So if NO lines match, do we assume it's NOT batch mode?
        # If I paste "My Title", I expect "my-title".
        # If I paste "Line 1\nLine 2", I probably expect "line-1\nline-2" or unchanged?
        # Let's stick to the explicit instruction: "Mode Detection: Check if *any* of those lines match the ZID format. If yes, enter batch mode."
        
        if len(lines) == 1:
             # Basic single line sanitization (legacy)
             return sanitizeName(lines[0], cfg)
        else:
            # Multi-line, NO ZIDs.
            # Behavior undefined in prompt, but "treats the entire clipboard as one single block" was the complaint.
            # Safe bet: Sanitize each line individually? Or literal return?
            # Let's sanitize each line individually as a useful default for "list of titles".
            for line in lines:
                if line.strip():
                     processed_lines.append(sanitizeName(line, cfg))
                else:
                     processed_lines.append(line)
                     
    return "\n".join(processed_lines)

def main():
    parser = argparse.ArgumentParser(description="Process string for a filename based on config.ini settings (ZID aware).")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    input_text = args.input_string if args.input_string is not None else get_clipboard_text()
    
    output_string = process_string(input_text)
    
    set_clipboard_text(output_string)

    print(output_string)

if __name__ == "__main__":
    main()