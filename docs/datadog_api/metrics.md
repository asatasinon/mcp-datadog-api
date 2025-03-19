# datadog api - metrics

## list metrics

### 概述

获取从指定时间到现在的活跃上报指标列表。该端点需要 `metrics_read` 权限。

OAuth 应用需要 `metrics_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v1/metrics`
method: `GET`

### 参数

#### 查询字符串

| 名称        | 类型    | 描述                                                                               |
| ----------- | ------- | ---------------------------------------------------------------------------------- |
| from [必需] | integer | Unix 纪元以来的秒数                                                                |
| host        | string  | 用于过滤返回的指标列表的主机名。如果设置，返回的指标是那些具有相应主机名标签的指标 |
| tag_filter  | string  | 过滤具有给定标签的已提交指标。支持布尔和通配符表达式。不能与其他过滤器组合使用     |

### 响应

200 成功

#### 模型

返回对象列出了自指定时间以来由Datadog存储的所有指标名称。

| 字段    | 类型     | 描述                               |
| ------- | -------- | ---------------------------------- |
| from    | string   | 指标活跃的时间，以Unix纪元秒数表示 |
| metrics | [string] | 指标名称列表                       |

#### 示例

```json
{
  "from": "1578521682",
  "metrics": [
    "system.cpu.idle",
    "system.cpu.system",
    "system.cpu.iowait",
    "system.cpu.user",
    "system.cpu.stolen",
    "system.cpu.guest"
  ]
}
```

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#list-metrics)

## search metrics

### 概述

根据前缀、文本搜索或指标标签列出指标。该端点需要 `metrics_read` 权限。

OAuth应用需要 `metrics_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v1/search`
method: `GET`

### 参数

#### 查询字符串

| 名称      | 类型    | 描述                          |
| --------- | ------- | ----------------------------- |
| q [必需]  | string  | 要搜索的查询字符串            |
| page_size | integer | 每页返回的指标数量，最大为200 |
| page      | integer | 要获取的分页，首页是0         |

##### 查询语法

查询参数 `q` 支持以下语法：

- 前缀搜索: `metrics:sys` 会找出所有以"sys"开头的指标
- 文本搜索: `metrics:cpu.idle` 会找出包含"cpu.idle"的指标
- 标签搜索: `tags:host:my-host` 会找出在主机"my-host"上报告的指标

标签搜索还支持复杂的布尔表达式:

- `tags:env:prod AND host:web-server` - 搜索生产环境中的web-server
- `tags:env:prod OR env:staging` - 搜索生产或测试环境的指标

### 响应

#### 200 成功

成功返回匹配的指标列表。

##### 模型

| 字段     | 类型   | 描述                     |
| -------- | ------ | ------------------------ |
| results  | object | 包含查询结果的对象       |
| metadata | object | 元数据信息，包括分页信息 |

##### results对象

| 字段    | 类型     | 描述           |
| ------- | -------- | -------------- |
| metrics | [string] | 匹配的指标列表 |

### 示例响应

```json
{
  "results": {
    "metrics": [
      "system.cpu.idle",
      "system.cpu.user",
      "system.cpu.system",
      "system.cpu.iowait",
      "system.cpu.stolen"
    ]
  },
  "metadata": {
    "page": 0,
    "page_size": 5,
    "total_count": 125
  }
}
```

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#search-metrics)

## query metric metadata

### 概述

查询指标元数据，获取指定指标的详细信息、类型和单位等。该端点需要 `metrics_read` 权限。

OAuth应用需要 `metrics_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v1/metrics/{metric_name}`
method: `GET`

### 路径参数

| 名称               | 类型   | 描述             |
| ------------------ | ------ | ---------------- |
| metric_name [必需] | string | 要查询的指标名称 |

### 响应

#### 200 成功

成功返回指定指标的元数据。

##### 模型

| 字段     | 类型   | 描述                 |
| -------- | ------ | -------------------- |
| metadata | object | 包含指标元数据的对象 |

##### metadata对象

