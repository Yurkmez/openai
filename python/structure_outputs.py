from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env
client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "calendar_event",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "date": {
                            "type": "string"
                        },
                        "participants": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                    },
                    "required": ["name", "date", "participants"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    event = json.loads(response.output_text)
    print(event)

except Exception as error:
    print("Error connections with OpenAI API: ", error)
