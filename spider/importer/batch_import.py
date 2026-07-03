"""
批量导入器
负责将数据批量写入MySQL
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

import pymysql

from utils.logger import logger
from config.config import config
from importer.field_mapper import field_mapper
from importer.validator import validator


@dataclass
class ImportResult:
    """导入结果"""
    files_read: int = 0
    parsed: int = 0
    inserted: int = 0
    duplicated: int = 0
    failed: int = 0
    errors: List[str] = field(default_factory=list)


class BatchImporter:
    """批量导入器"""

    BATCH_SIZE = 500  # 每批写入数量

    def __init__(self):
        self._connection: Optional[pymysql.Connection] = None
        self._school_id_cache: Dict[str, int] = {}
        self._major_id_cache: Dict[str, int] = {}

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
            logger.info("ETL数据库连接成功")
        except Exception as e:
            logger.error(f"ETL数据库连接失败: {e}")
            raise

    def _ensure_connection(self):
        """确保连接有效"""
        try:
            self._connection.ping(reconnect=True)
        except Exception:
            self._connect()

    def _load_caches(self):
        """加载学校和专业ID缓存"""
        try:
            self._ensure_connection()
            with self._connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, name FROM school WHERE deleted = 0")
                for row in cursor.fetchall():
                    self._school_id_cache[row["name"]] = row["id"]

                cursor.execute("SELECT id, name FROM major WHERE deleted = 0")
                for row in cursor.fetchall():
                    self._major_id_cache[row["name"]] = row["id"]

            field_mapper.set_school_id_cache(self._school_id_cache)
            field_mapper.set_major_id_cache(self._major_id_cache)

            logger.info(f"缓存加载: {len(self._school_id_cache)} 所学校, {len(self._major_id_cache)} 个专业")
        except Exception as e:
            logger.warning(f"加载缓存失败: {e}")

    def import_data(self, data: List[Dict[str, Any]], table: str) -> ImportResult:
        """
        导入数据到指定表

        Args:
            data: 原始数据列表
            table: 目标表名

        Returns:
            导入结果
        """
        result = ImportResult()
        result.parsed = len(data)

        if not data:
            return result

        # 连接数据库
        self._connect()
        self._load_caches()

        # 根据表名选择处理方法
        processors = {
            "school": self._process_school,
            "major": self._process_major,
            "admission_score": self._process_admission,
            "enrollment_plan": self._process_plan,
        }

        processor = processors.get(table)
        if not processor:
            logger.error(f"不支持的表: {table}")
            result.errors.append(f"不支持的表: {table}")
            return result

        # 处理数据
        valid_items = []
        for item in data:
            try:
                # 字段映射
                mapped = field_mapper.map_fields(item, table)

                # 数据校验
                is_valid, cleaned, errors = processor(mapped)

                if is_valid:
                    valid_items.append(cleaned)
                else:
                    result.failed += 1
                    result.errors.extend(errors)

            except Exception as e:
                result.failed += 1
                result.errors.append(f"处理失败: {e}")

        # 批量写入
        if valid_items:
            inserted, duplicated = self._batch_insert(valid_items, table)
            result.inserted = inserted
            result.duplicated = duplicated

        # 关闭连接
        self.close()

        return result

    def _process_school(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理学校数据"""
        # 解析省份ID
        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid
            else:
                data.pop("province_id", None)

        # 解析类型
        if "type" in data:
            t = field_mapper.resolve_type(data["type"])
            if t:
                data["type"] = t
            else:
                data.pop("type", None)

        # 解析层次
        if "level" in data:
            l = field_mapper.resolve_level(data["level"])
            if l:
                data["level"] = l
            else:
                data.pop("level", None)

        # 解析性质
        if "nature" in data:
            n = field_mapper.resolve_nature(data["nature"])
            if n:
                data["nature"] = n
            else:
                data.pop("nature", None)

        # 解析布尔值
        data["is_985"] = field_mapper.resolve_bool(data.get("is_985"))
        data["is_211"] = field_mapper.resolve_bool(data.get("is_211"))
        data["is_double_first_class"] = field_mapper.resolve_bool(data.get("is_double_first_class"))

        return validator.validate_school(data)

    def _process_major(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理专业数据"""
        return validator.validate_major(data)

    def _process_admission(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理录取数据"""
        # 解析学校ID
        if "school_name" in data and "school_id" not in data:
            school_id = field_mapper.get_school_id(data["school_name"])
            if school_id:
                data["school_id"] = school_id

        # 解析专业ID
        if "major_name" in data and "major_id" not in data:
            major_id = field_mapper.get_major_id(data["major_name"])
            if major_id:
                data["major_id"] = major_id

        # 解析省份ID
        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid

        # 解析科类
        if "subject_type" in data:
            st = field_mapper.resolve_subject_type(data["subject_type"])
            if st:
                data["subject_type"] = st

        return validator.validate_admission(data)

    def _process_plan(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理招生计划数据"""
        # 解析学校ID
        if "school_name" in data and "school_id" not in data:
            school_id = field_mapper.get_school_id(data["school_name"])
            if school_id:
                data["school_id"] = school_id

        # 解析专业ID
        if "major_name" in data and "major_id" not in data:
            major_id = field_mapper.get_major_id(data["major_name"])
            if major_id:
                data["major_id"] = major_id

        # 解析省份ID
        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid

        # 解析科类
        if "subject_type" in data:
            st = field_mapper.resolve_subject_type(data["subject_type"])
            if st:
                data["subject_type"] = st

        return validator.validate_plan(data)

    def _batch_insert(self, items: List[Dict[str, Any]], table: str) -> Tuple[int, int]:
        """
        批量插入数据

        Args:
            items: 数据列表
            table: 表名

        Returns:
            (插入数量, 重复数量)
        """
        total_inserted = 0
        total_duplicated = 0

        # 分批处理
        for i in range(0, len(items), self.BATCH_SIZE):
            batch = items[i:i + self.BATCH_SIZE]
            inserted, duplicated = self._insert_batch(batch, table)
            total_inserted += inserted
            total_duplicated += duplicated

            if (i + self.BATCH_SIZE) % (self.BATCH_SIZE * 10) == 0:
                logger.info(f"已处理 {i + len(batch)}/{len(items)} 条数据")

        return total_inserted, total_duplicated

    def _insert_batch(self, batch: List[Dict[str, Any]], table: str) -> Tuple[int, int]:
        """
        插入单批数据

        Args:
            batch: 数据批次
            table: 表名

        Returns:
            (插入数量, 重复数量)
        """
        if not batch:
            return 0, 0

        try:
            self._ensure_connection()

            # 移除非数据库字段
            clean_batch = []
            for item in batch:
                clean_item = {k: v for k, v in item.items()
                             if not k.startswith("_") and k not in ("school_name", "major_name", "province_name")}
                clean_batch.append(clean_item)

            if not clean_batch:
                return 0, 0

            # 构建SQL
            fields = list(clean_batch[0].keys())
            field_str = ', '.join(f'`{k}`' for k in fields)
            placeholders = ', '.join(['%s'] * len(fields))

            sql = f"INSERT IGNORE INTO `{table}` ({field_str}) VALUES ({placeholders})"

            inserted = 0
            with self._connection.cursor() as cursor:
                for item in clean_batch:
                    try:
                        values = [item.get(k) for k in fields]
                        affected = cursor.execute(sql, values)
                        if affected > 0:
                            inserted += 1
                    except Exception as e:
                        logger.debug(f"插入失败: {e}")

            self._connection.commit()
            duplicated = len(clean_batch) - inserted

            return inserted, duplicated

        except Exception as e:
            logger.error(f"批量插入失败: {e}")
            try:
                self._connection.rollback()
            except Exception:
                pass
            return 0, len(batch)

    def close(self):
        """关闭数据库连接"""
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass


# 全局实例
batch_importer = BatchImporter()
