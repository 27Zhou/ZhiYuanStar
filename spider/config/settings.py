"""
爬虫配置模块
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class SpiderSettings:
    """爬虫基础配置"""

    # 请求配置
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0

    # 并发配置
    max_workers: int = 5
    max_concurrent_requests: int = 10

    # 限速配置
    request_delay: float = 1.0
    request_delay_random: float = 0.5

    # 缓存配置
    enable_cache: bool = True
    cache_expire: int = 3600

    # 代理配置
    enable_proxy: bool = False
    proxy_list: List[str] = field(default_factory=list)

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/spider.log"
    log_rotation: str = "10 MB"
    log_retention: str = "30 days"

    # 数据保存配置
    save_batch_size: int = 100
    save_interval: int = 60

    # User-Agent配置
    random_user_agent: bool = True

    # 请求头配置
    default_headers: Dict[str, str] = field(default_factory=lambda: {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    })
