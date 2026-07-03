"""
字段映射器
负责将CSV/Excel的字段名映射到MySQL的字段名
"""
from typing import Dict, Any, Optional, List

from utils.logger import logger


class FieldMapper:
    """字段映射器"""

    # school表字段映射
    SCHOOL_MAPPING = {
        # 数据库字段 -> 可能的源字段名列表
        "name": ["name", "学校名称", "高校名称", "院校名称", "school_name", "名称", "学校"],
        "code": ["code", "学校代码", "高校代码", "院校代码", "school_code", "代码", "编码"],
        "province_id": ["province_id", "省份ID", "province", "省份", "所在地", "所在省份"],
        "city_id": ["city_id", "城市ID", "city", "城市", "所在城市"],
        "address": ["address", "地址", "详细地址", "学校地址", "校址"],
        "type": ["type", "类型", "学校类型", "school_type", "办学类型"],
        "level": ["level", "层次", "办学层次", "school_level", "学校层次"],
        "nature": ["nature", "性质", "办学性质", "school_nature", "学校性质"],
        "is_985": ["is_985", "985", "是否985", "is985"],
        "is_211": ["is_211", "211", "是否211", "is211"],
        "is_double_first_class": ["is_double_first_class", "双一流", "是否双一流", "is_double"],
        "website": ["website", "官网", "学校官网", "official_website", "网址", "网站"],
        "description": ["description", "简介", "学校简介", "介绍", "学校介绍"],
        "ranking": ["ranking", "排名", "综合排名", "全国排名"],
        "status": ["status", "状态"],
    }

    # major表字段映射
    MAJOR_MAPPING = {
        "name": ["name", "专业名称", "专业", "major_name", "名称"],
        "code": ["code", "专业代码", "major_code", "代码", "编码"],
        "category": ["category", "专业大类", "门类", "学科门类", "所属门类"],
        "sub_category": ["sub_category", "专业小类", "专业类", "学科", "所属学科"],
        "subject_requirements": ["subject_requirements", "选科要求", "选考科目", "选科"],
        "duration": ["duration", "学制", "年限", "修业年限"],
        "degree": ["degree", "授予学位", "学位"],
        "description": ["description", "专业介绍", "简介", "介绍"],
        "employment_direction": ["employment_direction", "就业方向", "就业", "就业前景"],
        "status": ["status", "状态"],
    }

    # admission_score表字段映射
    ADMISSION_MAPPING = {
        "school_id": ["school_id", "学校ID", "高校ID"],
        "school_name": ["school_name", "学校名称", "高校名称", "院校名称", "学校"],
        "major_id": ["major_id", "专业ID"],
        "major_name": ["major_name", "专业名称", "专业"],
        "year": ["year", "年份", "年度", "录取年份"],
        "province_id": ["province_id", "省份ID", "province", "省份", "招生省份"],
        "province_name": ["province_name", "省份名称", "省份"],
        "subject_type": ["subject_type", "科类", "文理科", "类别", "文理"],
        "batch": ["batch", "批次", "录取批次"],
        "min_score": ["min_score", "最低分", "最低分数", "录取最低分"],
        "max_score": ["max_score", "最高分", "最高分数", "录取最高分"],
        "avg_score": ["avg_score", "平均分", "平均分数", "录取平均分"],
        "min_ranking": ["min_ranking", "最低位次", "位次", "排名", "最低排名"],
        "plan_count": ["plan_count", "计划招生", "招生人数", "计划数"],
        "enroll_count": ["enroll_count", "实际录取", "录取人数", "录取数"],
    }

    # enrollment_plan表字段映射
    PLAN_MAPPING = {
        "school_id": ["school_id", "学校ID", "高校ID"],
        "school_name": ["school_name", "学校名称", "高校名称", "院校名称", "学校"],
        "major_id": ["major_id", "专业ID"],
        "major_name": ["major_name", "专业名称", "专业"],
        "year": ["year", "年份", "年度"],
        "province_id": ["province_id", "省份ID", "province", "省份", "招生省份"],
        "province_name": ["province_name", "省份名称", "省份"],
        "subject_type": ["subject_type", "科类", "文理科", "类别"],
        "batch": ["batch", "批次", "录取批次"],
        "plan_count": ["plan_count", "计划招生", "招生人数", "计划数", "人数"],
        "duration": ["duration", "学制", "年限"],
        "tuition": ["tuition", "学费", "学杂费"],
        "remark": ["remark", "备注", "说明"],
    }

    # 省份名称到ID映射
    PROVINCE_MAP = {
        "北京": 1, "北京市": 1, "天津": 2, "天津市": 2, "河北": 3, "河北省": 3,
        "山西": 4, "山西省": 4, "内蒙古": 5, "内蒙古自治区": 5,
        "辽宁": 6, "辽宁省": 6, "吉林": 7, "吉林省": 7, "黑龙江": 8, "黑龙江省": 8,
        "上海": 9, "上海市": 9, "江苏": 10, "江苏省": 10, "浙江": 11, "浙江省": 11,
        "安徽": 12, "安徽省": 12, "福建": 13, "福建省": 13, "江西": 14, "江西省": 14,
        "山东": 15, "山东省": 15, "河南": 16, "河南省": 16, "湖北": 17, "湖北省": 17,
        "湖南": 18, "湖南省": 18, "广东": 19, "广东省": 19, "广西": 20, "广西壮族自治区": 20,
        "海南": 21, "海南省": 21, "重庆": 22, "重庆市": 22, "四川": 23, "四川省": 23,
        "贵州": 24, "贵州省": 24, "云南": 25, "云南省": 25, "西藏": 26, "西藏自治区": 26,
        "陕西": 27, "陕西省": 27, "甘肃": 28, "甘肃省": 28, "青海": 29, "青海省": 29,
        "宁夏": 30, "宁夏回族自治区": 30, "新疆": 31, "新疆维吾尔自治区": 31,
    }

    # 学校类型映射
    TYPE_MAP = {
        "综合": 1, "综合类": 1, "理工": 2, "理工类": 2, "师范": 3, "师范类": 3,
        "医药": 4, "医药类": 4, "财经": 5, "财经类": 5, "政法": 6, "政法类": 6,
        "农林": 7, "农林类": 7, "艺术": 8, "艺术类": 8, "体育": 9, "体育类": 9,
        "民族": 10, "民族类": 10, "军事": 11, "军事类": 11,
    }

    # 办学层次映射
    LEVEL_MAP = {"本科": 1, "专科": 2, "高职": 2}

    # 办学性质映射
    NATURE_MAP = {"公办": 1, "民办": 2, "中外合作": 3, "中外合作办学": 3}

    # 科类映射
    SUBJECT_TYPE_MAP = {
        "文科": 1, "文史": 1, "文": 1,
        "理科": 2, "理工": 2, "理": 2,
        "综合改革": 3, "综合": 3, "新高考": 3, "物理类": 3, "历史类": 3,
    }

    def __init__(self):
        self._school_id_cache: Dict[str, int] = {}
        self._major_id_cache: Dict[str, int] = {}

    def map_fields(self, data: Dict[str, Any], table: str) -> Dict[str, Any]:
        """
        映射字段名

        Args:
            data: 原始数据
            table: 目标表名

        Returns:
            映射后的数据
        """
        mapping = self._get_mapping(table)
        if not mapping:
            return data

        result = {}
        used_source_keys = set()

        # 遍历映射规则
        for db_field, source_fields in mapping.items():
            for source_field in source_fields:
                if source_field in data and source_field not in used_source_keys:
                    value = data[source_field]
                    if value is not None and str(value).strip():
                        result[db_field] = str(value).strip()
                        used_source_keys.add(source_field)
                        break

        return result

    def _get_mapping(self, table: str) -> Optional[Dict]:
        """获取表的字段映射"""
        mappings = {
            "school": self.SCHOOL_MAPPING,
            "major": self.MAJOR_MAPPING,
            "admission_score": self.ADMISSION_MAPPING,
            "enrollment_plan": self.PLAN_MAPPING,
        }
        return mappings.get(table)

    def resolve_province_id(self, value: Any) -> Optional[int]:
        """解析省份ID"""
        if value is None:
            return None

        val_str = str(value).strip()

        # 如果是数字
        if val_str.isdigit():
            pid = int(val_str)
            return pid if 1 <= pid <= 31 else None

        # 名称映射
        return self.PROVINCE_MAP.get(val_str)

    def resolve_type(self, value: Any) -> Optional[int]:
        """解析学校类型"""
        if value is None:
            return None

        val_str = str(value).strip()
        if val_str.isdigit():
            t = int(val_str)
            return t if 1 <= t <= 11 else None
        return self.TYPE_MAP.get(val_str)

    def resolve_level(self, value: Any) -> Optional[int]:
        """解析办学层次"""
        if value is None:
            return None

        val_str = str(value).strip()
        if val_str.isdigit():
            l = int(val_str)
            return l if l in (1, 2) else None
        return self.LEVEL_MAP.get(val_str)

    def resolve_nature(self, value: Any) -> Optional[int]:
        """解析办学性质"""
        if value is None:
            return None

        val_str = str(value).strip()
        if val_str.isdigit():
            n = int(val_str)
            return n if 1 <= n <= 3 else None
        return self.NATURE_MAP.get(val_str)

    def resolve_subject_type(self, value: Any) -> Optional[int]:
        """解析科类"""
        if value is None:
            return None

        val_str = str(value).strip()
        if val_str.isdigit():
            t = int(val_str)
            return t if t in (1, 2, 3) else None
        return self.SUBJECT_TYPE_MAP.get(val_str)

    def resolve_bool(self, value: Any) -> int:
        """解析布尔值"""
        if value is None:
            return 0

        val_str = str(value).strip().lower()
        if val_str in ("1", "true", "是", "yes", "y"):
            return 1
        return 0

    def set_school_id_cache(self, cache: Dict[str, int]):
        """设置学校ID缓存"""
        self._school_id_cache = cache

    def set_major_id_cache(self, cache: Dict[str, int]):
        """设置专业ID缓存"""
        self._major_id_cache = cache

    def get_school_id(self, name: str) -> Optional[int]:
        """通过名称获取学校ID"""
        return self._school_id_cache.get(name)

    def get_major_id(self, name: str) -> Optional[int]:
        """通过名称获取专业ID"""
        return self._major_id_cache.get(name)


# 全局实例
field_mapper = FieldMapper()
