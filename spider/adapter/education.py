"""
教育部数据适配器
数据来源：教育部官方网站
"""
import json
from typing import List, Dict, Any, Optional

from adapter.base import BaseAdapter
from config.sources import EDUCATION_SOURCES


class EducationAdapter(BaseAdapter):
    """教育部数据适配器"""

    name = "education"
    priority = 10  # 最高优先级

    def fetch_school_list(self, **kwargs) -> List[Dict[str, Any]]:
        """从教育部获取高校名单"""
        url = EDUCATION_SOURCES.get("school_list_api")
        if not url:
            return []

        all_schools = []
        for page in range(1, 200):
            try:
                params = {"page": page, "size": 50}
                data = self.fetch_json(url, params=params)

                if not data:
                    break

                school_list = data.get("data", {}).get("list", [])
                if not school_list:
                    break

                all_schools.extend(school_list)

                if len(school_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"[{self.name}] 第 {page} 页获取失败: {e}")
                break

        return all_schools

    def fetch_major_list(self, **kwargs) -> List[Dict[str, Any]]:
        """教育部暂不提供专业列表API"""
        return []

    def fetch_admission_scores(self, year: int, province_id: int, **kwargs) -> List[Dict[str, Any]]:
        """教育部暂不提供录取分数线API"""
        return []
