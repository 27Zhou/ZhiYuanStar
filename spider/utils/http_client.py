"""
HTTP请求封装模块
提供统一的HTTP请求接口
"""
import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse

from utils.logger import logger
from utils.user_agent import ua_pool
from utils.rate_limiter import rate_limiter
from utils.exceptions import RequestException
from config.config import config


class HttpClient:
    """HTTP客户端（单例）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.session = requests.Session()
        self._setup_session()
        self._initialized = True

    def _setup_session(self):
        """配置Session"""
        retry_strategy = Retry(
            total=config.spider.max_retries,
            backoff_factor=config.spider.retry_backoff,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20,
        )

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(config.spider.default_headers)

    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """准备请求头"""
        final_headers = {}
        if config.spider.random_user_agent:
            final_headers["User-Agent"] = ua_pool.get_random()
        if headers:
            final_headers.update(headers)
        return final_headers

    def _prepare_proxies(self, proxies: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """准备代理配置"""
        if proxies:
            return proxies
        if config.spider.enable_proxy and config.spider.proxy_list:
            import random
            proxy = random.choice(config.spider.proxy_list)
            return {"http": proxy, "https": proxy}
        return None

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        enable_rate_limit: bool = True,
        **kwargs,
    ) -> requests.Response:
        """发送GET请求"""
        return self.request(
            method="GET", url=url, params=params,
            headers=headers, proxies=proxies,
            timeout=timeout, enable_rate_limit=enable_rate_limit,
            **kwargs,
        )

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        enable_rate_limit: bool = True,
        **kwargs,
    ) -> requests.Response:
        """发送POST请求"""
        return self.request(
            method="POST", url=url, data=data, json=json,
            headers=headers, proxies=proxies,
            timeout=timeout, enable_rate_limit=enable_rate_limit,
            **kwargs,
        )

    def request(
        self,
        method: str,
        url: str,
        enable_rate_limit: bool = True,
        **kwargs,
    ) -> requests.Response:
        """发送HTTP请求"""
        try:
            if enable_rate_limit:
                domain = urlparse(url).netloc
                rate_limiter.wait(domain)

            headers = self._prepare_headers(kwargs.pop("headers", None))
            proxies = self._prepare_proxies(kwargs.pop("proxies", None))
            timeout = kwargs.pop("timeout", None) or config.spider.timeout

            logger.info(f"发送 {method} 请求: {url}")
            response = self.session.request(
                method=method, url=url,
                headers=headers, proxies=proxies,
                timeout=timeout, **kwargs,
            )
            response.raise_for_status()

            logger.info(f"请求成功: {url} - 状态码: {response.status_code}")
            return response

        except requests.exceptions.Timeout:
            raise RequestException(message="请求超时", url=url)
        except requests.exceptions.ConnectionError:
            raise RequestException(message="连接失败", url=url)
        except requests.exceptions.HTTPError as e:
            raise RequestException(
                message=f"HTTP错误: {e.response.status_code}", url=url,
            )
        except requests.exceptions.RequestException as e:
            raise RequestException(message=str(e), url=url)

    def close(self):
        """关闭Session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局实例
http_client = HttpClient()
