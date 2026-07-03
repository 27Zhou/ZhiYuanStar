"""
录取数据解析器
负责清洗和标准化录取分数线数据
"""
import re
from typing import List, Dict, Any, Optional

from parser.base import BaseParser
from utils.data_cleaner import data_cleaner


class AdmissionParser(BaseParser):
    """录取数据解析器"""

    # 省份名称到ID映射
    PROVINCE_MAP = {
        "北京": 1, "天津": 2, "河北": 3, "山西": 4, "内蒙古": 5,
        "辽宁": 6, "吉林": 7, "黑龙江": 8, "上海": 9, "江苏": 10,
        "浙江": 11, "安徽": 12, "福建": 13, "江西": 14, "山东": 15,
        "河南": 16, "湖北": 17, "湖南": 18, "广东": 19, "广西": 20,
        "海南": 21, "重庆": 22, "四川": 23, "贵州": 24, "云南": 25,
        "西藏": 26, "陕西": 27, "甘肃": 28, "青海": 29, "宁夏": 30,
        "新疆": 31,
        "北京市": 1, "天津市": 2, "河北省": 3, "山西省": 4, "内蒙古自治区": 5,
        "辽宁省": 6, "吉林省": 7, "黑龙江省": 8, "上海市": 9, "江苏省": 10,
        "浙江省": 11, "安徽省": 12, "福建省": 13, "江西省": 14, "山东省": 15,
        "河南省": 16, "湖北省": 17, "湖南省": 18, "广东省": 19, "广西壮族自治区": 20,
        "海南省": 21, "重庆市": 22, "四川省": 23, "贵州省": 24, "云南省": 25,
        "西藏自治区": 26, "陕西省": 27, "甘肃省": 28, "青海省": 29, "宁夏回族自治区": 30,
        "新疆维吾尔自治区": 31,
    }

    # 科类映射
    SUBJECT_TYPE_MAP = {
        "文科": 1, "文史": 1, "文": 1,
        "理科": 2, "理工": 2, "理": 2,
        "综合改革": 3, "综合": 3, "新高考": 3, "物理类": 3, "历史类": 3,
    }

    # 批次映射
    BATCH_NORMALIZE = {
        "一批": "本科一批", "一本": "本科一批", "本科一批": "本科一批",
        "二批": "本科二批", "二本": "本科二批", "本科二批": "本科二批",
        "提前批": "本科提前批", "本科提前批": "本科提前批",
        "本科批": "本科批", "本科": "本科批",
        "专科批": "专科批", "专科": "专科批", "高职": "专科批",
    }

    def __init__(self):
        super().__init__(name="admission_parser")

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析内容（本模块主要处理JSON，此方法备用）"""
        return []

    def parse_single(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析单条录取数据

        Args:
            raw_data: 原始数据字典

        Returns:
            清洗后的数据字典，无效数据返回None
        """
        try:
            # 学校名称（必填，用于关联school_id）
            school_name = self._extract_school_name(raw_data)
            if not school_name:
                return None

            # 年份（必填）
            year = self._extract_year(raw_data)
            if not year:
                return None

            # 省份（必填）
            province_id = self._extract_province_id(raw_data)
            if not province_id:
                return None

            # 科类（必填）
            subject_type = self._extract_subject_type(raw_data)
            if not subject_type:
                return None

            # 专业名称（可选，用于关联major_id）
            major_name = self._extract_major_name(raw_data)

            # 批次
            batch = self._extract_batch(raw_data)

            # 分数相关
            min_score = self._extract_int(raw_data, ["min_score", "lowest_score", "最低分", "最低分数"])
            max_score = self._extract_int(raw_data, ["max_score", "highest_score", "最高分", "最高分数"])
            avg_score = self._extract_float(raw_data, ["avg_score", "average_score", "平均分", "平均分数"])
            min_ranking = self._extract_int(raw_data, ["min_ranking", "ranking", "lowest_rank", "最低位次", "位次"])

            # 招生人数
            plan_count = self._extract_int(raw_data, ["plan_count", "plan_num", "计划招生", "招生人数"])
            enroll_count = self._extract_int(raw_data, ["enroll_count", "enroll_num", "实际录取", "录取人数"])

            # 校验：至少有最低分或最低位次
            if min_score is None and min_ranking is None:
                return None

            result = {
                "school_name": school_name,
                "major_name": major_name,
                "year": year,
                "province_id": province_id,
                "subject_type": subject_type,
                "batch": batch,
                "min_score": min_score,
                "max_score": max_score,
                "avg_score": avg_score,
                "min_ranking": min_ranking,
                "plan_count": plan_count,
                "enroll_count": enroll_count,
            }

            return result

        except Exception as e:
            self.logger.error(f"解析录取数据失败: {e}")
            return None

    def _extract_school_name(self, data: Dict) -> Optional[str]:
        """提取学校名称"""
        for key in ["school_name", "school", "name", "学校名称", "高校名称", "院校名称"]:
            if key in data and data[key]:
                name = str(data[key]).strip()
                name = re.sub(r'\s+', '', name)
                return name if len(name) >= 2 else None
        return None

    def _extract_major_name(self, data: Dict) -> Optional[str]:
        """提取专业名称"""
        for key in ["major_name", "major", "专业名称", "专业"]:
            if key in data and data[key]:
                name = str(data[key]).strip()
                return name if len(name) >= 2 else None
        return None

    def _extract_year(self, data: Dict) -> Optional[int]:
        """提取年份"""
        # 先从扩展字段取
        year = data.get("_year")
        if year:
            return data_cleaner.clean_year(year)

        for key in ["year", "年份"]:
            if key in data and data[key]:
                return data_cleaner.clean_year(data[key])
        return None

    def _extract_province_id(self, data: Dict) -> Optional[int]:
        """提取省份ID"""
        # 先从扩展字段取
        pid = data.get("_province_id")
        if pid and isinstance(pid, int):
            return pid

        # 尝试从省份名称获取
        for key in ["province", "province_name", "省份", "招生省份"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                if val.isdigit():
                    return int(val)
                return self.PROVINCE_MAP.get(val)
        return None

    def _extract_subject_type(self, data: Dict) -> Optional[int]:
        """提取科类"""
        for key in ["subject_type", "subject", "category_type", "科类", "文理科"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                if val.isdigit():
                    t = int(val)
                    return t if t in (1, 2, 3) else None
                return self.SUBJECT_TYPE_MAP.get(val)
        return None

    def _extract_batch(self, data: Dict) -> Optional[str]:
        """提取批次"""
        for key in ["batch", "batch_name", "批次"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                return self.BATCH_NORMALIZE.get(val, val)
        return None

    def _extract_int(self, data: Dict, keys: List[str]) -> Optional[int]:
        """提取整数值"""
        for key in keys:
            if key in data and data[key]:
                val = data_cleaner.clean_integer(data[key])
                if val is not None:
                    return val
        return None

    def _extract_float(self, data: Dict, keys: List[str]) -> Optional[float]:
        """提取浮点值"""
        for key in keys:
            if key in data and data[key]:
                val = data_cleaner.clean_float(data[key])
                if val is not None:
                    return val
        return None