| 字段            | 类型    | 描述                                                             |
| --------------- | ------- | ---------------------------------------------------------------- |
| description     | string  | 指标的描述                                                       |
| integration     | string  | 采集此指标的集成名称                                             |
| per_unit        | string  | 指标的单位分母（如果适用）                                       |
| short_name      | string  | 指标的简短名称                                                   |
| statsd_interval | integer | 从StatsD采集此指标的间隔（如果适用）                             |
| type            | string  | 指标类型，可以是 `gauge`, `count`, `rate` 或 `histogram` |
| unit            | string  | 指标的单位                                                       |

### 示例响应

```json
{
  "metadata": {
    "description": "系统CPU用户时间比例",
    "integration": "system",
    "per_unit": "second",
    "short_name": "cpu user",
    "statsd_interval": 20,
    "type": "gauge",
    "unit": "percent"
  }
}
```

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#query-metric-metadata)

## list metric assets

### 概述

获取与指定指标相关联的仪表板、监控和其他资产。该端点需要 `metrics_read` 权限。

OAuth应用需要 `metrics_read` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/metrics/{metric_name}/assets`
method: `GET`

### 路径参数

| 名称               | 类型   | 描述             |
| ------------------ | ------ | ---------------- |
| metric_name [必需] | string | 要查询的指标名称 |

### 响应

#### 200 成功

成功返回与指标相关的资产列表。

##### 模型

| 字段 | 类型   | 描述               |
| ---- | ------ | ------------------ |
| data | object | 包含资产数据的对象 |

##### data对象

| 字段       | 类型  | 描述                   |
| ---------- | ----- | ---------------------- |
| dashboards | array | 使用该指标的仪表板列表 |
| monitors   | array | 使用该指标的监控列表   |
| notebooks  | array | 使用该指标的笔记本列表 |
| slos       | array | 使用该指标的SLO列表    |

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#list-metric-assets)

## query timeseries

### 概述

查询时间序列数据，跨各种数据源处理数据并应用公式和函数。该端点需要 `timeseries_query` 权限。

OAuth应用需要 `timeseries_query` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/query/timeseries`
method: `POST`

### 请求体

请求体应该包含查询参数，用于指定要检索的时间序列数据和如何处理这些数据。

#### 参数

| 名称        | 类型   | 描述               |
| ----------- | ------ | ------------------ |
| data [必需] | object | 查询定义和时间范围 |

##### data对象

| 名称              | 类型   | 描述                                   |
| ----------------- | ------ | -------------------------------------- |
| attributes [必需] | object | 查询详细信息，包括查询字符串和时间范围 |
| type [必需]       | string | 资源类型，应为 `timeseries_request`  |

##### attributes对象

| 名称           | 类型         | 描述                             |
| -------------- | ------------ | -------------------------------- |
| from [必需]    | integer      | 查询开始时间，Unix纪元毫秒数     |
| to [必需]      | integer      | 查询结束时间，Unix纪元毫秒数     |
| queries [必需] | array/object | 查询定义数组或包含多个查询的对象 |
| formulas       | array        | 公式定义数组（可选）             |
| interval       | integer      | 时间间隔（毫秒）（可选）         |

##### queries数组项

| 名称               | 类型   | 描述                                      |
| ------------------ | ------ | ----------------------------------------- |
| query [必需]       | string | 查询字符串，使用Datadog查询语言           |
| data_source [必需] | string | 数据源类型，如 `metrics`, `events` 等 |
| name [必需]        | string | 查询名称，用于在公式中引用                |

##### formula对象（可选）

| 名称           | 类型   | 描述                     |
| -------------- | ------ | ------------------------ |
| formula [必需] | string | 使用查询名称的公式表达式 |
| limit          | object | 限制配置（可选）         |

### 示例请求

```json
{
  "data": {
    "type": "timeseries_request",
    "attributes": {
      "from": 1636625471000,
      "to": 1636629071000,
      "queries": [
        {
          "data_source": "metrics",
          "query": "avg:system.cpu.user{*}",
          "name": "a"
        }
      ],
      "formulas": [
        {
          "formula": "a",
          "limit": {
            "count": 10,
            "order": "desc"
          }
        }
      ],
      "interval": 5000
    }
  }
}
```

### 响应

#### 200 成功

响应包含请求的时间序列数据。

##### 模型

| 字段 | 类型   | 描述               |
| ---- | ------ | ------------------ |
| data | object | 包含查询结果的对象 |

##### data对象

