"""
日志模块
使用loguru实现统一日志管理
"""
import sys
from pathlib import Path

from loguru import logger


class Logger:
    """日志管理类（单例）"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 确保日志目录存在
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        # 移除默认handler
        logger.remove()

        # 控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            level="INFO",
            colorize=True,
        )

        # 一般日志文件
        logger.add(
            "logs/spider_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="00:00",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
        )

        # 错误日志文件
        logger.add(
            "logs/error_{time:YYYY-MM-DD}.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="ERROR",
            rotation="00:00",
            retention="60 days",
            compression="zip",
            encoding="utf-8",
        )

        self._initialized = True

    def get_logger(self):
        """获取logger实例"""
        return logger


# 全局日志实例
logger_instance = Logger()
logger = logger_instance.get_logger()
