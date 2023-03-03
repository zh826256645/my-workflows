#!/usr/local/bin/python3
"""
字符串工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

import base64
import hashlib

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class StringHandler(QueryHandlerAbstract):
    """字符串处理"""

    def __init__(self) -> None:
        super().__init__()

        self.handle_methods = [self.get_len_result, self.get_base64_result, self.get_md5_result]

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        items = list()
        for handle_method in self.handle_methods:
            items.append(handle_method(query))

        return {"items": items}

    def get_len_result(self, query: str) -> dict:
        """获取长度结果

        :param str query: 查询
        :return dict: 结果
        """
        length = len(query)
        return {"arg": length, "title": length, "subtitle": "字符串长度", "icon": ""}

    def get_base64_result(self, query: str) -> dict:
        """获取 base64 结果

        :param str query: 查询
        :return dict: 结果
        """
        _str = None
        _type = None
        try:
            _str = base64.decodebytes(query.encode()).decode()
            _type = "解码"
        except Exception:
            _str = base64.b64encode(query.encode()).decode("ascii")
            _type = "编码"

        return {"arg": _str, "title": _str, "subtitle": f"base64 {_type}", "icon": ""}

    def get_md5_result(self, query: str) -> dict:
        """获取 md5 结果

        :param str query: 查询
        :return dict: 结果
        """
        md5_str = hashlib.md5(query.encode(encoding="UTF-8")).hexdigest()
        return {"arg": md5_str, "title": md5_str, "subtitle": "md5 编码", "icon": ""}


def main():
    string_tools = QueryBase()
    string_tools.add_handler(StringHandler())

    string_tools.main()


if __name__ == "__main__":
    main()
