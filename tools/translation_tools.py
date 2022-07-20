#!/usr/local/bin/python3
"""
翻译工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from public.base import QueryHandlerAbstract
from public.base import QueryBase

from spider.deepl import DeeplSpider


class TranslationHandler(QueryHandlerAbstract):

    def __init__(self) -> None:
        super().__init__()

        self.language_lang = {
            '中文': 'ZH',
            '日文': 'JA',
            '英文': 'EN',
            '德语': 'DE',
            '西班牙语': 'ES',
        }

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        target_lang = None
        if query:
            for language in self.language_lang.keys():
                target_lang = self.language_lang.get(query[:len(language)])
                if target_lang:
                    query = query[len(language):]
                    query = query.strip()
                    break

        items = list()
        if query:
            result = DeeplSpider.translation_text(query, target_lang)
            if result:
                for index, beam in enumerate(result['result']['translations'][0]['beams']):
                    items.append({
                        'arg': beam['sentences'][0]['text'],
                        'title': beam['sentences'][0]['text'],
                        'subtitle': '翻译' if not index else '其他翻译',
                        'icon': ''
                    })
        return {'items': items}


def main():
    translation_tools = QueryBase()
    translation_tools.add_handler(TranslationHandler())

    translation_tools.main()


if __name__ == '__main__':
    main()
