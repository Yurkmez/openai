from openai import OpenAI
from dotenv import load_dotenv
import sys
import os
import requests
import base64
from urllib.parse import urlparse
import json
from pprint import pprint
from datetime import datetime
from utils.conversion import object_to_dict
from utils.fileUtils import generate_file_name_with_extension
from utils.fileUtils import write_image_data_to_json_file

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()  # take environment variables from .env

my_prompt = 'Battle of the ships'  # _________Text request
size = "1024x1024"
style = "natural"
model = "dall-e-3"
json_filename = "images.json"

try:
    client = OpenAI()

    response = client.images.generate(  # __________ Request
        model=model,
        prompt=my_prompt,
        size=size,
        style=style,
        response_format="b64_json",  # ______________ format - b64_json
    )
    # pprint(object_to_dict(response))
    b64_data = response.data[0].b64_json
    revised_prompt = response.data[0].revised_prompt

    if b64_data:
        # __________ preparing directory
        module_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(module_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        file_name = generate_file_name_with_extension(
            my_prompt, images_dir, "png")
        file_path = os.path.join(images_dir, file_name)
        # __________ Save images b64_json format
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(b64_data))
            print("Successfully saved image:", file_name)

        # __________ Save images JSON format
        image_data = {
            "prompt": my_prompt,
            "revisedPrompt": revised_prompt,
            "size": size,
            "model": model,
            "style": style,
            "date": datetime.now().strftime("%d-%m-%Y"),
            "base64": b64_data,
        }
        json_file_path = os.path.join(images_dir, json_filename)
        write_image_data_to_json_file(json_file_path, image_data)
    else:
        print("Error get data from openAI")
except Exception as error:
    print("Error connections with OpenAI API: ", error)
