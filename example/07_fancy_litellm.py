import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

from art import *
from termcolor import colored

import pprint

script_name = os.path.basename(__file__)
tprint(script_name)

from litellm import completion

def generate_response(model_name, prompt, max_tokens=None, temperature=None, api_base=None):
    print(colored(f"Model: {model_name}", "cyan"))
    print(colored(f"Prompt: {prompt}", "yellow"))
    response = completion(
        model=model_name, 
        messages=[{ "content": prompt,"role": "user"}], 
        api_base=api_base
    )
    return response['choices'][0].message.content.strip()

response = generate_response("groq/llama3-70b-8192", "こんにちは !! 今日の気分はどう？")
print(colored(response, "green"))
print("-------------------")

response = generate_response("groq/gemma-7b-it", "こんにちは !! 今日の気分はどう？")
print(colored(response, "green")) 
print("-------------------")

response = generate_response("anthropic/claude-3-haiku-20240307", "こんにちは !! 今日の気分はどう？")
print(colored(response, "green"))