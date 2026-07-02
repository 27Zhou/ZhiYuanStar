"""
爬虫基类
所有爬虫必须继承此类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils.logger import logger
from utils.http_client import http_client
from utils.retry import retry, RetryHandler
from utils.data_cleaner import data_cleaner
from utils.exceptions import SpiderException, ParseException
from config.config import config


class BaseCrawler(ABC):
    """爬虫基类"""

    def __init__(self, name: str = "base_crawler"):
        """
        初始化爬虫

        Args:
            name: 爬虫名称
        """
        self.name = name
        self.http = http_client
        self.cleaner = data_cleaner
        self.logger = logger
        self.config = config

        # 统计信息
        self.stats = {
            "total_requests": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "total_items": 0,
            "start_time": None,
            "end_time": None,
        }

    @abstractmethod
    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """
        执行爬取（子类必须实现）

        Returns:
            爬取的数据列表
        """
        pass

    @abstractmethod
    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """
        解析内容（子类必须实现）

        Args:
            content: HTML内容
            **kwargs: 其他参数

        Returns:
            解析后的数据列表
        """
        pass

    def fetch_page(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        encoding: Optional[str] = None,
    ) -> Optional[str]:
        """
        获取页面内容

        Args:
            url: 页面URL
            params: 查询参数
            headers: 自定义请求头
            encoding: 页面编码

        Returns:
            页面HTML内容，失败返回None
        """
        try:
            self.stats["total_requests"] += 1

            response = self.http.get(
                url=url,
                params=params,
                headers=headers,
            )

            # 设置编码
            if encoding:
                response.encoding = encoding
            elif response.apparent_encoding:
                response.encoding = response.apparent_encoding

            self.stats["success_requests"] += 1
            return response.text

        except Exception as e:
            self.stats["failed_requests"] += 1
            self.logger.error(f"获取页面失败: {url} - {e}")
            return None

    def fetch_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        获取JSON数据

        Args:
            url: API地址
            params: 查询参数
            headers: 自定义请求头

        Returns:
            JSON数据，失败返回None
        """
        try:
            self.stats["total_requests"] += 1

            response = self.http.get(
                url=url,
                params=params,
                headers=headers,
            )

            self.stats["success_requests"] += 1
            return response.json()

        except Exception as e:
            self.stats["failed_requests"] += 1
            self.logger.error(f"获取JSON失败: {url} - {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        解析HTML

        Args:
            html: HTML内容

        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(html, 'lxml')

    def extract_text(self, element, default: str = "") -> str:
        """
        提取元素文本

        Args:
            element: BeautifulSoup元素
            default: 默认值

        Returns:
            文本内容
        """
        if element:
            return element.get_text(strip=True)
        return default

    def extract_attr(self, element, attr: str, default: str = "") -> str:
        """
        提取元素属性

        Args:
            element: BeautifulSoup元素
            attr: 属性名
            default: 默认值

        Returns:
            属性值
        """
        if element:
            return element.get(attr, default)
        return default

    def start(self, **kwargs):
        """
        启动爬虫
        """
        self.logger.info(f"爬虫 [{self.name}] 开始运行")
        self.stats["start_time"] = datetime.now()

        try:
            data = self.crawl(**kwargs)
            self.stats["total_items"] = len(data)
            self.logger.info(f"爬虫 [{self.name}] 完成，共获取 {len(data)} 条数据")
            return data
        except Exception as e:
            self.logger.error(f"爬虫 [{self.name}] 运行失败: {e}")
            raise SpiderException(f"爬虫运行失败: {e}")
        finally:
            self.stats["end_time"] = datetime.now()
            self.print_stats()

    def print_stats(self):
        """打印统计信息"""
        duration = None
        if self.stats["start_time"] and self.stats["end_time"]:
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

        self.logger.info(f"爬虫 [{self.name}] 统计:")
        self.logger.info(f"  - 总请求数: {self.stats['total_requests']}")
        self.logger.info(f"  - 成功请求数: {self.stats['success_requests']}")
        self.logger.info(f"  - 失败请求数: {self.stats['failed_requests']}")
        self.logger.info(f"  - 获取数据条数: {self.stats['total_items']}")
        if duration:
            self.logger.info(f"  - 运行时长: {duration:.2f} 秒")
