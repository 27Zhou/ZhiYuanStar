"""
配置模块
"""
from config.config import config
from config.database import DatabaseConfig
from config.settings import SpiderSettings

__all__ = ["config", "DatabaseConfig", "SpiderSettings"]
