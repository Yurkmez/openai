import sys
import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
# Импортируем наш модуль
# форматирования выходных данных в терминале
from utils.conversion import object_to_dict

load_dotenv()  # take environment variables from .env

# print(os.getenv("OPENAI_API_KEY"))  # Проверяем, какой API-ключ используется
# А также, если он другой (API_KEY - установлен глобально, поэтому из файла .env
# ключ не берется, а используется глобальный), см. файл - k_env.txt)

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # {"role": "system", "content": "Отвечай кратко, но весело в формате json."},
        {"role": "system", "content": "Отвечай кратко, но весело."},
        {"role": "user", "content": "Сколько тебе лет?"},
    ],

    # Если мы запрашиваем ответ в формате json,то в запросе должно быть слово "json"
    # response_format={'type': 'json_object'},

    # temperature=0.2,
    # stop=["}"],
    # top_p=0.2,
    # presence_penalty=0.2,
    # frequency_penalty=0.2,
    # max_completion_tokens=20,
    # n=2,
)

# _____________________________________________________
# Если раскладка клавиатуры не utf-8, а например CP1254 → это турецкая кодировка,
# то следует изменить раскладку
# print(sys.stdout.encoding)
sys.stdout.reconfigure(encoding='utf-8')
# print(sys.stdout.encoding)
# ________________________________________________

# print(completion.choices[0].message)
pprint(object_to_dict(completion.choices), indent=1)
# pprint(object_to_dict(completion), indent=1)
