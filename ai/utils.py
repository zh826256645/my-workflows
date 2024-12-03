# -*- coding: utf-8 -*-
"""
工具函数
"""
from dataclasses import dataclass
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

from typing import Any

from ollama import Client
from openai import OpenAI

try:
    import config
except Exception:
    import default_config as config


@dataclass
class AiMessage:
    content: str
    original_response: Any


def get_ollama_message(messages: list, model: str = "qwen2.5:3b") -> AiMessage:
    client = Client(
        host=config.OLLAMA_HOST,
        headers={"x-some-header": "some-value"},
    )
    response = client.chat(model=model, messages=messages)
    return AiMessage(content=response["message"]["content"], original_response=response)


def get_deepseek_message(messages: list, model: str = "deepseek-chat") -> AiMessage:
    client = OpenAI(
        api_key=config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    return AiMessage(
        content=response.choices[0].message.content, original_response=response
    )
