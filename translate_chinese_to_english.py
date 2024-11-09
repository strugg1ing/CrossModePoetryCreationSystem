from translate import Translator
import sys

def translate_english_to_chinese(english_text):
    translator = Translator(to_lang="zh-Hans")
    return translator.translate(english_text)

def translate_txt_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        english_text = file.read()

    chinese_text = translate_english_to_chinese(english_text)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(chinese_text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python translate_english_to_chinese.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    translate_txt_file(input_file_path, output_file_path)