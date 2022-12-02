#!/usr/local/bin/python3
"""
查询我的信息
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class MyInfoQueryHandler(QueryHandlerAbstract):
    """
    我的信息查询处理器
    """
    def __init__(self) -> None:
        super().__init__()

        self.info = self.config.MY_INFO

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        if not query:
            query = ''
        query = query.lower()

        keys = [key for key in self.info.keys() if query in key]
        items = list()
        for key in keys:
            items.append({
                'arg': self.info[key],
                'title': self.info[key],
                'subtitle': key,
                'icon': ''
            })

        result = {'items': items}
        return result


def main():
    my_info = QueryBase()
    handler = MyInfoQueryHandler()

    my_info.add_handler(handler)
    my_info.default_result = handler.get_result('')

    my_info.main()


if __name__ == '__main__':
    main()
