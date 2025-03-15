from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import sys
import os
import base64
from pprint import pprint
from utils.conversion import object_to_dict
from utils.fileUtils import generate_file_name_with_extension

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()  # take environment variables from .env

client = OpenAI()

model = "gpt-4o-audio-preview"
input_text = "Расскажи что-нибудь про океан."
response_format_file = "wav"
# Audio file will be stored in /audio/mp3 or /audio/wav folders
audio_folder_name = "audio"

try:
    # Step-1 - request
    completion = client.chat.completions.create(
        model=model,
        modalities=["text", "audio"],
        audio={"voice": "ballad", "format": "wav"},
        messages=[
            {
                "role": "user",
                "content": input_text
            }
        ]
    )
    print(completion.choices[0].message.audio.transcript)

    # Step-2 - make directory, file path and file name
    module_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(module_dir, response_format_file)
    os.makedirs(audio_dir, exist_ok=True)
    file_name = generate_file_name_with_extension(
        prompt=input_text,
        dir=audio_dir,
        extension=response_format_file)
    file_path = os.path.join(audio_dir, file_name)

    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open(file_path, "wb") as f:
        f.write(wav_bytes)

    print("Successfully saved generated audio file:", file_name)
except Exception as e:
    print("ome error occured: ", e)
