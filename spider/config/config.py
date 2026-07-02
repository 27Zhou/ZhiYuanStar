"""
主配置文件
"""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from config.database import DatabaseConfig
from config.settings import SpiderSettings


class Config:
    """爬虫主配置类（单例）"""

    _instance: Optional['Config'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 加载环境变量
        load_dotenv()

        # 项目根目录
        self.project_root = Path(__file__).parent.parent

        # 数据库配置
        self.database = DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "gaokao_ai"),
        )

        # 爬虫配置
        self.spider = SpiderSettings(
            timeout=int(os.getenv("SPIDER_TIMEOUT", "30")),
            max_retries=int(os.getenv("SPIDER_MAX_RETRIES", "3")),
            max_workers=int(os.getenv("SPIDER_MAX_WORKERS", "5")),
            request_delay=float(os.getenv("SPIDER_REQUEST_DELAY", "1.0")),
            log_level=os.getenv("SPIDER_LOG_LEVEL", "INFO"),
        )

        # 数据目录
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 日志目录
        self.log_dir = self.project_root / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._initialized = True

    def get_data_path(self, filename: str) -> Path:
        """获取数据文件路径"""
        return self.data_dir / filename

    def get_log_path(self, filename: str) -> Path:
        """获取日志文件路径"""
        return self.log_dir / filename


# 全局配置实例
config = Config()
