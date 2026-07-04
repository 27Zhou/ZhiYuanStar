"""
批量导入器
负责将数据批量写入MySQL

核心逻辑：
- 使用 INSERT ... ON DUPLICATE KEY UPDATE 实现 UPSERT
- 不存在 → 插入（INSERT）
- 已存在 → 更新（UPDATE）
- 通过 affected_rows 区分：1=新增, 2=更新, 0=无变化
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
    inserted: int = 0      # 新增条数
    updated: int = 0        # 更新条数
    duplicated: int = 0     # 无变化条数（数据完全相同）
    failed: int = 0
    errors: List[str] = field(default_factory=list)


class BatchImporter:
    """批量导入器"""

    BATCH_SIZE = 500

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
                sql = "SELECT id, name FROM school"
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    self._school_id_cache[row["name"]] = row["id"]
                logger.info(f"[缓存] school表加载 {len(rows)} 条记录")

                sql = "SELECT id, name FROM major"
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    self._major_id_cache[row["name"]] = row["id"]
                logger.info(f"[缓存] major表加载 {len(rows)} 条记录")

            field_mapper.set_school_id_cache(self._school_id_cache)
            field_mapper.set_major_id_cache(self._major_id_cache)

        except Exception as e:
            logger.warning(f"加载缓存失败: {e}")

    def _get_update_fields(self, table: str, all_fields: List[str]) -> List[str]:
        """
        获取需要在 ON DUPLICATE KEY UPDATE 时更新的字段
        即：所有字段 去掉 唯一键字段

        Args:
            table: 表名
            all_fields: INSERT 语句中的所有字段

        Returns:
            需要更新的字段列表
        """
        # 各表的唯一键字段（不参与UPDATE）
        unique_key_fields = {
            "school": {"code"},
            "major": {"code"},
            "admission_score": {"school_id", "major_id", "year", "province_id", "subject_type", "batch"},
            "enrollment_plan": {"school_id", "major_id", "year", "province_id", "subject_type"},
        }

        keys = unique_key_fields.get(table, set())
        return [f for f in all_fields if f not in keys]

    def _do_upsert(self, cursor, table: str, item: Dict[str, Any]) -> Tuple[bool, str, int]:
        """
        执行单条 UPSERT（INSERT ... ON DUPLICATE KEY UPDATE）

        MySQL affected_rows 返回值：
          1 → 新记录插入成功
          2 → 已有记录被更新
          0 → 已有记录但值完全相同，无需更新

        Args:
            cursor: 数据库游标
            table: 目标表名
            item: 要插入/更新的数据

        Returns:
            (是否成功, 原因, affected_rows)
        """
        fields = list(item.keys())
        values = [item.get(k) for k in fields]

        # 构建 INSERT 部分
        field_str = ', '.join(f'`{k}`' for k in fields)
        placeholders = ', '.join(['%s'] * len(fields))

        # 构建 ON DUPLICATE KEY UPDATE 部分
        # 排除唯一键字段，只更新非键字段
        update_fields = self._get_update_fields(table, fields)
        if not update_fields:
            # 所有字段都是唯一键，无需更新
            update_clause = f"`{fields[0]}` = `{fields[0]}`"  # 空更新（占位）
        else:
            update_parts = [f"`{f}` = VALUES(`{f}`)" for f in update_fields]
            update_clause = ', '.join(update_parts)

        sql = f"INSERT INTO `{table}` ({field_str}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_clause}"

        try:
            logger.debug(f"[UPSERT] SQL={sql}")
            logger.debug(f"[UPSERT] 参数={values}")
            affected = cursor.execute(sql, values)
            logger.debug(f"[UPSERT] affected_rows={affected}")
            return True, "ok", affected
        except Exception as e:
            logger.warning(f"[UPSERT] Exception: {e}")
            return False, f"error: {e}", 0

    def import_data(self, data: List[Dict[str, Any]], table: str) -> ImportResult:
        """导入数据到指定表"""
        result = ImportResult()
        result.parsed = len(data)

        logger.info(f"[导入] 表: {table}, 原始数据: {len(data)} 条")

        if not data:
            return result

        self._connect()
        self._load_caches()

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
        for idx, item in enumerate(data):
            try:
                mapped = field_mapper.map_fields(item, table)
                is_valid, cleaned, errors = processor(mapped)

                if is_valid:
                    valid_items.append(cleaned)
                else:
                    result.failed += 1
                    result.errors.extend(errors)

            except Exception as e:
                result.failed += 1
                result.errors.append(f"处理失败: {e}")

        logger.info(f"[导入] 校验完成: {len(valid_items)} 条有效, {result.failed} 条失败")

        # 批量写入
        if valid_items:
            inserted, updated, duplicated = self._batch_upsert(valid_items, table)
            result.inserted = inserted
            result.updated = updated
            result.duplicated = duplicated

        self.close()
        return result

    def _process_school(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理学校数据"""
        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid
            else:
                data.pop("province_id", None)

        if "type" in data:
            t = field_mapper.resolve_type(data["type"])
            if t:
                data["type"] = t
            else:
                data.pop("type", None)

        if "level" in data:
            l = field_mapper.resolve_level(data["level"])
            if l:
                data["level"] = l
            else:
                data.pop("level", None)

        if "nature" in data:
            n = field_mapper.resolve_nature(data["nature"])
            if n:
                data["nature"] = n
            else:
                data.pop("nature", None)

        data["is_985"] = field_mapper.resolve_bool(data.get("is_985"))
        data["is_211"] = field_mapper.resolve_bool(data.get("is_211"))
        data["is_double_first_class"] = field_mapper.resolve_bool(data.get("is_double_first_class"))

        return validator.validate_school(data)

    def _process_major(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理专业数据"""
        return validator.validate_major(data)

    def _process_admission(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理录取数据"""
        if "school_name" in data and "school_id" not in data:
            school_id = field_mapper.get_school_id(data["school_name"])
            if school_id:
                data["school_id"] = school_id

        if "major_name" in data and "major_id" not in data:
            major_id = field_mapper.get_major_id(data["major_name"])
            if major_id:
                data["major_id"] = major_id

        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid

        if "subject_type" in data:
            st = field_mapper.resolve_subject_type(data["subject_type"])
            if st:
                data["subject_type"] = st

        return validator.validate_admission(data)

    def _process_plan(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """处理招生计划数据"""
        if "school_name" in data and "school_id" not in data:
            school_id = field_mapper.get_school_id(data["school_name"])
            if school_id:
                data["school_id"] = school_id

        if "major_name" in data and "major_id" not in data:
            major_id = field_mapper.get_major_id(data["major_name"])
            if major_id:
                data["major_id"] = major_id

        if "province_id" in data:
            pid = field_mapper.resolve_province_id(data["province_id"])
            if pid:
                data["province_id"] = pid

        if "subject_type" in data:
            st = field_mapper.resolve_subject_type(data["subject_type"])
            if st:
                data["subject_type"] = st

        return validator.validate_plan(data)

    def _batch_upsert(self, items: List[Dict[str, Any]], table: str) -> Tuple[int, int, int]:
        """
        批量 UPSERT，按批次提交

        Returns:
            (新增数, 更新数, 无变化数)
        """
        total_inserted = 0
        total_updated = 0
        total_duplicated = 0

        for i in range(0, len(items), self.BATCH_SIZE):
            batch = items[i:i + self.BATCH_SIZE]
            logger.info(f"[批次] 处理 {i+1}~{min(i+self.BATCH_SIZE, len(items))}/{len(items)}")
            inserted, updated, duplicated = self._upsert_batch(batch, table)
            total_inserted += inserted
            total_updated += updated
            total_duplicated += duplicated

        return total_inserted, total_updated, total_duplicated

    def _upsert_batch(self, batch: List[Dict[str, Any]], table: str) -> Tuple[int, int, int]:
        """
        执行单批 UPSERT

        使用 INSERT ... ON DUPLICATE KEY UPDATE：
          - 不存在 → 插入（affected_rows=1）
          - 已存在且数据有变化 → 更新（affected_rows=2）
          - 已存在但数据无变化 → 跳过（affected_rows=0）

        Args:
            batch: 数据批次
            table: 表名

        Returns:
            (新增数, 更新数, 无变化数)
        """
        if not batch:
            return 0, 0, 0

        try:
            self._ensure_connection()

            # 移除非数据库字段（以_开头的扩展字段、关联名称字段）
            clean_batch = []
            for item in batch:
                clean_item = {k: v for k, v in item.items()
                             if not k.startswith("_") and k not in ("school_name", "major_name", "province_name")}
                clean_batch.append(clean_item)

            if not clean_batch:
                return 0, 0, 0

            inserted = 0
            updated = 0
            duplicated = 0
            db_errors = 0

            with self._connection.cursor() as cursor:
                for idx, item in enumerate(clean_batch):
                    item_name = item.get('name', item.get('code', f'第{idx+1}条'))

                    try:
                        success, reason, affected = self._do_upsert(cursor, table, item)

                        if not success:
                            db_errors += 1
                            logger.warning(f"[FAIL] {item_name}: {reason}")
                            continue

                        # 根据 affected_rows 判断操作类型
                        if affected == 1:
                            # 新增
                            inserted += 1
                            logger.info(f"[INSERT] 新增: {item_name}")
                        elif affected == 2:
                            # 更新
                            updated += 1
                            logger.info(f"[UPDATE] 更新: {item_name}")
                        else:
                            # affected == 0，数据完全相同，无需更新
                            duplicated += 1
                            logger.debug(f"[SKIP] 无变化: {item_name}")

                    except Exception as e:
                        db_errors += 1
                        logger.warning(f"[ERROR] {item_name}: {e}")

            # 整批提交
            try:
                self._connection.commit()
                logger.debug(f"[事务] 提交成功")
            except Exception as e:
                logger.error(f"[事务] 提交失败: {e}")
                try:
                    self._connection.rollback()
                except Exception:
                    pass

            logger.info(f"[批次完成] 新增={inserted}, 更新={updated}, 无变化={duplicated}, 错误={db_errors}")
            return inserted, updated, duplicated

        except Exception as e:
            logger.error(f"批量导入失败: {e}")
            try:
                self._connection.rollback()
            except Exception:
                pass
            return 0, 0, len(batch)

    def close(self):
        """关闭数据库连接"""
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass


# 全局实例
batch_importer = BatchImporter()
