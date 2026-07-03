"""
录取数据管道
负责录取数据的MySQL存储、去重、自动更新
"""
from typing import List, Dict, Any, Optional

from pipeline.base import BasePipeline
from utils.logger import logger
from utils.exceptions import DatabaseException
from config.config import config

import pymysql


class AdmissionPipeline(BasePipeline):
    """录取数据管道"""

    def __init__(self, name: str = "admission_pipeline"):
        super().__init__(name)
        self._connection: Optional[pymysql.Connection] = None
        # 缓存school_id和major_id的映射
        self._school_id_cache: Dict[str, int] = {}
        self._major_id_cache: Dict[str, int] = {}
        # 已存在的唯一键缓存（用于去重）
        self._existing_keys: set = set()
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
            self.logger.info("录取数据管道数据库连接成功")
        except Exception as e:
            self.logger.error(f"录取数据管道数据库连接失败: {e}")
            raise DatabaseException(f"数据库连接失败: {e}")

    def _ensure_connection(self):
        """确保数据库连接有效"""
        try:
            self._connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def _load_existing(self):
        """加载已存在的数据（用于去重）"""
        try:
            self._ensure_connection()
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 加载学校ID映射
                cursor.execute("SELECT id, name FROM school WHERE deleted = 0")
                for row in cursor.fetchall():
                    self._school_id_cache[row["name"]] = row["id"]

                # 加载专业ID映射
                cursor.execute("SELECT id, name FROM major WHERE deleted = 0")
                for row in cursor.fetchall():
                    self._major_id_cache[row["name"]] = row["id"]

                # 加载已存在的录取数据唯一键
                cursor.execute(
                    "SELECT school_id, major_id, year, province_id, subject_type, batch FROM admission_score"
                )
                for row in cursor.fetchall():
                    key = self._make_unique_key(
                        row["school_id"],
                        row.get("major_id"),
                        row["year"],
                        row["province_id"],
                        row["subject_type"],
                        row.get("batch", ""),
                    )
                    self._existing_keys.add(key)

            self.logger.info(
                f"已加载 {len(self._school_id_cache)} 所学校，"
                f"{len(self._major_id_cache)} 个专业，"
                f"{len(self._existing_keys)} 条录取数据"
            )
        except Exception as e:
            self.logger.warning(f"加载已有数据失败: {e}")

    def _make_unique_key(
        self,
        school_id: int,
        major_id: Optional[int],
        year: int,
        province_id: int,
        subject_type: int,
        batch: str,
    ) -> str:
        """生成唯一键"""
        return f"{school_id}_{major_id or 0}_{year}_{province_id}_{subject_type}_{batch}"

    def _resolve_school_id(self, school_name: str) -> Optional[int]:
        """通过学校名称查找school_id"""
        if school_name in self._school_id_cache:
            return self._school_id_cache[school_name]

        try:
            self._ensure_connection()
            with self._connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM school WHERE name = %s AND deleted = 0 LIMIT 1",
                    (school_name,),
                )
                row = cursor.fetchone()
                if row:
                    self._school_id_cache[school_name] = row[0]
                    return row[0]
        except Exception as e:
            self.logger.warning(f"查找学校ID失败: {school_name} - {e}")

        return None

    def _resolve_major_id(self, major_name: str) -> Optional[int]:
        """通过专业名称查找major_id"""
        if not major_name:
            return None

        if major_name in self._major_id_cache:
            return self._major_id_cache[major_name]

        try:
            self._ensure_connection()
            with self._connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM major WHERE name = %s AND deleted = 0 LIMIT 1",
                    (major_name,),
                )
                row = cursor.fetchone()
                if row:
                    self._major_id_cache[major_name] = row[0]
                    return row[0]
        except Exception as e:
            self.logger.warning(f"查找专业ID失败: {major_name} - {e}")

        return None

    def save_score(self, score: Dict[str, Any]) -> bool:
        """
        保存单条录取数据

        Args:
            score: 录取数据字典

        Returns:
            是否保存成功
        """
        school_name = score.get("school_name")
        if not school_name:
            return False

        # 解析school_id
        school_id = self._resolve_school_id(school_name)
        if not school_id:
            self.logger.debug(f"未找到学校: {school_name}，跳过")
            return False

        # 解析major_id
        major_id = self._resolve_major_id(score.get("major_name"))

        # 构建入库数据
        save_data = {
            "school_id": school_id,
            "major_id": major_id,
            "year": score.get("year"),
            "province_id": score.get("province_id"),
            "subject_type": score.get("subject_type"),
            "batch": score.get("batch"),
            "min_score": score.get("min_score"),
            "max_score": score.get("max_score"),
            "avg_score": score.get("avg_score"),
            "min_ranking": score.get("min_ranking"),
            "plan_count": score.get("plan_count"),
            "enroll_count": score.get("enroll_count"),
        }

        # 去重检查
        unique_key = self._make_unique_key(
            school_id, major_id,
            save_data["year"], save_data["province_id"],
            save_data["subject_type"], save_data.get("batch", ""),
        )

        if unique_key in self._existing_keys:
            # 已存在则更新
            if self._update_score(save_data, unique_key):
                return True
            return False

        self._buffer.append(save_data)
        self._existing_keys.add(unique_key)

        if len(self._buffer) >= self.batch_size:
            return self.flush()
        return True

    def _update_score(self, score: Dict[str, Any], unique_key: str) -> bool:
        """更新已存在的录取数据"""
        try:
            self._ensure_connection()
            sql = """
                UPDATE admission_score SET
                    min_score = %s, max_score = %s, avg_score = %s,
                    min_ranking = %s, plan_count = %s, enroll_count = %s
                WHERE school_id = %s AND IFNULL(major_id, 0) = %s
                    AND year = %s AND province_id = %s AND subject_type = %s
                    AND IFNULL(batch, '') = %s
            """
            params = (
                score.get("min_score"), score.get("max_score"), score.get("avg_score"),
                score.get("min_ranking"), score.get("plan_count"), score.get("enroll_count"),
                score["school_id"], score.get("major_id") or 0,
                score["year"], score["province_id"], score["subject_type"],
                score.get("batch") or "",
            )

            with self._connection.cursor() as cursor:
                cursor.execute(sql, params)
            self._connection.commit()
            return True
        except Exception as e:
            self.logger.warning(f"更新录取数据失败: {e}")
            try:
                self._connection.rollback()
            except Exception:
                pass
            return False

    def save(self, item: Dict[str, Any]) -> bool:
        """保存单条数据（基类要求）"""
        return self.save_score(item)

    def save_batch(self, items: List[Dict[str, Any]]) -> int:
        """批量保存录取数据"""
        if not items:
            return 0

        try:
            self._ensure_connection()

            fields = list(items[0].keys())
            field_str = ', '.join(f'`{k}`' for k in fields)
            placeholders = ', '.join(['%s'] * len(fields))

            sql = f"INSERT INTO `admission_score` ({field_str}) VALUES ({placeholders})"
            update_parts = []
            for k in fields:
                if k not in ("school_id", "major_id", "year", "province_id", "subject_type", "batch"):
                    update_parts.append(f"`{k}` = VALUES(`{k}`)")
            if update_parts:
                sql += " ON DUPLICATE KEY UPDATE " + ", ".join(update_parts)

            count = 0
            with self._connection.cursor() as cursor:
                for item in items:
                    try:
                        values = [item.get(k) for k in fields]
                        cursor.execute(sql, values)
                        count += 1
                    except Exception as e:
                        self.logger.warning(f"保存录取数据失败: {e}")

            self._connection.commit()
            self.logger.info(f"批量保存 {count}/{len(items)} 条录取数据到数据库")
            return count

        except Exception as e:
            self.logger.error(f"批量保存录取数据失败: {e}")
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
                self.logger.info("录取数据管道数据库连接已关闭")
            except Exception:
                pass
