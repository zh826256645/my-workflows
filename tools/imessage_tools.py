#!/Users/zhonghao/miniconda3/bin/python3
"""
iMessages 工具
"""
import re
import sqlite3
import sys
from os.path import abspath, dirname, join

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))


from public.base import QueryBase, QueryHandlerAbstract


class IMessageHandler(QueryHandlerAbstract):
    """信息处理工具"""

    def __init__(self) -> None:
        super().__init__()

        self.handle_methods = [
            self.get_recent_verification_code,
        ]

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        items = list()
        for handle_method in self.handle_methods:
            items.append(handle_method(query))

        return {"items": items}

    def get_recent_verification_code(self, query: str) -> dict:
        """获取最近的验证码

        :param str query: 查询
        :return dict: 结果
        """
        con = sqlite3.connect(self.config.IMESSAGE_DP_PATH)
        cur = con.cursor()
        res = cur.execute(
            'SELECT text FROM message WHERE datetime(date/1000000000 + 978307200,"unixepoch","localtime") > datetime("now","localtime","-120 second") ORDER BY date DESC LIMIT 1;'
        )
        title = res.fetchone()
        if title and "验证码" in title[0]:
            result = re.search("\d{4,6}", title[0])
            if result:
                return {
                    "arg": result.group(),
                    "title": result.group(),
                    "subtitle": title[0],
                    "icon": "",
                }

        return {
            "arg": "无",
            "title": "无",
            "subtitle": "未获取到 2 分钟内的验证码",
            "icon": "",
        }


def main():
    string_tools = QueryBase()
    handler = IMessageHandler()

    string_tools.add_handler(handler)
    string_tools.default_result = handler.get_result("")

    string_tools.main()


if __name__ == "__main__":
    main()
