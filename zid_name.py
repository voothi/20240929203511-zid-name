import argparse
import pyperclip
import re

def get_clipboard_text():
    return pyperclip.paste()

def set_clipboard_text(text):
    pyperclip.copy(text)

def replace_chars(input_string):
    # Замена специальных символов
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'ẞ': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue', '_': '-', ':': '-', '. ': '-', '.': '-'
    }
    for char, replacement in replacements.items():
        input_string = input_string.replace(char, replacement)
    return input_string

def process_string(input_string):
    """
    Обрабатывает строку: оставляет только первые 6 слов,
    соединяет их дефисами и приводит к нижнему регистру.
    """
    processed_string = replace_chars(input_string)

    cleaned_for_splitting = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s-]', '', processed_string)

    words = cleaned_for_splitting.split()

    first_words = words[:6]

    final_name = '-'.join(first_words)

    return final_name.lower()

def main():
    parser = argparse.ArgumentParser(description="Process string for a filename: takes first words, lowercases, and joins with '-'.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    input_text = args.input_string if args.input_string is not None else get_clipboard_text()
    
    output_string = process_string(input_text)
    
    set_clipboard_text(output_string)

    print(output_string)

if __name__ == "__main__":
    main()