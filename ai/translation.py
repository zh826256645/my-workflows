#!/Users/zhonghao/miniconda3/envs/workflows/bin/python
"""
AI 翻译 & 词典工具
- 句子 → 中英互译
- 单词 → 词典查询（翻译、音标、词性、时态变形等）
"""

import re
import sys
from os.path import abspath, dirname, join

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

from ai.utils import (
    get_deepseek_message,
    get_model_scope_message,
    get_nvidia_nim_message,
    get_ollama_message,
)
from public.base import QueryHandlerAbstract
from public.thread_base import QueryThreadBase

translation_prompt = """你是一个专业的中英互译翻译器。你的任务是将输入的文本翻译成另一种语言（中文→英文，英文→中文）。

要求：
1. 只输出翻译后的文本，不要添加任何解释、注释或额外说明
2. 不要输出"译文："、"翻译结果："等前缀标签
3. 保持原文的语气、风格和专业术语
4. 确保翻译准确、流畅、自然

示例：
输入："今天天气真好。" → 输出："It's a beautiful day."
输入："Hello, how are you?" → 输出："你好，你好吗？"

现在，请直接输出翻译结果："""

dictionary_prompt = """你是一个专业的英语词典和语言助手。当用户输入一个单词时，提供全面的词典信息。

输出格式：
**单词**：原词
**音标**：英式音标 / 美式音标
**词性**：名词/动词/形容词/副词等
**释义**：中文释义（列出多个常见释义）
**词形变化**（如适用）：过去式、过去分词、现在分词（进行时）、第三人称单数、比较级、最高级等
**搭配**（如适用）：常见短语搭配
**例句**：1-2个英文例句及中文翻译

若输入的是中文词，则输出：
**词语**：原词
**英文翻译**：对应英文单词
**释义**：英文释义

请直接输出词典内容，不要添加额外说明。"""

translation_messages = [
    {
        "role": "system",
        "content": translation_prompt,
    }
]

dictionary_messages = [
    {
        "role": "system",
        "content": dictionary_prompt,
    }
]


_CJK_PUNCTUATION = set("。，！？；：、（）「」『』～…—…《》")

_CJK_MAX = ord("\u9fff")


def _has_cjk(text: str) -> bool:
    return any(ord(ch) > 127 and ord(ch) <= _CJK_MAX for ch in text)


def is_dictionary_query(query: str) -> bool:
    query = query.strip()
    if not query:
        return False

    if " " in query or "\n" in query:
        return False

    if any(ch in _CJK_PUNCTUATION for ch in query):
        return False

    if _has_cjk(query) and len(query) > 5:
        return False

    return True


_SPLIT_SECTION_LABELS = {"例句"}


def _split_example_sentences(text: str) -> list[str]:
    parts = re.split(r"\n\s*(?=[-•]|\d+[\.\)、]\s*)", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _parse_dictionary_sections(content: str) -> list[tuple[str, str]]:
    sections = re.split(r"\n(?=\*\*[^*]+\*\*[：:])", content.strip())

    result = []
    for section in sections:
        m = re.match(r"\*\*([^*]+)\*\*[：:]\s*(.*)", section, re.DOTALL)
        if m:
            label = m.group(1).strip()
            text = m.group(2).strip()
            if label in _SPLIT_SECTION_LABELS:
                for ex in _split_example_sentences(text):
                    result.append((label, ex))
            else:
                result.append((label, text))

    return result


class AiTranslationHandler(QueryHandlerAbstract):
    @property
    def ai_name(self):
        return "AI"

    def is_available(self, query: str) -> bool:
        if query:
            return True
        return False

    def get_ai_message(self, query: str, is_word: bool = False) -> str:
        return ""

    @staticmethod
    def _make_item(text: str, label: str, query: str, ai_name: str, use_largetype: bool = True) -> dict:
        item = {
            "arg": text,
            "title": text.split("\n")[0],
            "subtitle": f"{label}；由 {ai_name}: {query}",
            "icon": "",
        }
        if use_largetype and "\n" in text:
            item["text"] = {"largetype": text}
        return item

    def get_result(self, query: str) -> dict:
        items = []
        is_word = is_dictionary_query(query)
        content = self.get_ai_message(query, is_word=is_word)

        if not content:
            return {"items": items}

        if is_word:
            sections = _parse_dictionary_sections(content)
            if sections:
                for label, text in sections:
                    items.append(
                        self._make_item(text, label, query, self.ai_name)
                    )
            else:
                items.append(
                    self._make_item(content, "词典", query, self.ai_name)
                )
        else:
            items.append(
                self._make_item(content, "翻译", query, self.ai_name, use_largetype=False)
            )

        return {"items": items}


class OllamaTranslationHandler(AiTranslationHandler):
    """通过 Ollama 翻译"""

    @property
    def ai_name(self):
        return "Ollama"

    def get_ai_message(self, query, is_word=False):
        _messages = (dictionary_messages if is_word else translation_messages)[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_ollama_message(_messages)
        return ai_message.content


class DeepseekTranslationHandler(AiTranslationHandler):
    """通过 Deepseek 翻译"""

    @property
    def ai_name(self):
        return "Deepseek"

    def get_ai_message(self, query, is_word=False):
        _messages = (dictionary_messages if is_word else translation_messages)[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_deepseek_message(_messages)
        return ai_message.content


class ModelScopeTranslationHandler(AiTranslationHandler):
    """通过魔搭翻译"""

    @property
    def ai_name(self):
        return "ModelScope"

    def get_ai_message(self, query, is_word=False):
        _messages = (dictionary_messages if is_word else translation_messages)[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_model_scope_message(_messages)
        return ai_message.content


class NvidiaNIMTranslationHandler(AiTranslationHandler):
    """通过 Nvidia NIM 翻译"""

    @property
    def ai_name(self):
        return "Nvidia NIM"

    def get_ai_message(self, query, is_word=False):
        _messages = (dictionary_messages if is_word else translation_messages)[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_nvidia_nim_message(
            _messages, model="mistralai/ministral-14b-instruct-2512"
        )
        return ai_message.content


def main():
    thread_base = QueryThreadBase()
    # thread_base.add_handler(OllamaTranslationHandler())
    thread_base.add_handler(DeepseekTranslationHandler())
    # thread_base.add_handler(ModelScopeTranslationHandler())
    # thread_base.add_handler(NvidiaNIMTranslationHandler())

    thread_base.main()


if __name__ == "__main__":
    main()
