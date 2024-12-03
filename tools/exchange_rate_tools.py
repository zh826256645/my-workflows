#!/usr/local/bin/python3.10
"""
汇率转换工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

import time
from typing import Tuple

import requests

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class ExchRateHandler(QueryHandlerAbstract):
    """汇率转换处理器"""

    def __init__(self) -> None:
        super().__init__()

        self.NAME_ISO = {
            "人民币": "CNY",
            "美元": "USD",
            "日元": "JPY",
            "港元": "HKD",
            "新台币": "TWD",
            "澳元": "MOP",
            "欧元": "EUR",
            "英镑": "GBP",
            "韩元": "KRW",
            # '克朗': 'DKK',
            # '格里夫纳': 'UAH',
            # '先令': 'UGX',
            # '比索': 'UYI',
            # '新谢克尔': 'ILS',
            "卢布": "RUB",
            "卢比": "INR",
            "瑞郎": "CHF",
            # '瓦图': 'VUV',
            "新西兰元": "NZD",
            "缅币": "MMK",
            "越南盾": "VND",
            "泰铢": "THB",
            "加元": "CAD",
        }

        self.num_method = {
            0: self.get_name_iso_info,
            1: self.get_name_iso_info,
            2: self.get_currency_exchange,
            3: self.get_currency_exchange,
        }

    def query_parse(self, query: str) -> Tuple:
        params = tuple()
        names = list(self.NAME_ISO.keys())
        if query:
            data = query.split(" ")
            if len(data) == 1 and data[0] in names:
                params = tuple(data)

            elif 1 < len(data) <= 3:
                currencies = list()
                amount = 0
                for item in data:
                    if item.replace(".", "").isdigit():
                        amount = item
                    elif item in names:
                        currencies.append(item)
                if currencies and amount:
                    _params = currencies
                    _params.append(amount)
                    params = tuple(_params)
        return params

    def is_available(self, query: str) -> bool:
        return True

    def get_result(self, query: str) -> dict:
        params_num = len(self.query_parse(query))
        method = self.num_method.get(params_num)

        items = method(query)
        return {"items": items}

    def get_name_iso_info(self, query: str = None):
        items = list()
        for name, iso in self.NAME_ISO.items():
            if query and query != name:
                continue

            items.append({"arg": iso, "title": iso, "subtitle": name, "icon": ""})

        return items

    def get_currency_exchange(self, query: str) -> list():
        """汇率转换"""
        params = self.query_parse(query)
        currency = params[0]
        to_currency = None
        amount = 0
        if len(params) == 3:
            to_currency = params[1]
            amount = params[2]
        else:
            amount = params[1]
        amount = float(amount)

        items = list()
        currency_rate = self.get_currency_rate(self.NAME_ISO[currency])
        if currency_rate:
            for name, iso in self.NAME_ISO.items():
                if currency == name or (to_currency and to_currency != name):
                    continue

                items.append(
                    {
                        "arg": round(currency_rate[iso] * amount, 2),
                        "title": f"{currency} {amount} = {name} {round(currency_rate[iso] * amount, 2)}",
                        "subtitle": name,
                        "icon": "",
                    }
                )

        return items

    def get_currency_rate(self, iso: str) -> dict():
        """获取货币转换数据"""
        url = f"https://api.apilayer.com/currency_data/historical?date={time.strftime('%Y-%m-%d')}&source={iso}"
        headers = {"apikey": "eBFDMeTnmcDRQD5Zzc51iXlqO79Oa7Mh"}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") is True and data.get("quotes"):
                return {
                    name.replace(iso, ""): rate for name, rate in data["quotes"].items()
                }
        return None


def main():
    exchange_rate_tools = QueryBase()
    exch_rate_handler = ExchRateHandler()

    exchange_rate_tools.add_handler(exch_rate_handler)
    exchange_rate_tools.default_result = exch_rate_handler.get_result("")

    exchange_rate_tools.main()


if __name__ == "__main__":
    main()