| 字段       | 类型   | 描述                                   |
| ---------- | ------ | -------------------------------------- |
| attributes | object | 包含查询结果数据的属性对象             |
| id         | string | 查询结果的唯一标识符                   |
| type       | string | 资源类型，值为 `timeseries_response` |

##### attributes对象

| 字段   | 类型  | 描述               |
| ------ | ----- | ------------------ |
| series | array | 时间序列数据点数组 |

##### series数组项

| 字段         | 类型    | 描述                   |
| ------------ | ------- | ---------------------- |
| metric       | string  | 指标名称               |
| display_name | string  | 显示名称               |
| pointlist    | array   | 时间戳和值的数组对     |
| tags         | array   | 与时间序列关联的标签   |
| query_index  | integer | 查询索引               |
| aggr         | string  | 聚合方法               |
| scope        | string  | 作用域                 |
| interval     | integer | 数据点之间的间隔（秒） |

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#query-timeseries)

## query scalar

### 概述

查询标量数据，跨各种数据源处理数据并应用公式和函数。该端点需要 `timeseries_query` 权限。

OAuth应用需要 `timeseries_query` 授权范围来访问此端点。

### 请求

api: `https://api.datadoghq.com/api/v2/query/scalar`
method: `POST`

### 请求体

请求体应该包含查询参数，用于指定要检索的标量数据和如何处理这些数据。

#### 参数

| 名称        | 类型   | 描述               |
| ----------- | ------ | ------------------ |
| data [必需] | object | 查询定义和时间范围 |

##### data对象

| 名称              | 类型   | 描述                                   |
| ----------------- | ------ | -------------------------------------- |
| attributes [必需] | object | 查询详细信息，包括查询字符串和时间范围 |
| type [必需]       | string | 资源类型，应为 `scalar_request`      |

##### attributes对象

| 名称           | 类型         | 描述                             |
| -------------- | ------------ | -------------------------------- |
| from [必需]    | integer      | 查询开始时间，Unix纪元毫秒数     |
| to [必需]      | integer      | 查询结束时间，Unix纪元毫秒数     |
| queries [必需] | array/object | 查询定义数组或包含多个查询的对象 |
| formulas       | array        | 公式定义数组（可选）             |

##### queries数组项

| 名称               | 类型   | 描述                                               |
| ------------------ | ------ | -------------------------------------------------- |
| aggregator [必需]  | string | 聚合函数，如 `avg`, `sum`, `min`, `max` 等 |
| data_source [必需] | string | 数据源类型，如 `metrics`                         |
| query [必需]       | string | 查询字符串，使用Datadog查询语言                    |
| name [必需]        | string | 查询名称，用于在公式中引用                         |

##### formula对象（可选）

| 名称           | 类型   | 描述                     |
| -------------- | ------ | ------------------------ |
| formula [必需] | string | 使用查询名称的公式表达式 |
| limit          | object | 限制配置（可选）         |

### 示例请求

```json
{
  "data": {
    "type": "scalar_request",
    "attributes": {
      "from": 1636625471000,
      "to": 1636629071000,
      "queries": [
        {
          "aggregator": "avg",
          "data_source": "metrics",
          "query": "avg:system.cpu.user{*}",
          "name": "a"
        }
      ],
      "formulas": [
        {
          "formula": "a",
          "limit": {
            "count": 10,
            "order": "desc"
          }
        }
      ]
    }
  }
}
```

### 响应

#### 200 成功

响应包含请求的标量数据值。

##### 模型

| 字段 | 类型   | 描述               |
| ---- | ------ | ------------------ |
| data | object | 包含查询结果的对象 |

##### data对象

| 字段       | 类型   | 描述                               |
| ---------- | ------ | ---------------------------------- |
| attributes | object | 包含查询结果数据的属性对象         |
| id         | string | 查询结果的唯一标识符               |
| type       | string | 资源类型，值为 `scalar_response` |

##### attributes对象

| 字段     | 类型   | 描述               |
| -------- | ------ | ------------------ |
| values   | array  | 标量数值数组       |
| times    | array  | 对应时间戳数组     |
| grouping | object | 分组信息（如果有） |

> **代码示例请参考：** [metrics_example.md](example/metrics_example.md#query-scalar)
