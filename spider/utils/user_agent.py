"""
User-Agent池模块
提供随机User-Agent
"""
import random
from typing import List

from fake_useragent import UserAgent


class UserAgentPool:
    """User-Agent池（单例）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._ua = UserAgent()
        self._pool: List[str] = []
        self._init_pool()
        self._initialized = True

    def _init_pool(self):
        """初始化UA池"""
        for _ in range(100):
            try:
                self._pool.append(self._ua.random)
            except Exception:
                continue

        # 备用UA列表
        self._fallback_ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        ]

    def get_random(self) -> str:
        """获取随机User-Agent"""
        if self._pool:
            return random.choice(self._pool)
        return random.choice(self._fallback_ua)

    def get_chrome(self) -> str:
        """获取Chrome User-Agent"""
        try:
            return self._ua.chrome
        except Exception:
            return self._fallback_ua[0]

    def get_firefox(self) -> str:
        """获取Firefox User-Agent"""
        try:
            return self._ua.firefox
        except Exception:
            return self._fallback_ua[3]

    def get_safari(self) -> str:
        """获取Safari User-Agent"""
        try:
            return self._ua.safari
        except Exception:
            return self._fallback_ua[4]

    def refresh(self):
        """刷新UA池"""
        self._pool.clear()
        self._init_pool()


# 全局实例
ua_pool = UserAgentPool()
