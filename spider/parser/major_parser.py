"""
专业数据解析器
负责清洗和标准化专业数据
"""
import re
from typing import List, Dict, Any, Optional

from parser.base import BaseParser
from utils.data_cleaner import data_cleaner


class MajorParser(BaseParser):
    """专业数据解析器"""

    # 学制映射
    DURATION_MAP = {
        "三年": 3, "3年": 3,
        "四年": 4, "4年": 4,
        "五年": 5, "5年": 5,
        "六年": 6, "6年": 6,
        "七年": 7, "7年": 7,
        "八年": 8, "8年": 8,
    }

    # 专业大类映射（教育部13个学科门类）
    CATEGORY_MAP = {
        "哲学": "01", "经济学": "02", "法学": "03", "教育学": "04",
        "文学": "05", "历史学": "06", "理学": "07", "工学": "08",
        "农学": "09", "医学": "10", "管理学": "11", "艺术学": "12",
        "交叉学科": "13",
    }

    def __init__(self):
        super().__init__(name="major_parser")

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析HTML内容（本模块主要处理JSON，此方法备用）"""
        return []

    def parse_single(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析单条专业数据

        Args:
            raw_data: 原始数据字典

        Returns:
            清洗后的数据字典，无效数据返回None
        """
        try:
            name = self._extract_name(raw_data)
            if not name:
                return None

            code = self._extract_code(raw_data)
            category = self._extract_category(raw_data)
            sub_category = self._extract_sub_category(raw_data)
            duration = self._extract_duration(raw_data)
            degree = self._extract_degree(raw_data)
            subject_req = self._extract_subject_requirements(raw_data)
            description = self._extract_description(raw_data)
            employment = self._extract_employment(raw_data)

            result = {
                "name": name,
                "code": code,
                "category": category,
                "sub_category": sub_category,
                "subject_requirements": subject_req,
                "duration": duration,
                "degree": degree,
                "description": description,
                "employment_direction": employment,
                "status": 1,
            }

            return result

        except Exception as e:
            self.logger.error(f"解析专业数据失败: {e}")
            return None

    def _extract_name(self, data: Dict) -> Optional[str]:
        """提取专业名称"""
        for key in ["name", "major_name", "title", "专业名称", "专业"]:
            if key in data and data[key]:
                name = str(data[key]).strip()
                name = re.sub(r'\s+', '', name)
                return name if len(name) >= 2 else None
        return None

    def _extract_code(self, data: Dict) -> Optional[str]:
        """提取专业代码"""
        for key in ["code", "major_code", "专业代码"]:
            if key in data and data[key]:
                code = str(data[key]).strip()
                return code if code else None
        return None

    def _extract_category(self, data: Dict) -> Optional[str]:
        """提取所属门类（专业大类）"""
        for key in ["category", "major_category", "category_name", "门类", "学科门类", "所属门类"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                return val
        return None

    def _extract_sub_category(self, data: Dict) -> Optional[str]:
        """提取所属学科（专业小类）"""
        for key in ["sub_category", "major_sub_category", "discipline", "学科", "所属学科", "专业类"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                return val
        return None

    def _extract_duration(self, data: Dict) -> Optional[int]:
        """提取学制"""
        for key in ["duration", "years", "学制"]:
            if key in data and data[key]:
                val = data[key]
                if isinstance(val, int):
                    return val if 1 <= val <= 10 else None
                val_str = str(val).strip()
                if val_str.isdigit():
                    d = int(val_str)
                    return d if 1 <= d <= 10 else None
                return self.DURATION_MAP.get(val_str)
        return None

    def _extract_degree(self, data: Dict) -> Optional[str]:
        """提取授予学位"""
        for key in ["degree", "degree_name", "授予学位", "学位"]:
            if key in data and data[key]:
                return str(data[key]).strip()
        return None

    def _extract_subject_requirements(self, data: Dict) -> Optional[str]:
        """提取选科要求"""
        for key in ["subject_requirements", "subject_req", "requirement", "选科要求", "选考科目"]:
            if key in data and data[key]:
                return data_cleaner.clean_string(str(data[key]))
        return None

    def _extract_description(self, data: Dict) -> Optional[str]:
        """提取专业介绍"""
        for key in ["description", "intro", "summary", "专业介绍", "简介"]:
            if key in data and data[key]:
                return data_cleaner.clean_string(str(data[key]))
        return None

    def _extract_employment(self, data: Dict) -> Optional[str]:
        """提取就业方向"""
        for key in ["employment", "employment_direction", "career", "就业方向", "就业"]:
            if key in data and data[key]:
                return data_cleaner.clean_string(str(data[key]))
        return None
