# MCP Datadog API工具

这是一个基于ModelContextProtocol (MCP)的Datadog API工具服务器，提供了查询和分析Datadog数据的能力。

## 功能

该工具提供以下Datadog API的访问：

### 指标工具 (Metrics)

- **list_metrics**: 获取活跃指标列表
- **search_metrics**: 搜索指标
- **get_metric_metadata**: 获取指标元数据
- **query_timeseries**: 查询时间序列数据
- **query_scalar**: 查询标量数据

### 调用链工具 (APM/Traces)

- **query_spans**: 查询APM调用链数据
- **aggregate_spans**: 聚合调用链数据

### 日志工具 (Logs)

- **query_logs**: 查询日志数据

## 安装

1. 确保您已安装Python 3.10或更高版本
2. 克隆此仓库
3. 安装依赖：

```bash
pip install -r requirements.txt
```

或者使用uv：

```bash
uv pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example`文件为 `.env`：

```bash
cp .env.example .env
```

2. 编辑 `.env`文件，填入您的Datadog API密钥和应用密钥：

```
DD_SITE=datadoghq.com
DD_API_KEY=your_api_key_here
DD_APP_KEY=your_app_key_here
```

## 运行

使用MCP CLI工具启动服务器：

```bash
mcp dev main.py
```

## 与Claude for Desktop集成

要将此MCP服务器与Claude for Desktop集成，请按照以下步骤操作：

1. 确保已安装最新版本的[Claude for Desktop](https://claude.ai/download)
2. 编辑Claude for Desktop的配置文件，位于：

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%AppData%\Claude\claude_desktop_config.json`
3. 添加以下配置（替换路径为您的实际路径）：

```json
{
    "mcpServers": {
        "datadog-api": {
            "command": "python",
            "args": [
                "-m",
                "mcp",
                "dev",
                "/ABSOLUTE/PATH/TO/main.py"
            ]
        }
    }
}
```

4. 重启Claude for Desktop

## 使用示例

一旦MCP服务器运行并与Claude集成，您可以使用自然语言查询Datadog数据：

- "查询过去1小时的系统CPU使用率"
- "查找最近15分钟内有错误的服务调用"
- "显示web服务器的日志"

## 许可证

MIT

# 本地开发

## 安装

```bash
# 通过uv安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate

# 运行服务器
python main.py
```

## 配置vscode

新建 `.vscode/settings.json` 文件，添加以下内容：

```json
{
  "editor.rulers": [88],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.pythonPath": "${workspaceFolder}/.venv/bin/python"
}
```
