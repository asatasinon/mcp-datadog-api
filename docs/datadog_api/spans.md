# datadog spans api

## query spans

### 概述

检索满足查询条件的APM调用链数据。该端点需要 `apm_read` 权限。

OAuth应用需要 `apm_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/spans/events/search`
method: `POST`

#### 请求体

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| filter | object | 查询过滤条件 |
| page | object | 分页参数 |
| sort | string | 排序方式，例如 `-timestamp` 表示按时间戳降序排序 |

##### filter对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| query | string | 查询字符串，使用Datadog APM查询语法 |
| from | string | 查询开始时间，ISO8601格式或相对时间（如 "now-15m"） |
| to | string | 查询结束时间，ISO8601格式或相对时间（如 "now"） |

##### page对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| limit | integer | 返回的最大调用链数量，默认为10，最大为1000 |
| cursor | string | 用于分页的游标 |

### 示例请求

```json
{
  "filter": {
    "query": "service:web-store",
    "from": "now-15m",
    "to": "now"
  },
  "page": {
    "limit": 25
  },
  "sort": "-timestamp"
}
```

### 响应

#### 200 成功

成功返回符合条件的调用链列表。

##### 模型

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| data | array | 调用链数组 |
| links | object | 分页链接 |
| meta | object | 元数据信息 |

###### data数组项

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 调用链唯一标识符 |
| type | string | 资源类型，值为 "span" |
| attributes | object | 调用链属性 |

###### attributes对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| service | string | 服务名称 |
| name | string | 操作名称 |
| resource | string | 资源名称 |
| trace_id | string | 所属跟踪ID |
| span_id | string | 调用链ID |
| parent_id | string | 父调用链ID |
| duration | integer | 持续时间（纳秒） |
| start | integer | 开始时间（纳秒） |
| error | boolean | 是否发生错误 |
| tags | object | 标签对象 |
| metrics | object | 指标对象 |
| meta | object | 元数据对象 |

###### links对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| next | string | 获取下一页结果的链接 |

###### meta对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| page | object | 分页信息 |

### 示例响应

```json
{
  "data": [
    {
      "id": "AAAAAYHyf5wRjw39LwAAAABBWUh5ZjV3UmpyOE5wdmFqRVZkUT09",
      "type": "span",
      "attributes": {
        "service": "web-store",
        "name": "web.request",
        "resource": "GET /api/products",
        "trace_id": "7136434181313622116",
        "span_id": "7136434181313622116",
        "parent_id": 0,
        "duration": 246600000,
        "start": 1623856690494787000,
        "error": false,
        "meta": {
          "http.method": "GET",
          "http.url": "/api/products",
          "env": "production",
          "version": "v1.0.0"
        },
        "metrics": {
          "system.process.cpu.user": 0.23,
          "system.process.cpu.system": 0.15
        }
      }
    }
  ],
  "links": {
    "next": "https://api.datadoghq.com/api/v2/spans/events?page[cursor]=eyJzdGFydEF0IjoiQVlIeVFyS1NZY3YyVVE9PSJ9"
  },
  "meta": {
    "page": {
      "after": "AAAAAYHyf5wRjw39LwAAAABBWUh5ZjV3UmpyOE5wdmFqRVZkUT09"
    }
  }
}
```

> **代码示例请参考：** [spans_example.md](example/spans_example.md#query-spans)

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

> **代码示例请参考：** [spans_example.md](example/spans_example.md#aggregate-spans)

