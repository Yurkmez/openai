import os
import re


def generate_file_name_with_extension(prompt, dir, extension):
    '''
    Generate a unique file name with extention based on the prompt
    '''
    base_file_name = "_".join(prompt.lower().split()[:3])
    # get_next_version_number - смотрит наличие
    version = get_next_version_number(base_file_name, extension, dir)
    return f"{base_file_name}_v{version}.{extension}"


'''
base_file_name = "_".join(prompt.lower().split())[:3]
        prompt.lower() – Преобразует строку prompt в нижний регистр.
        .split() – Разбивает строку prompt на список слов по пробелам.
        "_".join(...) – Соединяет слова из списка обратно в строку, вставляя между ними символ _ (подчеркивание).
        [:3] – выбирает только первые 3 слова.
        
        Пример.
            prompt = "Hello World This is Python"
            base_file_name = "_".join(prompt.lower().split()[:3])
            print(base_file_name)  # "hello_world_this"


'''


def get_next_version_number(base_file_name, extension, dir):
    # Generate version number
    if not dir or os.path.exists(dir):
        return 1
    file_pattern = re.compile(
        rf"^{base_file_name}_v(\d+)\.{re.escape(extension)}$")
    highest_version = 0
    existing_files = os.listdir(dir)
    for file in existing_files:
        # Проверяем, соответствует ли имя файла шаблону
        match = file_pattern.match(file)
        if match:
            # Извлекаем номер версии из первой группы `(\d+)`
            file_version = int(match.group(1))
            # Запоминаем наибольшую версию
            highest_version = max(highest_version, file_version)
    return highest_version + 1


'''
file_pattern = re.compile(rf"^{base_file_name}_v(\d+)\.{re.escape(extension)}$")
        rf"..." – это raw f-string, позволяющая вставлять 
        переменные (base_file_name, extension) без необходимости экранировать \.
        ^ – начало строки.
        {base_file_name}_v(\d+) – ищем файлы, начинающиеся с base_file_name, 
        затем _v, а после – число (\d+), обозначающее номер версии.
        \.{re.escape(extension)}$ – re.escape(extension) экранирует точку 
        в расширении (.png, .jpg и т. д.), $ обозначает конец строки.
        
        Пример. 
        ^image_v(\d+)\.png$
        Будет находить файлы, такие как:
            image_v1.png
            image_v2.png
            image_v10.png
'''
