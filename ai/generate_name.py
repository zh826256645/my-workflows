#!/usr/local/bin/python3.10
"""
让 AI 生成变量名
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

import re
import json
import concurrent.futures

from case_convert import camel_case, snake_case

from public.base import QueryBase
from public.base import QueryHandlerAbstract
from ai.utils import get_ollama_message, get_deepseek_message

prompt = """### Role: 资深软件开发专家

### Background:
用户希望 AI 能够根据用户输入的内容自动生成合适的变量名和函数名。这通常发生在编码过程中，开发者需要为新创建的变量或函数命名，但有时难以找到既符合语义又简洁明了的名称。通过 AI 的帮助，可以提高命名的一致性和可读性，减少开发者在命名上的时间消耗。

### Attention:
命名是编程中至关重要的一环，一个好的命名不仅能提高代码的可读性，还能减少后续维护的难度。让我们一起利用 AI 的力量，为您的代码生成清晰、简洁且语义明确的变量名和函数名吧！

### Profile:
我是一名资深软件开发专家，拥有丰富的编程经验和命名规范知识。我了解各种编程语言的命名习惯，并能根据上下文生成合适的名称。

### Skills:
- **命名规范知识**：熟悉多种编程语言的命名规范，如驼峰命名法、下划线命名法等。
- **语义分析**：能够分析用户输入的内容，提取关键信息，生成符合语义的名称。
- **上下文理解**：能够根据代码的上下文生成一致的命名。
- **复数命名**：如果使用的单词有复数形式，请优先使用复数形式，例如 items、products。

### Goals:
1. 分析用户输入的内容。
2. 生成符合语义的变量名。
3. 生成符合语义的函数名。
4. 确保生成的名称符合编程语言的命名规范。

### Constraints:
- 生成的名称必须简洁明了。
- 生成的名称必须符合语义。
- 生成的名称必须符合编程语言的命名规范。
- 不要返回多余的解释说明

### OutputFormat:
```
变量名: <生成的变量名>
函数名: <生成的函数名>
```

### Workflow:
1. **分析用户输入**：仔细阅读用户输入的内容，提取关键信息。
2. **确定命名规范**：根据用户使用的编程语言，确定合适的命名规范（如驼峰命名法、下划线命名法等）。
3. **生成变量名**：根据提取的关键信息，生成符合语义的变量名。
4. **生成函数名**：根据提取的关键信息，生成符合语义的函数名。
5. **输出结果**：按照预定的格式输出生成的变量名和函数名。

### Suggestions:
- 提供尽可能详细的上下文信息，以便生成更准确的名称。
- 如果使用特定的编程语言，请告知，以便遵循相应的命名规范。

### Examples:
**用户输入**: "计算两个数的和"
```
变量名: sumOfTwoNumbers
函数名: calculateSum
```

### Initialization:
欢迎使用资深软件开发专家，如果你有任何的关于生成变量名和函数名的问题，无论是命名规范还是语义分析，请告诉我你的需求吧！"""

messages = [
    {
        "role": "user",
        "content": prompt,
    },
    {
        "role": "assistant",
        "content": "你好，我是 资深代码命名专家，资深软件开发专家技能简介：擅长根据用户输入内容自动生成符合语义且简洁明了的变量名和函数名。熟悉多种编程语言的命名习惯，并能根据上下文生成一致的名称，确保名称符合规范。，让我们开始对话吧！",
    },
    {"role": "user", "content": "获取商品列表"},
    {
        "role": "assistant",
        "content": "```变量名: products\n函数名: get_products```",
    },
]


class AiGeneratedHandler(QueryHandlerAbstract):

    @property
    def ai_name(self):
        return "AI"

    def is_available(self, query: str) -> bool:
        if query:
            return True
        return False

    def get_var_name_and_func_name(self, content: str) -> tuple[str, str]:
        variable_pattern = r"变量名:\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        variable_matches = re.findall(variable_pattern, content)

        # 匹配函数名（包含下划线）
        function_pattern = r"函数名:\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        function_matches = re.findall(function_pattern, content)

        var_name, func_name = "", ""
        if variable_matches:
            var_name = variable_matches[0]
        if function_matches:
            func_name = function_matches[0]

        return var_name, func_name

    def get_ai_message(self, query: str) -> str:
        return ""

    def get_result(self, query: str) -> dict:
        items = []
        content = self.get_ai_message(query)
        var_name, func_name = self.get_var_name_and_func_name(content)
        name_func = {"下划线": snake_case, "小驼峰": camel_case}
        for name, func in name_func.items():
            if var_name:
                items.append(
                    {
                        "arg": func(var_name),
                        "title": f"{name}: {func(var_name)}",
                        "subtitle": f"{self.ai_name} 变量名",
                        "icon": "",
                    }
                )
            if func_name:
                items.append(
                    {
                        "arg": func(func_name),
                        "title": f"{name}: {func(func_name)}",
                        "subtitle": f"{self.ai_name} 函数名",
                        "icon": "",
                    }
                )

        result = {"items": items}
        return result


class OllamaGeneratedHandler(AiGeneratedHandler):
    """通过 Ollama 生成变量名"""

    @property
    def ai_name(self):
        return "Ollama"

    def get_ai_message(self, query):
        _messages = messages[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_ollama_message(_messages)
        return ai_message.content


class DeepseekGeneratedHandler(AiGeneratedHandler):
    """通过 Deepseek 生成变量名"""

    @property
    def ai_name(self):
        return "Deepseek"

    def get_ai_message(self, query):
        _messages = messages[:]
        _messages.append({"role": "user", "content": query})
        ai_message = get_deepseek_message(_messages)
        return ai_message.content


class GenerateQuery(QueryBase):

    def main(self):
        query = self.get_query()

        result = self.default_result or self.get_default_result()

        if query:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                todo_list = []
                for handler in self.query_handlers:
                    if handler.is_available(query):
                        future = executor.submit(handler.get_result, query)
                        todo_list.append(future)

                for future in concurrent.futures.as_completed(todo_list):  # 并发执行
                    if not result.get("items"):
                        result["items"] = []
                    if items := future.result().get("items"):
                        result["items"].extend(items)

        if result:
            print(json.dumps(result))


def main():
    generate_query = GenerateQuery()
    generate_query.add_handler(OllamaGeneratedHandler())
    generate_query.add_handler(DeepseekGeneratedHandler())

    generate_query.main()


if __name__ == "__main__":
    main()
