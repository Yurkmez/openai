from openai import OpenAI
from dotenv import load_dotenv
import sys
import os
import requests
from urllib.parse import urlparse
import json
from pprint import pprint
from utils.conversion import object_to_dict
from utils.fileUtils import generate_file_name_with_extension

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()  # take environment variables from .env
client = OpenAI()

# STEP-1 Text request
my_prompt = 'Horse sitting on the table'

# STEP-2 Request
response = client.images.generate(
    model="dall-e-3",
    prompt=my_prompt,
    # size="1024x1024", # by default
    # quality="standard", # by default
    # n=1, # by default
)

# pprint(object_to_dict(response))

# STEP-3 Response
image_url = response.data[0].url
# print(image_url)

# STEP-4 Get images by url and save it
# __________ preparing directory
module_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(module_dir, "images")
# print(images_dir)
os.makedirs(images_dir, exist_ok=True)
# __________ file_name, file_path

file_name = generate_file_name_with_extension(my_prompt, images_dir, "png")
file_path = os.path.join(images_dir, file_name)
# _________ Get image and save
try:
    response = requests.get(image_url, stream=True)
    # stream=True- we dont load whole image in the RAM,
    # we load it in stream
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")

    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise Exception(
            f"The URL does not point to an image. Content-Type: {content_type}")

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    print("Successfully saved image:", file_name)
except Exception as error:
    print("Error downloading image:", error)
