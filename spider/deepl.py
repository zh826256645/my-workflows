# -*- coding: utf-8 -*-
"""
Deelp 爬虫

https://www.deepl.com/
"""
import time
import random

import requests


class DeeplSpider:

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
            'cookie': '__cf_bm=vz7mTCZkAPqijnnb7IxV0k3J_wctidy.v1hY4hEcriw-1658807845-0-AfpvDupXav+zfihOQO53ul2wzpHcVXp35P55FMLpOyZkh2G7Dvs8jfAerOlyZcOiuIDLXT9AEka8I3fvuTNYmRY=; dapUid=f4d4e142-6994-452f-b561-d6cacb09681c; dapVn=1; LMTBID=v2|ec1d77a9-7b01-4577-b757-5d9bcf304f68|99e75b03854d8851a4fada362a8e8cbe; privacySettings=%7B%22v%22%3A%221%22%2C%22t%22%3A1658793600%2C%22m%22%3A%22LAX%22%2C%22consent%22%3A%5B%22NECESSARY%22%2C%22PERFORMANCE%22%2C%22COMFORT%22%5D%7D; dl_clearance=A_d7bmohbEAyL16neLPE--PbZWxhFwSwUyFBRLu1WAm_lzH0t4jw-FddO9EjFOuRIEbWm44vCZdhiYgaMw9n4Sc_O14WtYO50BnwreEZmK_9yAk; dl_session=fa.60d5ca02-76f4-a9fc-c7da-b8a2d8d62d8f; dapSid=%7B%22sid%22%3A%22d2d2d893-5d86-49d8-9dd5-4ecf58d7a53e%22%2C%22lastUpdate%22%3A1658807910%7D',
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
    def translation_text(text: str, target_lang: str = None, prox_setting: dict = None) -> dict:
        """翻译文本

        :param str text: 文本
        :param str target_lang: 目标语言
        :param dict prox_setting: 代理设置
        :return dict: 翻译结果
        """
        url = 'https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs'

        if not target_lang:
            result = DeeplSpider.identify_text_lang(text, prox_setting)
            if result:
                text_lang = result['result']['lang']['detected']
                target_lang = DeeplSpider.target_lang_mapping.get(text_lang.upper()) or 'ZH'
            else:
                target_lang = 'ZH'

        data = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": DeeplSpider.handle_text_params(text),
                "lang": {
                    "preference": {
                        "weight": {
                            'BG': 0.11069,
                            'CS': 0.2744,
                            'DA': 0.29623,
                            'DE': 0.4921,
                            'EL': 0.09788,
                            'EN': 3.75038,
                            'ES': 0.44803,
                            'ET': 0.25512,
                            'FI': 0.26772,
                            'FR': 0.31568,
                            'HU': 0.19951,
                            'ID': 0.25246,
                            'IT': 0.68214,
                            'JA': 1.79913,
                            'LT': 0.15493,
                            'LV': 0.15615,
                            'NL': 0.50608,
                            'PL': 0.58794,
                            'PT': 0.23738,
                            'RO': 0.16467,
                            'RU': 0.14666,
                            'SK': 0.2716,
                            'SL': 0.1598,
                            'SV': 0.30723,
                            'TR': 0.17896,
                            'ZH': 8.53534,
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
            "id": random.randint(30000000, 99999999)
        }
        response = requests.post(
            url=url,
            json=data,
            headers=DeeplSpider.get_headers(),
            proxies=prox_setting)
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def identify_text_lang(text: str, prox_setting: dict = None) -> dict:
        """识别文本的语言

        :param str text: 文本
        :param dict proxy_setting: 代理设置
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
                            'BG': 0.11069,
                            'CS': 0.2744,
                            'DA': 0.29623,
                            'DE': 0.4921,
                            'EL': 0.09788,
                            'EN': 3.75038,
                            'ES': 0.44803,
                            'ET': 0.25512,
                            'FI': 0.26772,
                            'FR': 0.31568,
                            'HU': 0.19951,
                            'ID': 0.25246,
                            'IT': 0.68214,
                            'JA': 1.79913,
                            'LT': 0.15493,
                            'LV': 0.15615,
                            'NL': 0.50608,
                            'PL': 0.58794,
                            'PT': 0.23738,
                            'RO': 0.16467,
                            'RU': 0.14666,
                            'SK': 0.2716,
                            'SL': 0.1598,
                            'SV': 0.30723,
                            'TR': 0.17896,
                            'ZH': 8.53534,
                        },
                        "default": "default"
                    },
                    "lang_user_selected": "auto"
                },
            },
            "id": 55100022
        }
        response = requests.post(url=url, json=data, headers=DeeplSpider.get_headers())
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
    text = """Excuse me you work with the buffer man because you liked to saw me triple six lollipop"""
    result = DeeplSpider.translation_text(text)
    print(result)


if __name__ == '__main__':
    main()
