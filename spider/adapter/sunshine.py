"""
阳光高考平台数据适配器
数据来源：阳光高考平台（gaokao.chsi.com.cn）
"""
import json
from typing import List, Dict, Any, Optional

from adapter.base import BaseAdapter
from config.sources import SUNSHINE_SOURCES


class SunshineAdapter(BaseAdapter):
    """阳光高考平台数据适配器"""

    name = "sunshine"
    priority = 20  # 次优先级

    def fetch_school_list(self, **kwargs) -> List[Dict[str, Any]]:
        """从阳光高考获取高校列表"""
        url = SUNSHINE_SOURCES.get("api_school")
        if not url:
            return []

        all_schools = []
        for page in range(1, 200):
            try:
                params = {"page": page, "size": 50, "school_type": 0}
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
        """从阳光高考获取专业列表"""
        url = SUNSHINE_SOURCES.get("api_major")
        if not url:
            return []

        all_majors = []
        for page in range(1, 100):
            try:
                params = {"page": page, "size": 50}
                data = self.fetch_json(url, params=params)

                if not data:
                    break

                major_list = data.get("data", {}).get("list", [])
                if not major_list:
                    break

                all_majors.extend(major_list)

                if len(major_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"[{self.name}] 第 {page} 页获取失败: {e}")
                break

        return all_majors

    def fetch_admission_scores(self, year: int, province_id: int, **kwargs) -> List[Dict[str, Any]]:
        """从阳光高考获取录取分数线"""
        url = SUNSHINE_SOURCES.get("api_score")
        if not url:
            return []

        all_scores = []
        for page in range(1, 200):
            try:
                params = {
                    "year": year,
                    "province_id": province_id,
                    "page": page,
                    "size": 50,
                }
                data = self.fetch_json(url, params=params)

                if not data:
                    break

                score_list = data.get("data", {}).get("list", [])
                if not score_list:
                    break

                # 附加年份和省份信息
                for item in score_list:
                    item["_year"] = year
                    item["_province_id"] = province_id

                all_scores.extend(score_list)

                if len(score_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"[{self.name}] 第 {page} 页获取失败: {e}")
                break

        return all_scores
