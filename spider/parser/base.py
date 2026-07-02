"""
解析器基类
所有解析器必须继承此类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from bs4 import BeautifulSoup, Tag

from utils.logger import logger
from utils.exceptions import ParseException


class BaseParser(ABC):
    """解析器基类"""

    def __init__(self, name: str = "base_parser"):
        self.name = name
        self.logger = logger

    @abstractmethod
    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """
        解析内容（子类必须实现）

        Args:
            content: HTML/XML内容
            **kwargs: 其他参数

        Returns:
            解析后的数据列表
        """
        pass

    def parse_html(self, html: str) -> BeautifulSoup:
        """解析HTML为BeautifulSoup对象"""
        return BeautifulSoup(html, 'lxml')

    def extract_text(self, element: Optional[Tag], default: str = "") -> str:
        """提取元素文本"""
        if element:
            return element.get_text(strip=True)
        return default

    def extract_attr(self, element: Optional[Tag], attr: str, default: str = "") -> str:
        """提取元素属性"""
        if element:
            return element.get(attr, default)
        return default

    def extract_all_text(self, elements: List[Tag]) -> List[str]:
        """提取多个元素的文本列表"""
        return [el.get_text(strip=True) for el in elements if el]

    def select_one(self, soup: BeautifulSoup, selector: str) -> Optional[Tag]:
        """CSS选择器选取单个元素"""
        try:
            return soup.select_one(selector)
        except Exception as e:
            self.logger.warning(f"CSS选择器失败: {selector} - {e}")
            return None

    def select_all(self, soup: BeautifulSoup, selector: str) -> List[Tag]:
        """CSS选择器选取多个元素"""
        try:
            return soup.select(selector)
        except Exception as e:
            self.logger.warning(f"CSS选择器失败: {selector} - {e}")
            return []

    def find(self, soup: BeautifulSoup, tag: str, attrs: Optional[Dict] = None) -> Optional[Tag]:
        """查找单个元素"""
        return soup.find(tag, attrs)

    def find_all(self, soup: BeautifulSoup, tag: str, attrs: Optional[Dict] = None) -> List[Tag]:
        """查找多个元素"""
        return soup.find_all(tag, attrs)
