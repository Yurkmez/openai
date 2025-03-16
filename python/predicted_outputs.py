from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env
client = OpenAI()

try:

    code = """
        class User {
            firstName: string = "";
            lastName: string = "";
            username: string = "";
        }
        export default User;
    """

    refactor_prompt = """
        Replace the "username" property with an "email" property. Respond only 
        with code, and with no markdown formatting.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": refactor_prompt
            },
            {
                "role": "user",
                "content": code
            }
        ],
        prediction={
            "type": "content",
            "content": code
        }
    )

    print(completion)
    print("___________________")
    print(completion.choices[0].message.content)

except Exception as error:
    print("Error connections with OpenAI API: ", error)
