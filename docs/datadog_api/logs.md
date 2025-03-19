# datadog logs api

## query logs

### 概述

检索符合给定查询条件的日志列表。该端点需要 `logs_read` 权限。

OAuth应用需要 `logs_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/logs/events/search`
method: `POST`

#### 请求体

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| filter | object | 查询过滤条件 |
| page | object | 分页参数 |
| sort | string | 排序方式 |

##### filter对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| query | string | 查询字符串，使用Datadog日志查询语法 |
| from | string | 日志开始时间，ISO8601格式或相对时间 |
| to | string | 日志结束时间，ISO8601格式或相对时间 |
| indexes | array | 要搜索的日志索引列表 |

##### page对象

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| limit | integer | 返回的最大日志数量，默认为10，最大为1000 |
| cursor | string | 用于分页的游标 |

### 示例请求

```json
{
  "filter": {
    "query": "service:web",
    "from": "2020-06-24T16:10:00Z",
    "to": "2020-06-24T16:11:00Z"
  },
  "page": {
    "limit": 5
  },
  "sort": "-time"
}
```

### 响应

#### 200 成功

成功返回符合条件的日志列表。

##### 模型

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| data | array | 日志事件数组 |
| links | object | 分页链接 |
| meta | object | 元数据信息 |

###### data数组项

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 日志唯一标识符 |
| type | string | 资源类型，值为 "log" |
| attributes | object | 日志属性 |

###### attributes对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| message | string | 日志原始消息 |
| status | string | 日志状态，如 "info", "warning", "error" |
| service | string | 源服务名称 |
| tags | array | 标签列表 |
| timestamp | string | 日志生成时间，ISO8601格式 |
| host | string | 来源主机 |
| attributes | object | 额外属性 |

###### links对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| next | string | 获取下一页结果的链接 |

###### meta对象

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| page | object | 分页信息 |
| status | string | 请求状态，如 "done" |
| warnings | array | 警告信息 |

### 示例响应

```json
{
  "data": [
    {
      "id": "AAAAAYNPZnQBs-Y69wAAAABBWVF1YW5mb2xFVFktNHRxUTBHYXc",
      "type": "log",
      "attributes": {
        "status": "info",
        "service": "web",
        "tags": [
          "env:prod",
          "service:web"
        ],
        "timestamp": "2020-06-24T16:10:32.000Z",
        "host": "web-server-1",
        "attributes": {
          "duration": 123,
          "http": {
            "method": "GET",
            "status_code": 200,
            "url": "/api/users"
          }
        },
        "message": "GET /api/users 200 123ms"
      }
    }
  ],
  "links": {
    "next": "https://api.datadoghq.com/api/v2/logs/events?page[cursor]=eyJzdGFydEF0IjoiQVlOUDNHWURzLVk2OXc9PSJ9"
  },
  "meta": {
    "page": {
      "after": "AAAAAYNPZnQBs-Y69wAAAABBWVF1YW5mb2xFVFktNHRxUTBHYXc"
    },
    "status": "done",
    "warnings": [
      {
        "code": "unknown_index",
        "detail": "indexes: foo, bar",
        "title": "One or several indexes are missing or invalid, results hold data from the other indexes"
      }
    ]
  }
}
```

> **代码示例请参考：** [logs_example.md](example/logs_example.md#query-logs)



