"""
适配器注册表
负责管理和调度多个数据源适配器，支持自动切换
"""
from typing import List, Dict, Any, Optional, Type

from adapter.base import BaseAdapter
from utils.logger import logger


class AdapterRegistry:
    """适配器注册表（单例）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._adapters: Dict[str, List[BaseAdapter]] = {}
        self._initialized = True

    def register(self, data_type: str, adapter: BaseAdapter):
        """
        注册适配器

        Args:
            data_type: 数据类型（school/major/admission）
            adapter: 适配器实例
        """
        if data_type not in self._adapters:
            self._adapters[data_type] = []

        self._adapters[data_type].append(adapter)
        # 按优先级排序
        self._adapters[data_type].sort(key=lambda a: a.priority)
        logger.debug(f"注册适配器 [{adapter.name}] -> {data_type}，优先级: {adapter.priority}")

    def get_adapter(self, data_type: str) -> Optional[BaseAdapter]:
        """
        获取可用的适配器（按优先级）

        Args:
            data_type: 数据类型

        Returns:
            可用的适配器，无可用返回None
        """
        adapters = self._adapters.get(data_type, [])
        for adapter in adapters:
            if adapter.check_available():
                return adapter
        return None

    def get_all_adapters(self, data_type: str) -> List[BaseAdapter]:
        """获取指定类型的所有适配器"""
        return self._adapters.get(data_type, [])

    def execute(self, data_type: str, method: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行数据采集（自动切换数据源）

        Args:
            data_type: 数据类型（school/major/admission）
            method: 方法名（fetch_school_list/fetch_major_list/fetch_admission_scores）
            **kwargs: 方法参数

        Returns:
            数据列表
        """
        adapters = self._adapters.get(data_type, [])

        for adapter in adapters:
            if not adapter.check_available():
                logger.debug(f"跳过不可用的适配器: {adapter.name}")
                continue

            try:
                logger.info(f"尝试数据源: {adapter.name}")
                func = getattr(adapter, method, None)
                if not func:
                    continue

                result = func(**kwargs)
                if result:
                    logger.info(f"数据源 {adapter.name} 获取到 {len(result)} 条数据")
                    return result
                else:
                    logger.warning(f"数据源 {adapter.name} 返回空数据")

            except Exception as e:
                logger.warning(f"数据源 {adapter.name} 失败: {e}")
                adapter.available = False

        logger.error(f"所有数据源均不可用: {data_type}")
        return []

    def reset_all(self):
        """重置所有适配器状态"""
        for adapters in self._adapters.values():
            for adapter in adapters:
                adapter.available = True
        logger.info("已重置所有适配器状态")


# 全局实例
adapter_registry = AdapterRegistry()
