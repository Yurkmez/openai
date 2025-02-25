import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

# ________________ Проверки по API-ключу _________________
# Проверяем, не задан ли ключ глобально
# for key, value in os.environ.items():
#     if "OPENAI" in key:  # Фильтруем только переменные, связанные с OpenAI
#         print(key, "=", value)
# Если OPENAI_API_KEY уже есть в системе (глобально), .env его не перезапишет.
# Поэтому, если он есть проще его удалить (см. файл k_env.txt)

# print(os.getenv("OPENAI_API_KEY"))  # Проверяем, какой API-ключ используется
# ___________________________________________________

client = OpenAI()

# chat.completions - означает, что мы будем использовать текстовую модель "завершение текста"
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
