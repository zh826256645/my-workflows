#!/usr/bin/python3
"""
查询我的书签
"""
import re

import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class MyBookmarksQueryHandler(QueryHandlerAbstract):
    """查询我的书签"""

    def __init__(self) -> None:
        super().__init__()

        self.bookmarks = self.config.MY_BOOKMARKS

        self.name_url = self.get_name_url_mapping()

    def get_name_url_mapping(self):
        """获取名称和 URL 的映射"""
        name_url = dict()
        for site_name, title_urls in self.bookmarks.items():
            for title, url in title_urls:
                name_url[f'{site_name.lower()} {title.lower()}'] = url

        return name_url

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> bool:
        if not query:
            query = ''

        query = query.lower()
        query = f'.*{query.replace(" ", ".*")}.*'
        names = [name for name, _ in self.name_url.items()]
        match_names = [name for name in names if re.match(query, name)][:10]

        items = list()
        for name in match_names:
            items.append({
                'arg': self.name_url[name],
                'title': name,
                'subtitle': name,
                'icon': ''
            })

        result = {'items': items}
        return result


def main():
    my_info = QueryBase()
    handler = MyBookmarksQueryHandler()

    my_info.add_handler(handler)

    my_info.main()


if __name__ == '__main__':
    main()
