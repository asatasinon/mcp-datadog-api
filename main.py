import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 导入各个模块
from tools.metrics_tools import register_metrics_tools
from tools.spans_tools import register_spans_tools
from tools.logs_tools import register_logs_tools

# 加载环境变量
load_dotenv()

# 创建FastMCP服务器实例
mcp = FastMCP("datadog-api")

# 注册各模块的工具
register_metrics_tools(mcp)
register_spans_tools(mcp)
register_logs_tools(mcp)

# 获取环境变量
api_key = os.environ.get("DD_API_KEY")
app_key = os.environ.get("DD_APP_KEY")
site = os.environ.get("DD_SITE", "datadoghq.com")


def main():
    """
    mcp-datadog-api的主入口函数

    这是一个ModelContextProtocol (MCP) 服务器，提供调用Datadog API的能力。
    可以查询指标、日志和APM调用链数据。
    """
    print("正在启动mcp-datadog-api服务器...")

    # 检查环境变量是否设置
    if not api_key or not app_key:
        print("警告: 未设置Datadog API密钥和/或应用密钥")
        print("请设置以下环境变量:")
        print("  - DD_API_KEY: Datadog API密钥")
        print("  - DD_APP_KEY: Datadog 应用密钥")
        print("  - DD_SITE: Datadog站点 (可选，默认为datadoghq.com)")
        return

    # 启动MCP服务器
    print(f"MCP服务器已启动，使用Datadog站点: {site}")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
