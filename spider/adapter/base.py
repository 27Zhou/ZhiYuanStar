"""
数据源适配器基类
所有数据源适配器必须继承此类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from utils.logger import logger
from utils.http_client import http_client
from utils.exceptions import SpiderException


class BaseAdapter(ABC):
    """数据源适配器基类"""

    # 适配器名称
    name: str = "base_adapter"
    # 优先级（数值越小优先级越高）
    priority: int = 100
    # 是否可用
    available: bool = True

    def __init__(self):
        self.http = http_client
        self.logger = logger

    @abstractmethod
    def fetch_school_list(self, **kwargs) -> List[Dict[str, Any]]:
        """
        获取高校列表

        Returns:
            高校数据列表
        """
        pass

    @abstractmethod
    def fetch_major_list(self, **kwargs) -> List[Dict[str, Any]]:
        """
        获取专业列表

        Returns:
            专业数据列表
        """
        pass

    @abstractmethod
    def fetch_admission_scores(self, year: int, province_id: int, **kwargs) -> List[Dict[str, Any]]:
        """
        获取录取分数线

        Args:
            year: 年份
            province_id: 省份ID

        Returns:
            录取数据列表
        """
        pass

    def check_available(self) -> bool:
        """
        检查数据源是否可用

        Returns:
            是否可用
        """
        return self.available

    def fetch_json(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """获取JSON数据"""
        try:
            response = self.http.get(url=url, params=params, enable_rate_limit=False)
            return response.json()
        except Exception as e:
            self.logger.debug(f"[{self.name}] JSON获取失败: {url} - {e}")
            return None

    def fetch_page(self, url: str, params: Optional[Dict] = None, encoding: str = "utf-8") -> Optional[str]:
        """获取HTML页面"""
        try:
            response = self.http.get(url=url, params=params, enable_rate_limit=False)
            if encoding:
                response.encoding = encoding
            return response.text
        except Exception as e:
            self.logger.debug(f"[{self.name}] 页面获取失败: {url} - {e}")
            return None
