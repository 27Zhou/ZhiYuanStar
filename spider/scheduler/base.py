"""
调度器基类
负责爬虫任务的调度和管理
"""
from typing import List, Callable, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.logger import logger
from config.config import config


class BaseScheduler:
    """调度器基类"""

    def __init__(self, name: str = "base_scheduler"):
        self.name = name
        self.logger = logger
        self.max_workers = config.spider.max_workers
        self._tasks: List[Dict[str, Any]] = []
        self._results: List[Any] = []

    def add_task(self, func: Callable, *args, **kwargs):
        """
        添加任务

        Args:
            func: 任务函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        """
        self._tasks.append({
            "func": func,
            "args": args,
            "kwargs": kwargs,
        })
        self.logger.debug(f"添加任务: {func.__name__}")

    def run_sequential(self) -> List[Any]:
        """
        顺序执行所有任务

        Returns:
            任务结果列表
        """
        self.logger.info(f"开始顺序执行 {len(self._tasks)} 个任务")
        self._results = []

        for i, task in enumerate(self._tasks):
            try:
                self.logger.info(f"执行任务 {i + 1}/{len(self._tasks)}: {task['func'].__name__}")
                result = task['func'](*task['args'], **task['kwargs'])
                self._results.append(result)
            except Exception as e:
                self.logger.error(f"任务失败: {task['func'].__name__} - {e}")
                self._results.append(None)

        self.logger.info(f"所有任务执行完成，成功: {sum(1 for r in self._results if r is not None)}/{len(self._tasks)}")
        return self._results

    def run_parallel(self) -> List[Any]:
        """
        并行执行所有任务

        Returns:
            任务结果列表
        """
        self.logger.info(f"开始并行执行 {len(self._tasks)} 个任务（最大并发: {self.max_workers}）")
        self._results = [None] * len(self._tasks)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {}
            for i, task in enumerate(self._tasks):
                future = executor.submit(task['func'], *task['args'], **task['kwargs'])
                future_to_index[future] = i

            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    self._results[index] = result
                    self.logger.info(f"任务 {index + 1} 完成")
                except Exception as e:
                    self.logger.error(f"任务 {index + 1} 失败: {e}")

        success_count = sum(1 for r in self._results if r is not None)
        self.logger.info(f"所有任务执行完成，成功: {success_count}/{len(self._tasks)}")
        return self._results

    def clear(self):
        """清空任务列表"""
        self._tasks.clear()
        self._results.clear()

    def get_results(self) -> List[Any]:
        """获取执行结果"""
        return self._results
