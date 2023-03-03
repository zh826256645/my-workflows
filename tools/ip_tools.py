#!/usr/local/bin/python3
"""
ip 识别工具
"""
import sys
from os.path import abspath, join, dirname

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))

import requests

from public.base import QueryHandlerAbstract
from public.base import QueryBase


class IpInfo:
    def __init__(
        self,
        ip: str = None,
        country: str = None,
        region: str = None,
        city: str = None,
        district: str = None,
        isp: str = None,
        zip: str = None,
        zone: str = None,
    ) -> None:
        """
        IP 信息

        :param str ip: ip
        :param str country: 国家
        :param str region: 省份
        :param str city: 城市
        :param str district: 区
        :param str isp: 运营商
        :param str zip: 邮编
        :param str zone: 区号
        """
        self.ip = ip
        self.country = country
        self.region = region
        self.city = city
        self.district = district
        self.isp = isp
        self.zip = zip
        self.zone = zone

        self.key_name = {
            "ip": "ip",
            "country": "国家",
            "region": "省份",
            "city": "城市",
            "district": "区",
            "isp": "运营商",
            "zip": "邮编",
            "zone": "区号",
        }

    def get_items(self) -> list:
        items = list()
        for key, name in self.key_name.items():
            value = getattr(self, key)
            if value:
                items.append({"arg": value, "title": value, "subtitle": name, "icon": ""})
        return items


class IpQueryHandler(QueryHandlerAbstract):
    """处理 IP 的处理器"""

    def is_available(self, query: str) -> bool:
        if (query.count(".") == 3 and query[-1] != ".") or query == "my":
            return True
        return False

    def get_result(self, query: str) -> dict:
        if query == "my":
            query = None

        ip_info = self.get_ip_info_by_ip138(query)
        if ip_info:
            items = ip_info.get_items()
            if items:
                result = {"items": items}
                return result

    def get_ip_info_by_ip138(self, ip: str) -> IpInfo:
        """
        通过 ip138 查询 ip 信息

        :param str ip: ip
        :return IpInfo: ip 信息
        """
        url = f'https://api.ip138.com/ip/?datatype=json&token={self.config.IP_138["token"]}'
        if ip:
            url += f"&ip={ip}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result.get("ret") == "ok" and result.get("data"):
                if not ip:
                    ip = result["ip"]

                data = result["data"]
                ip_info = IpInfo(ip, *data)
                return ip_info
        return None


def main():
    ip_tools = QueryBase()
    handler = IpQueryHandler()

    ip_tools.add_handler(handler)

    ip_tools.main()


if __name__ == "__main__":
    main()
