import sys
import os
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from utils.conversion import object_to_dict

load_dotenv()  # take environment variables from .env
client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "what's in this image?"},
                {"type": "image_url",
                         "image_url": {
                             "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                             "detail": "high",
                         }
                 }
            ],
        }],
        max_tokens=200,
    )

    pprint(object_to_dict(response))

except Exception as error:
    print("Error connections with OpenAI API: ", error)
