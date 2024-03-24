import os
import sys
import requests
from dotenv import load_dotenv
from huggingface_hub import HfApi

from .formatter import QAFormatterIO


load_dotenv()
API_TOKEN = os.environ.get('API_HF_TOKEN')
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}
DEFAULT_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_API_URL = "https://api-inference.huggingface.co/models"


class ConvAgent:
    def __init__(self, url, model=None, content_prompt=None,
                 width=None, is_table=True):
        self.formatter = QAFormatterIO(is_table=is_table, width=width)

        valid_model = self.is_model_valid(model)
        if not valid_model:
            if model is not None:
                self.formatter.console.log(
                    f"WARNING: {model} is not a valid model"
                    f" .. default model will be used: {DEFAULT_MODEL}")
            self.model = DEFAULT_MODEL
        else:
            self.model = model

        self.api_url = f"{HF_API_URL}/{self.model}"

        self.content = (f"You know everything there is to know about: {url}. "
                        "Stop generating words once the question is answered. "
                        "Give the shortest answer possible.")
        if content_prompt is not None and isinstance(content_prompt, str):
            self.content += f" {content_prompt}"

        self.history = ""

    def is_model_valid(self, model):
        if model is None or not isinstance(model, str):
            return False

        for m in HfApi().list_models(filter="text-generation"):
            if m.id == model:
                return True

        return False

    def clean_response(self, response):
        return (response
                .replace("<|im_start|>user", "")
                .replace("<|im_start|>assistant", "")
                .replace("<|im_end|>", "")
                .strip())

    def get_answer(self, input_text):
        self.history += "<|im_start|>user" + input_text + "<|im_end|>\n"
        payload = {
            "inputs": self.history,
            "role": "system",
            "content": self.content,
            "max_new_tokens": 10000,
        }

        response = (requests.post(self.api_url, headers=HEADERS, json=payload)
                    .json()[0]['generated_text']
                    .replace(self.history, ''))
        self.history += "<|im_start|>assistant" + response + "<|im_end|>\n"

        return self.clean_response(response)

    def one_step(self):
        try:
            input_text = self.formatter.ask()
            if input_text == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                return
        except (KeyboardInterrupt, EOFError):
            res = input("\nDo you really want to exit ([y]/n)? ")
            if res in ["y", "yes"]:
                self.formatter.answer("Hope you had fun :) Bye Bye!")
                sys.exit()
            else:
                return
        self.formatter.answer(self.get_answer(input_text))

    def start_conversation(self):
        while True:
            self.one_step()
