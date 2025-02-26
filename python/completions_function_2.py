import sys
import os
import json
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv
from utils.conversion import object_to_dict

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()  # take environment variables from .env
client = OpenAI()


def get_stock_price(stock):
    top_10_stocks = {
        "AAPL": {"name": "Apple Inc.", "price": 182.52, "market_cap": "2.8T"},
        "MSFT": {"name": "Microsoft Corp.", "price": 404.87, "market_cap": "3.0T"},
        "GOOGL": {"name": "Alphabet Inc. (Class A)", "price": 141.57, "market_cap": "1.8T"},
        "AMZN": {"name": "Amazon.com Inc.", "price": 174.58, "market_cap": "1.7T"},
        "NVDA": {"name": "NVIDIA Corp.", "price": 726.15, "market_cap": "1.8T"},
        "TSLA": {"name": "Tesla Inc.", "price": 192.01, "market_cap": "615B"},
        "BRK.B": {"name": "Berkshire Hathaway Inc. (Class B)", "price": 350.27, "market_cap": "770B"},
        "META": {"name": "Meta Platforms Inc.", "price": 465.23, "market_cap": "1.2T"},
        "LLY": {"name": "Eli Lilly and Co.", "price": 780.99, "market_cap": "740B"},
        "JPM": {"name": "JPMorgan Chase & Co.", "price": 182.50, "market_cap": "530B"}
    }
    symbol = stock.get("symbol")  # Получаем строку, например "AAPL"
    stock_info = top_10_stocks.get(symbol, {"price": 100.00})

    stock_price = {
        "symbol": symbol,
        "price": stock_info["price"],
    }
    return json.dumps(stock_price)


system_text = "Дай ответ не просто с ценой акций, а корткой аналитикой, не более 100 слов."


def process_user_text_input(user_text, system_text):
    tools = [{
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
    }]  # Здесь никакой запятой!!!!!!!!!!!!!!!!!!
    # Иначе это превращается в кортеж
    model = "gpt-4o-mini"
    avialable_functions = {"get_stock_price": get_stock_price, }
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

        # (2)____________ Вызов локальной функции
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
    print("Сделайте запрос стоимости акций")
    print("Apple, Microsoft, Alphabet, Amazon, NVIDIA, Tesla, Meta")

    user_input = input("\nEnter your text (or type 'exit' to quit): \n >")
    if user_input.lower() == "exit":
        print("Exiting program...")
        break
    process_user_text_input(user_text=user_input, system_text=system_text)

# text = 'Какая стоимость акций Amazon?'
# process_user_text_input(text)
