from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import sys
import os
from pprint import pprint
from utils.conversion import object_to_dict
from utils.fileUtils import generate_file_name_with_extension

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()  # take environment variables from .env

client = OpenAI()

model = "tts-1"
voice = "alloy"
input_text = "Расскажи что-нибудь про море."
response_format_file = "wav"
# Audio file will be stored in /audio/mp3 or /audio/wav folders
audio_folder_name = "audio"

try:
    # Step-1 - request
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text,
        response_format=response_format_file)
    # Step-2 - make directory, file path and file name
    module_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(module_dir, response_format_file)
    os.makedirs(audio_dir, exist_ok=True)
    file_name = generate_file_name_with_extension(
        prompt=input_text,
        dir=audio_dir,
        extension=response_format_file)
    file_path = os.path.join(audio_dir, file_name)

    with open(file_path, "wb") as audio_file:
        audio_file.write(response.content)

    print("Successfully saved generated audio file:", file_name)
except Exception as e:
    print("ome error occured: ", e)
