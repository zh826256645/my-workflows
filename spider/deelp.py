# -*- coding: utf-8 -*-
"""
Deelp 爬虫

https://www.deepl.com/
"""
import time

import requests


class DeelpSpider:

    target_lang_mapping = {
        'ZH': 'EN',
        'EN': 'ZH'
    }

    @staticmethod
    def get_headers():
        return {
            'authority': 'www2.deepl.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'cookie': 'dapUid=55cf2ce0-d8d8-42ad-8b91-4cfffbcc6762; privacySettings=%7B%22v%22%3A%221%22%2C%22t%22%3A1'
                      '657238400%2C%22m%22%3A%22LAX%22%2C%22consent%22%3A%5B%22NECESSARY%22%2C%22PERFORMANCE%22%2C%22C'
                      'OMFORT%22%5D%7D; LMTBID=v2|ab59ff5b-3dca-4a58-bf7b-2a2ef76a6584|418a98a4a521797e96070f61b8af9d0'
                      'c; dl_session=fa.64803f5d-a8c3-4dd7-9044-f60d31404424; dapVn=5; __cf_bm=5AQCEHdkyVp0VVMYv.MBHDA'
                      'VSNMVRlUmESXyHFKVjd0-1658282844-0-AXi79toXRbIAxThJwd0MBkEe5ouOJPfsmkwgZmO3F5Kq/fzqeigv0TG7qV0gi'
                      'K333/13WbX6HDhqiu9l854l9dc=; dapSid=%7B%22sid%22%3A%2224600300-32c9-4fe1-b527-a8313c95b8ea%22%2'
                      'C%22lastUpdate%22%3A1658283110%7D',
            'dnt': '1',
            'origin': 'https://www.deepl.com',
            'pragma': 'no-cache',
            'referer': 'https://www.deepl.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.0.0 Safari/537.36'
        }

    @staticmethod
    def translation_text(text: str, target_lang: str = None) -> dict:
        """翻译文本

        :param str text: 文本
        :return dict: 翻译结果
        """
        url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'

        if not target_lang:
            result = DeelpSpider.identify_text_lang(text)
            if result:
                text_lang = result['result']['lang']['detected']
                target_lang = DeelpSpider.target_lang_mapping.get(text_lang.upper()) or 'ZH'
            else:
                target_lang = 'ZH'

        data = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": DeelpSpider.handle_text_params(text),
                "lang": {
                    "preference": {
                        "weight": {
                            "DE": 0.33359,
                            "EN": 4.06419,
                            "ES": 0.20378,
                            "FR": 0.23443,
                            "IT": 0.16712,
                            "JA": 3.17509,
                            "NL": 0.23246,
                            "PL": 0.14714,
                            "PT": 0.15479,
                            "RU": 0.12624,
                            "ZH": 3.44308,
                            "SV": 0.25651,
                            "BG": 0.08955,
                            "CS": 0.15482,
                            "DA": 0.17385,
                            "EL": 0.08261,
                            "ET": 0.11885,
                            "FI": 0.12425,
                            "HU": 0.1148,
                            "LV": 0.08127,
                            "LT": 0.10038,
                            "RO": 0.10911,
                            "SK": 0.1355,
                            "SL": 0.10668,
                            "ID": 0.11985,
                            "TR": 0.11206
                        },
                        "default": "default"},
                    "source_lang_user_selected": "auto",
                    "target_lang": target_lang},
                "priority": -1,
                "commonJobParams": {
                    "browserType": 1,
                    "formality":  None},
                "timestamp": int(time.time() * 1000)
            },
            "id": 5510002
        }
        response = requests.post(url=url, json=data, headers=DeelpSpider.get_headers())
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def identify_text_lang(text: str) -> dict:
        """识别文本的语言

        :param str text: 文本
        :return dict: 识别结果
        """
        url = 'https://www2.deepl.com/jsonrpc?method=LMT_split_text'
        data = {
            "jsonrpc": "2.0",
            "method": "LMT_split_text",
            "params": {
                "texts": text.split('\n'),
                "lang": {
                    "preference": {
                        "weight": {
                            "DE": 0.33359,
                            "EN": 4.06419,
                            "ES": 0.20378,
                            "FR": 0.23443,
                            "IT": 0.16712,
                            "JA": 3.17509,
                            "NL": 0.23246,
                            "PL": 0.14714,
                            "PT": 0.15479,
                            "RU": 0.12624,
                            "ZH": 3.44308,
                            "SV": 0.25651,
                            "BG": 0.08955,
                            "CS": 0.15482,
                            "DA": 0.17385,
                            "EL": 0.08261,
                            "ET": 0.11885,
                            "FI": 0.12425,
                            "HU": 0.1148,
                            "LV": 0.08127,
                            "LT": 0.10038,
                            "RO": 0.10911,
                            "SK": 0.1355,
                            "SL": 0.10668,
                            "ID": 0.11985,
                            "TR": 0.11206
                        },
                        "default": "default"
                    },
                    "lang_user_selected": "auto"
                },
            },
            "id": 5510001
        }
        response = requests.post(url=url, json=data, headers=DeelpSpider.get_headers())
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def handle_text_params(text: str) -> list:
        """处理文本参数

        :param str text: 文本
        :return list: 文本参数列表
        """
        params = list()
        lines = text.split('\n')
        length = len(lines)
        for index, line in enumerate(lines):
            params.append({
                'kind': 'default',
                "sentences": [{"text": line, "id": index, "prefix": ""}],
                'preferred_num_beams': 4,
                'raw_en_context_after': [] if index + 1 >= length else [lines[index + 1]],
                'raw_en_context_before': [] if index == 0 else [lines[index - 1]],
                'quality': 'fast'
            })
        return params


def main():
    text = """Hello, World"""
    result = DeelpSpider.translation_text(text)
    print(result)


if __name__ == '__main__':
    main()
