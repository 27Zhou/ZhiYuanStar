"""
请求限速模块
控制请求频率，避免被封禁
"""
import time
import random
import threading
from typing import Optional
from collections import defaultdict

from utils.logger import logger


class RateLimiter:
    """请求限速器（单例）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._lock = threading.Lock()
        self._last_request_time: dict[str, float] = defaultdict(float)
        self._request_count: dict[str, int] = defaultdict(int)
        self._window_start: dict[str, float] = defaultdict(time.time)

        # 默认配置
        self.default_delay = 1.0
        self.default_random_delay = 0.5
        self.max_requests_per_minute = 60

        self._initialized = True

    def wait(self, domain: Optional[str] = None):
        """
        等待直到可以发送请求

        Args:
            domain: 域名，用于针对不同域名限速
        """
        domain = domain or "default"

        with self._lock:
            current_time = time.time()

            # 检查每分钟请求限制
            if current_time - self._window_start[domain] >= 60:
                self._request_count[domain] = 0
                self._window_start[domain] = current_time

            if self._request_count[domain] >= self.max_requests_per_minute:
                wait_time = 60 - (current_time - self._window_start[domain])
                if wait_time > 0:
                    logger.warning(f"达到每分钟请求限制，等待 {wait_time:.2f} 秒")
                    time.sleep(wait_time)
                    self._request_count[domain] = 0
                    self._window_start[domain] = time.time()

            # 计算延迟时间
            elapsed = current_time - self._last_request_time[domain]
            delay = self.default_delay + random.uniform(0, self.default_random_delay)

            if elapsed < delay:
                sleep_time = delay - elapsed
                logger.debug(f"请求限速，等待 {sleep_time:.2f} 秒")
                time.sleep(sleep_time)

            # 更新统计
            self._last_request_time[domain] = time.time()
            self._request_count[domain] += 1

    def set_delay(self, delay: float, random_delay: float = 0.5):
        """设置延迟参数"""
        self.default_delay = delay
        self.default_random_delay = random_delay

    def set_max_requests_per_minute(self, max_requests: int):
        """设置每分钟最大请求数"""
        self.max_requests_per_minute = max_requests

    def get_stats(self) -> dict:
        """获取请求统计"""
        return {
            "request_count": dict(self._request_count),
            "last_request_time": dict(self._last_request_time),
        }

    def reset(self, domain: Optional[str] = None):
        """重置统计"""
        if domain:
            self._request_count[domain] = 0
            self._last_request_time[domain] = 0
        else:
            self._request_count.clear()
            self._last_request_time.clear()


# 全局实例
rate_limiter = RateLimiter()
