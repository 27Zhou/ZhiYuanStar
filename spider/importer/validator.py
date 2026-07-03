"""
数据校验器
负责数据清洗、校验和补全
"""
import re
from typing import Dict, Any, Optional, List, Tuple

from utils.logger import logger


class Validator:
    """数据校验器"""

    def validate_school(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        校验学校数据

        Args:
            data: 学校数据

        Returns:
            (是否有效, 清洗后数据, 错误列表)
        """
        errors = []
        cleaned = {}

        # 学校名称（必填）
        name = self._clean_string(data.get("name"))
        if not name or len(name) < 2:
            errors.append("学校名称为空或过短")
        else:
            cleaned["name"] = name

        # 学校代码（必填）
        code = self._clean_string(data.get("code"))
        if not code:
            errors.append("学校代码为空")
        else:
            cleaned["code"] = code

        # 省份ID
        province_id = data.get("province_id")
        if province_id is not None:
            cleaned["province_id"] = self._clean_int(province_id)

        # 城市ID
        city_id = data.get("city_id")
        if city_id is not None:
            cleaned["city_id"] = self._clean_int(city_id)

        # 地址
        address = self._clean_string(data.get("address"))
        if address:
            cleaned["address"] = address

        # 类型
        type_val = data.get("type")
        if type_val is not None:
            cleaned["type"] = self._clean_int(type_val)

        # 层次
        level = data.get("level")
        if level is not None:
            cleaned["level"] = self._clean_int(level)

        # 性质
        nature = data.get("nature")
        if nature is not None:
            cleaned["nature"] = self._clean_int(nature)

        # 985/211/双一流
        cleaned["is_985"] = self._clean_bool(data.get("is_985"))
        cleaned["is_211"] = self._clean_bool(data.get("is_211"))
        cleaned["is_double_first_class"] = self._clean_bool(data.get("is_double_first_class"))

        # 官网
        website = self._clean_url(data.get("website"))
        if website:
            cleaned["website"] = website

        # 简介
        description = self._clean_string(data.get("description"))
        if description:
            cleaned["description"] = description

        # 排名
        ranking = data.get("ranking")
        if ranking is not None:
            cleaned["ranking"] = self._clean_int(ranking)

        # 状态
        cleaned["status"] = 1

        return len(errors) == 0, cleaned, errors

    def validate_major(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        校验专业数据

        Args:
            data: 专业数据

        Returns:
            (是否有效, 清洗后数据, 错误列表)
        """
        errors = []
        cleaned = {}

        # 专业名称（必填）
        name = self._clean_string(data.get("name"))
        if not name or len(name) < 2:
            errors.append("专业名称为空或过短")
        else:
            cleaned["name"] = name

        # 专业代码（必填）
        code = self._clean_string(data.get("code"))
        if not code:
            errors.append("专业代码为空")
        else:
            cleaned["code"] = code

        # 专业大类
        category = self._clean_string(data.get("category"))
        if category:
            cleaned["category"] = category

        # 专业小类
        sub_category = self._clean_string(data.get("sub_category"))
        if sub_category:
            cleaned["sub_category"] = sub_category

        # 选科要求
        subject_req = self._clean_string(data.get("subject_requirements"))
        if subject_req:
            cleaned["subject_requirements"] = subject_req

        # 学制
        duration = data.get("duration")
        if duration is not None:
            cleaned["duration"] = self._clean_int(duration)

        # 学位
        degree = self._clean_string(data.get("degree"))
        if degree:
            cleaned["degree"] = degree

        # 简介
        description = self._clean_string(data.get("description"))
        if description:
            cleaned["description"] = description

        # 就业方向
        employment = self._clean_string(data.get("employment_direction"))
        if employment:
            cleaned["employment_direction"] = employment

        # 状态
        cleaned["status"] = 1

        return len(errors) == 0, cleaned, errors

    def validate_admission(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        校验录取数据

        Args:
            data: 录取数据

        Returns:
            (是否有效, 清洗后数据, 错误列表)
        """
        errors = []
        cleaned = {}

        # 学校ID或学校名称（必填其一）
        school_id = data.get("school_id")
        school_name = self._clean_string(data.get("school_name"))
        if not school_id and not school_name:
            errors.append("学校ID和学校名称均为空")
        if school_id:
            cleaned["school_id"] = self._clean_int(school_id)
        if school_name:
            cleaned["school_name"] = school_name

        # 专业ID或专业名称（可选）
        major_id = data.get("major_id")
        major_name = self._clean_string(data.get("major_name"))
        if major_id:
            cleaned["major_id"] = self._clean_int(major_id)
        if major_name:
            cleaned["major_name"] = major_name

        # 年份（必填）
        year = self._clean_int(data.get("year"))
        if not year or year < 2000 or year > 2030:
            errors.append(f"年份无效: {data.get('year')}")
        else:
            cleaned["year"] = year

        # 省份ID（必填）
        province_id = data.get("province_id")
        if province_id is not None:
            cleaned["province_id"] = self._clean_int(province_id)
        if not cleaned.get("province_id"):
            errors.append("省份ID为空")

        # 科类（必填）
        subject_type = data.get("subject_type")
        if subject_type is not None:
            cleaned["subject_type"] = self._clean_int(subject_type)
        if not cleaned.get("subject_type"):
            errors.append("科类为空")

        # 批次
        batch = self._clean_string(data.get("batch"))
        if batch:
            cleaned["batch"] = batch

        # 分数
        min_score = self._clean_int(data.get("min_score"))
        max_score = self._clean_int(data.get("max_score"))
        avg_score = self._clean_float(data.get("avg_score"))
        min_ranking = self._clean_int(data.get("min_ranking"))

        if min_score is not None:
            cleaned["min_score"] = min_score
        if max_score is not None:
            cleaned["max_score"] = max_score
        if avg_score is not None:
            cleaned["avg_score"] = avg_score
        if min_ranking is not None:
            cleaned["min_ranking"] = min_ranking

        # 至少有最低分或最低位次
        if not cleaned.get("min_score") and not cleaned.get("min_ranking"):
            errors.append("最低分和最低位次均为空")

        # 招生人数
        plan_count = self._clean_int(data.get("plan_count"))
        enroll_count = self._clean_int(data.get("enroll_count"))
        if plan_count is not None:
            cleaned["plan_count"] = plan_count
        if enroll_count is not None:
            cleaned["enroll_count"] = enroll_count

        return len(errors) == 0, cleaned, errors

    def validate_plan(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        校验招生计划数据

        Args:
            data: 招生计划数据

        Returns:
            (是否有效, 清洗后数据, 错误列表)
        """
        errors = []
        cleaned = {}

        # 学校ID或学校名称（必填其一）
        school_id = data.get("school_id")
        school_name = self._clean_string(data.get("school_name"))
        if not school_id and not school_name:
            errors.append("学校ID和学校名称均为空")
        if school_id:
            cleaned["school_id"] = self._clean_int(school_id)
        if school_name:
            cleaned["school_name"] = school_name

        # 专业ID或专业名称（可选）
        major_id = data.get("major_id")
        major_name = self._clean_string(data.get("major_name"))
        if major_id:
            cleaned["major_id"] = self._clean_int(major_id)
        if major_name:
            cleaned["major_name"] = major_name

        # 年份（必填）
        year = self._clean_int(data.get("year"))
        if not year or year < 2000 or year > 2030:
            errors.append(f"年份无效: {data.get('year')}")
        else:
            cleaned["year"] = year

        # 省份ID（必填）
        province_id = data.get("province_id")
        if province_id is not None:
            cleaned["province_id"] = self._clean_int(province_id)
        if not cleaned.get("province_id"):
            errors.append("省份ID为空")

        # 科类（必填）
        subject_type = data.get("subject_type")
        if subject_type is not None:
            cleaned["subject_type"] = self._clean_int(subject_type)
        if not cleaned.get("subject_type"):
            errors.append("科类为空")

        # 批次
        batch = self._clean_string(data.get("batch"))
        if batch:
            cleaned["batch"] = batch

        # 招生人数
        plan_count = self._clean_int(data.get("plan_count"))
        if plan_count is not None:
            cleaned["plan_count"] = plan_count

        # 学制
        duration = self._clean_int(data.get("duration"))
        if duration is not None:
            cleaned["duration"] = duration

        # 学费
        tuition = self._clean_float(data.get("tuition"))
        if tuition is not None:
            cleaned["tuition"] = tuition

        # 备注
        remark = self._clean_string(data.get("remark"))
        if remark:
            cleaned["remark"] = remark

        return len(errors) == 0, cleaned, errors

    def _clean_string(self, value: Any) -> Optional[str]:
        """清洗字符串"""
        if value is None:
            return None
        val = str(value).strip()
        val = re.sub(r'\s+', ' ', val)
        return val if val else None

    def _clean_int(self, value: Any) -> Optional[int]:
        """清洗整数"""
        if value is None:
            return None
        try:
            val_str = str(value).strip().replace(",", "")
            match = re.search(r'-?\d+', val_str)
            if match:
                return int(match.group())
        except Exception:
            pass
        return None

    def _clean_float(self, value: Any) -> Optional[float]:
        """清洗浮点数"""
        if value is None:
            return None
        try:
            val_str = str(value).strip().replace(",", "")
            match = re.search(r'-?\d+\.?\d*', val_str)
            if match:
                return float(match.group())
        except Exception:
            pass
        return None

    def _clean_bool(self, value: Any) -> int:
        """清洗布尔值"""
        if value is None:
            return 0
        val_str = str(value).strip().lower()
        if val_str in ("1", "true", "是", "yes", "y"):
            return 1
        return 0

    def _clean_url(self, value: Any) -> Optional[str]:
        """清洗URL"""
        if value is None:
            return None
        val = str(value).strip()
        if not val:
            return None
        if not val.startswith("http"):
            val = "http://" + val
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if re.match(pattern, val, re.IGNORECASE):
            return val
        return None


# 全局实例
validator = Validator()
