"""
数据库管道
负责将数据保存到MySQL数据库
"""
from typing import List, Dict, Any, Optional

import pymysql

from pipeline.base import BasePipeline
from utils.logger import logger
from utils.exceptions import DatabaseException
from config.config import config


class DatabasePipeline(BasePipeline):
    """数据库管道"""

    def __init__(self, name: str = "db_pipeline"):
        super().__init__(name)
        self._connection: Optional[pymysql.Connection] = None
        self._connect()

    def _connect(self):
        """建立数据库连接"""
        try:
            self._connection = pymysql.connect(
                host=config.database.host,
                port=config.database.port,
                user=config.database.user,
                password=config.database.password,
                database=config.database.database,
                charset=config.database.charset,
                autocommit=True,
            )
            self.logger.info("数据库连接成功")
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            raise DatabaseException(f"数据库连接失败: {e}")

    def _ensure_connection(self):
        """确保数据库连接有效"""
        try:
            self._connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def save(self, item: Dict[str, Any], table: str) -> bool:
        """
        保存单条数据到数据库

        Args:
            item: 数据字典
            table: 表名

        Returns:
            是否保存成功
        """
        try:
            self._ensure_connection()

            fields = ', '.join(f'`{k}`' for k in item.keys())
            placeholders = ', '.join(['%s'] * len(item))
            sql = f"INSERT INTO `{table}` ({fields}) VALUES ({placeholders})"

            with self._connection.cursor() as cursor:
                cursor.execute(sql, list(item.values()))

            return True
        except Exception as e:
            self.logger.error(f"保存数据失败: {table} - {e}")
            return False

    def save_batch(self, items: List[Dict[str, Any]], table: str = "") -> int:
        """
        批量保存数据

        Args:
            items: 数据列表
            table: 表名

        Returns:
            成功保存的数量
        """
        if not items or not table:
            return 0

        try:
            self._ensure_connection()

            fields = ', '.join(f'`{k}`' for k in items[0].keys())
            placeholders = ', '.join(['%s'] * len(items[0]))
            sql = f"INSERT INTO `{table}` ({fields}) VALUES ({placeholders})"

            count = 0
            with self._connection.cursor() as cursor:
                for item in items:
                    try:
                        cursor.execute(sql, list(item.values()))
                        count += 1
                    except Exception as e:
                        self.logger.warning(f"单条数据保存失败: {e}")

            self.logger.info(f"批量保存 {count}/{len(items)} 条数据到 {table}")
            return count
        except Exception as e:
            self.logger.error(f"批量保存失败: {table} - {e}")
            return 0

    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行SQL语句

        Args:
            sql: SQL语句
            params: 参数

        Returns:
            影响的行数
        """
        try:
            self._ensure_connection()
            with self._connection.cursor() as cursor:
                return cursor.execute(sql, params)
        except Exception as e:
            self.logger.error(f"执行SQL失败: {e}")
            raise DatabaseException(f"执行SQL失败: {e}")

    def query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        查询数据

        Args:
            sql: SQL语句
            params: 参数

        Returns:
            查询结果列表
        """
        try:
            self._ensure_connection()
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"查询失败: {e}")
            raise DatabaseException(f"查询失败: {e}")

    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """查询单条数据"""
        results = self.query(sql, params)
        return results[0] if results else None

    def close(self):
        """关闭数据库连接"""
        super().close()
        if self._connection:
            try:
                self._connection.close()
                self.logger.info("数据库连接已关闭")
            except Exception:
                pass


# 全局实例
db_pipeline = DatabasePipeline()
