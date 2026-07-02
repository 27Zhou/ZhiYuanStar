"""
数据管道基类
负责数据的保存和持久化
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from utils.logger import logger


class BasePipeline(ABC):
    """数据管道基类"""

    def __init__(self, name: str = "base_pipeline"):
        self.name = name
        self.logger = logger
        self._buffer: List[Dict[str, Any]] = []
        self.batch_size = 100

    @abstractmethod
    def save(self, item: Dict[str, Any]) -> bool:
        """
        保存单条数据（子类必须实现）

        Args:
            item: 数据字典

        Returns:
            是否保存成功
        """
        pass

    @abstractmethod
    def save_batch(self, items: List[Dict[str, Any]]) -> int:
        """
        批量保存数据（子类必须实现）

        Args:
            items: 数据列表

        Returns:
            成功保存的数量
        """
        pass

    def process(self, item: Dict[str, Any]) -> bool:
        """
        处理单条数据（带缓冲）

        Args:
            item: 数据字典

        Returns:
            是否处理成功
        """
        self._buffer.append(item)

        if len(self._buffer) >= self.batch_size:
            return self.flush()
        return True

    def flush(self) -> bool:
        """刷新缓冲区"""
        if not self._buffer:
            return True

        try:
            count = self.save_batch(self._buffer)
            self.logger.info(f"批量保存 {count}/{len(self._buffer)} 条数据")
            self._buffer.clear()
            return count > 0
        except Exception as e:
            self.logger.error(f"刷新缓冲区失败: {e}")
            return False

    def close(self):
        """关闭管道（刷新剩余数据）"""
        self.flush()
        self.logger.info(f"管道 [{self.name}] 已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
