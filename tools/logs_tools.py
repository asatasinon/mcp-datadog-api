"""
Datadog 日志(Logs) API 工具模块

该模块提供对Datadog日志API的访问，包括:
- 查询日志数据
"""

from typing import Dict, Any, Optional, List

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import (
    LogsListRequestPage,
)
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter

from mcp.server.fastmcp import FastMCP
from utils.api_utils import get_api_client_configuration


def register_logs_tools(mcp: FastMCP) -> None:
    """
    向MCP服务器注册日志相关工具

    Args:
        mcp: MCP服务器实例
    """

    @mcp.tool()
    def query_logs(
        query: str,
        from_time: str = "now-15m",
        to_time: str = "now",
        limit: int = 25,
        sort: str = "-timestamp",
        indexes: Optional[List[str]] = ["main"],
    ) -> Dict[str, Any]:
        """
        查询日志数据

        Args:
            query: 查询字符串，例如 "service:web"
            from_time: 开始时间，可以是ISO8601格式或相对时间，默认为"now-15m"
            to_time: 结束时间，可以是ISO8601格式或相对时间，默认为"now"
            limit: 返回的最大日志数量，默认为25
            sort: 排序方式，默认为"-timestamp"(按时间戳降序排序)
            indexes: 可选，要搜索的日志索引列表

        Returns:
            包含日志数据的字典
        """
        # 创建查询过滤器
        filter_params = {
            "query": query,
            "from": from_time,
            "to": to_time,
        }

        # 如果提供了索引，添加到过滤器中
        if indexes:
            filter_params["indexes"] = indexes

        # 创建请求体
        body = LogsListRequest(
            filter=LogsQueryFilter(**filter_params),
            page=LogsListRequestPage(
                limit=limit,
            ),
            sort=sort,
        )

        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.list_logs(body=body)
            return response.to_dict()
