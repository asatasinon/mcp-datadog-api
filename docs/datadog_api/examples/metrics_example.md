# datadog api - metrics 代码示例

## list metrics

### 代码示例

```python
"""
Get active metrics list returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.list_active_metrics(
        _from=9223372036854775807,
    )

    print(response)
```

## search metrics

### 代码示例

```python
"""
搜索指标示例
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.list_metrics(
        q="metrics:system.cpu"
    )

    print(response)
```

## query metric metadata

### 代码示例

```python
"""
获取指标元数据示例
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.get_metric_metadata(
        metric_name="system.cpu.user",
    )

    print(response)
```

## query timeseries

### 代码示例

```python
"""
查询时间序列数据示例
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.formula_limit import FormulaLimit
from datadog_api_client.v2.model.metrics_data_source import MetricsDataSource
from datadog_api_client.v2.model.metrics_timeseries_query import MetricsTimeseriesQuery
from datadog_api_client.v2.model.query_formula import QueryFormula
from datadog_api_client.v2.model.query_sort_order import QuerySortOrder
from datadog_api_client.v2.model.timeseries_formula_query_request import TimeseriesFormulaQueryRequest
from datadog_api_client.v2.model.timeseries_formula_request import TimeseriesFormulaRequest
from datadog_api_client.v2.model.timeseries_formula_request_attributes import TimeseriesFormulaRequestAttributes
from datadog_api_client.v2.model.timeseries_formula_request_queries import TimeseriesFormulaRequestQueries
from datadog_api_client.v2.model.timeseries_formula_request_type import TimeseriesFormulaRequestType

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
            _from=1636625471000,  # 注意这里使用的是毫秒时间戳
            interval=5000,
            queries=TimeseriesFormulaRequestQueries(
                [
                    MetricsTimeseriesQuery(
                        data_source=MetricsDataSource.METRICS,
                        query="avg:datadog.estimated_usage.metrics.custom{*}",
                        name="a",
                    ),
                ]
            ),
            to=1636629071000,  # 注意这里使用的是毫秒时间戳
        ),
        type=TimeseriesFormulaRequestType.TIMESERIES_REQUEST,
    ),
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.query_timeseries_data(body=body)  # 注意正确的方法名是query_timeseries_data

    print(response)
```

## query scalar

### 代码示例

```python
"""
查询标量数据示例
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.formula_limit import FormulaLimit
from datadog_api_client.v2.model.metrics_aggregator import MetricsAggregator
from datadog_api_client.v2.model.metrics_data_source import MetricsDataSource
from datadog_api_client.v2.model.metrics_scalar_query import MetricsScalarQuery
from datadog_api_client.v2.model.query_formula import QueryFormula
from datadog_api_client.v2.model.query_sort_order import QuerySortOrder
from datadog_api_client.v2.model.scalar_formula_query_request import ScalarFormulaQueryRequest
from datadog_api_client.v2.model.scalar_formula_request import ScalarFormulaRequest
from datadog_api_client.v2.model.scalar_formula_request_attributes import ScalarFormulaRequestAttributes
from datadog_api_client.v2.model.scalar_formula_request_queries import ScalarFormulaRequestQueries
from datadog_api_client.v2.model.scalar_formula_request_type import ScalarFormulaRequestType

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
            _from=1636625471000,  # 注意这里使用的是毫秒时间戳
            queries=ScalarFormulaRequestQueries(
                [
                    MetricsScalarQuery(
                        aggregator=MetricsAggregator.AVG,
                        data_source=MetricsDataSource.METRICS,
                        query="avg:system.cpu.user{*}",
                        name="a",
                    ),
                ]
            ),
            to=1636629071000,  # 注意这里使用的是毫秒时间戳
        ),
        type=ScalarFormulaRequestType.SCALAR_REQUEST,
    ),
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.query_scalar_data(body=body)

    print(response)
```
