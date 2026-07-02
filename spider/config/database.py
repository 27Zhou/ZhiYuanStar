"""
数据库配置模块
"""
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "gaokao_ai"
    charset: str = "utf8mb4"
    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 3600

    @property
    def url(self) -> str:
        """获取SQLAlchemy连接URL"""
        return (
            f"mysql+pymysql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            f"?charset={self.charset}"
        )

    @property
    def connect_args(self) -> dict:
        """获取pymysql连接参数"""
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "charset": self.charset,
        }
