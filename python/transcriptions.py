from openai import OpenAI
from dotenv import load_dotenv
import json
from pathlib import Path
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()  # take environment variables from .env

client = OpenAI()

model = "whisper-1"
audio_transcriptions_dir = "transcriptions"
file_read_name = 'test_v1.m4a'
file_write_name = 'test_v1.json'

try:
    # Dir, path, file
    module_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir_and_name_file_read = os.path.join(
        module_dir, audio_transcriptions_dir, file_read_name)
    audio_dir_and_name_file_write = os.path.join(
        module_dir, audio_transcriptions_dir, file_write_name)
    # Open file
    audio_file = open(audio_dir_and_name_file_read, "rb")
    # Request
    transcription = client.audio.transcriptions.create(
        model=model,
        file=audio_file
    )

    transcription_dict = transcription.model_dump()
    print(transcription_dict)

    # Сохраняем JSON в файл
    with open(audio_dir_and_name_file_write, "w", encoding="utf-8") as f:
        json.dump(transcription_dict, f, ensure_ascii=False,
                  indent=4)  # Красивый вывод

    print("Successfully saved generated audio file:", file_write_name)
except Exception as e:
    print("Some error occured: ", e)
