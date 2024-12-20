import argparse
import pyperclip
import re

def get_clipboard_text():
    return pyperclip.paste()

def set_clipboard_text(text):
    pyperclip.copy(text)

def replace_german_chars(input_string):
    # Replacement for German special characters
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue'
    }
    for char, replacement in replacements.items():
        input_string = input_string.replace(char, replacement)
    return input_string

def process_string(input_string):
    # Apply replacements for German characters
    input_string = replace_german_chars(input_string)
    
    # Allow hyphens to remain and remove other unwanted characters
    cleaned_string = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]', '', input_string)
    
    # Convert the string to lowercase
    cleaned_string = cleaned_string.lower()
    
    # Replace spaces with "-"
    processed_string = re.sub(r'\s+', '-', cleaned_string)
    
    return processed_string

def main():
    parser = argparse.ArgumentParser(description="Process input string or clipboard content: lowercase, replace spaces with '-', remove special characters, handle German umlauts.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    if args.input_string is None:
        clipboard_content = get_clipboard_text()
        # print("Clipboard content before processing:", clipboard_content)  # Debug statement
        output_string = process_string(clipboard_content)
        set_clipboard_text(output_string)
    else:
        output_string = process_string(args.input_string)
        set_clipboard_text(output_string)
    print(output_string)

if __name__ == "__main__":
    main()