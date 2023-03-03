#!/usr/local/bin/python3
"""
时间处理工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

import time
import datetime

from bson.objectid import ObjectId

from public.base import QueryHandlerAbstract
from public.base import QueryBase


Second = int


class TimeQueryHandlerAbstract(QueryHandlerAbstract):
    """
    时间查询处理器
    """

    def __init__(self) -> None:
        super().__init__()

        self.NAME_FORMAT = {
            "完整": "%Y-%m-%d %H:%M:%S",
            "中文": "%Y年%m月%d日 %H时%M分%S秒",
            "日期": "%Y-%m-%d",
            "时间": "%H:%M:%S",
        }

        self.WEEK_NAMES = ["一", "二", "三", "四", "五", "六", "天"]

    def get_timestamp_result(self, timestamp: Second) -> list:
        """
        获取时间戳的结果

        :param Second timestamp: 时间戳
        :return list: 结果
        """
        items = list()
        for name, _format in self.NAME_FORMAT.items():
            format_time = time.strftime(_format, time.localtime(timestamp))
            item = {"arg": format_time, "title": format_time, "subtitle": name, "icon": ""}
            items.append(item)

        date = datetime.datetime.fromtimestamp(timestamp)
        week_name = f"星期{self.WEEK_NAMES[date.weekday()]}"
        items.append({"arg": week_name, "title": week_name, "subtitle": "星期", "icon": ""})

        month_name = f"{date.month}月"
        items.append({"arg": month_name, "title": month_name, "subtitle": "月份", "icon": ""})

        return items

    def get_other_result(self, timestamp: Second) -> list:
        """
        获取格式化时间的结果

        :param Second timestamp: 时间戳
        :return list: 结果
        """
        items = list()
        items.append({"arg": timestamp, "title": timestamp, "subtitle": "时间戳", "icon": ""})
        return items

    def build_result(self, items: list) -> dict:
        """
        构建结果

        :param list items: 数据列表
        :return dict: 结果
        """
        return {"items": items}

    def format_time_to_timestamp(self, format_time: str) -> Second:
        """
        格式化时间转时间戳

        :param str format_time: 格式化时间
        :return Second: 时间戳
        """
        _format = None
        if "-" in format_time and ":" in format_time:
            _format = self.NAME_FORMAT["完整"]
        elif "-" in format_time:
            _format = self.NAME_FORMAT["日期"]
        elif ":" in format_time:
            _format = self.NAME_FORMAT["时间"]

        timestamp = None
        if _format:
            timestamp = time.mktime(time.strptime(format_time, _format))

        return timestamp


class TimestampQueryHandler(TimeQueryHandlerAbstract):
    """
    处理时间戳的处理器
    """

    def is_available(self, query) -> bool:
        """
        判断是否是时间戳

        :param str query: 查询数据
        :return bool: 是否是时间戳
        """
        if query.isdigit() and len(query) in [10, 13]:
            return True
        return False

    def get_result(self, query: str):
        timestamp = int(query[:10])
        items = self.get_timestamp_result(timestamp)
        result = self.build_result(items)
        return result


class FormatTimeQueryHandler(TimeQueryHandlerAbstract):
    """
    处理格式化时间的处理器
    """

    def is_available(self, query: str) -> bool:
        """
        判断是否是格式化时间

        :param str query: 查询数据
        :return bool: 是否是格式化时间
        """
        if "-" in query or ":" in query:
            return True
        return False

    def get_result(self, query: str) -> dict:
        format_time = query.strip()
        timestamp = self.format_time_to_timestamp(format_time)

        items = self.get_other_result(timestamp)
        _items = self.get_timestamp_result(timestamp)
        items.extend(_items)

        result = self.build_result(items)
        return result


class ObjectIdQueryHandler(TimeQueryHandlerAbstract):
    """
    处理 ObjectId 的处理器
    """

    def is_available(self, query: str) -> bool:
        """
        判断是否是 ObjectId

        :param str query: 查询数据
        :return bool: 是否是 ObjectId
        """
        if len(query) == 24:
            return True
        return False

    def get_result(self, query: str) -> dict:
        object_id = ObjectId(query)
        timestamp = object_id.generation_time.timestamp()

        items = self.get_other_result(timestamp)
        _items = self.get_timestamp_result(timestamp)
        items.extend(_items)

        result = self.build_result(items)
        return result


class DateNameQueryHandler(TimeQueryHandlerAbstract):
    """
    处理昨天、今天的处理器
    """

    def __init__(self) -> None:
        super().__init__()

        self.name_format_time = {
            "今天": lambda: time.strftime("%Y-%m-%d"),
            "明天": lambda: time.strftime("%Y-%m-%d", time.localtime(int(time.time()) + 86400)),
            "昨天": lambda: time.strftime("%Y-%m-%d", time.localtime(int(time.time()) - 86400)),
            "这周": lambda: time.strftime(
                "%Y-%m-%d", time.localtime(int(time.time()) - datetime.datetime.now().weekday() * 86400)
            ),
            "这个月": lambda: time.strftime("%Y-%m-01"),
        }

    def is_available(self, query: str) -> bool:
        """
        判断是符合

        :param str query: 查询数据
        :return bool: 是否是 ObjectId
        """
        if query in self.name_format_time.keys():
            return True
        return False

    def get_result(self, query: str) -> dict:
        format_time = self.name_format_time[query]()
        timestamp = self.format_time_to_timestamp(format_time)

        items = self.get_other_result(timestamp)
        _items = self.get_timestamp_result(timestamp)
        items.extend(_items)

        result = self.build_result(items)
        return result


def main():
    time_tools = QueryBase()
    time_tools.add_handler(TimestampQueryHandler())
    time_tools.add_handler(FormatTimeQueryHandler())
    time_tools.add_handler(ObjectIdQueryHandler())
    time_tools.add_handler(DateNameQueryHandler())

    time_tools.main()


if __name__ == "__main__":
    main()
