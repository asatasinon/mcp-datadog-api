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

### 简化版本代码示例

```python
"""
简化版本的日志搜索
"""
from datadog import initialize, api
import time

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

initialize(**options)

# 设置查询参数
now = int(time.time())
fifteen_mins_ago = now - 15 * 60
query = 'service:web'

# 查询日志
logs = api.Logs.query(
    time={
        'from': fifteen_mins_ago,
        'to': now
    },
    query=query,
    limit=10
)

print(logs)
```
