# -*- coding: utf-8 -*-
"""
多线程基类
"""
import json
import concurrent.futures

from public.base import QueryBase


class QueryThreadBase(QueryBase):
    def __init__(self, default_result=None, query_handlers=None):
        super().__init__(default_result, query_handlers)

        self.max_workers = 10

    def main(self):
        query = self.get_query()

        result = self.default_result or self.get_default_result()

        if query:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers
            ) as executor:
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
