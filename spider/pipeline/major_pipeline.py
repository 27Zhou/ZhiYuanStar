"""
专业数据管道
负责专业数据的MySQL存储、重复检测
"""
from typing import List, Dict, Any, Optional

from pipeline.base import BasePipeline
from utils.logger import logger
from utils.exceptions import DatabaseException
from config.config import config

import pymysql


class MajorPipeline(BasePipeline):
    """专业数据管道"""

    def __init__(self, name: str = "major_pipeline"):
        super().__init__(name)
        self._connection: Optional[pymysql.Connection] = None
        self._existing_codes: set = set()
        self._existing_names: set = set()
        self.batch_size = 50
        self._connect()
        self._load_existing()

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
                autocommit=False,
            )
            self.logger.info("专业管道数据库连接成功")
        except Exception as e:
            self.logger.error(f"专业管道数据库连接失败: {e}")
            raise DatabaseException(f"数据库连接失败: {e}")

    def _ensure_connection(self):
        """确保数据库连接有效"""
        try:
            self._connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def _load_existing(self):
        """加载已存在的专业数据（用于重复检测）"""
        try:
            self._ensure_connection()
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT code, name FROM major WHERE deleted = 0")
                rows = cursor.fetchall()
                for row in rows:
                    if row.get("code"):
                        self._existing_codes.add(row["code"])
                    if row.get("name"):
                        self._existing_names.add(row["name"])

            self.logger.info(f"已加载 {len(self._existing_codes)} 个专业代码，{len(self._existing_names)} 个专业名称")
        except Exception as e:
            self.logger.warning(f"加载已有专业数据失败: {e}")

    def is_duplicate(self, major: Dict[str, Any]) -> bool:
        """检测是否重复"""
        code = major.get("code", "")
        name = major.get("name", "")

        if code and code in self._existing_codes:
            return True
        if name and name in self._existing_names:
            return True
        return False

    def save_major(self, major: Dict[str, Any]) -> bool:
        """保存单条专业数据"""
        if self.is_duplicate(major):
            self.logger.debug(f"跳过重复专业: {major.get('name')}")
            return False

        save_data = {k: v for k, v in major.items() if not k.startswith("_")}
        self._buffer.append(save_data)

        if save_data.get("code"):
            self._existing_codes.add(save_data["code"])
        if save_data.get("name"):
            self._existing_names.add(save_data["name"])

        if len(self._buffer) >= self.batch_size:
            return self.flush()
        return True

    def save(self, item: Dict[str, Any]) -> bool:
        """保存单条数据（基类要求）"""
        return self.save_major(item)

    def save_batch(self, items: List[Dict[str, Any]]) -> int:
        """批量保存专业数据"""
        if not items:
            return 0

        try:
            self._ensure_connection()

            fields = list(items[0].keys())
            field_str = ', '.join(f'`{k}`' for k in fields)
            placeholders = ', '.join(['%s'] * len(fields))

            sql = f"INSERT IGNORE INTO `major` ({field_str}) VALUES ({placeholders})"

            count = 0
            with self._connection.cursor() as cursor:
                for item in items:
                    try:
                        values = [item.get(k) for k in fields]
                        affected = cursor.execute(sql, values)
                        if affected > 0:
                            count += 1
                    except Exception as e:
                        self.logger.warning(f"保存专业数据失败: {item.get('name', '未知')} - {e}")

            self._connection.commit()
            self.logger.info(f"批量保存 {count}/{len(items)} 个专业到数据库")
            return count

        except Exception as e:
            self.logger.error(f"批量保存专业数据失败: {e}")
            try:
                self._connection.rollback()
            except Exception:
                pass
            return 0

    def flush(self) -> bool:
        """刷新缓冲区"""
        if not self._buffer:
            return True

        try:
            count = self.save_batch(self._buffer)
            self._buffer.clear()
            return count > 0
        except Exception as e:
            self.logger.error(f"刷新缓冲区失败: {e}")
            return False

    def close(self):
        """关闭数据库连接"""
        super().close()
        if self._connection:
            try:
                self._connection.close()
                self.logger.info("专业管道数据库连接已关闭")
            except Exception:
                pass
