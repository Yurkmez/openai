import sys
import os
import json
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from utils.conversion import object_to_dict

load_dotenv()  # take environment variables from .env
client = OpenAI()

# Здесь в примере tools - список объектов [{...}],
# но при вызове в # Первый запрос
# first_response = client.chat.completions.create(
# ...
# мы указываем
# tools=tools
# выдается ошибка:
# "параметр tools[0] должен быть объектом,
# а у вас tools — это список, содержащий объект."
# Поэтому здесь просто объект - {}
tools = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
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
},


def get_stock_price(stock):
    symbol = stock.get("symbol")
    stock_price = {
        "symbol": symbol,
        "price": 100
    }
    return json.dumps(stock_price)
# print(get_stock_price({"symbol": "AAPL"}))


avialable_functions = {"get_stock_price": get_stock_price, }

messages = []
messages.append(
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Какая стоимость акций Apple?"
            }
        ]
    })

# (1)____________ Первый запрос
first_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# pprint(object_to_dict(first_response), indent=1)
#  Что мы получаем (см. файл: k_response_first.txt)

# (2)____________ Вызов локальной функции
tool_calls = first_response.choices[0].message.tool_calls
if tool_calls:
    print("You have to call a function")
    function_name = tool_calls[0].function.name
    function_to_call = avialable_functions[function_name]
    function_arg_to_pass = json.loads(tool_calls[0].function.arguments)
    function_response = function_to_call(function_arg_to_pass)
    print(function_response)
else:
    print("There is no instruction to call a function")
    sys.exit()
