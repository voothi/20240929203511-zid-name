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
    Обрабатывает строку: оставляет только первые 3 слова,
    соединяет их дефисами и приводит к нижнему регистру.
    """
    # 1. Сначала применяем базовые замены символов (например, для немецкого языка)
    processed_string = replace_chars(input_string)

    # 2. Удаляем все символы, кроме букв (латиница и кириллица), цифр и пробелов.
    #    Пробелы важны для последующего разделения на слова.
    cleaned_for_splitting = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', '', processed_string)

    # 3. Разбиваем очищенную строку на список слов.
    #    Метод .split() автоматически обрабатывает несколько пробелов подряд.
    words = cleaned_for_splitting.split()

    # 4. Берем первые три слова из списка.
    first_three_words = words[:6]

    # 5. Соединяем эти три слова через дефис.
    final_name = '-'.join(first_three_words)

    # 6. Приводим итоговую строку к нижнему регистру.
    #    На этом этапе лишних символов в начале или конце быть не должно,
    #    но .lower() обязателен.
    return final_name.lower()

def main():
    parser = argparse.ArgumentParser(description="Process input string or clipboard content: takes first 3 words for a filename, lowercases, and joins with '-'.")
    parser.add_argument("input_string", nargs='?', type=str, help="Input string to process. If not provided, clipboard content will be used.")
    args = parser.parse_args()
    
    if args.input_string is None:
        clipboard_content = get_clipboard_text()
        output_string = process_string(clipboard_content)
        # Мы больше не устанавливаем измененный текст в буфер обмена,
        # так как это может быть нежелательно (теряется оригинальный текст).
        # Если вы хотите вернуть это поведение, раскомментируйте строку ниже.
        set_clipboard_text(output_string) 
    else:
        output_string = process_string(args.input_string)
        # Аналогично, не меняем буфер обмена при вызове с аргументом.
        set_clipboard_text(output_string)

    # Выводим результат в stdout, чтобы другие скрипты могли его использовать.
    print(output_string)

if __name__ == "__main__":
    main()