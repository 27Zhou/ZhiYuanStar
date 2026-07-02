"""
高校数据管道
负责高校数据的MySQL存储、重复检测
"""
from typing import List, Dict, Any, Optional

from pipeline.base import BasePipeline
from utils.logger import logger
from utils.exceptions import DatabaseException
from config.config import config

import pymysql


class SchoolPipeline(BasePipeline):
    """高校数据管道"""

    def __init__(self, name: str = "school_pipeline"):
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
            self.logger.info("高校管道数据库连接成功")
        except Exception as e:
            self.logger.error(f"高校管道数据库连接失败: {e}")
            raise DatabaseException(f"数据库连接失败: {e}")

    def _ensure_connection(self):
        """确保数据库连接有效"""
        try:
            self._connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def _load_existing(self):
        """加载已存在的高校数据（用于重复检测）"""
        try:
            self._ensure_connection()
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT code, name FROM school WHERE deleted = 0")
                rows = cursor.fetchall()
                for row in rows:
                    if row.get("code"):
                        self._existing_codes.add(row["code"])
                    if row.get("name"):
                        self._existing_names.add(row["name"])

            self.logger.info(f"已加载 {len(self._existing_codes)} 个高校代码，{len(self._existing_names)} 个高校名称")
        except Exception as e:
            self.logger.warning(f"加载已有高校数据失败: {e}")

    def is_duplicate(self, school: Dict[str, Any]) -> bool:
        """
        检测是否重复

        Args:
            school: 高校数据

        Returns:
            是否重复
        """
        code = school.get("code", "")
        name = school.get("name", "")

        if code and code in self._existing_codes:
            return True

        if name and name in self._existing_names:
            return True

        return False

    def save_school(self, school: Dict[str, Any]) -> bool:
        """
        保存单条高校数据

        Args:
            school: 高校数据字典

        Returns:
            是否保存成功
        """
        # 重复检测
        if self.is_duplicate(school):
            self.logger.debug(f"跳过重复高校: {school.get('name')}")
            return False

        # 移除扩展字段
        save_data = {k: v for k, v in school.items() if not k.startswith("_")}

        self._buffer.append(save_data)

        # 更新已存在集合
        if save_data.get("code"):
            self._existing_codes.add(save_data["code"])
        if save_data.get("name"):
            self._existing_names.add(save_data["name"])

        # 达到批量大小时自动保存
        if len(self._buffer) >= self.batch_size:
            return self.flush()

        return True

    def save(self, item: Dict[str, Any]) -> bool:
        """保存单条数据（基类要求）"""
        return self.save_school(item)

    def save_batch(self, items: List[Dict[str, Any]]) -> int:
        """
        批量保存高校数据

        Args:
            items: 高校数据列表

        Returns:
            成功保存数量
        """
        if not items:
            return 0

        try:
            self._ensure_connection()

            # 获取字段列表
            fields = list(items[0].keys())
            field_str = ', '.join(f'`{k}`' for k in fields)
            placeholders = ', '.join(['%s'] * len(fields))

            # 使用 INSERT IGNORE 避免重复插入
            sql = f"INSERT IGNORE INTO `school` ({field_str}) VALUES ({placeholders})"

            count = 0
            with self._connection.cursor() as cursor:
                for item in items:
                    try:
                        values = [item.get(k) for k in fields]
                        affected = cursor.execute(sql, values)
                        if affected > 0:
                            count += 1
                    except Exception as e:
                        self.logger.warning(f"保存高校数据失败: {item.get('name', '未知')} - {e}")

            self._connection.commit()
            self.logger.info(f"批量保存 {count}/{len(items)} 所高校到数据库")
            return count

        except Exception as e:
            self.logger.error(f"批量保存高校数据失败: {e}")
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

    def get_existing_count(self) -> int:
        """获取已存在的高校数量"""
        try:
            self._ensure_connection()
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM school WHERE deleted = 0")
                return cursor.fetchone()[0]
        except Exception as e:
            self.logger.error(f"查询高校数量失败: {e}")
            return 0

    def close(self):
        """关闭数据库连接"""
        super().close()
        if self._connection:
            try:
                self._connection.close()
                self.logger.info("高校管道数据库连接已关闭")
            except Exception:
                pass
