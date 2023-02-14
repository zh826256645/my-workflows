# -*- coding: utf-8 -*-
"""
基础类
"""
import sys
import json
from abc import ABCMeta, abstractmethod
from typing import List

try:
    import config
except ImportError:
    import default_config as config


class QueryHandlerAbstract(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.config = config

    @abstractmethod
    def is_available(self, query: str) -> bool:
        """
        校验 query 是否可用

        :param str query: 查询的数据
        :return bool: 是否可用
        """
        pass

    @abstractmethod
    def get_result(self, query: str) -> dict:
        """
        获取结果

        :param str query: 查询的数据
        :return dict: 结果
        """
        pass


class QueryBase:

    def __init__(self, default_result: dict = None,
                 query_handlers: List[QueryHandlerAbstract] = None):
        """
        初始化

        :param dict default_result: 默认输出
        :param List[QueryHandlerAbstract] query_handlers: 查询处理器列表
        """
        self.default_result = default_result
        self.query_handlers = query_handlers if query_handlers else []

    def add_handler(self, handler: QueryHandlerAbstract):
        """
        添加处理器

        :param QueryHandlerAbstract handler: 处理器
        """
        self.query_handlers.append(handler)

    def main(self):
        """
        入口方法
        """
        query = self.get_query()

        result = self.default_result or self.get_default_result()

        if query:
            for handler in self.query_handlers:
                if handler.is_available(query):
                    result = handler.get_result(query)
                    break

        if result:
            print(json.dumps(result))

    def get_query(self) -> str:
        """
        获取查询数据

        :return str: 查询数据
        """
        query = None
        if len(sys.argv) > 1:
            query = sys.argv[1].strip()
        return query

    def get_default_result(self) -> dict:
        """
        获取默认数据

        :return dict: 默认返回数据
        """
        return dict()
