# Datadog查询语法

本文档介绍了Datadog调用链搜索的查询语法，用于在API查询中筛选调用链数据。

## 搜索查询

搜索查询可用于过滤调用链数据，语法基于属性和值的组合。

### 基本语法

#### 属性搜索

要搜索特定属性，使用以下语法：

```
@attribute_name:value
```

属性名称前需要加上`@`符号，例如：

```
@http.status_code:200
```

#### 标签搜索

要搜索特定标签，使用以下语法（无需添加`@`前缀）：

```
tag_name:value
```

例如：

```
service:payment-api
```

#### 通配符

支持在搜索值中使用通配符：

```
service:web-*
```

这将匹配所有以"web-"开头的服务，例如web-store，web-api等。

#### 数值搜索

对于数值类型，支持使用比较操作符：

```
@http.status_code:>400          // 大于400
@duration:<100ms                // 小于100毫秒
@duration:[100ms TO 200ms]     // 介于100ms和200ms之间
```

支持的单位：
- 时间：`ns`（纳秒）、`us`（微秒）、`ms`（毫秒）、`s`（秒）、`m`（分钟）、`h`（小时）、`d`（天）
- 字节：`b`（字节）、`kb`（千字节）、`mb`（兆字节）、`gb`（吉字节）、`tb`（太字节）

### 组合查询

可以使用布尔操作符组合多个条件：

- `AND` 或空格：表示与操作
- `OR`：表示或操作
- `-`：表示非操作

例如：

```
service:web-store @http.status_code:>400          // 同时满足两个条件
service:web-store OR service:payment-api          // 满足任一条件
service:web-store -@http.status_code:404          // web-store服务但排除404状态码
```

### 转义特殊字符

如果搜索值中包含特殊字符，可以使用双引号将其括起来：

```
@http.url:"https://example.com/search?q=datadog"
```

需要转义的特殊字符包括：`:`, `/`, `?`, `=`, `&` 等。

### 常用保留属性

| 属性 | 描述 |
| --- | --- |
| @service | 发出调用链的服务名称 |
| @name | 操作名称 |
| @resource | 资源名称 |
| @duration | 调用链持续时间 |
| @error | 是否发生错误 |
| @trace_id | 跟踪ID |
| @span_id | 调用链ID |
| @parent_id | 父调用链ID |
| @env | 环境标识 |
| @version | 服务版本 |

### 同级服务属性

对于非直接检测的依赖服务，可以使用以下同级属性查询：

| 属性 | 描述 |
| --- | --- |
| @peer.service | 同级服务名称 |
| @peer.hostname | 同级主机名 |
| @peer.port | 同级端口 |
| @peer.db.system | 数据库类型 |
| @peer.db.name | 数据库名称 |
| @peer.db.user | 数据库用户 |

例如，查找与特定数据库表相关的调用链：

```
@peer.db.name:users @peer.db.system:postgres
```

## 查询示例

以下是一些常见的查询示例：

### 服务查询

```
service:web-store                 // 查询web-store服务的所有调用链
service:web-store env:production  // 查询生产环境中web-store服务的调用链
```

### 错误查询

```
@error:true                                // 所有错误的调用链
service:payment-api @error:true            // payment-api服务中的错误调用链
service:payment-api @http.status_code:>499 // payment-api服务中的HTTP 5xx错误
```

### 性能查询

```
service:web-store @duration:>1s            // 持续时间超过1秒的请求
@name:sql.query @duration:>100ms           // 持续时间超过100毫秒的SQL查询
```

### 组合示例

```
(service:web-store OR service:payment-api) @error:true        // 两个服务中的错误
service:web-store (@http.status_code:200 @duration:>500ms)    // 成功但较慢的请求
```

## 保存的搜索

在Datadog界面中可以保存常用的搜索查询以便快速访问。这些保存的搜索也可以通过API自动程序化使用。

## 高级用法

### 使用facets和measures

一旦为特定属性创建了facet或measure，就可以在查询中使用它们进行更复杂的搜索和聚合：

```
@http.response_size:>1mb         // 响应大小超过1MB的请求
@db.row_count:>1000              // 返回超过1000行的数据库查询
```
