import sys
import os
import json
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from utils.conversion import object_to_dict
import requests


sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()  # take environment variables from .env
client = OpenAI()


def get_stock_price_API(stock):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    # api_functon = "TIME_SERIES_DAILY"
    api_functon = "GLOBAL_QUOTE"
    if not api_key:
        print('ALPHA_VANTAGE_API_KEY not found')
        sys.exit()
    symbol = stock.get("symbol")
    URL = f"https://www.alphavantage.co/query?function={api_functon}&symbol={symbol}&apikey={api_key}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = float(data["Global Quote"]["05. price"])
            # print(json.dumps(price, indent=2))
        else:
            price = "Unknown"
        stock_price = {
            "symbol": symbol,
            "price": price,
        }
        # print(price)
        return json.dumps(stock_price)
    else:
        print("Error fetching data: {response.status_code}")


system_text = "Дай ответ не просто с ценой акций, а корткой аналитикой, не более 50 слов."


def process_user_text_input(user_text, system_text):
    tools = [{
        "type": "function",
        "function": {
            "name": "get_stock_price_API",
            "description": "Get the current stock price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol"
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "symbol"
                    ]
                },
            "strict": True
        }
    }]  # Здесь никакой запятой!!!!!!!!!!!!!!!!!!
    # Иначе это превращается в кортеж
    model = "gpt-4o-mini"
    avialable_functions = {"get_stock_price_API": get_stock_price_API, }
    messages = []
    messages.append(
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_text,
                }
            ]
        })
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_text
                }
            ]
        })

    # (1)____________ Первый запрос
    first_response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )

    tool_calls = first_response.choices[0].message.tool_calls
    if tool_calls:

        # (2)____________ Вызов функции
        # print("You have to call a function")
        function_name = tool_calls[0].function.name
        function_to_call = avialable_functions[function_name]
        function_arg_to_pass = json.loads(tool_calls[0].function.arguments)
        function_response = function_to_call(function_arg_to_pass)
        # print("Result of the `{function_name}` function call: ", function_response)

        # (3)____________ Send result of the function call to the assistant
        first_assistant_message = first_response.choices[0].message
        messages.append(first_assistant_message)
        # pprint(object_to_dict(messages), indent=1)

        tool_call_id = tool_calls[0].id
        tool_response_message = {
            "role": "tool",
            "content": [
                {"type": "text", "text": function_response, }
            ],
            "tool_call_id": tool_call_id,
        }  # Здесь никакой запятой!!!!!!!!!!!!!!!!!!
        # Иначе это превращается в кортеж
        messages.append(tool_response_message)
        # pprint(object_to_dict(messages), indent=1)
        # print(json.dumps(messages, ensure_ascii=False, indent=2))  # Должен быть JSON-список
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools
        )
        print(second_response.choices[0].message.content)

    else:
        print("There is no instruction to call a function\n")
        print(first_response.choices[0].message.content)
    #     # sys.exit()
    print("\n*****************************\n")


while True:
    print("Сделайте запрос стоимости акций (Apple, Microsoft, Meta, ...)\n")
    user_input = input("Введите запрос или 'exit' для выхода): \n >")
    if user_input.lower() == "exit":
        print("Выход из программы...")
        break
    process_user_text_input(user_text=user_input, system_text=system_text)
