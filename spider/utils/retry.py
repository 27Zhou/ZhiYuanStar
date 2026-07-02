"""
重试机制模块
支持指数退避重试
"""
import time
import functools
from typing import Callable, Any, Tuple, Type

from utils.logger import logger
from utils.exceptions import RetryException


class RetryHandler:
    """重试处理器"""

    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
    ):
        """
        初始化重试处理器

        Args:
            max_retries: 最大重试次数
            delay: 初始延迟时间（秒）
            backoff: 退避系数
            exceptions: 需要重试的异常类型
        """
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        执行函数，失败时重试

        Args:
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数

        Returns:
            函数返回值

        Raises:
            RetryException: 重试次数耗尽
        """
        last_exception = None
        current_delay = self.delay

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                last_exception = e
                if attempt < self.max_retries:
                    logger.warning(
                        f"第 {attempt + 1} 次尝试失败: {e}, "
                        f"等待 {current_delay:.2f} 秒后重试"
                    )
                    time.sleep(current_delay)
                    current_delay *= self.backoff
                else:
                    logger.error(f"重试 {self.max_retries} 次后仍然失败: {e}")

        raise RetryException(
            message=f"重试失败: {last_exception}",
            retries=self.max_retries,
        )


def retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """
    重试装饰器

    Args:
        max_retries: 最大重试次数
        delay: 初始延迟时间（秒）
        backoff: 退避系数
        exceptions: 需要重试的异常类型
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            handler = RetryHandler(
                max_retries=max_retries,
                delay=delay,
                backoff=backoff,
                exceptions=exceptions,
            )
            return handler.execute(func, *args, **kwargs)
        return wrapper
    return decorator
