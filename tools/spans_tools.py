"""
Datadog 调用链(Spans) API 工具模块

该模块提供对Datadog APM调用链API的访问，包括:
- 查询调用链数据
- 聚合调用链数据
"""

from typing import Dict, Any, Optional, List

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.spans_api import SpansApi
from datadog_api_client.v2.model.spans_list_request import SpansListRequest
from datadog_api_client.v2.model.spans_list_request_page import (
    SpansListRequestPage,
)
from datadog_api_client.v2.model.spans_query_filter import SpansQueryFilter
from datadog_api_client.v2.model.spans_aggregate_data import SpansAggregateData
from datadog_api_client.v2.model.spans_aggregate_request import (
    SpansAggregateRequest,
)
from datadog_api_client.v2.model.spans_aggregate_request_attributes import (
    SpansAggregateRequestAttributes,
)
from datadog_api_client.v2.model.spans_aggregate_request_type import (
    SpansAggregateRequestType,
)
from datadog_api_client.v2.model.spans_aggregation_function import (
    SpansAggregationFunction,
)
from datadog_api_client.v2.model.spans_compute import SpansCompute
from datadog_api_client.v2.model.spans_compute_type import SpansComputeType
from datadog_api_client.v2.model.spans_list_request_data import (
    SpansListRequestData,
)
from datadog_api_client.v2.model.spans_list_request_attributes import (
    SpansListRequestAttributes,
)
from datadog_api_client.v2.model.spans_list_request_type import (
    SpansListRequestType,
)
from datadog_api_client.v2.model.spans_query_options import SpansQueryOptions
from datadog_api_client.v2.model.spans_sort import SpansSort

from mcp.server.fastmcp import FastMCP
from utils.api_utils import get_api_client_configuration


def register_spans_tools(mcp: FastMCP) -> None:
    """
    向MCP服务器注册调用链相关工具

    Args:
        mcp: MCP服务器实例
    """

    @mcp.tool()
    def query_spans(
        query: str = "*",
        from_time: str = "now-15m",
        to_time: str = "now",
        limit: int = 25,
        sort: str = "timestamp",
        timezone: str = "GMT",
    ) -> Dict[str, Any]:
        """
        查询调用链数据

        Args:
            query: 查询字符串，例如"service:web-store"或"*"表示所有调用链
            from_time: 开始时间，可以是ISO8601格式或相对时间，默认为"now-15m"
            to_time: 结束时间，可以是ISO8601格式或相对时间，默认为"now"
            limit: 返回的最大调用链数量，默认为25
            sort: 排序方式，可选值："timestamp"(升序)或"-timestamp"(降序)，默认为"timestamp"
            timezone: 时区，默认为"GMT"

        Returns:
            包含调用链数据的字典
        """
        # 处理排序选项
        sort_enum = (
            SpansSort.TIMESTAMP_ASCENDING
            if sort == "timestamp"
            else SpansSort.TIMESTAMP_DESCENDING
        )

        # 创建请求体
        body = SpansListRequest(
            data=SpansListRequestData(
                attributes=SpansListRequestAttributes(
                    filter=SpansQueryFilter(
                        query=query,
                        _from=from_time,
                        to=to_time,
                    ),
                    options=SpansQueryOptions(
                        timezone=timezone,
                    ),
                    page=SpansListRequestPage(
                        limit=limit,
                    ),
                    sort=sort_enum,
                ),
                type=SpansListRequestType.SEARCH_REQUEST,
            ),
        )

        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = SpansApi(api_client)
            response = api_instance.list_spans(body=body)
            return response.to_dict()

    @mcp.tool()
    def aggregate_spans(
        query: str = "*",
        from_time: str = "now-15m",
        to_time: str = "now",
        aggregation: str = "count",
        interval: str = "5m",
        compute_type: str = "timeseries",
        group_by: Optional[List[str]] = None,
        measure: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        聚合调用链数据

        Args:
            query: 查询字符串，默认为"*"(所有调用链)
            from_time: 开始时间，可以是ISO8601格式或相对时间，默认为"now-15m"
            to_time: 结束时间，可以是ISO8601格式或相对时间，默认为"now"
            aggregation: 聚合函数，可选值: "count", "avg", "sum", "min", "max"
            interval: 时间间隔，例如"5m"表示5分钟，默认为"5m"
            compute_type: 计算类型，可选值: "timeseries", "total"
            group_by: 可选，分组字段列表
            measure: 可选，要聚合的度量，某些聚合函数(如avg、sum)需要此字段

        Returns:
            包含聚合结果的字典
        """
        # 转换聚合函数字符串为枚举
        aggregation_enum = SpansAggregationFunction(aggregation.upper())
        compute_type_enum = SpansComputeType(compute_type.upper())

        # 创建计算配置
        compute = SpansCompute(
            aggregation=aggregation_enum,
            interval=interval,
            type=compute_type_enum,
        )

        # 如果提供了measure参数，添加到计算配置中
        if measure:
            compute["measure"] = measure

        # 创建请求体
        body = SpansAggregateRequest(
            data=SpansAggregateData(
                attributes=SpansAggregateRequestAttributes(
                    compute=[compute],
                    filter=SpansQueryFilter(
                        from_=from_time,
                        query=query,
                        to=to_time,
                    ),
                    # 如果提供了group_by参数，添加到请求中
                    group_by=group_by if group_by else None,
                ),
                type=SpansAggregateRequestType.AGGREGATE_REQUEST,
            ),
        )

        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = SpansApi(api_client)
            response = api_instance.aggregate_spans(body=body)
            return response.to_dict()
