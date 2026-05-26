# -*- coding: utf-8 -*-
"""
工具函数
"""

import sys
from dataclasses import dataclass
from os.path import abspath, dirname, join

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

from typing import Any

from ollama import Client
from openai import OpenAI

try:
    import config
except ImportError:
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


def get_deepseek_message(messages: list, model: str = "deepseek-v4-flash") -> AiMessage:
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


def get_model_scope_message(
    messages: list, model: str = "Qwen/Qwen3-Coder-480B-A35B-Instruct"
) -> AiMessage:
    client = OpenAI(
        api_key=config.MODEL_SCOPE_API_KEY,
        base_url="https://api-inference.modelscope.cn/v1/",
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    return AiMessage(
        content=response.choices[0].message.content, original_response=response
    )


def get_nvidia_nim_message(
    messages: list, model: str = "nvidia/llama-3.1-nemotron-70b-instruct"
) -> AiMessage:
    client = OpenAI(
        api_key=config.NVIDIA_NIM_API_KEY,
        base_url="https://integrate.api.nvidia.com/v1",
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    return AiMessage(
        content=response.choices[0].message.content, original_response=response
    )
