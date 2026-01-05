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
        'process_non_zid_lines': False,
        'preserve_extension_depth': 0,
        'slugify_extension_depth': 0,
        'allowed_chars_regex': r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]',
        'lowercase': True,
        'separator': '-',
        'replacements': {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
            'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '. ': '-', '.': '-'
        }
    }

    if not os.path.exists(config_path):
        return defaults

    try:
        config.read(config_path)
        
        settings = {
            'slug_word_count': config.getint('Settings', 'slug_word_count', fallback=defaults['slug_word_count']),
            'process_non_zid_lines': config.getboolean('Settings', 'process_non_zid_lines', fallback=defaults['process_non_zid_lines']),
            'preserve_extension_depth': config.getint('Settings', 'preserve_extension_depth', fallback=defaults['preserve_extension_depth']),
            'slugify_extension_depth': config.getint('Settings', 'slugify_extension_depth', fallback=defaults['slugify_extension_depth']),
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
    except (configparser.Error, ValueError) as e:
        print(f"Warning: Error reading config.ini, using defaults. Error: {e}")
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
    # 0. Handle Extensions
    extension_suffix = ""
    preserve_depth = cfg.get('preserve_extension_depth', 0)
    slugify_depth = cfg.get('slugify_extension_depth', 0)
    
    parts = inputString.split('.')
    effective_level = 0
    
    if preserve_depth > 0:
        # Calculate effective nesting level: use the configured level, 
        # but ensure we leave at least one part for the stem (len(parts)-1).
        # This allows "level=2" to work on "file.png" (treating it as level 1)
        # while correctly handling "archive.tar.gz" as level 2.
        effective_level = min(preserve_depth, len(parts) - 1)
    
    elif slugify_depth > 0:
        # User wants to force extension inclusion in the slug (hyphenated).
        effective_level = min(slugify_depth, len(parts) - 1)

    if effective_level > 0:
        # Iterative check: try to find the longest valid suffix of extensions
        # starting from the requested depth down to 1.
        found_extensions = []
        found_stem = []
        
        for depth in range(effective_level, 0, -1):
            potential_extensions = parts[-depth:]
            
            # Constraint: Extensions typically do not contain spaces and are not empty.
            if all(ext and not re.search(r'\s', ext) for ext in potential_extensions):
                found_extensions = potential_extensions
                found_stem = parts[:-depth]
                break
        
        if found_extensions:
            # Reassemble stem so Step 1 can process it
            inputString = ".".join(found_stem)
            
            # Form the suffix
            if preserve_depth > 0:
                # Standard extension preservation: .ext
                extension_suffix = "." + ".".join(found_extensions)
            elif slugify_depth > 0:
                # Slug mode: -ext
                extension_suffix = cfg['separator'] + cfg['separator'].join(found_extensions)
                if cfg['lowercase']:
                    extension_suffix = extension_suffix.lower()

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
    
    # 4.5. Collapse multiple separators (clean up "--" to "-")
    # This handles cases like "foo. bar" -> "foo- bar" -> "foo--bar" -> "foo-bar"
    # treating ". " effectively as "-" without needing specific config for it.
    if cfg['separator']:
        finalName = re.sub(re.escape(cfg['separator']) + '+', cfg['separator'], finalName)

    # 5. Remove trailing separators (new requirement)
    finalName = finalName.rstrip(cfg['separator'])

    # 6. Case conversion
    if cfg['lowercase']:
        finalName = finalName.lower()
        extension_suffix = extension_suffix.lower()

    return finalName + extension_suffix

def process_line(line, cfg, force_sanitize=False):
    """
    Processes a single line: Detects ZID and handles word limit accordingly.
    """
    # Regex to detect ZID at the start (matching Obsidian template zidLineRegex)
    # Group 1: Prefix (indentation, bullets, checkboxes)
    # Group 2: ZID (14 digits)
    # Group 3: Remaining text
    zidLineRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+|#{1,6}\s+)?)(\d{14})\s+(.*)$'
    prefixOnlyRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+|#{1,6}\s+))(.*)$'
    
    zid_match = re.match(zidLineRegex, line)
    
    if zid_match:
        prefix = zid_match.group(1) or ""
        zid = zid_match.group(2)
        raw_text = zid_match.group(3)
        safe_name = sanitizeName(raw_text, cfg)
        return f"{prefix}{zid}{cfg['separator']}{safe_name}"
    else:
        # Check config to see if we should process non-ZID lines
        # OR if we are forced to (single string selection case)
        if force_sanitize:
             return sanitizeName(line, cfg) if line.strip() else line
        
        if cfg['process_non_zid_lines']:
             
             # 2. Smart List Prefix Preservation (even if no ZID)
             # If a line looks like a task/list item, preserve the prefix.
             prefix_match = re.match(prefixOnlyRegex, line)
             if prefix_match:
                 prefix = prefix_match.group(1)
                 raw_text = prefix_match.group(2)
                 if raw_text.strip():
                     return f"{prefix}{sanitizeName(raw_text, cfg)}"
                 else:
                     return line
             
             # 3. Regular non-ZID, non-list, non-heading line
             if line.strip():
                return sanitizeName(line, cfg)
             else:
                return line
        else:
            return line

def process_string(input_string):
    """
    Main processing logic: Handles batch processing for multi-line strings.
    """
    cfg = get_config()
    
    # "Smart" Detection:
    # If it's a single line (no newlines), we assume it's a specific selection 
    # or a single title, so we ALWAYS sanitize it (legacy/substring support).
    # If it's multi-line, we respect the process_non_zid_lines flag.
    
    if "\n" not in input_string and "\r" not in input_string:
        return process_line(input_string, cfg, force_sanitize=True)
    
    lines = input_string.splitlines()
    processed_lines = []
    
    for line in lines:
        processed_lines.append(process_line(line, cfg))
                     
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