# datadog logs api 代码示例

## query logs

### 代码示例

```python
"""
使用 POST 方法搜索日志
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter

body = LogsListRequest(
    filter=LogsQueryFilter(
        query="service:web",
        from_="now-15m",
        to="now",
        indexes=["main"],
    ),
    page=LogsListRequestPage(
        limit=10,
    ),
    sort="-time",
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = LogsApi(api_client)
    response = api_instance.list_logs_post(body=body)

    print(response)
```

