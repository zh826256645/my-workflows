#!/usr/local/bin/python3
"""
假数据生成工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), '../'))

from faker import Faker

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class FakerHandler(QueryHandlerAbstract):

    def __init__(self) -> None:
        super().__init__()

        self.faker = Faker(locale='zh_CN')
        self.MAX_NUM = 10

        self.query_method = {
            '姓名': self.get_name_faker,
            '电话': self.get_phone_faker,
            '邮箱': self.get_email_faker,
            '地址': self.get_street_faker,
            '公司': self.get_company_faker,
        }

    def is_available(self, query: str) -> bool:
        return True

    def get_name_faker(self, num: int = 10):
        items = list()
        for _ in range(num):
            value = self.faker.name()
            items.append({
                'arg': value,
                'title': value,
                'subtitle': '姓名',
                'icon': ''
            })
        return items

    def get_phone_faker(self, num: int = 10) -> dict:
        items = list()
        for _ in range(num):
            value = self.faker.phone_number()
            items.append({
                'arg': value,
                'title': value,
                'subtitle': '电话',
                'icon': ''
            })
        return items

    def get_company_faker(self, num: int = 10) -> dict:
        items = list()
        for _ in range(num):
            value = self.faker.company()
            items.append({
                'arg': value,
                'title': value,
                'subtitle': '公司',
                'icon': ''
            })
        return items

    def get_street_faker(self, num: int = 10) -> dict:
        items = list()
        for _ in range(num):
            value = self.faker.street_address()
            items.append({
                'arg': value,
                'title': value,
                'subtitle': '地址',
                'icon': ''
            })
        return items

    def get_email_faker(self, num: int = 10) -> dict:
        items = list()
        for _ in range(num):
            value = self.faker.free_email()
            items.append({
                'arg': value,
                'title': value,
                'subtitle': '邮箱',
                'icon': ''
            })
        return items

    def get_result(self, query: str) -> dict:
        methods = list()
        num = self.MAX_NUM
        if query != 'all':
            method = self.query_method.get(query)
            if method:
                methods.append(method)
        else:
            num = 1
            methods = self.query_method.values()

        items = list()
        for method in methods:
            items.extend(method(num))

        return {'items': items}


def main():
    Faker_tools = QueryBase()
    Faker_tools.add_handler(FakerHandler())

    Faker_tools.main()


if __name__ == '__main__':
    main()
