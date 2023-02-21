#!/usr/local/bin/python3
"""
翻译工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from translatepy.translators import GoogleTranslate
from translatepy import Language
from translatepy.utils.request import Request

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class TranslationHandler(QueryHandlerAbstract):

    def __init__(self) -> None:
        super().__init__()

        self.language_lang = {
            '中文': 'ZH',
            '日文': 'JA',
            '日语': 'JA',
            '英文': 'EN',
            '德语': 'DE',
            '西班牙语': 'ES',
        }

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        target_lang = 'EN'
        if query:
            if not self.is_contains_chinese(query):
                target_lang = 'ZH'

            for language in self.language_lang.keys():
                _target_lang = self.language_lang.get(query[:len(language)])
                if _target_lang:
                    target_lang = _target_lang
                    query = query[len(language):]
                    query = query.strip()
                    break

        items = list()
        if query:
            PROXY_SETTING = self.config.PROXY_SETTING or dict()
            proxies = [value for _, value in PROXY_SETTING.items()]
            translator = GoogleTranslate(request=Request(proxy_urls=proxies))
            result = translator.translate(text=query, destination_language=Language(target_lang))

            if result.result:
                items.append({
                    'arg': result.result,
                    'title': result.result,
                    'subtitle': '翻译',
                    'icon': ''
                })

            if result.source_language:
                items.append({
                    'arg': str(result.source_language),
                    'title': f'{result.source_language.name} 翻译为 {result.destination_language.name}',
                    'subtitle': '语言',
                    'icon': ''
                })

            if result.service:
                items.append({
                    'arg': str(result.service),
                    'title': f'由 {result.service} 提供服务',
                    'subtitle': 'service',
                    'icon': ''
                })
        return {'items': items}

    def is_contains_chinese(self, strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False


def main():
    translation_tools = QueryBase()
    translation_tools.add_handler(TranslationHandler())

    translation_tools.main()


if __name__ == '__main__':
    main()
