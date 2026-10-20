#!/usr/bin/env -S uv run --frozen --quiet
"""
解析请求信息
"""

import json
import sys
from dataclasses import asdict, dataclass
from os.path import abspath, dirname, join

sys.path.insert(0, join(abspath(dirname(__file__)), "../"))


from public.base import QueryBase, QueryHandlerAbstract


@dataclass
class RequestInfo:
    url: str | None
    request_headers: dict | None
    response_headers: dict | None
    request_body: dict | None
    response_body: dict | str | None


KEY_NAME = {
    "url": "请求链接",
    "request_headers": "请求头",
    "response_headers": "返回头",
    "request_body": "请求数据",
    "response_body": "返回数据",
}


class ParseRequestInfoHandler(QueryHandlerAbstract):
    """处理 IP 的处理器"""

    def _find_and_decode_json(self, text: str) -> tuple[dict, str] | None:
        decoder = json.JSONDecoder()
        idx = text.find("{")
        while idx != -1:
            try:
                obj, end = decoder.raw_decode(text[idx:])
                return obj, text[idx + end :]
            except json.JSONDecodeError:
                idx = text.find("{", idx + 1)
        return None

    def is_available(self, query: str) -> bool:
        return self._find_and_decode_json(query) is not None

    def get_result(self, query: str | None) -> dict | None:
        if not query:
            return None

        decoded_json = self._find_and_decode_json(query)
        if decoded_json:
            data, _ = decoded_json
            # Now that we have the parsed JSON, we need to decide which one to use.
            # Assuming the primary JSON object is the one containing 'originErrorInfo'
            # or similar structure that indicates it's the log data we're interested in.
            # If there are multiple JSON objects, this needs a clearer rule.
            # For now, let's assume the first valid JSON that has 'originErrorInfo' is the one.
            if "originErrorInfo" in data:
                origin_error_info = data.get("originErrorInfo", {})
                # Ensure requestHeaders, responseHeaders, and responseBody are parsed if they are strings
                request_headers = origin_error_info.get("requestHeaders", "{}")
                if isinstance(request_headers, str):
                    request_headers = json.loads(request_headers)

                response_headers = origin_error_info.get("responseHeaders", "{}")
                if isinstance(response_headers, str):
                    response_headers = json.loads(response_headers)

                response_body = origin_error_info.get("responseBody", "{}")
                if isinstance(response_body, str):
                    try:
                        response_body = json.loads(response_body)
                    except json.JSONDecodeError:
                        response_body = response_body

                request_body = origin_error_info.get("requestBody", "{}")
                if isinstance(request_body, str):
                    request_body = json.loads(request_body)

                request_info = RequestInfo(
                    url=origin_error_info.get("url"),
                    request_headers=request_headers,
                    response_headers=response_headers,
                    request_body=request_body,
                    response_body=response_body,
                )
                items = self.get_items(request_info)
                return {"items": items}
        return None

    def get_items(self, request_info: RequestInfo):
        items = list()
        data = asdict(request_info)
        all_info = ""
        for key, value in data.items():
            if value:
                if isinstance(value, dict) or isinstance(value, list):
                    value = json.dumps(value, ensure_ascii=False)

                all_info += f"{KEY_NAME[key]}:\n{value}\n\n"
                items.append(
                    {
                        "arg": value,
                        "title": KEY_NAME[key],
                        "subtitle": value,
                        "icon": "",
                    }
                )

        return [
            {"arg": all_info, "title": "请求信息", "subtitle": all_info, "icon": ""}
        ] + items


def main():
    parse_tools = QueryBase()
    handler = ParseRequestInfoHandler()

    parse_tools.add_handler(handler)

    parse_tools.main()


if __name__ == "__main__":
    main()
