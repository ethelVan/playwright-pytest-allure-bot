from typing import Optional, Dict, Any


def listen_for_graphql_response(page, url_keyword: str, query_keyword: str, timeout: Optional[float] = None) -> Dict[
    str, Any]:
    """
    监听 GraphQL 请求并返回响应数据。

    :param page: Playwright 页面对象。
    :param url_keyword: 接口 URL 的关键字（用于匹配请求 URL）。
    :param query_keyword: 请求内容的关键字（用于匹配请求体或响应体）。
    :param timeout: 超时时间（单位：毫秒）。
    :return: 返回接口的响应数据（字典格式）。
    """
    with page.expect_response(
            lambda resp: url_keyword in resp.url and query_keyword in resp.text(),
            timeout=timeout
    ) as resp_info:
        response = resp_info.value
        return response.json()
