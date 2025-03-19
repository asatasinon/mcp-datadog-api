"""
Datadog 指标(Metrics) API 工具模块

该模块提供对Datadog指标API的访问，包括:
- 列出活跃指标
- 搜索指标
- 查询指标元数据
- 查询时间序列数据
- 查询标量数据
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi as MetricsApiV1
from datadog_api_client.v2.api.metrics_api import MetricsApi as MetricsApiV2

from datadog_api_client.v2.model.formula_limit import FormulaLimit
from datadog_api_client.v2.model.metrics_data_source import MetricsDataSource
from datadog_api_client.v2.model.metrics_timeseries_query import (
    MetricsTimeseriesQuery,
)
from datadog_api_client.v2.model.query_formula import QueryFormula
from datadog_api_client.v2.model.query_sort_order import QuerySortOrder
from datadog_api_client.v2.model.timeseries_formula_query_request import (
    TimeseriesFormulaQueryRequest,
)
from datadog_api_client.v2.model.timeseries_formula_request import (
    TimeseriesFormulaRequest,
)
from datadog_api_client.v2.model.timeseries_formula_request_attributes import (
    TimeseriesFormulaRequestAttributes,
)
from datadog_api_client.v2.model.timeseries_formula_request_queries import (
    TimeseriesFormulaRequestQueries,
)
from datadog_api_client.v2.model.timeseries_formula_request_type import (
    TimeseriesFormulaRequestType,
)

from datadog_api_client.v2.model.metrics_aggregator import MetricsAggregator
from datadog_api_client.v2.model.metrics_scalar_query import MetricsScalarQuery
from datadog_api_client.v2.model.scalar_formula_query_request import (
    ScalarFormulaQueryRequest,
)
from datadog_api_client.v2.model.scalar_formula_request import (
    ScalarFormulaRequest,
)
from datadog_api_client.v2.model.scalar_formula_request_attributes import (
    ScalarFormulaRequestAttributes,
)
from datadog_api_client.v2.model.scalar_formula_request_queries import (
    ScalarFormulaRequestQueries,
)
from datadog_api_client.v2.model.scalar_formula_request_type import (
    ScalarFormulaRequestType,
)

from mcp.server.fastmcp import FastMCP
from utils.api_utils import get_api_client_configuration


def register_metrics_tools(mcp: FastMCP) -> None:
    """
    向MCP服务器注册指标相关工具

    Args:
        mcp: MCP服务器实例
    """

    @mcp.tool()
    def list_metrics(
        from_time: int, host: Optional[str] = None, tag_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取从指定时间到现在的活跃上报指标列表

        Args:
            from_time: Unix纪元秒数，表示开始时间
            host: 可选，用于过滤指标列表的主机名
            tag_filter: 可选，用于过滤指标的标签表达式

        Returns:
            包含指标列表的字典
        """
        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = MetricsApiV1(api_client)
            params = {"_from": from_time}

            if host:
                params["host"] = host
            if tag_filter:
                params["tag_filter"] = tag_filter

            response = api_instance.list_active_metrics(**params)
            return response.to_dict()

    @mcp.tool()
    def search_metrics(query: str) -> Dict[str, Any]:
        """
        根据查询字符串搜索指标

        Args:
            query: 查询字符串，例如 "metrics:system.cpu" 或者 "tags:host:my-host"

        Returns:
            包含匹配指标的字典
        """
        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = MetricsApiV1(api_client)
            response = api_instance.list_metrics(q=query)
            return response.to_dict()

    @mcp.tool()
    def get_metric_metadata(metric_name: str) -> Dict[str, Any]:
        """
        获取指定指标的元数据信息

        Args:
            metric_name: 指标名称，例如 "system.cpu.user"

        Returns:
            包含指标元数据的字典
        """
        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = MetricsApiV1(api_client)
            response = api_instance.get_metric_metadata(metric_name=metric_name)
            return response.to_dict()

    @mcp.tool()
    def query_timeseries(
        query: str,
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
        interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        查询时间序列数据

        Args:
            query: 指标查询字符串，例如 "avg:system.cpu.user{*}"
            from_time: 可选，开始时间的Unix毫秒时间戳，默认为15分钟前
            to_time: 可选，结束时间的Unix毫秒时间戳，默认为当前时间
            interval: 可选，时间间隔(毫秒)

        Returns:
            包含时间序列数据的字典
        """
        # 设置默认时间范围（如果未提供）
        if from_time is None:
            from_time = int((datetime.now() - timedelta(minutes=15)).timestamp() * 1000)
        if to_time is None:
            to_time = int(datetime.now().timestamp() * 1000)

        # 创建查询请求
        body = TimeseriesFormulaQueryRequest(
            data=TimeseriesFormulaRequest(
                attributes=TimeseriesFormulaRequestAttributes(
                    formulas=[
                        QueryFormula(
                            formula="a",
                            limit=FormulaLimit(
                                count=10,
                                order=QuerySortOrder.DESC,
                            ),
                        ),
                    ],
                    _from=from_time,
                    to=to_time,
                    queries=TimeseriesFormulaRequestQueries(
                        [
                            MetricsTimeseriesQuery(
                                data_source=MetricsDataSource.METRICS,
                                query=query,
                                name="a",
                            ),
                        ]
                    ),
                    interval=interval,
                ),
                type=TimeseriesFormulaRequestType.TIMESERIES_REQUEST,
            ),
        )

        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = MetricsApiV2(api_client)
            response = api_instance.query_timeseries_data(body=body)
            return response.to_dict()

    @mcp.tool()
    def query_scalar(
        query: str,
        aggregator: str = "avg",
        from_time: Optional[int] = None,
        to_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        查询标量数据

        Args:
            query: 指标查询字符串，例如 "avg:system.cpu.user{*}"
            aggregator: 聚合函数，可选值: "avg", "sum", "min", "max", "count"
            from_time: 可选，开始时间的Unix毫秒时间戳，默认为15分钟前
            to_time: 可选，结束时间的Unix毫秒时间戳，默认为当前时间

        Returns:
            包含标量数据的字典
        """
        # 设置默认时间范围（如果未提供）
        if from_time is None:
            from_time = int((datetime.now() - timedelta(minutes=15)).timestamp() * 1000)
        if to_time is None:
            to_time = int(datetime.now().timestamp() * 1000)

        # 将字符串聚合器转换为枚举
        aggregator_enum = MetricsAggregator(aggregator.upper())

        # 创建查询请求
        body = ScalarFormulaQueryRequest(
            data=ScalarFormulaRequest(
                attributes=ScalarFormulaRequestAttributes(
                    formulas=[
                        QueryFormula(
                            formula="a",
                            limit=FormulaLimit(
                                count=10,
                                order=QuerySortOrder.DESC,
                            ),
                        ),
                    ],
                    _from=from_time,
                    queries=ScalarFormulaRequestQueries(
                        [
                            MetricsScalarQuery(
                                aggregator=aggregator_enum,
                                data_source=MetricsDataSource.METRICS,
                                query=query,
                                name="a",
                            ),
                        ]
                    ),
                    to=to_time,
                ),
                type=ScalarFormulaRequestType.SCALAR_REQUEST,
            ),
        )

        with ApiClient(get_api_client_configuration()) as api_client:
            api_instance = MetricsApiV2(api_client)
            response = api_instance.query_scalar_data(body=body)
            return response.to_dict()
