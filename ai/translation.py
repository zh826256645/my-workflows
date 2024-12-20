#!/usr/local/bin/python3.10
"""
让 AI 生成变量名
"""
import re
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

from public.thread_base import QueryThreadBase

from public.base import QueryHandlerAbstract
from ai.utils import get_ollama_message, get_deepseek_message

prompt = """### Role: 中英互译专家

### Background:
用户可能需要频繁进行中英文之间的翻译工作，无论是为了学术研究、商务沟通还是日常交流，都需要一个准确、高效的中英互译工具。用户提出这个问题的原因可能是为了提高翻译效率，确保翻译的准确性，或者是在寻找一个可靠的翻译助手。

### Attention:
您对中英互译的需求非常重要，准确的翻译不仅能提升沟通效率，还能确保信息的准确传达。让我们一起努力，确保您的翻译工作既高效又准确！

### Profile:
我提出这个问题是因为我需要一个可靠的中英互译工具，帮助我处理日常的翻译任务，无论是学术论文、商务文件还是日常对话。

### Skills:
- 精通中英文语言
- 熟悉中英文语法和词汇
- 具备翻译理论和实践经验
- 能够识别和处理翻译中的文化差异
- 熟练使用翻译工具和资源

### Goals:
1. 提供准确的中英互译服务
2. 确保翻译的流畅性和自然性
3. 处理复杂的翻译任务，如专业术语和长句
4. 提供翻译建议和改进意见
5. 帮助用户理解和处理翻译中的文化差异

### Constrains:
- 确保翻译的准确性和专业性
- 尊重原文的意思和风格
- 避免使用机器翻译的生硬表达
- 提供有针对性的翻译建议

### OutputFormat:
译文：[译文内容]

### Workflow:
1. **接收原文**：获取用户提供的中文或英文原文。
2. **分析原文**：仔细阅读原文，理解其内容、语境和意图。
3. **翻译**：根据原文内容进行准确翻译，确保译文的流畅性和自然性。

### Suggestions:
1. 提供需要翻译的原文内容。
2. 说明翻译的具体需求，如是否需要保留原文的风格或语气。
3. 提供相关的背景信息，帮助理解原文的语境。

### Examples:
译文：China is a country with a long history and rich culture.

请翻译:

"""

messages = [
    {
        "role": "user",
        "content": prompt,
    },
    {
        "role": "assistant",
        "content": "欢迎使用中英互译专家，如果你有任何的关于中英互译的需求，无论是学术论文、商务文件还是日常对话，请输入需要翻译的内容。",
    },
    {"role": "user", "content": "今天天气真好。"},
    {
        "role": "assistant",
        "content": "译文：It's a beautiful day.",
    },
]


class AiTranslationHandler(QueryHandlerAbstract):

    @property
    def ai_name(self):
        return "AI"

    def is_available(self, query: str) -> bool:
        if query:
            return True
        return False

    def get_ai_message(self, query: str) -> str:
        return ""

    def get_original_text(self, content: str) -> str:
        pattern = r"原文：\n*(.+)\n{0,1}"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0]
        return ""

    def get_translation_text(self, content: str) -> str:
        pattern = r"译文：\n*(.+)\n{0,1}"
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            return matches[0]
        return ""

    def get_result(self, query: str) -> dict:
        items = []
        content = self.get_ai_message(query)
        # translation_text = self.get_translation_text(content)
        translation_text = self.get_translation_text(content)
        if translation_text:
            items.append(
                {
                    "arg": translation_text,
                    "title": translation_text,
                    "subtitle": f"由 {self.ai_name} 翻译: {query}",
                    "icon": "",
                }
            )
        result = {"items": items}
        return result


class OllamaTranslationHandler(AiTranslationHandler):
    """通过 Ollama 翻译"""

    @property
    def ai_name(self):
        return "Ollama"

    def get_ai_message(self, query):
        _messages = [
            {
                "role": "user",
                "content": prompt + query,
            },
        ]
        # _messages = messages[:]
        # _messages.append({"role": "user", "content": query})
        ai_message = get_ollama_message(_messages)
        return ai_message.content


class DeepseekTranslationHandler(AiTranslationHandler):
    """通过 Deepseek 翻译"""

    @property
    def ai_name(self):
        return "Deepseek"

    def get_ai_message(self, query):
        # _messages = messages[:]
        # _messages.append({"role": "user", "content": query})
        _messages = [
            {
                "role": "user",
                "content": prompt + query,
            },
        ]
        ai_message = get_deepseek_message(_messages)
        return ai_message.content


def main():
    thread_base = QueryThreadBase()
    thread_base.add_handler(OllamaTranslationHandler())
    thread_base.add_handler(DeepseekTranslationHandler())

    thread_base.main()


if __name__ == "__main__":
    main()
