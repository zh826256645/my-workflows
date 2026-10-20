#!/Users/zhonghao/Projects/my-workflows/.venv/bin/python
"""
测试翻译 & 词典功能
"""

import sys
from os.path import abspath, dirname, join

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

from ai.translation import (
    DeepseekTranslationHandler,
    is_dictionary_query,
)

TEST_CASES = [
    ("apple", "英文名词（多例句）"),
    ("goal", "英文名词（多例句）"),
    ("run", "英文动词（多例句）"),
    ("I went to the store yesterday", "英文句子 → 中文（翻译模式 - 单条）"),
]


def test_handler(handler, name):
    print(f"\n{'=' * 60}")
    print(f"  Handler: {name}")
    print(f"{'=' * 60}")

    for query, description in TEST_CASES:
        is_word = is_dictionary_query(query)
        mode = "词典" if is_word else "翻译"
        print(f"\n--- [{mode}] {description} ---")
        print(f"  输入: {query}")

        try:
            result = handler.get_result(query)
            items = result.get("items", [])
            print(f"  items 数量: {len(items)}")

            example_count = 0
            for i, item in enumerate(items):
                subtitle = item["subtitle"]
                if "例句" in subtitle:
                    example_count += 1
                    print(f"  [{i}] [例句] {item['title'][:80]}")
                else:
                    short_sub = subtitle.split(";")[0] if ";" in subtitle else subtitle
                    print(f"  [{i}] [{short_sub[:20]}] {item['title'][:60]}")

            print(f"  例句条数: {example_count}")

        except Exception as e:
            print(f"  [ERROR] {e}")


def main():
    print("=" * 60)
    print("  翻译/词典 功能测试")
    print("=" * 60)

    test_handler(DeepseekTranslationHandler(), "Deepseek")


if __name__ == "__main__":
    main()
