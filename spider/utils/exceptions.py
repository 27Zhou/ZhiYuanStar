"""
统一异常处理模块
"""


class SpiderException(Exception):
    """爬虫基础异常"""

    def __init__(self, message: str = "爬虫异常", code: int = 1000):
        self.message = message
        self.code = code
        super().__init__(self.message)


class RequestException(SpiderException):
    """请求异常"""

    def __init__(self, message: str = "请求失败", url: str = ""):
        self.url = url
        super().__init__(message=f"{message}: {url}", code=1001)


class ParseException(SpiderException):
    """解析异常"""

    def __init__(self, message: str = "解析失败"):
        super().__init__(message=message, code=1002)


class DatabaseException(SpiderException):
    """数据库异常"""

    def __init__(self, message: str = "数据库操作失败"):
        super().__init__(message=message, code=1003)


class RateLimitException(SpiderException):
    """限速异常"""

    def __init__(self, message: str = "请求频率超限"):
        super().__init__(message=message, code=1004)


class RetryException(SpiderException):
    """重试异常"""

    def __init__(self, message: str = "重试次数已耗尽", retries: int = 0):
        self.retries = retries
        super().__init__(message=f"{message}，已重试{retries}次", code=1005)


class ConfigException(SpiderException):
    """配置异常"""

    def __init__(self, message: str = "配置错误"):
        super().__init__(message=message, code=1006)


class DataCleanException(SpiderException):
    """数据清洗异常"""

    def __init__(self, message: str = "数据清洗失败"):
        super().__init__(message=message, code=1007)
