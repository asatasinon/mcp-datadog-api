"""
Datadog API工具通用工具函数模块

该模块提供了各个API工具模块共享的工具函数。
"""

import os
from datadog_api_client import Configuration


def get_api_client_configuration() -> Configuration:
    """
    创建并返回Datadog API客户端配置

    根据环境变量创建适当的API客户端配置。
    如果环境变量DD_SITE存在，则使用该值作为Datadog站点，
    否则默认为datadoghq.com。

    Returns:
        Configuration: 已配置的API客户端配置对象
    """
    configuration = Configuration()
    site = os.environ.get("DD_SITE", "datadoghq.com")
    configuration.server_variables["site"] = site

    # 设置API密钥和应用密钥
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")

    if api_key:
        configuration.api_key["apiKeyAuth"] = api_key
    if app_key:
        configuration.api_key["appKeyAuth"] = app_key

    return configuration
