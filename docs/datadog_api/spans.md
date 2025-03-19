# datadog spans api

## query spans

### 概述

查询接口返回与Span搜索查询匹配的调用链数据，结果支持分页。

该接口可用于构建复杂的Span过滤和搜索功能。此端点的访问限制为每小时`300`个请求。

OAuth应用需要`apm_read`授权范围才能访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/spans/events/search`
method: `POST`

#### 请求体

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| data | object | 搜索请求数据 |

##### data对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| attributes | object | 搜索请求属性 |
| type | string | 资源类型，应为 `search_request` |

##### attributes对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| filter | object | 查询过滤条件 |
| options | object | 查询选项（可选） |
| page | object | 分页选项（可选） |
| sort | string | 排序方式，如 `timestamp`（升序）或 `-timestamp`（降序） |

##### filter对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| query | string | 查询字符串 |
| from | string | 查询开始时间 |
| to | string | 查询结束时间 |

##### options对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| timezone | string | 时区，如 `GMT` |

##### page对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| limit | integer | 每页返回的结果数量 |

### 示例请求

```json
{
  "data": {
    "attributes": {
      "filter": {
        "from": "now-15m",
        "query": "*",
        "to": "now"
      },
      "options": {
        "timezone": "GMT"
      },
      "page": {
        "limit": 25
      },
      "sort": "timestamp"
    },
    "type": "search_request"
  }
}
```

### 响应

#### 200 成功

成功返回匹配的Span列表。

##### 模型

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| data | array | Span数据数组 |
| meta | object | 元数据信息 |
| links | object | 分页链接 |

###### data数组项

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| attributes | object | Span属性 |
| id | string | Span唯一标识符 |
| type | string | 资源类型，值为 `span` |

###### meta对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| page | object | 分页信息 |

###### links对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| next | string | 下一页链接（如果有） |

### 示例响应

```json
{
  "data": [
    {
      "attributes": {
        "duration": 105684,
        "service": "web-store",
        "span_id": "7395267463157753000",
        "start": "2023-06-16T14:05:12.252Z",
        "trace_id": "2798673868388127293",
        "attributes": {
          "environment": "production",
          "resource_name": "GET /api/products",
          "status": "ok"
        }
      },
      "id": "span-1",
      "type": "span"
    }
  ],
  "meta": {
    "page": {
      "after": "span-1"
    }
  },
  "links": {
    "next": "https://api.datadoghq.com/api/v2/spans/events/search?page[cursor]=span-1"
  }
}
```

> **代码示例请参考：** [spans_example.md](examples/spans_example.md#query-spans)

## aggregate spans

### 概述

聚合和计算APM调用链数据的统计信息。该端点需要 `apm_read` 权限。

OAuth应用需要 `apm_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/spans/analytics/aggregate`
method: `POST`

#### 请求体

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| data | object | 聚合请求数据 |

##### data对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| attributes | object | 聚合查询属性 |
| type | string | 资源类型，应为 `aggregate_request` |

##### attributes对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| compute | array | 计算方式数组 |
| filter | object | 查询过滤条件 |
| group_by | array | 分组字段数组（可选） |

##### compute数组项

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| aggregation | string | 聚合函数，如 `count`、`avg`、`sum` 等 |
| type | string | 计算类型，如 `timeseries`（时间序列）或 `total`（总计） |
| measure | string | 要聚合的度量，某些聚合函数需要此字段 |
| interval | string | 时间间隔，如 `5m`（5分钟），仅时间序列计算需要 |

##### filter对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| query | string | 查询字符串 |
| from | string | 查询开始时间 |
| to | string | 查询结束时间 |

### 示例请求

```json
{
  "data": {
    "attributes": {
      "compute": [
        {
          "aggregation": "count",
          "interval": "5m",
          "type": "timeseries"
        }
      ],
      "filter": {
        "from": "now-15m",
        "query": "*",
        "to": "now"
      }
    },
    "type": "aggregate_request"
  }
}
```

### 响应

#### 200 成功

成功返回聚合结果。

##### 模型

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| data | object | 聚合结果数据 |
| meta | object | 元数据信息 |

###### data对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| attributes | object | 结果属性 |
| id | string | 结果唯一标识符 |
| type | string | 资源类型，值为 `aggregate_response` |

###### attributes对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| buckets | array | 结果分桶数组 |

### 示例响应

```json
{
  "data": {
    "attributes": {
      "buckets": [
        {
          "computes": {
            "c0": 105
          },
          "by": {},
          "time": "2023-06-16T14:00:00.000Z"
        },
        {
          "computes": {
            "c0": 120
          },
          "by": {},
          "time": "2023-06-16T14:05:00.000Z"
        },
        {
          "computes": {
            "c0": 98
          },
          "by": {},
          "time": "2023-06-16T14:10:00.000Z"
        }
      ]
    },
    "id": "spans_agg_id_1",
    "type": "aggregate_response"
  },
  "meta": {
    "computation_time": 0.8521378040313721,
    "page": {
      "after": null
    },
    "status": "done"
  }
}
```

> **代码示例请参考：** [spans_example.md](examples/spans_example.md#aggregate-spans)

