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
        'slug_word_count': 6,
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

    # 5. Case conversion
    if cfg['lowercase']:
        finalName = finalName.lower()

    return finalName

def process_string(input_string):
    """
    Main processing logic: Detects ZID and handles word limit accordingly.
    """
    cfg = get_config()
    
    # Regex to detect ZID at the start (matching Obsidian template zidLineRegex)
    # /^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+)?)(\d{14})\s+(.*)$/
    zidLineRegex = r'^(\s*(?:(?:[-*+]|\d+\.)(?:\s+\[[ xX]\])?\s+)?)(\d{14})\s+(.*)$'
    zid_match = re.match(zidLineRegex, input_string)
    
    if zid_match:
        prefix = zid_match.group(1) or ""
        zid = zid_match.group(2)
        raw_text = zid_match.group(3)
        safe_name = sanitizeName(raw_text, cfg)
        return f"{prefix}{zid}{cfg['separator']}{safe_name}"
    else:
        return sanitizeName(input_string, cfg)

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