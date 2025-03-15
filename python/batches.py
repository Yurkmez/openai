import sys
import os
import json
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from utils.conversion import object_to_dict

load_dotenv()  # take environment variables from .env

# print(os.getenv("OPENAI_API_KEY"))  # Проверяем, какой API-ключ используется,
# a если он другой (API_KEY - установлен глобально, поэтому из файла .env
# ключ не берется, а используется глобальный), см. файл - k_env.txt)

client = OpenAI()

try:
    # STEP 1 - Uploading file for Batch API
    # batch_input_file = client.files.create(
    #     file=open("./batch/batch_input.jsonl", "rb"),
    #     purpose="batch")
    # pprint(object_to_dict(batch_input_file))

    # STEP 2 - Creating a Batch
    # batch_creation_response = client.batches.create(
    #     input_file_id=batch_input_file.id,
    #     endpoint="/v1/chat/completions",
    #     completion_window="24h",
    #     metadata={
    #         "description": "My first Batch",
    #         "internal_id": "123",
    #     }
    # )
    # batch_creation_response_id = batch_creation_response.id
    # print(batch_creation_response_id)

    # STEP 3 - Checking status of the batch
    # batch = client.batches.retrieve(batch_creation_response_id)
    # batch = client.batches.retrieve("batch_67d4519a742881909b67b50e554bfbf0")
    # output_file_id = batch.output_file_id
    # pprint(object_to_dict(batch))

    # STEP 4 - Retrieving the batch results
    file_response = client.files.content("file-Ag97vweroAbuRunPKy4RXP")
    # file_response = client.files.content(output_file_id)
    # print(file_response.text)

    # Мы получаем ответ в формате NDJSON (Newline Delimited JSON),
    # где каждая строка представляет собой отдельный JSON-объект.

    # Для вывода какого либо конкретного значения нужно
    # обработать его построчно.
    # texts = []
    # for line in file_response.text.strip().split("\n"):  # Разбиваем на строки
    #     try:
    #         data = json.loads(line)  # Загружаем строку как JSON
    #         # Достаем текст
    #         message = data["response"]["body"]["choices"][0]["message"]["content"]
    #         texts.append(message)
    #     except json.JSONDecodeError as e:
    #         print(f"Ошибка парсинга JSON: {e}")

    # # Выводим тексты ответов
    # for text in texts:
    #     print("____________")
    #     print(text)
    # # Запись в файл
    # with open("./batch/batch_output.jsonl", "wb") as f_out:
    #     for chunk in file_response.iter_bytes(1024):
    #         f_out.write(chunk)

    # STEP 5 - Getting list of all batches
    # list_my_butches = client.batches.list()
    # pprint(object_to_dict(list_my_butches.data))

    # STEP 6 - Cancel a batch
    # client.batches.cancel("batch_abc123")
    client.batches.cancel("batch_67d4519a742881909b67b50e554bfbf0")
    client.batches.cancel("batch_67d44ec9f3b88190ad375c63b2e3ccb7")
    client.batches.cancel("batch_67d44e59b67c8190b28805513bf225ca")
    client.batches.cancel("batch_67d44d99928881908cabc585307c04fe")
    client.batches.cancel("batch_67d44b47b1c4819087ebf5a7691ac68b")

except Exception as e:
    print("Error:", e)
