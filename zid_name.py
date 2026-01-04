import argparse
import pyperclip
import re
import configparser
import os

def get_config():
    """Reads all settings from config.ini."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    defaults = {
        'word_limit': 6,
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
            'word_limit': config.getint('Settings', 'word_limit', fallback=defaults['word_limit']),
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

def replace_chars(input_string, replacements):
    # Replace special characters from config
    for char, replacement in replacements.items():
        input_string = input_string.replace(char, replacement)
    return input_string

def process_string(input_string):
    """
    Processes a string using settings from config.ini.
    """
    cfg = get_config()
    
    # 1. Character replacements
    processed_string = replace_chars(input_string, cfg['replacements'])

    # 2. Regex filtering
    cleaned_for_splitting = re.sub(cfg['allowed_chars_regex'], '', processed_string)

    # 3. Splitting and limiting
    words = cleaned_for_splitting.split()
    first_words = words[:cfg['word_limit']]

    # 4. Joining with separator
    final_name = cfg['separator'].join(first_words)

    # 5. Case conversion
    if cfg['lowercase']:
        final_name = final_name.lower()

    return final_name

def main():
    parser = argparse.ArgumentParser(description="Process string for a filename based on config.ini settings.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    input_text = args.input_string if args.input_string is not None else get_clipboard_text()
    
    output_string = process_string(input_text)
    
    set_clipboard_text(output_string)

    print(output_string)

if __name__ == "__main__":
    main()